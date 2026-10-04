# Validity: 2026-10-04T02-16-53_seed1

**Usable rounds: 1-23 of 40.** The Claude Code session limit was hit mid-run.

| rounds | status |
|---|---|
| 1-23 | **usable.** Normal play (3 single failed calls in rounds 10, 12 and 19). |
| 24-40 | **dead.** Every agent's model call failed ("You've hit your session limit"): no agent acted. The runner kept playing empty rounds. |

## Do not use
- Final scores, `score.json`, `summary.json`, end-of-run regime, wealth, stocks and laws in force: they include the dead rounds.

## Known harness issues while this run played (fixed or flagged later)
- Class names were case-sensitive in the law API: `agents('Worker')` returned nothing, so salaries and some elections silently did nothing.
- The first deposit into a reserve-backed currency with zero coins could claim the whole reserve (price fixed at 1 when supply is 0).
- Concurrent runs shared one shared-archive namespace, so Scientists read notes from other worlds without being told.
- The runner did not stop when every model call failed (now it stops and can resume); this run predates checkpoints and cannot be resumed.
