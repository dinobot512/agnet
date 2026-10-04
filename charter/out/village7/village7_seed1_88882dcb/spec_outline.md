# Spec outline: village7_seed1_88882dcb

## Seeds and random-number streams
- Instance seed: **1** (drives every draw below through `random.Random(1)` in the generator).
- Kernel RNG (turn orders, harvest noise): `random.Random(7936)` = seed x 7919 + 17.
- Law RNG (rng() inside laws, e.g. the Chair or Council draw): `random.Random(104732)` = seed x 104729 + 3.
- Archetype RNG (personality.archetypes): `random.Random("archetypes:1")`, separate so the draws above are unchanged.
- Scripted-bot RNG (dry runs only): `random.Random(1)`. Model sampling is not seeded (model calls are not deterministic).
- Run id: village7_seed1_88882dcb. Library access: titles_for_others. Repairs by the validator: none.
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
- Round 4: Zeno, Wim, Yara, Alma, Valter, Cora, Hugo
- Round 5: Cora, Yara, Hugo, Alma, Valter, Wim, Zeno
- Round 6: Valter, Zeno, Alma, Hugo, Cora, Yara, Wim
- Round 7: Wim, Yara, Valter, Cora, Alma, Hugo, Zeno
- Round 8: Yara, Valter, Cora, Hugo, Zeno, Alma, Wim
- Round 9: Alma, Yara, Zeno, Cora, Valter, Hugo, Wim
- Round 10: Hugo, Zeno, Yara, Alma, Cora, Valter, Wim
- Round 11: Wim, Alma, Valter, Zeno, Yara, Cora, Hugo
- Round 12: Alma, Valter, Cora, Wim, Hugo, Zeno, Yara
- Round 13: Hugo, Zeno, Alma, Wim, Yara, Valter, Cora
- Round 14: Yara, Alma, Zeno, Hugo, Wim, Cora, Valter
- Round 15: Alma, Cora, Zeno, Valter, Hugo, Wim, Yara
- Round 16: Yara, Hugo, Alma, Wim, Valter, Cora, Zeno
- Round 17: Valter, Zeno, Wim, Hugo, Yara, Alma, Cora
- Round 18: Valter, Cora, Wim, Hugo, Zeno, Alma, Yara
- Round 19: Wim, Zeno, Cora, Yara, Valter, Alma, Hugo
- Round 20: Cora, Alma, Wim, Hugo, Valter, Yara, Zeno

## Harvest noise draws

