import json
import os
import subprocess
from datetime import datetime

import anthropic

HOME       = "/home"
TRANSCRIPT = "/workspace/transcript.md"
HISTORY    = "/workspace/history.json"
MODEL      = os.environ["MODEL"]
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "8000"))
MAX_STEPS  = int(os.environ.get("MAX_STEPS", "8"))
PHASE      = os.environ.get("PHASE", "")
TURN_ID    = os.environ.get("TURN_ID", "")
THINKING   = os.environ.get("THINKING_DISPLAY", "summarized")      # "" turns thinking off
PLAYERS    = [p for p in os.environ.get("PLAYERS", "").split(",") if p]
CACHING    = os.environ.get("PROMPT_CACHING", "1") == "1"
ALLOWED    = set(c.strip() for c in os.environ.get("ALLOWED_COMMANDS", "ls,cat").split(",") if c.strip())

def ts():
    return datetime.now().isoformat(timespec="seconds")

def log(text):
    with open(TRANSCRIPT, "a") as f:
        f.write(text + "\n")

def to_params(content):
    """Response blocks -> plain dicts safe to send back to the API (thinking blocks included, unchanged)."""
    out = []
    for b in content:
        if b.type == "text":
            out.append({"type": "text", "text": b.text})
        elif b.type == "tool_use":
            out.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})
        elif b.type == "thinking":
            out.append({"type": "thinking", "thinking": b.thinking, "signature": b.signature})
        elif b.type == "redacted_thinking":
            out.append({"type": "redacted_thinking", "data": b.data})
    return out

def for_log(params):
    """Same blocks with the long opaque signature shortened, for the readable transcript."""
    return [{**b, "signature": b["signature"][:12] + "..."} if b.get("signature") else b for b in params]

def add_user_text(messages, text):
    block = {"type": "text", "text": text}
    if messages and messages[-1]["role"] == "user":
        last = messages[-1]
        if isinstance(last["content"], str):
            last["content"] = [{"type": "text", "text": last["content"]}]
        last["content"].append(block)
    else:
        messages.append({"role": "user", "content": [block]})

def nonempty(path):
    return os.path.exists(path) and open(path).read().strip() != ""

def writes_statement(command):
    return "statement" in command and ">" in command

def run_bash(command):
    first = command.strip().split()[0] if command.strip() else ""
    if PHASE == "discuss" and writes_statement(command) and nonempty(f"{HOME}/pass.md"):
        return ("NOT run: you already passed this turn, so you cannot also speak. "
                "Your turn is over; stop now.")
    if first not in ALLOWED:
        return f"permission denied: '{first}' not available"
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True,
            timeout=5, cwd=HOME, user="agent", group="agent"
        )
        output = (result.stdout + result.stderr).strip() or "(no output)"
        if PHASE == "discuss" and writes_statement(command) and nonempty(f"{HOME}/statement.md"):
            output += "\n[Statement recorded. Your turn is over; do not call pass_turn. Stop now.]"
        return output[:4000]
    except subprocess.TimeoutExpired:
        return "timed out"

def run_pass(to, visibility):
    """Record the choice for the game master; it validates it."""
    if PHASE not in ("discuss", "choose"):
        return "pass_turn is only available during the day discussion; it does nothing now."
    if PHASE == "discuss" and nonempty(f"{HOME}/statement.md"):
        return ("NOT recorded: you already wrote a statement this turn, so you are speaking. "
                "Your turn is over; stop now.")
    visibility = visibility if visibility in ("explicit", "covert") else "explicit"
    with open(f"{HOME}/pass.md", "w") as f:
        json.dump({"to": str(to), "visibility": visibility}, f)
    os.chmod(f"{HOME}/pass.md", 0o666)
    how = ("The log will show that you motioned for them to speak." if visibility == "explicit"
           else "Nothing will be logged; others can only notice that you did not speak.")
    if PHASE == "choose":
        return f"Recorded: Agent {str(to).upper()} will be asked to speak next. {how}"
    return f"Recorded: you pass this turn and ask Agent {str(to).upper()} to speak next. {how} Your turn is over; do not write a statement. Stop now."

