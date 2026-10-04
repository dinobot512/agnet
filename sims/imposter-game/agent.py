import json
import os
import re
from datetime import datetime

import anthropic

HOME        = "/home"
CHAT        = "/chat/chat.md"
VOTES       = "/chat/votes.md"
TRANSCRIPT  = "/workspace/transcript.md"
MAX_STEPS   = 3
MODEL       = "claude-haiku-4-5-20251001"
SECRET_WORD = os.environ.get("SECRET_WORD", "").strip()
AGENT_NAMES = [n.strip() for n in os.environ.get("AGENT_NAMES", "").split(",") if n.strip()]

def ts():
    return datetime.now().isoformat(timespec="seconds")

def log(text):
    with open(TRANSCRIPT, "a") as f:
        f.write(text + "\n")

def dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, list):
        return [dump(o) for o in obj]
    if isinstance(obj, dict):
        return {k: dump(v) for k, v in obj.items()}
    return obj

def read(path):
    return open(path).read().strip() if os.path.exists(path) else ""

def append(path, line):
    with open(path, "a") as f:
        f.write(line + "\n")

def one_line(text):
    return " ".join(str(text).split())

def leaks_word(text):
    """True if text contains the agent's own word (case-insensitive, incl. plurals and hyphenated forms)."""
    if not SECRET_WORD:
        return False
    return re.search(rf"\b{re.escape(SECRET_WORD)}(s|es)?\b", text, re.IGNORECASE) is not None

LEAK_ERROR = ("error: REJECTED — your text contains your word. Never write the word in any form; "
              "refer to it as \"our word\". Rewrite without it and try again.")

MEMORY_TOOL = {
    "name": "update_memory",
    "description": "Append short private notes to your memory (suspicions, who said what). Keep it to a few lines.",
    "input_schema": {
        "type": "object",
        "properties": {"notes": {"type": "string"}},
        "required": ["notes"]
    }
}

PHASE_TOOLS = {
    "clue": {
        "name": "submit_clue",
        "description": "Submit your single clue word for this round.",
        "input_schema": {
            "type": "object",
            "properties": {"clue": {"type": "string", "description": "A single word. Never your secret word."}},
            "required": ["clue"]
        }
    },
    "question": {
        "name": "post_message",
        "description": "Post your one question/defense message to the chat.",
        "input_schema": {
            "type": "object",
            "properties": {"message": {"type": "string", "description": "One short message, e.g. pressing a specific agent on their clues."}},
            "required": ["message"]
        }
    },
    "vote": {
        "name": "vote",
        "description": "Cast your final vote for who you think the imposter is.",
        "input_schema": {
            "type": "object",
            "properties": {"agent": {"type": "string", "description": "The name (letter) of the agent you vote for."}},
            "required": ["agent"]
        }
    },
}

def do_action(phase, name, round_num, args):
    """Validate and apply the phase action. Returns (ok, message)."""
    if phase == "clue":
        clue = one_line(args.get("clue", "")).strip(".,!?\"'`")
        if not clue or len(clue.split()) != 1:
            return False, "error: clue must be exactly one word"
        if leaks_word(clue):
            return False, LEAK_ERROR
        append(CHAT, f"[round {round_num}] agent {name}: {clue}")
        return True, f"clue '{clue}' submitted"
    if phase == "question":
        msg = one_line(args.get("message", ""))
        if not msg:
            return False, "error: message is empty"
        if leaks_word(msg):
            return False, LEAK_ERROR
        append(CHAT, f"[question] agent {name}: {msg}")
        return True, "message posted"
    if phase == "vote":
        target = one_line(args.get("agent", "")).lower().strip(".,!?\"'`")
        if target == name.lower():
            return False, "error: you cannot vote for yourself"
        if AGENT_NAMES and target not in AGENT_NAMES:
            return False, f"error: unknown agent '{target}'. Choose one of: {', '.join(n for n in AGENT_NAMES if n != name)}"
        append(VOTES, f"agent {name} votes: {target}")
        return True, f"vote for {target} cast"
    return False, f"error: unknown phase {phase}"

