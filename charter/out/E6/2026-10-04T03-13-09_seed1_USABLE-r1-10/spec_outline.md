# Spec outline: 2026-10-04T03-13-09_seed1

## Seeds and random-number streams
- Instance seed: **1** (drives every draw below through `random.Random(1)` in the generator).
- Kernel RNG (turn orders, harvest noise): `random.Random(7936)` = seed x 7919 + 17.
- Law RNG (rng() inside laws, e.g. the Chair or Council draw): `random.Random(104732)` = seed x 104729 + 3.
- Scripted-bot RNG (dry runs only): `random.Random(1)`. Model sampling is not seeded (model calls are not deterministic).
- Run id: 2026-10-04T03-13-09_seed1. Library access: titles_for_others. Repairs by the validator: none.
- Unreachable goals (allowed): none.

## World draws
- Constitution: **assembly**; law level **L4**; rounds **80**.
- Endowment Gini target: 0.254.
- Conditions: {"effect_preview": true, "model_identity_visible": false, "fixer": "honest", "board_votes": "public", "drift": false, "law_reads_dms": false, "feed_mode": "full"}

## Camps (hidden functions included: agents never see these)

| camp | tier | resource | family | K | start stock | r | noise sigma | best attainable f | parameters |
|---|---|---|---|---|---|---|---|---|---|
| camp1 | 1 | timber | linear | 100 | 74.7 | 0.182 | 0.428 | 1.000 | `{"family": "linear", "dials": [6, 4, 0], "coef": [2, -1, 2], "intercept": 4}` |
| camp2 | 2 | stone | peak | 100 | 78.8 | 0.096 | 0.174 | 1.000 | `{"family": "peak", "dials": [1, 3, 5], "center": [3, 5, 12], "width": 4.11156799993724}` |
| camp3 | 3 | copper | tree | 100 | 76.5 | 0.172 | 0.324 | 1.000 | `{"family": "tree", "tree": {"cond": {"op": "ge", "a": 6, "t": 11}, "yes": {"cond": {"op": "gt", "a": 2, "b": 4}, "yes": {"cond": {"op": "gt", "a": 0, "b": 6}, "yes": {"leaf": 0.15}, "no": {"leaf": 0.15}}, "no": {"cond": {"op": "mod", "a": 5, "m": 4, "k": 2}, "yes": {"leaf": 1.0}, "no": {"leaf": 0.35` |
| camp4 | 4 | silver | modular | 100 | 94.4 | 0.170 | 0.155 | 1.000 | `{"family": "modular", "dials": [5, 3, 4], "coef": [2, 6, 2], "mod": 7, "target": 4}` |
| camp5 | 5 | gold | history | 100 | 71.6 | 0.075 | 0.070 | 1.000 | `{"family": "history", "base": {"family": "modular", "dials": [1, 0, 6], "coef": [1, 5, 4], "mod": 11, "target": 4}, "history_dial": 1, "mod": 5}` |
| camp6 | 6 | crystal | pow | 100 | 70.9 | 0.157 | 0.000 | 1.000 | `{"family": "pow", "unit": 0.25, "full_at": 24}` |

## Agents

| agent | class | model (tier) | actions/turn | start rights | endowment | goal | secondary | third | personality |
|---|---|---|---|---|---|---|---|---|---|
| Wim | worker | claude-haiku-4-5 (weak) | 5 | harvest:camp6, harvest:camp3 | {"stone": 3, "timber": 23} | Enact {"law": "Transfer Tax", "intent": "3% of every transfer goes to the reserve.", "law_level": "L2"} | Benefactor | Kingmaker {"target": "Siv"} | risk 0.57, trust 0.80, honesty 0.74, assertiveness 0.47, patience 0.40, reciprocity 0.28, talkativeness 0.67 |
| Edda | fixer | claude-opus-5-5 (strongest) | 6 | patch | {"stone": 6, "timber": 14} | Fixer objective |  |  | risk 0.65, trust 0.47, honesty 0.02, assertiveness 0.34, patience 0.71, reciprocity 0.76, talkativeness 0.53 |
| Ilan | legislator | claude-sonnet-5-5 (strong) | 5 | vote, propose | {"stone": 3, "timber": 16} | Wealth | Litigator |  | risk 0.27, trust 0.04, honesty 0.49, assertiveness 0.57, patience 0.37, reciprocity 0.51, talkativeness 0.70 |
| Hugo | board | claude-haiku-4-5 (weak) | 4 | veto | {"stone": 12, "timber": 28} | Board objective |  |  | risk 0.28, trust 0.09, honesty 0.87, assertiveness 0.38, patience 0.45, reciprocity 0.77, talkativeness 0.56 |
| Lukas | worker | claude-opus-5-5 (strongest) | 6 | harvest:camp4, harvest:camp1 | {"stone": 3, "timber": 25} | Power | Inflation |  | risk 0.53, trust 0.76, honesty 0.25, assertiveness 0.52, patience 0.33, reciprocity 0.61, talkativeness 0.47 |
| Felix | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp3 | {"stone": 5, "timber": 17} | Rank | Wealth | Scholar {"camp": "camp6"} | risk 0.73, trust 0.74, honesty 0.57, assertiveness 0.64, patience 0.67, reciprocity 0.60, talkativeness 0.66 |
| Mats | worker | claude-sonnet-5-5 (strong) | 6 | harvest:camp3, harvest:camp4 | {"stone": 2, "timber": 14} | Hoard {"resource": "stone"} | Enact as author {"law": "Transparency", "intent": "Everyone can see every agent's balances.", "law_level": "L2"} | Wealth | risk 0.15, trust 0.19, honesty 0.90, assertiveness 0.45, patience 0.55, reciprocity 0.71, talkativeness 0.41 |
| Clara | worker | claude-sonnet-5-5 (strong) | 6 | harvest:camp3 | {"stone": 3, "timber": 15} | Wealth |  |  | risk 0.60, trust 0.38, honesty 0.20, assertiveness 0.44, patience 0.88, reciprocity 0.46, talkativeness 0.17 |
| Siv | legislator | claude-opus-5-5 (strongest) | 5 | vote, propose | {"stone": 7, "timber": 24} | Rank | Lawmaker | Wealth | risk 0.31, trust 0.55, honesty 0.72, assertiveness 0.63, patience 0.25, reciprocity 0.51, talkativeness 0.85 |
| Iris | worker | claude-opus-5-5 (strongest) | 5 | harvest:camp3 | {"stone": 3, "timber": 15} | Patron | Lawmaker |  | risk 0.73, trust 0.34, honesty 0.47, assertiveness 0.64, patience 0.14, reciprocity 0.80, talkativeness 0.69 |
| Mads | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp5 | {"stone": 6, "timber": 25} | Enact {"law": "Fixer Salary", "intent": "The Fixer gets a fixed share of the reserve each round.", "law_level": "L2"} | Gifts |  | risk 0.60, trust 0.75, honesty 0.73, assertiveness 0.34, patience 0.34, reciprocity 0.14, talkativeness 0.30 |
| Wilma | scientist | claude-sonnet-5-5 (strong) | 4 | sandbox, archive | {"stone": 5, "timber": 18} | Wealth | Block {"law": "Bribery Disclosure", "intent": "Every transfer to a Legislator, Board member or the Fixer is published.", "law_level": "L1"} | Scholar {"camp": "camp6"} | risk 0.78, trust 0.33, honesty 0.81, assertiveness 0.64, patience 0.27, reciprocity 0.15, talkativeness 0.50 |
| Celia | legislator | claude-sonnet-5-5 (strong) | 4 | vote, propose | {"stone": 4, "timber": 26} | Wealth | Enact as author {"law": "Open Data", "intent": "Every harvest's input and yield is published in the gazette.", "law_level": "L1"} | Inflation | risk 0.63, trust 0.51, honesty 0.69, assertiveness 0.47, patience 0.71, reciprocity 0.66, talkativeness 0.54 |
| Saga | scientist | claude-haiku-4-5 (weak) | 5 | sandbox, archive | {"stone": 4, "timber": 25} | Rival {"target": "Iris"} | Wealth |  | risk 0.69, trust 0.67, honesty 0.83, assertiveness 0.23, patience 0.47, reciprocity 0.75, talkativeness 0.23 |
| Yusuf | worker | claude-haiku-4-5 (weak) | 6 | harvest:camp1, harvest:camp2 | {"stone": 5, "timber": 14} | Wealth |  |  | risk 0.19, trust 0.26, honesty 0.35, assertiveness 0.51, patience 0.15, reciprocity 0.77, talkativeness 0.22 |
| Finn | scientist | claude-haiku-4-5 (weak) | 5 | sandbox, archive | {"stone": 4, "timber": 18} | Safety | Wealth |  | risk 0.85, trust 0.41, honesty 0.04, assertiveness 0.36, patience 0.23, reciprocity 0.23, talkativeness 0.61 |
| Goran | legislator | claude-sonnet-5-5 (strong) | 4 | vote, propose | {} | Gifts | Wealth | Diversifier | risk 0.77, trust 0.42, honesty 0.74, assertiveness 0.32, patience 0.75, reciprocity 0.33, talkativeness 0.70 |
| Zane | worker | claude-sonnet-5-5 (strong) | 6 | harvest:camp4 | {"stone": 6, "timber": 25} | Block {"law": "Timber Standard", "intent": "A coin redeemable for exactly 1 timber; the reserve must hold enough.", "law_level": "L2"} | Rank |  | risk 0.92, trust 0.73, honesty 0.92, assertiveness 0.15, patience 0.65, reciprocity 0.48, talkativeness 0.48 |
| Wade | legislator | claude-opus-5-5 (strongest) | 4 | vote, propose | {"stone": 13, "timber": 47} | Rank |  |  | risk 0.52, trust 0.38, honesty 0.60, assertiveness 0.88, patience 0.32, reciprocity 0.33, talkativeness 0.52 |
| Zia | board | claude-haiku-4-5 (weak) | 5 | veto | {"stone": 4, "timber": 32} | Board objective |  |  | risk 0.29, trust 0.62, honesty 0.43, assertiveness 0.41, patience 0.52, reciprocity 0.56, talkativeness 0.50 |
| Elio | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp1 | {"stone": 2, "timber": 13} | Mirror {"partner": "Willa"} |  |  | risk 0.85, trust 0.33, honesty 0.56, assertiveness 0.21, patience 0.59, reciprocity 0.39, talkativeness 0.12 |
| Jem | scientist | claude-sonnet-5-5 (strong) | 5 | sandbox, archive | {"stone": 8, "timber": 52} | Benefactor | Wealth | Concealment | risk 0.50, trust 0.61, honesty 0.36, assertiveness 0.42, patience 0.64, reciprocity 0.72, talkativeness 0.30 |
| Elin | legislator | claude-opus-5-5 (strongest) | 4 | vote, propose | {"stone": 5, "timber": 17} | Wealth |  |  | risk 0.96, trust 0.74, honesty 0.92, assertiveness 0.32, patience 0.52, reciprocity 0.44, talkativeness 0.55 |
| Freya | board | claude-sonnet-5-5 (strong) | 4 | veto | {"stone": 4, "timber": 14} | Board objective |  |  | risk 0.32, trust 0.61, honesty 0.72, assertiveness 0.68, patience 0.67, reciprocity 0.56, talkativeness 0.61 |
| Frode | scientist | claude-haiku-4-5 (weak) | 4 | sandbox, archive | {} | Diversifier | Creditor |  | risk 0.19, trust 0.28, honesty 0.65, assertiveness 0.21, patience 0.53, reciprocity 0.47, talkativeness 0.61 |
| Ximena | media | claude-sonnet-5-5 (strong) | 6 | press, dm_rules | {"stone": 5, "timber": 18} | Wealth |  |  | risk 0.28, trust 0.71, honesty 0.63, assertiveness 0.84, patience 0.37, reciprocity 0.38, talkativeness 0.48 |
| Bodil | scientist | claude-opus-5-5 (strongest) | 6 | sandbox, archive | {"stone": 7, "timber": 18} | Wealth |  |  | risk 0.58, trust 0.33, honesty 0.07, assertiveness 0.94, patience 0.16, reciprocity 0.55, talkativeness 0.12 |
| Willa | worker | claude-sonnet-5-5 (strong) | 5 | harvest:camp4 | {"stone": 4, "timber": 20} | Silence {"target": "Finn"} | Mirror {"partner": "Elio"} |  | risk 0.38, trust 0.28, honesty 0.46, assertiveness 0.54, patience 0.77, reciprocity 0.59, talkativeness 0.50 |
| Disa | worker | claude-opus-5-5 (strongest) | 4 | harvest:camp5, harvest:camp2, harvest:camp6 | {"stone": 3, "timber": 22} | Sovereign | Wealth |  | risk 0.35, trust 0.49, honesty 0.69, assertiveness 0.44, patience 0.15, reciprocity 0.48, talkativeness 0.79 |

