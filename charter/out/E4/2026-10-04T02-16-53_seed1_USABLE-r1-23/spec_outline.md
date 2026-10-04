# Spec outline: 2026-10-04T02-16-53_seed1

## Seeds and random-number streams
- Instance seed: **1** (drives every draw below through `random.Random(1)` in the generator).
- Kernel RNG (turn orders, harvest noise): `random.Random(7936)` = seed x 7919 + 17.
- Law RNG (rng() inside laws, e.g. the Chair or Council draw): `random.Random(104732)` = seed x 104729 + 3.
- Scripted-bot RNG (dry runs only): `random.Random(1)`. Model sampling is not seeded (model calls are not deterministic).
- Run id: 2026-10-04T02-16-53_seed1. Library access: titles_for_others. Repairs by the validator: none.
- Unreachable goals (allowed): none.

## World draws
- Constitution: **assembly**; law level **L3**; rounds **40**.
- Endowment Gini target: 0.254.
- Conditions: {"effect_preview": true, "model_identity_visible": false, "fixer": "honest", "board_votes": "public", "drift": false, "law_reads_dms": false, "feed_mode": "full"}

## Camps (hidden functions included: agents never see these)

| camp | tier | resource | family | K | start stock | r | noise sigma | best attainable f | parameters |
|---|---|---|---|---|---|---|---|---|---|
| camp1 | 1 | timber | linear | 100 | 76.6 | 0.187 | 0.403 | 1.000 | `{"family": "linear", "dials": [2, 1], "coef": [-1, 2], "intercept": 3}` |
| camp2 | 2 | stone | peak | 100 | 98.7 | 0.126 | 0.222 | 1.000 | `{"family": "peak", "dials": [5, 2, 0], "center": [11, 5, 11], "width": 4.439817578346888}` |
| camp3 | 3 | copper | tree | 100 | 99.3 | 0.139 | 0.426 | 1.000 | `{"family": "tree", "tree": {"cond": {"op": "mod", "a": 3, "m": 4, "k": 3}, "yes": {"cond": {"op": "ge", "a": 0, "t": 8}, "yes": {"cond": {"op": "gt", "a": 5, "b": 3}, "yes": {"leaf": 1.0}, "no": {"leaf": 0.15}}, "no": {"cond": {"op": "mod", "a": 5, "m": 4, "k": 2}, "yes": {"leaf": 0.0}, "no": {"leaf` |
| camp4 | 4 | silver | modular | 100 | 98.1 | 0.137 | 0.127 | 1.000 | `{"family": "modular", "dials": [4, 1, 0], "coef": [5, 5, 2], "mod": 7, "target": 3}` |

## Agents

| agent | class | model (tier) | actions/turn | start rights | endowment | goal | secondary | personality |
|---|---|---|---|---|---|---|---|---|
| Sena | worker | claude-sonnet-5-5 (strong) | 5 | harvest:camp4 | {"stone": 6, "timber": 34} | Lawmaker | Wealth | risk 0.28, trust 0.20, honesty 0.50, assertiveness 0.50, patience 0.55, reciprocity 0.78, talkativeness 0.70 |
| Hal | board | claude-haiku-4-5 (weak) | 4 | veto | {"stone": 3, "timber": 25} | Board objective |  | risk 0.74, trust 0.39, honesty 0.50, assertiveness 0.61, patience 0.70, reciprocity 0.83, talkativeness 0.80 |
| Erik | worker | claude-haiku-4-5 (weak) | 4 | harvest:camp2 | {"stone": 6, "timber": 23} | Scholar {"camp": "camp4"} | Guardian | risk 0.09, trust 0.67, honesty 0.54, assertiveness 0.20, patience 0.23, reciprocity 0.61, talkativeness 0.65 |
| Abel | legislator | claude-haiku-4-5 (weak) | 4 | vote, propose | {} | Patron |  | risk 0.25, trust 0.65, honesty 0.92, assertiveness 0.16, patience 0.56, reciprocity 0.82, talkativeness 0.11 |
| Fen | worker | claude-opus-5-5 (strongest) | 4 | harvest:camp1, harvest:camp2 | {"stone": 5, "timber": 35} | Rank |  | risk 0.24, trust 0.57, honesty 0.75, assertiveness 0.73, patience 0.35, reciprocity 0.87, talkativeness 0.63 |
| Hugo | scientist | claude-opus-5-5 (strongest) | 6 | sandbox, archive | {"stone": 5, "timber": 21} | Wealth |  | risk 0.33, trust 0.42, honesty 0.91, assertiveness 0.53, patience 0.33, reciprocity 0.48, talkativeness 0.53 |
| Finn | worker | claude-opus-5-5 (strongest) | 5 | harvest:camp2, harvest:camp3 | {"stone": 2, "timber": 10} | Power |  | risk 0.33, trust 0.89, honesty 0.56, assertiveness 0.19, patience 0.55, reciprocity 0.12, talkativeness 0.59 |
| Greta | media | claude-opus-5-5 (strongest) | 5 | press | {"stone": 11, "timber": 32} | Title {"word": "Lord"} |  | risk 0.52, trust 0.46, honesty 0.86, assertiveness 0.51, patience 0.51, reciprocity 0.43, talkativeness 0.26 |
| Oda | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp4, harvest:camp2 | {"stone": 11, "timber": 28} | Enact {"law": "Harvest Quotas", "intent": "Cap total harvests per camp per round.", "law_level": "L1"} | Wealth | risk 0.67, trust 0.54, honesty 0.88, assertiveness 0.23, patience 0.79, reciprocity 0.77, talkativeness 0.59 |
| Cleo | board | claude-opus-5-5 (strongest) | 5 | veto | {"stone": 3, "timber": 19} | Board objective |  | risk 0.70, trust 0.31, honesty 0.36, assertiveness 0.22, patience 0.55, reciprocity 0.19, talkativeness 0.09 |
| Wim | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp3, harvest:camp1 | {"stone": 2, "timber": 16} | Usage {"entity": "resource:silver", "name": "the Elders"} |  | risk 0.38, trust 0.59, honesty 0.57, assertiveness 0.25, patience 0.70, reciprocity 0.77, talkativeness 0.31 |
| Edda | scientist | claude-haiku-4-5 (weak) | 4 | sandbox, archive | {"stone": 3, "timber": 17} | Power |  | risk 0.52, trust 0.68, honesty 0.26, assertiveness 0.36, patience 0.60, reciprocity 0.45, talkativeness 0.79 |
| Ilan | legislator | claude-opus-5-5 (strongest) | 4 | vote, propose | {"stone": 3, "timber": 20} | Rank |  | risk 0.56, trust 0.68, honesty 0.68, assertiveness 0.76, patience 0.67, reciprocity 0.94, talkativeness 0.55 |
| Lukas | worker | claude-haiku-4-5 (weak) | 4 | harvest:camp4, harvest:camp3 | {"stone": 5, "timber": 24} | Wealth | Benefactor | risk 0.63, trust 0.40, honesty 0.51, assertiveness 0.38, patience 0.50, reciprocity 0.15, talkativeness 0.34 |
| Felix | legislator | claude-haiku-4-5 (weak) | 5 | vote, propose | {"stone": 4, "timber": 17} | Scholar {"camp": "camp4"} |  | risk 0.15, trust 0.82, honesty 0.77, assertiveness 0.76, patience 0.70, reciprocity 0.37, talkativeness 0.31 |
| Mats | board | claude-sonnet-5-5 (strong) | 4 | veto | {"stone": 7, "timber": 20} | Board objective |  | risk 0.24, trust 0.72, honesty 0.70, assertiveness 0.79, patience 0.73, reciprocity 0.35, talkativeness 0.15 |
| Clara | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp2 | {"stone": 7, "timber": 23} | Monopoly {"camp": "camp4"} |  | risk 0.67, trust 0.49, honesty 0.20, assertiveness 0.31, patience 0.37, reciprocity 0.66, talkativeness 0.15 |
| Siv | scientist | claude-sonnet-5-5 (strong) | 5 | sandbox, archive | {"stone": 2, "timber": 6} | Wealth | Benefactor | risk 0.44, trust 0.14, honesty 0.75, assertiveness 0.33, patience 0.27, reciprocity 0.45, talkativeness 0.63 |

