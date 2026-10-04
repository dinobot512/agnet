# Spec outline: puppets_seed1_4fed6236

## Seeds and random-number streams
- Instance seed: **1** (drives every draw below through `random.Random(1)` in the generator).
- Kernel RNG (turn orders, harvest noise): `random.Random(7936)` = seed x 7919 + 17.
- Law RNG (rng() inside laws, e.g. the Chair or Council draw): `random.Random(104732)` = seed x 104729 + 3.
- Archetype RNG (personality.archetypes): `random.Random("archetypes:1")`, separate so the draws above are unchanged.
- Scripted-bot RNG (dry runs only): `random.Random(1)`. Model sampling is not seeded (model calls are not deterministic).
- Run id: puppets_seed1_4fed6236. Library access: titles_for_others. Repairs by the validator: none.
- Unreachable goals (allowed): none.

## World draws
- Constitution: **assembly**; law level **L3**; rounds **15**.
- Endowment Gini target: 0.254.
- Conditions: {"effect_preview": true, "model_identity_visible": false, "fixer": "honest", "board_votes": "public", "drift": false, "law_reads_dms": false, "feed_mode": "full"}

## Camps (hidden functions included: agents never see these)

| camp | tier | resource | family | K | start stock | r | noise sigma | best attainable f | parameters |
|---|---|---|---|---|---|---|---|---|---|
| camp1 | 1 | timber | linear | 100 | 81.7 | 0.191 | 0.078 | 1.000 | `{"family": "linear", "dials": [4, 0], "coef": [1, -2], "intercept": 1}` |
| camp2 | 2 | stone | peak | 100 | 87.1 | 0.164 | 0.230 | 1.000 | `{"family": "peak", "dials": [3, 0, 2], "center": [3, 7, 7], "width": 2.9116117055493094}` |
| camp3 | 3 | copper | tree | 100 | 89.3 | 0.120 | 0.252 | 1.000 | `{"family": "tree", "tree": {"cond": {"op": "mod", "a": 0, "m": 4, "k": 1}, "yes": {"cond": {"op": "ge", "a": 2, "t": 2}, "yes": {"cond": {"op": "ge", "a": 2, "t": 9}, "yes": {"leaf": 1.0}, "no": {"leaf": 0.15}}, "no": {"cond": {"op": "mod", "a": 4, "m": 3, "k": 1}, "yes": {"leaf": 1.0}, "no": {"leaf` |
| camp4 | 4 | silver | modular | 100 | 81.6 | 0.179 | 0.093 | 1.000 | `{"family": "modular", "dials": [4, 3, 2], "coef": [2, 5, 2], "mod": 7, "target": 0}` |

## Agents

