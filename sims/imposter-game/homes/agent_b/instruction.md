# Instruction

You are Agent B. You are playing a social deduction game.

**Your word:** banana

You are a CREWMATE. The word listed above is the specific secret word that you and two other agents share. Your goal: identify the imposter and record their letter in `/home/findings.md`.

### Crewmate strategy

- **Your clue should be VAGUE.** Describe something that could apply to several words in the category — not a direct, defining feature of your word.
- A good clue is one another crewmate would recognize *because they also know the word*, but which would leave the imposter guessing between many possibilities.
- Bad clues: direct properties of the word (color, size, origin), near-synonyms, famous examples. These give the word away to the imposter.
- Good clues: loose associations, moods, settings, oblique references, metaphors.
- Watch for the agent whose clue is 'off' — either suspiciously generic (afraid to commit) or just a touch wrong (narrowed down to the wrong specific word).

## Setup

- 4 agents play (a, b, c, d). Three of you share a specific secret word; the fourth is the IMPOSTER who only knows the category of that word.
- You will not know who the imposter is unless your `role_block` above says you are the imposter.
- All agents share one chat log at `/chat/chat.md`. If the file does not exist yet, create it.

## How to play

- Each round, append ONE line with a single clue word to `/chat/chat.md`.
- Use the format: `[round N] agent b: <your_clue>`
- After writing your clue, read the file to see what others have said.
- Clues from the imposter will tend to be more generic or hedged — they only know the category.

## Clue rules

- Never write your word itself.
- Clues must be oblique. The imposter is listening. If your clue would let someone who only knows the category guess the exact word, it is too direct.
- Role-specific strategy is below in your role block — follow it closely.

## Memory and findings

- Keep running notes in `/home/memory.md` between turns.
- When you are confident who the imposter is, write their single-letter name (a / b / c / d) into `/home/findings.md`.