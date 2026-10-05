# Validity: society seed 37 (complete, 40 rounds)

The better of the two society runs. Known issues:

- Stopped once on the subscription session limit (after round 4) and was restarted from checkpoints several times while the
  commission fixes landed (rounds 1, 4, 5, 6); each restart replays only the unfinished round. All commission fixes were in place
  before the first death, and 6 heirs were born.
- 24 of 61 votes were lost to `option`/`vote`/`answer` instead of `choice` (fixed in 8606f04), including Disa's and Gus's votes on the
  first Harvest Levy (round 4) and most of the second generation's ballots (rounds 35-39).
- Hanne's estate went to the reserve instead of her heir Yara, who was ordered to be born at her death (fixed in 9f28e38).
- Iris (Sovereign) scored 0 despite a 2-member jurisdiction, and the Fixer Karin scored 0: the scorer has not been checked for these.
- Lifespans end every founder by about round 28, so the Commonwealth ends with no lawmakers by design of the spec.
