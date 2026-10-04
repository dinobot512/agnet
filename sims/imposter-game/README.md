# Imposter game

A social deduction game for LLM agents. N agents each run in their own container. All but one share a secret word; the **imposter** only knows the word's category. Agents give one-word clues over several rounds, get one round to question each other, then vote on who the imposter is.

## Setup

1. **API key**: create a `.env` file in this directory:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

2. **Docker**: Docker must be installed.

## Run

```bash
python run.py                    # uses the words/imposter set in config.json
python run.py --fresh            # wipes memory and chat/votes first
python run.py --fresh --random   # random category + word from word_pool, random imposter
python run.py --random --seed 7  # reproducible randomization
```

| Flag | Effect |
|---|---|
| `--fresh` | Clear `memory.md` and the files in each world (`chat.md`, `votes.md`). |
| `--random-word` | Pick a random category and word from `word_pool`. Crewmates get the word; the imposter gets the category. |
| `--random-imposter` | Pick a random agent as the imposter. |
| `--random` | Shortcut for both of the above. |
| `--seed N` | Seed for the randomization. |

You will almost always want `--fresh`; otherwise the old chat log and memories carry into the new game.

Each run:
1. Reads `config.json` (and applies any randomization)
2. Regenerates `homes/agent_<name>/instruction.md` from the templates
3. Creates missing `worlds/<name>/` directories (chmod 777)
4. Builds the `multi-agent` image and starts one container per agent (`multi-agent-<name>`)
5. Plays the game (see below)
6. Tallies `votes.md` and prints who won
7. Writes per-agent transcripts to `transcripts/<timestamp>/agent_<name>.md`
8. Tears down the containers

A 6-agent, 2-round game takes about 1.5 minutes.

## Game flow

| Phase | Turn order | Agent action |
|---|---|---|
| CLUE × `rounds` | Sequential, so each agent sees the clues given before it | `submit_clue` → `[round N] agent x: <clue>` in `chat.md` |
| QUESTION × 1 | Sequential | `post_message` → `[question] agent x: <message>` in `chat.md` |
| VOTE × 1 | **Parallel**, so votes are secret and independent | `vote` → `agent x votes: <letter>` in `votes.md` |

The agent with the most votes is accused. Crewmates win only if the imposter gets strictly the most votes; ties favor the imposter.

## How an agent turn works (`agent.py`)

`run.py` runs `docker exec ... python agent.py` with `PHASE` (and `ROUND_NUM` for clue rounds) set. Agents have **no shell access**; they act only through tools.

- **Context is rebuilt on every API call:** `instruction.md`, the agent's `memory.md`, and the current `chat.md`, followed by the action for this phase.
- **Tools.** Each phase exposes exactly one action tool plus `update_memory`:

  | Tool | Phase | Validation |
  |---|---|---|
  | `submit_clue(clue)` | clue | Must be exactly one word |
  | `post_message(message)` | question | Must not be empty; collapsed to one line |
  | `vote(agent)` | vote | Must be a known agent name (from `AGENT_NAMES`) and not yourself |
  | `update_memory(notes)` | all | Appends notes to `/home/memory.md` under a phase heading |

- **Tool choice.** The first call forces a tool use (`tool_choice: any`). The turn ends as soon as the action succeeds, so a turn is normally **one API call**. If the action is invalid, the error is returned and the agent retries, up to `MAX_STEPS` (3) calls in total.
- **Model.** `claude-haiku-4-5-20251001`, `max_tokens=300`. Both are set at the top of `agent.py`.

The harness writes to the chat and votes files itself, so line formats are always correct and `tally_votes` in `run.py` can parse them.

## Config (`config.json`)

| Key | Meaning |
|---|---|
| `instruction_template` | Lines of the agent's `instruction.md`, rendered with `str.format()` |
| `imposter_notice` / `crewmate_notice` | Role-specific block inserted as `{role_block}` |
| `word_pool` | `[{category, words: [...]}]`, used by `--random-word` |
| `agents` | `[{name, word, is_imposter}]`. The imposter's `word` should be the category. |
| `worlds` | `[{name, agents}]`. The `chat` world is mounted at `/chat` and holds `chat.md` and `votes.md`. |
| `rounds` | Number of clue rounds |

An agent can also override `instruction_template` per agent.

### Template placeholders

| Placeholder | Value |
|---|---|
| `{name}` / `{name_upper}` | Agent name |
| `{word}` | The agent's word (the category, for the imposter) |
| `{role_block}` | Rendered `imposter_notice` or `crewmate_notice` (instruction_template only) |
| `{agent_count}` | Number of agents |
| `{crewmate_count}` / `{other_crewmate_count}` | Crewmates in total, and excluding the reader |
| `{agent_names}` / `{agent_names_slashed}` | `a, b, c` / `a / b / c` |

Literal `{` or `}` must be escaped as `{{` / `}}`.

## Filesystem layout inside each container

| Path | Notes |
|---|---|
| `/home` | Bind-mounted from `homes/agent_<name>/`: `instruction.md`, `memory.md` |
| `/chat` | Shared world: `chat.md`, `votes.md` |
| `/workspace` | `agent.py` and the transcript (mode 700, root) |

## Reading results

- Console output: every tool call, the vote tally, and the winner
- `worlds/chat/chat.md` / `votes.md`: the game log
- `homes/agent_<name>/memory.md`: each agent's private notes
- `transcripts/<timestamp>/agent_<name>.md`: full prompt, response, and tool-result log per turn
