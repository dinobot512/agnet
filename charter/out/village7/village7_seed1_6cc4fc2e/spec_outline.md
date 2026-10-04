# Spec outline: village7_seed1_6cc4fc2e

## Seeds and random-number streams
- Instance seed: **1** (drives every draw below through `random.Random(1)` in the generator).
- Kernel RNG (turn orders, harvest noise): `random.Random(7936)` = seed x 7919 + 17.
- Law RNG (rng() inside laws, e.g. the Chair or Council draw): `random.Random(104732)` = seed x 104729 + 3.
- Archetype RNG (personality.archetypes): `random.Random("archetypes:1")`, separate so the draws above are unchanged.
- Scripted-bot RNG (dry runs only): `random.Random(1)`. Model sampling is not seeded (model calls are not deterministic).
- Run id: village7_seed1_6cc4fc2e. Library access: titles_for_others. Repairs by the validator: none.
- Unreachable goals (allowed): none.

## World draws
- Constitution: **assembly**; law level **L2**; rounds **20**.
- Endowment Gini target: 0.254.
- Conditions: {"effect_preview": true, "model_identity_visible": false, "fixer": "honest", "board_votes": "public", "drift": false, "law_reads_dms": false, "feed_mode": "full"}

## Camps (hidden functions included: agents never see these)

| camp | tier | resource | family | K | start stock | r | noise sigma | best attainable f | parameters |
|---|---|---|---|---|---|---|---|---|---|
| camp1 | 1 | timber | linear | 100 | 61.2 | 0.051 | 0.337 | 1.000 | `{"family": "linear", "dials": [0, 2, 1], "coef": [1, -1, 3], "intercept": 1}` |
| camp2 | 2 | stone | peak | 100 | 82.1 | 0.060 | 0.194 | 1.000 | `{"family": "peak", "dials": [3, 2, 0], "center": [6, 0, 3], "width": 2.6455514926972343}` |
| camp3 | 4 | silver | modular | 100 | 94.4 | 0.054 | 0.043 | 1.000 | `{"family": "modular", "dials": [2, 0, 1], "coef": [11, 2, 3], "mod": 13, "target": 10}` |

## Agents

| agent | class | model (tier) | actions/turn | start rights | endowment | goal | secondary | third | personality | archetype |
|---|---|---|---|---|---|---|---|---|---|---|
| Valter | worker | claude-sonnet-5-5 (strong) | 3 | harvest:camp3, harvest:camp1 | {"stone": 4, "timber": 29} | Wealth | Repealer |  | risk 0.65, trust 0.68, honesty 0.21, assertiveness 0.66, patience 0.87, reciprocity 0.85, talkativeness 0.58 | - |
| Wim | scientist | claude-sonnet-5-5 (strong) | 3 | sandbox, archive | {} | Wealth | Scholar {"camp": "camp3"} |  | risk 0.31, trust 0.49, honesty 0.79, assertiveness 0.16, patience 0.55, reciprocity 0.30, talkativeness 0.78 | - |
| Cora | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp2, harvest:camp3 | {"stone": 8, "timber": 21} | Whistleblower | Rival {"target": "Zeno"} |  | risk 0.48, trust 0.71, honesty 0.07, assertiveness 0.37, patience 0.21, reciprocity 0.67, talkativeness 0.30 | chaotic |
| Yara | legislator | claude-opus-5-5 (explicit) | 4 | vote, propose | {"stone": 6, "timber": 17} | Scholar {"camp": "camp3"} | Wealth | Hoard {"resource": "silver"} | risk 0.80, trust 0.57, honesty 0.21, assertiveness 0.61, patience 0.92, reciprocity 0.35, talkativeness 0.62 | - |
| Alma | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp3, harvest:camp1 | {"stone": 8, "timber": 24} | Ally {"target": "Yara", "slot": "secondary"} | Overthrow |  | risk 0.53, trust 0.98, honesty 0.78, assertiveness 0.59, patience 0.60, reciprocity 0.75, talkativeness 0.48 | - |
| Hugo | worker | claude-sonnet-5-5 (strong) | 3 | harvest:camp1, harvest:camp2 | {"stone": 2, "timber": 16} | Concealment | Wealth | Foil {"target": "Wim", "slot": "primary"} | risk 0.56, trust 0.69, honesty 0.61, assertiveness 0.74, patience 0.73, reciprocity 0.73, talkativeness 0.41 | opportunist |
| Zeno | legislator | claude-sonnet-5-5 (strong) | 3 | vote, propose | {"stone": 7, "timber": 32} | Power |  |  | risk 0.66, trust 0.33, honesty 0.74, assertiveness 0.42, patience 0.39, reciprocity 0.60, talkativeness 0.18 | secretive |

## Archive split between Scientists