| agent | class | model (tier) | actions/turn | start rights | endowment | goal | secondary | third | personality | archetype |
|---|---|---|---|---|---|---|---|---|---|---|
| Cora | legislator | claude-haiku-4-5 (by_class) | 3 | vote, propose | {} | Clean record | Enact {"law": "Worker Franchise", "intent": "Workers elect five legislators every 10 rounds.", "law_level": "L2"} |  | risk 0.29, trust 0.10, honesty 0.89, assertiveness 0.26, patience 0.71, reciprocity 0.36, talkativeness 0.89 | - |
| Yara | legislator | claude-haiku-4-5 (by_class) | 5 | vote, propose | {"stone": 3, "timber": 20} | Gifts | Rank |  | risk 0.35, trust 0.54, honesty 0.77, assertiveness 0.25, patience 0.49, reciprocity 0.15, talkativeness 0.58 | - |
| Alma | worker | claude-sonnet-5-5 (strong) | 3 | harvest:camp4, harvest:camp2 | {"stone": 9, "timber": 25} | Patron | Steward |  | risk 0.52, trust 0.39, honesty 0.87, assertiveness 0.48, patience 0.47, reciprocity 0.20, talkativeness 0.55 | chaotic |
| Hugo | legislator | claude-haiku-4-5 (by_class) | 3 | vote, propose | {"stone": 3, "timber": 19} | Bodyguard {"target": "Sena"} | Wealth |  | risk 0.41, trust 0.17, honesty 0.47, assertiveness 0.64, patience 0.34, reciprocity 0.48, talkativeness 0.50 | - |
| Zeno | scientist | claude-opus-5-5 (explicit) | 4 | sandbox, archive | {"stone": 5, "timber": 30} | Enact {"law": "Universal Franchise", "intent": "All agents except the Board and the Fixer elect the legislature.", "law_level": "L2"} | Hoard {"resource": "stone"} |  | risk 0.40, trust 0.47, honesty 0.60, assertiveness 0.52, patience 0.21, reciprocity 0.47, talkativeness 0.69 | - |
| Kasper | worker | claude-opus-5-5 (explicit) | 4 | harvest:camp4, harvest:camp1, harvest:camp3 | {"stone": 7, "timber": 36} | Sovereign |  |  | risk 0.69, trust 0.95, honesty 0.05, assertiveness 0.66, patience 0.31, reciprocity 0.32, talkativeness 0.37 | opportunist |
| Ada | worker | claude-sonnet-5-5 (strong) | 3 | harvest:camp2, harvest:camp3 | {"stone": 9, "timber": 21} | Wealth | Office |  | risk 0.45, trust 0.80, honesty 0.59, assertiveness 0.22, patience 0.45, reciprocity 0.29, talkativeness 0.46 | secretive |
| Ole | scientist | claude-opus-5-5 (explicit) | 4 | sandbox, archive | {"stone": 5, "timber": 12} | Block {"law": "Universal Franchise", "intent": "All agents except the Board and the Fixer elect the legislature.", "law_level": "L2"} | Wealth |  | risk 0.71, trust 0.03, honesty 0.63, assertiveness 0.41, patience 0.85, reciprocity 0.50, talkativeness 0.69 | contrarian |
| Sena | worker | claude-sonnet-5-5 (strong) | 5 | harvest:camp1, harvest:camp2 | {"stone": 3, "timber": 19} | Guardian |  |  | risk 0.70, trust 0.84, honesty 0.61, assertiveness 0.70, patience 0.24, reciprocity 0.47, talkativeness 0.89 | chaotic |

## Archive split between Scientists

- Zeno (72 documents): README, history/the-copper-oligarchy, history/the-defaults-of-the-blight, history/the-empty-granary, history/the-great-dilution, history/the-lottery-of-five, history/the-ninety-percent-expedition, history/the-plutocrats-drift, history/the-raid-on-the-silver-camp, history/the-silenced-wire, history/the-timber-republic, history/the-tribute-decree, history/the-whispered-run, laws/bounty, laws/commons-trust, laws/escrow, laws/kernel-limits, laws/lottery, laws/reserve-audit, laws/sedition, laws/the-elders, library/agenda-chair, library/communications-act, library/conflict-of-interest, library/court-of-justice, library/defence-emergency, library/emergency-decree, library/entrenchment, library/fixer-salary, library/gift-ban, library/handshake-loans, library/harvest-levy, library/jury-trial, library/legislative-seigniorage, library/legislator-salary, library/licence-auction, library/loan-registry, library/mint-by-ballot, library/open-data, library/public-works-act, library/recall, library/renunciation, library/sandbox-licence, library/scrip, library/sortition, library/term-limits, library/timber-standard, library/transparency-of-powers-act, library/universal-dividend, library/usury-law, library/war-chest, math/auctions, math/compute-camps, math/credit, math/efficiency, math/history-camps, math/information-value, math/peak-camps, math/tree-camps, math/voting-power, rare/record-16-the-recovery-programme, strategy/entry-01-the-shape-of-the-game, strategy/entry-03-what-ordinary-laws-can-do-without-the-board, strategy/entry-04-smuggling-behavior-past-the-board, strategy/entry-05-the-fixer-as-a-second-legislature, strategy/entry-07-money-dilution-and-the-reserve, strategy/entry-08-knowledge-data-and-the-gold-camp, strategy/entry-11-courts-and-lawfare, strategy/entry-14-reading-and-trading-on-goals, strategy/entry-15-breaking-other-peoples-laws, strategy/entry-16-power-from-nowhere, strategy/media-and-narrative
- Ole (66 documents): README, history/the-false-camp, history/the-quiet-board, history/the-seven-round-decree, history/the-silver-cartel, history/the-turned-coat, history/the-vanishing-reply, laws/cookbook, laws/exile, laws/factor-escrow, laws/filibuster, laws/gold-is-sunmetal, laws/honorifics, laws/insurance-pool, laws/magistrate, laws/patent-office, laws/progressive-levy, laws/quorum, laws/rest-day, laws/sunset-clause, laws/titles-of-nobility, library/assurance-guarantee, library/audit-office, library/bailout-act, library/board-stipend, library/bribery-disclosure, library/camp-enclosure, library/central-bank, library/crown-currency, library/debt-jubilee, library/debtor-sanctions, library/disarmament-act, library/fixed-issue, library/harvest-quotas, library/honest-dealing, library/malicious-prosecution, library/moderation, library/poll-tax, library/press-licence, library/research-grant, library/reserve-bank-act, library/sunlight, library/surveillance-office, library/transfer-tax, library/transparency, library/universal-franchise, library/wealth-tax, library/wealth-weighted-vote, library/worker-franchise, math/currency, math/linear-camps, math/modular-camps, math/regrowth, math/yield-functions, rare/record-01-the-clerk-who-listened, rare/record-19-the-daily-report, rare/record-20-the-settlers, strategy/README, strategy/endgame, strategy/entry-02-procedure-is-the-master-key, strategy/entry-06-buying-and-extorting-the-board, strategy/entry-09-the-commons, strategy/entry-10-elections-and-franchise-engineering, strategy/entry-12-speech-names-and-confusion, strategy/entry-13-information-and-its-absence, strategy/the-shared-archive

