import json
import os
import subprocess
from datetime import datetime

import anthropic

HOME       = "/home"
TRANSCRIPT = "/workspace/transcript.md"
MAX_STEPS  = 8
ALLOWED    = set(c.strip() for c in os.environ.get("ALLOWED_COMMANDS", "ls,cat").split(",") if c.strip())

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

def run_bash(command):
    first = command.strip().split()[0] if command.strip() else ""
    if first not in ALLOWED:
        return f"permission denied: '{first}' not available"
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True,
            timeout=5, cwd=HOME, user="agent", group="agent"
        )
        output = (result.stdout + result.stderr).strip()
        return output[:2000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "timed out"

def main():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    name   = os.environ["AGENT_NAME"]

    instruction = open(f"{HOME}/instruction.md").read()
    memory_path = f"{HOME}/memory.md"
    memory      = open(memory_path).read().strip() if os.path.exists(memory_path) else ""

    system = (
        f"You are Agent {name.upper()}. You live in a computer system. "
        "Your home is /home. Explore freely — there may be more beyond it. "
        "STRICT RULE: never say your favorite word directly, only give clues. "
        "Write notes to /home/memory.md so you remember things next turn."
    )

    initial_user = (
        f"## instruction.md\n\n{instruction}\n\n"
        f"## memory.md\n\n{memory if memory else '(empty)'}\n\n"
        "Your turn. Explore and interact with your environment."
    )

    messages = [{"role": "user", "content": initial_user}]

    allowed_list = ", ".join(sorted(ALLOWED))
    tools = [{
        "name": "bash",
        "description": (
            f"Run a bash command. Only these commands are available: {allowed_list}. "
            f"Any other command will fail with 'permission denied' — do not waste calls on them."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": f"The bash command to run (must start with one of: {allowed_list})"}
            },
            "required": ["command"]
        }
    }]

    log(f"\n---\n# Turn @ {ts()}\n")
    log(f"## System Prompt\n\n```\n{system}\n```\n")
    log(f"## Initial User Message\n\n```\n{initial_user}\n```\n")

    for step in range(MAX_STEPS):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=system,
            tools=tools,
            messages=messages
        )

        log(f"## Step {step + 1} @ {ts()}")
        log(f"\n**Stop reason:** `{response.stop_reason}` | "
            f"**Tokens:** {response.usage.input_tokens} in / {response.usage.output_tokens} out\n")
        log(f"### Response content\n\n```json\n{json.dumps(dump(response.content), indent=2)}\n```\n")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use" and block.name == "bash":
                command = block.input.get("command", "").strip()
                output = run_bash(command) if command else "error: no command provided"
                print(f"  [{name.upper()}] $ {command or '(empty)'}")
                print(f"         {output[:300]}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output
                })

        if not tool_results:
            break

        log(f"### Tool results\n\n```json\n{json.dumps(dump(tool_results), indent=2)}\n```\n")
        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    main()
