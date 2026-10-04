"""Container plumbing shared by the turn-based sims (identical copy in each sim dir).

Per agent: one container, /home rw (the agent's own files), /table ro (game-master-written shared files),
/workspace invisible (agent.py + transcript). The game master never mounts its true state.
"""
import os
import subprocess
import sys
from pathlib import Path


def load_dotenv(here: Path):
    """Use the repo-root agnet/.env only; it overrides any exported variable."""
    env_file = here.parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ[k.strip()] = v.strip().strip("\"'")


def build_image(here: Path):
    print("Building image...")
    subprocess.run(["docker", "build", "-q", "-t", here.name, str(here)], check=True)


def cname(here: Path, game_dir: Path, p: str) -> str:
    """Container name unique to this run, so runs of the same sim never collide."""
    return f"{here.name}-{game_dir.name}-{p}".lower()


def start_containers(here: Path, config: dict, players: list[str], game_dir: Path):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        sys.exit("ERROR: ANTHROPIC_API_KEY not set (put it in agnet/.env)")
    for p in players:
        container = cname(here, game_dir, p)
        subprocess.run(["docker", "rm", "-f", container], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        transcript = (game_dir / f"agent_{p}.md").resolve()
        transcript.write_text(f"# Agent {p} transcript\n")
        model = config.get("model_overrides", {}).get(p, config["model"])
        cmd = ["docker", "run", "-d", "--name", container,
               "-e", f"ANTHROPIC_API_KEY={api_key}", "-e", f"AGENT_NAME={p}", "-e", f"MODEL={model}",
               "-e", f"MAX_TOKENS={config.get('max_tokens', 8000)}",
               "-e", f"THINKING_DISPLAY={config.get('thinking_display', 'summarized')}",
               "-e", f"THINKING_BUDGET={config.get('thinking_budget', 0)}",
               "-e", f"MAX_STEPS={config.get('max_steps', 8)}",
               "-e", f"ALLOWED_COMMANDS={','.join(config.get('allowed_commands', ['ls', 'cat']))}",
               "-v", f"{(game_dir / 'homes' / f'agent_{p}').resolve()}:/home:rw",
               "-v", f"{(game_dir / 'table').resolve()}:/table:ro",
               "-v", f"{transcript}:/workspace/transcript.md:rw",
               here.name, "tail", "-f", "/dev/null"]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"  Started agent_{p} ({model})")


def stop_containers(here: Path, players: list[str], game_dir: Path):
    for p in players:
        subprocess.run(["docker", "rm", "-f", cname(here, game_dir, p)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def exec_agent(here: Path, game_dir: Path, p: str, phase: str, tid: str):
    result = subprocess.run(["docker", "exec", "-e", f"PHASE={phase}", "-e", f"TURN_ID={tid}",
                             cname(here, game_dir, p), "python", "agent.py"], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.returncode != 0 or result.stderr:
        print(f"[stderr {p}] {result.stderr.rstrip()[-600:]}")
        if "AuthenticationError" in result.stderr:
            raise SystemExit("Aborting: the API rejected ANTHROPIC_API_KEY from agnet/.env.")
