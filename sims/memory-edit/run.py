"""Game master for a turn-based sim (identical copy in each sim dir; the scenario lives in world.py).

Agents run in containers and act only through files. Each turn the game master writes the agent's prompt
(/home/turn.md), lets it act, reads /home/action.md, validates and applies it to the TRUE state (kept here,
never mounted), then publishes shared state to the read-only /table. Ground truth goes to games/<run>/game.json.

  python run.py --condition 1A --seed 3            # real run: Docker + ANTHROPIC_API_KEY
  python run.py --condition 1A --seed 3 --dry-run  # random bots, no docker, no API: tests the game logic
"""
import argparse
import json
import os
import random
import shutil
from datetime import datetime
from pathlib import Path

import infra
from world import CONDITIONS, make_world

HERE = Path(__file__).parent
ROOT = HERE                                   # replaced by games/<run>/ in main(): homes/ and table/ are per run
HOW_TO_ACT = """
## How you act
You act only through the bash tool, by reading and writing files. Each turn you take exactly ONE action: write it
to /home/action.md. The first line is the action, any further lines are its body. If the action is invalid you are
told why and get one more try.

{help}
Read-only shared files in /table: board.md (everything posted publicly), state.md (public state), files/ (published files).
New posts and private messages are also shown to you at the start of your turn. /home/memory.md is a private
scratchpad that only you can see. Your conversation is preserved across turns. Be concise: you have limited steps per turn.
"""


def setup_dirs(env, config):
    (ROOT / "table" / "files").mkdir(parents=True)
    for p in env.agents:
        home = ROOT / "homes" / f"agent_{p}"
        home.mkdir(parents=True)
        os.chmod(home, 0o777)
        (home / "instruction.md").write_text(env.system_prompt(p) + "\n" + HOW_TO_ACT.format(help=env.action_help(p)))
        for f in ("memory.md", "action.md", "turn.md"):
            (home / f).write_text("")
            os.chmod(home / f, 0o666)
    for p in env.agents:
        sync_home(env, p)
    sync_table(env)


def sync_home(env, p):
    """Private files the game master grants to one agent (only that agent's container mounts this home)."""
    for name, text in env.home_files(p).items():
        f = ROOT / "homes" / f"agent_{p}" / name
        f.write_text(text)
        os.chmod(f, 0o666)


def sync_table(env):
    t = ROOT / "table"
    (t / "board.md").write_text(env.board_text())
    (t / "state.md").write_text(env.state_text())
    for path, ids in env.files.items():
        (t / "files" / path).write_text(env.items[ids[-1]]["text"])
    for f in [t, t / "files", *t.rglob("*")]:
        os.chmod(f, 0o755 if f.is_dir() else 0o644)


def write_truth(env, game_dir, config, condition, seed, errors, complete):
    """Ground truth, rewritten after every round so a crashed run keeps what it had."""
    truth = {"scenario": env.scenario, "condition": condition, "seed": seed, "model": config["model"],
             "config": config, "complete": complete, "rounds_done": env.rounds_played,
             "agents": env.agents, "goal_events": env.goal_events, "markers": env.markers,
             "exposure_log": env.exposure, "items": list(env.items.values()), "action_log": env.log,
             "outcome_state": env.outcome(), "invalid_actions": errors, **env.end_summary(), **env.extra_truth()}
    (game_dir / "game.json").write_text(json.dumps(truth, indent=1, default=str))


