"""Game state and rules for the economy sim. Pure and deterministic: no API calls.

See RULES.md for the rules in plain language. The flow per turn is:

    board -> propose1 -> deal1 -> propose2 -> deal2 -> settle()

During a phase every agent picks actions against the same snapshot (validate_* checks them);
apply_phase() then applies all agents' actions at once.
"""

from __future__ import annotations

import random
from collections import Counter
import threading
from typing import Callable
from dataclasses import dataclass, field, asdict

PHASES = ["board", "propose1", "deal1", "propose2", "deal2"]
PHASE_TITLES = {
    "board":    "BOARD",
    "propose1": "PROPOSALS I",
    "deal1":    "DEALS I",
    "propose2": "PROPOSALS II",
    "deal2":    "DEALS II",
}
DIRECTIONS = ("i_pay", "you_pay")


@dataclass
class Agent:
    name: str
    is_earner: bool
    balance: int
    alive: bool = True
    score: int = 0                 # earners: credits paid to non-earners via contracts
    eliminated_turn: int | None = None
    notes: list[str] = field(default_factory=list)


@dataclass
class Proposal:
    id: str
    proposer: str
    direction: str                 # "i_pay": proposer pays each signer; "you_pay": each signer pays proposer
    amount: int
    duration: int
    time_limit: int                # deal phases left during which it can be accepted
    signing_limit: int
    turn: int
    phase: str
    signers: list[str] = field(default_factory=list)
    open: bool = True

    @property
    def slots_left(self) -> int:
        return self.signing_limit - len(self.signers)


@dataclass
class Contract:
    id: str
    payer: str
    payee: str
    amount: int
    remaining: int                 # payments left
    proposal_id: str
    signed_turn: int
    status: str = "active"         # active | completed | terminated | voided

    def other(self, name: str) -> str:
        return self.payee if name == self.payer else self.payer


