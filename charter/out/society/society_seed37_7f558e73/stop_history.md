# Run stopped

- When: 2026-10-04 20:09:03
- Round 5 of 40 (simultaneous turns) was abandoned: 25 of 25 model calls failed (threshold 50% of max(25 planned decisions, calls made); DM-step reply calls count too).
- Nothing of round 5 is kept: events.jsonl and reasoning.jsonl were cut back to the checkpoint, which holds the state as of the end of round 4.
- Continue with `python -m charter resume /Users/zachmacaskill-smith/Documents/Github/AISwarms/agnet/charter/out/society/society_seed37_7f558e73` (or the same run command) once the cause is fixed.

## Sample errors

- Bram: RuntimeError: claude -p error (exit 1): {"subtype": "success", "result": "You've hit your session limit \u00b7 resets 10pm (America/Chicago)", "stop_reason": "stop_sequence", "api_error_status": 429}

