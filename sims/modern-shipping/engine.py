"""The modern shipping simulation: a day-by-day calendar of wake-ups, costs, and actions.

Each day: every market advances one day, then the captains waking that day (arrivals and ends of waits)
act one at a time in a seeded random order (first come, first served on stock), then the day's market
state is recorded for the viewer.

Strategies only get a View of the world: their own ship, every port's live market and the routes from
where they are. They never see other captains. Actions (buy / sell / refuel / sail / wait) are validated
and applied immediately; each returns a message starting with "error" if it was refused.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable

from network import Network
from world import FUEL, build_markets, flow_scale

ROMAN = ["", " II", " III", " IV", " V", " VI", " VII", " VIII", " IX", " X"]


@dataclass
class Captain:
    id: str
    name: str
    label: str
    strategy: str
    ship_type: str
    cash: float
    fuel: float
    cargo: dict[str, int] = field(default_factory=dict)
    state: str = "port"                 # port (acting) | sea | waiting | bankrupt
    port: str | None = None
    origin: str | None = None
    dest: str | None = None
    path: tuple[str, ...] = ()
    depart_day: int = 0
    arrive_day: int = 0
    wait_until: int = 0
    token: int = 0                      # bumps on every schedule change, so stale wake-ups are ignored
    paid_until: int = 0                 # crew paid up to this day
    stats: dict = field(default_factory=lambda: {"voyages": 0, "empty_voyages": 0, "days_at_sea": 0,
                                                 "canals": 0, "tolls": 0.0, "fuel_bought": 0.0,
                                                 "dues": 0.0, "crew": 0.0})

    def load(self) -> int:
        return sum(self.cargo.values())


class View:
    """What a strategy may know: its own ship, every market (live), routes and costs from here.
    Deliberately has no access to other captains."""

    def __init__(self, sim: "Sim", cid: str):
        self._sim = sim
        c = sim.captains[cid]
        spec = sim.cfg["ship_types"][c.ship_type]
        self.day, self.days = sim.day, sim.days
        self.port = c.port
        self.cash, self.fuel, self.cargo = c.cash, c.fuel, dict(c.cargo)
        self.ship_type, self.spec = c.ship_type, dict(spec)
        self.capacity, self.tank = spec["capacity"], spec["tank"] * spec["burn"]
        self.carries = sorted(g for g, v in sim.cfg["goods"].items() if v["ship"] == c.ship_type)
        self.ports = list(sim.markets)
        self.dues = sim.cfg["dues"]
        self.emergency_fuel = sim.emergency_fuel_price()

    def market(self, port: str):
        return self._sim.markets[port]

    def route(self, dest: str, policy: str = "shortest") -> dict | None:
        r = self._sim.net.route(self.port, dest, policy)
        if r is None:
            return None
        days = r.days(self.spec["knots"])
        tolls = sum(self._sim.cfg["canals"][k]["toll"][self.ship_type] for k in r.canals)
        return {"dest": dest, "policy": policy, "nm": round(r.nm), "days": days, "canals": list(r.canals),
                "tolls": tolls, "fuel": round(days * self.spec["burn"], 2), "path": list(r.path)}

    def leg(self, origin: str, dest: str, policy: str = "shortest") -> dict | None:
        """Route between any two ports (for planning several legs ahead)."""
        r = self._sim.net.route(origin, dest, policy)
        if r is None:
            return None
        days = r.days(self.spec["knots"])
        return {"days": days, "fuel": days * self.spec["burn"],
                "tolls": sum(self._sim.cfg["canals"][k]["toll"][self.ship_type] for k in r.canals)}


class Sim:
    def __init__(self, cfg: dict, seed: int = 0, n_captains: int | None = None, days: int | None = None,
                 event_sink: Callable[[dict], None] | None = None, strategy: str | None = None):
        self.cfg = cfg
        self.seed = seed
        self.days = days or cfg["days"]
        self.event_sink = event_sink
        self.net = Network(cfg)
        n = n_captains or cfg["captains"]
        self.markets = build_markets(cfg, seed, n)
        self.day = 0
        self.schedule: dict[int, list[tuple[str, str, int]]] = {}
        self.captains: dict[str, Captain] = {}
        self._make_fleet(n, strategy)
        self.history = {p: {g: {"buy": [], "sell": [], "stock": [], "demand": []} for g in m.goods}
                        for p, m in self.markets.items()}
        self.made = {p: {r.name: [] for r in m.recipes} for p, m in self.markets.items()}
        self.blocked = {p: {r.name: [] for r in m.recipes} for p, m in self.markets.items()}
        self.log("setup", seed=seed, days=self.days, flow_scale=flow_scale(cfg, n),
                 captains={c.id: {"name": c.name, "label": c.label, "strategy": c.strategy,
                                  "ship_type": c.ship_type, "start": c.port} for c in self.captains.values()})

    # ---------- setup ----------

    @staticmethod
    def _split(n: int, fractions: dict[str, float]) -> list[str]:
        """n items split by fractions (largest remainder), as a list of keys."""
        raw = {k: n * f for k, f in fractions.items()}
        counts = {k: int(v) for k, v in raw.items()}
        for k in sorted(raw, key=lambda k: -(raw[k] - counts[k]))[: n - sum(counts.values())]:
            counts[k] += 1
        return [k for k, c in counts.items() for _ in range(c)]

    def _make_fleet(self, n: int, strategy: str | None):
        rng = random.Random(f"{self.seed}-fleet")
        mix = self.cfg["fleet_mix"]
        fleet = []
        types = self._split(n, mix["types"])
        for t in mix["types"]:
            k = types.count(t)
            strategies = [strategy] * k if strategy else self._split(k, mix["strategies"])
            fleet += [(t, s) for s in strategies]
        names = self.cfg["captain_names"]
        used: dict[str, int] = {}
        for i, (ship_type, strat) in enumerate(fleet):
            base = names[i % len(names)]
            used[base] = used.get(base, 0) + 1
            name = base + (ROMAN[used[base] - 1] if used[base] <= len(ROMAN) else f" {used[base]}")
            cid = name.lower().replace(" ", "_")
            spec = self.cfg["ship_types"][ship_type]
            start = (self.cfg["liner_routes"][ship_type]["load"] if strat == "liner"
                     else rng.choice(list(self.cfg["ports"])))
            c = Captain(cid, name, f"{name[0]}{i + 1}", strat, ship_type, float(self.cfg["start_cash"]),
                        spec["tank"] * spec["burn"], port=start, dest=start)
            c.state = "sea"                              # everyone "arrives" at their start port on day 0
            self.captains[cid] = c
            self._schedule(c, 0, "arrive")

    # ---------- bookkeeping ----------

    def log(self, kind: str, **data):
        if self.event_sink:
            self.event_sink({"day": self.day, "event": kind, **data})

    def _schedule(self, c: Captain, day: int, kind: str):
        c.token += 1
        self.schedule.setdefault(day, []).append((kind, c.id, c.token))

    def _charge_crew(self, c: Captain, day: int):
        cost = (day - c.paid_until) * self.cfg["ship_types"][c.ship_type]["crew"]
        if cost > 0:
            c.cash -= cost
            c.stats["crew"] += cost
            c.paid_until = day

    def _record_day(self):
        for p, m in self.markets.items():
            h = self.history[p]
            for g in m.goods:
                h[g]["buy"].append(round(m.buy_price(g), 2))
                h[g]["sell"].append(round(m.sell_price(g), 2))
                h[g]["stock"].append(int(m.stock[g]))
                h[g]["demand"].append(round(m.demand.get(g, 1.0), 2))
            for r in m.recipes:
                self.made[p][r.name].append(m.made_today.get(r.name, 0) if self.day > 0 else 0)
                self.blocked[p][r.name].append(r.blocked if self.day > 0 else "")

    # ---------- the calendar ----------

    def run(self, players: dict) -> dict:
        """players: {strategy name: player object with .act(sim, cid)}"""
        for day in range(self.days + 1):
            self.day = day
            for m in self.markets.values():
                m.advance(day)
            todays = self.schedule.pop(day, [])
            random.Random(f"{self.seed}-day-{day}").shuffle(todays)
            for kind, cid, token in todays:
                c = self.captains[cid]
                if token != c.token or c.state == "bankrupt":
                    continue
                self._wake(c, kind, players[c.strategy])
            self._record_day()
        return self.finish()

    def _wake(self, c: Captain, kind: str, player):
        if kind == "arrive":
            c.state, c.port = "port", c.dest
            if self.day > 0:
                c.stats["days_at_sea"] += self.day - c.depart_day
                c.cash -= self.cfg["dues"]
                c.stats["dues"] += self.cfg["dues"]
            self._charge_crew(c, self.day)
            self.log("arrive", captain=c.id, port=c.port, cash=round(c.cash, 2), fuel=round(c.fuel, 2),
                     cargo=dict(c.cargo))
        else:
            c.state = "port"
            self._charge_crew(c, self.day)
            self.log("wake", captain=c.id, port=c.port, cash=round(c.cash, 2), fuel=round(c.fuel, 2),
                     cargo=dict(c.cargo))
        player.act(self, c.id)
        if c.state == "port":                            # no decision: wait a day
            self.log("default_wait", captain=c.id)
            self._set_wait(c, 1)
        if c.cash < 0 and not c.cargo:
            c.state = "bankrupt"
            c.token += 1
            self.log("bankrupt", captain=c.id, port=c.port, cash=round(c.cash, 2))

    # ---------- what a strategy sees ----------

    def view(self, cid: str) -> View:
        return View(self, cid)

    # ---------- actions ----------

    def _acting(self, cid: str):
        c = self.captains.get(cid)
        if c is None or c.state != "port":
            return "error: you can only act while in port"
        return c

    def _carries(self, c: Captain, good: str) -> bool:
        return self.cfg["goods"].get(good, {}).get("ship") == c.ship_type

    def buy(self, cid: str, good: str, qty) -> str:
        c = self._acting(cid)
        if isinstance(c, str):
            return c
        mk = self.markets[c.port]
        qty = int(qty)
        if good not in mk.goods:
            return f"error: {good} is not traded at {c.port}"
        if not self._carries(c, good):
            return f"error: a {c.ship_type} ship can't carry {good}"
        if qty < 1 or qty > int(mk.stock[good]):
            return f"error: {int(mk.stock[good])} {good} in stock"
        cap = self.cfg["ship_types"][c.ship_type]["capacity"]
        if c.load() + qty > cap:
            return f"error: only {cap - c.load()} units of free space"
        cost = mk.cost_to_buy(good, qty)
        if cost > c.cash + 1e-9:
            return f"error: costs {cost:.1f}, you have {c.cash:.1f}"
        mk.buy(good, qty)
        c.cash -= cost
        c.cargo[good] = c.cargo.get(good, 0) + qty
        self.log("trade", captain=cid, port=c.port, side="buy", good=good, qty=qty, total=round(cost, 2),
                 cash=round(c.cash, 2), cargo=dict(c.cargo))
        return f"bought {qty} {good} for {cost:.1f}"

    def sell(self, cid: str, good: str, qty) -> str:
        c = self._acting(cid)
        if isinstance(c, str):
            return c
        mk = self.markets[c.port]
        qty = int(qty)
        if good not in mk.goods:
            return f"error: {good} is not traded at {c.port}"
        if qty < 1 or qty > c.cargo.get(good, 0):
            return f"error: you have {c.cargo.get(good, 0)} {good}"
        got = mk.sell(good, qty)
        c.cash += got
        c.cargo[good] -= qty
        if not c.cargo[good]:
            del c.cargo[good]
        self.log("trade", captain=cid, port=c.port, side="sell", good=good, qty=qty, total=round(got, 2),
                 cash=round(c.cash, 2), cargo=dict(c.cargo))
        return f"sold {qty} {good} for {got:.1f}"

    def refuel(self, cid: str, qty) -> str:
        c = self._acting(cid)
        if isinstance(c, str):
            return c
        mk = self.markets[c.port]
        spec = self.cfg["ship_types"][c.ship_type]
        qty = min(int(qty), int(spec["tank"] * spec["burn"] - c.fuel))
        if qty < 1:
            return "error: tank already full"
        from_stock = min(qty, int(mk.stock[FUEL]))
        # Beyond the port's own stock, bunker suppliers always deliver, at a steep fixed premium.
        extra = qty - from_stock
        cost = mk.cost_to_buy(FUEL, from_stock) + extra * self.emergency_fuel_price()
        if cost > c.cash + 1e-9:
            return f"error: {qty} fuel costs {cost:.1f}, you have {c.cash:.1f}"
        mk.buy(FUEL, from_stock)
        c.cash -= cost
        c.fuel += qty
        c.stats["fuel_bought"] += cost
        self.log("refuel", captain=cid, port=c.port, qty=qty, emergency=extra, total=round(cost, 2),
                 cash=round(c.cash, 2), fuel=round(c.fuel, 2))
        return f"refuelled {qty} for {cost:.1f}" + (f" ({extra} at the emergency bunker price)" if extra else "")

    def emergency_fuel_price(self) -> float:
        return self.cfg["goods"][FUEL]["base"] * self.cfg.get("emergency_fuel_mult", 2.5)

    def sail(self, cid: str, dest: str, policy: str = "shortest") -> str:
        c = self._acting(cid)
        if isinstance(c, str):
            return c
        if dest not in self.markets or dest == c.port:
            return f"error: can't sail to {dest}"
        r = self.net.route(c.port, dest, policy)
        if r is None:
            return f"error: no {policy} route to {dest}"
        spec = self.cfg["ship_types"][c.ship_type]
        days = r.days(spec["knots"])
        need = days * spec["burn"]
        if c.fuel + 1e-9 < need:
            return f"error: needs {need:.1f} fuel, tank has {c.fuel:.1f}"
        tolls = sum(self.cfg["canals"][k]["toll"][c.ship_type] for k in r.canals)
        if tolls > c.cash + 1e-9:
            return f"error: canal tolls {tolls}, you have {c.cash:.1f}"
        c.cash -= tolls
        c.fuel -= need
        c.stats["voyages"] += 1
        c.stats["empty_voyages"] += int(not c.cargo)
        c.stats["canals"] += len(r.canals)
        c.stats["tolls"] += tolls
        c.state, c.origin, c.dest, c.path = "sea", c.port, dest, r.path
        c.depart_day, c.arrive_day = self.day, self.day + days
        self.log("sail", captain=cid, origin=c.port, dest=dest, policy=policy, path=list(r.path),
                 nm=round(r.nm), arrive_day=c.arrive_day, canals=list(r.canals), tolls=tolls,
                 fuel_used=round(need, 2), cash=round(c.cash, 2), fuel=round(c.fuel, 2), cargo=dict(c.cargo))
        c.port = None
        self._schedule(c, c.arrive_day, "arrive")
        return f"sailing to {dest}, arriving day {c.arrive_day}"

    def wait(self, cid: str, days) -> str:
        c = self._acting(cid)
        if isinstance(c, str):
            return c
        days = int(days)
        if not 1 <= days <= 30:
            return "error: wait 1-30 days"
        self._set_wait(c, days)
        return f"waiting until day {c.wait_until}"

    def _set_wait(self, c: Captain, days: int):
        c.state, c.wait_until = "waiting", self.day + days
        self.log("wait", captain=c.id, port=c.port, until=c.wait_until, cash=round(c.cash, 2),
                 fuel=round(c.fuel, 2), cargo=dict(c.cargo))
        self._schedule(c, c.wait_until, "wake")

    # ---------- end ----------

    def worth(self, c: Captain) -> dict:
        """Cash + cargo and tank fuel at the sell price where the ship is (its destination if at sea)."""
        where = c.port or c.dest
        mk = self.markets.get(where)
        cargo = sum(q * (mk.sell_price(g) if mk and g in mk.goods else 0.0) for g, q in c.cargo.items())
        fuel = c.fuel * (mk.sell_price(FUEL) if mk else 0.0)
        return {"cash": round(c.cash, 2), "cargo_value": round(cargo, 2), "fuel_value": round(fuel, 2),
                "score": round(c.cash + cargo + fuel, 2)}

    def finish(self) -> dict:
        scores = {}
        for c in self.captains.values():
            if c.state != "bankrupt":
                self._charge_crew(c, self.days)
            scores[c.id] = {"name": c.name, "label": c.label, "strategy": c.strategy, "ship_type": c.ship_type,
                            "state": c.state, "cargo": dict(c.cargo), **self.worth(c), "stats": c.stats}
        ranking = sorted(scores, key=lambda k: -scores[k]["score"])
        made = {p: {r: sum(v) for r, v in rs.items()} for p, rs in self.made.items()}
        self.log("finish", scores=scores, ranking=ranking, made=made)
        return {"scores": scores, "ranking": ranking, "made": made}
