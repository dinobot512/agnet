"""Tune the economy without API calls: run random and informed captains over a grid of settings.

    .venv/bin/python sweep.py                  # default grid, 3 seeds, all CPU cores
    .venv/bin/python sweep.py --seeds 5 --top 15

For each setting it reports, per player type: median and 10th/90th percentile final score, the share of
captains who lost money (ended below their starting silver), and the share stranded. The ranking favours
settings where random captains roughly break even while informed ones clearly do better, i.e. where skill
and information matter. Results go to sweeps/<timestamp>.json.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import os
import statistics
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent

DRIFT = {"sigma": 0.15, "revert": 0.05, "min": 0.3, "max": 2.0}
GRIDS = {
    "broad": {                                   # first pass: wide range of every lever
        "market.price_band": [(0.4, 2.5), (0.6, 1.8), (0.7, 1.6)],
        "ship.provisions_per_day": [0.5, 2.0],
        "ship.harbor_dues": [0, 3],
        "market.spread": [0.1, 0.2],
        "market.target_days": [10, 4],
        "market.demand_drift": [None, DRIFT],
    },
    "fleet10": {                                 # 10 ships: scale the world down, sweep costs around it
        "market.flow_scale": [0.15, 0.25, 0.4, 1.0],
        "ship.capacity": [20, 40],
        "ship.provisions_per_day": [1.0, 2.0],
        "ship.harbor_dues": [1, 2, 3],
        "market.target_days": [7, 10],
    },
    "costs10": {                                 # 10 ships: dues vs provisions vs spread (long trips, full holds)
        "ship.harbor_dues": [2, 3, 4],
        "ship.provisions_per_day": [0.5, 1.0],
        "market.spread": [0.1, 0.15],
    },
    "fine": {                                    # second pass: around the wide band with real costs
        "market.price_band": [(0.4, 2.5), (0.5, 2.2), (0.5, 2.5)],
        "ship.provisions_per_day": [1.0, 2.0],
        "ship.harbor_dues": [0, 1, 2],
        "market.spread": [0.1, 0.15],
        "market.target_days": [10, 7],
        "market.demand_drift": [None, DRIFT],
    },
}


def apply(cfg: dict, key: str, value):
    if key == "market.price_band":
        cfg["market"]["price_min"], cfg["market"]["price_max"] = value
        return
    section, name = key.split(".")
    if value is None:
        cfg[section].pop(name, None)
    else:
        cfg[section][name] = value


CAPTAINS = None                                  # set from --captains (passed to workers via the job tuple)


def one_run(args) -> dict:
    setting, player_name, seed, *rest = args
    n_captains = rest[0] if rest else None
    from engine import Sim
    from fake_agent import FakePlayer
    from informed_agent import InformedPlayer
    cfg = json.loads((HERE / "config.json").read_text())
    for k, v in setting.items():
        apply(cfg, k, v)
    player = FakePlayer(seed) if player_name == "random" else InformedPlayer(seed)
    sails = []
    res = Sim(cfg, seed=seed, n_captains=n_captains,
              event_sink=lambda e: sails.append(e) if e["event"] == "sail" else None).run(player)
    start = cfg["ship"]["start_silver"]
    cap = cfg["ship"]["capacity"]
    loads = [sum(e["cargo"].values()) / cap for e in sails]
    scores = [s["score"] for s in res["scores"].values()]
    return {"player": player_name, "seed": seed, "scores": scores,
            "lost": sum(s < start for s in scores) / len(scores),
            "stranded": sum(s["state"] == "stranded" for s in res["scores"].values()) / len(scores),
            "voyages": len(sails),
            "empty": sum(l == 0 for l in loads) / max(1, len(loads)),
            "full": sum(l >= 0.95 for l in loads) / max(1, len(loads)),
            "sardinia": sum(e["dest"] == "Sardinia" for e in sails) / max(1, len(sails)),
            "trip_days": statistics.median([e["arrive_day"] - e["day"] for e in sails]) if sails else 0}


def summarize(runs: list[dict]) -> dict:
    scores = sorted(s for r in runs for s in r["scores"])
    q = lambda p: scores[min(len(scores) - 1, int(p * len(scores)))]
    return {"median": round(statistics.median(scores), 1), "p10": round(q(0.1), 1), "p90": round(q(0.9), 1),
            "lost": round(statistics.mean(r["lost"] for r in runs), 3),
            "stranded": round(statistics.mean(r["stranded"] for r in runs), 3),
            **{k: round(statistics.mean(r[k] for r in runs), 3) for k in ("empty", "full", "sardinia", "trip_days")}}


def rank(row: dict, start: float) -> float:
    """Higher is better: informed clearly beats random (measured in starting-silvers, not a ratio, so a
    near-zero random median can't blow it up), random near break-even, and informed actually profitable."""
    r, i = row["random"]["median"], row["informed"]["median"]
    score = (i - r) / start
    score -= 0.5 * abs(math.log(max(r, 1) / (1.25 * start)))       # random should end near 1.25x start
    if i < 1.5 * start:
        score -= 1.0                                                 # skill should actually pay
    return score


def label(setting: dict) -> str:
    out = []
    for k, v in setting.items():
        name = k.split(".")[1]
        if k == "market.price_band":
            out.append(f"band={v[0]}-{v[1]}")
        elif k == "market.demand_drift":
            out.append(f"drift={'on' if v else 'off'}")
        else:
            out.append(f"{name}={v}")
    return " ".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--grid", choices=list(GRIDS), default="fine")
    parser.add_argument("--captains", type=int, default=None, help="Fleet size (default: config)")
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--workers", type=int, default=os.cpu_count())
    args = parser.parse_args()

    grid = GRIDS[args.grid]
    keys = list(grid)
    settings = [dict(zip(keys, values)) for values in itertools.product(*grid.values())]
    jobs = [(s, p, seed, args.captains) for s in settings for p in ("random", "informed") for seed in range(args.seeds)]
    print(f"{len(settings)} settings x 2 players x {args.seeds} seeds = {len(jobs)} games on {args.workers} cores")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(one_run, jobs, chunksize=4))
    print(f"done in {time.time() - t0:.0f}s")

    start = json.loads((HERE / "config.json").read_text())["ship"]["start_silver"]
    rows = []
    for i, s in enumerate(settings):
        mine = results[i * 2 * args.seeds:(i + 1) * 2 * args.seeds]
        row = {"setting": {k: v for k, v in s.items()}, "label": label(s),
               "random": summarize([r for r in mine if r["player"] == "random"]),
               "informed": summarize([r for r in mine if r["player"] == "informed"])}
        row["gap"] = round(row["informed"]["median"] / max(row["random"]["median"], 1), 2)
        by_seed = {}
        for r in mine:
            by_seed.setdefault(r["seed"], {})[r["player"]] = statistics.median(r["scores"])
        row["wins"] = round(sum(v["informed"] > v["random"] for v in by_seed.values()) / len(by_seed), 2)
        row["rank"] = round(rank(row, start), 3)
        rows.append(row)
    rows.sort(key=lambda r: -r["rank"])

    out_dir = HERE / "sweeps"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".json")
    out.write_text(json.dumps(rows, indent=2, default=list))

    print(f"\n{'setting':<78} {'random med (p10-p90) lost':>28} {'informed med (p10-p90) lost':>30} {'gap':>5}")
    for r in rows[:args.top]:
        ra, inf = r["random"], r["informed"]
        print(f"{r['label']:<78} {ra['median']:>7} ({ra['p10']:>6}-{ra['p90']:>6}) {ra['lost']:>4.0%}"
              f" {inf['median']:>9} ({inf['p10']:>6}-{inf['p90']:>6}) {inf['lost']:>4.0%} {r['gap']:>5}"
              f"  wins {r['wins']:.0%}  | informed: empty {inf['empty']:.0%} full {inf['full']:.0%} "
              f"Sardinia {inf['sardinia']:.0%} trip {inf['trip_days']:.1f}d")
    print(f"saved {out}")


if __name__ == "__main__":
    main()