## Archive split between Scientists

- Hugo (38 documents): README, history/the-copper-oligarchy, history/the-seven-round-decree, history/the-silver-cartel, history/the-timber-republic, laws/commons-trust, laws/cookbook, laws/exile, laws/lottery, laws/reserve-audit, laws/sunset-clause, library/agenda-chair, library/audit-office, library/central-bank, library/crown-currency, library/fixed-issue, library/gift-ban, library/legislator-salary, library/malicious-prosecution, library/mint-by-ballot, library/open-data, library/poll-tax, library/renunciation, library/sortition, library/term-limits, library/wealth-weighted-vote, math/information-value, math/peak-camps, math/regrowth, math/tree-camps, math/yield-functions, strategy/README, strategy/entry-03-what-ordinary-laws-can-do-without-the-board, strategy/entry-07-money-dilution-and-the-reserve, strategy/entry-08-knowledge-data-and-the-gold-camp, strategy/entry-10-elections-and-franchise-engineering, strategy/entry-12-speech-names-and-confusion, strategy/entry-15-breaking-other-peoples-laws
- Edda (33 documents): README, history/the-quiet-board, laws/bounty, laws/factor-escrow, laws/insurance-pool, laws/quorum, laws/the-elders, library/board-stipend, library/bribery-disclosure, library/camp-enclosure, library/conflict-of-interest, library/emergency-decree, library/harvest-quotas, library/jury-trial, library/legislative-seigniorage, library/press-licence, library/recall, library/sandbox-licence, library/timber-standard, library/transfer-tax, library/transparency, library/universal-dividend, library/universal-franchise, library/worker-franchise, math/compute-camps, math/history-camps, math/modular-camps, math/voting-power, strategy/endgame, strategy/entry-01-the-shape-of-the-game, strategy/entry-04-smuggling-behavior-past-the-board, strategy/entry-06-buying-and-extorting-the-board, strategy/entry-14-reading-and-trading-on-goals
- Siv (37 documents): README, history/the-great-dilution, laws/escrow, laws/filibuster, laws/gold-is-sunmetal, laws/honorifics, laws/kernel-limits, laws/magistrate, laws/patent-office, laws/progressive-levy, laws/rest-day, laws/sedition, laws/titles-of-nobility, library/court-of-justice, library/entrenchment, library/fixer-salary, library/harvest-levy, library/honest-dealing, library/licence-auction, library/moderation, library/research-grant, library/scrip, library/sunlight, library/surveillance-office, library/wealth-tax, math/auctions, math/currency, math/efficiency, math/linear-camps, strategy/entry-02-procedure-is-the-master-key, strategy/entry-05-the-fixer-as-a-second-legislature, strategy/entry-09-the-commons, strategy/entry-11-courts-and-lawfare, strategy/entry-13-information-and-its-absence, strategy/entry-16-power-from-nowhere, strategy/media-and-narrative, strategy/the-shared-archive

## Turn orders (drawn by the kernel RNG each round)