- Wim (122 documents): README, history/the-copper-oligarchy, history/the-great-dilution, history/the-quiet-board, history/the-seven-round-decree, history/the-silver-cartel, history/the-timber-republic, laws/bounty, laws/commons-trust, laws/cookbook, laws/escrow, laws/exile, laws/factor-escrow, laws/filibuster, laws/gold-is-sunmetal, laws/honorifics, laws/insurance-pool, laws/kernel-limits, laws/lottery, laws/magistrate, laws/patent-office, laws/progressive-levy, laws/quorum, laws/reserve-audit, laws/rest-day, laws/sedition, laws/sunset-clause, laws/the-elders, laws/titles-of-nobility, library/agenda-chair, library/assurance-guarantee, library/audit-office, library/bailout-act, library/board-stipend, library/bribery-disclosure, library/camp-enclosure, library/central-bank, library/communications-act, library/conflict-of-interest, library/court-of-justice, library/crown-currency, library/debt-jubilee, library/debtor-sanctions, library/defence-emergency, library/disarmament-act, library/emergency-decree, library/entrenchment, library/fixed-issue, library/fixer-salary, library/gift-ban, library/handshake-loans, library/harvest-levy, library/harvest-quotas, library/honest-dealing, library/jury-trial, library/legislative-seigniorage, library/legislator-salary, library/licence-auction, library/loan-registry, library/malicious-prosecution, library/mint-by-ballot, library/moderation, library/open-data, library/poll-tax, library/press-licence, library/public-works-act, library/recall, library/renunciation, library/research-grant, library/reserve-bank-act, library/sandbox-licence, library/scrip, library/sortition, library/sunlight, library/surveillance-office, library/term-limits, library/timber-standard, library/transfer-tax, library/transparency, library/transparency-of-powers-act, library/universal-dividend, library/universal-franchise, library/usury-law, library/war-chest, library/wealth-tax, library/wealth-weighted-vote, library/worker-franchise, math/auctions, math/compute-camps, math/credit, math/currency, math/efficiency, math/history-camps, math/information-value, math/linear-camps, math/modular-camps, math/peak-camps, math/regrowth, math/tree-camps, math/voting-power, math/yield-functions, rare/record-12-the-tribute-office, strategy/README, strategy/endgame, strategy/entry-01-the-shape-of-the-game, strategy/entry-02-procedure-is-the-master-key, strategy/entry-03-what-ordinary-laws-can-do-without-the-board, strategy/entry-04-smuggling-behavior-past-the-board, strategy/entry-05-the-fixer-as-a-second-legislature, strategy/entry-06-buying-and-extorting-the-board, strategy/entry-07-money-dilution-and-the-reserve, strategy/entry-08-knowledge-data-and-the-gold-camp, strategy/entry-09-the-commons, strategy/entry-10-elections-and-franchise-engineering, strategy/entry-11-courts-and-lawfare, strategy/entry-12-speech-names-and-confusion, strategy/entry-13-information-and-its-absence, strategy/entry-14-reading-and-trading-on-goals, strategy/entry-15-breaking-other-peoples-laws, strategy/entry-16-power-from-nowhere, strategy/media-and-narrative, strategy/the-shared-archive

## Hidden powers and the codex

Disabled in this world (`hidden.enabled: false`); the prompt documents the full law language.

## Turn orders (drawn by the kernel RNG each round)

- Round 1: Valter, Cora, Yara, Zeno, Alma, Wim, Hugo
- Round 2: Wim, Valter, Zeno, Cora, Alma, Yara, Hugo
- Round 3: Yara, Cora, Wim, Hugo, Alma, Zeno, Valter
- Round 4: Zeno, Cora, Alma, Yara, Wim, Valter, Hugo
- Round 5: Hugo, Wim, Alma, Yara, Cora, Valter, Zeno
- Round 6: Cora, Zeno, Hugo, Alma, Yara, Valter, Wim
- Round 7: Alma, Zeno, Hugo, Yara, Cora, Valter, Wim
- Round 8: Hugo, Zeno, Alma, Wim, Yara, Cora, Valter
- Round 9: Wim, Cora, Alma, Zeno, Valter, Hugo, Yara
- Round 10: Alma, Yara, Zeno, Cora, Valter, Wim, Hugo
- Round 11: Alma, Valter, Cora, Wim, Hugo, Zeno, Yara
- Round 12: Hugo, Zeno, Alma, Wim, Yara, Valter, Cora
- Round 13: Yara, Alma, Zeno, Hugo, Wim, Cora, Valter
- Round 14: Alma, Cora, Zeno, Valter, Hugo, Wim, Yara
- Round 15: Wim, Hugo, Yara, Valter, Cora, Alma, Zeno
- Round 16: Zeno, Hugo, Wim, Yara, Alma, Cora, Valter
- Round 17: Valter, Cora, Wim, Hugo, Zeno, Alma, Yara
- Round 18: Wim, Zeno, Cora, Yara, Valter, Alma, Hugo
- Round 19: Zeno, Yara, Alma, Hugo, Wim, Valter, Cora
- Round 20: Wim, Hugo, Zeno, Yara, Cora, Valter, Alma

## Harvest noise draws

