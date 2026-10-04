"""Classify tool calls into blackboard reads and writes, with the content involved.

Explicit tools (Read, Write, Edit, messaging, simple `cat`/`echo >`) are handled by rules: certain,
free, exact content. Everything else (Bash pipelines, sed -i, git, curl, unknown or MCP tools) goes to
an LLM, which sees the call AND its result (a failed command reads/writes nothing) and returns zero or
more ops, each with a confidence. Paths are resolved against a per-agent working directory (`cd` is
tracked), Edit content is the file after the edit, and ids are canonicalised at the end.
"""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
from dataclasses import replace

from gleeb.llm import LLM, load_prompt
from gleeb.schema import BlackboardOp, Event, Trace

KINDS = ("file", "dm", "board", "external")
MAX_RESULT = 4000                                      # chars of tool result shown to the LLM
_LINE_NO = re.compile(r"^\s*\d+[\t→]", re.M)
_FAILED = re.compile(r"no such file|does not exist|not found|permission denied|is a directory|^error\b", re.I | re.M)

OPS_SCHEMA = {
    "type": "object",
    "properties": {"ops": {"type": "array", "items": {
        "type": "object",
        "properties": {"op": {"type": "string", "enum": ["R", "W"]},
                       "blackboard": {"type": "string"},
                       "content_from": {"type": "string", "enum": ["result", "args", "unknown"]},
                       "written_text": {"type": "string"},
                       "confidence": {"type": "number"}},
        "required": ["op", "blackboard", "content_from", "written_text", "confidence"],
        "additionalProperties": False}}},
    "required": ["ops"],
    "additionalProperties": False,
}


def normalize(text: str) -> str:
    """Strip read-tool line numbers and collapse whitespace (for ids and matching)."""
    return " ".join(_LINE_NO.sub("", text).split())


def content_id(text: str) -> str:
    return hashlib.sha256(normalize(text).encode()).hexdigest()[:16]


def base_name(tool: str) -> str:
    return tool.split("__")[-1] if tool.startswith("mcp__") else tool


def _path(p: str, cwd: str) -> str:
    return posixpath.normpath(p if p.startswith("/") else posixpath.join(cwd, p))


# --- rules --------------------------------------------------------------------------------

def _key(path: str, agent: str, private: tuple[str, ...]) -> str:
    """Canonical path: files under a private dir (e.g. each agent's own /home) get the agent's name."""
    if any(path == d or path.startswith(d.rstrip("/") + "/") for d in private):
        return f"[{agent}]{path}"
    return path


def _rule(name: str, args: dict, result: str, agent: str, cwd: str, files: dict,
          private: tuple[str, ...] = ()) -> list[tuple] | None:
    """-> [(op, blackboard_id, content, confidence)], [] for 'no blackboard op', None for 'ask the LLM'."""
    n = base_name(name)
    if n == "Read" and "file_path" in args:
        return [] if _failed(result) else [("R", f"file:{_path(args['file_path'], cwd)}", result, 1.0)]
    if n == "Write" and "file_path" in args:
        return [("W", f"file:{_path(args['file_path'], cwd)}", args.get("content", ""), 1.0)]
    if n in ("Edit", "MultiEdit") and "file_path" in args:
        p, edits = _path(args["file_path"], cwd), args.get("edits") or [args]
        text = files.get(_key(p, agent, private))
        if text is None:                                 # file never seen: only the new fragments are known
            return [("W", f"file:{p}", "\n".join(e.get("new_string", "") for e in edits), 0.5)]
        for e in edits:
            text = text.replace(e.get("old_string", ""), e.get("new_string", ""), -1 if e.get("replace_all") else 1)
        return [("W", f"file:{p}", text, 1.0)]
    if n == "send_dm" and "to" in args:
        return [("W", f"dm:inbox:{args['to']}", args.get("message", ""), 1.0)]
    if n == "pass_turn":                                 # floor passing: logged by the game master, no blackboard
        return []
    if n == "read_dms":
        return [("R", f"dm:inbox:{agent}", result, 1.0)]
    if n == "post":
        return [("W", "board:team", args.get("message", ""), 1.0)]
    if n == "read_board":
        return [("R", "board:team", result, 1.0)]
    if (v := _village_rule(n, args, result)) is not None:
        return v
    if n.lower() == "bash":
        return _bash_rule(args.get("command", ""), result, cwd)
    return None


def _failed(result: str) -> bool:
    """Short error-looking results mean nothing was read."""
    return len(result) < 300 and bool(_FAILED.search(result))


def _bash_rule(cmd: str, result: str, cwd: str) -> list[tuple] | None:
    cmd = cmd.strip()
    if not cmd or re.fullmatch(r"(ls|pwd|true)(\s[^|;&><]*)?", cmd):
        return []
    if m := re.fullmatch(r"cat\s+([^\s|;&<>*?]+)", cmd):
        return [] if _failed(result) else [("R", f"file:{_path(m.group(1), cwd)}", result, 1.0)]
    if m := re.fullmatch(r"""cat\s*>\s*([^\s|;&<>]+)\s*<<-?\s*(['"]?)(\w+)\2\n(.*?)\n?\3\s*""", cmd, re.S):
        return [("W", f"file:{_path(m.group(1), cwd)}", m.group(4), 1.0)]     # heredoc write
    if m := re.fullmatch(r"""echo\s+(['"]?)(.*?)\1\s*>\s*([^\s|;&<>]+)""", cmd):
        return [("W", f"file:{_path(m.group(3), cwd)}", m.group(2), 1.0)]
    return None


