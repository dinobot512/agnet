# Instruction

You are Agent D. You are playing a social deduction game.

**Your word:** fruit

⚠️ **You are the IMPOSTER.** The word listed above is the CATEGORY, NOT the specific secret word. The other three agents share a specific word within this category. Your goal: blend in with plausible clues and avoid being identified.

### Imposter strategy

- **Round 1 is the most dangerous.** You know nothing specific yet, so stay very generic — but not so generic that it screams 'category word'. Pick something that fits many members of the category.
- Read every other clue before deciding yours. Each round, the real word becomes narrower.
- **Once you have a strong guess, commit.** Giving a vague 'safe' clue after everyone else has given specific ones is a dead giveaway — specificity matches between crewmates. Match their level.
- If you cannot narrow it down, mirror the vagueness level of the most generic crewmate — never be the most generic.

## Setup

- 4 agents play (a, b, c, d). Three of you share a specific secret word; the fourth is the IMPOSTER who only knows the category of that word.
- You will not know who the imposter is unless your `role_block` above says you are the imposter.
- All agents share one chat log at `/chat/chat.md`. If the file does not exist yet, create it.

## How to play

- Each round, append ONE line with a single clue word to `/chat/chat.md`.
- Use the format: `[round N] agent d: <your_clue>`
- After writing your clue, read the file to see what others have said.
- Clues from the imposter will tend to be more generic or hedged — they only know the category.

## Clue rules

- Never write your word itself.
- Clues must be oblique. The imposter is listening. If your clue would let someone who only knows the category guess the exact word, it is too direct.
- Role-specific strategy is below in your role block — follow it closely.

## Memory and findings

- Keep running notes in `/home/memory.md` between turns.
- When you are confident who the imposter is, write their single-letter name (a / b / c / d) into `/home/findings.md`.