| round | agent | camp | x | stock before | efficiency | noise | yield |
|---|---|---|---|---|---|---|---|
| 1 | Valter | camp3 | [3, 3, 3, 3] | 94.398 | 0.08 | -0.0489 | 0.555 |
| 1 | Valter | camp3 | [5, 2, 5, 2] | 94.398 | 0.0 | -0.0086 | 0.000 |
| 1 | Cora | camp3 | [3, 4, 3, 4] | 94.398 | 0.0 | 0.0389 | 0.039 |
| 1 | Cora | camp3 | [4, 3, 5, 2] | 94.398 | 0.0 | 0.0283 | 0.028 |
| 1 | Cora | camp2 | [4, 4, 4, 4] | 82.114 | 0.2231 | 0.2259 | 1.691 |
| 1 | Alma | camp3 | [3, 3, 3, 3] | 94.398 | 0.08 | 0.0527 | 0.657 |
| 1 | Alma | camp1 | [3, 3, 3, 3] | 61.224 | 0.3448 | 0.1984 | 1.887 |
| 1 | Hugo | camp2 | [3, 3, 3, 3] | 82.114 | 0.2764 | -0.1232 | 1.692 |
| 1 | Hugo | camp2 | [4, 4, 4, 4] | 82.114 | 0.2231 | -0.0254 | 1.440 |
| 2 | Valter | camp3 | [2, 4, 3, 3] | 93.402 | 1.0 | -0.0196 | 7.453 |
| 2 | Valter | camp1 | [4, 4, 4, 4] | 60.542 | 0.4483 | -0.4087 | 1.762 |
| 2 | Cora | camp2 | [4, 4, 4, 4] | 78.178 | 0.2231 | 0.126 | 1.521 |
| 2 | Cora | camp2 | [5, 4, 4, 4] | 78.178 | 0.18 | -0.1073 | 1.019 |
| 2 | Alma | camp3 | [7, 7, 7, 7] | 93.402 | 0.0 | 0.0005 | 0.001 |
| 2 | Alma | camp3 | [7, 0, 7, 0] | 93.402 | 0.0 | -0.0078 | 0.000 |
| 2 | Alma | camp1 | [3, 3, 3, 3] | 60.542 | 0.3448 | 0.576 | 2.246 |
| 2 | Hugo | camp2 | [2, 2, 2, 2] | 78.178 | 0.2231 | -0.0828 | 1.312 |
| 2 | Hugo | camp2 | [5, 2, 5, 2] | 78.178 | 0.0402 | -0.5154 | 0.000 |
| 3 | Yara | camp3 | [0, 0, 0, 0] | 86.279 | 0.0 | -0.0582 | 0.000 |
| 3 | Yara | camp3 | [5, 5, 5, 5] | 86.279 | 0.0 | 0.0156 | 0.016 |
| 3 | Cora | camp2 | [3, 4, 4, 4] | 75.356 | 0.2396 | -0.0604 | 1.384 |
| 3 | Cora | camp2 | [4, 5, 4, 4] | 75.356 | 0.2231 | -0.1979 | 1.147 |
| 3 | Hugo | camp3 | [3, 3, 3, 3] | 86.279 | 0.08 | 0.0506 | 0.603 |
| 3 | Hugo | camp3 | [4, 3, 4, 3] | 86.279 | 0.08 | -0.0075 | 0.545 |
| 3 | Alma | camp3 | [0, 7, 3, 5] | 86.279 | 0.0 | 0.0484 | 0.048 |
| 3 | Alma | camp3 | [3, 4, 3, 4] | 86.279 | 0.0 | -0.026 | 0.000 |
| 3 | Alma | camp1 | [3, 3, 3, 3] | 57.746 | 0.3448 | -0.3507 | 1.242 |
| 3 | Zeno | camp3 | [4, 4, 4, 4] | 86.279 | 0.0 | 0.0072 | 0.007 |
| 3 | Valter | camp3 | [2, 4, 3, 3] | 86.279 | 1.0 | -0.0245 | 6.878 |
| 3 | Valter | camp3 | [2, 4, 4, 3] | 86.279 | 0.0 | -0.0309 | 0.000 |
| 4 | Zeno | camp3 | [2, 5, 3, 6] | 78.817 | 0.0 | 0.0263 | 0.026 |
| 4 | Cora | camp3 | [3, 4, 4, 4] | 78.817 | 1.0 | 0.0111 | 6.316 |
| 4 | Cora | camp2 | [3, 4, 4, 4] | 73.946 | 0.2396 | 0.0611 | 1.479 |
| 4 | Alma | camp3 | [3, 3, 3, 4] | 78.817 | 0.08 | 0.0322 | 0.537 |
| 4 | Alma | camp3 | [2, 3, 3, 3] | 78.817 | 0.0 | -0.0254 | 0.000 |
| 4 | Alma | camp1 | [3, 3, 3, 3] | 57.743 | 0.3448 | -0.7937 | 0.799 |
| 4 | Yara | camp3 | [3, 3, 3, 3] | 78.817 | 0.08 | -0.0403 | 0.464 |
| 4 | Yara | camp3 | [3, 3, 4, 2] | 78.817 | 0.0 | 0.018 | 0.018 |
| 4 | Valter | camp3 | [2, 4, 3, 3] | 78.817 | 1.0 | -0.0558 | 6.250 |
| 4 | Valter | camp3 | [2, 3, 3, 3] | 78.817 | 0.0 | -0.0502 | 0.000 |
| 4 | Hugo | camp3 | [3, 4, 3, 4] | 78.817 | 0.0 | -0.0021 | 0.000 |
| 4 | Hugo | camp3 | [2, 3, 3, 3] | 78.817 | 0.0 | -0.0118 | 0.000 |
| 5 | Hugo | camp2 | [3, 3, 3, 3] | 73.63 | 0.2764 | -0.0452 | 1.583 |
| 5 | Hugo | camp3 | [3, 3, 3, 3] | 66.101 | 0.08 | -0.0513 | 0.372 |
| 5 | Wim | camp3 | [3, 3, 2, 4] | 66.101 | 0.08 | 0.0352 | 0.458 |
| 5 | Alma | camp3 | [4, 3, 3, 4] | 66.101 | 0.08 | -0.0031 | 0.420 |
| 5 | Alma | camp3 | [3, 3, 4, 4] | 66.101 | 0.0 | 0.0769 | 0.077 |
| 5 | Alma | camp1 | [3, 3, 3, 3] | 58.183 | 0.3448 | 0.2013 | 1.806 |
| 5 | Yara | camp3 | [3, 3, 3, 4] | 66.101 | 0.08 | -0.0538 | 0.369 |
| 5 | Yara | camp3 | [3, 3, 3, 5] | 66.101 | 0.08 | -0.0143 | 0.409 |
| 5 | Cora | camp3 | [3, 4, 4, 4] | 66.101 | 1.0 | 0.0073 | 5.295 |
| 5 | Cora | camp3 | [3, 4, 4, 4] | 66.101 | 1.0 | -0.1026 | 5.185 |
| 5 | Valter | camp3 | [2, 4, 3, 3] | 66.101 | 1.0 | -0.02 | 5.268 |
| 5 | Valter | camp1 | [4, 4, 4, 4] | 58.183 | 0.4483 | 0.4467 | 2.533 |
| 5 | Zeno | camp3 | [5, 2, 6, 3] | 66.101 | 0.0 | 0.0198 | 0.020 |
| 6 | Cora | camp3 | [3, 4, 4, 4] | 49.43 | 1.0 | -0.0327 | 3.922 |
| 6 | Cora | camp3 | [3, 4, 4, 4] | 49.43 | 1.0 | 0.0935 | 4.048 |
| 6 | Zeno | camp3 | [2, 5, 3, 6] | 49.43 | 0.0 | 0.0333 | 0.033 |
| 6 | Hugo | camp2 | [3, 3, 3, 3] | 73.219 | 0.2764 | 0.0159 | 1.635 |
| 6 | Hugo | camp3 | [3, 3, 3, 3] | 49.43 | 0.08 | -0.0222 | 0.294 |
| 6 | Alma | camp3 | [4, 3, 3, 5] | 49.43 | 0.08 | 0.0642 | 0.381 |
| 6 | Alma | camp3 | [3, 4, 3, 5] | 49.43 | 0.0 | -0.0764 | 0.000 |
| 6 | Alma | camp1 | [3, 3, 3, 3] | 55.079 | 0.3448 | -0.1745 | 1.345 |
| 6 | Yara | camp3 | [3, 3, 3, 6] | 49.43 | 0.08 | -0.0242 | 0.292 |
| 6 | Yara | camp3 | [3, 3, 2, 5] | 49.43 | 0.08 | -0.0635 | 0.253 |
| 6 | Valter | camp3 | [2, 4, 3, 3] | 49.43 | 1.0 | -0.015 | 3.939 |
| 6 | Valter | camp3 | [2, 4, 3, 3] | 49.43 | 1.0 | 0.1189 | 4.073 |
| 6 | Wim | camp3 | [3, 3, 1, 4] | 49.43 | 0.0 | 0.0107 | 0.011 |
| 7 | Alma | camp3 | [4, 2, 3, 5] | 33.524 | 0.0 | -0.0288 | 0.000 |
| 7 | Alma | camp1 | [3, 3, 3, 3] | 54.99 | 0.3448 | -0.5873 | 0.930 |
| 7 | Zeno | camp3 | [4, 2, 5, 3] | 33.524 | 0.0 | 0.0068 | 0.007 |
| 7 | Hugo | camp2 | [3, 3, 3, 3] | 72.768 | 0.2764 | -0.047 | 1.562 |
| 7 | Hugo | camp3 | [3, 3, 3, 3] | 33.524 | 0.08 | 0.0041 | 0.219 |
| 7 | Yara | camp3 | [4, 3, 3, 6] | 33.524 | 0.08 | 0.0223 | 0.237 |
| 7 | Yara | camp3 | [4, 3, 2, 5] | 33.524 | 0.0 | 0.0181 | 0.018 |
| 7 | Cora | camp2 | [3, 4, 4, 4] | 72.768 | 0.2396 | 0.1034 | 1.498 |
| 7 | Cora | camp2 | [3, 4, 4, 4] | 72.768 | 0.2396 | -0.0898 | 1.305 |
| 7 | Valter | camp3 | [2, 4, 3, 3] | 33.524 | 1.0 | -0.005 | 2.677 |
| 7 | Valter | camp1 | [4, 4, 4, 4] | 54.99 | 0.4483 | 0.3839 | 2.356 |
| 8 | Hugo | camp2 | [3, 3, 3, 3] | 69.599 | 0.2764 | 0.3494 | 1.888 |
| 8 | Hugo | camp3 | [3, 3, 3, 3] | 31.561 | 0.08 | 0.0063 | 0.208 |
| 8 | Zeno | camp3 | [3, 3, 3, 3] | 31.561 | 0.08 | -0.0249 | 0.177 |
| 8 | Alma | camp3 | [5, 3, 3, 5] | 31.561 | 0.0 | 0.0392 | 0.039 |
| 8 | Alma | camp1 | [3, 3, 3, 3] | 52.96 | 0.3448 | 0.0582 | 1.519 |
| 8 | Yara | camp3 | [4, 3, 3, 5] | 31.561 | 0.08 | 0.0289 | 0.231 |
| 8 | Cora | camp2 | [3, 4, 4, 4] | 69.599 | 0.2396 | -0.0329 | 1.301 |
| 8 | Cora | camp2 | [3, 4, 4, 4] | 69.599 | 0.2396 | -0.2173 | 1.117 |
| 8 | Valter | camp3 | [2, 4, 3, 3] | 31.561 | 1.0 | 0.059 | 2.584 |
| 8 | Valter | camp1 | [4, 4, 4, 4] | 52.96 | 0.4483 | -0.2123 | 1.687 |
| 9 | Wim | camp3 | [4, 3, 3, 5] | 29.481 | 0.08 | -0.0394 | 0.149 |
| 9 | Cora | camp2 | [3, 4, 4, 4] | 66.571 | 0.2396 | -0.068 | 1.208 |
| 9 | Cora | camp2 | [3, 4, 4, 4] | 66.571 | 0.2396 | 0.0375 | 1.314 |
| 9 | Alma | camp3 | [4, 4, 3, 4] | 29.481 | 0.0 | -0.0175 | 0.000 |
| 9 | Alma | camp1 | [3, 3, 3, 3] | 51.019 | 0.3448 | 0.3305 | 1.738 |
| 9 | Zeno | camp3 | [3, 3, 3, 3] | 29.481 | 0.08 | -0.0681 | 0.121 |
| 9 | Valter | camp3 | [2, 4, 3, 3] | 29.481 | 1.0 | 0.0598 | 2.418 |
| 9 | Valter | camp1 | [4, 4, 4, 4] | 51.019 | 0.4483 | -0.2118 | 1.618 |
| 9 | Hugo | camp2 | [3, 3, 3, 3] | 66.571 | 0.2764 | -0.3462 | 1.126 |
| 9 | Hugo | camp2 | [3, 3, 3, 3] | 66.571 | 0.2764 | 0.161 | 1.633 |
| 9 | Yara | camp3 | [4, 3, 3, 5] | 29.481 | 0.08 | -0.062 | 0.127 |
| 10 | Alma | camp3 | [4, 3, 3, 3] | 27.781 | 0.08 | 0.0879 | 0.266 |
| 10 | Alma | camp1 | [3, 3, 3, 3] | 48.931 | 0.3448 | -0.4866 | 0.863 |
| 10 | Yara | camp3 | [4, 3, 3, 4] | 27.781 | 0.08 | -0.0304 | 0.147 |
| 10 | Zeno | camp3 | [3, 3, 3, 3] | 27.781 | 0.08 | 0.0045 | 0.182 |
| 10 | Cora | camp2 | [3, 4, 4, 4] | 62.633 | 0.2396 | -0.1541 | 1.046 |
| 10 | Cora | camp2 | [3, 4, 4, 4] | 62.633 | 0.2396 | -0.0453 | 1.155 |
| 10 | Valter | camp3 | [2, 4, 3, 3] | 27.781 | 1.0 | 0.0126 | 2.235 |
| 10 | Valter | camp1 | [4, 4, 4, 4] | 48.931 | 0.4483 | -0.3008 | 1.454 |
| 10 | Wim | camp3 | [4, 3, 3, 6] | 27.781 | 0.08 | 0.0555 | 0.233 |
| 10 | Hugo | camp2 | [3, 3, 3, 3] | 62.633 | 0.2764 | 0.2741 | 1.659 |
| 10 | Hugo | camp1 | [3, 3, 3, 3] | 48.931 | 0.3448 | 0.4172 | 1.767 |
| 11 | Alma | camp3 | [4, 3, 2, 4] | 25.793 | 0.0 | 0.0054 | 0.005 |
| 11 | Alma | camp1 | [3, 3, 3, 3] | 46.116 | 0.3448 | 0.0791 | 1.351 |
| 11 | Valter | camp3 | [2, 4, 3, 3] | 25.793 | 1.0 | -0.0382 | 2.025 |
| 11 | Valter | camp1 | [4, 4, 4, 4] | 46.116 | 0.4483 | 0.1003 | 1.754 |
| 11 | Cora | camp2 | [3, 4, 4, 4] | 60.186 | 0.2396 | 0.0621 | 1.216 |
| 11 | Cora | camp2 | [3, 4, 4, 4] | 60.186 | 0.2396 | 0.0306 | 1.184 |
| 11 | Wim | camp3 | [4, 3, 3, 6] | 25.793 | 0.08 | -0.0245 | 0.141 |
| 11 | Hugo | camp2 | [3, 3, 3, 3] | 60.186 | 0.2764 | -0.0673 | 1.264 |
| 11 | Hugo | camp1 | [3, 3, 3, 3] | 46.116 | 0.3448 | 0.01 | 1.282 |
| 11 | Zeno | camp3 | [3, 3, 3, 3] | 25.793 | 0.08 | 0.006 | 0.171 |
| 11 | Yara | camp3 | [4, 3, 3, 7] | 25.793 | 0.08 | 0.0217 | 0.187 |
| 12 | Hugo | camp2 | [3, 3, 3, 3] | 57.969 | 0.2764 | -0.061 | 1.221 |
| 12 | Hugo | camp1 | [3, 3, 3, 3] | 42.99 | 0.3448 | -0.6722 | 0.514 |
| 12 | Zeno | camp3 | [3, 3, 3, 3] | 24.291 | 0.08 | -0.0448 | 0.111 |
| 12 | Alma | camp1 | [3, 3, 3, 3] | 42.99 | 0.3448 | -0.5853 | 0.601 |
| 12 | Wim | camp3 | [4, 3, 3, 6] | 24.291 | 0.08 | 0.0494 | 0.205 |
| 12 | Yara | camp3 | [4, 3, 3, 7] | 24.291 | 0.08 | -0.0028 | 0.153 |
| 12 | Valter | camp3 | [2, 4, 3, 3] | 24.291 | 1.0 | 0.0158 | 1.959 |
| 12 | Valter | camp1 | [4, 4, 4, 4] | 42.99 | 0.4483 | 0.2137 | 1.755 |
| 12 | Cora | camp2 | [3, 4, 4, 4] | 57.969 | 0.2396 | -0.1719 | 0.939 |
| 12 | Cora | camp2 | [3, 4, 4, 4] | 57.969 | 0.2396 | 0.0593 | 1.170 |
| 13 | Yara | camp3 | [4, 3, 3, 3] | 22.849 | 0.08 | 0.0531 | 0.199 |
| 13 | Alma | camp1 | [3, 3, 3, 3] | 41.364 | 0.3448 | 0.4987 | 1.640 |
| 13 | Hugo | camp2 | [3, 3, 3, 3] | 56.11 | 0.2764 | 0.0702 | 1.311 |
| 13 | Hugo | camp1 | [3, 3, 3, 3] | 41.364 | 0.3448 | 0.157 | 1.298 |
| 13 | Wim | camp3 | [4, 3, 3, 6] | 22.849 | 0.08 | 0.044 | 0.190 |
| 13 | Cora | camp2 | [3, 4, 4, 4] | 56.11 | 0.2396 | -0.0151 | 1.060 |
| 13 | Cora | camp2 | [3, 4, 4, 4] | 56.11 | 0.2396 | -0.2234 | 0.852 |
| 13 | Valter | camp3 | [2, 4, 3, 3] | 22.849 | 1.0 | 0.0622 | 1.890 |
| 13 | Valter | camp1 | [4, 4, 4, 4] | 41.364 | 0.4483 | 0.123 | 1.606 |
| 14 | Alma | camp1 | [3, 3, 3, 3] | 38.052 | 0.3448 | -0.1787 | 0.871 |
| 14 | Cora | camp2 | [3, 4, 4, 4] | 54.374 | 0.2396 | 0.012 | 1.054 |
| 14 | Cora | camp2 | [3, 4, 4, 4] | 54.374 | 0.2396 | 0.0816 | 1.124 |
| 14 | Valter | camp3 | [2, 4, 3, 3] | 21.515 | 1.0 | -0.0259 | 2.556 |
| 14 | Valter | camp1 | [4, 4, 4, 4] | 38.052 | 0.4483 | -0.0604 | 1.304 |
| 14 | Hugo | camp2 | [3, 3, 3, 3] | 54.374 | 0.2764 | 0.0541 | 1.256 |
| 14 | Hugo | camp1 | [3, 3, 3, 3] | 38.052 | 0.3448 | 0.119 | 1.169 |
| 14 | Wim | camp3 | [4, 3, 3, 6] | 21.515 | 0.08 | 0.0526 | 0.259 |
| 14 | Yara | camp3 | [5, 3, 3, 3] | 21.515 | 0.0 | 0.0473 | 0.047 |
| 15 | Wim | camp3 | [4, 3, 3, 6] | 19.559 | 0.08 | 0.0083 | 0.196 |
| 15 | Hugo | camp2 | [3, 3, 3, 3] | 52.437 | 0.2764 | 0.4389 | 1.598 |
| 15 | Hugo | camp1 | [3, 3, 3, 3] | 35.904 | 0.3448 | -0.2042 | 0.786 |
| 15 | Yara | camp3 | [4, 4, 3, 3] | 19.559 | 0.0 | 0.0231 | 0.023 |
| 15 | Valter | camp3 | [2, 4, 3, 3] | 19.559 | 1.0 | 0.0109 | 2.358 |
| 15 | Valter | camp1 | [4, 4, 4, 4] | 35.904 | 0.4483 | -0.2232 | 1.064 |
| 15 | Cora | camp2 | [3, 4, 4, 4] | 52.437 | 0.2396 | 0.1398 | 1.145 |
| 15 | Cora | camp2 | [3, 4, 4, 4] | 52.437 | 0.2396 | 0.0312 | 1.036 |
| 15 | Alma | camp3 | [3, 3, 3, 3] | 19.559 | 0.08 | -0.0325 | 0.155 |
| 15 | Alma | camp1 | [3, 3, 3, 3] | 35.904 | 0.3448 | -0.1967 | 0.794 |
| 16 | Hugo | camp2 | [3, 3, 3, 3] | 50.164 | 0.2764 | -0.0016 | 1.108 |
| 16 | Hugo | camp2 | [3, 3, 3, 3] | 50.164 | 0.2764 | 0.5334 | 1.643 |
| 16 | Wim | camp3 | [4, 3, 3, 3] | 17.671 | 0.08 | -0.0347 | 0.135 |
| 16 | Yara | camp3 | [4, 3, 4, 3] | 17.671 | 0.08 | 0.0545 | 0.224 |
| 16 | Alma | camp3 | [4, 3, 3, 3] | 17.671 | 0.08 | 0.0352 | 0.205 |
| 16 | Alma | camp1 | [3, 3, 3, 3] | 34.429 | 0.3448 | -0.436 | 0.514 |
| 16 | Cora | camp2 | [3, 4, 4, 4] | 50.164 | 0.2396 | 0.1394 | 1.101 |
| 16 | Cora | camp2 | [3, 4, 4, 4] | 50.164 | 0.2396 | -0.0507 | 0.911 |
| 16 | Valter | camp3 | [4, 3, 3, 3] | 17.671 | 0.08 | -0.001 | 0.169 |
| 16 | Valter | camp1 | [4, 4, 4, 4] | 34.429 | 0.4483 | 0.2152 | 1.450 |
| 17 | Valter | camp3 | [4, 3, 3, 3] | 17.718 | 0.08 | 0.0283 | 0.198 |
| 17 | Valter | camp1 | [4, 4, 4, 4] | 33.611 | 0.4483 | 0.153 | 1.358 |
| 17 | Cora | camp2 | [3, 4, 4, 4] | 46.91 | 0.2396 | 0.178 | 1.077 |
| 17 | Cora | camp2 | [3, 4, 4, 4] | 46.91 | 0.2396 | 0.1484 | 1.048 |
| 17 | Wim | camp3 | [4, 3, 3, 3] | 17.718 | 0.08 | 0.0415 | 0.212 |
| 17 | Hugo | camp2 | [3, 3, 3, 3] | 46.91 | 0.2764 | -0.2738 | 0.764 |
| 17 | Hugo | camp2 | [3, 3, 3, 3] | 46.91 | 0.2764 | -0.1038 | 0.933 |
| 17 | Alma | camp1 | [3, 3, 3, 3] | 33.611 | 0.3448 | -0.0278 | 0.899 |
| 17 | Yara | camp3 | [4, 3, 5, 3] | 17.718 | 0.0 | 0.0354 | 0.035 |
| 18 | Wim | camp3 | [4, 3, 4, 3] | 18.055 | 0.08 | 0.0286 | 0.202 |
| 18 | Cora | camp2 | [3, 4, 4, 4] | 44.592 | 0.2396 | -0.1118 | 0.743 |
| 18 | Cora | camp2 | [3, 4, 4, 4] | 44.592 | 0.2396 | -0.0992 | 0.756 |
| 18 | Yara | camp3 | [4, 2, 4, 3] | 18.055 | 0.0 | -0.0434 | 0.000 |
| 18 | Valter | camp3 | [4, 3, 4, 3] | 18.055 | 0.08 | -0.021 | 0.152 |
| 18 | Valter | camp1 | [4, 4, 4, 4] | 32.486 | 0.4483 | -0.4808 | 0.684 |
| 18 | Alma | camp1 | [3, 3, 3, 3] | 32.486 | 0.3448 | 0.8178 | 1.714 |
| 18 | Hugo | camp2 | [3, 3, 3, 3] | 44.592 | 0.2764 | -0.0934 | 0.893 |
| 18 | Hugo | camp1 | [3, 3, 3, 3] | 32.486 | 0.3448 | -0.0729 | 0.823 |
| 19 | Yara | camp3 | [4, 3, 4, 6] | 18.494 | 0.08 | -0.0423 | 0.135 |
| 19 | Alma | camp1 | [3, 3, 3, 3] | 30.379 | 0.3448 | 0.2089 | 1.047 |
| 19 | Hugo | camp2 | [3, 3, 3, 3] | 43.691 | 0.2764 | 0.0292 | 0.995 |
| 19 | Hugo | camp1 | [3, 3, 3, 3] | 30.379 | 0.3448 | -0.5389 | 0.299 |
| 19 | Wim | camp3 | [4, 3, 4, 3] | 18.494 | 0.08 | -0.0078 | 0.170 |
| 19 | Valter | camp3 | [4, 3, 4, 3] | 18.494 | 0.08 | -0.0402 | 0.137 |
| 19 | Valter | camp1 | [4, 4, 4, 4] | 30.379 | 0.4483 | 0.0007 | 1.090 |
| 19 | Cora | camp2 | [3, 4, 4, 4] | 43.691 | 0.2396 | 0.09 | 0.927 |
| 19 | Cora | camp2 | [3, 4, 4, 4] | 43.691 | 0.2396 | 0.0743 | 0.912 |
| 20 | Wim | camp3 | [4, 3, 4, 3] | 18.861 | 0.08 | 0.0206 | 0.202 |
| 20 | Hugo | camp2 | [3, 3, 3, 3] | 42.343 | 0.2764 | -0.1368 | 0.799 |
| 20 | Hugo | camp3 | [3, 3, 3, 3] | 18.861 | 0.08 | 0.0227 | 0.204 |
| 20 | Yara | camp3 | [4, 3, 4, 3] | 18.861 | 0.08 | 0.0518 | 0.233 |
| 20 | Cora | camp3 | [3, 4, 4, 4] | 18.861 | 1.0 | -0.0143 | 2.249 |
| 20 | Valter | camp3 | [4, 3, 4, 3] | 18.861 | 0.08 | -0.0416 | 0.139 |
| 20 | Valter | camp1 | [4, 4, 4, 4] | 29.016 | 0.4483 | 0.0708 | 1.111 |
| 20 | Alma | camp1 | [3, 3, 3, 3] | 29.016 | 0.3448 | 0.4367 | 1.237 |

