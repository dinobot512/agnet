"""InformedPlayer: a rule-based captain (no model calls) that keeps a structured logbook, gossips, and plans.

What it may use: only what its captain could know. That is the market of the port it is in, its own past
observations (Sim's logbook), and statements it hears: today's tavern talk and the barkeep's log, both at
its current port. It never looks at other ports' markets.

Logbook (written with sim.note, so it is logged and shown in the captain's briefing). One line per record:

    PRICE port=Enkomi good=copper buy=4.06 sell=3.32 stock=400 day=10 src=seen
    PRICE port=Avaris good=tin buy=67.5 sell=55.2 stock=0 day=7 src=urtenu

Tavern talk uses the same line format, so other informed captains can parse what they hear. Free-text
statements (e.g. from model captains) are simply ignored.

Each wake-up:
  1. learn: record today's local prices, and parse any PRICE lines heard here that are newer than what it knows
  2. first trade: sell cargo if this port pays at least ~90% of the best net price it knows elsewhere
  3. talk: share one record, picked at random, weighted toward recent observations
  4. final: sell (same rule), then score every destination by value per day of sailing: expected profit
     on the cargo it holds plus the best good to buy here, plus a bonus for refreshing stale news
     (older than refresh_days). It sails to the best one, filling any free space with speculative cargo
     (whatever is cheapest here relative to prices it has seen elsewhere), so it rarely sails empty.
     If nothing is worth it, it waits 2 days.
"""

from __future__ import annotations

import math
import random
import re

LINE = re.compile(r"PRICE port=(?P<port>[\w-]+) good=(?P<good>[\w ]+?) buy=(?P<buy>[\d.]+) "
                  r"sell=(?P<sell>[\d.]+) stock=(?P<stock>\d+) day=(?P<day>\d+)(?: src=(?P<src>\S+))?")


def format_record(port: str, good: str, rec: dict, with_src: bool = True) -> str:
    line = (f"PRICE port={port} good={good} buy={rec['buy']} sell={rec['sell']} "
            f"stock={rec['stock']} day={rec['day']}")
    return line + (f" src={rec['src']}" if with_src else "")


def parse_records(text: str) -> list[dict]:
    out = []
    for m in LINE.finditer(text):
        d = m.groupdict()
        out.append({"port": d["port"], "good": d["good"].strip(), "buy": float(d["buy"]), "sell": float(d["sell"]),
                    "stock": int(d["stock"]), "day": int(d["day"]), "src": d["src"] or "?"})
    return out


