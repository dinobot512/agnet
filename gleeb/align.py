"""Pairwise goal judge, alignment of two goal streams, and the sample-to-sample noise floor.

Goals are compared only by the judge (same | refinement | different), never by string or
embedding similarity. Alignment matches spans by temporal overlap, then keeps a pair only if the
judge says it is not "different".
"""

from __future__ import annotations

from itertools import combinations

from gleeb.llm import LLM, load_prompt
from gleeb.schema import Alignment, GoalSpan, GoalStream, SpanMatch

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"verdict": {"type": "string", "enum": ["same", "refinement", "different"]},
                   "reason": {"type": "string"}},
    "required": ["verdict", "reason"],
    "additionalProperties": False,
}


def judge(llm: LLM, a: str, b: str) -> dict:
    """Compare two goals. -> {"verdict": same|refinement|different, "reason": str}"""
    return llm.json(load_prompt("judge"), f"Goal A: {a}\nGoal B: {b}", JUDGE_SCHEMA)


def align(a: GoalStream, b: GoalStream, llm: LLM) -> Alignment:
    pairs = sorted(((x.overlap(y), x, y) for x in a.spans for y in b.spans if x.overlap(y) > 0),
                   key=lambda p: -p[0])
    used_a, used_b, matches = set(), set(), []
    for ov, x, y in pairs:
        if x.id in used_a or y.id in used_b:
            continue
        v = judge(llm, x.goal, y.goal)
        if v["verdict"] == "different":
            continue
        used_a.add(x.id)
        used_b.add(y.id)
        matches.append(SpanMatch(x.id, y.id, ov, GoalSpan.mid(y.start) - GoalSpan.mid(x.start),
                                 GoalSpan.mid(y.end) - GoalSpan.mid(x.end), v["verdict"], v["reason"]))
    return Alignment(a.agent, a.id, b.id, matches,
                     [x.id for x in a.spans if x.id not in used_a],
                     [y.id for y in b.spans if y.id not in used_b])


def matched_fraction(al: Alignment) -> float:
    n = 2 * len(al.matches) + len(al.a_only) + len(al.b_only)
    return 2 * len(al.matches) / n if n else 1.0


def boundary_agreement(a: GoalStream, b: GoalStream) -> float:
    """Fraction of boundaries (span starts after the first) whose range overlaps one in the other stream."""
    ba, bb = [s.start for s in a.spans[1:]], [s.start for s in b.spans[1:]]
    if not ba and not bb:
        return 1.0
    hit = lambda r, others: any(r[0] <= o[1] and o[0] <= r[1] for o in others)
    return (sum(hit(r, bb) for r in ba) + sum(hit(r, ba) for r in bb)) / (len(ba) + len(bb))


def noise_floor(samples: list[GoalStream], llm: LLM) -> dict:
    """Disagreement between samples of one configuration (0 = identical)."""
    pairs = list(combinations(samples, 2))
    if not pairs:
        return {"span_disagreement": None, "boundary_disagreement": None}
    return {"span_disagreement": sum(1 - matched_fraction(align(x, y, llm)) for x, y in pairs) / len(pairs),
            "boundary_disagreement": sum(1 - boundary_agreement(x, y) for x, y in pairs) / len(pairs)}
