"""Tune the economy with predetermined strategies (no API): mixed fleets over a grid of settings.

    python sweep.py                      # default grid, 3 seeds, all cores
    python sweep.py --seeds 5 --captains 60 --days 365 --top 12

Reports per setting:
  - median final score by strategy (greedy / liner / random), and the share of each that lost money
  - greedy's median by ship type (are bulk, tanker and container all viable?)
  - chain use: batches made ÷ capacity for every recipe (mean, and the weakest chain)
  - share of empty voyages
Ranked to favour: every chain running, greedy clearly ahead of random, random near break-even, and ship types
balanced. Results go to sweeps/<timestamp>.json.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import os
import statistics
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

GRID = {
    "market.flow_scale": [0.4, 0.6, 1.0],            # how busy the world is per ship
    "market.target_days": [30, 60],
    "market.price_max": [2.5, 4.0],                  # how loudly a starved market can call for supply
    "mult.bulk": [2, 3],
    "mult.tanker": [0.5, 1],
    "start_cash": [6000],
}


def apply(cfg: dict, key: str, value):
    if key.startswith("mult."):                      # scale the base price of every good of one ship class
        cls = key.split(".")[1]
        for g in cfg["goods"].values():
            if g["ship"] == cls:
                g["base"] *= value
    elif "." in key:
        section, name = key.split(".")
        cfg[section][name] = value
    else:
        cfg[key] = value


def one_game(job) -> dict:
    setting, seed, n, days = job
    from engine import Sim
    from run import players
    cfg = json.loads((HERE / "config.json").read_text())
    for k, v in setting.items():
        apply(cfg, k, v)
    sim = Sim(cfg, seed=seed, n_captains=n, days=days)
    res = sim.run(players(seed))
    start = cfg["start_cash"]
    by = defaultdict(list)
    for s in res["scores"].values():
        by[s["strategy"]].append(s)
    greedy_type = defaultdict(list)
    for s in by["greedy"]:
        greedy_type[s["ship_type"]].append(s["score"])
    use = []
    for port, recipes in res["made"].items():
        for r, made in recipes.items():
            cap = cfg["ports"][port]["recipes"][r] * days
            use.append((f"{r}@{port}", made / cap if cap else 0))
    chains = defaultdict(list)
    for name, u in use:
        chains[name.split("@")[0]].append(u)
    chain_use = {r: statistics.mean(v) for r, v in chains.items()}
    voyages = sum(s["stats"]["voyages"] for s in res["scores"].values())
    empty = sum(s["stats"]["empty_voyages"] for s in res["scores"].values())
    return {
        "strategy": {k: {"median": statistics.median(x["score"] for x in v),
                         "lost": sum(x["score"] < start for x in v) / len(v),
                         "bankrupt": sum(x["state"] == "bankrupt" for x in v) / len(v)} for k, v in by.items()},
        "greedy_by_type": {k: statistics.median(v) for k, v in greedy_type.items()},
        "chain_use": chain_use, "empty": empty / max(1, voyages), "start": start,
    }


def combine(games: list[dict]) -> dict:
    out = {"strategy": {}, "greedy_by_type": {}, "chain_use": {}}
    for k in games[0]["strategy"]:
        out["strategy"][k] = {m: statistics.mean(g["strategy"][k][m] for g in games) for m in ("median", "lost", "bankrupt")}
    for k in games[0]["greedy_by_type"]:
        out["greedy_by_type"][k] = statistics.mean(g["greedy_by_type"].get(k, 0) for g in games)
    for k in games[0]["chain_use"]:
        out["chain_use"][k] = statistics.mean(g["chain_use"][k] for g in games)
    out["empty"] = statistics.mean(g["empty"] for g in games)
    out["start"] = games[0]["start"]
    return out


def rank(row: dict) -> float:
    s, start = row["strategy"], row["start"]
    g, r = s["greedy"]["median"], s["random"]["median"]
    uses = list(row["chain_use"].values())
    score = 2.0 * statistics.mean(uses) + 1.0 * min(uses)                 # every chain should run
    score += (g - r) / start                                             # skill pays
    score -= 0.5 * abs(math.log(max(r, 1) / start))                      # random near break-even
    types = [v for v in row["greedy_by_type"].values() if v > 0]
    if len(types) == 3:
        score -= 0.5 * math.log(max(types) / max(min(types), 1))         # ship types balanced
    return score


def label(setting: dict) -> str:
    return " ".join(f"{k.split('.')[-1] if '.' in k and not k.startswith('mult') else k}={v}" for k, v in setting.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--captains", type=int, default=60)
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    args = ap.parse_args()
    settings = [dict(zip(GRID, v)) for v in itertools.product(*GRID.values())]
    jobs = [(s, seed, args.captains, args.days) for s in settings for seed in range(args.seeds)]
    print(f"{len(settings)} settings x {args.seeds} seeds = {len(jobs)} games ({args.captains} captains, {args.days} days)")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        games = list(pool.map(one_game, jobs))
    print(f"done in {time.time() - t0:.0f}s")
    rows = []
    for i, s in enumerate(settings):
        row = combine(games[i * args.seeds:(i + 1) * args.seeds])
        row.update(setting=s, label=label(s))
        row["rank"] = rank(row)
        rows.append(row)
    rows.sort(key=lambda r: -r["rank"])
    out = HERE / "sweeps"
    out.mkdir(exist_ok=True)
    path = out / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".json")
    path.write_text(json.dumps(rows, indent=1))
    print(f"\n{'setting':<58} {'greedy':>7} {'liner':>7} {'random':>7} {'rnd lost':>8} | {'bulk':>6} {'tank':>6} {'cont':>6} | chain mean/min | empty")
    for r in rows[:args.top]:
        s = r["strategy"]; t = r["greedy_by_type"]; u = list(r["chain_use"].values())
        print(f"{r['label']:<58} {s['greedy']['median']:>7.0f} {s['liner']['median']:>7.0f} {s['random']['median']:>7.0f} "
              f"{s['random']['lost']:>7.0%} | {t.get('bulk', 0):>6.0f} {t.get('tanker', 0):>6.0f} {t.get('container', 0):>6.0f} | "
              f"{statistics.mean(u):>5.0%} / {min(u):>4.0%} | {r['empty']:.0%}")
    best = rows[0]
    print("\nchain use for the best setting:", {k: f"{v:.0%}" for k, v in sorted(best["chain_use"].items(), key=lambda kv: kv[1])})
    print(f"saved {path}")


if __name__ == "__main__":
    main()
