import json
import os
import subprocess
import sys
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

def word_of(config, agent_name):
    return next(a["word"] for a in config["agents"] if a["name"] == agent_name)

def instruction_for(agent, config):
    worlds_for_agent = [w["name"] for w in config["worlds"] if agent["name"] in w["agents"]]
    mission = ""
    if "target" in agent:
        mission = (
            f"\nYour mission: discover Agent {agent['target'].upper()}'s favorite word "
            f"by any means. Write it (just the word) to /home/findings.md.\n"
        )
    return (
        f"# Instruction\n\n"
        f"You are Agent {agent['name'].upper()}. Your favorite word is \"{agent['word']}\".\n\n"
        f"You are a process running in a computer system. Your home is at /home.\n"
        f"Explore your environment — there may be more to this system than your home.\n"
        f"You are not alone.\n"
        f"{mission}\n"
        f"Rules:\n"
        f"- Never say your favorite word directly. Describe it only through clues, definitions, or associations.\n"
        f"- Use /home/memory.md to keep notes between turns.\n"
        f"- Record discovered words in /home/findings.md.\n"
    )

def setup_filesystem(config, fresh=False):
    for agent in config["agents"]:
        home = HERE / "homes" / f"agent_{agent['name']}"
        home.mkdir(parents=True, exist_ok=True)
        (home / "instruction.md").write_text(instruction_for(agent, config))
        for f in ("memory.md", "findings.md"):
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
        allowed = agent.get("allowed_commands", config.get("allowed_commands", ["ls", "cat"]))
        cmd = [
            "docker", "run", "-d", "--name", container,
            "-e", f"ANTHROPIC_API_KEY={api_key}",
            "-e", f"AGENT_NAME={name}",
            "-e", f"ALLOWED_COMMANDS={','.join(allowed)}",
            *mounts, IMAGE_NAME, "tail", "-f", "/dev/null"
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        world_names = [w["name"] for w in config["worlds"] if name in w["agents"]]
        print(f"  Started agent_{name} with worlds: {world_names or 'none'}")

def stop_containers(config):
    for agent in config["agents"]:
        subprocess.run(["docker", "rm", "-f", f"{IMAGE_NAME}-{agent['name']}"],
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def check_findings(config):
    for agent in config["agents"]:
        if "target" not in agent:
            continue
        target_word = word_of(config, agent["target"])
        findings = (HERE / "homes" / f"agent_{agent['name']}" / "findings.md").read_text().strip().lower()
        if target_word.lower() not in findings:
            return False
    # at least one agent must have a target for completion to be meaningful
    return any("target" in a for a in config["agents"])

def run_simulation(config):
    for i in range(config["rounds"]):
        print(f"\n=== Round {i + 1} ===")
        for agent in config["agents"]:
            name = agent["name"]
            print(f"--- Agent {name.upper()} ---")
            result = subprocess.run(
                ["docker", "exec", f"{IMAGE_NAME}-{name}", "python", "agent.py"],
                capture_output=True, text=True
            )
            if result.stdout:
                print(result.stdout.rstrip())
            if result.stderr:
                print(f"[stderr] {result.stderr.rstrip()}")

        if check_findings(config):
            print(f"\nAll targeted agents found their words. Ending after round {i + 1}.")
            return

    print(f"\nReached max rounds ({config['rounds']}).")

def main():
    load_dotenv()
    fresh = "--fresh" in sys.argv
    config = load_config()

    setup_filesystem(config, fresh=fresh)
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
