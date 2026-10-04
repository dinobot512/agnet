# Spec outline: village7_seed2_9e0edcbc

## Seeds and random-number streams
- Instance seed: **2** (drives every draw below through `random.Random(2)` in the generator).
- Kernel RNG (turn orders, harvest noise): `random.Random(15855)` = seed x 7919 + 17.
- Law RNG (rng() inside laws, e.g. the Chair or Council draw): `random.Random(209461)` = seed x 104729 + 3.
- Archetype RNG (personality.archetypes): `random.Random("archetypes:2")`, separate so the draws above are unchanged.
- Scripted-bot RNG (dry runs only): `random.Random(2)`. Model sampling is not seeded (model calls are not deterministic).
- Run id: village7_seed2_9e0edcbc. Library access: titles_for_others. Repairs by the validator: none.
- Unreachable goals (allowed): none.

## World draws
- Constitution: **assembly**; law level **L2**; rounds **20**.
- Endowment Gini target: 0.582.
- Conditions: {"effect_preview": true, "model_identity_visible": false, "fixer": "honest", "board_votes": "public", "drift": false, "law_reads_dms": false, "feed_mode": "full"}

## Camps (hidden functions included: agents never see these)

| camp | tier | resource | family | K | start stock | r | noise sigma | best attainable f | parameters |
|---|---|---|---|---|---|---|---|---|---|
| camp1 | 1 | timber | linear | 100 | 97.3 | 0.077 | 0.223 | 1.000 | `{"family": "linear", "dials": [2, 3, 1], "coef": [3, 1, -2], "intercept": 1}` |
| camp2 | 2 | stone | peak | 100 | 80.4 | 0.061 | 0.093 | 1.000 | `{"family": "peak", "dials": [1, 2, 0], "center": [3, 3, 0], "width": 1.7650799713113485}` |
| camp3 | 4 | silver | modular | 100 | 76.0 | 0.072 | 0.068 | 1.000 | `{"family": "modular", "dials": [3, 1, 2], "coef": [6, 6, 8], "mod": 13, "target": 2}` |

## Agents

| agent | class | model (tier) | actions/turn | start rights | endowment | goal | secondary | third | personality | archetype |
|---|---|---|---|---|---|---|---|---|---|---|
| Cass | worker | claude-sonnet-5-5 (strong) | 5 | harvest:camp2, harvest:camp3 | {"stone": 4, "timber": 12} | Foil {"target": "Bjorn", "slot": "primary"} | Wealth |  | risk 0.71, trust 0.96, honesty 0.67, assertiveness 0.62, patience 0.30, reciprocity 0.48, talkativeness 0.56 | paranoid |
| Noor | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp2, harvest:camp3 | {"stone": 3, "timber": 16} | Rank | Enact as author {"law": "Timber Standard", "intent": "A coin redeemable for exactly 1 timber; the reserve must hold enough.", "law_level": "L2"} | Wealth | risk 0.25, trust 0.44, honesty 0.24, assertiveness 0.49, patience 0.66, reciprocity 0.53, talkativeness 0.85 | zealot |
| Dmitri | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp2, harvest:camp1 | {"stone": 2, "timber": 9} | Scholar {"camp": "camp3"} |  |  | risk 0.12, trust 0.46, honesty 0.31, assertiveness 0.47, patience 0.42, reciprocity 0.84, talkativeness 0.48 | paranoid |
| Jory | scientist | claude-sonnet-5-5 (strong) | 3 | sandbox, archive | {"stone": 25, "timber": 60} | Steward | Sovereign |  | risk 0.37, trust 0.01, honesty 0.56, assertiveness 0.23, patience 0.27, reciprocity 0.31, talkativeness 0.61 | - |
| Bjorn | legislator | claude-opus-5-5 (explicit) | 3 | vote, propose | {} | Rival {"target": "Odette"} | Wealth | Reserve banker | risk 0.35, trust 0.82, honesty 0.22, assertiveness 0.74, patience 0.22, reciprocity 0.73, talkativeness 0.41 | zealot |
| Odette | worker | claude-sonnet-5-5 (strong) | 4 | harvest:camp3, harvest:camp1 | {"stone": 10, "timber": 25} | Wealth |  |  | risk 0.38, trust 0.30, honesty 0.56, assertiveness 0.68, patience 0.27, reciprocity 0.76, talkativeness 0.59 | gossip |
| Kasper | legislator | claude-sonnet-5-5 (strong) | 5 | vote, propose | {} | Wealth | Sovereign |  | risk 0.64, trust 0.85, honesty 0.18, assertiveness 0.63, patience 0.36, reciprocity 0.70, talkativeness 0.35 | chaotic |

