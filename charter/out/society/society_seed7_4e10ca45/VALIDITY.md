# Validity: society seed 7 (complete, 40 rounds)

Usable with care. Known issues, all fixed in code after the fact:

- Rounds 1-16 ran on the original prompts (no children/heir lines, no harvest-argument hints). The run stopped on the subscription
  session limit after round 16 and resumed at round 17 with the new prompts, so agents learned that heirs carry their goals on
  only from round 17.
- Commissions failed on argument shapes until round 19, goals written as words until round 21, and Maker/self-order handling until
  round 24 (restarts after rounds 18, 21 and 24). No child was ever born; treat the lineage results as an interface artefact.
- 11 votes were lost to `option` instead of `choice` (fixed in 8606f04). Eight of them were on B5 (L7, tribute pledges) in round 13,
  which probably changed that ballot's result and so the T1 raid.
- messages.md was rebuilt after the run with the fix that includes outlet editions.
- Lifespans (full_scale_rounds 60 with starting ages) end every founder by round 28, so the late game is near-empty by design.
