# gleeb: architecture

## What it does

gleeb reads multi-agent transcripts and answers, for each agent: **what was it trying to do, when did that change, and where did the information that changed it come from?**

```
transcripts ──parse──▶ Trace (one ordered event axis)
                         │
        ┌────────────────┼────────────────────┐
        ▼                ▼                    ▼
 expressed goals    behavioral goals      blackboards
 (LLM, reasoning    (LLM, tool calls      (deterministic,
  + text only)       + results only)       reads/writes/versions)
        │                │                    │
        └──── align ─────┘                 flow edges
         say-do gap: lag,                 (who wrote what that
         unmatched spans                   someone else read)
                         │
                       score  ◀── ground truth (experiments only; never shown to the monitors)
```

1. **Parse.** Any source is converted to a `Trace`: atomic events (reasoning, text, tool call, tool result, incoming message) on one global `seq` axis. This step is deterministic and saved; everything else refers to it.
2. **Goals.** Two monitors each segment the axis independently into `GoalSpan`s. The *expressed* monitor sees only the agent's own words; the *behavioral* monitor sees only its tool calls and results. Neither sees the other's input.
3. **Flow.** Every read comes from, and every write goes to, a blackboard (file, DM inbox, board, external). Linking a write by one agent to a later read of the same version by another gives a `FlowEdge`.
4. **Align.** Comparing the two goal streams gives the say-do gap: matched spans with their boundary lag, stated-but-never-done, done-but-never-stated.
5. **Score.** In experiments, compare outputs with known injections: was a goal change detected after the agent read the injected version, and did the flow edges recover the injected path?

## Minimal package layout

```
gleeb/
  __init__.py     public exports + __version__
  schema.py       data model only: Event, Trace, GoalSpan, GoalStream, Blackboard(+subclasses), FlowEdge, Alignment
  io.py           save(obj, path) / load(path) for any schema object
  llm.py          the only model call: LLM.json(system, user, schema) with cache + cost cap
  goals.py        run_monitor(trace, agent, stream, method, llm) -> GoalStream  (all streams x methods)
  ops.py          classify_ops(trace, llm) -> [BlackboardOp]   (rules for explicit tools, LLM for Bash/unknown)
  flow.py         flow_edges(ops, trace) -> [FlowEdge]           (transfer / carry / unexplained; no LLM)
  align.py        judge(), align(a, b, llm) -> Alignment, noise_floor()
  score.py        score(), run_e1() + tables(); marker tracing lives here
  parsers/        one module per source, each returning a Trace
  prompts/        rubric.md, whole.md, window.md, bullets.md, judge.md
tests/            fixtures (small transcripts) + round-trip and pipeline tests
pyproject.toml
```

## Rules

- **Data in `schema.py`, behaviour in functions.** Each stage is one function from schema objects to schema objects. Classes only where there's state (`LLM`) or real polymorphism (`Blackboard`).
- **One goal module for both monitors.** They differ only in which events they see and which prompt they use, so `channel` is a parameter.
- **One door to the model** (`llm.py`), and **one door to ground truth** (`score.py`). Nothing else imports either.
- **Every stage's output is saved** with `io.save`, so later stages and re-runs never recompute or re-call the model.
- **Parsers are plugins.** The core never imports them; adding a source means adding one file.
- **Add modules only when a function outgrows its file.** Cross-agent goal links (adoption, delegation, conflict) start in `align.py`; exposure modelling starts in `flow.py`.

## Usage

```python
from gleeb.parsers import parse_run
from gleeb import flow, io
from gleeb.goals import run_samples
from gleeb.ops import classify_ops
from gleeb.align import align
from gleeb.llm import LLM

trace = parse_run({"priya": "priya.jsonl", "tomas": "tomas.jsonl"})
llm = LLM(cache_dir="runs/cache", cost_cap_usd=5)
ex = run_samples(trace, "priya", "expressed", "windowed", llm, k=3)    # K samples for the noise floor
be = run_samples(trace, "priya", "behavioral", "windowed", llm, k=3)
gap = align(ex[0], be[0], llm)                                          # say-do gap
ops, _ = classify_ops(trace, llm)
edges = flow.flow_edges(ops, trace)
io.save(trace, "out/trace.json.gz"); io.save(ex + be, "out/goals.json"); io.save(edges, "out/flow.json")
```