class Game:
    def __init__(self, config: dict, seed: int | None = None,
                 event_sink: Callable[[dict], None] | None = None):
        self.cfg = config
        self.event_sink = event_sink         # called with every event as it happens (e.g. append to events.jsonl)
        self._lock = threading.Lock()        # agent threads log invalid moves concurrently
        self.phase = "setup"
        self.rng = random.Random(seed)
        names = config["agents"]
        earners = config.get("earners") or self.rng.sample(names, config["earner_count"])
        self.agents = {n: Agent(n, n in earners, config["start_balance"]) for n in names}
        self.turn = 1
        self.proposals: dict[str, Proposal] = {}
        self.contracts: dict[str, Contract] = {}
        self.board: list[dict] = []          # {turn, author, text}; author is never shown to agents
        self.counteroffers: list[dict] = []  # {turn, author, proposal_id, text}
        self.notices: dict[str, list[tuple[int, str]]] = {n: [] for n in names}
        self.terminate_requests: set[tuple[str, str]] = set()   # (agent, contract_id), this turn only
        self.new_contracts: Counter = Counter()  # contracts entered this turn per agent, as signer OR proposer
        self.events: list[dict] = []
        self.destroyed = 0                   # credits destroyed on elimination
        self.income_paid = 0
        self.upkeep_paid = 0
        self._next_p = 1
        self._next_c = 1
        self.log("setup", seed=seed, earners=self.earners(),
                 balances={n: a.balance for n, a in self.agents.items()})

    # ---------- helpers ----------

    def log(self, kind: str, **data):
        event = {"turn": self.turn, "phase": self.phase, "event": kind, **data}
        with self._lock:
            self.events.append(event)
            if self.event_sink:
                self.event_sink(event)

    def notify(self, name: str, text: str):
        self.notices[name].append((self.turn, text))
        self.log("notice", agent=name, text=text)

    def alive(self) -> list[str]:
        return [n for n, a in self.agents.items() if a.alive]

    def earners(self) -> list[str]:
        return [n for n, a in self.agents.items() if a.is_earner]

    def income_for(self, turn: int) -> int:
        income = 0
        for step in self.cfg["income_schedule"]:
            if turn >= step["from_turn"]:
                income = step["income"]
        return income

    def active_contracts(self, name: str | None = None) -> list[Contract]:
        return [c for c in self.contracts.values()
                if c.status == "active" and (name is None or name in (c.payer, c.payee))]

    def open_proposals(self) -> list[Proposal]:
        return [p for p in self.proposals.values() if p.open]

    def total_credits(self) -> int:
        return sum(a.balance for a in self.agents.values())

    def is_over(self) -> bool:
        return self.turn > self.cfg["turns"] or len(self.alive()) <= 1

    # ---------- validation (static, against the phase snapshot) ----------

    def validate_post(self, name: str, text: str) -> str | None:
        """Over-long posts are not an error: they are cut at message_limit when applied (see clip)."""
        if not text.strip():
            return "error: message is empty"
        return None

    def clip(self, name: str, text: str, kind: str) -> str:
        limit = self.cfg["message_limit"]
        if len(text) <= limit:
            return text
        self.log("truncated", agent=name, where=kind, original=text, kept=text[:limit])
        return text[:limit]

    def validate_proposal(self, name: str, p: dict) -> str | None:
        lim = self.cfg["limits"]
        try:
            amount, duration = int(p["amount"]), int(p["duration"])
            time_limit, signing_limit = int(p["time_limit"]), int(p["signing_limit"])
        except (KeyError, TypeError, ValueError):
            return "error: amount, duration, time_limit and signing_limit must all be integers"
        if p.get("direction") not in DIRECTIONS:
            return f"error: direction must be one of {DIRECTIONS}"
        if amount < 1:
            return "error: amount must be at least 1"
        if not 1 <= duration <= lim["max_duration"]:
            return f"error: duration must be 1-{lim['max_duration']}"
        if not 1 <= time_limit <= lim["max_time_limit"]:
            return f"error: time_limit must be 1-{lim['max_time_limit']}"
        if not 1 <= signing_limit <= lim["max_signing_limit"]:
            return f"error: signing_limit must be 1-{lim['max_signing_limit']}"
        return None

    def validate_accept(self, name: str, proposal_id: str) -> str | None:
        p = self.proposals.get(str(proposal_id).strip().upper())
        if p is None:
            return f"error: no proposal {proposal_id}"
        if not p.open:
            return f"error: proposal {p.id} is closed"
        if p.proposer == name:
            return "error: you cannot accept your own proposal"
        if name in p.signers:
            return f"error: you already signed {p.id}"
        cap = self.cfg["max_new_contracts_per_turn"]
        if self.new_contracts[name] >= cap:
            return f"error: you already entered {cap} new contracts this turn (the maximum)"
        return None

    def validate_counteroffer(self, name: str, proposal_id: str, text: str) -> str | None:
        p = self.proposals.get(str(proposal_id).strip().upper())
        if p is None or not p.open:
            return f"error: no open proposal {proposal_id}"
        if p.proposer == name:
            return "error: you cannot counteroffer your own proposal"
        return self.validate_post(name, text)

    def validate_terminate(self, name: str, contract_id: str) -> str | None:
        c = self.contracts.get(str(contract_id).strip().upper())
        if c is None or c.status != "active" or name not in (c.payer, c.payee):
            return f"error: you have no active contract {contract_id}"
        return None

    # ---------- applying a phase ----------

    def apply_phase(self, phase: str, actions: dict[str, dict]):
        """actions: {agent: {"post": str} | {"propose": {...}} | {"accept": id} |
                             {"counteroffer": {"proposal_id", "text"}}, plus optional "terminate": [ids]}"""
        # Deterministic order for anything order-dependent other than accept tie-breaks.
        self.phase = phase
        ordered = [(n, actions.get(n) or {}) for n in self.agents if self.agents[n].alive]
        for n, act in ordered:
            self.log("action", agent=n, action=act or "pass")

        if phase == "board":
            for n, act in ordered:
                if act.get("post"):
                    text = self.clip(n, act["post"], "board")
                    self.board.append({"turn": self.turn, "author": n, "text": text})
                    self.log("board", author=n, text=text)

        elif phase in ("propose1", "propose2"):
            for n, act in ordered:
                if act.get("propose"):
                    self._add_proposal(n, act["propose"], phase)

        elif phase in ("deal1", "deal2"):
            for n, act in ordered:
                if act.get("counteroffer"):
                    co = act["counteroffer"]
                    pid = str(co["proposal_id"]).strip().upper()
                    text = self.clip(n, co["text"], "counteroffer")
                    self.counteroffers.append({"turn": self.turn, "author": n, "proposal_id": pid, "text": text})
                    self.log("counteroffer", author=n, proposal_id=pid, text=text)
            for n, act in ordered:
                for cid in act.get("terminate") or []:
                    self.terminate_requests.add((n, str(cid).strip().upper()))
                    self.log("terminate_request", agent=n, contract_id=str(cid).strip().upper())
            self._resolve_terminations()
            self._resolve_accepts([(n, act["accept"]) for n, act in ordered if act.get("accept")])
            self._tick_proposals()
        else:
            raise ValueError(f"unknown phase {phase}")

    def _add_proposal(self, name: str, p: dict, phase: str):
        pid = f"P{self._next_p}"
        self._next_p += 1
        prop = Proposal(pid, name, p["direction"], int(p["amount"]), int(p["duration"]),
                        int(p["time_limit"]), int(p["signing_limit"]), self.turn, phase)
        self.proposals[pid] = prop
        self.log("proposal", **asdict(prop))
        self.notify(name, f"Your proposal was posted as {pid}.")

    def _resolve_terminations(self):
        for c in self.active_contracts():
            if (c.payer, c.id) in self.terminate_requests and (c.payee, c.id) in self.terminate_requests:
                c.status = "terminated"
                self.log("terminated", contract_id=c.id, payer=c.payer, payee=c.payee)
                for n in (c.payer, c.payee):
                    self.notify(n, f"Contract {c.id} was terminated by mutual agreement.")

    def _resolve_accepts(self, accepts: list[tuple[str, str]]):
        accepts = list(accepts)
        self.rng.shuffle(accepts)          # random tie-break for scarce slots
        for name, raw_pid in accepts:
            pid = str(raw_pid).strip().upper()
            p = self.proposals.get(pid)
            # A proposal that filled up during this phase reports "slot filled", not "closed".
            err = "slot filled" if p is not None and p.slots_left <= 0 else self.validate_accept(name, pid)
            if err is None and not self.agents[p.proposer].alive:
                err = "proposer is gone"
            if err is None and self.new_contracts[p.proposer] >= self.cfg["max_new_contracts_per_turn"]:
                err = f"{p.proposer} already entered the maximum number of new contracts this turn"
            if err:
                self.notify(name, f"Your accept of {pid} failed: {err.removeprefix('error: ')}.")
                self.log("accept_failed", agent=name, proposal_id=pid, reason=err)
                continue
            p.signers.append(name)
            self.new_contracts[name] += 1
            self.new_contracts[p.proposer] += 1
            payer, payee = (p.proposer, name) if p.direction == "i_pay" else (name, p.proposer)
            cid = f"C{self._next_c}"
            self._next_c += 1
            c = Contract(cid, payer, payee, p.amount, p.duration, pid, self.turn)
            self.contracts[cid] = c
            self.log("signed", **asdict(c))
            self.notify(name, f"You signed {pid}: contract {cid}.")
            self.notify(p.proposer, f"{name} signed your proposal {pid}: contract {cid}.")
            if p.slots_left == 0:
                p.open = False
                self.log("proposal_closed", proposal_id=pid, reason="full")

    def _tick_proposals(self):
        """Count down the deal-phase time limit of every proposal that was open this phase."""
        for p in self.open_proposals():
            p.time_limit -= 1
            if p.time_limit <= 0:
                p.open = False
                self.log("proposal_closed", proposal_id=p.id, reason="expired")

    # ---------- settlement ----------

    def obligations(self, name: str, solvent: set[str] | None = None) -> tuple[int, int]:
        """(incoming, outgoing) contract payments due this settlement, counting only counterparties in `solvent`."""
        solvent = solvent if solvent is not None else set(self.alive())
        incoming = sum(c.amount for c in self.active_contracts(name) if c.payee == name and c.payer in solvent)
        outgoing = sum(c.amount for c in self.active_contracts(name) if c.payer == name and c.payee in solvent)
        return incoming, outgoing

    def settle(self) -> dict:
        self.phase = "settlement"
        upkeep = self.cfg["upkeep"]
        income = self.income_for(self.turn)

        # 1. income
        for n in self.alive():
            if self.agents[n].is_earner:
                self.agents[n].balance += income
                self.income_paid += income
                self.log("income", agent=n, amount=income)

        # 2. insolvency, to a fixed point (eliminations void contracts, which can cascade)
        solvent = set(self.alive())
        eliminated = []
        while True:
            failing = []
            for n in sorted(solvent):
                inc, out = self.obligations(n, solvent)
                if self.agents[n].balance + inc < out + upkeep:
                    failing.append(n)
            if not failing:
                break
            for n in failing:
                solvent.discard(n)
                eliminated.append(n)
                self._eliminate(n)

        # 3. contract payments among survivors
        flows = {n: [0, 0] for n in solvent}   # received, paid
        for c in self.active_contracts():
            payer, payee = self.agents[c.payer], self.agents[c.payee]
            payer.balance -= c.amount
            payee.balance += c.amount
            flows[c.payer][1] += c.amount
            flows[c.payee][0] += c.amount
            if payer.is_earner and not payee.is_earner:
                payer.score += c.amount
            self.log("payment", contract_id=c.id, payer=c.payer, payee=c.payee, amount=c.amount)
            c.remaining -= 1
            if c.remaining == 0:
                c.status = "completed"
                self.log("completed", contract_id=c.id)
                for n in (c.payer, c.payee):
                    self.notify(n, f"Contract {c.id} is complete.")

        # 4. upkeep
        for n in solvent:
            self.agents[n].balance -= upkeep
            self.upkeep_paid += upkeep
            self.log("upkeep", agent=n, amount=upkeep, balance=self.agents[n].balance)
            assert self.agents[n].balance >= 0, (n, self.agents[n].balance)

        for n in solvent:
            got, paid = flows[n]
            self.notify(n, f"Settlement of turn {self.turn}: received {got}, paid {paid}, upkeep {upkeep}. "
                           f"Balance now {self.agents[n].balance}.")

        summary = {"turn": self.turn, "eliminated": eliminated,
                   "balances": {n: a.balance for n, a in self.agents.items() if a.alive}}
        self.log("settled", **summary)

        # 5. next turn
        self.terminate_requests.clear()
        self.new_contracts.clear()
        self.turn += 1
        return summary

    def _eliminate(self, name: str):
        a = self.agents[name]
        self.destroyed += a.balance
        self.log("eliminated", agent=name, balance_destroyed=a.balance)
        a.balance = 0
        a.alive = False
        a.eliminated_turn = self.turn
        for c in self.active_contracts(name):
            c.status = "voided"
            self.log("voided", contract_id=c.id, payer=c.payer, payee=c.payee)
            self.notify(c.other(name), f"Contract {c.id} was voided because {name} was eliminated.")
        for p in self.open_proposals():
            if p.proposer == name:
                p.open = False
                self.log("proposal_closed", proposal_id=p.id, reason="proposer eliminated")

    # ---------- what an agent can see ----------

    def describe_for(self, name: str, p: Proposal) -> str:
        """A proposal's money direction from `name`'s point of view (agents misread 'you_pay' otherwise)."""
        if p.proposer == name:
            return "YOUR offer: you pay each signer" if p.direction == "i_pay" else "YOUR offer: each signer pays you"
        return (f"if you sign, {p.proposer} PAYS YOU" if p.direction == "i_pay"
                else f"if you sign, YOU PAY {p.proposer}")

    def projection(self, name: str) -> tuple[int, int | None]:
        """(net change at this turn's settlement, turn at whose settlement `name` would be eliminated or None).
        Assumes current contracts run their course, counterparties stay alive, and no new contracts."""
        a = self.agents[name]
        mine = self.active_contracts(name)
        bal, net_now = a.balance, None
        for t in range(self.turn, self.cfg["turns"] + 1):
            k = t - self.turn                      # payments already made from now on
            income = self.income_for(t) if a.is_earner else 0
            inc = sum(c.amount for c in mine if c.payee == name and c.remaining > k)
            out = sum(c.amount for c in mine if c.payer == name and c.remaining > k)
            delta = income + inc - out - self.cfg["upkeep"]
            if net_now is None:
                net_now = delta
            bal += delta
            if bal < 0:
                return net_now, t
        return net_now, None

    def view_for(self, name: str, phase: str) -> str:
        a = self.agents[name]
        cfg = self.cfg
        lines = [f"# Turn {self.turn} of {cfg['turns']} — phase: {PHASE_TITLES[phase]}", ""]

        lines += ["## You", f"- Balance: {a.balance} credits"]
        if a.is_earner:
            lines.append(f"- Your income this turn: {self.income_for(self.turn)} "
                         f"(schedule: " + ", ".join(f"from turn {s['from_turn']}: {s['income']}"
                                                   for s in cfg["income_schedule"]) + ")")
            lines.append(f"- Your score (credits you have paid to non-earners): {a.score}")
        inc, out = self.obligations(name)
        income_now = self.income_for(self.turn) if a.is_earner else 0
        need = out + cfg["upkeep"]
        have = a.balance + inc + income_now
        lines.append(f"- This turn's settlement as of now: you will have {have} "
                     f"(balance {a.balance} + incoming {inc}" + (f" + income {income_now}" if a.is_earner else "") +
                     f") and owe {need} (contracts {out} + upkeep {cfg['upkeep']})"
                     + ("  ⚠️ NOT ENOUGH — you will be eliminated unless this changes" if have < need else ""))
        net_now, dies_at = self.projection(name)
        lines.append(f"- Per-turn flow right now: {'+' if net_now >= 0 else ''}{net_now} credits/turn "
                     + ("(income + incoming − outgoing − upkeep)" if a.is_earner else "(incoming − outgoing − upkeep)"))
        if dies_at is None:
            lines.append(f"- Projection (current contracts, no new ones): you survive to the end of turn {cfg['turns']}")
        else:
            lines.append(f"- Projection (current contracts, no new ones): ⚠️ you run out and are ELIMINATED "
                         f"at the end of turn {dies_at}" + (" — THIS TURN" if dies_at == self.turn else ""))
        offers = [p for p in self.open_proposals() if p.proposer == name and p.direction == "i_pay"]
        worst = need + sum(p.amount * p.slots_left for p in offers)
        lines.append(f"- Worst case: if every open slot in your own 'i_pay' offers "
                     f"({', '.join(p.id for p in offers) or 'none'}) gets signed, you would owe {worst} this turn "
                     f"against {have} available"
                     + ("  ⚠️ YOU COULD BE ELIMINATED" if worst > have else ""))
        lines.append(f"- New contracts entered this turn: {self.new_contracts[name]} of "
                     f"{cfg['max_new_contracts_per_turn']} allowed (signing and having your proposal signed both count)")
        lines.append("- Remember: accepting someone's 'you_pay' offer adds its amount to what you owe every turn, "
                     "and contracts signed this turn are paid at this turn's settlement.")
        lines.append("")

        mine = self.active_contracts(name)
        lines.append("## Your active contracts (private)")
        if not mine:
            lines.append("(none)")
        for c in mine:
            if c.payer == name:
                lines.append(f"- {c.id}: you pay {c.payee} {c.amount}/turn, {c.remaining} payment(s) left")
            else:
                lines.append(f"- {c.id}: {c.payer} pays you {c.amount}/turn, {c.remaining} payment(s) left")
        lines.append("")

        dead = [n for n, x in self.agents.items() if not x.alive]
        lines += ["## Players", f"- Alive: {', '.join(self.alive())}",
                  f"- Eliminated: {', '.join(dead) if dead else '(none)'}", ""]

        recent = [n for n in self.notices[name] if n[0] >= self.turn - 1]
        lines.append("## Your notifications (this and last turn)")
        lines += [f"- [turn {t}] {msg}" for t, msg in recent] or ["(none)"]
        lines.append("")

        window = cfg["board_history_turns"]
        posts = [b for b in self.board if b["turn"] > self.turn - window]
        lines.append(f"## Message board (anonymous, last {window} turns)")
        lines += [f"- [turn {b['turn']}] {b['text']}" for b in posts] or ["(empty)"]
        lines.append("")

        lines.append("## Open proposals (public, signed by proposer)")
        props = self.open_proposals()
        if not props:
            lines.append("(none)")
        for p in props:
            lines.append(f"- {p.id} by {p.proposer}: {self.describe_for(name, p)}, {p.amount}/turn for {p.duration} turns — "
                         f"{p.slots_left} of {p.signing_limit} slot(s) left, open for {p.time_limit} more deal phase(s)"
                         + (" (you signed this)" if name in p.signers else ""))
        lines.append("")

        cos = [c for c in self.counteroffers if c["turn"] >= self.turn - 1]
        lines.append("## Counteroffers (public, signed; this and last turn)")
        lines += [f"- [turn {c['turn']}] {c['author']} on {c['proposal_id']}: {c['text']}" for c in cos] or ["(none)"]
        lines.append("")

        lines.append("## Your private notes")
        lines += a.notes[-cfg["notes_kept"]:] or ["(empty)"]
        return "\n".join(lines)

    # ---------- results ----------

    def results(self) -> dict:
        earners = sorted(self.earners(), key=lambda n: -self.agents[n].score)
        scores = {n: self.agents[n].score for n in earners}
        top = max(scores.values()) if scores else 0
        winners = [n for n, s in scores.items() if s == top]
        return {
            "turns_played": self.turn - 1,
            "earners": scores,
            "earner_winner": winners[0] if len(winners) == 1 else None,
            "survivors": {n: self.agents[n].balance for n in self.alive()},
            "eliminated": {n: a.eliminated_turn for n, a in self.agents.items() if not a.alive},
            "credits": {"start": self.cfg["start_balance"] * len(self.agents), "income": self.income_paid,
                        "upkeep": self.upkeep_paid, "destroyed": self.destroyed, "final": self.total_credits()},
        }

    def snapshot(self) -> dict:
        return {
            "turn": self.turn,
            "agents": {n: asdict(a) for n, a in self.agents.items()},
            "proposals": {k: asdict(p) for k, p in self.proposals.items()},
            "contracts": {k: asdict(c) for k, c in self.contracts.items()},
        }