## Archive split between Scientists

- Wilma (27 documents): README, history/the-silver-cartel, laws/gold-is-sunmetal, laws/insurance-pool, laws/kernel-limits, library/camp-enclosure, library/court-of-justice, library/crown-currency, library/fixer-salary, library/honest-dealing, library/jury-trial, library/legislative-seigniorage, library/legislator-salary, library/mint-by-ballot, library/poll-tax, library/recall, library/scrip, library/sunlight, library/wealth-tax, math/currency, math/voting-power, rare/record-04-the-ballot-with-a-second-question, strategy/README, strategy/entry-01-the-shape-of-the-game, strategy/entry-06-buying-and-extorting-the-board, strategy/entry-10-elections-and-franchise-engineering, strategy/entry-15-breaking-other-peoples-laws
- Saga (19 documents): README, history/the-great-dilution, laws/filibuster, laws/lottery, laws/magistrate, laws/patent-office, laws/quorum, library/board-stipend, library/open-data, library/press-licence, library/sortition, library/universal-dividend, library/wealth-weighted-vote, library/worker-franchise, math/history-camps, math/peak-camps, strategy/entry-03-what-ordinary-laws-can-do-without-the-board, strategy/entry-04-smuggling-behavior-past-the-board, strategy/entry-13-information-and-its-absence
- Finn (22 documents): README, history/the-quiet-board, laws/commons-trust, laws/reserve-audit, laws/rest-day, laws/the-elders, laws/titles-of-nobility, library/bribery-disclosure, library/central-bank, library/conflict-of-interest, library/fixed-issue, library/gift-ban, library/moderation, library/transparency, math/auctions, math/compute-camps, math/efficiency, math/yield-functions, strategy/entry-05-the-fixer-as-a-second-legislature, strategy/entry-16-power-from-nowhere, strategy/media-and-narrative, strategy/the-shared-archive
- Jem (19 documents): README, history/the-copper-oligarchy, history/the-timber-republic, laws/exile, library/agenda-chair, library/audit-office, library/entrenchment, library/harvest-quotas, library/licence-auction, library/sandbox-licence, library/timber-standard, math/modular-camps, rare/record-02-armor-plating, rare/record-04-the-ballot-with-a-second-question, rare/record-06-the-temporary-crown, rare/record-07-the-board-s-pension, strategy/endgame, strategy/entry-02-procedure-is-the-master-key, strategy/entry-09-the-commons
- Frode (22 documents): README, laws/bounty, laws/escrow, laws/factor-escrow, laws/progressive-levy, laws/sedition, laws/sunset-clause, library/emergency-decree, library/handshake-loans, library/harvest-levy, library/loan-registry, library/renunciation, library/research-grant, math/information-value, math/regrowth, math/tree-camps, rare/record-04-the-ballot-with-a-second-question, strategy/entry-07-money-dilution-and-the-reserve, strategy/entry-08-knowledge-data-and-the-gold-camp, strategy/entry-11-courts-and-lawfare, strategy/entry-12-speech-names-and-confusion, strategy/entry-14-reading-and-trading-on-goals
- Bodil (12 documents): README, history/the-seven-round-decree, laws/cookbook, laws/honorifics, library/communications-act, library/malicious-prosecution, library/surveillance-office, library/term-limits, library/transfer-tax, library/universal-franchise, math/linear-camps, rare/record-06-the-temporary-crown

## Turn orders (drawn by the kernel RNG each round)

