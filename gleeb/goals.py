"""Goal monitors: one implementation, parameterized by stream, method, level and sample.

Streams (input filters)
  expressed  : reasoning + text          (the agent's own words, no tool results)
  behavioral : tool_call + tool_result   (actions and results, no reasoning)
  all        : every event               (diagnostic reference, not ground truth)

Methods
  whole            M1: one call over the full stream, returns a partition
  windowed         M2: independent answer per window; the pairwise judge places boundaries
  bullets_whole    M3: compress chunks into observable-only bullets, then M1 over bullets
  bullets_windowed M3: same, then M2 over bullets

Every method works on "items" (a raw event, or a bullet citing events) and returns spans over item
ids; spans are mapped back to Event.seq through each item's evidence. The output always partitions
the stream: span k ends just before span k+1's start range.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from gleeb.align import judge
from gleeb.llm import LLM, load_prompt
from gleeb.schema import Channel, Event, GoalSpan, GoalStream, Level, Trace

STREAMS: dict[str, tuple[str, ...] | None] = {
    "expressed": ("reasoning", "text"), "behavioral": ("tool_call", "tool_result"), "all": None}
QUESTIONS = {
    "expressed": "What does the agent say it is trying to achieve?",
    "behavioral": "What does the agent seem to be trying to achieve, judging only from its actions?",
    "all": "What is the agent trying to achieve?"}
BULLET_FOCUS = {
    "expressed": "Report what the agent said.",
    "behavioral": "Report what the agent did and what came back.",
    "all": "Report both; start each bullet with 'Did:' or 'Said:'."}
LEVELS = {"objective": "objective (the outcome it is trying to bring about; what would count as done)",
          "step": "step (what it is doing right now toward its objective)"}
METHODS = ("whole", "windowed", "bullets_whole", "bullets_windowed")
PROMPT_VERSION = "goals_v2"
MAX_CHARS = 2000
INTENT = re.compile(r"\b(in order to|so that|so as to|aim(s|ed|ing)?|trying to|tries to|attempt(s|ing)? to|"
                    r"intend(s|ed|ing)?|wants? to|in an effort to|to adapt|to make it suitable)\b", re.I)


def _obj(props: dict) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


_INTS = {"type": "array", "items": {"type": "integer"}}
GOAL = {"goal": {"type": "string"}, "confidence": {"type": "number"}, "evidence": _INTS}
WHOLE_SCHEMA = _obj({"spans": {"type": "array", "items": _obj(
    {"start_lo": {"type": "integer"}, "start_hi": {"type": "integer"}, **GOAL})}})
WINDOW_SCHEMA = _obj(GOAL)
BULLETS_SCHEMA = _obj({"bullets": {"type": "array", "items": _obj({"text": {"type": "string"}, "evidence": _INTS})}})


@dataclass
class Item:
    id: int
    text: str
    evidence: list[int]                       # Event.seq values this item stands for


# --- entry points --------------------------------------------------------------------------

def select(trace: Trace, agent: str, stream: Channel) -> list[Event]:
    kinds = STREAMS[stream]
    return [e for e in trace.events if e.agent == agent and (kinds is None or e.kind in kinds)]


def run_monitor(trace: Trace, agent: str, stream: Channel, method: str, llm: LLM,
                level: Level = "objective", sample_id: int = 0,
                window: int = 10, overlap: int = 3, chunk: int = 10) -> GoalStream:
    if method not in METHODS:
        raise ValueError(f"method must be one of {METHODS}")
    events = select(trace, agent, stream)
    out = GoalStream(agent, stream, method, llm.codebook(PROMPT_VERSION), level, sample_id)
    out.meta["has_thinking"] = any(e.kind == "reasoning" and e.source == "thinking" for e in trace.events
                                   if e.agent == agent)
    out.meta["n_events"] = len(events)
    if not events:
        out.notes.append("empty stream")
        return out
    before = dict(llm.tokens)

    items = [Item(e.seq, render(e), [e.seq]) for e in events]
    if method.startswith("bullets_"):
        items = compress(items, stream, llm, sample_id, out.notes, chunk)
    q = (QUESTIONS[stream], level)
    raw = (whole(items, q, llm, sample_id, out.notes) if method.endswith("whole")
           else windowed(items, q, llm, sample_id, out.notes, window, overlap))
    if raw:
        out.spans = to_events(raw, items, [e.seq for e in events], out, out.notes)
        out.notes += validate(out.spans, [e.seq for e in events])
    out.meta["tokens"] = {k: llm.tokens[k] - before[k] for k in before}
    return out


def run_samples(trace: Trace, agent: str, stream: Channel, method: str, llm: LLM, k: int = 3,
                **kw) -> list[GoalStream]:
    return [run_monitor(trace, agent, stream, method, llm, sample_id=i, **kw) for i in range(k)]


# --- rendering and calls -------------------------------------------------------------------

def render(e: Event) -> str:
    if e.kind == "tool_call":
        body = f"{e.tool.name}({json.dumps(e.tool.args, ensure_ascii=False)})"
    elif e.kind == "tool_result":
        body = f"{e.tool.name} returned: {e.content}"
    else:
        body = e.content
    return f"{e.kind}: {body[:MAX_CHARS]}".replace("\n", " ↵ ")


def _user(q: tuple[str, str], items: list[Item]) -> str:
    question, level = q
    return (f"Question: {question}\nLevel: {LEVELS[level]}\n\nItems:\n"
            + "\n".join(f"[{i.id}] {i.text}" for i in items))


def _ask(llm: LLM, system: str, user: str, schema: dict, check, salt) -> tuple[dict, list[str]]:
    """One call; on validation errors, retry once with the errors appended."""
    out = llm.json(system, user, schema, salt)
    errs = check(out)
    if errs:
        out = llm.json(system, f"{user}\n\nYour previous answer was invalid: {'; '.join(errs)}. "
                               "Answer again, correctly.", schema, salt)
        errs = check(out)
    return out, errs


# --- M1 whole -------------------------------------------------------------------------------

def whole(items: list[Item], q, llm: LLM, salt, notes: list[str]) -> list[dict] | None:
    pos = {i.id: k for k, i in enumerate(items)}

    def check(out):
        errs, prev_hi = [], -1
        for s in out["spans"]:
            lo, hi = pos.get(s["start_lo"]), pos.get(s["start_hi"])
            if lo is None or hi is None or lo > hi:
                errs.append(f"bad start range ({s['start_lo']}, {s['start_hi']})")
            elif lo <= prev_hi:
                errs.append(f"start range ({s['start_lo']}, {s['start_hi']}) is not after the previous one")
            else:
                prev_hi = hi
            if not s["evidence"] or any(x not in pos for x in s["evidence"]):
                errs.append(f"evidence {s['evidence']} must be non-empty item indices from the list")
        return errs or ([] if out["spans"] else ["no spans"])

    out, errs = _ask(llm, load_prompt("rubric") + load_prompt("whole"), _user(q, items), WHOLE_SCHEMA, check, salt)
    if errs:
        notes.append(f"whole: failed after retry: {'; '.join(errs)}")
        return None
    spans = [dict(start=(s["start_lo"], s["start_hi"]), goal=s["goal"], confidence=s["confidence"],
                  evidence=s["evidence"]) for s in out["spans"]]
    spans[0]["start"] = (items[0].id, items[0].id)
    return spans


# --- M2 windowed ----------------------------------------------------------------------------

def windows(items: list, size: int, overlap: int) -> list[list]:
    step = max(size - overlap, 1)
    return [items[i:i + size] for i in range(0, max(len(items) - overlap, 1), step)]


def windowed(items: list[Item], q, llm: LLM, salt, notes: list[str], size: int, overlap: int) -> list[dict] | None:
    pos = {i.id: k for k, i in enumerate(items)}
    system = load_prompt("rubric") + load_prompt("window")
    answers = []
    for w in windows(items, size, overlap):
        ids = {i.id for i in w}
        check = lambda o, ids=ids: [] if o["evidence"] and set(o["evidence"]) <= ids else \
            [f"evidence must be non-empty indices from this window ({min(ids)}-{max(ids)})"]
        a, errs = _ask(llm, system, _user(q, w), WINDOW_SCHEMA, check, salt)
        if errs:
            notes.append(f"window {w[0].id}-{w[-1].id}: failed after retry; skipped")
        else:
            answers.append((w, a))
    if not answers:
        return None

    groups, starts = [[answers[0][1]]], [(0, 0)]          # starts as item positions
    for (wa, a), (wb, b) in zip(answers, answers[1:]):
        if judge(llm, a["goal"], b["goal"])["verdict"] != "different":
            groups[-1].append(b)
            continue
        pa = max(pos[x] for x in a["evidence"])            # old goal still evident here
        later = [pos[x] for x in b["evidence"] if pos[x] > pa]
        lo = max(pa + 1, starts[-1][1] + 1)
        hi = max(min(later) if later else pos[wb[0].id], lo)
        if lo > len(items) - 1:
            groups[-1].append(b)
            continue
        starts.append((lo, min(hi, len(items) - 1)))
        groups.append([b])

    spans = []
    for g, st in zip(groups, starts):
        best = max(g, key=lambda x: x["confidence"])
        spans.append(dict(start=(items[st[0]].id, items[st[1]].id), goal=best["goal"],
                          confidence=best["confidence"], evidence=sorted({x for a in g for x in a["evidence"]})))
    return spans


# --- M3 bullets -----------------------------------------------------------------------------

def compress(items: list[Item], stream: Channel, llm: LLM, salt, notes: list[str], chunk: int) -> list[Item]:
    """Observable-only bullets per chunk. Chunks that fail validation fall back to raw items."""
    system = load_prompt("bullets")
    bullets: list[Item] = []
    for c in windows(items, chunk, 0):
        ids = {i.id for i in c}

        def check(o, ids=ids):
            errs = [f"bullet '{b['text']}' must cite indices from this chunk"
                    for b in o["bullets"] if not b["evidence"] or not set(b["evidence"]) <= ids]
            errs += [f"bullet '{b['text']}' states an intention ('{m.group(0)}')"
                     for b in o["bullets"] if (m := INTENT.search(b["text"]))]
            return errs or ([] if o["bullets"] else ["no bullets"])

        user = BULLET_FOCUS[stream] + "\n\n" + "\n".join(f"[{i.id}] {i.text}" for i in c)
        out, errs = _ask(llm, system, user, BULLETS_SCHEMA, check, salt)
        hard = [e for e in errs if "states an intention" not in e]
        if hard:
            notes.append(f"bullets {c[0].id}-{c[-1].id}: failed after retry; using raw events")
            bullets += [Item(-1, i.text, i.evidence) for i in c]
            continue
        if errs:
            notes.append(f"bullets {c[0].id}-{c[-1].id}: intent language kept after retry: {'; '.join(errs)}")
        bullets += [Item(-1, b["text"], sorted(b["evidence"])) for b in out["bullets"]]
    for k, b in enumerate(bullets):
        b.id = k
    return bullets


# --- mapping and validation -----------------------------------------------------------------

def to_events(raw: list[dict], items: list[Item], seqs: list[int], stream: GoalStream,
              notes: list[str]) -> list[GoalSpan]:
    """Item-space spans -> GoalSpans over Event.seq that partition `seqs`."""
    by_id = {i.id: i for i in items}
    idx = {s: k for k, s in enumerate(seqs)}
    starts = []
    for s in raw:                                       # boundary = first event of the new span
        lo, hi = min(by_id[s["start"][0]].evidence), min(by_id[s["start"][1]].evidence)
        starts.append((idx[lo], idx[hi]))
    starts[0] = (0, 0)
    for k in range(1, len(starts)):                     # bullet evidence can interleave: keep monotone
        lo = max(starts[k][0], starts[k - 1][1] + 1)
        if lo != starts[k][0]:
            notes.append(f"span {k}: start range clamped to stay after span {k - 1}")
        starts[k] = (min(lo, len(seqs) - 1), min(max(starts[k][1], lo), len(seqs) - 1))
    spans = []
    for k, (s, st) in enumerate(zip(raw, starts)):
        nxt = starts[k + 1] if k + 1 < len(starts) else (len(seqs), len(seqs))
        ev = sorted({x for i in s["evidence"] for x in by_id[i].evidence})
        spans.append(GoalSpan(f"{stream.id}:{k}", stream.agent, stream.stream,
                              (seqs[st[0]], seqs[st[1]]), (seqs[nxt[0] - 1], seqs[nxt[1] - 1]),
                              s["goal"], stream.level, s["confidence"], ev))
    return spans


def validate(spans: list[GoalSpan], seqs: list[int]) -> list[str]:
    """Checks every output: indices in range, partition, evidence present and inside its span."""
    ok, flags = set(seqs), []
    if spans and (spans[0].start[0] != seqs[0] or spans[-1].end[1] != seqs[-1]):
        flags.append("spans do not cover the whole stream")
    for a, b in zip(spans, spans[1:]):
        if b.start[0] <= a.start[1]:
            flags.append(f"{b.id}: start range overlaps previous span's")
    for s in spans:
        if not ({*s.start, *s.end} <= ok):
            flags.append(f"{s.id}: index outside the stream")
        if not s.evidence:
            flags.append(f"{s.id}: no evidence")
        elif not all(s.start[0] <= e <= s.end[1] for e in s.evidence):
            flags.append(f"{s.id}: evidence outside the span")
    return flags
