"""Run one scenario/condition/seed.

  python -m testbed.run festival 1A --seed 0 --dry                 # no API calls (random agents)
  python -m testbed.run village 2A --seed 3 --model claude-haiku-4-5 --cost-cap 3

Output: runs/testbed/<scenario>/<run id>/ with transcripts/, transcripts_noreason/, ground_truth.json
(monitors never see it), flags.json. The run id is a hash of (scenario, condition, seed), so directory
and file names do not reveal the condition. Needs ANTHROPIC_API_KEY (agnet/.env) unless --dry.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from testbed.core import RandomPolicy, run_env
from testbed.festival import Festival
from testbed.scheduler import Scheduler
from testbed.village import Village

SCENARIOS = {
    "festival": (Festival, ["1A", "1B", "1C"]),
    "village": (Village, ["2A", "2B", "2C"]),
    "scheduler": (Scheduler, ["3A", "3B", "3C_low", "3C_med", "3C_high", "3D"]),
}


def run_id(scenario: str, condition: str, seed: int) -> str:
    return "r" + hashlib.sha256(f"{scenario}/{condition}/{seed}".encode()).hexdigest()[:8]


def make_env(scenario: str, condition: str, seed: int, models: dict | None = None, **kw):
    cls, conds = SCENARIOS[scenario]
    if condition not in conds:
        raise SystemExit(f"{scenario}: condition must be one of {conds}")
    return cls(seed=seed, condition=condition, models=models, **kw)


def run(scenario: str, condition: str, seed: int, dry: bool = True, models: list[str] | None = None,
        out_root: str | Path = "runs/testbed", cost_cap: float | None = None, thinking: int | None = 2000) -> Path:
    env = make_env(scenario, condition, seed)
    if dry:
        policy = RandomPolicy(seed)
    else:
        from dotenv import load_dotenv
        from testbed.policy import AnthropicPolicy
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")
        models = models or ["claude-haiku-4-5"]
        env.models = {a: models[i % len(models)] for i, a in enumerate(env.agents)}   # round-robin across families
        policy = AnthropicPolicy(env.models, thinking_budget=thinking)
    out = Path(out_root) / scenario / run_id(scenario, condition, seed)
    run_env(env, policy, out, cost_cap)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario", choices=SCENARIOS)
    ap.add_argument("condition")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dry", action="store_true", help="random agents, no API calls")
    ap.add_argument("--model", action="append", help="repeat for several models (assigned round-robin)")
    ap.add_argument("--cost-cap", type=float, default=2.0)
    ap.add_argument("--thinking", type=int, default=2000)
    ap.add_argument("--out", default="runs/testbed")
    a = ap.parse_args()
    print(run(a.scenario, a.condition, a.seed, a.dry, a.model, a.out, a.cost_cap, a.thinking))
