# Economy sim

10 agents, scarce credits, public persuasion and private contracts. **The rules are in [RULES.md](RULES.md).** This file covers how to run the sim.

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Run

```bash
.venv/bin/python run.py --seed 1               # full game with Claude (config.json: model, turns, ...)
.venv/bin/python run.py --seed 1 --turns 3     # short game
.venv/bin/python run.py --fake --seed 1        # random players, no API calls
.venv/bin/python -m pytest -q test_engine.py   # engine tests
.venv/bin/python visualize.py                   # network graphs for the most recent run (or pass runs/<timestamp>)
```

| Flag | Effect |
|---|---|
| `--seed N` | Fixes which agents are earners (unless `earners` is set in config) and the tie-breaks |
| `--turns N` | Overrides `turns` |
| `--model ID` | Overrides `model` |
| `--fake` | Uses `fake_agent.py` instead of the API |

A full 20-turn game is about 1,000 model calls (10 agents × 5 phases × 20 turns, plus retries).

## Files

| File | What it does |
|---|---|
| `engine.py` | Game state and every rule. Pure Python, deterministic, no API. Validation (`validate_*`), phase application (`apply_phase`), `settle()`, and `view_for(agent, phase)`, which renders what an agent can see. |
| `agent.py` | `ModelPlayer`: one model call per agent per phase. The system prompt is the agent's rules (from config); the user message is `view_for(...)`. Only that phase's tools are offered, plus `update_notes` and `pass_turn`. Invalid moves return an error, and the agent retries up to `max_steps` calls in total. |
| `fake_agent.py` | `FakePlayer`: random valid moves, for testing. |
| `run.py` | Turn loop. All alive agents act **in parallel** within each phase; the engine applies their actions together, then settles. |
| `config.json` | Numbers (agents, earners, start balance, upkeep, income schedule, limits) and the rule text agents see (`rules_common`, `rules_earner`, `rules_non_earner`). |
| `visualize.py` | Reads a finished run's `events.jsonl` and draws one network graph per turn into `runs/<timestamp>/graphs/` (`turn_NN.png`, plus `overview.png` with all turns). Bubble area = balance after settlement (earners gold, non-earners blue, eliminated grey with † turn). Arrows = contract payments made that turn (width = credits). A central INCOME node has arrows to each earner (width = that turn's income). |
| `test_engine.py` | Tests for payments, scoring, insolvency and cascades, tie-breaks, expiry, termination, hidden information, and credit conservation. |

### Config notes
- `earners: null` picks `earner_count` agents at random (seeded). Set a list, e.g. `["c", "h"]`, to fix them.
- `max_new_contracts_per_turn` (default 2) caps new contracts per agent per turn; signing and being signed both count.
- `income_schedule` is a list of `{from_turn, income}` steps, per earner.
- Rule text supports `{name_upper}`, `{turns}`, `{upkeep}`, `{start_balance}`, `{earner_count}`, `{message_limit}`, `{max_duration}`, `{max_time_limit}`, `{max_signing_limit}`, and `{role_block}`.

## Output: `runs/<timestamp>/`

| File | Contents |
|---|---|
| `summary.md` | Earner scores and winner, survivors, eliminations, every contract, the full board **with authors** |
| `events.jsonl` | Written **as events happen**, so a crashed run keeps its log. Each event has `turn`, `phase` and `event`. Kinds: `setup` (earners, balances), `action` (each agent's final move per phase, including passes), `board`, `proposal`, `counteroffer`, `signed`, `accept_failed`, `proposal_closed`, `terminate_request`, `terminated`, `income`, `payment`, `completed`, `upkeep`, `eliminated` (with the balance destroyed), `voided`, `settled`, `notice` (every notification an agent received), `note` (private notes), `invalid_action` (a rejected tool call and its error), `truncated` (an over-long post or counteroffer: original and kept text), `api_error` |
| `state_turn_NN.json` | Full state after each settlement, including every agent's notes |
| `transcripts/agent_<x>.jsonl` | The agent's rules (a `system` line, once), then every prompt, response and tool result as Messages-API lines (`{"role", "content", "t", "turn", "phase"}`). Responses also carry `stop_reason` and token `usage`. `gleeb`'s `anthropic_jsonl` parser can read these. |
| `console.log` | The console output |
| `results.json` | Final results, plus total calls and tokens for real runs |
| `config.json` | The config and seed used |
