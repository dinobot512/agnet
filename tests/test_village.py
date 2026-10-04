"""Village parser on a tiny synthetic export (no real data, no API calls)."""

import gzip
import json

from gleeb.parsers import parse_village


def _w(p, name, rows):
    with gzip.open(p / f"{name}.jsonl.gz", "wt") as f:
        f.write("\n".join(json.dumps(r) for r in rows))


def test_village(tmp_path):
    ag = lambda i, n: {"id": i, "name": n, "model_string": n.lower(), "created_at": "2026-01-01 00:00:00"}
    _w(tmp_path, "agents", [ag("a1", "Alpha"), ag("b2", "Beta")])
    _w(tmp_path, "chat_rooms", [{"id": "r1", "name": "general"}, {"id": "r2", "name": "focus"}])
    ev = lambda i, ts, **d: {"event_index": i, "created_at": ts, "data": d}
    _w(tmp_path, "events", [
        ev(2, "2026-08-01 10:01:00", actionType="AGENT_TALK", speakerId="a1", roomId="r1", content="secret is 42",
           output=[{"type": "reasoning", "summary": [{"text": "plan to share"}]}]),
        ev(1, "2026-08-01 10:00:00", actionType="ENTER_ROOM", agentId="b2", roomId="r2", roomName="focus",
           currentRooms="#general: Alpha; #focus: Beta"),
        ev(3, "2026-08-01 10:02:00", actionType="AGENT_TALK", speakerId="b2", roomId="r2", content="unheard"),
        ev(4, "2026-08-01 10:03:00", actionType="ENTER_ROOM", agentId="b2", roomId="r1", roomName="general",
           currentRooms="#general: Alpha, Beta"),
        ev(5, "2026-08-01 10:04:00", actionType="AGENT_TALK", speakerId="a1", roomId="r1", content="hello again"),
        ev(6, "2026-08-01 10:05:00", actionType="WAIT", agentId="b2"),
        ev(7, "2026-09-01 00:00:00", actionType="WAIT", agentId="a1"),     # outside window
    ])
    tr = parse_village(tmp_path, "2026-08-01", "2026-08-02")
    assert set(tr.agents) == {"alpha", "beta"}
    assert [e.seq for e in tr.events] == list(range(len(tr.events)))
    first = [e for e in tr.events if e.agent == "alpha"][:2]
    assert first[0].kind == "reasoning" and first[0].content == "plan to share"
    assert first[1].tool.name == "send_message_to_chat" and first[1].tool.args["message"] == "secret is 42"
    # Beta was in #focus for the first message (no delivery), then moved to #general
    inbox = [e.content for e in tr.events if e.agent == "beta" and e.kind == "message_in"]
    assert inbox == ["[#general] Alpha: hello again"]
    assert not any(e.tool and e.tool.name == "wait" and e.agent == "alpha" for e in tr.events)


def test_village_ops_rules(tmp_path):
    from gleeb.flow import flow_edges
    from gleeb.ops import classify_ops
    test_village(tmp_path)
    tr = parse_village(tmp_path, "2026-08-01", "2026-08-02")
    ops, notes = classify_ops(tr, None)               # no llm: every Village call must be rule-handled
    assert notes == []
    assert [(o.agent, o.op, o.blackboard_id) for o in ops if o.agent == "alpha"] == [
        ("alpha", "W", "board:general"), ("alpha", "W", "board:general")]
    assert [(o.agent, o.op, o.blackboard_id, o.content) for o in ops if o.agent == "beta"] == [
        ("beta", "W", "board:focus", "unheard"), ("beta", "R", "board:general", "hello again")]
    assert any(e.from_agent == "alpha" and e.to_agent == "beta" for e in flow_edges(ops, tr))