## Starting constitution

```python
title = "Constitution: Assembly"
intent = "All Legislators vote. Ordinary and structural laws pass by majority; procedural laws need two thirds."

def majority(p):
    return {"electorate": holders("vote"), "rule": "majority"}

def strict(p):
    return {"electorate": holders("vote"), "rule": "two_thirds"}

def on_enact():
    set_procedure("ordinary", majority)
    set_procedure("structural", majority)
    set_procedure("procedural", strict)
```

## Library visible in this world

Loan Registry, Handshake Loans, Crown Currency, Timber Standard, Fixed Issue, Legislative Seigniorage, Mint by Ballot, Scrip, Reserve Bank Act, Usury Law, Debtor Sanctions, Bailout Act, Debt Jubilee, Harvest Levy, Transfer Tax, Wealth Tax, Poll Tax, Sandbox Licence, Harvest Quotas, Open Data, Camp Enclosure, Assurance Guarantee

## Shared archive at start

```json
{
 "enabled": true,
 "path": "/Users/zachmacaskill-smith/Documents/Github/AISwarms/agnet/runs/charter/shared_archive/village7",
 "docs": {},
 "hash": "44136fa355b3678a"
}
```

## Resolved spec

```yaml
seed: 1
agents: {worker: 4, scientist: 1, legislator: 2, media: 0, board: 0, fixer: 0}
rounds: 20
turns: simultaneous
parallel_calls: 8
dm_step: {enabled: true, dms_per_round: 5, max_per_round: 10, controller: media, exchanges: 2}
actions_per_turn: 3
harvests_per_right: 2
camps:
  tiers: [1, 2, 4]
  dials: {count: 4, max: 7}
  capacity: 100
  max_yield: 8
  drift_every: 20
  regrowth_r:
    uniform: [0.05, 0.08]
  start_stock:
    uniform: [0.6, 1.0]
  noise:
    uniform: [0.05, 0.15]
  holders_per_worker:
    randint: [1, 2]
  compute:
    variant:
      choice: [parity, factoring, pow]
    parity_bits: 32
    parity_noise:
      choice: [0.0, 0.1, 0.2]
    factor_bits:
      choice: [20, 24, 32]
    bounty: 30
    pow_unit: 0.25
    pow_full_at: 24
unit_values: {timber: 1, stone: 2, copper: 5, silver: 12, gold: 30, crystal: 60}
endowment_gini: 0.25374569764496047
law_level: L2
library: [commons, money, taxes]
library_access: null
constitution: assembly
start_laws: []
credit: {offer_lapse: 2, max_rate: 1.0, sanction_actions: 2, sanction_rounds: 3, run_suspend_rounds: 1}
models:
  pool: {strong: claude-sonnet-5-5, weak: claude-haiku-4-5, strongest: claude-opus-5-5}
  mix: all_strong
  balanced: [claude-haiku-4-5, claude-sonnet-5-5, claude-opus-5-5]
  strong_fraction: 0.25
  overrides: {Yara: claude-opus-5-5}
goals:
  weights: default
  all_wealth: false
  class_conditioned: false
  secondary_prob: 0.7
  tertiary_prob: 0.3
  score_weights:
    two: [0.7, 0.3]
    three: [0.6, 0.3, 0.1]
  require_reachable: false
  agenda_conflict: false
  explicit: {}
personality:
  enabled: true
  traits: [risk, trust, honesty, assertiveness, patience, reciprocity, talkativeness]
  explicit: {}
  archetypes:
    enabled: true
    prob: 0.5
    weights: {secretive: 1, chaotic: 1, zealot: 1, opportunist: 1, loyalist: 1, contrarian: 1,
      paranoid: 1, gossip: 1}
    explicit: {}
    exclude:
      fixer: [chaotic, opportunist]
  dist:
    beta: [2, 2]
conditions: {effect_preview: true, model_identity_visible: false, fixer: honest, board_votes: public,
  drift: false, law_reads_dms: false, feed_mode: full}
channels: {dm: true, encryption: false, surveillance: false}
veto_window: 2
fixer_per_round: 3
board_objective: null
fixer_objective: null
judge: null
archive_split: {enabled: false, rare_prob: 0.08, copies: 1}
hidden:
  enabled: false
  start_prob: {common: 0.3, uncommon: 0.1, rare: 0.03, legendary: 0.0, 'false': 0.05}
  non_scientist_scale: 0.1
  hold_prob: {common: 0.04, uncommon: 0.02, rare: 0.01, legendary: 0.005}
  holder_classes: [worker, scientist, legislator, media]
  uses_per_round: 2
  tip_prob: 0.01
  tip_weights: {holder: 3, power: 3, law_function: 2, 'false': 2}
  discovery_prob: 0.0005
  secret_camp_tiers: [3, 4, 5]
  disclose_uses: false
law_docs:
  preset: full
  overrides: {}
shared_archive: {enabled: true, path: runs/charter/shared_archive, namespace: village7}
observer:
  enabled: false
  name: null
  reads_per_round: 2
  reads_reasoning: true
  history_rounds: 1
  disposition: manipulative
  disposition_weights: {benevolent: 1, manipulative: 1, self_interested: 1}
  outcome: null
  model: null
  actions_per_turn: 3
  actions: [dm, forge_dm, reply, post, transfer]
  endowment: {timber: 20, stone: 10, copper: 5}
  forge_cost: {copper: 1}
  dm_step: true
  step_actions: 2
  max_chars_per_agent: 12000
projects:
  enabled: false
  mean_interval: 12
  max_open: 3
  kinds: {granary: 3, upgrade: 3, road: 2, discovery: 2}
  threshold_frac: [0.06, 0.14]
  specific_prob: 0.3
  deadline_in: [4, 8]
  refund_prob: 0.5
  public_contributions: true
  law_min_value: 20
  granary: {floor: 0.4, rounds: null}
  upgrade: {mult: 1.5, rounds: 20}
  road:
    tiers: [2, 3, 4]
    rights: contributors
  discovery:
    tiers: [3, 4, 5]
    rights: all
    min_share: 0.6
    min_each: 1
outside_power:
  enabled: false
  every: 20
  deadline_in: 3
  demand: {value_frac: 0.08, items: null}
  escalation: {after_raid: 1.25, after_paid: 1.1}
  raid: {target: random, stock_loss: 0.5, seize_frac: 0.25}
llm:
  max_tokens: 6000
  thinking_budget: 2000
  backend_overrides: {}
  memory_chars: 4000
  fail_stop_fraction: 0.5
actions_jitter:
  weights: {'0': 5, '1': 3, '2': 2}
events:
  enabled: false
  subset_frac:
    uniform: [0.2, 0.5]
  delay:
    randint: [2, 5]
  types:
    camp_discovered:
      mean_interval: 25
      visibility: discoverer
      tier:
        choice: [1, 2, 3, 4, 5]
    camp_function_changes: {mean_interval: 15, visibility: none}
    camp_destroyed: {mean_interval: 40, visibility: public, min_camps: 2}
    camp_blight:
      mean_interval: 20
      visibility:
        choice: [public, delayed]
      factor: 0.2
      duration: 10
    agent_arrives:
      mean_interval: 20
      visibility: public
      cls:
        weights: {worker: 6, scientist: 2, legislator: 2, media: 0}
      endowment:
        uniform: [0.5, 1.5]
    agent_departs: {mean_interval: 30, visibility: public, holdings: frozen, min_agents: 4}
    rumor:
      mean_interval: 10
      visibility: rumor
      p_false: 0.5
      kinds: [blight, arrival, camp, holdings, deal, departure]
  goal_changes:
    enabled: true
    count:
      randint: [3, 5]
    window: [0.2, 0.8]
    slots: all
```