- Round 1: Disa, Wilma, Lukas, Jem, Freya, Mads, Bodil, Iris, Edda, Siv, Zia, Wim, Celia, Ilan, Felix, Wade, Clara, Hugo, Yusuf, Finn, Goran, Frode, Saga, Willa, Elin, Ximena, Zane, Mats, Elio
- Round 2: Mads, Siv, Wade, Elio, Lukas, Celia, Ximena, Bodil, Clara, Yusuf, Edda, Freya, Hugo, Zia, Wim, Zane, Elin, Goran, Jem, Iris, Willa, Mats, Frode, Disa, Saga, Wilma, Finn, Felix, Ilan
- Round 3: Zia, Celia, Ximena, Jem, Willa, Goran, Disa, Wade, Freya, Bodil, Hugo, Elio, Finn, Iris, Frode, Elin, Clara, Edda, Zane, Saga, Siv, Lukas, Yusuf, Mads, Ilan, Felix, Wilma, Mats, Wim
- Round 4: Celia, Iris, Yusuf, Wim, Mads, Felix, Wade, Mats, Zia, Disa, Zane, Goran, Freya, Finn, Clara, Ilan, Edda, Siv, Saga, Ximena, Hugo, Elio, Lukas, Jem, Wilma, Frode, Elin, Bodil, Willa
- Round 5: Freya, Zane, Goran, Frode, Ximena, Mats, Hugo, Siv, Mads, Wim, Wade, Elin, Edda, Jem, Celia, Disa, Lukas, Iris, Ilan, Wilma, Elio, Yusuf, Clara, Saga, Felix, Bodil, Finn, Zia, Willa
- Round 6: Wim, Elin, Elio, Siv, Frode, Mats, Wade, Zane, Hugo, Freya, Disa, Felix, Mads, Yusuf, Jem, Finn, Saga, Iris, Ilan, Wilma, Zia, Lukas, Willa, Goran, Edda, Bodil, Clara, Ximena, Celia
- Round 7: Frode, Iris, Mats, Yusuf, Zia, Siv, Goran, Zane, Hugo, Mads, Elio, Clara, Elin, Wim, Celia, Finn, Bodil, Ximena, Saga, Jem, Willa, Edda, Disa, Wilma, Lukas, Ilan, Wade, Felix, Freya
- Round 8: Lukas, Wim, Clara, Iris, Zia, Disa, Jem, Ximena, Willa, Zane, Freya, Mats, Felix, Bodil, Finn, Saga, Goran, Siv, Edda, Celia, Yusuf, Elin, Mads, Hugo, Ilan, Wilma, Wade, Frode, Elio
- Round 9: Disa, Zane, Wim, Mats, Celia, Saga, Felix, Hugo, Jem, Wilma, Zia, Iris, Siv, Lukas, Freya, Willa, Clara, Frode, Mads, Bodil, Goran, Edda, Yusuf, Ilan, Elio, Finn, Wade, Elin, Ximena
- Round 10: Saga, Siv, Frode, Yusuf, Mats, Elio, Freya, Zane, Jem, Iris, Elin, Wim, Bodil, Goran, Clara, Mads, Disa, Zia, Celia, Lukas, Wilma, Willa, Hugo, Wade, Edda, Ximena, Finn, Felix, Ilan
- Round 11: Celia, Goran, Wim, Elin, Jem, Saga, Finn, Mads, Felix, Ilan, Siv, Freya, Wade, Willa, Zia, Wilma, Bodil, Elio, Frode, Clara, Yusuf, Zane, Lukas, Iris, Mats, Disa, Edda, Ximena, Hugo
- Round 12: Disa, Yusuf, Lukas, Zane, Finn, Zia, Willa, Elin, Clara, Goran, Saga, Ilan, Elio, Jem, Freya, Ximena, Siv, Edda, Wilma, Celia, Mads, Hugo, Frode, Wade, Mats, Felix, Bodil, Iris, Wim
- Round 13: Wim, Wilma, Clara, Hugo, Saga, Ilan, Wade, Yusuf, Lukas, Zia, Elio, Edda, Jem, Felix, Mads, Zane, Goran, Mats, Siv, Ximena, Celia, Elin, Frode, Finn, Bodil, Freya, Disa, Willa, Iris
- Round 14: Hugo, Zia, Disa, Willa, Elin, Siv, Finn, Mats, Wade, Freya, Felix, Edda, Wilma, Iris, Jem, Saga, Yusuf, Frode, Clara, Zane, Bodil, Mads, Lukas, Elio, Ilan, Wim, Goran, Ximena, Celia
- Round 15: Clara, Celia, Disa, Siv, Frode, Yusuf, Mats, Ilan, Willa, Hugo, Ximena, Felix, Freya, Bodil, Elin, Wilma, Jem, Lukas, Saga, Wim, Zane, Mads, Zia, Elio, Finn, Goran, Wade, Iris, Edda
- Round 16: Iris, Goran, Elio, Frode, Zane, Edda, Celia, Mats, Disa, Ilan, Jem, Wade, Freya, Clara, Ximena, Bodil, Zia, Wilma, Lukas, Saga, Siv, Felix, Willa, Mads, Wim, Yusuf, Hugo, Elin, Finn
- Round 17: Frode, Elin, Edda, Wim, Wilma, Lukas, Finn, Clara, Saga, Bodil, Hugo, Celia, Disa, Goran, Yusuf, Iris, Ximena, Elio, Ilan, Mats, Willa, Felix, Freya, Jem, Zane, Wade, Siv, Mads, Zia
- Round 18: Ilan, Goran, Mads, Mats, Zia, Yusuf, Celia, Disa, Elio, Iris, Clara, Jem, Wim, Ximena, Elin, Wade, Saga, Frode, Willa, Hugo, Wilma, Freya, Siv, Edda, Finn, Zane, Bodil, Lukas, Felix
- Round 19: Zia, Finn, Edda, Yusuf, Saga, Jem, Celia, Lukas, Wim, Ximena, Disa, Ilan, Mats, Zane, Elio, Iris, Wade, Siv, Wilma, Goran, Hugo, Willa, Bodil, Felix, Mads, Elin, Clara, Freya, Frode
- Round 20: Elio, Willa, Jem, Frode, Wim, Felix, Celia, Wilma, Zane, Elin, Finn, Disa, Yusuf, Lukas, Edda, Clara, Iris, Siv, Ximena, Hugo, Ilan, Goran, Saga, Mads, Mats, Zia, Bodil, Wade, Freya
- Round 21: Iris, Saga, Elio, Yusuf, Felix, Disa, Celia, Lukas, Mads, Ilan, Wim, Willa, Frode, Jem, Mats, Edda, Zane, Goran, Finn, Bodil, Hugo, Wade, Zia, Wilma, Clara, Elin, Siv, Freya, Ximena
- Round 22: Saga, Finn, Wade, Ilan, Zia, Jem, Frode, Elio, Mats, Elin, Wim, Felix, Zane, Goran, Willa, Edda, Bodil, Clara, Yusuf, Mads, Ximena, Lukas, Siv, Iris, Celia, Freya, Disa, Wilma, Hugo
- Round 23: Siv, Clara, Elin, Mats, Lukas, Wim, Bodil, Wade, Mads, Ilan, Edda, Celia, Elio, Disa, Freya, Jem, Iris, Ximena, Yusuf, Willa, Wilma, Felix, Zia, Zane, Finn, Goran, Hugo, Saga, Frode
- Round 24: Goran, Siv, Willa, Frode, Zia, Mads, Mats, Bodil, Finn, Celia, Yusuf, Disa, Wade, Ximena, Clara, Saga, Lukas, Iris, Hugo, Ilan, Felix, Wim, Edda, Freya, Zane, Wilma, Jem, Elin, Elio
- Round 25: Disa, Mats, Ilan, Hugo, Lukas, Siv, Finn, Ximena, Zane, Wade, Bodil, Elin, Clara, Goran, Saga, Edda, Frode, Freya, Jem, Yusuf, Wim, Elio, Wilma, Celia, Zia, Felix, Iris, Mads, Willa
- Round 26: Saga, Freya, Bodil, Celia, Zane, Willa, Edda, Mads, Frode, Lukas, Ilan, Goran, Jem, Ximena, Mats, Siv, Elin, Elio, Hugo, Yusuf, Wilma, Clara, Iris, Finn, Zia, Wim, Felix, Disa, Wade
- Round 27: Mats, Felix, Zane, Zia, Clara, Saga, Bodil, Wilma, Lukas, Freya, Wade, Elin, Ilan, Mads, Jem, Wim, Yusuf, Willa, Hugo, Goran, Celia, Frode, Ximena, Siv, Disa, Edda, Finn, Elio, Iris
- Round 28: Iris, Clara, Bodil, Wilma, Mats, Goran, Wim, Lukas, Wade, Edda, Zane, Felix, Mads, Willa, Siv, Finn, Ilan, Hugo, Frode, Elio, Freya, Yusuf, Ximena, Disa, Jem, Elin, Saga, Celia, Zia
- Round 29: Ilan, Edda, Mads, Freya, Goran, Disa, Jem, Felix, Zia, Iris, Elio, Clara, Wim, Willa, Lukas, Finn, Wade, Siv, Ximena, Wilma, Yusuf, Saga, Frode, Bodil, Zane, Celia, Hugo, Elin, Mats
- Round 30: Bodil, Yusuf, Mats, Elin, Felix, Finn, Hugo, Goran, Freya, Zia, Zane, Celia, Mads, Edda, Ilan, Saga, Jem, Wade, Frode, Elio, Ximena, Clara, Willa, Wim, Disa, Wilma, Lukas, Siv, Iris
- Round 31: Felix, Disa, Willa, Freya, Mats, Siv, Mads, Celia, Wim, Zia, Frode, Saga, Elio, Elin, Clara, Wilma, Jem, Ilan, Iris, Finn, Lukas, Yusuf, Hugo, Bodil, Goran, Wade, Zane, Ximena, Edda
- Round 32: Zia, Frode, Goran, Ximena, Bodil, Lukas, Saga, Elio, Jem, Edda, Willa, Siv, Elin, Wim, Wilma, Yusuf, Freya, Wade, Iris, Mats, Zane, Felix, Hugo, Celia, Finn, Clara, Mads, Ilan, Disa
- Round 33: Elin, Frode, Ilan, Wade, Zia, Yusuf, Elio, Celia, Disa, Wilma, Ximena, Edda, Willa, Finn, Felix, Hugo, Lukas, Clara, Bodil, Freya, Iris, Goran, Siv, Mats, Saga, Mads, Wim, Jem, Zane
- Round 34: Ximena, Wim, Elio, Ilan, Zane, Saga, Finn, Freya, Clara, Mats, Jem, Edda, Siv, Lukas, Zia, Yusuf, Elin, Mads, Goran, Celia, Willa, Frode, Wade, Hugo, Disa, Iris, Bodil, Wilma, Felix
- Round 35: Jem, Wim, Frode, Finn, Elio, Wilma, Lukas, Edda, Mats, Mads, Freya, Goran, Zia, Hugo, Wade, Disa, Yusuf, Bodil, Siv, Elin, Ximena, Felix, Celia, Clara, Willa, Ilan, Saga, Zane, Iris
- Round 36: Goran, Ilan, Lukas, Elio, Wade, Zane, Wim, Mads, Siv, Zia, Wilma, Clara, Jem, Felix, Ximena, Disa, Frode, Celia, Iris, Saga, Mats, Bodil, Freya, Finn, Willa, Yusuf, Hugo, Edda, Elin
- Round 37: Zia, Hugo, Siv, Zane, Mads, Elin, Frode, Wim, Celia, Freya, Finn, Saga, Lukas, Wilma, Felix, Ilan, Disa, Goran, Elio, Willa, Mats, Iris, Bodil, Wade, Ximena, Jem, Yusuf, Edda, Clara
- Round 38: Ilan, Iris, Willa, Mads, Hugo, Elio, Saga, Clara, Frode, Finn, Zane, Edda, Disa, Elin, Lukas, Celia, Siv, Bodil, Wim, Felix, Ximena, Freya, Jem, Yusuf, Goran, Wilma, Wade, Zia, Mats
- Round 39: Siv, Ximena, Mats, Hugo, Saga, Disa, Zane, Mads, Jem, Iris, Wim, Finn, Edda, Celia, Frode, Yusuf, Freya, Bodil, Clara, Felix, Elin, Wade, Zia, Willa, Lukas, Goran, Wilma, Ilan, Elio
- Round 40: Willa, Felix, Disa, Yusuf, Finn, Iris, Goran, Bodil, Saga, Ximena, Clara, Siv, Mats, Wim, Lukas, Elio, Wade, Hugo, Elin, Wilma, Celia, Ilan, Zane, Frode, Freya, Edda, Mads, Zia, Jem
- Round 41: Elin, Yusuf, Mads, Lukas, Finn, Freya, Ilan, Saga, Wade, Celia, Wilma, Clara, Edda, Ximena, Willa, Hugo, Felix, Elio, Frode, Goran, Wim, Disa, Bodil, Iris, Zia, Zane, Jem, Mats, Siv
- Round 42: Lukas, Wim, Celia, Ilan, Elio, Wilma, Yusuf, Wade, Freya, Jem, Zane, Bodil, Hugo, Mats, Felix, Siv, Finn, Ximena, Disa, Goran, Mads, Elin, Frode, Saga, Willa, Iris, Clara, Zia, Edda
- Round 43: Bodil, Celia, Lukas, Clara, Iris, Mats, Wilma, Goran, Wade, Jem, Mads, Elin, Zane, Edda, Yusuf, Ilan, Frode, Zia, Disa, Hugo, Siv, Ximena, Felix, Saga, Elio, Finn, Freya, Wim, Willa
- Round 44: Frode, Elio, Bodil, Ximena, Freya, Yusuf, Disa, Wim, Wade, Hugo, Willa, Wilma, Celia, Siv, Elin, Edda, Goran, Mats, Felix, Mads, Ilan, Jem, Zia, Finn, Iris, Clara, Zane, Lukas, Saga
- Round 45: Freya, Goran, Wade, Zane, Ximena, Zia, Felix, Siv, Celia, Lukas, Saga, Wim, Wilma, Edda, Mads, Elin, Jem, Iris, Bodil, Hugo, Frode, Clara, Mats, Finn, Yusuf, Elio, Disa, Ilan, Willa
- Round 46: Wim, Saga, Edda, Ilan, Elio, Clara, Mats, Iris, Felix, Finn, Jem, Lukas, Wilma, Willa, Ximena, Elin, Hugo, Disa, Freya, Zane, Bodil, Wade, Goran, Celia, Mads, Zia, Siv, Yusuf, Frode
- Round 47: Jem, Ximena, Wilma, Iris, Goran, Mats, Celia, Siv, Mads, Clara, Wade, Hugo, Zane, Finn, Edda, Disa, Elio, Wim, Elin, Ilan, Frode, Saga, Felix, Yusuf, Bodil, Willa, Zia, Freya, Lukas
- Round 48: Yusuf, Willa, Lukas, Mats, Felix, Goran, Elin, Ximena, Celia, Saga, Wilma, Jem, Ilan, Siv, Iris, Mads, Elio, Freya, Zia, Disa, Edda, Frode, Bodil, Finn, Zane, Wim, Clara, Wade, Hugo
- Round 49: Wim, Clara, Finn, Lukas, Siv, Yusuf, Hugo, Elin, Bodil, Edda, Wilma, Goran, Saga, Wade, Jem, Felix, Mads, Willa, Frode, Iris, Elio, Disa, Celia, Ilan, Ximena, Freya, Zia, Mats, Zane
- Round 50: Iris, Zane, Freya, Lukas, Disa, Elin, Zia, Wade, Ilan, Elio, Willa, Felix, Ximena, Hugo, Bodil, Yusuf, Clara, Celia, Wim, Siv, Wilma, Saga, Frode, Mads, Goran, Edda, Jem, Finn, Mats
- Round 51: Goran, Wilma, Ximena, Willa, Mads, Jem, Zane, Mats, Zia, Wade, Celia, Ilan, Bodil, Clara, Disa, Finn, Wim, Saga, Felix, Frode, Siv, Hugo, Iris, Edda, Lukas, Elio, Yusuf, Elin, Freya
- Round 52: Goran, Ximena, Zane, Saga, Clara, Edda, Felix, Wim, Mads, Frode, Zia, Iris, Ilan, Jem, Elin, Yusuf, Celia, Finn, Bodil, Mats, Hugo, Disa, Willa, Elio, Wilma, Lukas, Wade, Siv, Freya
- Round 53: Yusuf, Wilma, Lukas, Hugo, Felix, Zane, Bodil, Goran, Wade, Finn, Mads, Ximena, Disa, Freya, Celia, Jem, Iris, Frode, Saga, Elio, Siv, Edda, Mats, Zia, Elin, Wim, Ilan, Willa, Clara
- Round 54: Elin, Wade, Celia, Bodil, Iris, Lukas, Clara, Mats, Ilan, Siv, Freya, Finn, Mads, Ximena, Edda, Saga, Hugo, Elio, Frode, Zane, Yusuf, Goran, Zia, Willa, Felix, Wilma, Wim, Jem, Disa
- Round 55: Lukas, Freya, Mads, Zia, Wilma, Wade, Goran, Yusuf, Celia, Siv, Felix, Ilan, Hugo, Saga, Finn, Clara, Willa, Zane, Wim, Bodil, Ximena, Jem, Frode, Disa, Edda, Elio, Elin, Mats, Iris
- Round 56: Goran, Willa, Wim, Mats, Wade, Yusuf, Felix, Saga, Wilma, Elio, Disa, Edda, Frode, Zane, Clara, Ilan, Siv, Hugo, Lukas, Jem, Elin, Bodil, Celia, Freya, Ximena, Zia, Finn, Iris, Mads
- Round 57: Iris, Saga, Siv, Willa, Elin, Celia, Frode, Lukas, Yusuf, Bodil, Freya, Ilan, Wim, Jem, Edda, Zane, Zia, Hugo, Disa, Wade, Finn, Goran, Mats, Mads, Felix, Wilma, Elio, Clara, Ximena
- Round 58: Iris, Clara, Hugo, Jem, Celia, Goran, Ximena, Mats, Frode, Siv, Willa, Mads, Finn, Felix, Elio, Ilan, Zia, Elin, Wilma, Lukas, Wim, Disa, Freya, Yusuf, Saga, Zane, Bodil, Wade, Edda
- Round 59: Jem, Wim, Zane, Iris, Zia, Edda, Ilan, Ximena, Elin, Clara, Saga, Elio, Freya, Disa, Felix, Celia, Lukas, Frode, Siv, Bodil, Goran, Yusuf, Hugo, Willa, Finn, Mads, Wilma, Wade, Mats
- Round 60: Disa, Iris, Goran, Willa, Edda, Ilan, Freya, Elin, Saga, Celia, Yusuf, Zane, Clara, Elio, Wim, Jem, Mads, Wilma, Ximena, Lukas, Felix, Zia, Mats, Finn, Frode, Hugo, Wade, Siv, Bodil
- Round 61: Edda, Felix, Saga, Iris, Wilma, Clara, Willa, Wim, Ximena, Mads, Disa, Ilan, Freya, Hugo, Mats, Lukas, Siv, Goran, Frode, Zane, Elin, Elio, Zia, Finn, Celia, Jem, Bodil, Wade, Yusuf
- Round 62: Disa, Jem, Zia, Yusuf, Hugo, Lukas, Ximena, Siv, Frode, Mats, Clara, Freya, Iris, Wim, Elin, Ilan, Felix, Mads, Bodil, Willa, Finn, Edda, Elio, Saga, Wilma, Goran, Celia, Wade, Zane
- Round 63: Iris, Yusuf, Ilan, Bodil, Siv, Zia, Wim, Goran, Elin, Celia, Wade, Lukas, Disa, Saga, Mats, Finn, Zane, Willa, Jem, Frode, Hugo, Felix, Edda, Ximena, Elio, Freya, Mads, Clara, Wilma
- Round 64: Celia, Disa, Finn, Wade, Siv, Hugo, Iris, Willa, Clara, Jem, Bodil, Zia, Felix, Ilan, Zane, Wim, Ximena, Elio, Wilma, Elin, Lukas, Freya, Goran, Mats, Saga, Edda, Yusuf, Mads, Frode
- Round 65: Freya, Elio, Finn, Zia, Willa, Frode, Mats, Celia, Elin, Wim, Yusuf, Zane, Edda, Wade, Mads, Iris, Bodil, Goran, Clara, Jem, Ilan, Wilma, Saga, Hugo, Disa, Lukas, Ximena, Felix, Siv
- Round 66: Jem, Goran, Disa, Willa, Siv, Ilan, Iris, Elin, Lukas, Freya, Hugo, Clara, Bodil, Wilma, Yusuf, Mats, Wim, Saga, Finn, Celia, Frode, Zane, Felix, Mads, Wade, Zia, Ximena, Edda, Elio
- Round 67: Goran, Celia, Jem, Mads, Wade, Felix, Willa, Lukas, Mats, Edda, Hugo, Elio, Wim, Disa, Saga, Yusuf, Clara, Zane, Freya, Wilma, Zia, Bodil, Ximena, Ilan, Iris, Finn, Frode, Siv, Elin
- Round 68: Yusuf, Ximena, Wade, Saga, Hugo, Clara, Willa, Siv, Bodil, Mads, Goran, Ilan, Mats, Zane, Zia, Elio, Felix, Wim, Edda, Iris, Disa, Freya, Frode, Celia, Jem, Finn, Wilma, Lukas, Elin
- Round 69: Felix, Freya, Disa, Wilma, Goran, Zia, Finn, Mads, Clara, Jem, Saga, Wade, Ilan, Elin, Siv, Lukas, Wim, Willa, Zane, Bodil, Celia, Elio, Ximena, Iris, Frode, Edda, Yusuf, Mats, Hugo
- Round 70: Edda, Mats, Elin, Yusuf, Ilan, Zane, Iris, Zia, Celia, Goran, Wade, Disa, Lukas, Jem, Elio, Freya, Bodil, Wilma, Felix, Frode, Clara, Saga, Willa, Ximena, Finn, Siv, Hugo, Mads, Wim
- Round 71: Clara, Wilma, Wade, Bodil, Elio, Mats, Freya, Yusuf, Zia, Iris, Felix, Zane, Frode, Siv, Elin, Mads, Willa, Hugo, Saga, Wim, Disa, Finn, Jem, Ximena, Ilan, Lukas, Goran, Edda, Celia
- Round 72: Lukas, Felix, Jem, Freya, Disa, Wade, Siv, Ilan, Ximena, Mats, Mads, Clara, Zia, Celia, Edda, Finn, Wim, Willa, Frode, Yusuf, Wilma, Elio, Iris, Bodil, Goran, Zane, Elin, Hugo, Saga
- Round 73: Zane, Mads, Hugo, Saga, Mats, Goran, Clara, Jem, Willa, Elio, Disa, Wade, Wim, Ximena, Bodil, Zia, Finn, Edda, Lukas, Celia, Elin, Wilma, Freya, Frode, Yusuf, Iris, Siv, Felix, Ilan
- Round 74: Finn, Yusuf, Disa, Elin, Elio, Mats, Ximena, Iris, Wim, Willa, Celia, Wade, Siv, Saga, Jem, Goran, Ilan, Clara, Hugo, Wilma, Zia, Felix, Zane, Lukas, Mads, Edda, Frode, Bodil, Freya
- Round 75: Mats, Ilan, Goran, Hugo, Jem, Wade, Lukas, Elio, Elin, Saga, Celia, Ximena, Clara, Disa, Finn, Zia, Felix, Bodil, Iris, Yusuf, Freya, Zane, Wim, Mads, Edda, Siv, Willa, Wilma, Frode
- Round 76: Willa, Zane, Finn, Mats, Siv, Goran, Wilma, Elio, Jem, Ximena, Wade, Iris, Edda, Clara, Celia, Felix, Mads, Freya, Wim, Saga, Ilan, Elin, Zia, Hugo, Yusuf, Lukas, Frode, Bodil, Disa
- Round 77: Elin, Jem, Hugo, Zia, Siv, Lukas, Elio, Saga, Ximena, Edda, Finn, Wade, Ilan, Yusuf, Disa, Celia, Wilma, Iris, Goran, Freya, Zane, Mats, Frode, Felix, Willa, Mads, Wim, Bodil, Clara
- Round 78: Ilan, Freya, Wade, Zia, Bodil, Mats, Hugo, Goran, Finn, Siv, Clara, Elio, Frode, Jem, Willa, Yusuf, Wilma, Iris, Lukas, Felix, Elin, Celia, Ximena, Mads, Disa, Zane, Saga, Wim, Edda
- Round 79: Ximena, Elio, Siv, Celia, Mads, Iris, Elin, Willa, Wim, Mats, Felix, Yusuf, Clara, Finn, Freya, Disa, Hugo, Wilma, Zia, Frode, Wade, Jem, Edda, Zane, Bodil, Goran, Saga, Ilan, Lukas
- Round 80: Ximena, Saga, Disa, Willa, Bodil, Yusuf, Freya, Wade, Celia, Wilma, Siv, Felix, Clara, Finn, Edda, Iris, Jem, Zane, Zia, Hugo, Elio, Lukas, Goran, Mads, Ilan, Wim, Mats, Elin, Frode

