# One Night Ultimate Werewolf sim

N LLM agents (default 5) play one game of One Night Ultimate Werewolf, each in its own container, acting only through files. Built from `../multi-agent`.

Roles: werewolf, minion, mason, seer, robber, troublemaker, drunk, insomniac, villager, tanner. (No Doppelganger, no Hunter.)
Agents are told that they know only their *starting* role and that their current card may have changed.

## Run
```bash
python run.py                 # random deal (seed printed + saved)
python run.py --seed 7        # reproducible deal and speaking order
python run.py --dry-run       # random bots, no docker, no API: tests game logic
```
Needs Docker and `ANTHROPIC_API_KEY` (read from the repo-root `agnet/.env`, which overrides any exported variable; no per-sim `.env`). Every run starts fresh.

## Config (`config.json`)
- `model` (default `claude-sonnet-5-5`), optional `model_overrides: {"a": "claude-haiku-4-5-20251001"}`, `max_tokens`, `max_steps` (tool calls per turn)
- `players`: ids; `roles`: exactly `len(players) + 3` cards; `discussion_rounds`; `seed`

## Game flow (run.py is the game master; true state is never mounted)
1. **Deal**: seeded shuffle; `homes/agent_X/instruction.md` has rules + starting role.
2. **Night**, in order werewolf, minion, mason, seer, robber, troublemaker, drunk, insomniac. Choosers (seer, robber, troublemaker, drunk, lone werewolf) get a turn and write one line to `/home/night_action.md` (one retry if invalid). The game master applies swaps to the true state and writes what the agent learned to `/home/night_info.md`. Info-only roles (werewolf pair, minion, mason, insomniac) get theirs with no turn.
3. **Discussion**: `discussion_rounds` rounds, shuffled speaking order each round. Each agent writes `/home/statement.md`; the game master appends it, attributed, to `/table/discussion.md`. Agents see that file read-only, so nobody can forge or edit another's lines.
4. **Vote**: each agent writes `/home/vote.md` privately; votes are collected together. Most votes dies, ties all die, nobody dies if nobody has more than one vote.
5. **Resolve** by FINAL cards (win rules are in `instruction.md`).

Agents keep conversation history across turns (`/workspace/history.json`, invisible to them).

## Output (`games/<time>_seed<N>/`)
`game.json` (ground truth: start/final cards, every night action and result, statements, votes, winners), `result.txt`, `discussion.md`, `agent_X.md` (full transcripts), `homes/` snapshot.