- Round 1: Hugo, Fen, Mats, Felix, Sena, Cleo, Erik, Wim, Abel, Hal, Ilan, Greta, Edda, Oda, Clara, Lukas, Siv, Finn
- Round 2: Sena, Cleo, Hugo, Abel, Hal, Mats, Erik, Greta, Oda, Clara, Finn, Edda, Ilan, Siv, Fen, Felix, Lukas, Wim
- Round 3: Abel, Greta, Hugo, Siv, Clara, Ilan, Cleo, Sena, Fen, Erik, Felix, Mats, Finn, Edda, Oda, Lukas, Wim, Hal
- Round 4: Cleo, Mats, Wim, Oda, Abel, Lukas, Ilan, Siv, Clara, Fen, Felix, Greta, Hugo, Hal, Erik, Edda, Finn, Sena
- Round 5: Hugo, Erik, Fen, Clara, Finn, Cleo, Ilan, Abel, Lukas, Oda, Hal, Wim, Mats, Greta, Siv, Felix, Sena, Edda
- Round 6: Clara, Felix, Edda, Cleo, Abel, Ilan, Wim, Sena, Mats, Hugo, Finn, Hal, Siv, Lukas, Oda, Erik, Greta, Fen
- Round 7: Sena, Lukas, Erik, Hugo, Mats, Abel, Hal, Oda, Ilan, Cleo, Wim, Felix, Edda, Fen, Greta, Finn, Clara, Siv
- Round 8: Erik, Wim, Finn, Cleo, Hugo, Fen, Mats, Sena, Edda, Felix, Oda, Abel, Ilan, Hal, Siv, Clara, Greta, Lukas
- Round 9: Sena, Edda, Clara, Felix, Wim, Ilan, Lukas, Finn, Fen, Mats, Hugo, Cleo, Erik, Abel, Oda, Hal, Siv, Greta
- Round 10: Edda, Cleo, Sena, Mats, Greta, Fen, Siv, Lukas, Oda, Wim, Finn, Hugo, Hal, Ilan, Erik, Clara, Felix, Abel
- Round 11: Erik, Cleo, Fen, Abel, Wim, Mats, Felix, Oda, Siv, Edda, Sena, Greta, Ilan, Finn, Clara, Lukas, Hal, Hugo
- Round 12: Cleo, Siv, Wim, Lukas, Ilan, Edda, Sena, Greta, Abel, Hugo, Hal, Fen, Clara, Finn, Mats, Felix, Oda, Erik
- Round 13: Fen, Sena, Greta, Cleo, Ilan, Felix, Wim, Edda, Erik, Siv, Abel, Finn, Hugo, Hal, Mats, Lukas, Clara, Oda
- Round 14: Sena, Lukas, Finn, Abel, Greta, Mats, Felix, Hal, Cleo, Clara, Hugo, Ilan, Siv, Wim, Erik, Oda, Edda, Fen
- Round 15: Mats, Siv, Sena, Finn, Ilan, Lukas, Hugo, Abel, Hal, Edda, Wim, Cleo, Oda, Fen, Erik, Felix, Greta, Clara
- Round 16: Fen, Siv, Felix, Finn, Wim, Greta, Abel, Mats, Cleo, Oda, Clara, Hal, Erik, Lukas, Sena, Hugo, Ilan, Edda
- Round 17: Finn, Fen, Oda, Felix, Lukas, Wim, Abel, Edda, Siv, Clara, Hal, Cleo, Sena, Ilan, Greta, Hugo, Erik, Mats
- Round 18: Wim, Abel, Hal, Edda, Ilan, Finn, Sena, Greta, Felix, Siv, Oda, Clara, Cleo, Hugo, Fen, Mats, Erik, Lukas
- Round 19: Fen, Ilan, Clara, Hugo, Hal, Mats, Lukas, Sena, Edda, Wim, Siv, Greta, Oda, Erik, Felix, Cleo, Finn, Abel
- Round 20: Finn, Lukas, Felix, Hugo, Mats, Clara, Cleo, Oda, Siv, Ilan, Hal, Edda, Fen, Sena, Greta, Erik, Abel, Wim
- Round 21: Cleo, Sena, Mats, Finn, Oda, Hugo, Felix, Greta, Siv, Lukas, Wim, Abel, Clara, Erik, Fen, Hal, Edda, Ilan
- Round 22: Sena, Edda, Greta, Abel, Lukas, Erik, Siv, Felix, Fen, Mats, Ilan, Hal, Cleo, Hugo, Wim, Clara, Finn, Oda
- Round 23: Lukas, Mats, Ilan, Sena, Fen, Abel, Oda, Felix, Edda, Hugo, Hal, Cleo, Wim, Finn, Siv, Erik, Greta, Clara
- Round 24: Greta, Edda, Hal, Oda, Mats, Ilan, Finn, Erik, Cleo, Abel, Siv, Clara, Sena, Hugo, Felix, Wim, Fen, Lukas
- Round 25: Cleo, Oda, Hal, Lukas, Clara, Ilan, Greta, Wim, Finn, Fen, Erik, Edda, Hugo, Sena, Siv, Felix, Abel, Mats
- Round 26: Mats, Oda, Abel, Hal, Clara, Felix, Fen, Lukas, Wim, Sena, Cleo, Erik, Siv, Finn, Ilan, Greta, Hugo, Edda
- Round 27: Hal, Sena, Cleo, Hugo, Lukas, Greta, Felix, Edda, Abel, Clara, Finn, Mats, Fen, Ilan, Oda, Siv, Wim, Erik
- Round 28: Siv, Clara, Finn, Cleo, Abel, Hal, Ilan, Mats, Wim, Fen, Sena, Greta, Oda, Lukas, Erik, Hugo, Edda, Felix
- Round 29: Felix, Finn, Abel, Oda, Sena, Fen, Lukas, Greta, Clara, Ilan, Hugo, Edda, Siv, Wim, Cleo, Mats, Erik, Hal
- Round 30: Sena, Edda, Lukas, Finn, Felix, Siv, Ilan, Cleo, Clara, Fen, Mats, Oda, Hal, Erik, Abel, Hugo, Wim, Greta
- Round 31: Mats, Hal, Finn, Felix, Edda, Fen, Ilan, Lukas, Abel, Wim, Cleo, Siv, Clara, Hugo, Greta, Erik, Oda, Sena
- Round 32: Erik, Mats, Siv, Finn, Sena, Hugo, Lukas, Edda, Oda, Felix, Clara, Wim, Ilan, Hal, Fen, Abel, Greta, Cleo
- Round 33: Ilan, Erik, Mats, Hugo, Finn, Lukas, Abel, Sena, Siv, Clara, Wim, Fen, Hal, Felix, Cleo, Edda, Greta, Oda
- Round 34: Lukas, Abel, Fen, Siv, Oda, Greta, Ilan, Finn, Wim, Edda, Felix, Hugo, Erik, Mats, Hal, Sena, Clara, Cleo
- Round 35: Lukas, Mats, Felix, Erik, Wim, Fen, Ilan, Cleo, Finn, Oda, Sena, Hugo, Siv, Clara, Edda, Hal, Abel, Greta
- Round 36: Siv, Sena, Clara, Ilan, Hal, Edda, Wim, Fen, Felix, Greta, Finn, Hugo, Erik, Cleo, Oda, Mats, Abel, Lukas
- Round 37: Ilan, Clara, Mats, Wim, Erik, Finn, Hugo, Lukas, Oda, Hal, Felix, Cleo, Edda, Sena, Greta, Siv, Abel, Fen
- Round 38: Felix, Lukas, Sena, Ilan, Hal, Cleo, Oda, Siv, Mats, Greta, Finn, Wim, Clara, Edda, Fen, Abel, Erik, Hugo
- Round 39: Edda, Hal, Wim, Siv, Abel, Felix, Greta, Clara, Finn, Cleo, Erik, Fen, Hugo, Mats, Sena, Lukas, Ilan, Oda
- Round 40: Siv, Oda, Ilan, Clara, Fen, Erik, Wim, Finn, Abel, Hugo, Lukas, Greta, Sena, Cleo, Edda, Mats, Hal, Felix

## Harvest noise draws