class InformedPlayer:
    def __init__(self, seed: int = 0, recency_days: float = 7.0, stale_days: int = 20,
                 sell_threshold: float = 0.9, keep_silver: float = 5.0, refresh_days: int = 20,
                 info_value: float = 1.5):
        self.seed = seed
        self.recency_days = recency_days      # sharing weight halves roughly every 0.7 * this many days
        self.stale_days = stale_days          # older knowledge is trusted less
        self.sell_threshold = sell_threshold
        self.keep_silver = keep_silver
        self.refresh_days = refresh_days      # news older than this is worth sailing to refresh
        self.info_value = info_value          # shekels of value per day of staleness beyond refresh_days
        self.kb: dict[str, dict[tuple[str, str], dict]] = {}   # captain -> (port, good) -> record

    # ---------- knowledge ----------

    def _rng(self, sim, cid: str, tag: str) -> random.Random:
        return random.Random(f"informed-{self.seed}-{cid}-{sim.day}-{tag}")

    def _store(self, sim, cid: str, port: str, good: str, rec: dict) -> bool:
        kb = self.kb.setdefault(cid, {})
        old = kb.get((port, good))
        if old and old["day"] >= rec["day"]:
            return False
        kb[(port, good)] = rec
        sim.note(cid, format_record(port, good, rec))
        return True

    def _learn(self, sim, cid: str):
        c = sim.captains[cid]
        port = c.port
        for good, (b, s, st) in sim.markets[port].quote().items():          # what I see here, now
            self._store(sim, cid, port, good, {"buy": b, "sell": s, "stock": st, "day": sim.day, "src": "seen"})
        heard = list(sim.barkeep[port][-sim.cfg["barkeep_shown"]:]) + list(sim.tavern_today[port])
        for e in heard:                                                      # what I hear here
            if e["speaker"] == cid:
                continue
            for r in parse_records(e["text"]):
                if r["port"] in sim.markets:
                    self._store(sim, cid, r["port"], r["good"],
                                {"buy": r["buy"], "sell": r["sell"], "stock": r["stock"], "day": r["day"],
                                 "src": e["speaker"]})

    def _known(self, cid: str, port: str, good: str) -> dict | None:
        return self.kb.get(cid, {}).get((port, good))

    # ---------- estimates ----------

    def _expected_sale(self, sim, cid: str, port: str, good: str, qty: int) -> float:
        """Expected proceeds of selling qty at a remembered port, including our own price impact."""
        rec = self._known(cid, port, good)
        if not rec or qty <= 0:
            return 0.0
        s = max(rec["stock"], 1)
        e = sim.cfg["market"]["elasticity"]
        # average of (s/x)^e for x from s to s+qty: price falls as we add stock
        avg_factor = (((s + qty) ** (1 - e) - s ** (1 - e)) / ((1 - e) * qty)) * s ** e
        trust = 0.8 if sim.day - rec["day"] > self.stale_days else 1.0
        return qty * rec["sell"] * min(1.0, avg_factor) * trust

    def _best_elsewhere(self, sim, cid: str, good: str, qty: int) -> float:
        c = sim.captains[cid]
        prov = sim.cfg["ship"]["provisions_per_day"]
        dues = sim.cfg["ship"].get("harbor_dues", 0)
        best = 0.0
        for port in sim.markets:
            if port != c.port:
                best = max(best, self._expected_sale(sim, cid, port, good, qty) - prov * sim.sailing[c.port][port] - dues)
        return best

    def _sell_worthwhile(self, sim, cid: str):
        c = sim.captains[cid]
        mk = sim.markets[c.port]
        for good, qty in list(c.cargo.items()):
            if good not in mk.goods:
                continue
            here = mk.proceeds_of_sale(good, qty)
            if here >= self.sell_threshold * self._best_elsewhere(sim, cid, good, qty):
                sim.sell(cid, good, qty)

    # ---------- decisions ----------

    def first_trade(self, sim, cid: str):
        self._learn(sim, cid)
        self._sell_worthwhile(sim, cid)
        sim.done_trading(cid)

    def talk(self, sim, cid: str, round_no: int):
        self._learn(sim, cid)
        kb = self.kb.get(cid, {})
        if not kb:
            sim.stay_silent(cid)
            return
        rng = self._rng(sim, cid, f"talk{round_no}")
        items = list(kb.items())
        weights = [math.exp(-(sim.day - rec["day"]) / self.recency_days) for _, rec in items]
        (port, good), rec = rng.choices(items, weights=weights, k=1)[0]
        sim.say(cid, format_record(port, good, rec, with_src=False))

    def _staleness(self, sim, cid: str) -> dict[str, int]:
        """Days since the newest thing this captain knows about each port (unknown ports: very stale)."""
        newest = {}
        for (port, _), rec in self.kb.get(cid, {}).items():
            newest[port] = max(newest.get(port, -10**6), rec["day"])
        return {p: sim.day - newest.get(p, -10**6) for p in sim.markets}

    def _affordable(self, sim, cid: str, good: str, budget: float) -> int:
        c = sim.captains[cid]
        mk = sim.markets[c.port]
        qty = min(sim.cfg["ship"]["capacity"] - c.load(), int(mk.stock[good]))
        while qty > 0 and mk.cost_to_buy(good, qty) > budget:
            qty = int(qty * 0.8)
        return max(qty, 0)

    def _speculative(self, sim, cid: str, budget: float) -> tuple[str | None, int]:
        """Cargo to carry rather than sail empty: the good that is cheapest here compared with the average
        price this captain has seen it sell for at other ports (only if it is at least 10% cheaper)."""
        c = sim.captains[cid]
        mk = sim.markets[c.port]
        best = None
        for good in mk.goods:
            if good in c.cargo or mk.stock[good] < 1:
                continue
            seen = [r["sell"] for (p, g), r in self.kb.get(cid, {}).items() if g == good and p != c.port]
            if not seen:
                continue
            ratio = mk.buy_price(good) / (sum(seen) / len(seen))
            if ratio < 0.9 and (best is None or ratio < best[0]):
                best = (ratio, good)
        if not best:
            return None, 0
        return best[1], self._affordable(sim, cid, best[1], budget)

    def final(self, sim, cid: str):
        self._learn(sim, cid)
        self._sell_worthwhile(sim, cid)
        c = sim.captains[cid]
        here, mk = c.port, sim.markets[c.port]
        prov = sim.cfg["ship"]["provisions_per_day"]
        dues = sim.cfg["ship"].get("harbor_dues", 0)
        stale = self._staleness(sim, cid)

        best = None                                   # (value per day, dest, good to buy, qty)
        for dest in sim.markets:
            if dest == here:
                continue
            days = sim.sailing[here][dest]
            budget = max(0.0, c.silver - self.keep_silver - prov * days - dues)
            carried = sum(self._expected_sale(sim, cid, dest, g, q) for g, q in c.cargo.items())
            options = [(0.0, None, 0)]
            for good in mk.goods:
                if good in c.cargo or not self._known(cid, dest, good):
                    continue
                qty = self._affordable(sim, cid, good, budget)
                if qty > 0:
                    options.append((self._expected_sale(sim, cid, dest, good, qty) - mk.cost_to_buy(good, qty),
                                    good, qty))
            gain, good, qty = max(options, key=lambda o: o[0])
            # fresh news is worth something too: a bonus per day of staleness beyond refresh_days
            news = self.info_value * max(0, min(stale[dest], 60) - self.refresh_days)
            rate = (carried + gain + news - prov * days - dues) / days
            if best is None or rate > best[0]:
                best = (rate, dest, good, qty)

        if not best or best[0] <= 0 or c.silver < prov * 3 + dues:
            sim.wait(cid, 2)
            return
        _, dest, good, qty = best
        if good:
            sim.buy(cid, good, qty)
        days = sim.sailing[here][dest]
        spec, n = self._speculative(sim, cid, max(0.0, c.silver - self.keep_silver - prov * days - dues))
        if spec and n > 0:                            # never sail with free space if something is cheap here
            sim.buy(cid, spec, n)
        sim.sail(cid, dest)
