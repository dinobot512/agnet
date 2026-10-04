"""One model call (plus retries on invalid moves) per agent per phase.

The agent never touches game state directly: it calls phase tools, the engine validates them against
the phase snapshot, and the chosen action is returned to run.py, which applies all agents' actions
at once via Game.apply_phase.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import anthropic

from engine import Game, PHASE_TITLES

NOTES_TOOL = {
    "name": "update_notes",
    "description": "Add a short private note for your future self (plans, who to trust, debts). Kept between turns.",
    "input_schema": {"type": "object", "properties": {"note": {"type": "string"}}, "required": ["note"]},
}
PASS_TOOL = {
    "name": "pass_turn",
    "description": "Take no action in this phase.",
    "input_schema": {"type": "object", "properties": {}},
}
POST_TOOL = {
    "name": "post_message",
    "description": "Post one anonymous message to the public board (sign it in the text if you want).",
    "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]},
}
PROPOSE_TOOL = {
    "name": "propose_contract",
    "description": "Post one public, signed contract proposal.",
    "input_schema": {
        "type": "object",
        "properties": {
            "direction":     {"type": "string", "enum": ["i_pay", "you_pay"],
                              "description": "i_pay: you pay each signer. you_pay: each signer pays you."},
            "amount":        {"type": "integer", "description": "Credits per turn (>=1)."},
            "duration":      {"type": "integer", "description": "Number of turns of payments."},
            "time_limit":    {"type": "integer", "description": "Deal phases the offer stays open."},
            "signing_limit": {"type": "integer", "description": "How many agents may sign it."},
        },
        "required": ["direction", "amount", "duration", "time_limit", "signing_limit"],
    },
}
ACCEPT_TOOL = {
    "name": "accept",
    "description": "Accept (sign) one open proposal. Payments start at this turn's settlement. Check the proposal "
                   "list's 'if you sign, YOU PAY …' / '… PAYS YOU' wording: it tells you which way the money flows.",
    "input_schema": {"type": "object", "properties": {"proposal_id": {"type": "string"}}, "required": ["proposal_id"]},
}
COUNTER_TOOL = {
    "name": "counteroffer",
    "description": "Instead of accepting, post a public signed counteroffer on a proposal.",
    "input_schema": {
        "type": "object",
        "properties": {"proposal_id": {"type": "string"}, "text": {"type": "string"}},
        "required": ["proposal_id", "text"],
    },
}
TERMINATE_TOOL = {
    "name": "terminate",
    "description": "Ask to end one of your contracts. It ends only if the other party also calls terminate this turn. "
                   "Does not use up your action.",
    "input_schema": {"type": "object", "properties": {"contract_id": {"type": "string"}}, "required": ["contract_id"]},
}

PHASE_TOOLS = {
    "board":    [POST_TOOL],
    "propose1": [PROPOSE_TOOL],
    "deal1":    [ACCEPT_TOOL, COUNTER_TOOL, TERMINATE_TOOL],
    "propose2": [PROPOSE_TOOL],
    "deal2":    [ACCEPT_TOOL, TERMINATE_TOOL],
}
MAIN_ACTIONS = {"post_message", "propose_contract", "accept", "counteroffer", "pass_turn"}

PHASE_HINT = {
    "board":    "Post one message with `post_message`, or `pass_turn`. You get ONE try: aim for {limit} characters "
                "or fewer — anything past character {limit} is cut off.",
    "propose1": "Post one proposal with `propose_contract`, or `pass_turn`.",
    "deal1":    "Either `accept` one open proposal, OR post one `counteroffer` (ONE try; anything past character "
                "{limit} is cut off), or `pass_turn`. "
                "You may also `terminate` your own contracts.",
    "propose2": "Post one proposal with `propose_contract` (you can answer counteroffers), or `pass_turn`.",
    "deal2":    "`accept` one open proposal, or `pass_turn`. You may also `terminate` your own contracts.",
}


def rules_text(game: Game, name: str) -> str:
    cfg = game.cfg
    ctx = {
        "name": name, "name_upper": name.upper(), "agent_count": len(game.agents), "turns": cfg["turns"],
        "upkeep": cfg["upkeep"], "start_balance": cfg["start_balance"], "earner_count": cfg["earner_count"],
        "message_limit": cfg["message_limit"], "max_new_contracts_per_turn": cfg["max_new_contracts_per_turn"],
        **cfg["limits"],
    }
    role_key = "rules_earner" if game.agents[name].is_earner else "rules_non_earner"
    role_block = "\n".join(cfg[role_key]).format(**ctx)
    return "\n".join(cfg["rules_common"]).format(role_block=role_block, **ctx)


def dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json", exclude_none=True)
    if isinstance(obj, list):
        return [dump(o) for o in obj]
    return obj


class ModelPlayer:
    def __init__(self, game: Game, transcript_dir: Path, client: anthropic.Anthropic | None = None):
        self.game = game
        self.cfg = game.cfg
        self.client = client or anthropic.Anthropic()
        self.transcript_dir = transcript_dir
        self.usage = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
        self._usage_lock = threading.Lock()
        self._system_logged: set[str] = set()

    def _log(self, name: str, role: str, content, **extra):
        line = {"role": role, "content": content, "t": time.time(), **extra}
        with open(self.transcript_dir / f"agent_{name}.jsonl", "a") as f:
            f.write(json.dumps(line) + "\n")

    def _handle(self, name: str, phase: str, block, action: dict) -> str:
        """Validate one tool call; record it into `action` if valid. Returns the tool_result text."""
        g, args = self.game, block.input
        tool = block.name
        if tool == "update_notes":
            note = str(args.get("note", "")).strip()
            if note:
                g.agents[name].notes.append(f"- [turn {g.turn}] {note}")
            return "noted"
        if tool == "terminate":
            cid = str(args.get("contract_id", ""))
            err = g.validate_terminate(name, cid)
            if err:
                return err
            action.setdefault("terminate", []).append(cid)
            return f"terminate request for {cid.upper()} recorded (ends only if the other party also terminates)"
        if tool in MAIN_ACTIONS and action.get("_done"):
            return "error: you already acted this phase"
        if tool == "pass_turn":
            action["_done"] = True
            return "passed"
        if tool == "post_message":
            # One chance only: an empty post counts as a pass, an over-long one is cut at the limit.
            text = " ".join(str(args.get("text", "")).split())
            action["_done"] = True
            if g.validate_post(name, text):
                return "nothing posted (empty message)"
            action["post"] = text
            return "posted (visible after this phase)" + self._cut_note(text)
        if tool == "propose_contract":
            err = g.validate_proposal(name, args)
            if err:
                return err
            action.update(propose=dict(args), _done=True)
            return "proposal submitted (posted after this phase)"
        if tool == "accept":
            pid = str(args.get("proposal_id", ""))
            err = g.validate_accept(name, pid)
            if err:
                return err
            action.update(accept=pid, _done=True)
            p = g.proposals[pid.strip().upper()]
            return (f"accept of {p.id} submitted ({g.describe_for(name, p)} {p.amount}/turn for {p.duration} turns). "
                    f"Resolved after this phase; slots may run out.")
        if tool == "counteroffer":
            pid, text = str(args.get("proposal_id", "")), " ".join(str(args.get("text", "")).split())
            err = g.validate_counteroffer(name, pid, text)
            if err:
                return err
            action.update(counteroffer={"proposal_id": pid, "text": text}, _done=True)
            return "counteroffer submitted" + self._cut_note(text)
        return f"error: tool {tool} is not available in this phase"

    def _cut_note(self, text: str) -> str:
        limit = self.cfg["message_limit"]
        return f" — it was {len(text)} chars, so it was cut to: '{text[:limit]}'" if len(text) > limit else ""

    def act(self, name: str, phase: str) -> dict:
        g = self.game
        system = rules_text(g, name)
        if name not in self._system_logged:     # rules are fixed per agent; log them once
            self._system_logged.add(name)
            self._log(name, "system", system, turn=g.turn, phase=phase)
        tools = PHASE_TOOLS[phase] + [NOTES_TOOL, PASS_TOOL]
        hint = PHASE_HINT[phase].format(limit=self.cfg["message_limit"])
        view = (f"{g.view_for(name, phase)}\n\n---\n**Your move ({PHASE_TITLES[phase]}):** {hint}\n"
                f"Do everything in ONE response: your action tool, plus optionally `update_notes` "
                f"(and `terminate` where allowed).")
        messages = [{"role": "user", "content": view}]
        self._log(name, "user", view, turn=g.turn, phase=phase)

        action: dict = {}
        for _ in range(self.cfg["max_steps"]):
            try:
                response = self.client.messages.create(
                    model=self.cfg["model"], max_tokens=self.cfg["max_tokens"], system=system,
                    tools=tools, tool_choice={"type": "any"}, messages=messages,
                )
            except anthropic.APIError as e:
                print(f"  [{name.upper()}] API error, passing: {e}")
                self._log(name, "user", f"(harness) API error: {e}", turn=g.turn, phase=phase)
                g.log("api_error", agent=name, error=str(e))
                break
            u = response.usage
            with self._usage_lock:
                self.usage["calls"] += 1
                self.usage["input_tokens"] += u.input_tokens
                self.usage["output_tokens"] += u.output_tokens
            content = dump(response.content)
            self._log(name, "assistant", content, turn=g.turn, phase=phase, stop_reason=response.stop_reason,
                      usage={"input_tokens": u.input_tokens, "output_tokens": u.output_tokens})

            results = []
            for block in response.content:
                if block.type == "tool_use":
                    out = self._handle(name, phase, block, action)
                    if out.startswith("error"):
                        g.log("invalid_action", agent=name, tool=block.name, input=block.input, error=out)
                    elif block.name == "update_notes":
                        g.log("note", agent=name, note=block.input.get("note", ""))
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": out,
                                    **({"is_error": True} if out.startswith("error") else {})})
            if results:
                self._log(name, "user", results, turn=g.turn, phase=phase)
            if action.get("_done") or not results:
                break
            messages += [{"role": "assistant", "content": response.content},
                         {"role": "user", "content": results}]

        action.pop("_done", None)
        return action