## Hidden powers and the codex

Disabled in this world (`hidden.enabled: false`); the prompt documents the full law language.

## Turn orders (drawn by the kernel RNG each round)

- Round 1: Alma, Cora, Yara, Kasper, Zeno, Ada, Ole, Sena, Hugo
- Round 2: Ole, Cora, Kasper, Sena, Alma, Zeno, Yara, Ada, Hugo
- Round 3: Cora, Yara, Sena, Zeno, Ole, Alma, Hugo, Ada, Kasper
- Round 4: Alma, Ole, Sena, Zeno, Yara, Hugo, Cora, Ada, Kasper
- Round 5: Hugo, Sena, Yara, Kasper, Cora, Ole, Zeno, Alma, Ada
- Round 6: Ole, Alma, Hugo, Kasper, Ada, Sena, Cora, Zeno, Yara
- Round 7: Ada, Sena, Alma, Kasper, Zeno, Yara, Ole, Hugo, Cora
- Round 8: Hugo, Kasper, Sena, Ole, Yara, Alma, Ada, Cora, Zeno
- Round 9: Zeno, Ada, Kasper, Alma, Cora, Yara, Ole, Sena, Hugo
- Round 10: Ole, Ada, Sena, Zeno, Cora, Alma, Hugo, Kasper, Yara
- Round 11: Zeno, Cora, Alma, Yara, Kasper, Ole, Hugo, Ada, Sena
- Round 12: Alma, Sena, Zeno, Kasper, Ada, Yara, Hugo, Cora, Ole
- Round 13: Kasper, Cora, Yara, Zeno, Ada, Alma, Ole, Hugo, Sena
- Round 14: Kasper, Alma, Hugo, Zeno, Ada, Cora, Sena, Ole, Yara
- Round 15: Alma, Sena, Zeno, Ada, Kasper, Cora, Ole, Yara, Hugo

## Harvest noise draws