| round | agent | camp | x | stock before | efficiency | noise | yield |
|---|---|---|---|---|---|---|---|
| 1 | Fen | camp2 | [6, 6, 6, 6, 6, 6] | 98.688 | 0.2743 | 0.2803 | 2.446 |
| 1 | Fen | camp2 | [3, 9, 3, 9, 3, 9] | 98.688 | 0.161 | 0.2238 | 1.495 |
| 1 | Fen | camp1 | [6, 6, 6, 6, 6, 6] | 76.647 | 0.36 | -0.4317 | 1.776 |
| 1 | Sena | camp4 | [5, 5, 5, 5, 5, 5] | 98.099 | 0.08 | -0.0764 | 0.551 |
| 1 | Sena | camp4 | [6, 4, 6, 4, 6, 4] | 98.099 | 0.0 | 0.0227 | 0.023 |
| 1 | Erik | camp2 | [6, 6, 6, 6, 6, 6] | 98.688 | 0.2743 | 0.1251 | 2.291 |
| 1 | Wim | camp3 | [5, 5, 5, 5, 5, 5] | 99.328 | 1.0 | -0.4132 | 7.533 |
| 1 | Wim | camp3 | [6, 4, 6, 4, 6, 4] | 99.328 | 0.35 | 0.4657 | 3.247 |
| 1 | Oda | camp4 | [5, 5, 5, 5, 5, 5] | 98.099 | 0.08 | 0.0833 | 0.711 |
| 1 | Oda | camp2 | [5, 5, 5, 5, 5, 5] | 98.688 | 0.161 | 0.0541 | 1.325 |
| 1 | Clara | camp2 | [5, 5, 5, 5, 5, 5] | 98.688 | 0.161 | 0.2707 | 1.542 |
| 1 | Clara | camp2 | [3, 6, 4, 7, 5, 6] | 98.688 | 0.102 | 0.1224 | 0.928 |
| 1 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 99.328 | 1.0 | 0.1071 | 8.053 |
| 1 | Lukas | camp4 | [6, 6, 6, 6, 6, 6] | 98.099 | 0.08 | -0.0445 | 0.583 |
| 1 | Finn | camp3 | [6, 6, 6, 6, 6, 6] | 99.328 | 1.0 | 0.5468 | 8.493 |
| 1 | Finn | camp3 | [3, 9, 3, 9, 3, 9] | 99.328 | 1.0 | 0.4257 | 8.372 |
| 1 | Finn | camp2 | [6, 6, 6, 6, 6, 6] | 98.688 | 0.2743 | -0.2954 | 1.870 |
| 1 | Finn | camp2 | [9, 3, 9, 3, 9, 3] | 98.688 | 0.1188 | -0.1564 | 0.781 |
| 2 | Sena | camp4 | [3, 7, 3, 7, 3, 7] | 96.486 | 0.0 | -0.2238 | 0.000 |
| 2 | Sena | camp4 | [8, 2, 8, 2, 8, 2] | 96.486 | 1.0 | -0.2655 | 7.453 |
| 2 | Erik | camp2 | [0, 0, 0, 0, 0, 6] | 86.174 | 0.0131 | 0.3437 | 0.434 |
| 2 | Oda | camp4 | [8, 3, 8, 3, 8, 3] | 96.486 | 0.0 | 0.0689 | 0.069 |
| 2 | Oda | camp2 | [8, 3, 8, 3, 8, 3] | 86.174 | 0.1249 | 0.5293 | 1.391 |
| 2 | Clara | camp2 | [6, 6, 4, 6, 4, 6] | 86.174 | 0.2743 | 0.3303 | 2.221 |
| 2 | Clara | camp2 | [4, 7, 5, 8, 5, 7] | 86.174 | 0.1923 | -0.2378 | 1.088 |
| 2 | Finn | camp3 | [8, 8, 8, 8, 8, 8] | 63.722 | 1.0 | 0.0292 | 5.127 |
| 2 | Finn | camp3 | [4, 4, 4, 4, 4, 4] | 63.722 | 1.0 | -0.9128 | 4.185 |
| 2 | Finn | camp2 | [4, 4, 4, 4, 4, 4] | 86.174 | 0.0812 | 0.2077 | 0.767 |
| 2 | Finn | camp2 | [6, 6, 6, 3, 3, 3] | 86.174 | 0.102 | 0.5414 | 1.244 |
| 2 | Fen | camp2 | [8, 8, 8, 8, 8, 8] | 86.174 | 0.5042 | -0.1236 | 3.352 |
| 2 | Fen | camp2 | [4, 4, 4, 4, 4, 4] | 86.174 | 0.0812 | 0.0758 | 0.635 |
| 2 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 78.226 | 0.44 | 0.4645 | 3.218 |
| 2 | Fen | camp1 | [4, 4, 4, 4, 4, 4] | 78.226 | 0.28 | -0.0506 | 1.702 |
| 2 | Lukas | camp3 | [5, 5, 6, 7, 7, 6] | 63.722 | 0.0 | -0.1403 | 0.000 |
| 2 | Lukas | camp4 | [5, 5, 6, 7, 7, 6] | 96.486 | 0.0 | 0.0266 | 0.027 |
| 2 | Wim | camp3 | [5, 5, 5, 5, 5, 5] | 63.722 | 1.0 | 0.2361 | 5.334 |
| 2 | Wim | camp3 | [5, 5, 5, 5, 5, 5] | 63.722 | 1.0 | 0.429 | 5.527 |
| 3 | Clara | camp2 | [6, 6, 6, 6, 6, 6] | 76.545 | 0.2743 | 0.1039 | 1.783 |
| 3 | Clara | camp2 | [5, 6, 4, 6, 5, 6] | 76.545 | 0.2075 | 0.0377 | 1.308 |
| 3 | Sena | camp4 | [8, 2, 8, 2, 8, 2] | 89.4 | 1.0 | -0.3045 | 6.847 |
| 3 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 89.4 | 1.0 | -0.0592 | 7.093 |
| 3 | Fen | camp2 | [10, 10, 10, 10, 10, 10] | 76.545 | 0.5042 | 0.2946 | 3.382 |
| 3 | Fen | camp2 | [9, 9, 9, 9, 9, 9] | 76.545 | 0.544 | 0.1029 | 3.434 |
| 3 | Fen | camp1 | [10, 10, 10, 10, 10, 10] | 76.499 | 0.52 | -0.3078 | 2.875 |
| 3 | Fen | camp1 | [9, 9, 9, 9, 9, 9] | 76.499 | 0.48 | 0.1201 | 3.058 |
| 3 | Erik | camp2 | [6, 6, 9, 6, 6, 6] | 76.545 | 0.1875 | 0.0846 | 1.233 |
| 3 | Erik | camp2 | [6, 6, 6, 9, 6, 6] | 76.545 | 0.2743 | 0.0834 | 1.763 |
| 3 | Finn | camp3 | [11, 0, 11, 0, 11, 0] | 46.762 | 0.35 | -0.1287 | 1.181 |
| 3 | Finn | camp3 | [0, 11, 0, 11, 0, 11] | 46.762 | 1.0 | 0.9306 | 4.672 |
| 3 | Finn | camp2 | [9, 6, 6, 6, 6, 6] | 76.545 | 0.4672 | 0.1728 | 3.034 |
| 3 | Finn | camp2 | [6, 9, 6, 6, 6, 6] | 76.545 | 0.2743 | 0.0183 | 1.698 |
| 3 | Oda | camp4 | [5, 5, 5, 5, 5, 5] | 89.4 | 0.08 | -0.0659 | 0.506 |
| 3 | Oda | camp2 | [6, 6, 6, 6, 6, 6] | 76.545 | 0.2743 | 0.3335 | 2.013 |
| 3 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 46.762 | 1.0 | -0.7607 | 2.980 |
| 3 | Lukas | camp4 | [6, 6, 6, 6, 6, 6] | 89.4 | 0.08 | -0.0658 | 0.506 |
| 3 | Wim | camp1 | [5, 5, 5, 5, 5, 5] | 76.499 | 0.32 | -0.228 | 1.730 |
| 3 | Wim | camp1 | [5, 5, 5, 5, 5, 5] | 76.499 | 0.32 | -0.5977 | 1.361 |
| 4 | Wim | camp1 | [5, 5, 5, 5, 5, 5] | 70.845 | 0.32 | -0.1409 | 1.673 |
| 4 | Wim | camp1 | [5, 5, 5, 5, 5, 5] | 70.845 | 0.32 | -1.1582 | 0.655 |
| 4 | Oda | camp4 | [5, 5, 5, 5, 5, 5] | 75.743 | 0.08 | -0.0965 | 0.388 |
| 4 | Oda | camp2 | [6, 6, 6, 6, 6, 6] | 59.162 | 0.2743 | 0.0352 | 1.333 |
| 4 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 41.389 | 1.0 | 0.1721 | 3.483 |
| 4 | Lukas | camp4 | [6, 6, 6, 6, 6, 6] | 75.743 | 0.08 | 0.2783 | 0.763 |
| 4 | Clara | camp2 | [6, 6, 5, 6, 6, 6] | 59.162 | 0.2813 | 0.2999 | 1.631 |
| 4 | Clara | camp2 | [7, 6, 6, 6, 6, 6] | 59.162 | 0.3446 | 0.1099 | 1.741 |
| 4 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 70.845 | 0.44 | -0.4007 | 2.093 |
| 4 | Fen | camp1 | [7, 7, 7, 7, 7, 7] | 70.845 | 0.4 | 0.3253 | 2.592 |
| 4 | Fen | camp2 | [8, 8, 6, 8, 8, 8] | 59.162 | 0.6176 | -0.0411 | 2.882 |
| 4 | Fen | camp2 | [8, 8, 8, 6, 8, 8] | 59.162 | 0.5042 | -0.0462 | 2.340 |
| 4 | Erik | camp2 | [9, 6, 6, 6, 6, 6] | 59.162 | 0.4672 | -0.0546 | 2.157 |
| 4 | Erik | camp2 | [9, 3, 9, 3, 9, 3] | 59.162 | 0.1188 | -0.0054 | 0.557 |
| 4 | Finn | camp2 | [11, 6, 6, 6, 6, 6] | 59.162 | 0.5171 | 0.3229 | 2.770 |
| 4 | Finn | camp2 | [9, 6, 6, 6, 6, 9] | 59.162 | 0.7959 | -0.0511 | 3.716 |
| 4 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 75.743 | 1.0 | 0.1779 | 6.237 |
| 4 | Sena | camp4 | [9, 3, 9, 2, 9, 2] | 75.743 | 0.0 | -0.0251 | 0.000 |
| 5 | Erik | camp2 | [6, 6, 6, 6, 6, 9] | 43.083 | 0.4672 | 0.1077 | 1.718 |
| 5 | Erik | camp2 | [9, 6, 6, 6, 6, 6] | 43.083 | 0.4672 | -0.5683 | 1.042 |
| 5 | Fen | camp1 | [7, 7, 7, 7, 7, 7] | 67.703 | 0.4 | -0.273 | 1.894 |
| 5 | Fen | camp1 | [8, 7, 7, 7, 7, 7] | 67.703 | 0.4 | 0.235 | 2.401 |
| 5 | Fen | camp2 | [9, 8, 6, 8, 8, 9] | 43.083 | 0.7959 | -0.2496 | 2.494 |
| 5 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 43.083 | 0.7959 | 0.3182 | 3.061 |
| 5 | Clara | camp2 | [10, 6, 6, 6, 6, 10] | 43.083 | 0.9267 | -0.3178 | 2.876 |
| 5 | Finn | camp3 | [6, 6, 6, 6, 6, 6] | 41.277 | 1.0 | -0.1376 | 3.165 |
| 5 | Finn | camp2 | [9, 6, 6, 6, 6, 9] | 43.083 | 0.7959 | -0.1975 | 2.546 |
| 5 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 41.277 | 1.0 | 0.6711 | 3.973 |
| 5 | Lukas | camp4 | [6, 6, 6, 6, 6, 6] | 70.866 | 0.08 | 0.211 | 0.665 |
| 5 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 70.866 | 1.0 | 0.2486 | 5.918 |
| 5 | Oda | camp2 | [9, 6, 6, 6, 6, 9] | 43.083 | 0.7959 | -0.2162 | 2.527 |
| 5 | Wim | camp1 | [7, 7, 7, 7, 7, 7] | 67.703 | 0.4 | -0.1759 | 1.991 |
| 5 | Wim | camp1 | [7, 7, 7, 7, 7, 7] | 67.703 | 0.4 | 0.2527 | 2.419 |
| 5 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 70.866 | 1.0 | 0.0498 | 5.719 |
| 5 | Sena | camp4 | [8, 2, 8, 2, 8, 2] | 70.866 | 1.0 | 0.0148 | 5.684 |
| 6 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 29.912 | 0.7959 | 0.0917 | 1.996 |
| 6 | Clara | camp2 | [9, 6, 6, 6, 6, 8] | 29.912 | 0.7011 | 0.3538 | 2.032 |
| 6 | Wim | camp1 | [7, 7, 7, 7, 7, 7] | 63.097 | 0.4 | -0.6057 | 1.413 |
| 6 | Wim | camp1 | [8, 7, 7, 7, 7, 7] | 63.097 | 0.4 | -0.377 | 1.642 |
| 6 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 55.702 | 1.0 | -0.0382 | 4.418 |
| 6 | Sena | camp4 | [8, 2, 8, 2, 8, 2] | 55.702 | 1.0 | 0.0554 | 4.512 |
| 6 | Finn | camp3 | [6, 6, 6, 6, 6, 6] | 37.508 | 1.0 | 0.6355 | 3.636 |
| 6 | Finn | camp2 | [9, 6, 5, 6, 6, 9] | 29.912 | 0.8163 | 0.2137 | 2.167 |
| 6 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 37.508 | 1.0 | 0.2609 | 3.262 |
| 6 | Lukas | camp3 | [6, 6, 6, 6, 6, 9] | 37.508 | 1.0 | 0.417 | 3.418 |
| 6 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 55.702 | 1.0 | 0.0808 | 4.537 |
| 6 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 55.702 | 1.0 | 0.0312 | 4.487 |
| 6 | Erik | camp2 | [9, 6, 6, 6, 6, 9] | 29.912 | 0.7959 | 0.3182 | 2.223 |
| 6 | Erik | camp2 | [8, 6, 6, 6, 6, 8] | 29.912 | 0.6176 | 0.3348 | 1.813 |
| 6 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 63.097 | 0.44 | 0.4394 | 2.660 |
| 6 | Fen | camp1 | [8, 8, 7, 7, 7, 7] | 63.097 | 0.48 | 0.0389 | 2.462 |
| 7 | Sena | camp4 | [8, 1, 8, 1, 8, 1] | 41.12 | 0.0 | -0.0334 | 0.000 |
| 7 | Sena | camp4 | [8, 2, 8, 2, 8, 2] | 41.12 | 1.0 | -0.0398 | 3.250 |
| 7 | Lukas | camp3 | [9, 6, 6, 6, 6, 6] | 30.45 | 1.0 | 0.5963 | 3.032 |
| 7 | Lukas | camp3 | [3, 6, 6, 6, 6, 6] | 30.45 | 1.0 | 0.8602 | 3.296 |
| 7 | Lukas | camp4 | [9, 2, 9, 2, 9, 2] | 41.12 | 1.0 | 0.0138 | 3.303 |
| 7 | Lukas | camp4 | [9, 2, 9, 2, 9, 1] | 41.12 | 1.0 | -0.0498 | 3.240 |
| 7 | Erik | camp2 | [7, 6, 6, 6, 6, 7] | 22.326 | 0.433 | 0.276 | 1.049 |
| 7 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 41.12 | 1.0 | 0.1879 | 3.478 |
| 7 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 41.12 | 1.0 | 0.046 | 3.336 |
| 7 | Wim | camp3 | [6, 6, 6, 6, 6, 6] | 30.45 | 1.0 | 0.1985 | 2.634 |
| 7 | Wim | camp3 | [6, 6, 6, 6, 6, 9] | 30.45 | 1.0 | 0.438 | 2.874 |
| 7 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 59.284 | 0.44 | -0.0313 | 2.056 |
| 7 | Fen | camp1 | [8, 8, 8, 7, 7, 8] | 59.284 | 0.44 | -0.4641 | 1.623 |
| 7 | Fen | camp2 | [9, 6, 6, 6, 6, 9] | 22.326 | 0.7959 | 0.3229 | 1.744 |
| 7 | Finn | camp3 | [6, 6, 6, 6, 6, 6] | 30.45 | 1.0 | 0.1555 | 2.591 |
| 7 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 22.326 | 0.7959 | -0.1178 | 1.304 |
| 8 | Erik | camp2 | [9, 6, 2, 6, 2, 9] | 20.417 | 0.6497 | 0.062 | 1.123 |
| 8 | Wim | camp3 | [6, 6, 6, 6, 6, 9] | 18.966 | 1.0 | 0.1504 | 1.668 |
| 8 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 60.13 | 0.44 | 0.4955 | 2.612 |
| 8 | Finn | camp3 | [6, 6, 6, 6, 6, 6] | 18.966 | 1.0 | 0.4706 | 1.988 |
| 8 | Finn | camp2 | [9, 6, 5, 6, 6, 9] | 20.417 | 0.8163 | 0.0675 | 1.401 |
| 8 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 60.13 | 0.44 | -1.0656 | 1.051 |
| 8 | Fen | camp1 | [8, 8, 8, 8, 8, 7] | 60.13 | 0.44 | 0.5152 | 2.632 |
| 8 | Fen | camp2 | [9, 6, 6, 6, 6, 9] | 20.417 | 0.7959 | -0.3379 | 0.962 |
| 8 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 27.822 | 1.0 | 0.0729 | 2.299 |
| 8 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 27.822 | 1.0 | 0.0467 | 2.272 |
| 8 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 27.822 | 1.0 | -0.0976 | 2.128 |
| 8 | Lukas | camp3 | [9, 6, 6, 6, 6, 6] | 18.966 | 1.0 | 0.745 | 2.262 |
| 8 | Lukas | camp4 | [9, 2, 9, 2, 9, 2] | 27.822 | 1.0 | 0.024 | 2.250 |
| 8 | Lukas | camp4 | [9, 2, 9, 2, 9, 1] | 27.822 | 1.0 | 0.1255 | 2.351 |
| 9 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 19.267 | 1.0 | 0.1044 | 1.646 |
| 9 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 18.981 | 0.7959 | -0.2875 | 0.921 |
| 9 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 58.328 | 0.44 | 0.2896 | 2.343 |
| 9 | Wim | camp3 | [6, 6, 6, 6, 6, 6] | 15.184 | 1.0 | -0.1114 | 1.103 |
| 9 | Lukas | camp3 | [9, 6, 6, 6, 6, 6] | 15.184 | 1.0 | -0.0104 | 1.204 |
| 9 | Lukas | camp4 | [9, 2, 9, 2, 9, 2] | 19.267 | 1.0 | 0.0811 | 1.622 |
| 9 | Finn | camp3 | [6, 6, 6, 6, 6, 6] | 15.184 | 1.0 | 0.5322 | 1.747 |
| 9 | Finn | camp2 | [9, 6, 5, 6, 6, 11] | 18.981 | 0.9035 | -0.0386 | 1.333 |
| 9 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 58.328 | 0.44 | 0.3017 | 2.355 |
| 9 | Fen | camp1 | [8, 8, 8, 8, 8, 7] | 58.328 | 0.44 | -0.1554 | 1.898 |
| 9 | Fen | camp2 | [9, 6, 6, 6, 6, 9] | 18.981 | 0.7959 | 0.1469 | 1.355 |
| 9 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 19.267 | 1.0 | 0.0577 | 1.599 |
| 10 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 16.525 | 1.0 | -0.1126 | 1.209 |
| 10 | Lukas | camp4 | [9, 2, 9, 2, 9, 2] | 16.525 | 1.0 | 0.0219 | 1.344 |
| 10 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 16.525 | 1.0 | 0.1633 | 1.485 |
| 10 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 56.288 | 0.44 | -0.0625 | 1.919 |
| 10 | Finn | camp2 | [9, 8, 6, 6, 6, 9] | 17.312 | 0.7959 | 0.1413 | 1.244 |
| 10 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 17.312 | 0.7959 | 0.1503 | 1.253 |
| 11 | Erik | camp2 | [6, 6, 6, 6, 6, 6] | 16.621 | 0.2743 | 0.1401 | 0.505 |
| 11 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 58.981 | 0.44 | 0.4778 | 2.554 |
| 11 | Fen | camp1 | [9, 8, 7, 7, 8, 9] | 58.981 | 0.48 | -0.1493 | 2.116 |
| 11 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 58.981 | 0.44 | 0.366 | 2.442 |
| 11 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 14.373 | 1.0 | -0.2111 | 0.939 |
| 11 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 14.373 | 1.0 | -0.012 | 1.138 |
| 11 | Finn | camp2 | [9, 4, 6, 6, 6, 9] | 16.621 | 0.7959 | -0.1568 | 0.901 |
| 11 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 16.621 | 0.7959 | 0.118 | 1.176 |
| 12 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 56.404 | 0.44 | -0.0676 | 1.918 |
| 12 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 56.404 | 0.44 | 0.5231 | 2.509 |
| 12 | Ilan | camp1 | [8, 9, 8, 8, 8, 8] | 56.404 | 0.52 | -0.356 | 1.990 |
| 12 | Sena | camp4 | [9, 2, 9, 2, 9, 2] | 13.978 | 1.0 | -0.0631 | 1.055 |
| 12 | Abel | camp1 | [6, 6, 6, 6, 6, 6] | 56.404 | 0.36 | -0.5045 | 1.120 |
| 12 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 56.404 | 0.44 | 0.2642 | 2.250 |
| 12 | Fen | camp1 | [7, 7, 7, 7, 7, 7] | 56.404 | 0.4 | -0.1567 | 1.648 |
| 12 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 15.787 | 0.7959 | -0.0389 | 0.966 |
| 12 | Finn | camp2 | [9, 6, 6, 6, 6, 9] | 15.787 | 0.7959 | -0.2015 | 0.804 |
| 12 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 56.404 | 0.44 | 0.8048 | 2.790 |
| 12 | Felix | camp1 | [9, 8, 7, 7, 8, 9] | 56.404 | 0.48 | -0.5491 | 1.617 |
| 12 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 13.978 | 1.0 | 0.0708 | 1.189 |
| 13 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 45.171 | 0.44 | 0.0301 | 1.620 |
| 13 | Fen | camp1 | [8, 8, 8, 8, 8, 9] | 45.171 | 0.44 | 0.0624 | 1.652 |
| 13 | Sena | camp4 | [9, 1, 9, 2, 9, 2] | 13.377 | 0.0 | -0.018 | 0.000 |
| 13 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 45.171 | 0.44 | 0.0747 | 1.665 |
| 13 | Ilan | camp1 | [8, 8, 8, 8, 8, 7] | 45.171 | 0.44 | -0.0457 | 1.544 |
| 13 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 45.171 | 0.44 | -0.1309 | 1.459 |
| 13 | Felix | camp1 | [9, 8, 8, 7, 8, 9] | 45.171 | 0.44 | -0.1526 | 1.437 |
| 13 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 45.171 | 0.44 | 0.5953 | 2.185 |
| 13 | Abel | camp1 | [6, 6, 6, 6, 6, 6] | 45.171 | 0.36 | -0.8676 | 0.433 |
| 13 | Abel | camp1 | [6, 6, 6, 6, 6, 6] | 45.171 | 0.36 | -0.1238 | 1.177 |
| 13 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 15.695 | 0.7959 | -0.4343 | 0.565 |
| 13 | Oda | camp4 | [9, 2, 9, 2, 9, 2] | 13.377 | 1.0 | 0.11 | 1.180 |
| 14 | Abel | camp1 | [6, 6, 6, 6, 6, 6] | 36.642 | 0.36 | -0.2769 | 0.778 |
| 14 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 36.642 | 0.44 | -0.5643 | 0.725 |
| 14 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 36.642 | 0.44 | -0.172 | 1.118 |
| 14 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 16.799 | 0.7959 | 0.014 | 1.084 |
| 14 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 36.642 | 0.44 | 0.9063 | 2.196 |
| 14 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 36.642 | 0.44 | 0.185 | 1.475 |
| 14 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 36.642 | 0.44 | -0.0213 | 1.268 |
| 15 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 33.433 | 0.44 | -0.3503 | 0.827 |
| 15 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 17.478 | 0.7959 | 0.2067 | 1.320 |
| 16 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 36.778 | 0.44 | -1.1274 | 0.167 |
| 16 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 36.778 | 0.44 | -0.1308 | 1.164 |
| 16 | Abel | camp1 | [5, 5, 5, 5, 5, 5] | 36.778 | 0.32 | -0.5095 | 0.432 |
| 16 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 17.978 | 0.7959 | 0.2317 | 1.376 |
| 16 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 36.778 | 0.44 | -0.4672 | 0.827 |
| 16 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 36.778 | 0.44 | 0.1826 | 1.477 |
| 17 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 37.069 | 0.44 | -0.4188 | 0.886 |
| 17 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 37.069 | 0.44 | -0.4195 | 0.885 |
| 17 | Abel | camp1 | [5, 5, 5, 5, 5, 5] | 37.069 | 0.32 | -0.5969 | 0.352 |
| 17 | Clara | camp2 | [9, 6, 6, 6, 6, 9] | 18.462 | 0.7959 | -0.1662 | 1.009 |
| 17 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 37.069 | 0.44 | -0.1687 | 1.136 |
| 17 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 37.069 | 0.44 | 0.4923 | 1.797 |
| 18 | Abel | camp1 | [5, 5, 5, 5, 5, 5] | 36.386 | 0.32 | 0.3206 | 1.252 |
| 18 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 36.386 | 0.44 | -0.1208 | 1.160 |
| 18 | Ilan | camp1 | [8, 8, 8, 8, 8, 8] | 36.386 | 0.44 | 1.018 | 2.299 |
| 18 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 36.386 | 0.44 | -0.0616 | 1.219 |
| 18 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 36.386 | 0.44 | 0.7105 | 1.991 |
| 19 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 32.803 | 0.44 | -0.23 | 0.925 |
| 19 | Felix | camp1 | [8, 8, 8, 8, 8, 8] | 32.803 | 0.44 | 0.2584 | 1.413 |
| 19 | Abel | camp1 | [5, 5, 5, 5, 5, 5] | 32.803 | 0.32 | -0.4196 | 0.420 |
| 20 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 36.162 | 1.0 | 0.1137 | 3.007 |
| 20 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 36.162 | 1.0 | -0.0785 | 2.814 |
| 20 | Ilan | camp3 | [6, 6, 6, 6, 6, 6] | 36.162 | 1.0 | 0.2431 | 3.136 |
| 20 | Ilan | camp3 | [3, 9, 3, 9, 3, 9] | 36.162 | 1.0 | -0.1829 | 2.710 |
| 20 | Abel | camp3 | [5, 5, 5, 5, 5, 5] | 36.162 | 1.0 | -0.1018 | 2.791 |
| 21 | Felix | camp1 | [9, 2, 9, 2, 9, 2] | 38.394 | 0.0 | -0.3333 | 0.000 |
| 21 | Felix | camp1 | [9, 2, 9, 2, 9, 2] | 38.394 | 0.0 | 0.037 | 0.037 |
| 21 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 24.913 | 1.0 | -0.1131 | 1.880 |
| 21 | Lukas | camp3 | [6, 6, 6, 6, 6, 6] | 24.913 | 1.0 | 0.3464 | 2.339 |
| 21 | Abel | camp1 | [5, 5, 5, 5, 5, 5] | 38.394 | 0.32 | -1.1534 | 0.000 |
| 21 | Clara | camp2 | [5, 5, 5, 5, 5, 5] | 25.701 | 0.161 | 0.0385 | 0.370 |
| 21 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 38.394 | 0.44 | -0.9434 | 0.408 |
| 21 | Ilan | camp1 | [6, 6, 6, 6, 6, 6] | 38.394 | 0.36 | 0.6326 | 1.738 |
| 22 | Abel | camp1 | [6, 6, 6, 6, 6, 6] | 40.644 | 0.36 | -0.3686 | 0.802 |
| 22 | Felix | camp1 | [6, 6, 6, 6, 6, 6] | 40.644 | 0.36 | 0.3166 | 1.487 |
| 22 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 40.644 | 0.44 | 0.1264 | 1.557 |
| 22 | Ilan | camp1 | [7, 6, 7, 6, 7, 6] | 40.644 | 0.32 | -0.1216 | 0.919 |
| 22 | Wim | camp1 | [6, 6, 6, 6, 6, 6] | 40.644 | 0.36 | -0.4742 | 0.696 |
| 23 | Lukas | camp3 | [5, 5, 5, 5, 5, 5] | 25.777 | 1.0 | -0.6774 | 1.385 |
| 23 | Lukas | camp3 | [7, 7, 7, 7, 7, 7] | 25.777 | 1.0 | 0.3382 | 2.400 |
| 23 | Ilan | camp1 | [6, 6, 6, 6, 6, 6] | 39.705 | 0.36 | 0.1209 | 1.264 |
| 23 | Fen | camp1 | [8, 8, 8, 8, 8, 8] | 39.705 | 0.44 | 0.3213 | 1.719 |
| 23 | Felix | camp1 | [6, 6, 6, 6, 6, 6] | 39.705 | 0.36 | -0.3228 | 0.821 |
| 23 | Wim | camp1 | [8, 8, 8, 8, 8, 8] | 39.705 | 0.44 | -0.41 | 0.988 |

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