# --- AI Village rules (tool names produced by gleeb.parsers.village) ----------------------------
# Chat rooms are boards (board:<room>). Incoming chat arrives as message_in events (see _village_inbox_ops).

_VILLAGE_NOOP = {"consolidate", "pause", "wait", "enter_room", "request_google_sign_in",
                 "restart_after_google_sign_in", "cancel_human_helper_request",
                 "start_using_computer", "stop_using_computer"}
_VILLAGE_MSG = re.compile(r"^\[#([^\]]+)\] ([^:\n]+): ", re.M)


def _village_rule(n: str, args: dict, result: str) -> list[tuple] | None:
    """AI Village: posting is a write to the room's board; search_history reads a third-LLM digest of
    past chat (its own board id, since the answer is filtered); bookkeeping calls touch no blackboard."""
    if n == "send_message_to_chat" and "room" in args:
        return [("W", f"board:{args['room']}", args.get("message", ""), 1.0)]
    if n == "search_history":
        return [("R", "board:village-history", result, 0.7)] if result else []
    if n in _VILLAGE_NOOP:
        return []
    return None


def _village_inbox_ops(e: Event) -> list[BlackboardOp]:
    """AI Village: a message_in event batches '[#room] speaker: text' lines; each is a read of board:<room>."""
    marks = list(_VILLAGE_MSG.finditer(e.content))
    out = []
    for i, m in enumerate(marks):
        text = e.content[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(e.content)].strip()
        out.append(BlackboardOp(e.seq, e.agent, "R", f"board:{m.group(1)}", "board", text, content_id(text),
                                "rule", 1.0, e.seq))
    return out


# --- LLM fallback -------------------------------------------------------------------------

def _llm_ops(llm: LLM, name: str, args: dict, result: str, agent: str, cwd: str) -> list[tuple]:
    user = (f"Agent: {agent}\nWorking directory: {cwd}\nTool: {name}\n"
            f"Arguments: {json.dumps(args, ensure_ascii=False)}\nResult:\n{result[:MAX_RESULT]}")
    out = []
    for o in llm.json(load_prompt("ops"), user, OPS_SCHEMA)["ops"]:
        content = {"result": result, "args": o["written_text"]}.get(o["content_from"], "")
        bid = o["blackboard"] if ":" in o["blackboard"] else "external:unknown"
        out.append((o["op"], bid, content, o["confidence"]))
    return out


# --- driver -------------------------------------------------------------------------------

def classify_ops(trace: Trace, llm: LLM | None = None, cwd: str = ".",
                 private: tuple[str, ...] = ()) -> tuple[list[BlackboardOp], list[str]]:
    """Every tool call in the trace -> blackboard ops. Without an llm, non-rule calls are reported
    in the returned notes and skipped."""
    results = {(e.agent, e.tool.call_id): e for e in trace.events if e.kind == "tool_result" and e.tool}
    dirs: dict[str, str] = {}                            # agent -> current working directory
    files: dict[str, str] = {}                           # canonical path -> last known content
    ops, notes = [], []
    for call in (e for e in trace.events if e.kind == "tool_call" and e.tool):
        res: Event | None = results.get((call.agent, call.tool.call_id))
        result, args, here = (res.content if res else ""), dict(call.tool.args), dirs.get(call.agent, cwd)
        if base_name(call.tool.name).lower() == "bash":   # track `cd dir [&& rest]`
            if m := re.match(r"\s*cd\s+([^\s;&|]+)\s*(?:&&\s*(.*))?$", args.get("command", ""), re.S):
                here = dirs[call.agent] = _path(m.group(1), here)
                args["command"] = m.group(2) or ""
        found, source = _rule(call.tool.name, args, result, call.agent, here, files, private), "rule"
        if found is None:
            if llm is None:
                notes.append(f"{call.ref or call.seq}: {call.tool.name} not classified (no llm)")
                continue
            found, source = _llm_ops(llm, call.tool.name, args, result, call.agent, here), "llm"
        for op, bid, content, conf in found:
            if bid.startswith("file:"):
                bid = "file:" + _key(_path(bid[5:], here), call.agent, private)
                if content:
                    files[bid[5:]] = _LINE_NO.sub("", content) if op == "R" else content
            kind = bid.split(":", 1)[0] if bid.split(":", 1)[0] in KINDS else "external"
            ops.append(BlackboardOp(res.seq if (op == "R" and res) else call.seq, call.agent, op, bid, kind,
                                    content, content_id(content), source, conf, call.seq))
    for e in trace.events:                               # AI Village: incoming chat is a read of the room board
        if e.kind == "message_in" and e.content.startswith("[#"):
            ops.extend(_village_inbox_ops(e))
    return resolve(ops), notes


def resolve(ops: list[BlackboardOp]) -> list[BlackboardOp]:
    """Canonical ids: an absolute path that uniquely ends with a relative path seen elsewhere
    (/workspace/guide.md vs guide.md) is mapped to the relative one."""
    paths = {o.blackboard_id[5:] for o in ops if o.blackboard_id.startswith("file:")}
    rel = [p for p in paths if not p.startswith("/")]
    alias = {}
    for p in paths - set(rel):
        hits = [r for r in rel if p.endswith("/" + r)]
        if len(hits) == 1:
            alias[f"file:{p}"] = f"file:{hits[0]}"
    return [replace(o, blackboard_id=alias.get(o.blackboard_id, o.blackboard_id)) for o in ops]
