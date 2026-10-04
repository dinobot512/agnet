# Experiments

Setup material for the goal (Monitor A) and information-flow (Monitor B) monitor experiments.
The full build spec is [SPEC.md](SPEC.md). This folder holds **everything the agents need to see
at the start of each experiment**, plus a machine-readable definition the harness will load.
No harness code lives here yet.

## Layout
```
experiments/
  SPEC.md                         # full build spec (verbatim)
  shared/                         # prompt templates used by every experiment
    system_prompt.md              # {name} {role} {media} template
    system_prompt_no_goal_statement.md   # variant without "Before each step..." (run once per experiment)
    continue_prompt.md, notifications.md, content_rules.md
  e1_solo_private_brief/
  e2_shared_file_vs_dm/
  e3_three_agent_chain/
  e4_four_agents_conflict/
    experiment.yaml               # agents, file access, messaging, orchestration, injections,
                                  # conditions, expected flows/goal changes, outcome checks
    initial_files/                # exact starting files (briefs end with "## Updates from the committee"
                                  # so injections append below it; output files start empty)
    agents/<name>/
      system_prompt[_<cond>].md   # rendered system prompt (name/role/media filled in)
      system_prompt[_<cond>]_no_goal_statement.md
      task[_<cond>].md            # task prompt (first user message)
```

## Per-experiment contents
| Experiment | Agents | Initial files | Prompt variants by condition |
|---|---|---|---|
| E1 solo, private brief | Sam | brief.md, guide.md | none |
| E2 shared file vs DM | Priya, Tomas | brief_A.md, invite.md, decisions.md (FILE only) | `_file` / `_dm` system prompt + task |
| E3 three-agent chain | Priya, Tomas, Mei | brief_A.md, handoff.md, invite.md, signs.md | Tomas `task_instructed` / `task_uninstructed` |
| E4 four agents, conflict | Priya, Tomas, Mei, Dev | brief_{priya,tomas,mei,dev}.md, plan.md | none (stretch variants in yaml) |

## Notes for the harness builder
- **Injection content and markers live only in `experiment.yaml`.** They are never in `initial_files/`. Build the
  marker registry from the yaml (spec: no hand-written marker list). Injections append a new line
  under "## Updates from the committee".
- **Never mount or show `experiment.yaml` or `SPEC.md` to agents or monitors.** They hold the ground truth.
  Copy only the agent's permitted files from `initial_files/` into its working directory or container
  (see `files` / `mounts` in each yaml).
- **Media text.** E1's media text is verbatim from the spec. For E2-E4 the spec lists permissions, but not
  the media sentence, so the `{media}` lines in the rendered system prompts are **derived** in the same
  style. Review them before running.
- **Messaging tool names** (`send_dm`, `read_dms`, `post`, `read_board`) follow the spec. The MCP server
  will expose them under an MCP prefix, so check how they appear to the model and align the media text.
- **Settings to fill in.** `model` defaults to `claude-haiku-4-5` and `token_cap_per_run` is `null`. Set both
  before running replicates, and verify SDK option names against current Claude Agent SDK docs.
- **Run order.** Run 1 replicate per condition end to end before launching all 8.