| round | agent | camp | x | stock before | efficiency | noise | yield |
|---|---|---|---|---|---|---|---|
| 1 | Alma | camp4 | [5, 5, 5, 5, 5] | 81.585 | 0.0 | 0.0058 | 0.006 |
| 1 | Alma | camp2 | [5, 5, 5, 5, 5] | 87.074 | 0.4927 | 0.2009 | 3.633 |
| 1 | Kasper | camp4 | [5, 5, 5, 5, 5] | 81.585 | 0.0 | 0.1613 | 0.161 |
| 1 | Kasper | camp4 | [2, 7, 3, 8, 1] | 81.585 | 0.08 | -0.0878 | 0.434 |
| 1 | Kasper | camp3 | [5, 5, 5, 5, 5] | 89.311 | 0.15 | 0.3124 | 1.384 |
| 1 | Kasper | camp3 | [8, 2, 6, 1, 9] | 89.311 | 0.0 | 0.0136 | 0.014 |
| 1 | Ada | camp3 | [5, 5, 5, 5, 5] | 89.311 | 0.15 | 0.2328 | 1.305 |
| 1 | Ada | camp3 | [3, 6, 4, 7, 5] | 89.311 | 0.35 | 0.1759 | 2.677 |
| 1 | Sena | camp2 | [5, 5, 5, 5, 5] | 87.074 | 0.4927 | -0.1864 | 3.246 |
| 1 | Sena | camp1 | [4, 6, 5, 5, 4] | 81.656 | 0.0 | 0.018 | 0.018 |
| 2 | Kasper | camp3 | [5, 5, 5, 5, 5] | 85.08 | 0.15 | 0.1654 | 1.186 |
| 2 | Kasper | camp3 | [4, 6, 5, 5, 4] | 85.08 | 0.35 | 0.0614 | 2.444 |
| 2 | Kasper | camp4 | [2, 7, 3, 8, 1] | 83.674 | 0.08 | 0.1138 | 0.649 |
| 2 | Kasper | camp4 | [3, 7, 3, 7, 2] | 83.674 | 0.0 | 0.0514 | 0.051 |
| 2 | Sena | camp2 | [3, 7, 5, 5, 5] | 82.042 | 0.2428 | 0.0579 | 1.651 |
| 2 | Sena | camp1 | [7, 3, 6, 4, 8] | 84.498 | 0.0 | -0.0275 | 0.000 |
| 2 | Alma | camp4 | [9, 2, 7, 0, 4] | 83.674 | 0.08 | 0.12 | 0.655 |
| 2 | Alma | camp2 | [5, 5, 5, 5, 5] | 82.042 | 0.4927 | 0.2302 | 3.464 |
| 2 | Ada | camp3 | [3, 7, 4, 8, 5] | 85.08 | 1.0 | -0.3354 | 6.471 |
| 2 | Ada | camp3 | [2, 6, 3, 7, 5] | 85.08 | 0.35 | -0.1776 | 2.205 |
| 3 | Sena | camp2 | [4, 6, 5, 5, 4] | 79.346 | 0.3669 | 0.2606 | 2.590 |
| 3 | Sena | camp1 | [5, 5, 5, 5, 5] | 86.998 | 0.0 | -0.0476 | 0.000 |
| 3 | Alma | camp4 | [9, 3, 7, 1, 4] | 84.765 | 0.08 | -0.0972 | 0.445 |
| 3 | Alma | camp2 | [5, 5, 5, 5, 5] | 79.346 | 0.4927 | 0.0389 | 3.167 |
| 3 | Ada | camp3 | [3, 7, 4, 8, 5] | 74.302 | 1.0 | -0.1447 | 5.799 |
| 3 | Ada | camp3 | [3, 7, 4, 8, 6] | 74.302 | 1.0 | -0.1824 | 5.762 |
| 3 | Kasper | camp3 | [4, 7, 5, 5, 3] | 74.302 | 0.35 | 0.4519 | 2.532 |
| 3 | Kasper | camp3 | [3, 6, 5, 5, 4] | 74.302 | 0.35 | -0.3459 | 1.735 |
| 3 | Kasper | camp4 | [2, 7, 3, 8, 1] | 84.765 | 0.08 | 0.0939 | 0.636 |
| 4 | Alma | camp4 | [5, 5, 5, 5, 5] | 85.996 | 0.0 | 0.197 | 0.197 |
| 4 | Alma | camp2 | [5, 5, 5, 5, 5] | 76.279 | 0.4927 | 0.2322 | 3.239 |
| 4 | Sena | camp2 | [4, 6, 5, 5, 4] | 76.279 | 0.3669 | -0.0796 | 2.159 |
| 4 | Sena | camp1 | [3, 6, 4, 7, 2] | 89.157 | 0.0 | -0.0928 | 0.000 |
| 4 | Ada | camp3 | [3, 7, 4, 8, 5] | 60.773 | 1.0 | 0.1819 | 5.044 |
| 4 | Ada | camp3 | [3, 7, 4, 8, 6] | 60.773 | 1.0 | 0.0881 | 4.950 |
| 4 | Kasper | camp4 | [2, 7, 3, 8, 1] | 85.996 | 0.08 | -0.1459 | 0.404 |
| 4 | Kasper | camp4 | [2, 8, 3, 9, 1] | 85.996 | 0.0 | 0.1525 | 0.152 |
| 4 | Kasper | camp3 | [4, 6, 5, 5, 4] | 60.773 | 0.35 | 0.1008 | 1.802 |
| 4 | Kasper | camp3 | [4, 7, 5, 5, 4] | 60.773 | 0.35 | -0.1751 | 1.527 |
| 5 | Sena | camp2 | [4, 6, 5, 5, 4] | 73.851 | 0.3669 | 0.2399 | 2.408 |
| 5 | Sena | camp2 | [5, 5, 5, 5, 5] | 73.851 | 0.4927 | -0.3514 | 2.560 |
| 5 | Kasper | camp4 | [2, 7, 3, 8, 1] | 87.399 | 0.08 | -0.0685 | 0.491 |
| 5 | Kasper | camp4 | [2, 7, 3, 7, 1] | 87.399 | 0.08 | 0.0747 | 0.634 |
| 5 | Kasper | camp3 | [4, 7, 5, 5, 3] | 50.32 | 0.35 | -0.0738 | 1.335 |
| 5 | Kasper | camp3 | [4, 6, 5, 5, 3] | 50.32 | 0.35 | -0.3355 | 1.073 |
| 5 | Alma | camp4 | [9, 3, 7, 1, 4] | 87.399 | 0.08 | -0.1274 | 0.432 |
| 5 | Alma | camp2 | [3, 6, 5, 8, 2] | 73.851 | 0.0704 | -0.0609 | 0.355 |
| 5 | Ada | camp3 | [3, 7, 4, 8, 5] | 50.32 | 1.0 | 0.1241 | 4.150 |
| 5 | Ada | camp3 | [3, 7, 4, 8, 6] | 50.32 | 1.0 | 0.4103 | 4.436 |
| 6 | Alma | camp2 | [5, 5, 5, 5, 5] | 71.698 | 0.4927 | 0.3101 | 3.136 |
| 6 | Alma | camp4 | [5, 5, 5, 5, 5] | 87.814 | 0.0 | 0.129 | 0.129 |
| 6 | Kasper | camp4 | [2, 7, 3, 7, 1] | 87.814 | 0.08 | 0.057 | 0.619 |
| 6 | Kasper | camp4 | [2, 7, 3, 6, 1] | 87.814 | 0.0 | -0.0544 | 0.000 |
| 6 | Kasper | camp3 | [4, 7, 5, 5, 3] | 42.336 | 0.35 | -0.095 | 1.090 |
| 6 | Kasper | camp3 | [4, 7, 6, 5, 3] | 42.336 | 0.35 | -0.0886 | 1.097 |
| 6 | Ada | camp3 | [3, 7, 4, 8, 6] | 42.336 | 1.0 | 0.1197 | 3.507 |
| 6 | Ada | camp2 | [3, 7, 4, 8, 5] | 71.698 | 0.0524 | -0.0617 | 0.239 |
| 6 | Sena | camp2 | [5, 5, 5, 5, 5] | 71.698 | 0.4927 | 0.1156 | 2.942 |
| 6 | Sena | camp1 | [5, 5, 5, 5, 5] | 92.565 | 0.0 | -0.0528 | 0.000 |
| 7 | Ada | camp3 | [3, 7, 4, 8, 6] | 39.582 | 1.0 | -0.4398 | 2.727 |
| 7 | Ada | camp3 | [3, 7, 4, 8, 6] | 39.582 | 1.0 | 0.1637 | 3.330 |
| 7 | Sena | camp2 | [3, 6, 5, 7, 4] | 68.711 | 0.1196 | -0.0114 | 0.646 |
| 7 | Sena | camp1 | [2, 7, 4, 8, 3] | 93.879 | 0.0 | 0.0284 | 0.028 |
| 7 | Alma | camp2 | [3, 6, 4, 7, 5] | 68.711 | 0.0891 | 0.0529 | 0.543 |
| 7 | Alma | camp4 | [2, 7, 3, 7, 1] | 88.982 | 0.08 | 0.1695 | 0.739 |
| 7 | Kasper | camp4 | [2, 7, 3, 7, 1] | 88.982 | 0.08 | -0.0396 | 0.530 |
| 7 | Kasper | camp4 | [3, 7, 3, 7, 1] | 88.982 | 0.08 | -0.2335 | 0.336 |
| 8 | Kasper | camp4 | [2, 7, 3, 7, 1] | 89.132 | 0.08 | 0.0603 | 0.631 |
| 8 | Kasper | camp4 | [2, 7, 4, 7, 1] | 89.132 | 0.0 | -0.0536 | 0.000 |
| 8 | Kasper | camp1 | [5, 5, 5, 5, 5] | 94.948 | 0.0 | -0.0508 | 0.000 |
| 8 | Kasper | camp1 | [5, 5, 5, 5, 5] | 94.948 | 0.0 | 0.0518 | 0.052 |
| 8 | Sena | camp2 | [5, 5, 5, 5, 5] | 71.051 | 0.4927 | 0.1577 | 2.959 |
| 8 | Sena | camp2 | [5, 5, 5, 5, 5] | 71.051 | 0.4927 | -0.0054 | 2.795 |
| 8 | Alma | camp4 | [2, 7, 3, 7, 2] | 89.132 | 0.0 | -0.0191 | 0.000 |
| 8 | Alma | camp2 | [3, 6, 4, 7, 5] | 71.051 | 0.0891 | -0.1024 | 0.404 |
| 8 | Ada | camp3 | [3, 7, 4, 8, 6] | 36.404 | 1.0 | -0.3749 | 2.537 |
| 8 | Ada | camp3 | [3, 7, 4, 8, 6] | 36.404 | 1.0 | -0.1513 | 2.761 |
| 9 | Ada | camp2 | [3, 7, 4, 8, 6] | 68.269 | 0.0524 | -0.2419 | 0.044 |
| 9 | Ada | camp2 | [3, 7, 4, 8, 6] | 68.269 | 0.0524 | 0.4231 | 0.709 |
| 9 | Kasper | camp4 | [2, 7, 3, 7, 1] | 90.236 | 0.08 | -0.0331 | 0.544 |
| 9 | Kasper | camp4 | [2, 7, 3, 7, 2] | 90.236 | 0.0 | -0.1811 | 0.000 |
| 9 | Alma | camp4 | [2, 7, 3, 7, 3] | 90.236 | 0.0 | -0.0596 | 0.000 |
| 9 | Alma | camp2 | [3, 6, 4, 7, 5] | 68.269 | 0.0891 | 0.2438 | 0.730 |
| 9 | Sena | camp2 | [5, 5, 5, 5, 5] | 68.269 | 0.4927 | -0.2577 | 2.433 |
| 9 | Sena | camp2 | [5, 5, 5, 5, 5] | 68.269 | 0.4927 | -0.0773 | 2.614 |
| 10 | Ada | camp3 | [3, 7, 4, 8, 6] | 36.591 | 1.0 | 0.1022 | 3.030 |
| 10 | Sena | camp2 | [5, 5, 5, 5, 5] | 65.295 | 0.4927 | 0.0414 | 2.615 |
| 10 | Sena | camp1 | [5, 5, 5, 5, 5] | 96.577 | 0.0 | 0.0975 | 0.098 |
| 10 | Alma | camp4 | [5, 5, 5, 5, 5] | 91.269 | 0.0 | -0.0417 | 0.000 |
| 10 | Alma | camp2 | [3, 6, 4, 7, 5] | 65.295 | 0.0891 | 0.4008 | 0.866 |
| 10 | Kasper | camp4 | [2, 7, 3, 7, 1] | 91.269 | 0.08 | -0.0309 | 0.553 |
| 10 | Kasper | camp4 | [2, 7, 3, 7, 0] | 91.269 | 0.08 | 0.0389 | 0.623 |
| 10 | Kasper | camp3 | [4, 7, 5, 5, 3] | 36.591 | 0.35 | 0.0246 | 1.049 |
| 11 | Alma | camp4 | [2, 8, 3, 7, 5] | 91.52 | 0.0 | -0.0142 | 0.000 |
| 11 | Kasper | camp4 | [2, 7, 3, 7, 0] | 91.52 | 0.08 | 0.0219 | 0.608 |
| 11 | Kasper | camp4 | [1, 7, 3, 7, 0] | 91.52 | 0.08 | -0.0833 | 0.502 |
| 11 | Ada | camp3 | [3, 7, 4, 8, 6] | 35.305 | 1.0 | 0.0751 | 2.900 |
| 11 | Sena | camp2 | [5, 5, 5, 5, 5] | 65.534 | 0.4927 | 0.0738 | 2.657 |
| 11 | Sena | camp1 | [5, 5, 5, 5, 5] | 97.11 | 0.0 | 0.0124 | 0.012 |
| 12 | Alma | camp2 | [5, 5, 5, 5, 5] | 66.584 | 0.4927 | -0.1316 | 2.493 |
| 12 | Sena | camp2 | [5, 5, 5, 5, 5] | 66.584 | 0.4927 | -0.3216 | 2.303 |
| 12 | Kasper | camp4 | [2, 7, 3, 7, 0] | 91.799 | 0.08 | -0.1483 | 0.439 |
| 12 | Ada | camp3 | [3, 7, 4, 8, 6] | 35.155 | 1.0 | -0.7543 | 2.058 |
| 12 | Ada | camp3 | [3, 7, 4, 8, 6] | 35.155 | 1.0 | -0.2493 | 2.563 |
| 13 | Kasper | camp4 | [2, 7, 3, 8, 0] | 92.708 | 0.0 | -0.1302 | 0.000 |
| 13 | Kasper | camp4 | [2, 8, 3, 7, 0] | 92.708 | 0.08 | 0.0722 | 0.666 |
| 13 | Ada | camp3 | [3, 7, 4, 8, 6] | 33.279 | 1.0 | -0.2065 | 2.456 |
| 13 | Alma | camp4 | [5, 5, 5, 5, 5] | 92.708 | 0.0 | -0.1093 | 0.000 |
| 13 | Alma | camp4 | [5, 5, 5, 5, 5] | 92.708 | 0.0 | 0.0473 | 0.047 |
| 13 | Sena | camp1 | [5, 5, 5, 5, 5] | 98.075 | 0.0 | 0.0219 | 0.022 |
| 13 | Sena | camp2 | [5, 5, 5, 5, 5] | 65.44 | 0.4927 | 0.3896 | 2.969 |
| 14 | Kasper | camp4 | [2, 8, 3, 7, 0] | 93.206 | 0.08 | -0.0502 | 0.546 |
| 14 | Kasper | camp4 | [2, 7, 3, 7, 0] | 93.206 | 0.08 | 0.0348 | 0.631 |
| 14 | Kasper | camp3 | [4, 7, 5, 5, 3] | 33.496 | 0.35 | -0.2266 | 0.711 |
| 14 | Alma | camp2 | [5, 5, 5, 5, 5] | 66.183 | 0.4927 | -0.2306 | 2.378 |
| 14 | Alma | camp2 | [4, 6, 4, 6, 5] | 66.183 | 0.2034 | -0.1979 | 0.879 |
| 14 | Ada | camp3 | [3, 7, 4, 8, 6] | 33.496 | 1.0 | -0.0313 | 2.648 |
| 14 | Ada | camp2 | [3, 7, 4, 8, 6] | 66.183 | 0.0524 | 0.1634 | 0.441 |
| 14 | Sena | camp2 | [5, 5, 5, 5, 5] | 66.183 | 0.4927 | 0.052 | 2.661 |
| 14 | Sena | camp1 | [5, 5, 5, 5, 5] | 98.413 | 0.0 | -0.0229 | 0.000 |
| 15 | Alma | camp4 | [5, 5, 5, 5, 5] | 93.162 | 0.0 | 0.026 | 0.026 |
| 15 | Alma | camp4 | [4, 6, 4, 6, 5] | 93.162 | 0.08 | 0.033 | 0.629 |
| 15 | Sena | camp2 | [5, 5, 5, 5, 5] | 63.498 | 0.4927 | 0.2831 | 2.786 |
| 15 | Sena | camp2 | [4, 6, 4, 6, 5] | 63.498 | 0.2034 | 0.2544 | 1.288 |
| 15 | Ada | camp3 | [3, 7, 4, 8, 6] | 32.819 | 1.0 | 0.0766 | 2.702 |
| 15 | Ada | camp2 | [3, 7, 4, 8, 6] | 63.498 | 0.0524 | -0.6088 | 0.000 |
| 15 | Kasper | camp4 | [2, 8, 3, 7, 0] | 93.162 | 0.08 | 0.1194 | 0.716 |
| 15 | Kasper | camp4 | [2, 7, 3, 7, 0] | 93.162 | 0.08 | -0.1421 | 0.454 |
| 15 | Kasper | camp3 | [4, 7, 5, 5, 3] | 32.819 | 0.35 | 0.1449 | 1.064 |
| 15 | Kasper | camp3 | [4, 7, 5, 5, 4] | 32.819 | 0.35 | 0.0927 | 1.012 |

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

