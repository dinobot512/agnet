"""Parse Anthropic-format transcripts (JSONL) into a Trace.

Accepts two line shapes, mixed freely:
  - Claude Code / Agent SDK session lines: {"type": "user"|"assistant", "message": {...},
    "timestamp": ISO-8601, "uuid": ...}. Other line types (summary, system, ...) are skipped.
  - Plain Messages-API log lines: {"role": "user"|"assistant", "content": ..., "t": epoch}
    (what our own harness writes).

Turns: a new assistant message starts a new turn. Tool results belong to the turn whose calls
they answer; user prompts belong to the turn they prompt (the next one). Claude Code writes one
response as several lines sharing message.id; those stay in one turn.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from gleeb.schema import Agent, Event, ToolInfo, Trace


def _ts(line: dict) -> float:
    if isinstance(line.get("t"), (int, float)):
        return float(line["t"])
    ts = line.get("timestamp")
    if ts:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    return 0.0


def _message(line: dict) -> tuple[str, object, str, str] | None:
    """-> (role, content, message_id, ref) or None if the line is not a message."""
    if line.get("type") in ("user", "assistant") and isinstance(line.get("message"), dict):
        m = line["message"]
        return m.get("role", line["type"]), m.get("content", ""), m.get("id", ""), line.get("uuid", "")
    if line.get("role") in ("user", "assistant"):
        return line["role"], line.get("content", ""), line.get("id", ""), line.get("ref", "")
    return None


def _blocks(content) -> list[dict]:
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [b for b in content or [] if isinstance(b, dict)]


def _result_text(block: dict) -> str:
    """Model-visible tool result text (tool_result.content), never the UI-only field."""
    c = block.get("content", "")
    if isinstance(c, str):
        return c
    return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")


def parse_agent_file(path: str | Path, agent: str) -> list[Event]:
    """One agent's transcript -> events with per-agent order (seq assigned later by parse_run)."""
    events: list[Event] = []
    calls: dict[str, tuple[str, dict]] = {}     # call_id -> (tool name, args)
    turn, last_msg_id = -1, None

    for lineno, raw in enumerate(Path(path).read_text().splitlines(), 1):
        if not raw.strip():
            continue
        line = json.loads(raw)
        msg = _message(line)
        if msg is None:
            continue
        role, content, msg_id, uuid = msg
        t = _ts(line)
        ref = f"{Path(path).name}:{lineno}" + (f"#{uuid}" if uuid else "")

        def add(kind, text="", **kw):
            events.append(Event(seq=len(events), agent=agent, turn=kw.pop("turn", turn),
                                kind=kind, content=text, t=t, ref=ref, **kw))

        if role == "assistant":
            if not (msg_id and msg_id == last_msg_id):
                turn += 1
            last_msg_id = msg_id
            for b in _blocks(content):
                if b["type"] == "thinking" and b.get("thinking"):
                    add("reasoning", b["thinking"], source="thinking")
                elif b["type"] == "text" and b.get("text", "").strip():
                    add("text", b["text"], source="assistant_text")
                elif b["type"] == "tool_use":
                    name, args = b.get("name", ""), b.get("input", {}) or {}
                    calls[b.get("id", "")] = (name, args)
                    add("tool_call", json.dumps(args),
                        tool=ToolInfo(name, b.get("id", ""), args))
        else:
            last_msg_id = None
            for b in _blocks(content):
                if b["type"] == "tool_result":
                    call_id = b.get("tool_use_id", "")
                    name, args = calls.get(call_id, ("", {}))
                    text = _result_text(b)
                    add("tool_result", text,
                        tool=ToolInfo(name, call_id, args))
                elif b["type"] == "text" and b.get("text", "").strip():
                    add("message_in", b["text"], turn=turn + 1)
    return events


def parse_run(paths: dict[str, str | Path], trace_id: str = "",
              agents: dict[str, Agent] | None = None) -> Trace:
    """Several agents' transcripts -> one Trace with a global seq.

    Events are ordered by wall clock; ties keep the per-agent order, then the order of `paths`.
    """
    rank = {a: i for i, a in enumerate(paths)}
    merged = []
    for agent, p in paths.items():
        merged += parse_agent_file(p, agent)
    merged.sort(key=lambda e: (e.t, rank[e.agent], e.seq))
    events = [Event(**{**e.__dict__, "seq": i}) for i, e in enumerate(merged)]
    agents = agents or {a: Agent(a) for a in paths}
    return Trace(trace_id or "+".join(paths), agents, events)
