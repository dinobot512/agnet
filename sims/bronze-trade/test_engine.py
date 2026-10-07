import copy
import json
from pathlib import Path

import pytest

from engine import Sim
from fake_agent import FakePlayer

CFG = json.loads((Path(__file__).parent / "config.json").read_text())
# With 10 captains: one per home port, plus a second Avaris captain (tiye).


class Script:
    """Scripted player: per-captain functions for each stage; records every call."""

    def __init__(self, first=None, talk=None, final=None):
        self.first_fns, self.talk_fns, self.final_fns = first or {}, talk or {}, final or {}
        self.calls = []

    def first_trade(self, sim, cid):
        self.calls.append((sim.day, cid, "first"))
        self.first_fns.get(cid, lambda s, c: None)(sim, cid)
        sim.done_trading(cid)

    def talk(self, sim, cid, r):
        self.calls.append((sim.day, cid, f"talk{r}"))
        fn = self.talk_fns.get(cid)
        fn(sim, cid, r) if fn else sim.stay_silent(cid)

    def final(self, sim, cid):
        self.calls.append((sim.day, cid, "final"))
        fn = self.final_fns.get(cid)
        fn(sim, cid) if fn else sim.wait(cid, 30)


def make(n=10, days=20):
    events = []
    sim = Sim(copy.deepcopy(CFG), seed=0, event_sink=events.append, n_captains=n, days=days)
    return sim, events


def test_captains_named_and_start_home():
    sim, _ = make(10)
    assert sim.captains["nebamun"].home == "Avaris" and sim.captains["tiye"].home == "Avaris"
    assert sim.captains["rib_hadda"].home == "Byblos"
    sim2, _ = make(60)                                   # names repeat after 9 ports x 6 names
    assert "nebamun_ii" in sim2.captains and sim2.captains["nebamun_ii"].name == "Nebamun II"


def test_newcomer_trades_first_then_waiter_wakes_and_sees_new_prices():
    sim, events = make(10, days=6)
    seen = {}

    def nebamun_final(s, c):
        if s.day == 0:
            s.buy(c, "grain", 40)
            s.sail(c, "Enkomi")                        # arrives day 4
        else:
            s.wait(c, 30)

    def kush_final(s, c):
        if s.day == 4:
            seen["grain_price"] = s.markets["Enkomi"].sell_price("grain")
        s.wait(c, 10)

    p = Script(first={"nebamun": lambda s, c: s.sell(c, "grain", 40)},
               final={"nebamun": nebamun_final, "kushmeshusha": kush_final})
    sim.run(p)
    day4 = [x for x in p.calls if x[0] == 4]
    assert day4[0] == (4, "nebamun", "first")          # newcomer acts before anyone else
    assert (4, "kushmeshusha", "talk1") in day4 and (4, "kushmeshusha", "final") in day4
    wake = next(e for e in events if e["event"] == "wake" and e["captain"] == "kushmeshusha")
    sale = next(e for e in events if e["event"] == "trade" and e["side"] == "sell")
    assert events.index(sale) < events.index(wake) and wake["reason"] == "arrival"
    assert seen["grain_price"] < sim.markets["Enkomi"].goods["grain"].base * 2.5   # grain no longer scarce


def test_deadline_wakes_alone_and_stale_deadlines_ignored():
    sim, events = make(9, days=12)
    p = Script(final={"kushmeshusha": lambda s, c: s.wait(c, 3 if s.day == 0 else 30)})
    sim.run(p)
    assert (3, "kushmeshusha", "final") in p.calls
    wake = next(e for e in events if e["event"] == "wake" and e["captain"] == "kushmeshusha")
    assert wake["day"] == 3 and wake["reason"] == "deadline"
    assert [x for x in p.calls if x[1] == "kushmeshusha"] == [(0, "kushmeshusha", "final"), (3, "kushmeshusha", "final")]


