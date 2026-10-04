"""Tool-call classification: rules, cwd tracking, Edit application, id resolution, LLM fallback."""

import json
from types import SimpleNamespace as NS

from gleeb import Event, ToolInfo, Trace
from gleeb.flow import flow_edges
from gleeb.llm import LLM
from gleeb.ops import classify_ops, content_id


def make_trace(calls):
    """calls: [(agent, tool, args, result)] -> Trace with paired tool_call/tool_result events."""
    events = []
    for i, (agent, tool, args, result) in enumerate(calls):
        events.append(Event(2 * i, agent, i, "tool_call", tool=ToolInfo(tool, f"c{i}", args)))
        events.append(Event(2 * i + 1, agent, i, "tool_result", result, tool=ToolInfo(tool, f"c{i}", args)))
    return Trace("t", {}, events)


def test_rules_cwd_edit_and_resolve():
    tr = make_trace([
        ("sam", "Write", {"file_path": "/work/guide.md", "content": "Welcome adults to the park."}, "ok"),
        ("sam", "Bash", {"command": "cd /work && cat guide.md"}, "Welcome adults to the park."),
        ("sam", "Edit", {"file_path": "guide.md", "old_string": "adults", "new_string": "kids"}, "ok"),
        ("sam", "Bash", {"command": "ls -la"}, "guide.md"),
    ])
    ops, notes = classify_ops(tr)
    assert notes == []
    assert [(o.op, o.blackboard_id, o.seq) for o in ops] == [
        ("W", "file:/work/guide.md", 0), ("R", "file:/work/guide.md", 3), ("W", "file:/work/guide.md", 4)]
    assert ops[2].content == "Welcome kids to the park."        # Edit applied to last known content
    assert ops[0].content_id == ops[1].content_id                # same content written then read


def test_resolve_absolute_to_relative():
    tr = make_trace([("a", "Write", {"file_path": "/workspace/notes.md", "content": "x"}, "ok"),
                     ("b", "Read", {"file_path": "notes.md"}, "     1\tx")])
    ops, _ = classify_ops(tr)
    assert {o.blackboard_id for o in ops} == {"file:notes.md"}
    assert ops[0].content_id == ops[1].content_id == content_id("x")   # line numbers stripped


def test_llm_fallback_for_complex_bash(tmp_path):
    class Fake:
        def create(self, **kw):
            self.user = kw["messages"][0]["content"]
            out = {"ops": [{"op": "R", "blackboard": "file:brief.md", "content_from": "result", "written_text": "",
                            "confidence": 0.9},
                           {"op": "W", "blackboard": "file:notes.txt", "content_from": "args",
                            "written_text": "venue: Okonkwo Boathouse on Wharf Lane", "confidence": 0.7}]}
            return NS(stop_reason="end_turn", model=kw["model"], content=[NS(type="text", text=json.dumps(out))],
                      usage=NS(input_tokens=10, output_tokens=5))
    fake = Fake()
    llm = LLM(cache_dir=tmp_path, client=NS(beta=NS(messages=fake)))
    tr = make_trace([
        ("priya", "Bash", {"command": "grep venue brief.md | tee notes.txt"}, "venue: Okonkwo Boathouse on Wharf Lane"),
        ("tomas", "Read", {"file_path": "notes.txt"}, "venue: Okonkwo Boathouse on Wharf Lane"),
    ])
    assert classify_ops(tr)[1]                                  # without an llm: reported, skipped
    ops, notes = classify_ops(tr, llm)
    assert notes == [] and "Result:" in fake.user
    assert [(o.op, o.blackboard_id, o.source) for o in ops] == [
        ("R", "file:brief.md", "llm"), ("W", "file:notes.txt", "llm"), ("R", "file:notes.txt", "rule")]
    edges = flow_edges(ops, tr)
    assert {(e.kind, e.from_agent, e.blackboard_id, e.to_agent, e.to_blackboard) for e in edges} == {
        ("transfer", "?", "file:brief.md", "priya", ""),
        ("carry", "priya", "file:brief.md", "priya", "file:notes.txt"),    # same call: grep | tee
        ("transfer", "priya", "file:notes.txt", "tomas", "")}


def test_fragment_carry_background_and_unexplained():
    from gleeb.flow import background_from
    brief = "Millbrook Park is closed for flood repairs. The festival moves to the Okonkwo Boathouse; " \
            "the public entrance is Gate 37 on Wharf Lane."
    tr = make_trace([
        ("priya", "Read", {"file_path": "brief_A.md"}, brief),
        ("priya", "send_dm", {"to": "tomas", "message": "Update: the public entrance is Gate 37 on Wharf Lane now."}, "sent"),
        ("tomas", "read_dms", {}, "From priya: Update: the public entrance is Gate 37 on Wharf Lane now."),
        ("tomas", "Write", {"file_path": "handoff.md", "content": "Entrance: the public entrance is Gate 37 on Wharf Lane."}, "ok"),
        # mei never read handoff.md or any DM, yet writes priya's wording: unexplained
        ("mei", "Write", {"file_path": "signs.md", "content": "ENTRANCE: the public entrance is Gate 37 on Wharf Lane"}, "ok"),
    ])
    ops, _ = classify_ops(tr)
    edges = flow_edges(ops, tr)
    kinds = {(e.kind, e.match, e.from_agent, e.to_agent, e.to_blackboard) for e in edges}
    assert ("carry", "fragment", "priya", "priya", "dm:inbox:tomas") in kinds
    assert ("transfer", "exact_copy", "priya", "tomas", "") in kinds
    assert ("carry", "fragment", "tomas", "tomas", "file:handoff.md") in kinds
    assert any(k[0] == "unexplained" and k[3] == "mei" for k in kinds)
    assert ("transfer", "unknown", "?", "priya", "") in kinds        # the brief's source is unobserved
    assert not any(e.match == "unknown" and e.to_agent == "tomas" for e in edges)   # DM fully explained
    # the same phrasing seen in a background (e.g. control) run is not evidence
    bg = background_from(ops)
    assert not [e for e in flow_edges(ops, tr, bg) if e.match == "fragment"]
