"""Simple rule-of-thumb captains, for testing the engine and tuning the economy without API calls.

Each captain sells whatever this port will buy, buys the good that is cheapest here relative to its
base price, repeats a price from its logbook in the tavern, and sails somewhere at random (sometimes waits).
"""

from __future__ import annotations

import random


class FakePlayer:
    def __init__(self, seed: int = 0):
        self.seed = seed

    def _rng(self, sim, cid: str, tag: str) -> random.Random:
        return random.Random(f"{self.seed}-{cid}-{sim.day}-{tag}")

    def _sell_all(self, sim, cid: str):
        c = sim.captains[cid]
        for good, qty in list(c.cargo.items()):
            if good in sim.markets[c.port].goods:
                sim.sell(cid, good, qty)

    def _buy_cheapest(self, sim, cid: str, rng: random.Random):
        c = sim.captains[cid]
        mk = sim.markets[c.port]
        options = [g for g in mk.goods if mk.stock[g] >= 1]
        if not options or c.silver < 5:
            return
        good = min(options, key=lambda g: mk.buy_price(g) / sim.cfg["goods"][g] + rng.random() * 0.2)
        free = sim.cfg["ship"]["capacity"] - c.load()
        qty = min(free, int(mk.stock[good]))
        budget = c.silver * 0.8
        while qty > 0 and mk.cost_to_buy(good, qty) > budget:
            qty -= 1
        if qty > 0:
            sim.buy(cid, good, qty)

    def first_trade(self, sim, cid: str):
        self._sell_all(sim, cid)
        sim.done_trading(cid)

    def talk(self, sim, cid: str, round_no: int):
        c = sim.captains[cid]
        rng = self._rng(sim, cid, f"talk{round_no}")
        others = [(p, e) for p, e in c.logbook.items() if p != c.port]
        if others and rng.random() < 0.6:
            port, entry = rng.choice(others)
            good, (b, s, st) = rng.choice(list(entry["quote"].items()))
            sim.say(cid, f"{good} sold for {s} at {port} on day {entry['day']}")
        else:
            sim.stay_silent(cid)

    def final(self, sim, cid: str):
        rng = self._rng(sim, cid, "final")
        self._sell_all(sim, cid)
        self._buy_cheapest(sim, cid, rng)
        c = sim.captains[cid]
        if rng.random() < 0.15:
            sim.wait(cid, rng.randint(1, 4))
        else:
            sim.sail(cid, rng.choice([p for p in sim.markets if p != c.port]))