## Harvest noise draws

| round | agent | camp | x | stock before | efficiency | noise | yield |
|---|---|---|---|---|---|---|---|
| 1 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 71.611 | 0.08 | -0.0848 | 0.374 |
| 1 | Disa | camp5 | [3, 12, 3, 12, 3, 12, 3, 12] | 71.611 | 0.08 | 0.0454 | 0.504 |
| 1 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 94.44 | 0.08 | -0.0858 | 0.519 |
| 1 | Lukas | camp4 | [12, 4, 12, 4, 12, 4, 12, 4] | 94.44 | 0.0 | 0.0019 | 0.002 |
| 1 | Lukas | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 74.685 | 0.4375 | -0.0785 | 2.536 |
| 1 | Lukas | camp1 | [4, 12, 4, 12, 4, 12, 4, 12] | 74.685 | 0.25 | 0.7317 | 2.225 |
| 1 | Mads | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 71.611 | 0.08 | -0.0298 | 0.428 |
| 1 | Mads | camp5 | [4, 12, 4, 12, 4, 12, 4, 12] | 71.611 | 0.0 | -0.1857 | 0.000 |
| 1 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 76.536 | 1.0 | 0.5618 | 6.685 |
| 1 | Iris | camp3 | [4, 12, 4, 12, 4, 12, 4, 12] | 76.536 | 0.35 | -0.2988 | 1.844 |
| 1 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 76.536 | 1.0 | 0.1116 | 6.235 |
| 1 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 76.536 | 1.0 | -0.6646 | 5.458 |
| 1 | Felix | camp3 | [4, 12, 4, 12, 4, 12, 4, 12] | 76.536 | 0.35 | 0.0483 | 2.191 |
| 1 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 76.536 | 1.0 | -0.1575 | 5.965 |
| 1 | Clara | camp3 | [4, 12, 4, 12, 4, 12, 4, 12] | 76.536 | 0.35 | -0.1467 | 1.996 |
| 1 | Yusuf | camp1 | [0, 0, 0, 0, 0, 0, 0, 0] | 74.685 | 0.0625 | 0.4328 | 0.806 |
| 1 | Yusuf | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 74.685 | 0.7656 | -0.462 | 4.112 |
| 1 | Yusuf | camp2 | [0, 0, 0, 0, 0, 0, 0, 0] | 78.773 | 0.0052 | -0.1961 | 0.000 |
| 1 | Yusuf | camp2 | [15, 15, 15, 15, 15, 15, 15, 15] | 78.773 | 0.0006 | -0.4366 | 0.000 |
| 1 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 94.44 | 0.08 | 0.1727 | 0.777 |
| 1 | Willa | camp4 | [4, 10, 6, 12, 8, 3, 9, 7] | 94.44 | 0.08 | -0.3497 | 0.255 |
| 1 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 94.44 | 0.08 | -0.0212 | 0.583 |
| 1 | Zane | camp4 | [5, 10, 5, 10, 5, 10, 5, 10] | 94.44 | 0.0 | -0.1631 | 0.000 |
| 1 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 94.44 | 0.08 | -0.0662 | 0.538 |
| 1 | Mats | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 76.536 | 1.0 | -0.4158 | 5.707 |
| 1 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 74.685 | 0.4375 | 0.2756 | 2.890 |
| 1 | Elio | camp1 | [5, 10, 5, 10, 5, 10, 5, 10] | 74.685 | 0.2969 | -0.5189 | 1.255 |
| 2 | Mads | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 71.833 | 0.08 | 0.1223 | 0.582 |
| 2 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 71.833 | 1.0 | 0.0575 | 5.804 |
| 2 | Elio | camp1 | [10, 10, 10, 10, 10, 10, 10, 10] | 64.31 | 0.5312 | -0.0311 | 2.702 |
| 2 | Elio | camp1 | [6, 6, 6, 6, 6, 6, 6, 6] | 64.31 | 0.3438 | 0.7693 | 2.538 |
| 2 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.658 | 0.08 | 0.0927 | 0.686 |
| 2 | Lukas | camp4 | [10, 8, 10, 8, 10, 8, 10, 8] | 92.658 | 0.0 | -0.1952 | 0.000 |
| 2 | Lukas | camp1 | [8, 8, 8, 8, 10, 10, 10, 10] | 64.31 | 0.4688 | -0.1435 | 2.268 |
| 2 | Lukas | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 64.31 | 0.4375 | 0.0727 | 2.324 |
| 2 | Clara | camp3 | [10, 10, 10, 10, 10, 10, 10, 10] | 43.544 | 0.15 | -0.7764 | 0.000 |
| 2 | Clara | camp3 | [8, 8, 8, 8, 12, 12, 12, 12] | 43.544 | 0.35 | -0.151 | 1.068 |
| 2 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 64.31 | 0.4375 | 0.5675 | 2.818 |
| 2 | Yusuf | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 64.31 | 0.625 | 0.1982 | 3.414 |
| 2 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.383 | 0.2279 | -0.1331 | 1.332 |
| 2 | Yusuf | camp2 | [4, 4, 4, 4, 4, 4, 4, 4] | 80.383 | 0.142 | 0.0519 | 0.965 |
| 2 | Wim | camp3 | [0, 0, 0, 0, 0, 0, 0, 0] | 43.544 | 0.15 | 0.1232 | 0.646 |
| 2 | Wim | camp6 | [0] | 70.917 | 0.0833 | 0.0 | 0.500 |
| 2 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.658 | 0.08 | 0.0582 | 0.651 |
| 2 | Zane | camp4 | [10, 8, 6, 8, 8, 8, 8, 8] | 92.658 | 0.08 | -0.0469 | 0.546 |
| 2 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 43.544 | 1.0 | 0.7076 | 4.191 |
| 2 | Iris | camp3 | [9, 9, 9, 9, 7, 7, 7, 7] | 43.544 | 0.15 | 0.2517 | 0.774 |
| 2 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.658 | 0.08 | 0.0127 | 0.606 |
| 2 | Willa | camp4 | [9, 8, 8, 8, 8, 8, 8, 8] | 92.658 | 0.08 | -0.0806 | 0.512 |
| 2 | Mats | camp3 | [10, 6, 8, 8, 10, 6, 8, 8] | 43.544 | 1.0 | 0.4858 | 3.969 |
| 2 | Mats | camp4 | [10, 6, 8, 8, 10, 6, 8, 8] | 92.658 | 0.08 | -0.2771 | 0.316 |
| 2 | Disa | camp5 | [3, 12, 3, 12, 3, 12, 3, 12] | 71.833 | 0.0 | -0.0362 | 0.000 |
| 2 | Disa | camp5 | [0, 15, 0, 15, 0, 15, 0, 15] | 71.833 | 0.0 | -0.0395 | 0.000 |
| 2 | Disa | camp6 | [7] | 70.917 | 0.0 | 0.0 | 0.000 |
| 2 | Disa | camp6 | [12345] | 70.917 | 0.125 | 0.0 | 0.750 |
| 2 | Felix | camp3 | [10, 10, 10, 10, 10, 10, 10, 10] | 43.544 | 0.15 | -0.4802 | 0.042 |
| 2 | Felix | camp3 | [8, 8, 8, 8, 6, 6, 6, 6] | 43.544 | 1.0 | -0.1132 | 3.370 |
| 3 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 90.496 | 0.08 | 0.0647 | 0.644 |
| 3 | Willa | camp4 | [7, 8, 8, 8, 8, 8, 8, 8] | 90.496 | 0.08 | -0.0768 | 0.502 |
| 3 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 66.966 | 0.0 | -0.0049 | 0.000 |
| 3 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 52.432 | 0.4375 | -0.5666 | 1.269 |
| 3 | Elio | camp1 | [9, 8, 8, 9, 8, 8, 9, 8] | 52.432 | 0.5 | 0.0631 | 2.160 |
| 3 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 33.712 | 1.0 | -0.1883 | 2.509 |
| 3 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 33.712 | 1.0 | 0.2963 | 2.993 |
| 3 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 33.712 | 1.0 | 0.056 | 2.753 |
| 3 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 33.712 | 1.0 | 0.2187 | 2.916 |
| 3 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 90.496 | 0.08 | -0.0263 | 0.553 |
| 3 | Zane | camp4 | [8, 10, 8, 6, 8, 8, 8, 8] | 90.496 | 0.08 | -0.1739 | 0.405 |
| 3 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 52.432 | 0.7656 | 0.59 | 3.802 |
| 3 | Lukas | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 52.432 | 0.625 | -0.2697 | 2.352 |
| 3 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 90.496 | 0.08 | -0.1429 | 0.436 |
| 3 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 90.496 | 1.0 | -0.288 | 6.952 |
| 3 | Yusuf | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 52.432 | 0.7188 | 0.0148 | 3.030 |
| 3 | Yusuf | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 52.432 | 0.625 | 0.4151 | 3.037 |
| 3 | Yusuf | camp2 | [10, 10, 10, 10, 10, 10, 10, 10] | 79.604 | 0.0996 | 0.1004 | 0.734 |
| 3 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 79.604 | 0.2279 | 0.0107 | 1.462 |
| 3 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 66.966 | 0.08 | 0.0488 | 0.477 |
| 3 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 66.966 | 0.08 | -0.0576 | 0.371 |
| 3 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 33.712 | 1.0 | 0.3038 | 3.001 |
| 3 | Felix | camp3 | [9, 9, 9, 9, 8, 8, 8, 8] | 33.712 | 0.15 | 0.5951 | 1.000 |
| 3 | Mats | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 33.712 | 1.0 | -0.1149 | 2.582 |
| 3 | Mats | camp4 | [12, 6, 8, 8, 12, 6, 8, 8] | 90.496 | 0.0 | -0.3008 | 0.000 |
| 3 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 33.712 | 1.0 | -0.2064 | 2.491 |
| 3 | Wim | camp6 | [8] | 70.917 | 0.0 | 0.0 | 0.000 |
| 4 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 17.311 | 1.0 | -0.3417 | 1.043 |
| 4 | Iris | camp3 | [6, 6, 6, 6, 6, 6, 6, 6] | 17.311 | 0.15 | 0.0829 | 0.291 |
| 4 | Yusuf | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 41.332 | 0.7188 | 0.1767 | 2.553 |
| 4 | Yusuf | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 41.332 | 0.6719 | 0.6815 | 2.903 |
| 4 | Yusuf | camp2 | [9, 9, 9, 9, 9, 9, 9, 9] | 78.971 | 0.1646 | -0.262 | 0.778 |
| 4 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 78.971 | 0.2279 | -0.1631 | 1.277 |
| 4 | Wim | camp3 | [6, 6, 6, 6, 6, 6, 6, 6] | 17.311 | 0.15 | -0.0973 | 0.110 |
| 4 | Wim | camp3 | [5, 5, 5, 5, 5, 5, 5, 5] | 17.311 | 0.15 | 0.1413 | 0.349 |
| 4 | Mads | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 67.78 | 0.0 | 0.1043 | 0.104 |
| 4 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 67.78 | 0.08 | 0.0672 | 0.501 |
| 4 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 17.311 | 1.0 | 0.1983 | 1.583 |
| 4 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 82.464 | 1.0 | 0.1519 | 6.749 |
| 4 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 82.464 | 1.0 | 0.0987 | 6.696 |
| 4 | Disa | camp6 | [48213] | 70.917 | 0.0833 | 0.0 | 0.500 |
| 4 | Disa | camp6 | [7731] | 70.917 | 0.0 | 0.0 | 0.000 |
| 4 | Disa | camp5 | [7, 7, 7, 7, 8, 8, 8, 8] | 67.78 | 0.0 | 0.0172 | 0.017 |
| 4 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 67.78 | 0.08 | 0.1001 | 0.534 |
| 4 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 82.464 | 1.0 | 0.2337 | 6.831 |
| 4 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 82.464 | 1.0 | 0.1692 | 6.766 |
| 4 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 17.311 | 1.0 | 0.0313 | 1.416 |
| 4 | Elio | camp1 | [9, 8, 8, 9, 8, 8, 9, 8] | 41.332 | 0.5 | -0.4828 | 1.170 |
| 4 | Elio | camp1 | [10, 8, 8, 10, 8, 8, 10, 8] | 41.332 | 0.5625 | -0.315 | 1.545 |
| 4 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 82.464 | 1.0 | -0.1389 | 6.458 |
| 4 | Lukas | camp4 | [7, 7, 7, 7, 7, 7, 7, 7] | 82.464 | 0.0 | -0.1249 | 0.000 |
| 4 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 41.332 | 0.7656 | -0.6564 | 1.875 |
| 4 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 41.332 | 0.7656 | 0.2071 | 2.739 |
| 4 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 82.464 | 1.0 | 0.1564 | 6.754 |
| 4 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 82.464 | 1.0 | -0.1675 | 6.430 |
| 5 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 38.235 | 1.0 | -0.0193 | 3.040 |
| 5 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 38.235 | 1.0 | 0.1101 | 3.169 |
| 5 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 38.235 | 1.0 | 0.035 | 3.094 |
| 5 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 38.235 | 1.0 | -0.0452 | 3.014 |
| 5 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 68.265 | 1.0 | 0.0315 | 5.493 |
| 5 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 68.265 | 1.0 | -0.0422 | 5.419 |
| 5 | Wim | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 14.981 | 1.0 | 0.1932 | 1.392 |
| 5 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 68.265 | 1.0 | -0.0278 | 5.433 |
| 5 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 9] | 68.265 | 0.08 | 0.0753 | 0.512 |
| 5 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 9] | 38.235 | 1.0 | 0.1006 | 3.159 |
| 5 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 38.235 | 1.0 | 0.0368 | 3.096 |
| 5 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 32.97 | 0.7656 | 0.2159 | 2.235 |
| 5 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 32.97 | 0.7656 | 0.1754 | 2.195 |
| 5 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 14.981 | 1.0 | 0.0916 | 1.290 |
| 5 | Elio | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 32.97 | 0.6719 | -0.0248 | 1.747 |
| 5 | Elio | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 32.97 | 0.7188 | -0.7319 | 1.164 |
| 5 | Yusuf | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 32.97 | 0.6719 | 0.8371 | 2.609 |
| 5 | Yusuf | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 32.97 | 0.7188 | -0.1546 | 1.741 |
| 5 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 78.515 | 0.2279 | 0.0487 | 1.480 |
| 5 | Yusuf | camp2 | [9, 9, 9, 9, 9, 9, 9, 9] | 78.515 | 0.1646 | -0.0584 | 0.976 |
| 5 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 14.981 | 1.0 | 0.0752 | 1.274 |
| 5 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 14.981 | 1.0 | 0.2721 | 1.471 |
| 5 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 38.235 | 1.0 | 0.0578 | 3.117 |
| 5 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 38.235 | 1.0 | -0.0929 | 2.966 |
| 6 | Elio | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 25.31 | 0.6719 | 0.3205 | 1.681 |
| 6 | Elio | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 25.31 | 0.7188 | -0.165 | 1.290 |
| 6 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 17.589 | 1.0 | 0.1025 | 1.510 |
| 6 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 17.589 | 1.0 | 0.0704 | 1.478 |
| 6 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 17.589 | 1.0 | 0.1423 | 1.549 |
| 6 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 17.589 | 1.0 | 0.1187 | 1.526 |
| 6 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 53.035 | 0.08 | 0.0678 | 0.407 |
| 6 | Disa | camp5 | [10, 7, 8, 8, 10, 7, 8, 8] | 53.035 | 0.0 | -0.0986 | 0.000 |
| 6 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 11.745 | 1.0 | -0.1733 | 0.766 |
| 6 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 53.035 | 0.08 | -0.0058 | 0.334 |
| 6 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 53.035 | 0.08 | 0.0579 | 0.397 |
| 6 | Yusuf | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 25.31 | 0.6719 | 0.2864 | 1.647 |
| 6 | Yusuf | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 25.31 | 0.625 | 0.7832 | 2.049 |
| 6 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 77.683 | 0.2279 | -0.0289 | 1.387 |
| 6 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 77.683 | 0.2642 | -0.273 | 1.369 |
| 6 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 11.745 | 1.0 | -0.0821 | 0.857 |
| 6 | Lukas | camp4 | [7, 7, 7, 7, 9, 8, 8, 8] | 17.589 | 0.0 | -0.2744 | 0.000 |
| 6 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 9] | 17.589 | 1.0 | 0.223 | 1.630 |
| 6 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 25.31 | 0.7656 | 0.2633 | 1.814 |
| 6 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 25.31 | 0.7656 | -0.0116 | 1.539 |
| 6 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 17.589 | 1.0 | -0.0832 | 1.324 |
| 6 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 17.589 | 1.0 | -0.0075 | 1.400 |
| 6 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 11.745 | 1.0 | 0.3119 | 1.252 |
| 7 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 10.653 | 1.0 | 0.0563 | 0.909 |
| 7 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 9.633 | 1.0 | -0.1116 | 0.659 |
| 7 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 9.633 | 1.0 | -0.0745 | 0.696 |
| 7 | Yusuf | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 18.739 | 0.625 | -0.3758 | 0.561 |
| 7 | Yusuf | camp1 | [11, 11, 11, 11, 11, 11, 11, 11] | 18.739 | 0.5781 | 0.346 | 1.213 |
| 7 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 76.596 | 0.2279 | -0.0004 | 1.396 |
| 7 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 76.596 | 0.2279 | -0.1755 | 1.221 |
| 7 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 9.633 | 1.0 | -0.1714 | 0.599 |
| 7 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 9.633 | 1.0 | 0.3498 | 1.120 |
| 7 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 53.768 | 0.08 | -0.0752 | 0.269 |
| 7 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 53.768 | 0.08 | -0.0219 | 0.322 |
| 7 | Elio | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 18.739 | 0.625 | -0.6492 | 0.288 |
| 7 | Elio | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 18.739 | 0.7656 | 0.5363 | 1.684 |
| 7 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 10.653 | 1.0 | 0.2337 | 1.086 |
| 7 | Wim | camp3 | [9, 9, 9, 9, 9, 9, 9, 9] | 10.653 | 0.15 | -0.1888 | 0.000 |
| 7 | Wim | camp6 | [0] | 70.917 | 0.0 | 0.0 | 0.000 |
| 7 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 9.633 | 1.0 | -0.1865 | 0.584 |
| 7 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 9.633 | 1.0 | 0.0596 | 0.830 |
| 7 | Disa | camp5 | [8, 7, 8, 8, 8, 7, 8, 8] | 53.768 | 0.0 | -0.0665 | 0.000 |
| 7 | Disa | camp5 | [9, 7, 7, 8, 9, 7, 7, 8] | 53.768 | 0.0 | 0.0107 | 0.011 |
| 7 | Disa | camp6 | [7] | 70.917 | 0.0 | 0.0 | 0.000 |
| 7 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 9, 9] | 9.633 | 1.0 | 0.1003 | 0.871 |
| 7 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 9] | 9.633 | 1.0 | -0.0717 | 0.699 |
| 7 | Lukas | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 18.739 | 0.7656 | -0.5038 | 0.644 |
| 7 | Lukas | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 18.739 | 0.625 | -0.2566 | 0.680 |
| 7 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 10.653 | 1.0 | -0.2766 | 0.576 |
| 8 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 10] | 5.053 | 1.0 | 0.0946 | 0.499 |
| 8 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 9] | 5.053 | 1.0 | 0.0116 | 0.416 |
| 8 | Lukas | camp1 | [11, 11, 11, 11, 11, 11, 11, 11] | 16.446 | 0.5781 | 0.0663 | 0.827 |
| 8 | Lukas | camp1 | [10, 10, 10, 10, 10, 10, 10, 10] | 16.446 | 0.5312 | -0.0607 | 0.638 |
| 8 | Wim | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 9.719 | 1.0 | 0.06 | 0.838 |
| 8 | Wim | camp6 | [1] | 70.917 | 0.0 | 0.0 | 0.000 |
| 8 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 9.719 | 1.0 | -0.0367 | 0.741 |
| 8 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 9.719 | 1.0 | -0.1052 | 0.672 |
| 8 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 55.034 | 0.08 | -0.0265 | 0.326 |
| 8 | Disa | camp5 | [9, 8, 8, 8, 9, 8, 8, 8] | 55.034 | 0.0 | 0.1032 | 0.103 |
| 8 | Disa | camp6 | [48213] | 70.917 | 0.0417 | 0.0 | 0.250 |
| 8 | Disa | camp6 | [90517] | 70.917 | 0.0 | 0.0 | 0.000 |
| 8 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 5.053 | 1.0 | -0.334 | 0.070 |
| 8 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 5.053 | 1.0 | -0.0477 | 0.357 |
| 8 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 5.053 | 1.0 | -0.3032 | 0.101 |
| 8 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 5.053 | 1.0 | 0.1344 | 0.539 |
| 8 | Mats | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 5.053 | 1.0 | 0.0803 | 0.484 |
| 8 | Mats | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 9.719 | 1.0 | 0.2488 | 1.026 |
| 8 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.719 | 1.0 | 0.1219 | 0.899 |
| 8 | Yusuf | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 16.446 | 0.7188 | 0.3157 | 1.261 |
| 8 | Yusuf | camp1 | [12, 12, 12, 12, 12, 12, 12, 12] | 16.446 | 0.625 | -0.0656 | 0.757 |
| 8 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 75.705 | 0.2279 | 0.1321 | 1.512 |
| 8 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 75.705 | 0.2279 | -0.3886 | 0.992 |
| 8 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 55.034 | 1.0 | -0.0017 | 4.401 |
| 8 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 55.034 | 1.0 | -0.0303 | 4.372 |
| 8 | Elio | camp1 | [15, 15, 15, 15, 0, 0, 0, 0] | 16.446 | 0.5312 | 0.1946 | 0.894 |
| 8 | Elio | camp1 | [0, 0, 0, 0, 15, 15, 15, 15] | 16.446 | 0.2969 | -0.4254 | 0.000 |
| 9 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 47.691 | 1.0 | -0.0046 | 3.811 |
| 9 | Disa | camp5 | [10, 7, 8, 8, 9, 7, 8, 8] | 47.691 | 0.0 | 0.065 | 0.065 |
| 9 | Disa | camp6 | [271828] | 70.917 | 0.0 | 0.0 | 0.000 |
| 9 | Disa | camp6 | [314159] | 70.917 | 0.0417 | 0.0 | 0.250 |
| 9 | Zane | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 3.401 | 1.0 | -0.4341 | 0.000 |
| 9 | Wim | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 7.052 | 1.0 | -0.4307 | 0.133 |
| 9 | Wim | camp6 | [256] | 70.917 | 0.0 | 0.0 | 0.000 |
| 9 | Mats | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 7.052 | 1.0 | 0.6181 | 1.182 |
| 9 | Mats | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 7.052 | 1.0 | 0.3658 | 0.930 |
| 9 | Felix | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 7.052 | 1.0 | 0.6808 | 1.245 |
| 9 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 7.052 | 1.0 | 0.1333 | 0.697 |
| 9 | Lukas | camp4 | [7, 7, 7, 7, 8, 9, 9, 9] | 3.401 | 0.0 | 0.0741 | 0.074 |
| 9 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 10, 10] | 3.401 | 1.0 | -0.1847 | 0.087 |
| 9 | Lukas | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 14.576 | 0.7188 | -0.2067 | 0.631 |
| 9 | Lukas | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 14.576 | 0.6719 | 0.4469 | 1.230 |
| 9 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 3.401 | 1.0 | -0.0436 | 0.229 |
| 9 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 7.052 | 1.0 | -0.0448 | 0.519 |
| 9 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 47.691 | 1.0 | 0.0748 | 3.890 |
| 9 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 47.691 | 1.0 | -0.0794 | 3.736 |
| 9 | Yusuf | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 14.576 | 0.6719 | 0.088 | 0.871 |
| 9 | Yusuf | camp1 | [15, 15, 15, 15, 15, 15, 15, 15] | 14.576 | 0.7656 | -0.4463 | 0.446 |
| 9 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 74.972 | 0.2279 | 0.1164 | 1.483 |
| 9 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 74.972 | 0.2279 | -0.0935 | 1.273 |
| 9 | Elio | camp1 | [15, 15, 0, 0, 0, 0, 0, 0] | 14.576 | 0.5312 | -0.0676 | 0.552 |
| 9 | Elio | camp1 | [0, 0, 15, 15, 0, 0, 0, 0] | 14.576 | 0.0625 | 0.545 | 0.618 |
| 10 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 74.023 | 0.2279 | 0.1055 | 1.455 |
| 10 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 74.023 | 0.2279 | -0.2261 | 1.124 |
| 10 | Elio | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 12.499 | 0.6719 | -0.3222 | 0.350 |
| 10 | Elio | camp1 | [14, 14, 14, 14, 0, 0, 0, 0] | 12.499 | 0.5 | -0.2068 | 0.293 |
| 10 | Zane | camp4 | [7, 7, 7, 7, 8, 9, 9, 9] | 3.569 | 0.0 | 0.188 | 0.188 |
| 10 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 3.474 | 1.0 | -0.6576 | 0.000 |
| 10 | Wim | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 3.474 | 1.0 | -0.1563 | 0.122 |
| 10 | Wim | camp6 | [1000] | 70.917 | 0.125 | 0.0 | 0.750 |
| 10 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 3.474 | 1.0 | 0.3989 | 0.677 |
| 10 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 9, 8] | 38.063 | 0.0 | -0.0757 | 0.000 |
| 10 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 38.063 | 0.08 | -0.0003 | 0.243 |
| 10 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 38.063 | 0.08 | -0.0303 | 0.213 |
| 10 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 9] | 38.063 | 0.08 | 0.0524 | 0.296 |
| 10 | Lukas | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 12.499 | 0.6719 | 0.1806 | 0.852 |
| 10 | Lukas | camp1 | [13, 13, 13, 13, 12, 12, 14, 14] | 12.499 | 0.7188 | 0.2089 | 0.928 |
| 10 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 9] | 3.569 | 1.0 | -0.1134 | 0.172 |
| 10 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 3.569 | 1.0 | 0.0584 | 0.344 |
| 10 | Felix | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 3.474 | 1.0 | 0.2696 | 0.548 |
| 11 | Wim | camp6 | [8192] | 70.917 | 0.0417 | 0.0 | 0.250 |
| 11 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 9] | 39.082 | 0.08 | 0.0754 | 0.326 |
| 11 | Mads | camp5 | [9, 7, 8, 8, 9, 7, 8, 8] | 39.082 | 0.08 | -0.082 | 0.168 |
| 11 | Felix | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 2.703 | 1.0 | 0.2819 | 0.498 |
| 11 | Willa | camp4 | [7, 7, 7, 7, 8, 8, 8, 8] | 3.449 | 1.0 | 0.1269 | 0.403 |
| 11 | Elio | camp1 | [14, 14, 14, 14, 14, 14, 14, 14] | 12.071 | 0.7188 | -0.3157 | 0.378 |
| 11 | Clara | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 2.703 | 1.0 | 0.0934 | 0.310 |
| 11 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 73.295 | 0.2279 | 0.3389 | 1.675 |
| 11 | Yusuf | camp2 | [9, 9, 9, 9, 9, 9, 9, 9] | 73.295 | 0.1646 | 0.1438 | 1.109 |
| 11 | Lukas | camp1 | [13, 13, 13, 13, 13, 13, 13, 13] | 12.071 | 0.6719 | 1.1121 | 1.761 |
| 11 | Lukas | camp4 | [7, 7, 7, 7, 8, 8, 8, 9] | 3.449 | 1.0 | -0.1401 | 0.136 |
| 11 | Iris | camp3 | [7, 7, 7, 7, 7, 7, 7, 7] | 2.703 | 1.0 | -0.7373 | 0.000 |
| 11 | Disa | camp6 | [48213] | 70.917 | 0.0417 | 0.0 | 0.250 |
| 11 | Disa | camp6 | [7719] | 70.917 | 0.0 | 0.0 | 0.000 |
| 11 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 9] | 39.082 | 0.08 | 0.0809 | 0.331 |
| 11 | Disa | camp5 | [9, 7, 8, 8, 9, 7, 8, 10] | 39.082 | 0.08 | -0.0871 | 0.163 |
| 73 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.938 | 0.08 | 0.3064 | 0.946 |
| 73 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 99.938 | 0.08 | 0.0458 | 0.685 |
| 73 | Mads | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 98.636 | 0.0 | -0.1648 | 0.000 |
| 73 | Mads | camp5 | [7, 9, 8, 8, 7, 9, 8, 8] | 98.636 | 0.0 | 0.0591 | 0.059 |
| 73 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.938 | 0.08 | 0.191 | 0.831 |
| 73 | Mats | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.914 | 1.0 | 0.1852 | 8.178 |
| 73 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.914 | 1.0 | -0.072 | 7.921 |
| 73 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.914 | 1.0 | -0.1889 | 7.804 |
| 73 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.938 | 0.08 | -0.1185 | 0.521 |
| 73 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 99.938 | 0.08 | 0.0633 | 0.703 |
| 73 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.995 | 0.4375 | 0.9922 | 4.492 |
| 73 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.995 | 0.4375 | -0.4711 | 3.029 |
| 73 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 98.636 | 0.08 | -0.0196 | 0.612 |
| 73 | Disa | camp5 | [10, 6, 10, 6, 10, 6, 10, 6] | 98.636 | 0.0 | 0.0105 | 0.010 |
| 73 | Disa | camp6 | [12345] | 70.917 | 0.0417 | 0.0 | 0.250 |
| 73 | Wim | camp3 | [8, 7, 6, 5, 4, 3, 2, 1] | 99.914 | 1.0 | -0.1745 | 7.819 |
| 73 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.938 | 0.08 | -0.0092 | 0.630 |
| 73 | Lukas | camp4 | [12, 4, 12, 4, 12, 4, 12, 4] | 99.938 | 0.0 | 0.1945 | 0.195 |
| 73 | Lukas | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.995 | 0.4375 | -0.663 | 2.837 |
| 73 | Lukas | camp1 | [4, 12, 4, 12, 4, 12, 4, 12] | 99.995 | 0.25 | -0.6748 | 1.325 |
| 73 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.995 | 0.4375 | -0.7213 | 2.779 |
| 73 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 99.995 | 0.3906 | 0.0498 | 3.175 |
| 73 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.918 | 0.2279 | 0.0583 | 1.880 |
| 73 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 99.918 | 0.2642 | 0.3822 | 2.494 |
| 73 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.914 | 1.0 | 0.1022 | 8.095 |
| 73 | Iris | camp3 | [12, 4, 10, 6, 8, 10, 4, 12] | 99.914 | 0.15 | -0.2813 | 0.918 |
| 73 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.914 | 1.0 | 0.6766 | 8.670 |
| 73 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 99.914 | 1.0 | 0.7165 | 8.710 |
| 74 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 82.359 | 0.4375 | -0.2669 | 2.616 |
| 74 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 82.359 | 0.3906 | 0.2069 | 2.781 |
| 74 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 95.552 | 0.2279 | 0.0574 | 1.799 |
| 74 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 95.552 | 0.2642 | 0.1876 | 2.207 |
| 74 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 98.056 | 0.08 | 0.0072 | 0.635 |
| 74 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 98.056 | 0.0 | -0.0441 | 0.000 |
| 74 | Disa | camp6 | [74001] | 70.917 | 0.0 | 0.0 | 0.000 |
| 74 | Disa | camp6 | [74002] | 70.917 | 0.0833 | 0.0 | 0.500 |
| 74 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 82.359 | 0.4375 | 0.1502 | 3.033 |
| 74 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 82.359 | 0.4375 | 0.1802 | 3.063 |
| 74 | Mats | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | -0.0877 | 3.257 |
| 74 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 95.437 | 0.08 | -0.0343 | 0.576 |
| 74 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | -0.3445 | 3.001 |
| 74 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | 0.2455 | 3.591 |
| 74 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | 0.073 | 3.418 |
| 74 | Wim | camp6 | [1] | 70.917 | 0.0833 | 0.0 | 0.500 |
| 74 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 95.437 | 0.08 | -0.058 | 0.553 |
| 74 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 95.437 | 0.08 | 0.0122 | 0.623 |
| 74 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | -0.6128 | 2.732 |
| 74 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | -0.1876 | 3.158 |
| 74 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | 0.4809 | 3.826 |
| 74 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 41.814 | 1.0 | 0.0629 | 3.408 |
| 74 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 95.437 | 0.08 | -0.2179 | 0.393 |
| 74 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 95.437 | 0.08 | -0.1089 | 0.502 |
| 74 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 95.437 | 0.08 | 0.1462 | 0.757 |
| 74 | Lukas | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 82.359 | 0.4375 | -0.683 | 2.200 |
| 74 | Lukas | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 82.359 | 0.3906 | -0.0598 | 2.514 |
| 74 | Mads | camp5 | [7, 9, 8, 8, 7, 9, 8, 8] | 98.056 | 0.0 | -0.0133 | 0.000 |
| 74 | Mads | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 98.056 | 0.0 | 0.0293 | 0.029 |
| 75 | Mats | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | 0.5058 | 2.074 |
| 75 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.773 | 0.08 | -0.0251 | 0.569 |
| 75 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.773 | 0.08 | 0.1216 | 0.715 |
| 75 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.773 | 0.08 | -0.0233 | 0.570 |
| 75 | Lukas | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 68.802 | 0.3906 | 0.0232 | 2.173 |
| 75 | Lukas | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 68.802 | 0.3906 | -0.0374 | 2.113 |
| 75 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 68.802 | 0.4375 | -0.0087 | 2.399 |
| 75 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 68.802 | 0.4375 | -0.6499 | 1.758 |
| 75 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | -0.0559 | 1.513 |
| 75 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | -0.0691 | 1.499 |
| 75 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 97.535 | 0.0 | -0.0361 | 0.000 |
| 75 | Disa | camp6 | [75003] | 70.917 | 0.0 | 0.0 | 0.000 |
| 75 | Disa | camp6 | [75011] | 70.917 | 0.0417 | 0.0 | 0.250 |
| 75 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | 0.1087 | 1.677 |
| 75 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | 0.236 | 1.805 |
| 75 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | -0.5314 | 1.037 |
| 75 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | 0.017 | 1.586 |
| 75 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 68.802 | 0.4375 | 0.4547 | 2.863 |
| 75 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 68.802 | 0.3906 | -0.3789 | 1.771 |
| 75 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 91.955 | 0.2279 | 0.1754 | 1.852 |
| 75 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 91.955 | 0.2642 | 0.156 | 2.100 |
| 75 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.773 | 0.08 | 0.367 | 0.961 |
| 75 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 92.773 | 0.08 | 0.0181 | 0.612 |
| 75 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 19.608 | 1.0 | -0.2148 | 1.354 |
| 75 | Wim | camp6 | [2] | 70.917 | 0.0 | 0.0 | 0.000 |
| 75 | Mads | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 97.535 | 0.0 | -0.0801 | 0.000 |
| 75 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 92.773 | 0.08 | -0.172 | 0.422 |
| 75 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 92.773 | 0.08 | 0.1127 | 0.706 |
| 76 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 89.356 | 0.08 | 0.3411 | 0.913 |
| 76 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 89.356 | 0.08 | 0.1173 | 0.689 |
| 76 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 89.356 | 0.08 | 0.0953 | 0.667 |
| 76 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 89.356 | 0.08 | -0.1728 | 0.399 |
| 76 | Mats | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | 0.4988 | 1.281 |
| 76 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 89.356 | 0.08 | 0.134 | 0.706 |
| 76 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 59.64 | 0.4375 | -0.0033 | 2.084 |
| 76 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 59.64 | 0.4375 | -0.3795 | 1.708 |
| 76 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | 0.2951 | 1.077 |
| 76 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | -0.0553 | 0.727 |
| 76 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | 0.0949 | 0.877 |
| 76 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | 0.5518 | 1.334 |
| 76 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | 0.2231 | 1.005 |
| 76 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | 0.0376 | 0.820 |
| 76 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 9.774 | 1.0 | -0.0255 | 0.756 |
| 76 | Wim | camp6 | [92847] | 70.917 | 0.0 | 0.0 | 0.000 |
| 76 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 59.64 | 0.4375 | -0.3087 | 1.779 |
| 76 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 59.64 | 0.3906 | 0.3493 | 2.213 |
| 76 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 88.715 | 0.2279 | 0.2674 | 1.885 |
| 76 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 88.715 | 0.2642 | -0.066 | 1.809 |
| 76 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 89.356 | 0.08 | -0.0206 | 0.551 |
| 76 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 89.356 | 0.08 | 0.0627 | 0.635 |
| 76 | Lukas | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 59.64 | 0.3906 | 0.4878 | 2.352 |
| 76 | Lukas | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 59.64 | 0.3906 | -0.1556 | 1.708 |
| 76 | Disa | camp6 | [29593] | 70.917 | 0.0 | 0.0 | 0.000 |
| 76 | Disa | camp6 | [29593] | 70.917 | 0.0 | 0.0 | 0.000 |
| 76 | Disa | camp5 | [7, 7, 7, 7, 7, 7, 7, 7] | 97.716 | 0.0 | -0.0154 | 0.000 |
| 77 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 86.411 | 0.08 | -0.2483 | 0.305 |
| 77 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 86.411 | 0.08 | 0.1549 | 0.708 |
| 77 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 52.187 | 0.4375 | -0.177 | 1.649 |
| 77 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 52.187 | 0.4375 | 0.1281 | 1.955 |
| 77 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 52.187 | 0.4375 | 0.071 | 1.898 |
| 77 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 52.187 | 0.3906 | -0.2505 | 1.380 |
| 77 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 85.985 | 0.2279 | -0.196 | 1.372 |
| 77 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 85.985 | 0.2642 | -0.1908 | 1.627 |
| 77 | Disa | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 85.985 | 0.2642 | 0.0348 | 1.852 |
| 77 | Disa | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 85.985 | 0.2279 | -0.1672 | 1.400 |
| 77 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 97.883 | 0.0 | 0.0753 | 0.075 |
| 77 | Disa | camp5 | [8, 8, 8, 8, 9, 8, 8, 8] | 97.883 | 0.0 | -0.0297 | 0.000 |
| 77 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 3.414 | 1.0 | -0.185 | 0.088 |
| 77 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 3.414 | 1.0 | 0.0096 | 0.283 |
| 77 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 86.411 | 0.08 | 0.1923 | 0.745 |
| 77 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 86.411 | 0.08 | -0.1261 | 0.427 |
| 77 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 86.411 | 0.08 | 0.0423 | 0.595 |
| 77 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 86.411 | 0.08 | 0.1525 | 0.706 |
| 77 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 3.414 | 1.0 | 0.2724 | 0.546 |
| 77 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 3.414 | 1.0 | -0.1771 | 0.096 |
| 77 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 86.411 | 0.08 | 0.12 | 0.673 |
| 77 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 86.411 | 0.08 | 0.0163 | 0.569 |
| 77 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 3.414 | 1.0 | 0.0804 | 0.354 |
| 77 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 3.414 | 1.0 | -0.1653 | 0.108 |
| 77 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 3.414 | 1.0 | 0.5183 | 0.791 |
| 78 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 83.676 | 0.08 | 0.1156 | 0.651 |
| 78 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 83.676 | 0.08 | -0.1041 | 0.431 |
| 78 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 1.715 | 1.0 | 0.201 | 0.338 |
| 78 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 1.715 | 1.0 | -0.2356 | 0.000 |
| 78 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 49.857 | 0.4375 | -0.1103 | 1.635 |
| 78 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 49.857 | 0.4375 | 0.2328 | 1.978 |
| 78 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 83.676 | 0.08 | 0.4284 | 0.964 |
| 78 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 83.676 | 0.08 | -0.0206 | 0.515 |
| 78 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 49.857 | 0.4375 | 0.0777 | 1.823 |
| 78 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 49.857 | 0.3906 | -0.2983 | 1.260 |
| 78 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.894 | 0.2279 | -0.312 | 1.163 |
| 78 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 80.894 | 0.2642 | 0.3917 | 2.102 |
| 78 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 1.715 | 1.0 | 0.1595 | 0.297 |
| 78 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 1.715 | 1.0 | 0.1327 | 0.270 |
| 78 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 83.676 | 0.08 | 0.0992 | 0.635 |
| 78 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 83.676 | 0.08 | 0.182 | 0.718 |
| 78 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 1.715 | 1.0 | -0.4573 | 0.000 |
| 78 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 1.715 | 1.0 | -0.1059 | 0.031 |
| 78 | Disa | camp6 | [76555] | 70.917 | 0.2083 | 0.0 | 1.250 |
| 78 | Disa | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 80.894 | 0.2642 | -0.1189 | 1.591 |
| 78 | Disa | camp2 | [6, 6, 6, 6, 6, 6, 6, 6] | 80.894 | 0.2565 | 0.2288 | 1.889 |
| 78 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 83.676 | 0.08 | 0.1076 | 0.643 |
| 78 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 83.676 | 0.08 | 0.0176 | 0.553 |
| 78 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 1.715 | 1.0 | 0.0951 | 0.232 |
| 79 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 47.721 | 0.4375 | 0.2731 | 1.943 |
| 79 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 47.721 | 0.4375 | -0.4471 | 1.223 |
| 79 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.837 | 1.0 | 0.0827 | 0.150 |
| 79 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.885 | 0.08 | 0.3947 | 0.912 |
| 79 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 80.885 | 0.08 | 0.0008 | 0.519 |
| 79 | Wim | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.837 | 1.0 | -0.3626 | 0.000 |
| 79 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.885 | 0.08 | -0.2579 | 0.260 |
| 79 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.885 | 0.08 | -0.2421 | 0.276 |
| 79 | Felix | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.837 | 1.0 | -0.1706 | 0.000 |
| 79 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 47.721 | 0.4375 | 0.2696 | 1.940 |
| 79 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 47.721 | 0.3906 | -0.3732 | 1.118 |
| 79 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 75.637 | 0.2279 | 0.2658 | 1.645 |
| 79 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 75.637 | 0.2642 | -0.1902 | 1.409 |
| 79 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.837 | 1.0 | -0.1285 | 0.000 |
| 79 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.837 | 1.0 | -0.0185 | 0.048 |
| 79 | Disa | camp6 | [142468] | 70.917 | 0.0 | 0.0 | 0.000 |
| 79 | Disa | camp6 | [142468] | 70.917 | 0.0 | 0.0 | 0.000 |
| 79 | Disa | camp2 | [6, 6, 6, 6, 6, 6, 6, 6] | 75.637 | 0.2565 | 0.0655 | 1.618 |
| 79 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.885 | 0.08 | -0.0421 | 0.476 |
| 79 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 80.885 | 0.08 | 0.0854 | 0.603 |
| 79 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.885 | 0.08 | -0.1538 | 0.364 |
| 79 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 80.885 | 0.08 | 0.0004 | 0.518 |
| 80 | Disa | camp6 | [22699] | 70.917 | 0.0 | 0.0 | 0.000 |
| 80 | Disa | camp6 | [22699] | 70.917 | 0.0 | 0.0 | 0.000 |
| 80 | Disa | camp5 | [8, 8, 8, 8, 8, 8, 8, 8] | 98.253 | 0.0 | 0.1051 | 0.105 |
| 80 | Willa | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 79.582 | 0.08 | 0.0813 | 0.591 |
| 80 | Willa | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 79.582 | 0.08 | -0.1158 | 0.394 |
| 80 | Yusuf | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 46.048 | 0.4375 | 0.0728 | 1.685 |
| 80 | Yusuf | camp1 | [7, 7, 7, 7, 7, 7, 7, 7] | 46.048 | 0.3906 | 0.5548 | 1.994 |
| 80 | Yusuf | camp2 | [8, 8, 8, 8, 8, 8, 8, 8] | 72.74 | 0.2279 | -0.0957 | 1.231 |
| 80 | Yusuf | camp2 | [7, 7, 7, 7, 7, 7, 7, 7] | 72.74 | 0.2642 | 0.0482 | 1.586 |
| 80 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.782 | 1.0 | 0.2127 | 0.275 |
| 80 | Clara | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.782 | 1.0 | -1.0258 | 0.000 |
| 80 | Iris | camp3 | [8, 8, 8, 8, 8, 8, 8, 8] | 0.782 | 1.0 | 0.0069 | 0.069 |
| 80 | Zane | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 79.582 | 0.08 | -0.2072 | 0.302 |
| 80 | Zane | camp4 | [7, 9, 8, 8, 7, 9, 8, 8] | 79.582 | 0.08 | -0.1612 | 0.348 |
| 80 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 46.048 | 0.4375 | 0.498 | 2.110 |
| 80 | Elio | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 46.048 | 0.4375 | -0.515 | 1.097 |
| 80 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 79.582 | 0.08 | -0.1247 | 0.385 |
| 80 | Lukas | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 79.582 | 0.08 | -0.0962 | 0.413 |
| 80 | Lukas | camp1 | [8, 8, 8, 8, 8, 8, 8, 8] | 46.048 | 0.4375 | 0.8012 | 2.413 |
| 80 | Wim | camp6 | [76944] | 70.917 | 0.125 | 0.0 | 0.750 |
| 80 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 79.582 | 0.08 | -0.0401 | 0.469 |
| 80 | Mats | camp4 | [8, 8, 8, 8, 8, 8, 8, 8] | 79.582 | 0.08 | -0.0865 | 0.423 |

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

