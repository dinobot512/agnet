import argparse
import json
import os
import random
from datetime import datetime
from pathlib import Path

from engine import Sim

HERE = Path(__file__).parent


def load_dotenv():
    env_file = HERE / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def write_summary(sim: Sim, res: dict, run_dir: Path, aborted: str | None):
    scores = res["scores"]
    lines = ["# Bronze Age trade: run summary", ""]
    if aborted:
        lines += [f"**ABORTED on day {sim.day}:** {aborted}", ""]
    lines += [f"- Seed {sim.seed}, {len(sim.captains)} captains, {sim.days} days", "", "## Leaderboard", "",
              "| # | captain | home | state | silver | cargo | score |", "|---|---|---|---|---|---|---|"]
    for i, cid in enumerate(res["ranking"], 1):
        s = scores[cid]
        cargo = ", ".join(f"{q} {g}" for g, q in s["cargo"].items()) or "—"
        lines.append(f"| {i} | {s['name']} | {s['home']} | {s['state']} | {s['silver']} | {cargo} | {s['score']} |")
    lines += ["", "## What each barkeep heard", ""]
    for port, entries in sim.barkeep.items():
        lines += [f"### {port} ({len(entries)} statements)", ""]
        lines += [f"- [day {e['day']}] {e['name']}: \"{e['text']}\"" for e in entries] or ["(nothing)"]
        lines.append("")
    (run_dir / "summary.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Run the Bronze Age trade simulation")
    parser.add_argument("--seed", type=int, default=None, help="Random if omitted (recorded in the run)")
    parser.add_argument("--captains", type=int, default=None, help="Override the number of captains")
    parser.add_argument("--days", type=int, default=None, help="Override the number of days")
    parser.add_argument("--player", choices=["model", "random", "informed"], default="model",
                        help="model: Claude captains; random: rule-of-thumb; informed: rule-based logbook + gossip")
    parser.add_argument("--fake", action="store_true", help="Same as --player random")
    parser.add_argument("--model", default=None, help="Override the model in config.json")
    parser.add_argument("--config", default=None,
                        help="Use another config file, e.g. runs/<timestamp>/config.json to replay a run's world")
    args = parser.parse_args()

    if args.fake:
        args.player = "random"
    config = json.loads(Path(args.config).read_text() if args.config else (HERE / "config.json").read_text())
    if args.model:
        config["model"] = args.model
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)

    suffix = {"model": "", "random": "-fake", "informed": "-informed"}[args.player]
    run_dir = HERE / "runs" / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + suffix)
    (run_dir / "transcripts").mkdir(parents=True, exist_ok=True)
    events_file = open(run_dir / "events.jsonl", "a")
    console = open(run_dir / "console.log", "a")

    def say(text=""):
        print(text, flush=True)
        console.write(text + "\n")
        console.flush()

    def sink(event):                  # stream events so a crashed run still leaves a full log
        events_file.write(json.dumps(event) + "\n")
        events_file.flush()
        kind = event["event"]
        if kind == "session":
            say(f"day {event['day']:>3} {event['port']:<9} arrive {event['newcomers']} woken {event['woken']}")
        elif kind == "trade":
            say(f"          {event['captain']}: {event['side']} {event['qty']} {event['good']} "
                f"for {event['total']} ({event['price_before']} -> {event['price_after']})")
        elif kind == "statement":
            say(f"          {event['name']} (round {event['round']}): \"{event['text']}\"")
        elif kind == "sail":
            say(f"          {event['captain']}: sails {event['origin']} -> {event['dest']} (arrives day {event['arrive_day']})")
        elif kind == "wait":
            say(f"          {event['captain']}: waits in {event['port']} until day {event['until']}")
        elif kind in ("stranded", "api_error", "default_wait"):
            say(f"          !! {kind}: {event}")

    sim = Sim(config, seed=seed, event_sink=sink, n_captains=args.captains, days=args.days)
    (run_dir / "config.json").write_text(json.dumps({**config, "seed": seed, "captains": len(sim.captains),
                                                     "days": sim.days}, indent=2))
    if args.player == "random":
        from fake_agent import FakePlayer
        player = FakePlayer(seed)
    elif args.player == "informed":
        from informed_agent import InformedPlayer
        player = InformedPlayer(seed)
    else:
        load_dotenv()
        from agent import CaptainPlayer
        player = CaptainPlayer(run_dir / "transcripts", config)

    say(f"Run: {run_dir}  (seed {seed}, {len(sim.captains)} captains, {sim.days} days)")
    aborted = None
    try:
        res = sim.run(player)
    except Exception as e:            # e.g. out of API credits: keep everything logged so far
        aborted = f"{type(e).__name__}: {e}"
        say(f"\n!! ABORTED: {aborted}")
        res = sim.finish()
    events_file.close()
    if args.player == "model":
        res["usage"] = player.usage
    res["aborted"] = aborted
    (run_dir / "results.json").write_text(json.dumps(res, indent=2))
    write_summary(sim, res, run_dir, aborted)
    top = res["ranking"][:5]
    say("\n=== Top 5 ===")
    for cid in top:
        s = res["scores"][cid]
        say(f"{s['name']} of {s['home']}: {s['score']}")
    if args.player == "model":
        say(f"Usage: {player.usage}")
    try:                              # always leave a playback page next to the run
        from viewer import write_viewer
        say(f"Viewer: {write_viewer(run_dir)}")
    except Exception as e:
        say(f"(viewer not generated: {type(e).__name__}: {e})")


if __name__ == "__main__":
    main()
