"""Markets and the sea-lane map. Pure and deterministic: no agents, no API.

A Market holds one port's stock of every good it trades. It is updated lazily: advance(day) applies
the daily production, bronze-making and consumption for every day since it was last touched.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

BRONZE = "bronze"


@dataclass
class Good:
    name: str
    base: float          # base price in shekels
    target: float        # stock at which the price equals base
    cap: float           # production pauses at this stock
    produce: float = 0.0 # units/day
    consume: float = 0.0 # units/day


@dataclass
class Market:
    port: str
    goods: dict[str, Good]
    stock: dict[str, float]
    bronze_batches: float = 0        # batches/day of the bronze recipe this port can run (may be fractional)
    day: int = 0                     # last day applied
    cfg: dict = field(default_factory=dict)
    rng: random.Random = field(default_factory=random.Random)
    demand: dict[str, float] = field(default_factory=dict)   # drifting multiplier on each good's consumption
    bronze_progress: float = 0.0     # fractional batches carried over between days

    # ---------- pricing ----------

    def price(self, good: str, stock: float | None = None) -> float:
        """Mid price at a given stock (default: current)."""
        g = self.goods[good]
        s = self.stock[good] if stock is None else stock
        ratio = (g.target / max(s, 0.5)) ** self.cfg["elasticity"]
        ratio = min(max(ratio, self.cfg["price_min"]), self.cfg["price_max"])
        return g.base * ratio

    def buy_price(self, good: str) -> float:
        """What a captain pays for the next unit."""
        return self.price(good) * (1 + self.cfg["spread"])

    def sell_price(self, good: str) -> float:
        """What a captain receives for the next unit."""
        return self.price(good) * (1 - self.cfg["spread"])

    def quote(self) -> dict[str, tuple[float, float, int]]:
        """{good: (captain buys at, captain sells at, whole units in stock)}"""
        return {g: (round(self.buy_price(g), 2), round(self.sell_price(g), 2), int(self.stock[g]))
                for g in self.goods}

    # ---------- trading (every unit moves the price) ----------

    def cost_to_buy(self, good: str, qty: int) -> float:
        s = self.stock[good]
        return sum(self.price(good, s - i) for i in range(qty)) * (1 + self.cfg["spread"])

    def proceeds_of_sale(self, good: str, qty: int) -> float:
        s = self.stock[good]
        return sum(self.price(good, s + i) for i in range(qty)) * (1 - self.cfg["spread"])

    def buy(self, good: str, qty: int) -> float:
        total = self.cost_to_buy(good, qty)
        self.stock[good] -= qty
        return total

    def sell(self, good: str, qty: int) -> float:
        total = self.proceeds_of_sale(good, qty)
        self.stock[good] += qty
        return total

    # ---------- daily flows ----------

    def advance(self, to_day: int):
        recipe = self.cfg["bronze_recipe"]
        while self.day < to_day:
            self.day += 1
            for g in self.goods.values():                      # raw production, up to storage cap
                if g.produce and g.name != BRONZE:
                    self.stock[g.name] = min(g.cap, self.stock[g.name] + g.produce)
            if self.bronze_batches:                             # bronze stops if an input runs out
                self.bronze_progress = min(self.bronze_progress + self.bronze_batches, max(1.0, self.bronze_batches))
                while (self.bronze_progress >= 1 - 1e-9 and self.stock.get("copper", 0) >= recipe["copper"]
                       and self.stock.get("tin", 0) >= recipe["tin"]
                       and self.stock[BRONZE] + recipe["out"] <= self.goods[BRONZE].cap):
                    self.stock["copper"] -= recipe["copper"]
                    self.stock["tin"] -= recipe["tin"]
                    self.stock[BRONZE] += recipe["out"]
                    self.bronze_progress -= 1
            self._drift()
            for g in self.goods.values():                      # consumption pauses at 0
                if g.consume:
                    rate = g.consume * self.demand.get(g.name, 1.0)
                    self.stock[g.name] = max(0.0, self.stock[g.name] - rate)

    def _drift(self):
        """Each day, every consumed good's demand multiplier takes a random step, pulled back toward 1.
        Deterministic per port (seeded), whatever the order in which ports are visited."""
        d = self.cfg.get("demand_drift") or {}
        sigma = d.get("sigma", 0)
        if not sigma:
            return
        for g in self.goods.values():
            if g.consume:
                m = self.demand.get(g.name, 1.0) * math.exp(self.rng.gauss(0, sigma))
                m += d.get("revert", 0.05) * (1.0 - m)
                self.demand[g.name] = min(d.get("max", 2.0), max(d.get("min", 0.3), m))


def build_markets(cfg: dict, seed: int = 0) -> dict[str, Market]:
    mcfg = cfg["market"]
    recipe = mcfg["bronze_recipe"]
    markets = {}
    scale = mcfg.get("flow_scale", 1.0)       # how busy the world is: scales every port's daily flows
    for port, p in cfg["ports"].items():
        produce = {g: r * scale for g, r in p.get("produce", {}).items()}
        consume = {g: r * scale for g, r in p.get("consume", {}).items()}
        batches = p.get("bronze_batches", 0) * scale
        traded = set(produce) | set(consume)
        if batches:
            traded |= {"copper", "tin", BRONZE}
        goods, stock = {}, {}
        for name in sorted(traded):
            flow = max(produce.get(name, 0), consume.get(name, 0))
            if batches and name == "copper":
                flow = max(flow, batches * recipe["copper"])
            elif batches and name == "tin":
                flow = max(flow, batches * recipe["tin"])
            elif batches and name == BRONZE:
                flow = max(flow, batches * recipe["out"])
            target = max(mcfg["min_target"], mcfg["target_days"] * flow)
            goods[name] = Good(name, cfg["goods"][name], target, mcfg["storage_cap"] * target,
                               produce.get(name, 0), consume.get(name, 0))
            stock[name] = float(target)
        markets[port] = Market(port, goods, stock, batches, 0, mcfg, random.Random(f"{seed}-{port}"))
    return markets


def sailing_days(cfg: dict) -> dict[str, dict[str, int]]:
    """All-pairs shortest sea route (Floyd-Warshall over the lanes), in whole days."""
    ports = list(cfg["ports"])
    inf = float("inf")
    dist = {a: {b: (0 if a == b else inf) for b in ports} for a in ports}
    for a, b, nm in cfg["lanes"]:
        dist[a][b] = dist[b][a] = min(dist[a][b], nm)
    for k in ports:
        for i in ports:
            for j in ports:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    speed = cfg["ship"]["speed_nm_per_day"]
    return {a: {b: (0 if a == b else max(1, math.ceil(dist[a][b] / speed))) for b in ports} for a in ports}
