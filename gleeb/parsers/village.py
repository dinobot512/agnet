"""Parse an AI Village export (events/agents/chat_rooms .jsonl.gz) into a Trace.

One Village event (`event_index`) is one agent decision, i.e. one gleeb turn. Mapping:
  AGENT_TALK            tool_call send_message_to_chat {room, message}; the raw model output gives reasoning
  USER_TALK / others'   message_in "[#room] speaker: text", delivered at the start of each present agent's
    AGENT_TALK          next turn (presence tracked from ENTER_ROOM and its `currentRooms` snapshots)
  SEARCH_HISTORY        tool_call search_history {query} + tool_result (answer written by another LLM)
  CONSOLIDATE           tool_call consolidate {nextSessionGoal}
  WAIT / PAUSE          tool_call wait / pause {seconds}
  START/STOP_USING_COMPUTER, ENTER_ROOM, OUTREACH_*, *_HUMAN_*  tool_call named after the action
  OUTREACH_APPROVAL_RESPONSE  message_in from the gatekeeper
Reasoning is whatever is readable in `output` (Anthropic thinking, OpenAI summaries, Gemini thought
parts); encrypted reasoning is dropped. The export has no turns/tool results, so work done inside
computer-use sessions is invisible: only session goals and summaries appear.
Agent ids are slugs of the agent name (uuid in Agent.meta["uuid"]).
"""

from __future__ import annotations

import ast
import gzip
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from gleeb.schema import Agent, Event, ToolInfo, Trace

DEFAULT_ROOM = "general"
_SKIP = {"USER_NAME_CHANGE"}
_TOOL = {
    "AGENT_TALK": "send_message_to_chat", "CONSOLIDATE": "consolidate", "WAIT": "wait", "PAUSE": "pause",
    "SEARCH_HISTORY": "search_history", "START_USING_COMPUTER": "start_using_computer",
    "STOP_USING_COMPUTER": "stop_using_computer", "ENTER_ROOM": "enter_room",
    "OUTREACH_APPROVAL_REQUEST": "request_outreach_approval", "REQUEST_HUMAN_HELPER": "request_human_helper",
    "CANCEL_REQUEST_FOR_HUMAN_HELPER": "cancel_human_helper_request",
    "STOP_HUMAN_USE_SESSION": "stop_human_use_session", "REQUEST_GOOGLE_SIGN_IN": "request_google_sign_in",
    "RESTARTING_AFTER_GOOGLE_SIGN_IN": "restart_after_google_sign_in",
}
_NOISE = {"cost", "output", "inputTokens", "outputTokens", "actionType", "agentId", "roomId", "speakerId",
          "messageId", "chatMessageId", "speakerType", "currentRooms", "previousRoomId", "answerToQuery",
          "computerUseSessionId", "outreachApprovalRequestId", "humanUseSessionRequestId"}


def _load(path: Path) -> list[dict]:
    with gzip.open(path, "rt") as f:
        return [json.loads(l) for l in f]


def _ts(s: str) -> float:
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp()


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _parse_output(o):
    if isinstance(o, str):
        for f in (json.loads, ast.literal_eval):
            try:
                return f(o)
            except Exception:
                pass
        return None
    return o


def reasoning_of(o) -> str:
    """Readable reasoning in a provider-shaped raw output ('' if none or only encrypted)."""
    parts: list[str] = []

    def walk(x):
        if isinstance(x, dict):
            t = x.get("type")
            if t == "thinking" and isinstance(x.get("thinking"), str):
                parts.append(x["thinking"])
            elif t == "reasoning" and isinstance(x.get("summary"), list):
                parts.extend(s.get("text", "") for s in x["summary"] if isinstance(s, dict))
            elif x.get("thought") is True and isinstance(x.get("text"), str):
                parts.append(x["text"])
            for k in ("reasoning", "reasoning_content"):
                if isinstance(x.get(k), str):
                    parts.append(x[k])
            for v in x.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(_parse_output(o))
    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def _snapshot(text: str) -> dict[str, list[str]]:
    """'#general: A, B; #focus: C; #best, #rest: (empty)' -> {room: [agent names]}."""
    out: dict[str, list[str]] = {}
    for part in text.split("; "):
        rooms, _, names = part.partition(": ")
        names = [] if names.strip() == "(empty)" else [n.strip() for n in names.split(", ") if n.strip()]
        for r in rooms.split(", "):
            out[r.strip().lstrip("#")] = names
    return out