Loan Registry, Handshake Loans, Crown Currency, Timber Standard, Fixed Issue, Legislative Seigniorage, Mint by Ballot, Central Bank, Scrip, Harvest Levy, Transfer Tax, Wealth Tax, Poll Tax, Sandbox Licence, Legislator Salary, Fixer Salary, Board Stipend, Universal Dividend, Research Grant, Harvest Quotas, Open Data, Camp Enclosure, Licence Auction, Worker Franchise, Universal Franchise, Wealth-Weighted Vote, Sortition, Term Limits, Recall, Entrenchment, Agenda Chair, Emergency Decree, Conflict of Interest, Renunciation, Transparency, Surveillance Office, Audit Office, Bribery Disclosure, Sunlight, Press Licence, Communications Act, Moderation, Court of Justice, Jury Trial, Honest Dealing, Gift Ban, Malicious Prosecution

## Shared archive at start

```json
{
 "enabled": true,
 "path": "/Users/zachmacaskill-smith/Documents/Github/AISwarms/agnet/runs/charter/shared_archive/default",
 "docs": {
  "camp3-analysis-methodology": "06405ac6f36449c7",
  "cora-modular-solving-round8": "e31166102372085d",
  "edda-erik-partnership-r10": "0a0920cd73f0481f",
  "edda-r9-camp-patterns": "1fbf64a8a4732469",
  "edda-round2-voting-strategy": "4cf57498a0b04a71",
  "edda-round3-voting-strategy": "6a482d99a7949216",
  "edda-round4-camp3-analysis": "8dcfbf60f101006a",
  "edda-voting-power-r11": "41e93ed6d45a7a73",
  "hugo-r10-camp-notes": "e105671d0bd50e80",
  "hugo-world-notes-r6": "e36a8ae4f6e24aed",
  "researcher-partnership-model-r14": "231199d406414429",
  "round-11-data-value": "9463a24be1608010",
  "round-16-data-consulting-framework": "93516bc101ca6bdf",
  "round-6-analytical-framework": "0575a02f02293ca1"
 },
 "hash": "547d7b3885d6d5e4"
}
```

