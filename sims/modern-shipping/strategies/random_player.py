"""Random baseline: sells what it can, buys a random good it can carry, sails somewhere random."""

from __future__ import annotations

import random

from strategies.common import affordable, ensure_fuel


class RandomPlayer:
    name = "random"

    def __init__(self, seed: int = 0):
        self.seed = seed

    def act(self, sim, cid: str):
        rng = random.Random(f"random-{self.seed}-{cid}-{sim.day}")
        v = sim.view(cid)
        mk = v.market(v.port)
        for good, qty in v.cargo.items():
            if good in mk.goods:
                sim.sell(cid, good, qty)
        v = sim.view(cid)
        if v.cash > 0 and v.fuel < v.tank * 0.6:
            sim.refuel(cid, min(v.tank - v.fuel, v.cash * 0.4 / max(mk.buy_price("fuel"), 1e-6)))
        v = sim.view(cid)
        options = [g for g in v.carries if g in mk.goods and mk.stock[g] >= 1]
        if options and v.cash > 20:
            good = rng.choice(options)
            qty = affordable(mk, good, v.cash * 0.6, v.capacity - sum(v.cargo.values()))
            if qty > 0:
                sim.buy(cid, good, qty)
        v = sim.view(cid)
        dests = [p for p in v.ports if p != v.port]
        rng.shuffle(dests)
        for dest in dests:
            policy = rng.choice(["shortest", "no_canals"])
            r = v.route(dest, policy)
            if r and r["fuel"] <= v.fuel and r["tolls"] <= v.cash:
                sim.sail(cid, dest, policy)
                return
        sim.wait(cid, 2)