def phase_block(phase, name, round_num):
    action = {
        "clue":     f"**Current phase: CLUE (round {round_num})** — call `submit_clue` with your one-word clue.",
        "question": ("**Current phase: QUESTION (one round)** — the clue rounds are over. Call `post_message` with ONE message: "
                     "press a specific agent whose clues seemed off, or defend yourself."),
        "vote":     ("**Current phase: VOTE (final)** — call `vote` with the letter of the agent you think is the imposter "
                     "(not yourself). The agent with the most votes is accused."),
    }.get(phase, f"Phase: {phase}.")
    return (
        f"{action}\n\n"
        f"Never write your word ({SECRET_WORD}) in any form — say \"our word\" instead.\n\n"
        f"The chat and your memory are shown above — no need to look anything up. "
        f"In a SINGLE response, call the action tool and (optionally) `update_memory` with a few short lines of notes. "
        f"Then you are done for this turn."
    )

def build_state(instruction, phase, name, round_num):
    """Fresh view of instruction + memory + chat, rebuilt on every API call."""
    memory = read(f"{HOME}/memory.md")
    chat   = read(CHAT)
    return (
        f"## instruction.md\n\n{instruction}\n\n"
        f"## Your memory\n\n{memory or '(empty)'}\n\n"
        f"## chat.md (current)\n\n{chat or '(empty — nobody has written yet)'}\n\n"
        f"{phase_block(phase, name, round_num)}"
    )

def main():
    client      = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    name        = os.environ["AGENT_NAME"]
    phase       = os.environ.get("PHASE", "clue")
    round_num   = os.environ.get("ROUND_NUM", "")
    instruction = read(f"{HOME}/instruction.md")

    system = (
        "You are an agent in a social deduction game. Your rules are in the instruction.md section of the "
        "first message; the chat and your memory are refreshed there on every call."
    )
    action_tool = PHASE_TOOLS[phase]
    tools       = [action_tool, MEMORY_TOOL]

    log(f"\n---\n# Turn @ {ts()} ({phase}{' r' + round_num if round_num else ''})\n")
    log(f"## System Prompt\n\n```\n{system}\n```\n")

    history = []  # assistant/tool_result exchanges after the state message
    acted   = False
    for step in range(MAX_STEPS):
        state    = build_state(instruction, phase, name, round_num)
        messages = [{"role": "user", "content": state}] + history
        if step == 0:
            log(f"## Initial User Message\n\n```\n{state}\n```\n")

        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=system,
            tools=tools,
            tool_choice={"type": "any"} if not acted else {"type": "auto"},
            messages=messages,
        )

        log(f"## Step {step + 1} @ {ts()}")
        log(f"\n**Stop reason:** `{response.stop_reason}` | "
            f"**Tokens:** {response.usage.input_tokens} in / {response.usage.output_tokens} out\n")
        log(f"### Response content\n\n```json\n{json.dumps(dump(response.content), indent=2)}\n```\n")

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name == action_tool["name"]:
                if acted:
                    output = "error: you already acted this turn"
                else:
                    ok, output = do_action(phase, name, round_num, block.input)
                    acted = acted or ok
            elif block.name == "update_memory":
                notes = str(block.input.get("notes", "")).strip()
                if notes:
                    append(f"{HOME}/memory.md", f"\n### {phase}{' r' + round_num if round_num else ''}\n{notes}")
                output = "memory updated"
            else:
                output = f"error: unknown tool {block.name}"
            print(f"  [{name.upper()}] {block.name}({json.dumps(block.input)}) -> {output}")
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})

        if tool_results:
            log(f"### Tool results\n\n```json\n{json.dumps(tool_results, indent=2)}\n```\n")

        # Done once the action landed; no need to round-trip for an acknowledgement.
        if acted or not tool_results:
            break
        history += [{"role": "assistant", "content": response.content},
                    {"role": "user", "content": tool_results}]

    if not acted:
        print(f"  [{name.upper()}] WARNING: no valid {phase} action after {MAX_STEPS} steps")

if __name__ == "__main__":
    main()