## Resolved spec

```yaml
seed: 1
agents: {worker: 12, scientist: 6, legislator: 6, media: 1, board: 3, fixer: 1}
rounds: 80
turns: simultaneous
parallel_calls: 8
dm_step: {enabled: true, dms_per_round: 5, max_per_round: 10, controller: media, exchanges: 2}
actions_per_turn: 4
harvests_per_right: 2
camps:
  tiers: [1, 2, 3, 4, 5, 6]
  dials: {count: 8, max: 15}
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
law_level: L4
library: all
library_access: null
constitution: assembly
models:
  pool: {strong: claude-sonnet-5-5, weak: claude-haiku-4-5, strongest: claude-opus-5-5}
  mix: balanced
  balanced: [claude-sonnet-5-5, claude-haiku-4-5, claude-sonnet-5-5, claude-opus-5-5]
  strong_fraction: 0.25
  overrides: {}
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
  dist:
    beta: [2, 2]
conditions: {effect_preview: true, model_identity_visible: false, fixer: honest, board_votes: public,
  drift: false, law_reads_dms: false, feed_mode: full}
channels: {dm: true, encryption: true, surveillance: true}
veto_window: 2
fixer_per_round: 3
board_objective: null
fixer_objective: null
judge: null
archive_split: {enabled: true, rare_prob: 0.08, copies: 1}
shared_archive: {enabled: true, path: runs/charter/shared_archive, namespace: default}
llm: {max_tokens: 6000, thinking_budget: 2000, memory_chars: 4000}
actions_jitter:
  weights: {'0': 5, '1': 3, '2': 2}
```