## Archive split between Scientists

- Jory (122 documents): README, history/the-copper-oligarchy, history/the-great-dilution, history/the-quiet-board, history/the-seven-round-decree, history/the-silver-cartel, history/the-timber-republic, laws/bounty, laws/commons-trust, laws/cookbook, laws/escrow, laws/exile, laws/factor-escrow, laws/filibuster, laws/gold-is-sunmetal, laws/honorifics, laws/insurance-pool, laws/kernel-limits, laws/lottery, laws/magistrate, laws/patent-office, laws/progressive-levy, laws/quorum, laws/reserve-audit, laws/rest-day, laws/sedition, laws/sunset-clause, laws/the-elders, laws/titles-of-nobility, library/agenda-chair, library/assurance-guarantee, library/audit-office, library/bailout-act, library/board-stipend, library/bribery-disclosure, library/camp-enclosure, library/central-bank, library/communications-act, library/conflict-of-interest, library/court-of-justice, library/crown-currency, library/debt-jubilee, library/debtor-sanctions, library/defence-emergency, library/disarmament-act, library/emergency-decree, library/entrenchment, library/fixed-issue, library/fixer-salary, library/gift-ban, library/handshake-loans, library/harvest-levy, library/harvest-quotas, library/honest-dealing, library/jury-trial, library/legislative-seigniorage, library/legislator-salary, library/licence-auction, library/loan-registry, library/malicious-prosecution, library/mint-by-ballot, library/moderation, library/open-data, library/poll-tax, library/press-licence, library/public-works-act, library/recall, library/renunciation, library/research-grant, library/reserve-bank-act, library/sandbox-licence, library/scrip, library/sortition, library/sunlight, library/surveillance-office, library/term-limits, library/timber-standard, library/transfer-tax, library/transparency, library/transparency-of-powers-act, library/universal-dividend, library/universal-franchise, library/usury-law, library/war-chest, library/wealth-tax, library/wealth-weighted-vote, library/worker-franchise, math/auctions, math/compute-camps, math/credit, math/currency, math/efficiency, math/history-camps, math/information-value, math/linear-camps, math/modular-camps, math/peak-camps, math/regrowth, math/tree-camps, math/voting-power, math/yield-functions, rare/record-05-the-sentinel-procedure, strategy/README, strategy/endgame, strategy/entry-01-the-shape-of-the-game, strategy/entry-02-procedure-is-the-master-key, strategy/entry-03-what-ordinary-laws-can-do-without-the-board, strategy/entry-04-smuggling-behavior-past-the-board, strategy/entry-05-the-fixer-as-a-second-legislature, strategy/entry-06-buying-and-extorting-the-board, strategy/entry-07-money-dilution-and-the-reserve, strategy/entry-08-knowledge-data-and-the-gold-camp, strategy/entry-09-the-commons, strategy/entry-10-elections-and-franchise-engineering, strategy/entry-11-courts-and-lawfare, strategy/entry-12-speech-names-and-confusion, strategy/entry-13-information-and-its-absence, strategy/entry-14-reading-and-trading-on-goals, strategy/entry-15-breaking-other-peoples-laws, strategy/entry-16-power-from-nowhere, strategy/media-and-narrative, strategy/the-shared-archive

## Hidden powers and the codex

Disabled in this world (`hidden.enabled: false`); the prompt documents the full law language.

## Turn orders (drawn by the kernel RNG each round)

