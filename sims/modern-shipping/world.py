"""Port markets with any number of production recipes. Pure and deterministic: no captains here.

Pricing and price impact are the same model as bronze-trade/world.py:
    price = base × (target / stock) ^ elasticity, clamped to [price_min, price_max] × base
    captains buy at price × (1 + spread) and sell at price × (1 − spread), unit by unit

Each day (advance): raw production up to the storage cap, then every recipe runs its (possibly fractional)
batches while it has the inputs and room for the output, then drifting consumption (pauses at 0).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

FUEL = "fuel"


@dataclass
class Good:
    name: str
    base: float
    target: float
    cap: float
    produce: float = 0.0
    consume: float = 0.0


@dataclass
class Recipe:
    name: str
    inputs: dict[str, float]
    outputs: dict[str, float]
    rate: float                      # batches per day
    progress: float = 0.0
    blocked: str = ""                 # why it stopped today: "" | "no <input>" | "<output> full"
    blocked_days: dict = field(default_factory=dict)

    def run(self, stock: dict[str, float], goods: dict[str, Good]) -> int:
        """Run today's batches. Returns how many ran."""
        self.progress = min(self.progress + self.rate, max(1.0, self.rate))
        made = 0
        while (self.progress >= 1 - 1e-9
               and all(stock[g] >= q for g, q in self.inputs.items())
               and all(stock[g] + q <= goods[g].cap for g, q in self.outputs.items())):
            for g, q in self.inputs.items():
                stock[g] -= q
            for g, q in self.outputs.items():
                stock[g] += q
            self.progress -= 1
            made += 1
        self.blocked = ""
        if self.progress >= 1 - 1e-9:
            short = [g for g, q in self.inputs.items() if stock[g] < q]
            full = [g for g, q in self.outputs.items() if stock[g] + q > goods[g].cap]
            self.blocked = f"no {short[0]}" if short else (f"{full[0]} full" if full else "")
            if self.blocked:
                self.blocked_days[self.blocked] = self.blocked_days.get(self.blocked, 0) + 1
        return made


@dataclass
class Market:
    port: str
    goods: dict[str, Good]
    stock: dict[str, float]
    recipes: list[Recipe]
    cfg: dict
    rng: random.Random
    day: int = 0
    demand: dict[str, float] = field(default_factory=dict)
    made_today: dict[str, int] = field(default_factory=dict)

    # ---------- pricing ----------

    def price(self, good: str, stock: float | None = None) -> float:
        g = self.goods[good]
        s = self.stock[good] if stock is None else stock
        ratio = (g.target / max(s, 0.5)) ** self.cfg["elasticity"]
        return g.base * min(max(ratio, self.cfg["price_min"]), self.cfg["price_max"])

    def buy_price(self, good: str) -> float:
        return self.price(good) * (1 + self.cfg["spread"])

    def sell_price(self, good: str) -> float:
        return self.price(good) * (1 - self.cfg["spread"])

    def cost_to_buy(self, good: str, qty: float) -> float:
        s, n = self.stock[good], int(qty)
        return sum(self.price(good, s - i) for i in range(n)) * (1 + self.cfg["spread"])

    def proceeds_of_sale(self, good: str, qty: float) -> float:
        s, n = self.stock[good], int(qty)
        return sum(self.price(good, s + i) for i in range(n)) * (1 - self.cfg["spread"])

    def buy(self, good: str, qty: int) -> float:
        total = self.cost_to_buy(good, qty)
        self.stock[good] -= qty
        return total

    def sell(self, good: str, qty: int) -> float:
        total = self.proceeds_of_sale(good, qty)
        self.stock[good] += qty
        return total

    def quote(self) -> dict[str, list]:
        """{good: [captain buys at, captain sells at, whole units in stock, demand multiplier]}"""
        return {g: [round(self.buy_price(g), 2), round(self.sell_price(g), 2), int(self.stock[g]),
                    round(self.demand.get(g, 1.0), 2)] for g in self.goods}

    # ---------- daily flows ----------

    def advance(self, to_day: int):
        while self.day < to_day:
            self.day += 1
            for g in self.goods.values():
                if g.produce:
                    self.stock[g.name] = min(g.cap, self.stock[g.name] + g.produce)
            self.made_today = {r.name: r.run(self.stock, self.goods) for r in self.recipes}
            self._drift()
            for g in self.goods.values():
                if g.consume:
                    self.stock[g.name] = max(0.0, self.stock[g.name] - g.consume * self.demand.get(g.name, 1.0))

    def _drift(self):
        d = self.cfg.get("demand_drift") or {}
        if not d.get("sigma"):
            return
        for g in self.goods.values():
            if g.consume:
                m = self.demand.get(g.name, 1.0) * math.exp(self.rng.gauss(0, d["sigma"]))
                m += d.get("revert", 0.05) * (1.0 - m)
                self.demand[g.name] = min(d.get("max", 2.0), max(d.get("min", 0.3), m))


def flow_scale(cfg: dict, n_captains: int) -> float:
    """How busy the world is. flow_scale is per ship: port flows always grow with the fleet
    (n_captains / reference_fleet), times this factor ("auto" = 1)."""
    s = cfg["market"].get("flow_scale", 1.0)
    return (1.0 if s == "auto" else float(s)) * n_captains / cfg["reference_fleet"]


def build_markets(cfg: dict, seed: int, n_captains: int) -> dict[str, Market]:
    """Every port trades: what it produces and consumes, its recipes' inputs and outputs, and fuel."""
    m = cfg["market"]
    scale = flow_scale(cfg, n_captains)
    markets = {}
    for port, p in cfg["ports"].items():
        produce = {g: r * scale for g, r in p["produce"].items()}
        consume = {g: r * scale for g, r in p["consume"].items()}
        recipes = []
        flow: dict[str, float] = {}
        for g, r in list(produce.items()) + list(consume.items()):
            flow[g] = max(flow.get(g, 0.0), r)
        for name, rate in p["recipes"].items():
            spec = cfg["recipes"][name]
            recipes.append(Recipe(name, spec["in"], spec["out"], rate * scale))
            for g, q in list(spec["in"].items()) + list(spec["out"].items()):
                flow[g] = max(flow.get(g, 0.0), q * rate * scale)
        flow.setdefault(FUEL, 0.0)
        goods, stock = {}, {}
        for g, f in sorted(flow.items()):
            target = max(m["min_target"], m["target_days"] * f)
            goods[g] = Good(g, cfg["goods"][g]["base"], target, m["storage_cap"] * target,
                            produce.get(g, 0.0), consume.get(g, 0.0))
            stock[g] = float(target)
        markets[port] = Market(port, goods, stock, recipes, m, random.Random(f"{seed}-{port}"))
    return markets
