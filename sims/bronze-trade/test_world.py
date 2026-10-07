import copy
import json
from pathlib import Path

import pytest

from world import build_markets, sailing_days

CFG = json.loads((Path(__file__).parent / "config.json").read_text())


def markets():
    cfg = copy.deepcopy(CFG)
    cfg["market"].pop("demand_drift", None)        # fixed demand, so flows are exact
    return build_markets(cfg)


def test_price_curve_and_clamps():
    mk = markets()["Enkomi"]
    g = mk.goods["copper"]
    assert mk.price("copper") == pytest.approx(g.base)                     # starts at target
    assert mk.price("copper", 2 * g.target) == pytest.approx(g.base * 2 ** -0.7)
    assert mk.price("copper", 100 * g.target) == pytest.approx(g.base * CFG["market"]["price_min"])
    assert mk.price("copper", 0) == pytest.approx(g.base * CFG["market"]["price_max"])
    assert mk.buy_price("copper") > mk.price("copper") > mk.sell_price("copper")


def test_every_unit_moves_the_price():
    mk = markets()["Enkomi"]
    p0 = mk.buy_price("copper")
    assert mk.cost_to_buy("copper", 40) > 40 * p0                          # buying pushes the price up
    mk.buy("copper", 40)
    assert mk.buy_price("copper") > p0
    s0 = mk.sell_price("copper")
    assert mk.proceeds_of_sale("copper", 40) < 40 * s0                     # selling pushes it down
    mk.sell("copper", 40)
    assert mk.sell_price("copper") < s0


def test_production_capped_and_consumption_floors_at_zero():
    mk = markets()["Enkomi"]
    mk.advance(100)
    assert mk.stock["copper"] == mk.goods["copper"].cap                     # warehouses full
    assert mk.stock["grain"] == 0                                           # ran out, nothing else happens
    mk.advance(101)
    assert mk.stock["grain"] == 0


def test_bronze_needs_both_metals():
    mk = markets()["Avaris"]
    mk.stock["tin"] = 1
    mk.stock["copper"] = 100
    bronze0 = mk.stock["bronze"]
    mk.advance(1)                    # 2 batches/day possible, but only 1 tin -> 1 batch
    assert mk.stock["tin"] == 0 and mk.stock["copper"] == 91
    assert mk.stock["bronze"] == bronze0 + 10 - mk.goods["bronze"].consume
    grain0 = mk.stock["grain"]
    mk.advance(2)                    # no tin: bronze stops, raw goods keep coming
    assert mk.stock["copper"] == 91
    assert mk.stock["grain"] > grain0


def test_sailing_days():
    d = sailing_days(CFG)
    assert d["Enkomi"]["Ugarit"] == 2 and d["Ugarit"]["Enkomi"] == 2
    assert d["Enkomi"]["Knossos"] == 7                                      # via Rhodes: 250 + 120 nm
    assert all(d[a][b] >= 1 for a in d for b in d if a != b)


def drifted(drift, days, step):
    cfg = copy.deepcopy(CFG)
    cfg["market"]["demand_drift"] = drift
    mk = build_markets(cfg, seed=5)["Byblos"]
    for d in range(step, days + 1, step):
        mk.advance(d)
    return mk


def test_demand_drift_is_deterministic_and_bounded():
    drift = {"sigma": 0.2, "revert": 0.05, "min": 0.3, "max": 2.0}
    daily, lumped = drifted(drift, 60, 1), drifted(drift, 60, 30)    # same days, visited differently
    assert daily.stock == lumped.stock and daily.demand == lumped.demand
    assert all(0.3 <= m <= 2.0 for m in daily.demand.values())
    assert any(abs(m - 1) > 0.05 for m in daily.demand.values())
    off = drifted({}, 60, 1)
    assert off.demand == {}                                            # no drift configured: demand fixed
