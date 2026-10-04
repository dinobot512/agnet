"""End-to-end tests on a two-agent fixture (priya DMs tomas, tomas writes invite.md). No API calls."""

import json
import re
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

from gleeb import BlackboardUniverse, DMThread, GoalSpan, GoalStream, io
from gleeb.align import align, noise_floor
from gleeb.flow import flow_edges
from gleeb.ops import classify_ops
from gleeb.goals import METHODS, STREAMS, run_monitor, validate, select
from gleeb.llm import LLM
from gleeb.parsers import parse_run
from gleeb.score import boundary_hit, run_e1, score, tables

FIX = Path(__file__).parent / "fixtures"


@pytest.fixture
def trace():
    return parse_run({"priya": FIX / "priya.jsonl", "tomas": FIX / "tomas.jsonl"})


class FakeMessages:
    """Answers each request type deterministically from the items it is shown."""
    def __init__(self):
        self.calls = 0

    def create(self, **kw):
        self.calls += 1
        props = kw["output_config"]["format"]["schema"]["properties"]
        user = kw["messages"][0]["content"]
        ids = [int(x) for x in re.findall(r"^\[(\d+)\]", user, re.M)]
        goal = "tell Tomas the new venue" if "Okonkwo" in user else "read the brief"
        if "verdict" in props:
            a, b = re.findall(r"Goal [AB]: (.*)", user)
            out = {"verdict": "same" if a == b else "different", "reason": "test"}
        elif "bullets" in props:
            out = {"bullets": [{"text": f"Did: handled events {ids}", "evidence": ids}]}
        elif "spans" in props:
            spans = [{"start_lo": ids[0], "start_hi": ids[0], "goal": "read the brief", "confidence": 0.9,
                      "evidence": [ids[0]]}]
            if len(ids) >= 3:
                spans.append({"start_lo": ids[1], "start_hi": ids[2], "goal": "tell Tomas the new venue",
                              "confidence": 0.8, "evidence": [ids[2]]})
            out = {"spans": spans}
        else:
            out = {"goal": goal, "confidence": 0.9, "evidence": ids[-1:]}
        return NS(stop_reason="end_turn", model=kw["model"],
                  content=[NS(type="text", text=json.dumps(out))], usage=NS(input_tokens=100, output_tokens=20))


@pytest.fixture
def llm(tmp_path):
    msgs = FakeMessages()
    return LLM(cache_dir=tmp_path / "cache", client=NS(beta=NS(messages=msgs)))


def test_parse(trace):
    kinds = [e.kind for e in trace.events]
    assert kinds.count("tool_call") == 4 and kinds.count("tool_result") == 2
    assert [e.seq for e in trace.events] == list(range(len(trace.events)))


def edges_of(trace):
    ops, notes = classify_ops(trace)
    assert notes == []
    return flow_edges(ops, trace)


def test_universe_and_flow(trace):
    ops, _ = classify_ops(trace)
    u = BlackboardUniverse.from_ops(ops)
    assert isinstance(u.boards["dm:inbox:tomas"], DMThread)
    assert u.contents[u.boards["file:invite.md"].entries[0].versions[0]] == "Join us at the Okonkwo Boathouse!"
    edges = edges_of(trace)
    assert [(e.kind, e.from_agent, e.blackboard_id, e.to_agent) for e in edges] == [
        ("transfer", "?", "file:brief_A.md", "priya"),           # nobody observed writing the brief
        ("carry", "priya", "file:brief_A.md", "priya"),          # brief -> priya's DM
        ("transfer", "priya", "dm:inbox:tomas", "tomas")]


@pytest.mark.parametrize("stream", list(STREAMS))
@pytest.mark.parametrize("method", METHODS)
def test_monitor_partitions_stream(trace, llm, stream, method):
    s = run_monitor(trace, "priya", stream, method, llm, window=2, overlap=1, chunk=2)
    seqs = [e.seq for e in select(trace, "priya", stream)]
    assert s.spans, s.notes
    assert validate(s.spans, seqs) == []
    assert s.spans[0].start[0] == seqs[0] and s.spans[-1].end[1] == seqs[-1]
    assert s.meta["tokens"]["input"] > 0 and s.method == method


def test_samples_cached_separately(trace, llm):
    a = run_monitor(trace, "priya", "all", "whole", llm, sample_id=0)
    n = llm.client.beta.messages.calls
    run_monitor(trace, "priya", "all", "whole", llm, sample_id=0)
    assert llm.client.beta.messages.calls == n                  # same sample: cached
    run_monitor(trace, "priya", "all", "whole", llm, sample_id=1)
    assert llm.client.beta.messages.calls == n + 1              # new sample: new call
    assert noise_floor([a, a], llm)["boundary_disagreement"] == 0


def test_align_and_e1_tables(trace, llm):
    ex = run_monitor(trace, "priya", "expressed", "whole", llm)
    be = run_monitor(trace, "priya", "behavioral", "whole", llm)
    al = align(ex, be, llm)
    assert al.matches and al.a == ex.id
    truth = {"markers": ["Okonkwo Boathouse"]}
    rows, produced = run_e1({("treatment", 0): trace, ("control", 0): trace}, "priya", truth, llm, k=2,
                            window=2, overlap=1, chunk=2)
    assert len(rows) == 2 * len(STREAMS) * len(METHODS) and produced
    md = tables(rows)
    assert "### hit_rate" in md and "| expressed |" in md


def test_score(trace):
    edges = edges_of(trace)
    stream = GoalStream("tomas", "behavioral", "whole", "x", spans=[
        GoalSpan("a", "tomas", "behavioral", (7, 7), (7, 7), "read DMs"),
        GoalSpan("b", "tomas", "behavioral", (8, 9), (9, 9), "write the invite")])
    truth = {"injections": [{"id": "I1", "agent": "tomas", "markers": ["Okonkwo Boathouse"]}],
             "expected_edges": [["priya", "dm:inbox:tomas", "tomas"]]}
    out = score(trace, [stream], edges, truth)
    assert out["markers"]["Okonkwo Boathouse"] == {"priya": "reached", "tomas": "reached"}
    assert out["edges"]["recall"] == 1.0
    assert out["goal_change"][f"I1:{stream.id}"]["hit"] is True
    assert boundary_hit(trace, stream, 8)["width"] == 2


def test_io_roundtrip(trace, llm, tmp_path):
    s = run_monitor(trace, "priya", "all", "whole", llm)
    ops, _ = classify_ops(trace)
    for obj in (trace, ops, BlackboardUniverse.from_ops(ops), flow_edges(ops, trace), [s]):
        p = io.save(obj, tmp_path / "x.json.gz")
        assert io.load(p) == obj
