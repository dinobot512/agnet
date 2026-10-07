"""Shared helpers for predetermined strategies. They use only what a View exposes."""

from __future__ import annotations

from world import FUEL


def _avg_factor(target: float, a: float, b: float, e: float) -> float:
    """Average of (target/x)^e for x between a and b (a < b): the mean price multiplier over a trade."""
    a, b = max(a, 0.5), max(b, 0.5)
    if b - a < 1e-9:
        return (target / a) ** e
    return target ** e * (b ** (1 - e) - a ** (1 - e)) / ((1 - e) * (b - a))


def est_buy(market, good: str, qty: int) -> float:
    """Fast estimate of market.cost_to_buy (closed form instead of unit by unit)."""
    if qty <= 0:
        return 0.0
    g, cfg = market.goods[good], market.cfg
    s = market.stock[good]
    f = _avg_factor(g.target, s - qty, s, cfg["elasticity"])
    f = min(max(f, cfg["price_min"]), cfg["price_max"])
    return qty * g.base * f * (1 + cfg["spread"])


def est_sell(market, good: str, qty: int) -> float:
    """Fast estimate of market.proceeds_of_sale."""
    if qty <= 0 or good not in market.goods:
        return 0.0
    g, cfg = market.goods[good], market.cfg
    s = market.stock[good]
    f = _avg_factor(g.target, s, s + qty, cfg["elasticity"])
    f = min(max(f, cfg["price_min"]), cfg["price_max"])
    return qty * g.base * f * (1 - cfg["spread"])


def affordable(market, good: str, budget: float, room: int) -> int:
    """Most units of good we can buy here with budget and room (binary search on the estimate)."""
    hi = min(room, int(market.stock[good]))
    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if est_buy(market, good, mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo


def leg_cost(view, origin: str, dest: str, fuel_price: float) -> tuple[float, int, str]:
    """Cheapest way between two ports: (cost incl. fuel, crew, tolls and dues; days; policy)."""
    best = None
    for policy in ("shortest", "no_canals"):
        leg = view.leg(origin, dest, policy)
        if leg is None:
            continue
        cost = leg["fuel"] * fuel_price + leg["tolls"] + leg["days"] * view.spec["crew"] + view.dues
        if best is None or cost < best[0]:
            best = (cost, leg["days"], policy)
    return best


def fuel_price(view, port: str) -> float:
    """Price of fuel at a port: its market price, or the emergency bunker price if it's nearly out."""
    mk = view.market(port)
    return mk.buy_price(FUEL) if mk.stock[FUEL] >= 20 else max(mk.buy_price(FUEL), view.emergency_fuel)


def ensure_fuel(sim, cid: str, view, needed: float, top_up: bool = False) -> bool:
    """Refuel so the tank holds at least `needed` (or fill it if top_up). False if we can't."""
    if top_up:
        sim.refuel(cid, view.tank - view.fuel)
    elif view.fuel < needed:
        sim.refuel(cid, needed - view.fuel + 1)
    return sim.captains[cid].fuel + 1e-9 >= needed