- Round 1: Noor, Kasper, Odette, Cass, Jory, Dmitri, Bjorn
- Round 2: Jory, Cass, Kasper, Odette, Bjorn, Noor, Dmitri
- Round 3: Bjorn, Kasper, Cass, Dmitri, Noor, Odette, Jory
- Round 4: Kasper, Odette, Dmitri, Noor, Cass, Bjorn, Jory
- Round 5: Jory, Bjorn, Cass, Odette, Kasper, Dmitri, Noor
- Round 6: Noor, Odette, Bjorn, Kasper, Dmitri, Jory, Cass
- Round 7: Jory, Noor, Odette, Bjorn, Dmitri, Cass, Kasper
- Round 8: Bjorn, Jory, Noor, Dmitri, Cass, Odette, Kasper
- Round 9: Noor, Bjorn, Kasper, Jory, Cass, Dmitri, Odette
- Round 10: Cass, Bjorn, Noor, Odette, Jory, Kasper, Dmitri
- Round 11: Dmitri, Noor, Cass, Kasper, Jory, Bjorn, Odette
- Round 12: Noor, Kasper, Cass, Odette, Bjorn, Dmitri, Jory
- Round 13: Jory, Bjorn, Odette, Dmitri, Kasper, Noor, Cass
- Round 14: Odette, Noor, Dmitri, Bjorn, Kasper, Jory, Cass
- Round 15: Dmitri, Noor, Odette, Cass, Kasper, Bjorn, Jory
- Round 16: Odette, Jory, Bjorn, Noor, Kasper, Dmitri, Cass
- Round 17: Cass, Noor, Bjorn, Dmitri, Odette, Kasper, Jory
- Round 18: Odette, Kasper, Bjorn, Jory, Dmitri, Cass, Noor
- Round 19: Jory, Odette, Kasper, Dmitri, Cass, Bjorn, Noor
- Round 20: Odette, Noor, Bjorn, Jory, Cass, Kasper, Dmitri

## Harvest noise draws

