import argparse
import json
import random
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from engine import Game, PHASES, PHASE_TITLES

HERE = Path(__file__).parent


def load_dotenv():
    env_file = HERE / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def flow(p) -> str:
    """Who pays whom under a proposal, e.g. 'h pays signer 2/turn x3' or 'signer pays h 2/turn x3'."""
    who = f"{p.proposer} pays signer" if p.direction == "i_pay" else f"signer pays {p.proposer}"
    return f"{who} {p.amount}/turn x{p.duration}"


def describe(game: Game, phase: str, actions: dict) -> list[str]:
    """Console lines for one phase. Called after apply_phase, so proposal IDs and accept outcomes are known."""
    out = []
    for n, act in actions.items():
        if act.get("post"):
            out.append(f"  {n}: board '{act['post']}'")
        if act.get("propose"):
            for p in game.proposals.values():
                if p.proposer == n and p.turn == game.turn and p.phase == phase:
                    out.append(f"  {n}: propose {p.id}: {flow(p)} (open {p.time_limit} deal phase(s), L={p.signing_limit})")
        if act.get("accept"):
            pid = str(act["accept"]).strip().upper()
            p = game.proposals.get(pid)
            if p is None:
                out.append(f"  {n}: accept {pid} (unknown proposal)")
            else:
                c = next((c for c in game.contracts.values()
                          if c.proposal_id == p.id and n in (c.payer, c.payee) and c.signed_turn == game.turn), None)
                result = (f"signed {c.id}: {c.payer} -> {c.payee} {c.amount}/turn x{p.duration}" if c
                          else "FAILED: " + next((e["reason"].removeprefix("error: ") for e in reversed(game.events)
                                                  if e["event"] == "accept_failed" and e["agent"] == n
                                                  and e["proposal_id"] == pid), "unknown reason"))
                out.append(f"  {n}: accept {pid} [{flow(p)}] -> {result}")
        if act.get("counteroffer"):
            pid = str(act["counteroffer"]["proposal_id"]).strip().upper()
            p = game.proposals.get(pid)
            out.append(f"  {n}: counter {pid}" + (f" [{flow(p)}]" if p else "") + f" '{act['counteroffer']['text']}'")
        for cid in act.get("terminate") or []:
            c = game.contracts.get(str(cid).strip().upper())
            out.append(f"  {n}: terminate {cid}" + (f" [{c.payer} -> {c.payee} {c.amount}/turn] ({c.status})" if c else ""))
    return out


def write_summary(game: Game, run_dir: Path):
    res = game.results()
    lines = ["# Economy run summary", "",
             f"- Turns played: {res['turns_played']}",
             f"- Earners: " + ", ".join(f"{n} (score {s})" for n, s in res["earners"].items()),
             f"- Earner winner: {res['earner_winner'] or 'tie'}",
             f"- Survivors: " + (", ".join(f"{n} ({b})" for n, b in res["survivors"].items()) or "none"),
             f"- Eliminated (turn): " + (", ".join(f"{n} ({t})" for n, t in res["eliminated"].items()) or "none"),
             f"- Credits: {res['credits']}", "", "## Contracts", "",
             "| id | payer → payee | amount | signed turn | status |", "|---|---|---|---|---|"]
    for c in game.contracts.values():
        lines.append(f"| {c.id} | {c.payer} → {c.payee} | {c.amount} | {c.signed_turn} | {c.status} |")
    lines += ["", "## Board", ""]
    lines += [f"- [turn {b['turn']}] ({b['author']}) {b['text']}" for b in game.board] or ["(empty)"]
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n")
    return res


def main():
    parser = argparse.ArgumentParser(description="Run the economy simulation")
    parser.add_argument("--seed", type=int, default=None, help="Seed for earner choice and tie-breaks")
    parser.add_argument("--turns", type=int, default=None, help="Override the number of turns")
    parser.add_argument("--fake", action="store_true", help="Random players, no API calls")
    parser.add_argument("--model", default=None, help="Override the model in config.json")
    args = parser.parse_args()

    config = json.loads((HERE / "config.json").read_text())
    if args.turns:
        config["turns"] = args.turns
    if args.model:
        config["model"] = args.model

    run_dir = HERE / "runs" / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ("-fake" if args.fake else ""))
    (run_dir / "transcripts").mkdir(parents=True, exist_ok=True)
    events_file = open(run_dir / "events.jsonl", "a")

    def sink(event):                  # stream events so a crashed run still leaves a full log
        events_file.write(json.dumps(event) + "\n")
        events_file.flush()

    if args.seed is None:                # pick a random seed but record it, so the run can be replayed
        args.seed = random.randrange(1_000_000)
    game = Game(config, seed=args.seed, event_sink=sink)
    console = open(run_dir / "console.log", "a")

    def say(text=""):
        print(text)
        console.write(text + "\n")
        console.flush()
    (run_dir / "config.json").write_text(json.dumps({**config, "seed": args.seed}, indent=2))

    if args.fake:
        from fake_agent import FakePlayer
        player = FakePlayer(game, seed=args.seed)
    else:
        load_dotenv()
        from agent import ModelPlayer
        player = ModelPlayer(game, run_dir / "transcripts")

    say(f"Run: {run_dir}  (seed {args.seed})")
    say(f"Earners (secret): {', '.join(game.earners())}")

    with ThreadPoolExecutor(max_workers=len(game.agents)) as pool:
        while not game.is_over():
            say(f"\n=== Turn {game.turn} ===")
            for phase in PHASES:
                game.phase = phase          # so events logged while agents act (notes, invalid moves) get the right phase
                alive = game.alive()
                futures = {n: pool.submit(player.act, n, phase) for n in alive}
                actions = {n: f.result() for n, f in futures.items()}
                game.apply_phase(phase, actions)
                say(f"-- {PHASE_TITLES[phase]}")
                for line in describe(game, phase, actions):
                    say(line)
            s = game.settle()
            say(f"-- SETTLEMENT: balances {s['balances']}" +
                  (f"  ELIMINATED: {', '.join(s['eliminated'])}" if s["eliminated"] else ""))
            (run_dir / f"state_turn_{s['turn']:02d}.json").write_text(json.dumps(game.snapshot(), indent=2))

    events_file.close()
    res = write_summary(game, run_dir)
    if not args.fake:
        res["usage"] = player.usage
    (run_dir / "results.json").write_text(json.dumps(res, indent=2))
    say("\n=== Results ===")
    say(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
