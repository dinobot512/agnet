import argparse
import json
import random
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from engine import Sim
from strategies.greedy import GreedyPlayer
from strategies.liner import LinerPlayer
from strategies.random_player import RandomPlayer

HERE = Path(__file__).parent


def players(seed: int) -> dict:
    return {"greedy": GreedyPlayer(), "liner": LinerPlayer(), "random": RandomPlayer(seed)}


def write_summary(sim: Sim, res: dict, run_dir: Path):
    scores = res["scores"]
    lines = ["# Modern shipping: run summary", "",
             f"- Seed {sim.seed}, {len(sim.captains)} captains, {sim.days} days", "", "## By strategy and ship type", "",
             "| strategy | ship | captains | median score | bankrupt | voyages | empty voyages | canal transits |",
             "|---|---|---|---|---|---|---|---|"]
    groups = defaultdict(list)
    for s in scores.values():
        groups[(s["strategy"], s["ship_type"])].append(s)
    for (strat, ship), g in sorted(groups.items()):
        lines.append(f"| {strat} | {ship} | {len(g)} | {statistics.median(x['score'] for x in g):.0f} | "
                     f"{sum(x['state'] == 'bankrupt' for x in g)} | {sum(x['stats']['voyages'] for x in g)} | "
                     f"{sum(x['stats']['empty_voyages'] for x in g)} | {sum(x['stats']['canals'] for x in g)} |")
    lines += ["", "## Supply chains (batches made over the game)", "", "| product | batches |", "|---|---|"]
    totals = defaultdict(int)
    for port, recipes in res["made"].items():
        for r, n in recipes.items():
            totals[r] += n
    lines += [f"| {r} | {n} |" for r, n in sorted(totals.items(), key=lambda kv: -kv[1])]
    lines += ["", "## Leaderboard", "", "| # | captain | strategy | ship | state | score | cash |", "|---|---|---|---|---|---|---|"]
    for i, cid in enumerate(res["ranking"], 1):
        s = scores[cid]
        lines.append(f"| {i} | {s['name']} ({s['label']}) | {s['strategy']} | {s['ship_type']} | {s['state']} | "
                     f"{s['score']:.0f} | {s['cash']:.0f} |")
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Run the modern shipping simulation (predetermined strategies)")
    parser.add_argument("--seed", type=int, default=None, help="Random if omitted (recorded in the run)")
    parser.add_argument("--captains", type=int, default=None)
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--strategy", choices=["greedy", "liner", "random"], default=None,
                        help="Give every captain this strategy (default: the config's mix)")
    parser.add_argument("--config", default=None, help="Another config file, e.g. runs/<timestamp>/config.json")
    parser.add_argument("--quiet", action="store_true", help="Don't print every event")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text() if args.config else (HERE / "config.json").read_text())
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    run_dir = HERE / "runs" / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + (f"-{args.strategy}" if args.strategy else ""))
    run_dir.mkdir(parents=True, exist_ok=True)
    events_file = open(run_dir / "events.jsonl", "a")
    console = open(run_dir / "console.log", "a")

    def say(text=""):
        if not args.quiet:
            print(text, flush=True)
        console.write(text + "\n")

    def sink(event):                  # stream events so a crashed run still leaves a full log
        events_file.write(json.dumps(event) + "\n")
        kind = event["event"]
        if kind == "sail":
            say(f"day {event['day']:>3} {event['captain']:<12} {event['origin']} -> {event['dest']} "
                f"(day {event['arrive_day']}{', via ' + '+'.join(event['canals']) if event['canals'] else ''}) "
                f"cargo {event['cargo'] or 'empty'}")
        elif kind == "bankrupt":
            say(f"day {event['day']:>3} !! {event['captain']} bankrupt at {event['port']}")

    sim = Sim(config, seed=seed, n_captains=args.captains, days=args.days, event_sink=sink, strategy=args.strategy)
    (run_dir / "config.json").write_text(json.dumps({**config, "seed": seed, "captains": len(sim.captains),
                                                     "days": sim.days}, indent=1, ensure_ascii=False))
    print(f"Run: {run_dir}  (seed {seed}, {len(sim.captains)} captains, {sim.days} days)")
    res = sim.run(players(seed))
    events_file.close()
    (run_dir / "markets.json").write_text(json.dumps({"history": sim.history, "made": sim.made, "blocked": sim.blocked},
                                                     separators=(",", ":")))
    (run_dir / "results.json").write_text(json.dumps(res, indent=1))
    write_summary(sim, res, run_dir)
    print((run_dir / "summary.md").read_text().split("## Leaderboard")[0])
    try:
        from viewer import write_viewer
        print(f"Viewer: {write_viewer(run_dir)}")
    except Exception as e:
        print(f"(viewer not generated: {type(e).__name__}: {e})")


if __name__ == "__main__":
    main()