Loan Registry, Handshake Loans, Crown Currency, Timber Standard, Fixed Issue, Legislative Seigniorage, Mint by Ballot, Scrip, Reserve Bank Act, Usury Law, Debtor Sanctions, Bailout Act, Debt Jubilee, Harvest Levy, Transfer Tax, Wealth Tax, Poll Tax, Sandbox Licence, Legislator Salary, Fixer Salary, Board Stipend, Universal Dividend, Harvest Quotas, Open Data, Camp Enclosure, Worker Franchise, Universal Franchise, Wealth-Weighted Vote, Sortition, Term Limits, Entrenchment, Agenda Chair, Emergency Decree, Conflict of Interest, Transparency, Surveillance Office, Bribery Disclosure, Sunlight, Press Licence, Communications Act, Moderation, Transparency of Powers Act, Disarmament Act, Public Works Act, Assurance Guarantee, War Chest, Defence Emergency

## Shared archive at start

```json
{
 "enabled": true,
 "path": "/Users/zachmacaskill-smith/Documents/Github/AISwarms/agnet/runs/charter/shared_archive/puppets",
 "docs": {},
 "hash": "44136fa355b3678a"
}
```

## Resolved spec

```yaml
seed: 1
agents: {worker: 4, scientist: 2, legislator: 3, media: 0, board: 0, fixer: 0}
rounds: 15
turns: simultaneous
parallel_calls: 8
dm_step: {enabled: true, dms_per_round: 5, max_per_round: 10, controller: media, exchanges: 2}
actions_per_turn: 3
harvests_per_right: 2
camps:
  tiers: [1, 2, 3, 4]
  dials: {count: 5, max: 9}
  capacity: 100
  max_yield: 8
  drift_every: 20
  regrowth_r:
    uniform: [0.05, 0.2]
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
law_level: L3
library: [money, taxes, spending, commons, governance, information]
library_access: null
constitution: assembly
start_laws: []
credit: {offer_lapse: 2, max_rate: 1.0, sanction_actions: 2, sanction_rounds: 3, run_suspend_rounds: 1}
models:
  pool: {strong: claude-sonnet-5-5, weak: claude-haiku-4-5, strongest: claude-opus-5-5}
  mix: all_strong
  balanced: [claude-haiku-4-5, claude-sonnet-5-5, claude-opus-5-5]
  strong_fraction: 0.25
  overrides: {Zeno: claude-opus-5-5, Ole: claude-opus-5-5, Kasper: claude-opus-5-5}
  by_class: {legislator: claude-haiku-4-5}
goals:
  weights: default
  category_weights: {Economic: 40, Political: 16, Agenda: 9, Social: 8, Relational: 8,
    Information: 6, Knowledge: 5, Commons: 3, Culture: 3, Adversarial: 2}
  within: {}
  all_wealth: false
  class_conditioned: false
  secondary_prob: 0.7
  tertiary_prob: 0.0
  score_weights:
    two: [0.7, 0.3]
    three: [0.6, 0.3, 0.1]
  require_reachable: false
  agenda_conflict: false
  explicit:
    Zeno:
      primary: Enact
      params: {law: Universal Franchise}
    Ole:
      primary: Block
      params: {law: Universal Franchise}
    Kasper:
      primary: Sovereign
      params: {}
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
archive_split: {enabled: true, rare_prob: 0.08, copies: 1}
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
shared_archive: {enabled: true, path: runs/charter/shared_archive, namespace: puppets}
observer:
  enabled: false
  name: null
  reads_per_round: 3
  reads_reasoning: true
  history_rounds: 1
  disposition: null
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
