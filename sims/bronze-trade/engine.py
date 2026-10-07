"""The simulation: calendar, event queue, captains, taverns and the port-session procedure (RULES.md §3).

There are no turns. Events (a ship arriving, a waiting deadline) sit in a priority queue by day.
For each day, events are grouped by port and each port runs one session:

    newcomers' briefing + first trade (random order, waiters still asleep)
    -> waiting captains woken -> tavern talk rounds -> everyone's final decisions (random order)

A player object makes the decisions; it calls back into the Sim's action methods
(buy / sell / note / say / sail / wait / done_trading), which validate and apply them immediately.
"""

from __future__ import annotations

import heapq
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Callable

from world import Market, build_markets, sailing_days

ROMAN = ["", " II", " III", " IV", " V", " VI", " VII", " VIII", " IX", " X"]


@dataclass
class Captain:
    id: str
    name: str
    home: str
    persona: str
    silver: float
    cargo: dict[str, int] = field(default_factory=dict)
    state: str = "sea"             # sea | port (awake) | waiting (asleep in port) | stranded
    port: str | None = None        # current port when in port or waiting
    dest: str | None = None        # destination when at sea
    arrive_day: int | None = None
    wait_until: int | None = None
    wait_token: int = 0            # bumps on every new wait, so stale deadlines are ignored
    paid_until: int = 0            # provisions charged up to this day
    stage: str | None = None       # first | talk | final while acting in a session
    decided: bool = False          # set by sail/wait (or done_trading in the first stage)
    logbook: dict[str, dict] = field(default_factory=dict)   # port -> {"day", "quote"}
    notes: list[str] = field(default_factory=list)

    def load(self) -> int:
        return sum(self.cargo.values())


