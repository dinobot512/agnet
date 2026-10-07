import copy
import json
import statistics
from pathlib import Path

from engine import Sim
from run import players

CFG = json.loads((Path(__file__).parent / "config.json").read_text())


def play(strategy=None, seed=1, n=30, days=120):
    sim = Sim(copy.deepcopy(CFG), seed=seed, n_captains=n, days=days, strategy=strategy)
    return sim.run(players(seed))


def test_mixed_fleet_runs_and_ships_sail():
    res = play()
    assert sum(s["stats"]["voyages"] for s in res["scores"].values()) > 30


def test_greedy_beats_random():
    g = play("greedy", seed=2)
    r = play("random", seed=2)
    med = lambda res: statistics.median(s["score"] for s in res["scores"].values())
    assert med(g) > med(r)