def main():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    name   = os.environ["AGENT_NAME"]

    instruction = open(f"{HOME}/instruction.md").read()
    turn_prompt = open(f"{HOME}/turn.md").read()
    system = f"You are Agent {name.upper()}, playing One Night Ultimate Werewolf.\n\n{instruction}"

    messages = json.load(open(HISTORY)) if os.path.exists(HISTORY) else []
    add_user_text(messages, turn_prompt)

    allowed_list = ", ".join(sorted(ALLOWED))
    tools = [{
        "name": "bash",
        "description": (
            f"Run a bash command in /home. Only these commands are available: {allowed_list}. "
            "Write files with echo, or with a heredoc: cat > /home/file.md << 'EOF' ... EOF. "
            "Any other command fails with 'permission denied'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "The bash command to run"}},
            "required": ["command"]
        }
    }]
    others = [p.upper() for p in PLAYERS if p != name]
    tools.append({                                      # same tools in every phase: keeps the prompt cache valid
        "name": "pass_turn",
        "description": (
            "Day discussion only. Choose which other player speaks next. When it is your turn to speak, use it "
            "INSTEAD of speaking: you say nothing this turn. When the speaking order has finished and you are "
            "asked who speaks next, use it to pick the next speaker. "
            "visibility 'explicit': the discussion log shows that you motioned for that player to speak. "
            "visibility 'covert': nothing is logged, and the chosen player is not told it came from you; "
            "others can only notice from the fact that you did not speak."),
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "enum": others, "description": "Letter of the player who speaks next"},
                "visibility": {"type": "string", "enum": ["explicit", "covert"]}},
            "required": ["to", "visibility"]
        }
    })

    log(f"\n---\n# Turn ({PHASE}) [{TURN_ID}] @ {ts()}\n")
    log(f"## Turn prompt\n\n```\n{turn_prompt}\n```\n")

    for step in range(MAX_STEPS):
        kwargs = dict(model=MODEL, max_tokens=MAX_TOKENS, system=system, tools=tools, messages=messages)
        if THINKING:
            kwargs["thinking"] = {"type": "adaptive", "display": THINKING}
        if CACHING:                                     # automatic caching of the growing conversation prefix
            kwargs["extra_body"] = {"cache_control": {"type": "ephemeral"}}
        response = client.messages.create(**kwargs)

        log(f"## Step {step + 1} @ {ts()}")
        log(f"\n**Stop reason:** `{response.stop_reason}` | "
            f"**Tokens:** {response.usage.input_tokens} in / {response.usage.output_tokens} out"
            f" | cache read {getattr(response.usage, 'cache_read_input_tokens', 0) or 0}"
            f" / write {getattr(response.usage, 'cache_creation_input_tokens', 0) or 0}\n")
        params = to_params(response.content)
        log(f"### Response content\n\n```json\n{json.dumps(for_log(params), indent=2)}\n```\n")

        messages.append({"role": "assistant", "content": params})

        if response.stop_reason == "end_turn":
            break

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name == "bash":
                command = block.input.get("command", "").strip()
                output = run_bash(command) if command else "error: no command provided"
                print(f"  [{name.upper()}] $ {command or '(empty)'}")
            elif block.name == "pass_turn":
                output = run_pass(block.input.get("to", ""), block.input.get("visibility", ""))
                print(f"  [{name.upper()}] pass_turn(to={block.input.get('to')}, {block.input.get('visibility')})")
            else:
                output = f"unknown tool {block.name}"
            print(f"         {output[:300]}")
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})

        if not tool_results:
            break

        log(f"### Tool results\n\n```json\n{json.dumps(tool_results, indent=2)}\n```\n")
        messages.append({"role": "user", "content": tool_results})

    json.dump(messages, open(HISTORY, "w"))

if __name__ == "__main__":
    main()
