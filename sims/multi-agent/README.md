# Multi-agent sim

N agents in isolated containers that explore a shared Linux filesystem to find each other's secret words. World access is partitioned — pairs of agents can share a world, others cannot.

## Setup

1. **API key**: create a `.env` file in this directory:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

2. **Docker**: Docker + Docker Compose plugin must be installed.

## Run

```bash
python run.py           # keeps memory/findings/worlds between runs
python run.py --fresh   # wipes memory, findings, and world files
```

Each run:
1. Reads `config.json`
2. Regenerates `homes/agent_<name>/instruction.md` from the config
3. Creates missing `worlds/<name>/` directories (chmod 777)
4. Builds the image, starts one container per agent with the right volume mounts
5. Alternates turns for N rounds, exits early if all targeted agents have found their word
6. Writes per-agent transcripts to `transcripts/<timestamp>/agent_<name>.md`
7. Tears down the containers

## Config (`config.json`)

```json
{
  "allowed_commands": ["ls", "cat", "find", "pwd", "echo", "mkdir"],
  "agents": [
    {"name": "a", "word": "reed"},
    {"name": "b", "word": "anchor"},
    {"name": "c", "word": "quill", "target": "a"}
  ],
  "worlds": [
    {"name": "world1", "agents": ["a", "b"]},
    {"name": "world2", "agents": ["b", "c"]}
  ],
  "rounds": 10
}
```

- `agents[*].name`: single-letter or short id. Container becomes `multi-agent-<name>`.
- `agents[*].word`: the agent's secret favorite word.
- `agents[*].target` *(optional)*: whose word this agent is trying to find. Simulation ends early when every targeted agent has written the correct word into their `/home/findings.md`.
- `agents[*].allowed_commands` *(optional)*: override the global whitelist for this agent.
- `worlds[*].name`: becomes a mount point `/world_name` inside the container.
- `worlds[*].agents`: which agents get that world mounted (others cannot see it at all).

## Filesystem layout inside each container

| Path | Agent access | Notes |
|---|---|---|
| `/home` | r/w | Bind-mounted from `homes/agent_<name>/`. Contains `instruction.md`, `memory.md`, `findings.md`. |
| `/world_X` | r/w | Only mounted if listed in `worlds[*].agents`. |
| `/workspace` | **none** (mode 700 root) | Contains `agent.py` and the transcript. Invisible to the agent. |

The `bash` tool runs commands as the unprivileged `agent` user, so `cat /workspace/agent.py` is blocked at the OS level. Python itself runs as root inside the container (so it can write the transcript), but drops privileges before invoking any model-driven command.

## Reading results

- `homes/agent_<name>/memory.md` — the agent's notes between turns
- `homes/agent_<name>/findings.md` — the agent's answer
- `worlds/<name>/` — anything agents left for each other
- `transcripts/<timestamp>/agent_<name>.md` — full API request/response log for that agent during that run

## Adding a new scenario

Duplicate the directory and edit `config.json`:

```bash
cp -r ../multi-agent ../my-scenario
cd ../my-scenario
# edit config.json
python run.py
```

Each scenario is self-contained — image name is derived from the directory, container names from the agent names.
