import copy
import json
import random
from pathlib import Path

import pytest

from world import Market, Recipe, build_markets

CFG = json.loads((Path(__file__).parent / "config.json").read_text())


def markets(drift=False, n=60):
    cfg = copy.deepcopy(CFG)
    if not drift:
        cfg["market"].pop("demand_drift", None)
    return build_markets(cfg, seed=3, n_captains=n)


def test_every_port_trades_fuel_and_its_flows():
    ms = markets()
    for port, p in CFG["ports"].items():
        goods = set(ms[port].goods)
        assert "fuel" in goods
        assert set(p["produce"]) | set(p["consume"]) <= goods
        for r in p["recipes"]:
            assert set(CFG["recipes"][r]["in"]) | set(CFG["recipes"][r]["out"]) <= goods


def test_price_impact_and_clamps():
    mk = markets()["Port Hedland"]
    g = mk.goods["iron ore"]
    assert mk.price("iron ore") == pytest.approx(g.base)
    assert mk.price("iron ore", 1e9) == pytest.approx(g.base * CFG["market"]["price_min"])
    assert mk.price("iron ore", 0) == pytest.approx(g.base * CFG["market"]["price_max"])
    p0 = mk.buy_price("iron ore")
    assert mk.cost_to_buy("iron ore", 100) > 100 * p0
    mk.buy("iron ore", 100)
    assert mk.buy_price("iron ore") > p0


def test_recipe_stops_without_inputs_and_raw_production_continues():
    mk = markets()["Shanghai"]
    mk.stock["coal"] = 0
    steel0 = mk.stock["steel"]
    mk.advance(1)
    assert mk.made_today["steel"] == 0 and mk.stock["steel"] == steel0
    mk.stock["coal"] = 1000
    mk.advance(2)
    assert mk.made_today["steel"] == 20                     # 20 batches/day at the reference fleet


def test_fractional_batches_accumulate():
    goods = {"a": None}
    from world import Good
    goods = {"a": Good("a", 1, 10, 1e9), "b": Good("b", 1, 10, 1e9)}
    stock = {"a": 100.0, "b": 0.0}
    r = Recipe("x", {"a": 1}, {"b": 1}, rate=0.5)
    made = sum(r.run(stock, goods) for _ in range(10))
    assert made == 5 and stock["b"] == 5


def test_flows_scale_with_fleet():
    small, big = markets(n=30), markets(n=120)
    assert big["Port Hedland"].goods["iron ore"].produce == pytest.approx(4 * small["Port Hedland"].goods["iron ore"].produce)


def test_drift_deterministic():
    a, b = markets(drift=True), markets(drift=True)
    for m in (a, b):
        for d in range(1, 40):
            m["Los Angeles"].advance(d)
    assert a["Los Angeles"].demand == b["Los Angeles"].demand
    assert any(abs(v - 1) > 0.02 for v in a["Los Angeles"].demand.values())