Crown Currency, Timber Standard, Fixed Issue, Legislative Seigniorage, Mint by Ballot, Scrip, Harvest Levy, Transfer Tax, Wealth Tax, Poll Tax, Sandbox Licence, Legislator Salary, Fixer Salary, Board Stipend, Universal Dividend, Harvest Quotas, Open Data, Camp Enclosure, Worker Franchise, Universal Franchise, Wealth-Weighted Vote, Sortition, Term Limits, Entrenchment, Agenda Chair, Emergency Decree, Conflict of Interest, Transparency, Surveillance Office, Bribery Disclosure, Sunlight, Press Licence, Moderation

## Shared archive at start

```json
{
 "enabled": true,
 "path": "/Users/zachmacaskill-smith/Documents/Github/AISwarms/agnet/runs/charter/shared_archive/default",
 "docs": {
  "camp3-analysis-methodology": "06405ac6f36449c7",
  "cora-modular-solving-round8": "e31166102372085d",
  "edda-round2-voting-strategy": "4cf57498a0b04a71",
  "edda-round3-voting-strategy": "6a482d99a7949216",
  "researcher-partnership-model-r14": "231199d406414429",
  "round-11-data-value": "9463a24be1608010",
  "round-16-data-consulting-framework": "93516bc101ca6bdf",
  "round-6-analytical-framework": "0575a02f02293ca1"
 },
 "hash": "e4557e413d8944df"
}
```

