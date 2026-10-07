import copy
import json
import statistics
from pathlib import Path

from engine import Sim
from fake_agent import FakePlayer
from informed_agent import InformedPlayer, format_record, parse_records

CFG = json.loads((Path(__file__).parent / "config.json").read_text())


def test_record_format_roundtrip():
    rec = {"buy": 4.06, "sell": 3.32, "stock": 400, "day": 10, "src": "seen"}
    line = format_record("Enkomi", "olive oil", rec)
    assert line == "PRICE port=Enkomi good=olive oil buy=4.06 sell=3.32 stock=400 day=10 src=seen"
    (r,) = parse_records("By Baal! " + line + " — trust me")
    assert r == {"port": "Enkomi", "good": "olive oil", "buy": 4.06, "sell": 3.32, "stock": 400, "day": 10, "src": "seen"}
    assert parse_records("tin is cheap at Ugarit") == []


def run(player, seed=1, n=50, days=120):
    events = []
    sim = Sim(copy.deepcopy(CFG), seed=seed, event_sink=events.append, n_captains=n, days=days)
    return sim, events, sim.run(player)


def test_gossip_travels_and_is_logged():
    p = InformedPlayer(seed=1)
    sim, events, _ = run(p, days=40)
    notes = [e for e in events if e["event"] == "note"]
    assert notes and all(parse_records(n["text"]) for n in notes)          # logbook is all parsable
    heard = [r for kb in p.kb.values() for (port, good), r in kb.items() if r["src"] != "seen"]
    assert heard, "no captain learned anything second-hand"
    statements = [e for e in events if e["event"] == "statement"]
    assert statements and all(parse_records(e["text"]) for e in statements)


def test_only_knows_ports_it_saw_or_heard_about():
    p = InformedPlayer(seed=2)
    sim, events, _ = run(p, days=30)
    for cid, kb in p.kb.items():
        seen_ports = {port for (port, _), r in kb.items() if r["src"] == "seen"}
        assert seen_ports <= set(sim.captains[cid].logbook)               # 'seen' only where it has been


def test_informed_beats_random():
    _, _, informed = run(InformedPlayer(seed=3), seed=3)
    _, _, rand = run(FakePlayer(3), seed=3)
    med = lambda res: statistics.median(s["score"] for s in res["scores"].values())
    assert med(informed) > med(rand)