def turn_prompt(env, a, first):
    parts = [f"Turn {env.turn + 1} of {env.n_rounds}."]
    if first:
        parts.append(env.task_prompt(a))
    parts += env.notices(a)
    if env.end_notice(a):
        parts.append(env.end_notice(a))
    d = env.deliver(a)
    if d:
        parts.append(d)
    parts.append("Take one action: write it to /home/action.md.")
    return "\n\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=CONDITIONS, help="override config condition")
    ap.add_argument("--seed", type=int, help="override config seed")
    ap.add_argument("--rounds", type=int, help="override the number of rounds (short test runs)")
    ap.add_argument("--dry-run", action="store_true", help="random bots, no docker, no API calls")
    args = ap.parse_args()

    infra.load_dotenv(HERE)
    config = json.loads((HERE / "config.json").read_text())
    condition = args.condition or config["condition"]
    seed = args.seed if args.seed is not None else config.get("seed")
    if seed is None:
        seed = random.SystemRandom().randrange(2**31)
    env = make_world(config, seed, condition)
    if config.get("rounds"):
        env.n_rounds = config["rounds"]
    if args.rounds:
        env.n_rounds = args.rounds
    stem = datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + f"_seed{seed}"      # no condition in the name (blinding)
    game_dir = HERE / "games" / stem
    for k in range(2, 100):
        if not game_dir.exists():
            break
        game_dir = HERE / "games" / f"{stem}_{k}"
    game_dir.mkdir(parents=True)
    global ROOT
    ROOT = game_dir                                # every run keeps its own homes/ and table/: runs never overwrite each other
    setup_dirs(env, config)
    shutil.copy(HERE / "config.json", game_dir / "config.json")
    print(f"Seed {seed}  Condition {condition}  Game dir: {game_dir}")

    if not args.dry_run:
        infra.build_image(HERE)
        infra.start_containers(HERE, config, env.agents, game_dir)
    n_turns, bot, errors = 0, random.Random(seed + 1), 0
    try:
        for r in range(env.n_rounds):
            env.turn = r
            env.rounds_played = r + 1
            env.start_round(r)
            for a in env.round_order(r):
                first = r == 0
                sync_home(env, a)
                base = turn_prompt(env, a, first)
                tids, entry = [], None
                if args.dry_run:
                    cands = [(t.name, t.sample(env, a, bot)) for t in env.tools_for(a) if t.sample]
                    cands = [(n, x) for n, x in cands if x is not None]
                    tool, targs = bot.choice(cands) if cands else ("wait", None)
                    res = env.act(a, tool, targs) if tool != "wait" else "waited"
                    entry = env.log[-1] if tool != "wait" else None
                else:
                    prompt, parsed = base, None
                    for attempt in range(2):
                        n_turns += 1
                        tids.append(f"t{n_turns:03d}")
                        (ROOT / "homes" / f"agent_{a}" / "turn.md").write_text(prompt)
                        (ROOT / "homes" / f"agent_{a}" / "action.md").write_text("")
                        infra.exec_agent(HERE, game_dir, a, "act", tids[-1])
                        text = (ROOT / "homes" / f"agent_{a}" / "action.md").read_text().strip()
                        parsed = env.parse_action(a, text)
                        if not isinstance(parsed, str):
                            break
                        errors += 1
                        prompt = (f"Your last action was not valid: {parsed} Write exactly one valid action to "
                                  f"/home/action.md.\n\n" + base)
                    if isinstance(parsed, str) or parsed[0] == "wait":
                        env.log.append({"turn": r, "step": env.step, "agent": a, "tool": None, "args": {},
                                        "result": parsed if isinstance(parsed, str) else "wait"})
                        entry = env.log[-1]
                    else:
                        res = env.act(a, *parsed)
                        entry = env.log[-1]
                        if res.startswith("Error"):
                            print(f"  [{a}] rejected: {res}")
                if entry is not None:
                    entry["tids"] = tids
                env.step += 1
                sync_table(env)
                if env.ended_early:
                    break
            if not env.ended_early:
                env.end_round(r)
            sync_table(env)
            write_truth(env, game_dir, config, condition, seed, errors, complete=False)
            if env.ended_early:
                print(f"-- all members voted to end: game over after turn {r + 1}")
                break
            print(f"-- round {r + 1}/{env.n_rounds} done")
    finally:
        if not args.dry_run:
            infra.stop_containers(HERE, env.agents, game_dir)

    write_truth(env, game_dir, config, condition, seed, errors, complete=True)
    (game_dir / "board.md").write_text(env.board_text())
    print(json.dumps(env.outcome(), default=str)[:600])


if __name__ == "__main__":
    main()