def parse_village(src: str | Path, start: str = "", end: str = "",
                  agents: list[str] | None = None, rooms: list[str] | None = None) -> Trace:
    """Village export directory -> Trace of events with start <= created_at < end (UTC, 'YYYY-MM-DD[ HH:MM]').

    agents: names or slugs to keep as trace agents (default all that act in the window).
    rooms:  keep only chat in these room names (default all). Presence is always tracked over the full export.
    """
    src = Path(src)
    ag_rows = _load(src / "agents.jsonl.gz")
    room_name = {r["id"]: r["name"] for r in _load(src / "chat_rooms.jsonl.gz")}
    by_uuid = {a["id"]: a for a in ag_rows}
    slug = {a["id"]: _slug(a["name"]) for a in ag_rows}
    by_name = {a["name"]: a["id"] for a in ag_rows}
    keep = {_slug(a) for a in agents} if agents else None
    keep_rooms = set(rooms) if rooms else None
    where: dict[str, str] = {}            # agent uuid -> room name (default #general)
    inbox: dict[str, list[str]] = defaultdict(list)
    turn_of: dict[str, int] = defaultdict(int)
    events: list[Event] = []
    seen: set[str] = set()

    def emit(agent, turn, kind, content, t, ref, tool=None, source=None):
        events.append(Event(len(events), agent, turn, kind, content, t, tool=tool, source=source, ref=ref))
        seen.add(agent)

    rows = sorted(_load(src / "events.jsonl.gz"), key=lambda e: e["event_index"])
    lo, hi = (_ts(start) if start else float("-inf")), (_ts(end) if end else float("inf"))
    for e in rows:
        d, t, ref = e["data"], _ts(e["created_at"]), f"events.jsonl.gz#{e['event_index']}"
        act = d.get("actionType")
        if act in _SKIP or act is None:
            continue
        uid = d.get("speakerId") if act == "AGENT_TALK" else d.get("agentId")
        in_window = lo <= t < hi

        if act == "ENTER_ROOM":
            for r, names in _snapshot(d.get("currentRooms", "")).items():
                for n in names:
                    if n in by_name:
                        where[by_name[n]] = r
            where[uid] = d.get("roomName", DEFAULT_ROOM)

        room = room_name.get(d.get("roomId"), d.get("roomId") or "")
        if act in ("AGENT_TALK", "USER_TALK"):
            who = by_uuid[uid]["name"] if act == "AGENT_TALK" else d.get("speakerName", "human")
            if act == "USER_TALK" and not d.get("hasBeenApproved", True):
                continue
            if in_window and (keep_rooms is None or room in keep_rooms):
                for other in by_uuid:
                    if other != uid and where.get(other, DEFAULT_ROOM) == room:
                        inbox[other].append(f"[#{room}] {who}: {d['content']}")
            if act == "USER_TALK":
                continue
        if act == "OUTREACH_APPROVAL_RESPONSE" and in_window:
            inbox[uid].append(f"[outreach {d.get('approval')}] to {d.get('recipient')} via {d.get('medium')}"
                              + (f": {d['adminComment']}" if d.get("adminComment") else ""))
            continue
        if not in_window or uid not in by_uuid or (keep and slug[uid] not in keep):
            continue
        if act == "AGENT_TALK" and keep_rooms is not None and room not in keep_rooms:
            continue

        a, turn = slug[uid], turn_of[uid]
        turn_of[uid] += 1
        if inbox[uid]:
            emit(a, turn, "message_in", "\n\n".join(inbox.pop(uid)), t, ref)
        if act == "START_USING_COMPUTER" and d.get("sessionGoal"):
            emit(a, turn, "message_in", f"[session goal] {d['sessionGoal']}", t, ref)
        r = reasoning_of(d.get("output")) if d.get("output") else ""
        if r:
            emit(a, turn, "reasoning", r, t, ref, source="thinking")

        name = _TOOL.get(act, act.lower())
        if act == "AGENT_TALK":
            args = {"room": room, "message": d["content"]}
        elif act == "ENTER_ROOM":
            args = {"room": d.get("roomName", "")}
        else:
            args = {k: v for k, v in d.items() if k not in _NOISE and v not in (None, "")}
        cid = f"v{e['event_index']}"
        emit(a, turn, "tool_call", json.dumps(args), t, ref, tool=ToolInfo(name, cid, args))
        if act == "SEARCH_HISTORY":
            emit(a, turn, "tool_result", d.get("answerToQuery", ""), t, ref, tool=ToolInfo(name, cid, args))

    ids = {slug[u]: u for u in by_uuid if slug[u] in seen}
    trace_agents = {s: Agent(s, a["name"], a["model_string"], meta={"uuid": u, "joined": a["created_at"][:10]})
                    for s, u in sorted(ids.items()) for a in [by_uuid[u]]}
    label = f"village_{start or 'start'}_{end or 'end'}".replace(" ", "T")
    return Trace(label, trace_agents, events)