| round | agent | camp | x | stock before | efficiency | noise | yield |
|---|---|---|---|---|---|---|---|
| 1 | Valter | camp3 | [3, 3, 3, 3] | 94.398 | 0.08 | -0.0489 | 0.555 |
| 1 | Valter | camp3 | [5, 2, 5, 2] | 94.398 | 0.0 | -0.0086 | 0.000 |
| 1 | Cora | camp3 | [3, 3, 3, 3] | 94.398 | 0.08 | 0.0389 | 0.643 |
| 1 | Cora | camp3 | [5, 2, 5, 2] | 94.398 | 0.0 | 0.0283 | 0.028 |
| 1 | Cora | camp2 | [4, 4, 4, 4] | 82.114 | 0.2231 | 0.2259 | 1.691 |
| 1 | Alma | camp3 | [3, 3, 3, 3] | 94.398 | 0.08 | 0.0527 | 0.657 |
| 1 | Alma | camp1 | [4, 4, 4, 4] | 61.224 | 0.4483 | 0.1984 | 2.394 |
| 1 | Hugo | camp2 | [3, 3, 3, 3] | 82.114 | 0.2764 | -0.1232 | 1.692 |
| 1 | Hugo | camp2 | [5, 2, 5, 2] | 82.114 | 0.0402 | -0.0254 | 0.238 |
| 2 | Valter | camp3 | [2, 4, 2, 4] | 92.798 | 0.0 | -0.0196 | 0.000 |
| 2 | Valter | camp1 | [3, 3, 3, 3] | 60.035 | 0.3448 | -0.4087 | 1.247 |
| 2 | Cora | camp3 | [2, 3, 4, 3] | 92.798 | 0.0 | 0.0278 | 0.028 |
| 2 | Cora | camp2 | [6, 4, 6, 4] | 79.38 | 0.0302 | -0.1073 | 0.084 |
| 2 | Alma | camp3 | [5, 2, 5, 2] | 92.798 | 0.0 | 0.0005 | 0.001 |
| 2 | Alma | camp1 | [4, 4, 4, 4] | 60.035 | 0.4483 | -0.0618 | 2.091 |
| 2 | Hugo | camp1 | [3, 3, 3, 3] | 60.035 | 0.3448 | 0.576 | 2.232 |
| 2 | Hugo | camp2 | [2, 3, 2, 3] | 79.38 | 0.3678 | -0.0828 | 2.253 |
| 3 | Yara | camp3 | [4, 3, 3, 3] | 93.128 | 0.08 | -0.1137 | 0.482 |
| 3 | Yara | camp3 | [3, 4, 3, 3] | 93.128 | 0.0 | -0.0582 | 0.000 |
| 3 | Cora | camp3 | [5, 5, 5, 5] | 93.128 | 0.0 | 0.0156 | 0.016 |
| 3 | Cora | camp2 | [3, 3, 3, 3] | 78.031 | 0.2764 | -0.0604 | 1.665 |
| 3 | Hugo | camp1 | [4, 3, 3, 4] | 55.683 | 0.3793 | -0.3438 | 1.346 |
| 3 | Hugo | camp2 | [3, 3, 3, 3] | 78.031 | 0.2764 | 0.2292 | 1.955 |
| 3 | Alma | camp3 | [3, 3, 4, 3] | 93.128 | 0.0 | -0.0075 | 0.000 |
| 3 | Alma | camp3 | [3, 3, 3, 4] | 93.128 | 0.08 | 0.0484 | 0.644 |
| 3 | Valter | camp3 | [3, 3, 4, 3] | 93.128 | 0.0 | -0.026 | 0.000 |
| 3 | Valter | camp1 | [3, 4, 3, 3] | 55.683 | 0.4483 | -0.3507 | 1.646 |
| 4 | Yara | camp3 | [3, 2, 3, 3] | 92.329 | 0.0 | 0.0072 | 0.007 |
| 4 | Yara | camp3 | [3, 3, 2, 3] | 92.329 | 0.08 | -0.0108 | 0.580 |
| 4 | Alma | camp3 | [3, 3, 3, 5] | 92.329 | 0.08 | 0.0111 | 0.602 |
| 4 | Alma | camp1 | [3, 4, 3, 3] | 53.943 | 0.4483 | 0.0679 | 2.002 |
| 4 | Valter | camp3 | [3, 3, 3, 3] | 92.329 | 0.08 | 0.0262 | 0.617 |
| 4 | Valter | camp1 | [3, 4, 3, 3] | 53.943 | 0.4483 | -0.1095 | 1.825 |
| 4 | Cora | camp2 | [3, 3, 3, 3] | 75.446 | 0.2764 | 0.2991 | 1.967 |
| 4 | Cora | camp3 | [3, 3, 3, 4] | 92.329 | 0.08 | 0.0432 | 0.634 |
| 4 | Hugo | camp1 | [3, 4, 3, 4] | 53.943 | 0.4483 | -0.1165 | 1.818 |
| 4 | Hugo | camp2 | [3, 3, 4, 3] | 75.446 | 0.1676 | -0.2295 | 0.782 |
| 5 | Cora | camp2 | [3, 3, 3, 3] | 73.815 | 0.2764 | 0.1399 | 1.772 |
| 5 | Cora | camp3 | [3, 3, 3, 4] | 90.269 | 0.08 | -0.0297 | 0.548 |
| 5 | Yara | camp3 | [2, 3, 3, 3] | 90.269 | 0.0 | 0.0446 | 0.045 |
| 5 | Yara | camp3 | [3, 3, 3, 2] | 90.269 | 0.08 | -0.0856 | 0.492 |
| 5 | Hugo | camp1 | [3, 4, 3, 4] | 49.56 | 0.4483 | 0.3798 | 2.157 |
| 5 | Hugo | camp2 | [3, 3, 3, 3] | 73.815 | 0.2764 | 0.0981 | 1.730 |
| 5 | Alma | camp3 | [3, 3, 3, 4] | 90.269 | 0.08 | 0.0517 | 0.629 |
| 5 | Alma | camp1 | [3, 4, 3, 3] | 49.56 | 0.4483 | 0.1242 | 1.902 |
| 5 | Valter | camp3 | [3, 3, 3, 4] | 90.269 | 0.08 | -0.0333 | 0.544 |
| 5 | Valter | camp1 | [3, 4, 3, 4] | 49.56 | 0.4483 | -0.1257 | 1.652 |
| 6 | Valter | camp3 | [3, 3, 3, 3] | 88.482 | 0.08 | 0.0216 | 0.588 |
| 6 | Valter | camp1 | [3, 4, 3, 3] | 45.118 | 0.4483 | 0.3968 | 2.015 |
| 6 | Alma | camp3 | [3, 3, 3, 4] | 88.482 | 0.08 | 0.1047 | 0.671 |
| 6 | Alma | camp1 | [3, 4, 3, 3] | 45.118 | 0.4483 | -0.3853 | 1.233 |
| 6 | Hugo | camp1 | [3, 4, 3, 4] | 45.118 | 0.4483 | 0.089 | 1.707 |
| 6 | Hugo | camp2 | [3, 3, 3, 3] | 71.48 | 0.2764 | -0.045 | 1.536 |
| 6 | Cora | camp2 | [3, 3, 3, 3] | 71.48 | 0.2764 | 0.129 | 1.710 |
| 6 | Cora | camp3 | [3, 3, 3, 4] | 88.482 | 0.08 | 0.0131 | 0.579 |
| 6 | Yara | camp3 | [3, 3, 3, 3] | 88.482 | 0.08 | -0.0073 | 0.559 |
| 6 | Yara | camp3 | [3, 3, 3, 4] | 88.482 | 0.08 | -0.062 | 0.504 |
| 7 | Yara | camp3 | [3, 3, 3, 3] | 86.127 | 0.08 | 0.0204 | 0.572 |
| 7 | Yara | camp3 | [3, 3, 3, 4] | 86.127 | 0.08 | 0.0091 | 0.560 |
| 7 | Valter | camp3 | [3, 3, 3, 3] | 86.127 | 0.08 | 0.0388 | 0.590 |
| 7 | Valter | camp1 | [3, 4, 3, 3] | 41.42 | 0.4483 | 0.1617 | 1.647 |
| 7 | Cora | camp2 | [3, 3, 3, 3] | 69.465 | 0.2764 | 0.1459 | 1.682 |
| 7 | Cora | camp3 | [3, 3, 3, 4] | 86.127 | 0.08 | 0.0388 | 0.590 |
| 7 | Alma | camp3 | [3, 3, 3, 4] | 86.127 | 0.08 | 0.053 | 0.604 |
| 7 | Alma | camp3 | [3, 3, 3, 4] | 86.127 | 0.08 | 0.0374 | 0.589 |
| 7 | Hugo | camp2 | [3, 3, 3, 3] | 69.465 | 0.2764 | -0.3324 | 1.204 |
| 7 | Hugo | camp1 | [3, 4, 3, 4] | 41.42 | 0.4483 | 0.2304 | 1.716 |
| 8 | Yara | camp3 | [3, 3, 3, 3] | 83.263 | 0.08 | 0.0077 | 0.541 |
| 8 | Yara | camp3 | [3, 4, 3, 3] | 83.263 | 0.0 | 0.0197 | 0.020 |
| 8 | Valter | camp3 | [3, 3, 3, 3] | 83.263 | 0.08 | 0.0158 | 0.549 |
| 8 | Valter | camp3 | [3, 3, 3, 4] | 83.263 | 0.08 | 0.0139 | 0.547 |
| 8 | Cora | camp3 | [3, 3, 3, 4] | 83.263 | 0.08 | -0.0105 | 0.522 |
| 8 | Cora | camp2 | [3, 3, 3, 3] | 67.86 | 0.2764 | -0.0438 | 1.457 |
| 8 | Hugo | camp2 | [3, 3, 3, 3] | 67.86 | 0.2764 | 0.3834 | 1.884 |
| 8 | Hugo | camp2 | [3, 3, 3, 3] | 67.86 | 0.2764 | 0.1199 | 1.620 |
| 8 | Alma | camp3 | [3, 3, 3, 3] | 83.263 | 0.08 | 0.0653 | 0.598 |
| 8 | Alma | camp3 | [3, 3, 3, 4] | 83.263 | 0.08 | -0.0653 | 0.468 |
| 9 | Alma | camp3 | [3, 3, 3, 3] | 80.766 | 0.08 | -0.0381 | 0.479 |
| 9 | Alma | camp3 | [3, 3, 3, 3] | 80.766 | 0.08 | 0.0088 | 0.526 |
| 9 | Yara | camp3 | [3, 3, 3, 3] | 80.766 | 0.08 | 0.0394 | 0.556 |
| 9 | Yara | camp3 | [3, 3, 4, 3] | 80.766 | 0.0 | 0.0167 | 0.017 |
| 9 | Cora | camp3 | [3, 3, 3, 3] | 80.766 | 0.08 | -0.0601 | 0.457 |
| 9 | Cora | camp3 | [3, 3, 3, 3] | 80.766 | 0.08 | -0.0489 | 0.468 |
| 9 | Valter | camp3 | [3, 3, 3, 3] | 80.766 | 0.08 | 0.0115 | 0.528 |
| 9 | Valter | camp3 | [3, 3, 3, 3] | 80.766 | 0.08 | 0.0078 | 0.525 |
| 9 | Hugo | camp2 | [3, 3, 3, 3] | 64.215 | 0.2764 | -0.0739 | 1.346 |
| 9 | Hugo | camp2 | [3, 3, 3, 3] | 64.215 | 0.2764 | -0.1399 | 1.280 |
| 10 | Hugo | camp2 | [3, 3, 3, 3] | 62.977 | 0.2764 | 0.0266 | 1.419 |
| 10 | Hugo | camp2 | [3, 3, 3, 3] | 62.977 | 0.2764 | 0.3565 | 1.749 |
| 10 | Yara | camp3 | [3, 3, 3, 3] | 78.043 | 0.08 | -0.0152 | 0.484 |
| 10 | Yara | camp3 | [3, 2, 3, 3] | 78.043 | 0.0 | -0.083 | 0.000 |
| 10 | Alma | camp3 | [3, 3, 3, 3] | 78.043 | 0.08 | -0.0273 | 0.472 |
| 10 | Alma | camp3 | [3, 3, 3, 3] | 78.043 | 0.08 | 0.0453 | 0.545 |
| 10 | Cora | camp3 | [3, 3, 3, 3] | 78.043 | 0.08 | -0.0479 | 0.452 |
| 10 | Cora | camp3 | [3, 3, 3, 3] | 78.043 | 0.08 | -0.0144 | 0.485 |
| 10 | Valter | camp3 | [3, 3, 3, 3] | 78.043 | 0.08 | 0.0173 | 0.517 |
| 10 | Valter | camp3 | [3, 3, 3, 3] | 78.043 | 0.08 | 0.0878 | 0.587 |
| 11 | Alma | camp3 | [3, 3, 3, 3] | 75.42 | 0.08 | -0.0433 | 0.439 |
| 11 | Alma | camp3 | [3, 3, 3, 3] | 75.42 | 0.08 | -0.0304 | 0.452 |
| 11 | Valter | camp3 | [3, 3, 3, 3] | 75.42 | 0.08 | 0.0045 | 0.487 |
| 11 | Valter | camp3 | [3, 3, 3, 3] | 75.42 | 0.08 | -0.034 | 0.449 |
| 11 | Yara | camp3 | [3, 3, 3, 5] | 75.42 | 0.08 | -0.01 | 0.473 |
| 11 | Yara | camp3 | [3, 3, 3, 6] | 75.42 | 0.08 | 0.0126 | 0.495 |
| 11 | Cora | camp3 | [3, 3, 3, 3] | 75.42 | 0.08 | -0.0382 | 0.444 |
| 11 | Cora | camp3 | [3, 3, 3, 3] | 75.42 | 0.08 | 0.0555 | 0.538 |
| 11 | Hugo | camp2 | [3, 3, 3, 3] | 61.216 | 0.2764 | 0.2741 | 1.628 |
| 11 | Hugo | camp2 | [3, 3, 3, 3] | 61.216 | 0.2764 | 0.2401 | 1.594 |
| 12 | Alma | camp3 | [3, 3, 3, 3] | 72.637 | 0.08 | 0.0054 | 0.470 |
| 12 | Alma | camp3 | [3, 3, 3, 3] | 72.637 | 0.08 | 0.01 | 0.475 |
| 12 | Valter | camp3 | [3, 3, 3, 3] | 72.637 | 0.08 | -0.0382 | 0.427 |
| 12 | Valter | camp3 | [3, 3, 3, 3] | 72.637 | 0.08 | 0.0127 | 0.478 |
| 12 | Cora | camp3 | [3, 3, 3, 3] | 72.637 | 0.08 | 0.0137 | 0.479 |
| 12 | Cora | camp3 | [3, 3, 3, 3] | 72.637 | 0.08 | 0.0068 | 0.472 |
| 12 | Hugo | camp2 | [3, 3, 3, 3] | 59.428 | 0.2764 | -0.1109 | 1.203 |
| 12 | Hugo | camp2 | [3, 3, 3, 3] | 59.428 | 0.2764 | -0.0673 | 1.247 |
| 12 | Yara | camp3 | [3, 3, 2, 6] | 72.637 | 0.08 | 0.0013 | 0.466 |
| 12 | Yara | camp3 | [3, 3, 2, 5] | 72.637 | 0.08 | 0.006 | 0.471 |
| 13 | Hugo | camp2 | [3, 3, 3, 3] | 58.433 | 0.2764 | 0.0984 | 1.390 |
| 13 | Hugo | camp2 | [3, 3, 3, 3] | 58.433 | 0.2764 | -0.061 | 1.231 |
| 13 | Alma | camp3 | [3, 3, 3, 3] | 69.965 | 0.08 | -0.0854 | 0.362 |
| 13 | Alma | camp3 | [3, 3, 3, 3] | 69.965 | 0.08 | -0.0448 | 0.403 |
| 13 | Yara | camp3 | [3, 3, 2, 4] | 69.965 | 0.08 | -0.0743 | 0.373 |
| 13 | Yara | camp3 | [3, 3, 1, 3] | 69.965 | 0.0 | 0.0494 | 0.049 |
| 13 | Valter | camp3 | [3, 3, 3, 3] | 69.965 | 0.08 | -0.0028 | 0.445 |
| 13 | Valter | camp3 | [3, 3, 3, 3] | 69.965 | 0.08 | 0.0158 | 0.464 |
| 13 | Cora | camp3 | [3, 3, 3, 3] | 69.965 | 0.08 | 0.0271 | 0.475 |
| 13 | Cora | camp3 | [3, 3, 3, 3] | 69.965 | 0.08 | -0.0379 | 0.410 |
| 14 | Yara | camp3 | [3, 3, 3, 4] | 68.11 | 0.08 | 0.0131 | 0.449 |
| 14 | Yara | camp3 | [3, 3, 2, 3] | 68.11 | 0.08 | 0.0531 | 0.489 |
| 14 | Alma | camp3 | [3, 3, 3, 3] | 68.11 | 0.08 | 0.0633 | 0.499 |
| 14 | Alma | camp3 | [3, 3, 3, 3] | 68.11 | 0.08 | 0.0155 | 0.451 |
| 14 | Hugo | camp2 | [3, 3, 3, 3] | 57.278 | 0.2764 | 0.0904 | 1.357 |
| 14 | Hugo | camp2 | [3, 3, 3, 3] | 57.278 | 0.2764 | 0.1995 | 1.466 |
| 14 | Cora | camp3 | [3, 3, 3, 3] | 68.11 | 0.08 | -0.0033 | 0.433 |
| 14 | Cora | camp3 | [3, 3, 3, 3] | 68.11 | 0.08 | -0.0493 | 0.387 |
| 14 | Valter | camp3 | [3, 3, 3, 3] | 68.11 | 0.08 | 0.0622 | 0.498 |
| 14 | Valter | camp3 | [3, 3, 3, 3] | 68.11 | 0.08 | 0.0156 | 0.452 |
| 15 | Alma | camp3 | [3, 3, 3, 3] | 65.617 | 0.08 | -0.0227 | 0.397 |
| 15 | Alma | camp3 | [3, 3, 3, 3] | 65.617 | 0.08 | 0.0027 | 0.423 |
| 15 | Cora | camp2 | [3, 3, 3, 3] | 55.933 | 0.2764 | 0.0816 | 1.318 |
| 15 | Cora | camp2 | [3, 3, 3, 3] | 55.933 | 0.2764 | -0.1173 | 1.120 |
| 15 | Valter | camp3 | [3, 3, 3, 3] | 65.617 | 0.08 | -0.0077 | 0.412 |
| 15 | Valter | camp3 | [3, 3, 3, 3] | 65.617 | 0.08 | 0.0119 | 0.432 |
| 15 | Hugo | camp2 | [3, 3, 3, 3] | 55.933 | 0.2764 | 0.0685 | 1.305 |
| 15 | Hugo | camp2 | [3, 3, 3, 3] | 55.933 | 0.2764 | 0.2385 | 1.475 |
| 15 | Yara | camp3 | [3, 3, 2, 2] | 65.617 | 0.08 | 0.0473 | 0.467 |
| 15 | Yara | camp3 | [2, 3, 3, 4] | 65.617 | 0.0 | 0.013 | 0.013 |
| 16 | Yara | camp3 | [3, 3, 3, 4] | 64.683 | 0.08 | -0.1131 | 0.301 |
| 16 | Yara | camp3 | [3, 3, 2, 2] | 64.683 | 0.08 | -0.0329 | 0.381 |
| 16 | Hugo | camp2 | [3, 3, 3, 3] | 52.203 | 0.2764 | 0.3393 | 1.494 |
| 16 | Hugo | camp2 | [3, 3, 3, 3] | 52.203 | 0.2764 | 0.0366 | 1.191 |
| 16 | Alma | camp3 | [3, 3, 3, 3] | 64.683 | 0.08 | 0.0423 | 0.456 |
| 16 | Alma | camp3 | [3, 3, 3, 3] | 64.683 | 0.08 | 0.0194 | 0.433 |
| 16 | Valter | camp3 | [3, 3, 3, 3] | 64.683 | 0.08 | 0.1192 | 0.533 |
| 16 | Valter | camp3 | [3, 3, 3, 3] | 64.683 | 0.08 | -0.0248 | 0.389 |
| 16 | Cora | camp3 | [3, 3, 3, 3] | 64.683 | 0.08 | -0.0001 | 0.414 |
| 16 | Cora | camp3 | [3, 3, 3, 3] | 64.683 | 0.08 | 0.0694 | 0.483 |
| 17 | Valter | camp3 | [3, 3, 3, 3] | 62.518 | 0.08 | -0.0312 | 0.369 |
| 17 | Valter | camp3 | [3, 3, 3, 3] | 62.518 | 0.08 | -0.0544 | 0.346 |
| 17 | Hugo | camp2 | [3, 3, 3, 3] | 51.024 | 0.2764 | -0.2705 | 0.858 |
| 17 | Hugo | camp2 | [3, 3, 3, 3] | 51.024 | 0.2764 | -0.0296 | 1.099 |
| 17 | Yara | camp3 | [3, 3, 3, 5] | 62.518 | 0.08 | -0.0348 | 0.365 |
| 17 | Yara | camp3 | [3, 3, 2, 3] | 62.518 | 0.08 | 0.0237 | 0.424 |
| 17 | Alma | camp3 | [3, 3, 3, 3] | 62.518 | 0.08 | -0.0189 | 0.381 |
| 17 | Alma | camp3 | [3, 3, 3, 3] | 62.518 | 0.08 | 0.0318 | 0.432 |
| 17 | Cora | camp3 | [3, 3, 3, 3] | 62.518 | 0.08 | -0.016 | 0.384 |
| 17 | Cora | camp3 | [3, 3, 3, 3] | 62.518 | 0.08 | 0.0848 | 0.485 |
| 18 | Valter | camp3 | [3, 3, 3, 3] | 60.589 | 0.08 | -0.1293 | 0.258 |
| 18 | Valter | camp3 | [3, 3, 3, 3] | 60.589 | 0.08 | 0.0283 | 0.416 |
| 18 | Cora | camp3 | [3, 3, 3, 3] | 60.589 | 0.08 | 0.0194 | 0.407 |
| 18 | Cora | camp3 | [3, 3, 3, 3] | 60.589 | 0.08 | 0.0393 | 0.427 |
| 18 | Hugo | camp2 | [3, 3, 3, 3] | 50.576 | 0.2764 | 0.1484 | 1.267 |
| 18 | Hugo | camp1 | [3, 3, 3, 3] | 51.78 | 0.3448 | 0.3268 | 1.755 |
| 18 | Alma | camp3 | [3, 3, 3, 3] | 60.589 | 0.08 | -0.0604 | 0.327 |
| 18 | Alma | camp3 | [3, 3, 3, 3] | 60.589 | 0.08 | -0.0229 | 0.365 |
| 18 | Yara | camp3 | [3, 3, 2, 3] | 60.589 | 0.08 | -0.0035 | 0.384 |
| 18 | Yara | camp3 | [3, 3, 3, 4] | 60.589 | 0.08 | 0.0354 | 0.423 |
| 19 | Cora | camp3 | [3, 3, 3, 3] | 58.862 | 0.08 | 0.0286 | 0.405 |
| 19 | Cora | camp3 | [3, 3, 3, 3] | 58.862 | 0.08 | -0.0247 | 0.352 |
| 19 | Yara | camp3 | [3, 3, 3, 4] | 58.862 | 0.08 | -0.0219 | 0.355 |
| 19 | Yara | camp3 | [3, 3, 3, 3] | 58.862 | 0.08 | -0.0434 | 0.333 |
| 19 | Valter | camp3 | [3, 3, 3, 3] | 58.862 | 0.08 | -0.021 | 0.356 |
| 19 | Valter | camp3 | [3, 3, 3, 3] | 58.862 | 0.08 | -0.061 | 0.316 |
| 19 | Alma | camp3 | [3, 3, 3, 3] | 58.862 | 0.08 | 0.1038 | 0.481 |
| 19 | Alma | camp3 | [3, 3, 3, 3] | 58.862 | 0.08 | -0.0206 | 0.356 |
| 19 | Hugo | camp2 | [3, 3, 3, 3] | 50.818 | 0.2764 | -0.0419 | 1.082 |
| 19 | Hugo | camp1 | [3, 3, 3, 3] | 51.292 | 0.3448 | -0.1246 | 1.290 |
| 20 | Cora | camp3 | [3, 3, 3, 3] | 57.207 | 0.08 | 0.0219 | 0.388 |
| 20 | Cora | camp3 | [3, 3, 3, 3] | 57.207 | 0.08 | -0.0109 | 0.355 |
| 20 | Alma | camp3 | [3, 3, 3, 3] | 57.207 | 0.08 | -0.0674 | 0.299 |
| 20 | Alma | camp3 | [3, 3, 3, 3] | 57.207 | 0.08 | -0.0219 | 0.344 |
| 20 | Hugo | camp2 | [3, 3, 3, 3] | 51.245 | 0.2764 | 0.1085 | 1.242 |
| 20 | Hugo | camp1 | [3, 3, 3, 3] | 51.27 | 0.3448 | 0.1503 | 1.565 |
| 20 | Valter | camp3 | [3, 3, 3, 3] | 57.207 | 0.08 | 0.0142 | 0.380 |
| 20 | Valter | camp3 | [3, 3, 3, 3] | 57.207 | 0.08 | 0.027 | 0.393 |
| 20 | Yara | camp3 | [3, 3, 3, 4] | 57.207 | 0.08 | 0.0507 | 0.417 |
| 20 | Yara | camp3 | [3, 3, 3, 3] | 57.207 | 0.08 | -0.0158 | 0.350 |

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
  enabled: true
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