def test_no_calls_at_sea_and_provisions_charged():
    sim, _ = make(9, days=10)
    p = Script(final={"nebamun": lambda s, c: s.sail(c, "Knossos") if s.day == 0 else s.wait(c, 30)})
    sim.run(p)
    days_called = sorted({x[0] for x in p.calls if x[1] == "nebamun"})
    assert days_called == [0, 6]                              # asleep at sea from day 0 to arrival on day 6
    ship = CFG["ship"]
    assert sim.captains["nebamun"].silver == pytest.approx(
        ship["start_silver"] - ship["provisions_per_day"] * 10 - ship.get("harbor_dues", 0))


def test_information_stays_in_port_and_barkeep_repeats_it():
    sim, _ = make(10, days=8)
    briefings = {}

    def tiye_talk(s, c, r):
        s.say(c, "Tin is dear at Knossos") if (r == 1 and s.day == 0) else s.stay_silent(c)

    def kush_final(s, c):
        briefings[s.day] = s.briefing(c)
        s.sail(c, "Avaris") if s.day == 0 else s.wait(c, 30)

    p = Script(talk={"tiye": tiye_talk}, final={"kushmeshusha": kush_final})
    sim.run(p)
    assert [e["text"] for e in sim.barkeep["Avaris"]] == ["Tin is dear at Knossos"]
    assert all(not v for k, v in sim.barkeep.items() if k != "Avaris")
    assert "Tin is dear" not in briefings[0]                 # kushmeshusha was in Enkomi on day 0
    assert "[day 0] Tiye: \"Tin is dear at Knossos\"" in briefings[4]   # the barkeep at Avaris tells it


def test_talk_rounds_are_simultaneous():
    sim, _ = make(10, days=1)
    seen = {}

    def talk(s, c, r):
        seen[(c, r)] = s.briefing(c)
        s.say(c, f"hello from {c} round {r}")

    p = Script(talk={"nebamun": talk, "tiye": talk})
    sim.run(p)
    assert "hello from tiye round 1" not in seen[("nebamun", 1)]
    assert "hello from tiye round 1" in seen[("nebamun", 2)]


def test_trade_validation():
    sim, _ = make(9, days=1)
    out = {}

    def final(s, c):
        out["space"] = s.buy(c, "grain", 41)
        out["silver"] = s.buy(c, "copper", 40)
        out["not_traded"] = s.buy(c, "tin", 1)
        out["sell_none"] = s.sell(c, "copper", 1)
        out["ok"] = s.buy(c, "grain", 10)
        s.wait(c, 30)

    sim.run(Script(final={"kushmeshusha": final}))           # at Enkomi, which doesn't trade tin
    assert "free space" in out["space"] and "would cost" in out["silver"]
    assert "not traded" in out["not_traded"] and out["sell_none"].startswith("error")
    assert out["ok"].startswith("bought 10 grain")


def test_stranded_captain_leaves_the_game():
    sim, events = make(9, days=10)

    def final(s, c):
        s.captains[c].silver = 0
        s.wait(c, 2)

    p = Script(final={"kushmeshusha": final})
    sim.run(p)
    assert sim.captains["kushmeshusha"].state == "stranded"
    assert [x for x in p.calls if x[1] == "kushmeshusha"] == [(0, "kushmeshusha", "final")]


@pytest.mark.parametrize("seed", range(3))
def test_fake_run_silver_accounting(seed):
    events = []
    sim = Sim(copy.deepcopy(CFG), seed=seed, event_sink=events.append)
    res = sim.run(FakePlayer(seed))
    days = [e["day"] for e in events if e["event"] == "session"]
    assert days == sorted(days)                              # time never runs backwards
    for cid, c in sim.captains.items():
        trades = [e for e in events if e["event"] == "trade" and e["captain"] == cid]
        net = sum(e["total"] if e["side"] == "sell" else -e["total"] for e in trades)
        arrivals = sum(1 for e in events if e["event"] == "arrive" and e["captain"] == cid and e["day"] > 0)
        ship = CFG["ship"]
        expected = (ship["start_silver"] + net - ship["provisions_per_day"] * c.paid_until
                    - ship.get("harbor_dues", 0) * arrivals)
        assert c.silver == pytest.approx(expected, abs=0.01 * max(1, len(trades)))
        assert sum(c.cargo.values()) <= CFG["ship"]["capacity"]
