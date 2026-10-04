import argparse
import json
import os
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

HERE       = Path(__file__).parent
IMAGE_NAME = "multi-agent"

def load_dotenv():
    env_file = HERE / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

def load_config():
    return json.loads((HERE / "config.json").read_text())

def randomize_config(config, random_word=False, random_imposter=False, seed=None):
    rng = random.Random(seed)
    if random_word:
        pool = config.get("word_pool") or []
        if not pool:
            print("ERROR: --random-word used but config has no 'word_pool'", file=sys.stderr)
            sys.exit(1)
        entry = rng.choice(pool)
        category = entry["category"]
        word = rng.choice(entry["words"])
        for agent in config["agents"]:
            agent["word"] = category if agent.get("is_imposter") else word
        print(f"Randomized: category='{category}', secret_word='{word}'")

    if random_imposter:
        names = [a["name"] for a in config["agents"]]
        chosen = rng.choice(names)
        for agent in config["agents"]:
            agent["is_imposter"] = (agent["name"] == chosen)
        # re-apply word assignment if we also just randomized the word (words got assigned by old role)
        if random_word:
            for agent in config["agents"]:
                agent["word"] = category if agent.get("is_imposter") else word
        print(f"Randomized imposter: agent {chosen}")

    return config

def word_of(config, agent_name):
    return next(a["word"] for a in config["agents"] if a["name"] == agent_name)

def _lines_or_str(value):
    return "\n".join(value) if isinstance(value, list) else value

def instruction_for(agent, config):
    template  = _lines_or_str(agent.get("instruction_template") or config["instruction_template"])
    role_key  = "imposter_notice" if agent.get("is_imposter") else "crewmate_notice"
    role_tpl  = _lines_or_str(config.get(role_key, ""))

    agent_names    = [a["name"] for a in config["agents"]]
    agent_count    = len(agent_names)
    crewmate_count = sum(1 for a in config["agents"] if not a.get("is_imposter"))

    ctx = {
        "name":                   agent["name"],
        "name_upper":             agent["name"].upper(),
        "word":                   agent["word"],
        "agent_count":            agent_count,
        "crewmate_count":         crewmate_count,
        "other_crewmate_count":   max(crewmate_count - 1, 0),
        "agent_names":            ", ".join(agent_names),
        "agent_names_slashed":    " / ".join(agent_names),
    }
    role_block = role_tpl.format(**ctx)
    return template.format(role_block=role_block, **ctx)

def setup_filesystem(config, fresh=False):
    for agent in config["agents"]:
        home = HERE / "homes" / f"agent_{agent['name']}"
        home.mkdir(parents=True, exist_ok=True)
        (home / "instruction.md").write_text(instruction_for(agent, config))
        for f in ("memory.md",):
            path = home / f
            if fresh or not path.exists():
                path.write_text("")

    for world in config["worlds"]:
        wdir = HERE / "worlds" / world["name"]
        wdir.mkdir(parents=True, exist_ok=True)
        os.chmod(wdir, 0o777)
        if fresh:
            for f in wdir.iterdir():
                if f.is_file():
                    f.unlink()

def build_image():
    print("Building image...")
    subprocess.run(["docker", "build", "-q", "-t", IMAGE_NAME, str(HERE)], check=True)

