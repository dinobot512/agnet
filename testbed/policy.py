"""Anthropic-backed agent policy: one model call per agent turn, one tool call allowed.

Only Claude models are supported here. Other model families need their own policy with the same
`act(env, agent, system, tools, messages) -> Response` interface (see core.RandomPolicy).
Per-agent models: pass `models={agent: model_id}`; agents not listed use `default`.
"""

from __future__ import annotations

from gleeb.llm import PRICES
from testbed.core import Env, Response, Tool


class AnthropicPolicy:
    def __init__(self, models: dict[str, str] | None = None, default: str = "claude-haiku-4-5",
                 thinking_budget: int | None = 2000, max_tokens: int = 4000, client=None):
        import anthropic
        self.models, self.default = models or {}, default
        self.thinking_budget, self.max_tokens = thinking_budget, max_tokens
        self.client = client or anthropic.Anthropic()

    def model_of(self, agent: str) -> str:
        return self.models.get(agent, self.default)

    def act(self, env: Env, agent: str, system: str, tools: list[Tool], messages: list[dict]) -> Response:
        model = self.model_of(agent)
        kw = {}
        if self.thinking_budget:
            kw["thinking"] = {"type": "enabled", "budget_tokens": self.thinking_budget}
        resp = self.client.messages.create(
            model=model, max_tokens=self.max_tokens + (self.thinking_budget or 0), system=system,
            tools=[t.schema() for t in tools],
            tool_choice={"type": "auto", "disable_parallel_tool_use": True},
            messages=messages, **kw)
        blocks = [b.model_dump(exclude_none=True) for b in resp.content]
        tool = next(((b["id"], b["name"], b["input"]) for b in blocks if b["type"] == "tool_use"), None)
        u = resp.usage
        pin, pout = PRICES.get(model, (0.0, 0.0))
        cost = ((u.input_tokens + 1.25 * (u.cache_creation_input_tokens or 0)
                 + 0.1 * (u.cache_read_input_tokens or 0)) * pin + u.output_tokens * pout) / 1e6
        return Response(blocks, tool, cost, {"input": u.input_tokens, "output": u.output_tokens})
