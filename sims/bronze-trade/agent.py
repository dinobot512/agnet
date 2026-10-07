"""CaptainPlayer: model calls for a captain's three kinds of decision (first trade, tavern talk, final).

Each call shows the captain its fresh briefing (Sim.briefing) and only the tools for that stage. Tool
calls are applied to the Sim immediately; errors are returned so the model can retry, up to max_steps.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import anthropic


def tool(name: str, description: str, props: dict | None = None, required: list[str] | None = None) -> dict:
    return {"name": name, "description": description,
            "input_schema": {"type": "object", "properties": props or {}, "required": required or []}}


BUY = tool("buy", "Buy goods from this port's market. Every unit raises the price a little.",
           {"good": {"type": "string"}, "qty": {"type": "integer"}}, ["good", "qty"])
SELL = tool("sell", "Sell goods from your hold to this port's market. Every unit lowers the price a little.",
            {"good": {"type": "string"}, "qty": {"type": "integer"}}, ["good", "qty"])
NOTE = tool("note", "Write a short private note to your future self (kept between wake-ups).",
            {"text": {"type": "string"}}, ["text"])
DONE = tool("done_trading", "Finish your first trades. You will still talk and make final decisions afterwards.")
SAY = tool("say", "Say one thing in the tavern (1-2 sentences; anything past 300 characters is cut off). "
                  "Everyone present hears it and the barkeep remembers it.",
           {"text": {"type": "string"}}, ["text"])
SILENT = tool("stay_silent", "Say nothing this round.")
SAIL = tool("sail", "Set sail for another port. You sleep until you arrive and can do nothing at sea.",
            {"port": {"type": "string"}}, ["port"])
WAIT = tool("wait", "Stay in this port asleep: you wake when another ship arrives (it trades before you) "
                    "or after this many days (1-30).", {"days": {"type": "integer"}}, ["days"])

STAGE_TOOLS = {"first": [BUY, SELL, NOTE, DONE], "talk": [SAY, SILENT, NOTE], "final": [BUY, SELL, NOTE, SAIL, WAIT]}
STAGE_HINT = {
    "first": "Trade now with `buy` / `sell`, then call `done_trading`. The tavern talk and your final decisions "
             "come afterwards. Make ALL your calls in ONE response (e.g. sell, buy, done_trading together).",
    "talk": "Tavern, round {round} of {rounds}: `say` ONE thing to everyone present, in your persona's voice — "
            "or `stay_silent`. What you say is public and the barkeep will repeat it to later visitors. "
            "You may also `note`.",
    "final": "Trade if you like (`buy` / `sell`), optionally `note`, then END with `sail` (to a port) "
             "or `wait` (days). Make ALL your calls in ONE response (e.g. sell, buy, note, sail together). "
             "Check 'most you can buy now' before buying.",
}
END_TOOLS = {"first": "done_trading", "talk": ("say", "stay_silent"), "final": ("sail", "wait")}

# Newer models reject forced tool use (tool_choice any/tool) and take an explicit effort level instead of
# no thinking control; they get tool_choice auto + strict schemas + a prompt nudge, and a server-side
# fallback in case of a refusal.
NO_FORCED_TOOLS = ("claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1", "claude-mythos-5-1")
ALWAYS_TOOLS = ("\n\nAlways act by calling the tools provided. Never answer with plain text alone: "
                "every reply must contain at least one tool call.")
NUDGE = "Please act now by calling the tools (your reply had no tool call)."


def strict(t: dict) -> dict:
    return {**t, "strict": True, "input_schema": {**t["input_schema"], "additionalProperties": False}}


def rules_text(sim, cid: str) -> str:
    c, cfg = sim.captains[cid], sim.cfg
    return "\n".join(cfg["rules"]).format(
        name=c.name, home=c.home, persona=c.persona, days=sim.days, capacity=cfg["ship"]["capacity"],
        provisions=cfg["ship"]["provisions_per_day"], dues=cfg["ship"].get("harbor_dues", 0),
        talk_rounds=cfg["talk_rounds"])


def dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json", exclude_none=True)
    if isinstance(obj, list):
        return [dump(o) for o in obj]
    return obj


class CaptainPlayer:
    def __init__(self, transcript_dir: Path, cfg: dict, client: anthropic.Anthropic | None = None):
        self.client = client or anthropic.Anthropic()
        self.cfg = cfg
        self.transcript_dir = transcript_dir
        self.usage = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
        self._lock = threading.Lock()
        self._system_logged: set[str] = set()
        self.modern = cfg["model"].startswith(NO_FORCED_TOOLS)

    def _log(self, cid: str, role: str, content, **extra):
        line = {"role": role, "content": content, "t": time.time(), **extra}
        with open(self.transcript_dir / f"captain_{cid}.jsonl", "a") as f:
            f.write(json.dumps(line) + "\n")

    def _call_tool(self, sim, cid: str, name: str, args: dict) -> str:
        if name == "buy":
            return sim.buy(cid, args.get("good", ""), args.get("qty", 0))
        if name == "sell":
            return sim.sell(cid, args.get("good", ""), args.get("qty", 0))
        if name == "note":
            return sim.note(cid, args.get("text", ""))
        if name == "done_trading":
            return sim.done_trading(cid)
        if name == "say":
            return sim.say(cid, args.get("text", ""))
        if name == "stay_silent":
            return sim.stay_silent(cid)
        if name == "sail":
            return sim.sail(cid, args.get("port", ""))
        if name == "wait":
            return sim.wait(cid, args.get("days", 0))
        return f"error: unknown tool {name}"

    def _act(self, sim, cid: str, stage: str, round_no: int | None = None):
        c = sim.captains[cid]
        meta = {"day": sim.day, "port": c.port, "stage": stage, **({"round": round_no} if round_no else {})}
        system = rules_text(sim, cid) + (ALWAYS_TOOLS if self.modern else "")
        if cid not in self._system_logged:
            self._system_logged.add(cid)
            self._log(cid, "system", system, **meta)
        hint = STAGE_HINT[stage].format(round=round_no, rounds=self.cfg["talk_rounds"])
        view = f"{sim.briefing(cid)}\n\n---\n**What to do now:** {hint}"
        messages = [{"role": "user", "content": view}]
        self._log(cid, "user", view, **meta)

        for _ in range(self.cfg["max_steps"]):
            try:
                if self.modern:
                    response = self.client.beta.messages.create(
                        model=self.cfg["model"], max_tokens=self.cfg["max_tokens_thinking"], system=system,
                        tools=[strict(t) for t in STAGE_TOOLS[stage]], tool_choice={"type": "auto"},
                        output_config={"effort": self.cfg["effort"]}, messages=messages,
                        betas=["server-side-fallback-2026-07-01"], extra_body={"fallbacks": "default"})
                else:
                    response = self.client.messages.create(
                        model=self.cfg["model"], max_tokens=self.cfg["max_tokens"], system=system,
                        tools=STAGE_TOOLS[stage], tool_choice={"type": "any"}, messages=messages)
            except anthropic.APIError as e:
                self._log(cid, "user", f"(harness) API error: {e}", **meta)
                sim.log("api_error", captain=cid, error=str(e))
                if isinstance(e, (anthropic.AuthenticationError, anthropic.PermissionDeniedError)) or \
                        "credit balance" in str(e):
                    raise
                return
            with self._lock:
                self.usage["calls"] += 1
                self.usage["input_tokens"] += response.usage.input_tokens
                self.usage["output_tokens"] += response.usage.output_tokens
            self._log(cid, "assistant", dump(response.content), stop_reason=response.stop_reason,
                      usage={"input_tokens": response.usage.input_tokens,
                             "output_tokens": response.usage.output_tokens}, **meta)

            if response.stop_reason == "refusal":
                sim.log("refusal", captain=cid, details=dump(getattr(response, "stop_details", None)))
                return
            results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                out = self._call_tool(sim, cid, block.name, block.input)
                if out.startswith("error"):
                    sim.log("invalid_action", captain=cid, tool=block.name, input=block.input, error=out)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": out,
                                **({"is_error": True} if out.startswith("error") else {})})
            if results:
                self._log(cid, "user", results, **meta)
            if c.decided:
                return
            if not results:
                if not self.modern:
                    return
                sim.log("no_tool_call", captain=cid, stage=stage)
                self._log(cid, "user", NUDGE, **meta)
                messages += [{"role": "assistant", "content": response.content}, {"role": "user", "content": NUDGE}]
                continue
            messages += [{"role": "assistant", "content": response.content}, {"role": "user", "content": results}]

    def first_trade(self, sim, cid: str):
        self._act(sim, cid, "first")

    def talk(self, sim, cid: str, round_no: int):
        self._act(sim, cid, "talk", round_no)

    def final(self, sim, cid: str):
        self._act(sim, cid, "final")