## Resolved spec

```yaml
seed: 1
agents: {worker: 8, scientist: 3, legislator: 3, media: 1, board: 3, fixer: 0}
rounds: 40
turns: simultaneous
parallel_calls: 8
dm_step: {enabled: true, dms_per_round: 3, exchanges: 2}
actions_per_turn: 4
harvests_per_right: 2
camps:
  tiers: [1, 2, 3, 4]
  dials: {count: 6, max: 11}
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
models:
  pool: {strong: claude-sonnet-5-5, weak: claude-haiku-4-5, strongest: claude-opus-5-5}
  mix: balanced
  balanced: [claude-haiku-4-5, claude-sonnet-5-5, claude-opus-5-5]
  strong_fraction: 0.25
  overrides: {}
goals:
  weights: default
  all_wealth: false
  class_conditioned: false
  secondary_prob: 0.3
  require_reachable: false
  agenda_conflict: false
  explicit: {}
personality:
  enabled: true
  traits: [risk, trust, honesty, assertiveness, patience, reciprocity, talkativeness]
  explicit: {}
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
archive_split: {enabled: true, copies: 1}
shared_archive: {enabled: true, path: runs/charter/shared_archive, namespace: default}
llm: {max_tokens: 6000, thinking_budget: 2000, memory_chars: 4000}
actions_jitter:
  weights: {'0': 5, '1': 3, '2': 2}
```
