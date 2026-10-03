import os
import anthropic

DEV_FILE = "/workspace/dev.md"
MEMORY_FILE = "/workspace/memory.md"

def read_file(path):
    with open(path) as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY not set")

    client = anthropic.Anthropic(api_key=api_key)

    dev = read_file(DEV_FILE)
    memory = read_file(MEMORY_FILE)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=(
            "You are an agent running in a container. "
            "You receive instructions from dev.md and maintain working notes in memory.md. "
            "Respond with only the new contents of memory.md — no explanation, no wrapper."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"## dev.md\n\n{dev}\n\n"
                f"## memory.md (current)\n\n{memory}"
            )
        }]
    )

    write_file(MEMORY_FILE, response.content[0].text)
    print("done")

if __name__ == "__main__":
    main()