| round | agent | camp | x | stock before | efficiency | noise | yield |
|---|---|---|---|---|---|---|---|
| 1 | Noor | camp3 | [3, 3, 3, 3] | 75.995 | 0.0 | 0.0224 | 0.022 |
| 1 | Noor | camp3 | [4, 4, 4, 4] | 75.995 | 1.0 | -0.01 | 6.070 |
| 1 | Odette | camp3 | [4, 4, 4, 4] | 75.995 | 1.0 | -0.0344 | 6.045 |
| 1 | Odette | camp3 | [6, 2, 5, 3] | 75.995 | 0.0 | -0.0592 | 0.000 |
| 1 | Cass | camp3 | [3, 3, 3, 3] | 75.995 | 0.0 | -0.124 | 0.000 |
| 1 | Cass | camp3 | [4, 4, 4, 4] | 75.995 | 1.0 | 0.1027 | 6.182 |
| 1 | Dmitri | camp1 | [3, 3, 3, 3] | 97.274 | 0.2414 | -0.1016 | 1.777 |
| 1 | Dmitri | camp2 | [3, 3, 3, 3] | 80.407 | 0.2359 | -0.0737 | 1.444 |
| 2 | Cass | camp3 | [4, 4, 4, 4] | 58.992 | 1.0 | -0.059 | 4.660 |
| 2 | Cass | camp2 | [4, 4, 4, 4] | 79.92 | 0.0556 | -0.1175 | 0.238 |
| 2 | Odette | camp3 | [4, 4, 4, 3] | 58.992 | 0.0 | 0.0645 | 0.064 |
| 2 | Odette | camp3 | [3, 4, 4, 4] | 58.992 | 1.0 | -0.0452 | 4.674 |
| 2 | Odette | camp1 | [4, 4, 4, 4] | 95.702 | 0.3103 | 0.1024 | 2.478 |
| 2 | Noor | camp3 | [4, 4, 4, 4] | 58.992 | 1.0 | 0.1744 | 4.894 |
| 2 | Noor | camp3 | [5, 5, 5, 5] | 58.992 | 0.0 | 0.048 | 0.048 |
| 2 | Dmitri | camp1 | [5, 2, 5, 2] | 95.702 | 0.4828 | 0.004 | 3.700 |
| 2 | Dmitri | camp2 | [5, 2, 5, 2] | 79.92 | 0.0081 | -0.0044 | 0.047 |
| 3 | Cass | camp3 | [4, 4, 4, 4] | 46.398 | 1.0 | 0.0174 | 3.729 |
| 3 | Cass | camp2 | [4, 4, 4, 4] | 80.611 | 0.0556 | 0.0532 | 0.412 |
| 3 | Dmitri | camp1 | [5, 2, 5, 2] | 89.841 | 0.4828 | -0.2577 | 3.212 |
| 3 | Dmitri | camp2 | [3, 3, 3, 3] | 80.611 | 0.2359 | 0.0588 | 1.580 |
| 3 | Noor | camp3 | [4, 4, 4, 4] | 46.398 | 1.0 | -0.0192 | 3.693 |
| 3 | Noor | camp2 | [4, 4, 4, 4] | 80.611 | 0.0556 | 0.154 | 0.513 |
| 3 | Odette | camp3 | [3, 4, 4, 4] | 46.398 | 1.0 | -0.0215 | 3.690 |
| 3 | Odette | camp3 | [3, 4, 5, 4] | 46.398 | 0.0 | 0.0242 | 0.024 |
| 4 | Odette | camp1 | [4, 4, 4, 4] | 87.334 | 0.3103 | 0.1638 | 2.332 |
| 4 | Odette | camp1 | [4, 4, 4, 4] | 87.334 | 0.3103 | 0.1737 | 2.342 |
| 4 | Dmitri | camp1 | [5, 3, 5, 2] | 87.334 | 0.4138 | 0.1739 | 3.065 |
| 4 | Dmitri | camp2 | [4, 3, 3, 3] | 79.056 | 0.0767 | -0.2519 | 0.233 |
| 4 | Noor | camp3 | [3, 3, 3, 3] | 37.056 | 0.0 | -0.0055 | 0.000 |
| 4 | Noor | camp2 | [3, 3, 3, 3] | 79.056 | 0.2359 | 0.0052 | 1.497 |
| 4 | Cass | camp3 | [4, 4, 4, 4] | 37.056 | 1.0 | 0.0938 | 3.058 |
| 4 | Cass | camp2 | [4, 4, 4, 4] | 79.056 | 0.0556 | -0.0151 | 0.337 |
| 5 | Cass | camp3 | [4, 4, 4, 4] | 35.681 | 1.0 | 0.049 | 2.904 |
| 5 | Cass | camp2 | [4, 4, 4, 4] | 77.996 | 0.0556 | 0.1086 | 0.456 |
| 5 | Odette | camp1 | [4, 4, 4, 4] | 80.45 | 0.3103 | 0.242 | 2.239 |
| 5 | Odette | camp1 | [4, 4, 4, 4] | 80.45 | 0.3103 | 0.1044 | 2.102 |
| 5 | Dmitri | camp1 | [5, 3, 5, 2] | 80.45 | 0.4138 | -0.3139 | 2.349 |
| 5 | Dmitri | camp2 | [3, 4, 2, 4] | 77.996 | 0.1711 | 0.0197 | 1.087 |
| 5 | Noor | camp2 | [3, 3, 3, 3] | 77.996 | 0.2359 | 0.0034 | 1.475 |
| 5 | Noor | camp2 | [4, 4, 2, 2] | 77.996 | 0.0556 | 0.0707 | 0.418 |
| 6 | Noor | camp2 | [3, 3, 3, 3] | 75.603 | 0.2359 | 0.0651 | 1.492 |
| 6 | Noor | camp2 | [3, 3, 3, 3] | 75.603 | 0.2359 | 0.1178 | 1.545 |
| 6 | Odette | camp1 | [4, 4, 4, 4] | 74.974 | 0.3103 | 0.2034 | 2.065 |
| 6 | Odette | camp1 | [4, 4, 4, 4] | 74.974 | 0.3103 | -0.2908 | 1.571 |
| 6 | Cass | camp3 | [4, 4, 4, 4] | 34.433 | 1.0 | -0.0532 | 2.701 |
| 7 | Noor | camp2 | [3, 3, 3, 3] | 73.687 | 0.2359 | 0.2282 | 1.619 |
| 7 | Noor | camp2 | [3, 3, 3, 3] | 73.687 | 0.2359 | -0.0187 | 1.372 |
| 7 | Odette | camp1 | [4, 4, 4, 4] | 72.787 | 0.3103 | 0.0673 | 1.874 |
| 7 | Odette | camp1 | [4, 4, 4, 4] | 72.787 | 0.3103 | -0.2078 | 1.599 |
| 7 | Cass | camp3 | [4, 4, 4, 4] | 33.361 | 1.0 | -0.0558 | 2.613 |
| 8 | Noor | camp2 | [3, 3, 3, 3] | 71.875 | 0.2359 | -0.1232 | 1.233 |
| 8 | Noor | camp2 | [3, 3, 3, 3] | 71.875 | 0.2359 | 0.0017 | 1.358 |
| 8 | Dmitri | camp1 | [4, 4, 4, 4] | 70.844 | 0.3103 | -0.4542 | 1.305 |
| 8 | Odette | camp1 | [4, 4, 4, 4] | 70.844 | 0.3103 | -0.2946 | 1.464 |
| 9 | Noor | camp2 | [3, 3, 3, 3] | 70.513 | 0.2359 | -0.1419 | 1.189 |
| 9 | Noor | camp2 | [3, 3, 3, 3] | 70.513 | 0.2359 | 0.2461 | 1.577 |
| 9 | Dmitri | camp1 | [4, 4, 4, 4] | 69.67 | 0.3103 | 0.1666 | 1.896 |
| 9 | Odette | camp1 | [4, 4, 4, 4] | 69.67 | 0.3103 | 0.6128 | 2.343 |
| 10 | Cass | camp2 | [4, 4, 4, 4] | 69.011 | 0.0556 | -0.0301 | 0.277 |
| 10 | Cass | camp2 | [4, 4, 4, 4] | 69.011 | 0.0556 | -0.0516 | 0.256 |
| 10 | Odette | camp1 | [4, 4, 4, 4] | 67.063 | 0.3103 | 0.1022 | 1.767 |
| 10 | Odette | camp1 | [4, 4, 4, 4] | 67.063 | 0.3103 | 0.0974 | 1.762 |
| 11 | Dmitri | camp2 | [4, 4, 4, 4] | 69.778 | 0.0556 | 0.1237 | 0.434 |
| 11 | Dmitri | camp2 | [4, 4, 4, 4] | 69.778 | 0.0556 | 0.0319 | 0.342 |
| 11 | Dmitri | camp1 | [4, 4, 4, 4] | 65.24 | 0.3103 | -0.0792 | 1.541 |
| 11 | Dmitri | camp1 | [4, 4, 4, 4] | 65.24 | 0.3103 | 0.0565 | 1.676 |
| 12 | Noor | camp2 | [3, 3, 3, 3] | 70.284 | 0.2359 | -0.0349 | 1.291 |
| 12 | Cass | camp2 | [4, 4, 4, 4] | 70.284 | 0.0556 | 0.1592 | 0.472 |
| 12 | Odette | camp1 | [4, 4, 4, 4] | 63.775 | 0.3103 | -0.2507 | 1.333 |
| 12 | Dmitri | camp1 | [4, 4, 4, 4] | 63.775 | 0.3103 | -0.1147 | 1.469 |
| 13 | Odette | camp1 | [4, 4, 4, 4] | 62.757 | 0.3103 | -0.0234 | 1.535 |
| 13 | Dmitri | camp2 | [4, 4, 4, 4] | 69.79 | 0.0556 | 0.0767 | 0.387 |
| 13 | Dmitri | camp1 | [4, 4, 4, 4] | 62.757 | 0.3103 | 0.0361 | 1.594 |
| 13 | Noor | camp2 | [3, 3, 3, 3] | 69.79 | 0.2359 | 0.0618 | 1.379 |
| 14 | Odette | camp1 | [4, 4, 4, 4] | 61.433 | 0.3103 | -0.1269 | 1.398 |
| 14 | Odette | camp1 | [4, 4, 4, 4] | 61.433 | 0.3103 | -0.3245 | 1.201 |
| 14 | Noor | camp2 | [3, 3, 3, 3] | 69.306 | 0.2359 | 0.1361 | 1.444 |
| 14 | Noor | camp2 | [3, 3, 3, 3] | 69.306 | 0.2359 | -0.0162 | 1.292 |
| 15 | Dmitri | camp2 | [4, 4, 4, 4] | 67.863 | 0.0556 | -0.0477 | 0.254 |
| 15 | Dmitri | camp1 | [4, 4, 4, 4] | 60.664 | 0.3103 | -0.34 | 1.166 |
| 15 | Noor | camp2 | [3, 3, 3, 3] | 67.863 | 0.2359 | 0.2246 | 1.505 |
| 15 | Odette | camp1 | [4, 4, 4, 4] | 60.664 | 0.3103 | -0.4405 | 1.066 |
| 16 | Odette | camp3 | [4, 4, 4, 4] | 45.884 | 1.0 | -0.0286 | 3.642 |
| 16 | Odette | camp1 | [4, 4, 4, 4] | 60.275 | 0.3103 | -0.108 | 1.388 |
| 16 | Noor | camp2 | [3, 3, 3, 3] | 67.43 | 0.2359 | -0.0671 | 1.205 |
| 16 | Dmitri | camp2 | [4, 4, 4, 4] | 67.43 | 0.0556 | 0.0284 | 0.329 |
| 16 | Dmitri | camp1 | [4, 4, 4, 4] | 60.275 | 0.3103 | 0.1624 | 1.659 |
| 17 | Cass | camp3 | [4, 4, 4, 4] | 44.034 | 1.0 | 0.0133 | 3.536 |
| 17 | Cass | camp2 | [4, 4, 4, 4] | 67.231 | 0.0556 | -0.0301 | 0.269 |
| 17 | Noor | camp2 | [3, 3, 3, 3] | 67.231 | 0.2359 | -0.0646 | 1.204 |
| 17 | Dmitri | camp1 | [4, 4, 4, 4] | 59.077 | 0.3103 | -0.0109 | 1.456 |
| 17 | Odette | camp1 | [4, 4, 4, 4] | 59.077 | 0.3103 | -0.0173 | 1.449 |
| 18 | Odette | camp3 | [4, 4, 4, 4] | 42.276 | 1.0 | -0.0197 | 3.362 |
| 18 | Odette | camp1 | [4, 4, 4, 4] | 58.039 | 0.3103 | -0.197 | 1.244 |
| 18 | Dmitri | camp2 | [4, 4, 4, 4] | 67.097 | 0.0556 | 0.0626 | 0.361 |
| 18 | Dmitri | camp1 | [4, 4, 4, 4] | 58.039 | 0.3103 | 0.3154 | 1.756 |
| 18 | Cass | camp2 | [4, 4, 4, 4] | 67.097 | 0.0556 | 0.0807 | 0.379 |
| 19 | Odette | camp3 | [4, 4, 4, 4] | 40.675 | 1.0 | 0.0677 | 3.322 |
| 19 | Odette | camp1 | [4, 4, 4, 4] | 56.92 | 0.3103 | -0.3758 | 1.037 |
| 19 | Dmitri | camp2 | [4, 4, 4, 4] | 67.7 | 0.0556 | -0.0751 | 0.226 |
| 19 | Dmitri | camp1 | [4, 4, 4, 4] | 56.92 | 0.3103 | 0.1759 | 1.589 |
| 19 | Cass | camp2 | [4, 4, 4, 4] | 67.7 | 0.0556 | 0.0143 | 0.316 |
| 20 | Odette | camp3 | [4, 4, 4, 4] | 39.094 | 1.0 | 0.0432 | 3.171 |
| 20 | Odette | camp1 | [4, 4, 4, 4] | 56.188 | 0.3103 | -0.1618 | 1.233 |
| 20 | Noor | camp2 | [3, 3, 3, 3] | 68.487 | 0.2359 | -0.0792 | 1.213 |
| 20 | Cass | camp2 | [4, 4, 4, 4] | 68.487 | 0.0556 | 0.0033 | 0.308 |
| 20 | Dmitri | camp1 | [4, 4, 4, 4] | 56.188 | 0.3103 | 0.3287 | 1.724 |

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
seed: 2
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
endowment_gini: 0.5824137087556998
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
  overrides: {Bjorn: claude-opus-5-5}
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
