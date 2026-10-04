"""Parse sims/multi-agent transcripts (transcripts/<run>/agent_<name>.md) into a Trace.

Each agent turn ("# Turn @ <time>") holds a system prompt, an initial user message (instruction +
memory), then "## Step N @ <time>" sections with the response content and tool results as JSON
(Anthropic block format). Each step is one model response, i.e. one gleeb turn.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from gleeb.parsers.anthropic_jsonl import _blocks, _result_text
from gleeb.schema import Agent, Event, ToolInfo, Trace

_HEADER = re.compile(r"^(# Turn(?: \(\w*\))?(?: \[\w*\])? @ (?P<turn>\S+)|## Initial User Message|## Turn prompt|## Step \d+ @ (?P<step>\S+)|"
                     r"### Response content|### Tool results)\s*$", re.M)


def _json_after(text: str):
    start = text.index("```json") + len("```json")
    return json.JSONDecoder().raw_decode(text[start:].lstrip())[0]


def _fenced(text: str) -> str:
    """Body of the first ``` fence in a section (to the section's last fence)."""
    body = text.split("```", 1)[1] if "```" in text else text
    body = body.split("\n", 1)[1] if "\n" in body else body
    return body.rsplit("```", 1)[0].strip()


def parse_sim_file(path: str | Path, agent: str) -> list[Event]:
    text = Path(path).read_text()
    marks = list(_HEADER.finditer(text))
    events: list[Event] = []
    turn, t = -1, 0.0
    calls: dict[str, tuple[str, dict]] = {}
    for i, m in enumerate(marks):
        body = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        ref = f"{Path(path).name}:{text.count(chr(10), 0, m.start()) + 1}"
        head = m.group(1)
        if m.group("turn") or m.group("step"):
            t = datetime.fromisoformat(m.group("turn") or m.group("step")).timestamp()
            if m.group("step"):
                turn += 1
            continue

        def add(kind, content="", **kw):
            events.append(Event(len(events), agent, kw.pop("turn", turn), kind, content, t, ref=ref, **kw))

        if head in ("## Initial User Message", "## Turn prompt"):
            add("message_in", _fenced(body), turn=turn + 1)
        elif head == "### Response content":
            for b in _blocks(_json_after(body)):
                if b.get("type") == "thinking" and b.get("thinking"):
                    add("reasoning", b["thinking"], source="thinking")
                elif b.get("type") == "text" and b.get("text", "").strip():
                    add("text", b["text"], source="assistant_text")
                elif b.get("type") == "tool_use":
                    calls[b["id"]] = (b["name"], b.get("input") or {})
                    add("tool_call", json.dumps(b.get("input") or {}), tool=ToolInfo(b["name"], b["id"], b.get("input") or {}))
        elif head == "### Tool results":
            for b in _blocks(_json_after(body)):
                if b.get("type") == "tool_result":
                    name, args = calls.get(b["tool_use_id"], ("", {}))
                    add("tool_result", _result_text(b), tool=ToolInfo(name, b["tool_use_id"], args))
    return events


def parse_sim_run(transcript_dir: str | Path, order: list[str] | None = None) -> Trace:
    """All agent_<name>.md files in a run directory -> one Trace. `order` = the sim's round order
    (config agent order), used to break same-second ties; defaults to sorted names."""
    d = Path(transcript_dir)
    files = {p.stem.removeprefix("agent_"): p for p in sorted(d.glob("agent_*.md"))}
    order = order or sorted(files)
    rank = {a: i for i, a in enumerate(order)}
    merged = [e for a in order for e in parse_sim_file(files[a], a)]
    merged.sort(key=lambda e: (e.t, rank[e.agent], e.seq))
    events = [Event(**{**e.__dict__, "seq": i}) for i, e in enumerate(merged)]
    return Trace(d.name, {a: Agent(a, name=f"Agent {a.upper()}") for a in order}, events)
