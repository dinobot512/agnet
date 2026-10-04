"""The only module that calls a model: JSON-schema answers, a disk cache, refusal checks, a cost cap.

Server-side refusal fallbacks are on ("default" routing): if the model declines, the API re-runs
the request on an Anthropic-chosen fallback model. `salt` separates repeated samples of the same
request in the cache. `tokens` counts every answer used (cached or not), for per-run cost reports;
`spent_usd` counts only real API calls, for the cap.
"""

from __future__ import annotations

import hashlib
import json
from importlib import resources
from pathlib import Path

import anthropic

# USD per million tokens (input, output), from the Anthropic docs 2026-09-25. Estimate only.
PRICES = {"claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0), "claude-haiku-4-5": (1.0, 5.0)}


class LLM:
    def __init__(self, model: str = "claude-opus-5-5", effort: str = "medium",
                 cache_dir: str | Path | None = None, cost_cap_usd: float | None = None, client=None):
        self.model, self.effort, self.cost_cap_usd = model, effort, cost_cap_usd
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.client = client or anthropic.Anthropic()
        self.spent_usd = 0.0
        self.tokens = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}   # input = all input incl. cached
        self.calls: list[dict] = []                      # per real API call: input, output, cache_read, cache_write

    def codebook(self, prompt_version: str) -> str:
        """Tag for outputs: which prompt and model produced them."""
        return f"{prompt_version}@{self.model}"

    def json(self, system: str, user: str, schema: dict, salt: int | str = 0) -> dict:
        params = dict(model=self.model, max_tokens=16000, system=system,
                      messages=[{"role": "user", "content": user}],
                      output_config={"effort": self.effort,
                                     "format": {"type": "json_schema", "schema": schema}})
        key = hashlib.sha256(json.dumps([params, salt], sort_keys=True).encode()).hexdigest()
        cached = self.cache_dir / f"{key}.json" if self.cache_dir else None
        if cached and cached.exists():
            hit = json.loads(cached.read_text())
            self._count(hit["usage"])
            return hit["out"]

        if self.cost_cap_usd is not None and self.spent_usd >= self.cost_cap_usd:
            raise RuntimeError(f"cost cap reached: ${self.spent_usd:.2f} of ${self.cost_cap_usd:.2f}")
        resp = self.client.beta.messages.create(
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
            cache_control={"type": "ephemeral"}, **params)
        if resp.stop_reason != "end_turn":
            raise RuntimeError(f"stop_reason={resp.stop_reason} {getattr(resp, 'stop_details', '')}")

        u = resp.usage
        write, read = getattr(u, "cache_creation_input_tokens", 0) or 0, getattr(u, "cache_read_input_tokens", 0) or 0
        usage = {"input": u.input_tokens + write + read, "output": u.output_tokens,
                 "cache_read": read, "cache_write": write}
        self.calls.append(usage)
        pin, pout = PRICES.get(resp.model, (0.0, 0.0))     # cache writes 1.25x input, reads 0.1x
        self.spent_usd += ((u.input_tokens + 1.25 * write + 0.1 * read) * pin + u.output_tokens * pout) / 1e6
        self._count(usage)
        out = json.loads(next(b.text for b in resp.content if b.type == "text"))
        if cached:
            cached.write_text(json.dumps({"out": out, "usage": usage}))
        return out

    def _count(self, usage: dict) -> None:
        for k in self.tokens:
            self.tokens[k] += usage.get(k, 0)


def load_prompt(name: str) -> str:
    """Read gleeb/prompts/<name>.md, e.g. load_prompt("rubric")."""
    return resources.files("gleeb").joinpath("prompts", f"{name}.md").read_text(encoding="utf-8")