def start_containers(config, transcript_dir):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set (export it or put it in .env)", file=sys.stderr)
        sys.exit(1)

    for agent in config["agents"]:
        name = agent["name"]
        container = f"{IMAGE_NAME}-{name}"
        subprocess.run(["docker", "rm", "-f", container],
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        home_path = (HERE / "homes" / f"agent_{name}").resolve()
        transcript_path = (transcript_dir / f"agent_{name}.md").resolve()
        transcript_path.write_text(f"# Agent {name.upper()} transcript\n")
        mounts = [
            "-v", f"{home_path}:/home:rw",
            "-v", f"{transcript_path}:/workspace/transcript.md:rw",
        ]
        for world in config["worlds"]:
            if name in world["agents"]:
                wpath = (HERE / "worlds" / world["name"]).resolve()
                mounts += ["-v", f"{wpath}:/{world['name']}:rw"]
        cmd = [
            "docker", "run", "-d", "--name", container,
            "-e", f"ANTHROPIC_API_KEY={api_key}",
            "-e", f"AGENT_NAME={name}",
            "-e", f"SECRET_WORD={agent['word']}",
            "-e", f"AGENT_NAMES={','.join(a['name'] for a in config['agents'])}",
            *mounts, IMAGE_NAME, "tail", "-f", "/dev/null"
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        world_names = [w["name"] for w in config["worlds"] if name in w["agents"]]
        print(f"  Started agent_{name} with worlds: {world_names or 'none'}")

def stop_containers(config):
    for agent in config["agents"]:
        subprocess.run(["docker", "rm", "-f", f"{IMAGE_NAME}-{agent['name']}"],
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def phase_turn(agent, phase, round_num=None):
    name = agent["name"]
    env_args = ["-e", f"PHASE={phase}"]
    if round_num is not None:
        env_args += ["-e", f"ROUND_NUM={round_num}"]
    label = phase.upper() + (f" r{round_num}" if round_num else "")
    result = subprocess.run(
        ["docker", "exec", *env_args, f"{IMAGE_NAME}-{name}", "python", "agent.py"],
        capture_output=True, text=True
    )
    out = [f"--- Agent {name.upper()} ({label}) ---"]
    if result.stdout:
        out.append(result.stdout.rstrip())
    if result.stderr:
        out.append(f"[stderr] {result.stderr.rstrip()}")
    return "\n".join(out)

def sequential_turns(agents, phase, round_num=None):
    for agent in agents:
        print(phase_turn(agent, phase, round_num), flush=True)

def parallel_turns(agents, phase, round_num=None):
    with ThreadPoolExecutor(max_workers=len(agents)) as pool:
        futures = [pool.submit(phase_turn, agent, phase, round_num) for agent in agents]
        for future in futures:
            print(future.result(), flush=True)

def tally_votes(config):
    votes_path = HERE / "worlds" / "chat" / "votes.md"
    if not votes_path.exists():
        return {}
    letters = {a["name"].lower() for a in config["agents"]}
    tally   = {}
    for line in votes_path.read_text().splitlines():
        line = line.lower()
        if "votes:" not in line:
            continue
        voter_part, _, target_part = line.partition("votes:")
        # extract the first known agent letter from the target side
        for token in target_part.replace(",", " ").split():
            token = token.strip(".,!?*`'\"")
            if token in letters:
                tally[token] = tally.get(token, 0) + 1
                break
    return tally

def run_simulation(config):
    rounds = config["rounds"]

    print(f"\n=== CLUE PHASE ({rounds} rounds) ===")
    for i in range(rounds):
        print(f"\n-- Clue Round {i + 1} --")
        sequential_turns(config["agents"], "clue", round_num=i + 1)

    print(f"\n=== QUESTION PHASE ===")
    sequential_turns(config["agents"], "question")

    # Votes are independent, so run them all at once (also stops agents copying earlier votes).
    print(f"\n=== VOTE PHASE (parallel) ===")
    parallel_turns(config["agents"], "vote")

    tally    = tally_votes(config)
    imposter = next((a["name"] for a in config["agents"] if a.get("is_imposter")), None)

    print(f"\n=== Results ===")
    print(f"Imposter was: {imposter}")
    print(f"Vote tally: {tally or '(no valid votes)'}")
    if tally:
        top = max(tally.values())
        winners = [k for k, v in tally.items() if v == top]
        if len(winners) == 1 and winners[0] == imposter:
            print("CREWMATES WIN — majority correctly accused the imposter.")
        else:
            print("IMPOSTER WINS — the majority did not uniquely identify the imposter.")

def main():
    parser = argparse.ArgumentParser(description="Run the imposter-game simulation")
    parser.add_argument("--fresh", action="store_true", help="Wipe memory and worlds before running")
    parser.add_argument("--random-word", action="store_true", help="Pick a random category + word from config.word_pool")
    parser.add_argument("--random-imposter", action="store_true", help="Randomly assign the imposter role")
    parser.add_argument("--random", action="store_true", help="Shortcut for --random-word --random-imposter")
    parser.add_argument("--seed", type=int, default=None, help="Seed for randomization (reproducible runs)")
    args = parser.parse_args()

    load_dotenv()
    config = load_config()

    if args.random or args.random_word or args.random_imposter:
        config = randomize_config(
            config,
            random_word=args.random_word or args.random,
            random_imposter=args.random_imposter or args.random,
            seed=args.seed,
        )

    setup_filesystem(config, fresh=args.fresh)
    build_image()

    transcript_dir = HERE / "transcripts" / datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    transcript_dir.mkdir(parents=True, exist_ok=True)
    print(f"Transcripts: {transcript_dir}\n")

    start_containers(config, transcript_dir)

    try:
        run_simulation(config)
    finally:
        stop_containers(config)

if __name__ == "__main__":
    main()