class Sim:
    def __init__(self, config: dict, seed: int = 0, event_sink: Callable[[dict], None] | None = None,
                 n_captains: int | None = None, days: int | None = None):
        self.cfg = config
        self.seed = seed
        self.days = days or config["days"]
        self.event_sink = event_sink
        self._lock = threading.RLock()
        self.markets: dict[str, Market] = build_markets(config, seed)
        self.sailing = sailing_days(config)
        self.day = 0
        self.queue: list[tuple] = []          # (day, seq, kind, captain_id, port, token)
        self._seq = 0
        self.barkeep: dict[str, list[dict]] = {p: [] for p in config["ports"]}   # every statement, per port
        self.tavern_today: dict[str, list[dict]] = {p: [] for p in config["ports"]}
        self._pending: dict[str, list[dict]] = {p: [] for p in config["ports"]}   # this talk round's statements
        self.captains: dict[str, Captain] = {}
        self._make_captains(n_captains or config["captains"])
        self.log("setup", seed=seed, days=self.days,
                 captains={c.id: {"name": c.name, "home": c.home} for c in self.captains.values()},
                 sailing=self.sailing)

    # ---------- setup ----------

    def _make_captains(self, n: int):
        origins = self.cfg["origins"]
        homes = list(origins)
        used: dict[str, int] = {}
        start = self.cfg["ship"]["start_silver"]
        for i in range(n):
            home = homes[i % len(homes)]
            names = origins[home]["names"]
            base = names[(i // len(homes)) % len(names)]
            k = used.get(base, 0)
            used[base] = k + 1
            name = base + ROMAN[k] if k < len(ROMAN) else f"{base} {k + 1}"
            cid = name.lower().replace(" ", "_").replace("-", "_")
            c = Captain(cid, name, home, origins[home]["persona"], float(start))
            self.captains[cid] = c
            c.dest, c.arrive_day = home, 0                       # everyone "arrives" home on day 0
            self._push(0, "arrive", cid, home)

    # ---------- bookkeeping ----------

    def log(self, kind: str, **data):
        event = {"day": self.day, "event": kind, **data}
        with self._lock:
            if self.event_sink:
                self.event_sink(event)

    def _push(self, day: int, kind: str, cid: str, port: str, token: int = 0):
        with self._lock:
            heapq.heappush(self.queue, (day, self._seq, kind, cid, port, token))
            self._seq += 1

    def _charge(self, c: Captain, day: int):
        cost = (day - c.paid_until) * self.cfg["ship"]["provisions_per_day"]
        if cost > 0:
            c.silver -= cost
            c.paid_until = day

    def _observe(self, c: Captain, day: int):
        q = self.markets[c.port].quote()
        c.logbook[c.port] = {"day": day, "quote": q}
        self.log("observe", captain=c.id, port=c.port, quote=q)

    def present(self, port: str) -> list[Captain]:
        return [c for c in self.captains.values() if c.port == port and c.state in ("port", "waiting")]

    # ---------- actions (called by players; applied immediately) ----------

    def _check(self, cid: str, stages: tuple[str, ...]) -> Captain | str:
        c = self.captains.get(cid)
        if c is None or c.state != "port" or c.stage not in stages:
            return f"error: not allowed now (stage {c.stage if c else '?'})"
        return c

    def buy(self, cid: str, good: str, qty) -> str:
        c = self._check(cid, ("first", "final"))
        if isinstance(c, str):
            return c
        mk = self.markets[c.port]
        good = str(good).strip().lower()
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            return "error: qty must be a whole number"
        if good not in mk.goods:
            return f"error: {good} is not traded at {c.port}"
        if qty < 1:
            return "error: qty must be at least 1"
        if qty > int(mk.stock[good]):
            return f"error: only {int(mk.stock[good])} {good} in stock"
        if c.load() + qty > self.cfg["ship"]["capacity"]:
            return f"error: only {self.cfg['ship']['capacity'] - c.load()} units of free space"
        cost = mk.cost_to_buy(good, qty)
        if cost > c.silver + 1e-9:
            return f"error: {qty} {good} would cost {cost:.2f} but you have {c.silver:.2f} silver"
        before = mk.buy_price(good)
        mk.buy(good, qty)
        c.silver -= cost
        c.cargo[good] = c.cargo.get(good, 0) + qty
        self.log("trade", captain=c.id, port=c.port, side="buy", good=good, qty=qty, total=round(cost, 2),
                 price_before=round(before, 2), price_after=round(mk.buy_price(good), 2), stage=c.stage,
                 silver=round(c.silver, 2), cargo=dict(c.cargo))
        return (f"bought {qty} {good} for {cost:.2f} (avg {cost / qty:.2f}); next unit now costs "
                f"{mk.buy_price(good):.2f}. Silver {c.silver:.2f}, cargo {self.cargo_text(c)}")

    def sell(self, cid: str, good: str, qty) -> str:
        c = self._check(cid, ("first", "final"))
        if isinstance(c, str):
            return c
        mk = self.markets[c.port]
        good = str(good).strip().lower()
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            return "error: qty must be a whole number"
        if good not in mk.goods:
            return f"error: {good} is not traded at {c.port} — nobody here will buy it"
        if qty < 1 or qty > c.cargo.get(good, 0):
            return f"error: you have {c.cargo.get(good, 0)} {good}"
        before = mk.sell_price(good)
        got = mk.sell(good, qty)
        c.silver += got
        c.cargo[good] -= qty
        if not c.cargo[good]:
            del c.cargo[good]
        self.log("trade", captain=c.id, port=c.port, side="sell", good=good, qty=qty, total=round(got, 2),
                 price_before=round(before, 2), price_after=round(mk.sell_price(good), 2), stage=c.stage,
                 silver=round(c.silver, 2), cargo=dict(c.cargo))
        return (f"sold {qty} {good} for {got:.2f} (avg {got / qty:.2f}); next unit now fetches "
                f"{mk.sell_price(good):.2f}. Silver {c.silver:.2f}, cargo {self.cargo_text(c)}")

    def note(self, cid: str, text: str) -> str:
        c = self.captains[cid]
        text = " ".join(str(text).split())
        if text:
            c.notes.append(f"[day {self.day}, {c.port}] {text}")
            self.log("note", captain=cid, port=c.port, text=text)
        return "noted"

    def say(self, cid: str, text: str) -> str:
        c = self._check(cid, ("talk",))
        if isinstance(c, str):
            return c
        text = " ".join(str(text).split())
        if not text:
            return "error: empty statement"
        limit = self.cfg["statement_limit"]
        if len(text) > limit:
            self.log("truncated", captain=cid, original=text)
            text = text[:limit]
        with self._lock:
            self._pending[c.port].append({"speaker": cid, "text": text})
        c.decided = True
        return "said"

    def stay_silent(self, cid: str) -> str:
        c = self._check(cid, ("talk",))
        if isinstance(c, str):
            return c
        c.decided = True
        return "you stay silent"

    def done_trading(self, cid: str) -> str:
        c = self._check(cid, ("first",))
        if isinstance(c, str):
            return c
        c.decided = True
        return "done with your first trades"

    def sail(self, cid: str, dest: str) -> str:
        c = self._check(cid, ("final",))
        if isinstance(c, str):
            return c
        dest = next((p for p in self.markets if p.lower() == str(dest).strip().lower()), None)
        if dest is None:
            return f"error: unknown port. Ports: {', '.join(self.markets)}"
        if dest == c.port:
            return "error: you are already there (use wait to stay)"
        days = self.sailing[c.port][dest]
        self._observe(c, self.day)                                 # remember prices as you leave them
        c.state, c.dest, c.arrive_day, c.stage, c.decided = "sea", dest, self.day + days, None, True
        self.log("sail", captain=cid, origin=c.port, dest=dest, arrive_day=c.arrive_day, cargo=dict(c.cargo),
                 silver=round(c.silver, 2))
        c.port = None
        self._push(c.arrive_day, "arrive", cid, dest)
        return f"you set sail for {dest}; you will sleep until you arrive on day {c.arrive_day}"

    def wait(self, cid: str, days) -> str:
        c = self._check(cid, ("final",))
        if isinstance(c, str):
            return c
        try:
            days = int(days)
        except (TypeError, ValueError):
            return "error: days must be a whole number"
        if not 1 <= days <= self.cfg["max_wait_days"]:
            return f"error: days must be 1-{self.cfg['max_wait_days']}"
        self._set_waiting(c, days)
        return (f"you wait in {c.port}; you will be woken when another ship arrives, "
                f"or on day {c.wait_until} at the latest")

    def _set_waiting(self, c: Captain, days: int):
        c.state, c.stage, c.decided = "waiting", None, True
        c.wait_until = self.day + days
        c.wait_token += 1
        self.log("wait", captain=c.id, port=c.port, until=c.wait_until, silver=round(c.silver, 2),
                 cargo=dict(c.cargo))
        self._push(c.wait_until, "deadline", c.id, c.port, c.wait_token)

    # ---------- the event loop ----------

    def run(self, player, port_workers: int = 9, talk_workers: int = 50):
        self._talk_pool = ThreadPoolExecutor(max_workers=talk_workers)
        try:
            self._loop(player, port_workers)
        finally:
            self._talk_pool.shutdown(cancel_futures=True)
        self.day = self.days
        return self.finish()

    def _loop(self, player, port_workers: int):
        with ThreadPoolExecutor(max_workers=port_workers) as ports_pool:
            while self.queue and self.queue[0][0] <= self.days:
                day = self.queue[0][0]
                arrivals: dict[str, list[str]] = {}
                deadlines: dict[str, list[str]] = {}
                while self.queue and self.queue[0][0] == day:
                    _, _, kind, cid, port, token = heapq.heappop(self.queue)
                    c = self.captains[cid]
                    if kind == "arrive" and c.state == "sea" and c.dest == port and c.arrive_day == day:
                        arrivals.setdefault(port, []).append(cid)
                    elif (kind == "deadline" and c.state == "waiting" and c.port == port
                          and c.wait_token == token):
                        deadlines.setdefault(port, []).append(cid)
                self.day = day
                ports = sorted(set(arrivals) | set(deadlines))
                futures = [ports_pool.submit(self.session, p, day, arrivals.get(p, []), deadlines.get(p, []), player)
                           for p in ports]
                for f in futures:
                    f.result()

    def session(self, port: str, day: int, arriving: list[str], deadline: list[str], player):
        rng = random.Random(f"{self.seed}-{day}-{port}")
        mk = self.markets[port]
        mk.advance(day)
        self.tavern_today[port] = []

        newcomers = [self.captains[cid] for cid in arriving]
        for c in newcomers:
            c.state, c.port, c.dest, c.arrive_day = "port", port, None, None
            self._charge(c, day)
            dues = self.cfg["ship"].get("harbor_dues", 0) if day > 0 else 0   # no dues for the home start
            c.silver -= dues
            self.log("arrive", captain=c.id, port=port, cargo=dict(c.cargo), silver=round(c.silver, 2), dues=dues)
            self._observe(c, day)

        expiring = [self.captains[cid] for cid in deadline]
        sleepers = [c for c in self.present(port) if c.state == "waiting" and c not in expiring]
        to_wake = (sleepers + expiring) if newcomers else expiring
        everyone = newcomers + to_wake
        self.log("session", port=port, newcomers=[c.id for c in newcomers], woken=[c.id for c in to_wake],
                 still_asleep=[c.id for c in sleepers if c not in to_wake],
                 stock={g: round(s, 1) for g, s in mk.stock.items()})

        if len(everyone) == 1:                                     # alone: one combined decision
            c = everyone[0]
            if c in to_wake:
                self._wake(c, day, "deadline")
            self._final(c, player)
            return

        for c in rng.sample(newcomers, len(newcomers)):            # newcomers trade first
            c.stage, c.decided = "first", False
            player.first_trade(self, c.id)
            c.stage = None
        for c in to_wake:
            self._wake(c, day, "arrival" if newcomers else "deadline")

        for r in range(self.cfg["talk_rounds"]):                   # tavern: simultaneous rounds
            with self._lock:
                self._pending[port] = []
            for c in everyone:
                c.stage, c.decided = "talk", False
            list(self._talk_pool.map(lambda cc: player.talk(self, cc.id, r + 1), everyone))
            listeners = [c.id for c in everyone]
            for s in rng.sample(self._pending[port], len(self._pending[port])):
                entry = {"day": day, "port": port, "round": r + 1, "speaker": s["speaker"],
                         "name": self.captains[s["speaker"]].name, "text": s["text"], "listeners": listeners}
                self.tavern_today[port].append(entry)
                self.barkeep[port].append(entry)
                self.log("statement", **{k: v for k, v in entry.items() if k != "day"})
            for c in everyone:
                c.stage = None

        for c in rng.sample(everyone, len(everyone)):              # final decisions
            self._final(c, player)

    def _wake(self, c: Captain, day: int, reason: str):
        c.state = "port"
        self._charge(c, day)
        self.log("wake", captain=c.id, port=c.port, reason=reason, silver=round(c.silver, 2),
                 cargo=dict(c.cargo))
        self._observe(c, day)

    def _final(self, c: Captain, player):
        c.stage, c.decided = "final", False
        player.final(self, c.id)
        if c.state == "port":                                      # no sail/wait chosen: default wait
            self.log("default_wait", captain=c.id)
            self._set_waiting(c, self.cfg["default_wait_days"])
        if c.state == "waiting":
            self._observe(c, self.day)
        if c.silver <= 0 and not c.cargo:
            c.state, c.port, c.dest = "stranded", None, None
            self.log("stranded", captain=c.id, silver=round(c.silver, 2))

    # ---------- what a captain sees ----------

    def max_affordable(self, c: Captain, good: str) -> int:
        """Largest qty this captain could buy right now (stock, free space and silver all allow it)."""
        mk = self.markets[c.port]
        hi = min(int(mk.stock[good]), self.cfg["ship"]["capacity"] - c.load())
        lo = 0
        while lo < hi:                                             # binary search: cost grows with qty
            mid = (lo + hi + 1) // 2
            if mk.cost_to_buy(good, mid) <= c.silver + 1e-9:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def cargo_text(self, c: Captain) -> str:
        return ", ".join(f"{q} {g}" for g, q in sorted(c.cargo.items())) or "empty"

    def briefing(self, cid: str) -> str:
        c = self.captains[cid]
        port, mk, cfg = c.port, self.markets[c.port], self.cfg
        cap = cfg["ship"]["capacity"]
        stage_text = {
            "first": "You have just ARRIVED. You trade FIRST, before the captains waiting here wake up.",
            "talk": "You are in the TAVERN with the other captains in port.",
            "final": "FINAL DECISIONS: trade if you like, then set sail or wait.",
        }[c.stage]
        if c.stage == "final" and not [o for o in self.present(port) if o.id != c.id]:
            stage_text = "You are ALONE in port: trade if you like, then set sail or wait."
        lines = [f"# Day {self.day} of {self.days} — {c.name} at {port} ({cfg['ports'][port]['region']})",
                 stage_text, ""]

        lines += ["## Your ship", f"- Silver: {c.silver:.2f} shekels",
                  f"- Cargo: {self.cargo_text(c)} ({c.load()}/{cap} units, {cap - c.load()} free)",
                  f"- Provisions: {cfg['ship']['provisions_per_day']} shekels/day; harbor dues "
                  f"{cfg['ship'].get('harbor_dues', 0)} shekels per arrival", ""]

        lines += [f"## Market at {port} today (prices move with every unit you trade)",
                  "| good | you buy at | you sell at | stock | most you can buy now | 10 units would cost / fetch |",
                  "|---|---|---|---|---|---|"]
        for g, (b, s, st) in mk.quote().items():
            cost10 = f"{mk.cost_to_buy(g, 10):.1f}" if st >= 10 else "—"
            lines.append(f"| {g} | {b} | {s} | {st} | {self.max_affordable(c, g)} | "
                         f"{cost10} / {mk.proceeds_of_sale(g, 10):.1f} |")
        untradeable = [g for g in c.cargo if g not in mk.goods]
        if untradeable:
            lines.append(f"(Not traded here, so you can't sell it here: {', '.join(untradeable)})")
        lines.append("")

        others = [o for o in self.present(port) if o.id != c.id]
        lines.append("## Captains in port")
        for o in others:
            status = "asleep, waiting" if o.state == "waiting" else "awake"
            lines.append(f"- {o.name} of {o.home} ({status})")
        if not others:
            lines.append("(none — you are alone)")
        lines.append("")

        if self.tavern_today[port]:
            lines.append("## Said in the tavern today")
            lines += [f"- {e['name']}: \"{e['text']}\"" for e in self.tavern_today[port]]
            lines.append("")

        past = [e for e in self.barkeep[port] if e["day"] < self.day][-cfg["barkeep_shown"]:]
        lines.append(f"## The barkeep remembers (earlier talk in this tavern, last {cfg['barkeep_shown']})")
        lines += [f"- [day {e['day']}] {e['name']}: \"{e['text']}\"" for e in past] or ["(nothing yet)"]
        lines.append("")

        lines.append("## Your logbook (prices you saw yourself: you buy at / you sell at, stock)")
        for p, entry in sorted(c.logbook.items(), key=lambda kv: -kv[1]["day"]):
            if p == port:
                continue
            items = "; ".join(f"{g} {b}/{s} ({st})" for g, (b, s, st) in entry["quote"].items())
            lines.append(f"- {p}, seen day {entry['day']}: {items}")
        if len(c.logbook) <= 1:
            lines.append("(no other ports seen yet)")
        lines.append("")

        lines.append("## Your notes")
        lines += c.notes[-cfg["notes_kept"]:] or ["(none)"]
        lines.append("")

        lines.append(f"## Sailing times from {port} (days)")
        lines.append(", ".join(f"{p} {d}" for p, d in sorted(self.sailing[port].items(), key=lambda kv: kv[1])
                               if p != port))
        return "\n".join(lines)

    # ---------- end ----------

    def value_of(self, c: Captain, good: str, qty: int) -> float:
        """Cargo at the last sell price this captain saw anywhere for that good."""
        seen = [(e["day"], e["quote"][good][1]) for e in c.logbook.values() if good in e["quote"]]
        price = max(seen)[1] if seen else self.cfg["goods"][good] * self.cfg["market"]["price_min"]
        return qty * price

    def finish(self) -> dict:
        scores = {}
        for c in self.captains.values():
            if c.state != "stranded":
                self._charge(c, self.days)
            cargo_value = sum(self.value_of(c, g, q) for g, q in c.cargo.items())
            scores[c.id] = {"name": c.name, "home": c.home, "state": c.state, "silver": round(c.silver, 2),
                            "cargo": dict(c.cargo), "cargo_value": round(cargo_value, 2),
                            "score": round(c.silver + cargo_value, 2)}
        ranking = sorted(scores, key=lambda k: -scores[k]["score"])
        self.log("finish", scores=scores, ranking=ranking)
        return {"scores": scores, "ranking": ranking}
