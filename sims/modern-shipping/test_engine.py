import copy
import json
from pathlib import Path

import pytest

from engine import Sim, View

CFG = json.loads((Path(__file__).parent / "config.json").read_text())


class Script:
    def __init__(self, fn=None):
        self.fn = fn or (lambda sim, cid: sim.wait(cid, 30))
        self.calls = []

    def act(self, sim, cid):
        self.calls.append((sim.day, cid))
        self.fn(sim, cid)


def make(n=10, days=30, **kw):
    events = []
    sim = Sim(copy.deepcopy(CFG), seed=1, n_captains=n, days=days, event_sink=events.append, **kw)
    return sim, events


def first(sim, ship_type):
    return next(c for c in sim.captains.values() if c.ship_type == ship_type)


def test_fleet_mix_and_strategy_override():
    sim, _ = make(n=20)
    types = [c.ship_type for c in sim.captains.values()]
    assert types.count("bulk") == 8 and types.count("tanker") == 5 and types.count("container") == 7
    sim2, _ = make(n=20, strategy="greedy")
    assert {c.strategy for c in sim2.captains.values()} == {"greedy"}


def test_view_has_no_other_captains():
    sim, _ = make()
    cid = next(iter(sim.captains))
    sim.captains[cid].state = "port"
    v = sim.view(cid)
    public = {k for k in vars(v) if not k.startswith("_")}
    assert not public & {"captains", "others", "fleet"}
    assert all(not callable(getattr(v, k)) or k in ("market", "route", "leg") for k in dir(v) if not k.startswith("_"))


def test_cargo_class_capacity_fuel_and_tolls():
    sim, events = make(days=60)
    bulk = first(sim, "bulk")
    out = {}

    def act(s, cid):
        if cid != bulk.id or s.day != 0:
            return s.wait(cid, 30)
        s.captains[cid].port = "Los Angeles"                # trades cars, which bulk carriers can't carry
        port = s.captains[cid].port
        out["wrong"] = s.buy(cid, "cars", 1)
        s.captains[cid].fuel = 0
        out["nofuel"] = s.sail(cid, "Rotterdam" if port != "Rotterdam" else "Shanghai")
        s.captains[cid].fuel = 1000
        s.captains[cid].port = "Shanghai"
        cash = s.captains[cid].cash
        out["sail"] = s.sail(cid, "Rotterdam", "shortest")
        out["toll_paid"] = cash - s.captains[cid].cash

    sim.run({"greedy": Script(act), "liner": Script(act), "random": Script(act)})
    assert "can't carry" in out["wrong"]
    assert out["nofuel"].startswith("error: needs")
    assert out["sail"].startswith("sailing to Rotterdam")
    assert out["toll_paid"] == CFG["canals"]["Suez"]["toll"]["bulk"]


def test_no_calls_at_sea_and_cash_accounting():
    sim, events = make(n=6, days=80)
    def act(s, cid):
        c = s.captains[cid]
        if c.port != "Rotterdam":
            s.refuel(cid, 1000)
            if s.sail(cid, "Rotterdam").startswith("error"):
                s.wait(cid, 5)
        else:
            s.wait(cid, 30)
    p = Script(act)
    sim.run({"greedy": p, "liner": p, "random": p})
    for c in sim.captains.values():
        sails = [e for e in events if e["event"] == "sail" and e["captain"] == c.id]
        for s in sails:                                   # never called between departure and arrival
            assert not [d for d, cid in p.calls if cid == c.id and s["day"] < d < s["arrive_day"]]
        spent = sum(e["total"] for e in events if e.get("captain") == c.id and e["event"] in ("refuel",))
        tolls = sum(e["tolls"] for e in sails)
        arrivals = sum(1 for e in events if e["event"] == "arrive" and e["captain"] == c.id and e["day"] > 0)
        crew = CFG["ship_types"][c.ship_type]["crew"] * c.paid_until
        assert c.cash == pytest.approx(CFG["start_cash"] - spent - tolls - CFG["dues"] * arrivals - crew, abs=0.05)


def test_wake_order_is_seeded():
    orders = []
    for _ in range(2):
        sim, events = make(n=12, days=0)
        sim.run({k: Script() for k in ("greedy", "liner", "random")})
        orders.append([e["captain"] for e in events if e["event"] == "arrive"])
    assert orders[0] == orders[1]
