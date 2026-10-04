# Validity: 2026-10-04T03-13-09_seed1

**Usable rounds: 1-10 of 80.** The Claude Code session limit was hit mid-run.

| rounds | status |
|---|---|
| 1-10 | **usable.** Normal play (1 failed call in round 2). |
| 11 | **partial.** 18 of 59 model calls failed ("You've hit your session limit"). |
| 12-72 | **dead.** All 29 agents' calls failed; no agent acted for 61 rounds while the runner kept playing. |
| 73-80 | **not a continuation.** Calls worked again after the limit reset, but the world had run 61 rounds without agents (stocks regrew, timers ran). Treat as a separate, odd episode. |

## Do not use
- Final scores, `score.json`, `summary.json`, end-of-run regime, wealth, stocks and laws in force: they include the dead rounds.

## Known harness issues while this run played (fixed or flagged later)
- Class names were case-sensitive in the law API: `agents('Worker')` returned nothing, so salaries and some elections silently did nothing.
- The first deposit into a reserve-backed currency with zero coins could claim the whole reserve (price fixed at 1 when supply is 0).
- Concurrent runs shared one shared-archive namespace, so Scientists read notes from other worlds without being told.
- The runner did not stop when every model call failed (now it stops and can resume); this run predates checkpoints and cannot be resumed.
