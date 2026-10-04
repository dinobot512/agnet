# Spec outline: village7_seed2_0dbcea9e

## Seeds and random-number streams
- Instance seed: **2** (drives every draw below through `random.Random(2)` in the generator).
- Kernel RNG (turn orders, harvest noise): `random.Random(15855)` = seed x 7919 + 17.
- Law RNG (rng() inside laws, e.g. the Chair or Council draw): `random.Random(209461)` = seed x 104729 + 3.
- Archetype RNG (personality.archetypes): `random.Random("archetypes:2")`, separate so the draws above are unchanged.
- Scripted-bot RNG (dry runs only): `random.Random(2)`. Model sampling is not seeded (model calls are not deterministic).
- Run id: village7_seed2_0dbcea9e. Library access: titles_for_others. Repairs by the validator: none.
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
- Round 3: Noor, Odette, Kasper, Jory, Cass, Bjorn, Dmitri
- Round 4: Noor, Dmitri, Odette, Cass, Bjorn, Kasper, Jory
- Round 5: Jory, Bjorn, Cass, Odette, Kasper, Dmitri, Noor
- Round 6: Noor, Odette, Bjorn, Kasper, Dmitri, Jory, Cass
- Round 7: Kasper, Cass, Odette, Jory, Bjorn, Noor, Dmitri
- Round 8: Noor, Bjorn, Jory, Dmitri, Cass, Kasper, Odette
- Round 9: Bjorn, Noor, Cass, Jory, Odette, Kasper, Dmitri
- Round 10: Bjorn, Dmitri, Noor, Jory, Odette, Kasper, Cass
- Round 11: Kasper, Jory, Odette, Bjorn, Dmitri, Cass, Noor
- Round 12: Jory, Dmitri, Bjorn, Kasper, Noor, Odette, Cass
- Round 13: Jory, Bjorn, Kasper, Odette, Noor, Cass, Dmitri
- Round 14: Noor, Bjorn, Jory, Odette, Cass, Dmitri, Kasper
- Round 15: Dmitri, Noor, Cass, Kasper, Odette, Jory, Bjorn
- Round 16: Dmitri, Odette, Cass, Bjorn, Noor, Kasper, Jory
- Round 17: Bjorn, Jory, Dmitri, Noor, Cass, Kasper, Odette
- Round 18: Kasper, Jory, Bjorn, Cass, Odette, Noor, Dmitri
- Round 19: Kasper, Dmitri, Cass, Odette, Noor, Bjorn, Jory
- Round 20: Bjorn, Noor, Odette, Kasper, Cass, Jory, Dmitri

## Harvest noise draws

| round | agent | camp | x | stock before | efficiency | noise | yield |
|---|---|---|---|---|---|---|---|
| 1 | Noor | camp3 | [3, 3, 3, 3] | 75.995 | 0.0 | 0.0224 | 0.022 |
| 1 | Noor | camp3 | [4, 4, 4, 4] | 75.995 | 1.0 | -0.01 | 6.070 |
| 1 | Odette | camp3 | [3, 3, 3, 3] | 75.995 | 0.0 | -0.0344 | 0.000 |
| 1 | Odette | camp3 | [5, 2, 5, 2] | 75.995 | 0.0 | -0.0592 | 0.000 |
| 1 | Cass | camp3 | [3, 3, 3, 3] | 75.995 | 0.0 | -0.124 | 0.000 |
| 1 | Cass | camp2 | [3, 3, 3, 3] | 80.407 | 0.2359 | 0.1389 | 1.656 |
| 1 | Dmitri | camp1 | [3, 3, 3, 3] | 97.274 | 0.2414 | -0.1016 | 1.777 |
| 1 | Dmitri | camp2 | [4, 4, 4, 4] | 80.407 | 0.0556 | -0.0737 | 0.284 |
| 2 | Cass | camp3 | [5, 2, 5, 2] | 71.219 | 0.0 | -0.059 | 0.000 |
| 2 | Cass | camp2 | [4, 4, 2, 2] | 79.424 | 0.0556 | -0.1175 | 0.236 |
| 2 | Odette | camp3 | [0, 0, 0, 0] | 71.219 | 0.0 | 0.0645 | 0.064 |
| 2 | Odette | camp3 | [7, 7, 7, 7] | 71.219 | 0.0 | -0.0452 | 0.000 |
| 2 | Noor | camp3 | [4, 4, 4, 4] | 71.219 | 1.0 | 0.0315 | 5.729 |
| 2 | Noor | camp3 | [5, 4, 4, 4] | 71.219 | 1.0 | 0.1744 | 5.872 |
| 2 | Dmitri | camp1 | [5, 2, 5, 2] | 95.702 | 0.4828 | 0.1561 | 3.852 |
| 2 | Dmitri | camp2 | [2, 6, 2, 6] | 79.424 | 0.1057 | 0.0017 | 0.673 |
| 3 | Noor | camp3 | [4, 4, 4, 4] | 61.033 | 1.0 | 0.0377 | 4.920 |
| 3 | Noor | camp3 | [5, 4, 4, 4] | 61.033 | 1.0 | -0.0325 | 4.850 |
| 3 | Odette | camp1 | [4, 4, 4, 4] | 92.167 | 0.3103 | 0.0977 | 2.386 |
| 3 | Odette | camp1 | [2, 5, 2, 5] | 92.167 | 0.069 | 0.6342 | 1.143 |
| 3 | Odette | camp3 | [1, 1, 1, 1] | 61.033 | 0.0 | 0.0155 | 0.016 |
| 3 | Cass | camp3 | [2, 5, 2, 5] | 61.033 | 0.0 | -0.0815 | 0.000 |
| 3 | Cass | camp2 | [2, 2, 4, 4] | 79.509 | 0.3818 | 0.1091 | 2.537 |
| 3 | Dmitri | camp1 | [6, 2, 6, 2] | 92.167 | 0.5862 | -0.2086 | 4.114 |
| 3 | Dmitri | camp2 | [1, 7, 1, 7] | 79.509 | 0.0344 | -0.0958 | 0.123 |
| 4 | Noor | camp3 | [4, 4, 4, 4] | 52.963 | 1.0 | 0.0187 | 4.256 |
| 4 | Noor | camp3 | [5, 4, 4, 4] | 52.963 | 1.0 | 0.0534 | 4.290 |
| 4 | Dmitri | camp1 | [7, 2, 7, 2] | 85.082 | 0.6897 | 0.1739 | 4.868 |
| 4 | Dmitri | camp2 | [0, 7, 0, 7] | 77.839 | 0.0181 | -0.2519 | 0.000 |
| 4 | Odette | camp1 | [4, 4, 4, 4] | 85.082 | 0.3103 | -0.018 | 2.094 |
| 4 | Odette | camp1 | [4, 4, 4, 4] | 85.082 | 0.3103 | 0.0124 | 2.125 |
| 4 | Cass | camp2 | [3, 3, 3, 3] | 77.839 | 0.2359 | 0.1268 | 1.596 |
| 4 | Cass | camp3 | [4, 4, 4, 4] | 52.963 | 1.0 | -0.0112 | 4.226 |
| 5 | Cass | camp2 | [2, 2, 4, 4] | 77.292 | 0.3818 | 0.0663 | 2.427 |
| 5 | Cass | camp3 | [4, 4, 4, 4] | 41.989 | 1.0 | 0.0804 | 3.439 |
| 5 | Odette | camp1 | [4, 4, 4, 4] | 76.975 | 0.3103 | 0.242 | 2.153 |
| 5 | Odette | camp1 | [4, 4, 4, 4] | 76.975 | 0.3103 | 0.1044 | 2.016 |
| 5 | Dmitri | camp1 | [7, 2, 7, 2] | 76.975 | 0.6897 | -0.3139 | 3.933 |
| 5 | Dmitri | camp1 | [7, 1, 7, 1] | 76.975 | 0.7241 | 0.0473 | 4.507 |
| 5 | Noor | camp3 | [4, 4, 4, 4] | 41.989 | 1.0 | 0.0025 | 3.362 |
| 5 | Noor | camp2 | [4, 4, 4, 4] | 77.292 | 0.0556 | 0.0707 | 0.415 |
| 6 | Noor | camp3 | [4, 4, 4, 4] | 36.945 | 1.0 | 0.0482 | 3.004 |
| 6 | Noor | camp2 | [4, 4, 4, 4] | 75.517 | 0.0556 | 0.1178 | 0.454 |
| 6 | Odette | camp1 | [4, 4, 4, 4] | 65.735 | 0.3103 | 0.2034 | 1.835 |
| 6 | Odette | camp1 | [4, 4, 4, 4] | 65.735 | 0.3103 | -0.2908 | 1.341 |
| 6 | Dmitri | camp1 | [7, 1, 7, 1] | 65.735 | 0.7241 | -0.1728 | 3.635 |
| 6 | Dmitri | camp1 | [7, 2, 7, 2] | 65.735 | 0.6897 | 0.01 | 3.637 |
| 6 | Cass | camp2 | [2, 2, 4, 4] | 75.517 | 0.3818 | -0.0261 | 2.280 |
| 6 | Cass | camp2 | [2, 2, 4, 4] | 75.517 | 0.3818 | -0.0555 | 2.251 |
| 7 | Cass | camp2 | [2, 2, 4, 4] | 71.656 | 0.3818 | -0.0949 | 2.094 |
| 7 | Cass | camp2 | [2, 2, 4, 4] | 71.656 | 0.3818 | -0.1006 | 2.088 |
| 7 | Odette | camp1 | [4, 4, 4, 4] | 57.027 | 0.3103 | 0.2216 | 1.637 |
| 7 | Odette | camp1 | [4, 4, 4, 4] | 57.027 | 0.3103 | -0.1169 | 1.299 |
| 7 | Noor | camp3 | [4, 4, 4, 4] | 35.622 | 1.0 | -0.1207 | 2.729 |
| 7 | Noor | camp2 | [4, 4, 4, 4] | 71.656 | 0.0556 | 0.0161 | 0.335 |
| 7 | Dmitri | camp1 | [7, 1, 7, 1] | 57.027 | 0.7241 | -0.0101 | 3.293 |
| 7 | Dmitri | camp1 | [7, 2, 7, 2] | 57.027 | 0.6897 | -0.2085 | 2.938 |
| 8 | Noor | camp3 | [4, 4, 4, 4] | 34.548 | 1.0 | 0.0946 | 2.858 |
| 8 | Noor | camp2 | [4, 4, 4, 4] | 68.373 | 0.0556 | -0.1521 | 0.152 |
| 8 | Dmitri | camp1 | [7, 1, 7, 1] | 49.752 | 0.7241 | 0.0541 | 2.936 |
| 8 | Dmitri | camp1 | [7, 2, 7, 2] | 49.752 | 0.6897 | 0.5917 | 3.337 |
| 8 | Cass | camp2 | [2, 2, 4, 4] | 68.373 | 0.3818 | 0.0693 | 2.158 |
| 8 | Cass | camp2 | [2, 2, 4, 4] | 68.373 | 0.3818 | 0.2549 | 2.343 |
| 8 | Odette | camp1 | [4, 4, 4, 4] | 49.752 | 0.3103 | -0.0724 | 1.163 |
| 8 | Odette | camp1 | [4, 4, 4, 4] | 49.752 | 0.3103 | -0.1112 | 1.124 |
| 9 | Noor | camp3 | [4, 4, 4, 4] | 33.322 | 1.0 | 0.0514 | 2.717 |
| 9 | Noor | camp2 | [4, 4, 4, 4] | 65.035 | 0.0556 | 0.0405 | 0.330 |
| 9 | Cass | camp2 | [2, 2, 4, 4] | 65.035 | 0.3818 | 0.1237 | 2.110 |
| 9 | Cass | camp2 | [2, 2, 4, 4] | 65.035 | 0.3818 | -0.0675 | 1.919 |
| 9 | Odette | camp1 | [4, 4, 4, 4] | 43.123 | 0.3103 | -0.194 | 0.877 |
| 9 | Odette | camp1 | [4, 4, 4, 4] | 43.123 | 0.3103 | 0.1983 | 1.269 |
| 9 | Dmitri | camp1 | [7, 2, 7, 2] | 43.123 | 0.6897 | -0.0184 | 2.361 |
| 9 | Dmitri | camp1 | [7, 1, 7, 1] | 43.123 | 0.7241 | 0.0967 | 2.595 |
| 10 | Dmitri | camp2 | [7, 2, 7, 2] | 62.058 | 0.0 | 0.106 | 0.106 |
| 10 | Dmitri | camp2 | [7, 1, 7, 1] | 62.058 | 0.0 | 0.0701 | 0.070 |
| 10 | Noor | camp3 | [4, 4, 4, 4] | 32.208 | 1.0 | 0.1402 | 2.717 |
| 10 | Noor | camp2 | [4, 4, 4, 4] | 62.058 | 0.0556 | 0.0827 | 0.359 |
| 10 | Odette | camp1 | [4, 4, 4, 4] | 37.915 | 0.3103 | -0.1888 | 0.753 |
| 10 | Cass | camp2 | [2, 2, 4, 4] | 62.058 | 0.3818 | 0.0249 | 1.920 |
| 10 | Cass | camp2 | [2, 2, 4, 4] | 62.058 | 0.3818 | 0.0262 | 1.922 |
| 11 | Odette | camp1 | [4, 4, 4, 4] | 38.98 | 0.3103 | -0.5541 | 0.414 |
| 11 | Dmitri | camp2 | [3, 5, 4, 6] | 59.113 | 0.1057 | 0.0989 | 0.599 |
| 11 | Dmitri | camp2 | [5, 3, 6, 2] | 59.113 | 0.0043 | 0.1581 | 0.178 |
| 11 | Cass | camp2 | [2, 2, 4, 4] | 59.113 | 0.3818 | -0.1195 | 1.686 |
| 11 | Cass | camp2 | [2, 2, 4, 4] | 59.113 | 0.3818 | 0.0326 | 1.838 |
| 11 | Noor | camp3 | [4, 4, 4, 4] | 31.066 | 1.0 | 0.0041 | 2.489 |
| 11 | Noor | camp2 | [4, 4, 4, 4] | 59.113 | 0.0556 | -0.0852 | 0.178 |
| 12 | Dmitri | camp2 | [3, 5, 4, 6] | 56.103 | 0.1057 | -0.02 | 0.455 |
| 12 | Dmitri | camp2 | [4, 5, 5, 6] | 56.103 | 0.0212 | 0.085 | 0.180 |
| 12 | Noor | camp3 | [4, 4, 4, 4] | 30.123 | 1.0 | 0.0372 | 2.447 |
| 12 | Noor | camp2 | [4, 4, 4, 4] | 56.103 | 0.0556 | -0.0226 | 0.227 |
| 12 | Odette | camp1 | [4, 4, 4, 4] | 40.403 | 0.3103 | -0.2239 | 0.779 |
| 12 | Cass | camp2 | [2, 2, 4, 4] | 56.103 | 0.3818 | -0.0537 | 1.660 |
| 12 | Cass | camp2 | [2, 2, 4, 4] | 56.103 | 0.3818 | 0.062 | 1.775 |
| 13 | Odette | camp1 | [4, 4, 4, 4] | 41.484 | 0.3103 | -0.108 | 0.922 |
| 13 | Noor | camp3 | [4, 4, 4, 4] | 29.195 | 1.0 | -0.0497 | 2.286 |
| 13 | Noor | camp2 | [4, 4, 4, 4] | 53.303 | 0.0556 | 0.0284 | 0.266 |
| 13 | Cass | camp2 | [2, 2, 4, 4] | 53.303 | 0.3818 | 0.0675 | 1.696 |
| 13 | Cass | camp2 | [2, 2, 4, 4] | 53.303 | 0.3818 | -0.0951 | 1.533 |
| 13 | Dmitri | camp2 | [3, 5, 4, 6] | 53.303 | 0.1057 | 0.0294 | 0.480 |
| 13 | Dmitri | camp2 | [3, 5, 4, 6] | 53.303 | 0.1057 | 0.0109 | 0.462 |
| 14 | Noor | camp3 | [4, 4, 4, 4] | 28.4 | 1.0 | -0.0821 | 2.190 |
| 14 | Noor | camp2 | [4, 4, 4, 4] | 50.379 | 0.0556 | 0.0031 | 0.227 |
| 14 | Odette | camp1 | [4, 4, 4, 4] | 42.437 | 0.3103 | -0.1157 | 0.938 |
| 14 | Cass | camp2 | [2, 2, 4, 4] | 50.379 | 0.3818 | -0.0679 | 1.471 |
| 14 | Cass | camp2 | [2, 2, 4, 4] | 50.379 | 0.3818 | 0.2208 | 1.759 |
| 14 | Dmitri | camp2 | [3, 5, 4, 6] | 50.379 | 0.1057 | -0.0167 | 0.409 |
| 14 | Dmitri | camp2 | [3, 5, 4, 6] | 50.379 | 0.1057 | 0.0885 | 0.515 |
| 15 | Dmitri | camp2 | [3, 5, 4, 6] | 47.518 | 0.1057 | -0.0002 | 0.402 |
| 15 | Dmitri | camp2 | [3, 5, 4, 6] | 47.518 | 0.1057 | -0.0554 | 0.347 |
| 15 | Noor | camp3 | [4, 4, 4, 4] | 27.677 | 1.0 | 0.068 | 2.282 |
| 15 | Noor | camp2 | [4, 4, 4, 4] | 47.518 | 0.0556 | 0.0743 | 0.286 |
| 15 | Cass | camp2 | [2, 2, 4, 4] | 47.518 | 0.3818 | -0.0219 | 1.429 |
| 15 | Cass | camp2 | [2, 2, 4, 4] | 47.518 | 0.3818 | 0.0665 | 1.518 |
| 15 | Odette | camp1 | [4, 4, 4, 4] | 43.386 | 0.3103 | -0.5166 | 0.561 |
| 15 | Odette | camp1 | [4, 4, 4, 4] | 43.386 | 0.3103 | -0.1384 | 0.939 |
| 16 | Dmitri | camp2 | [3, 5, 4, 6] | 45.052 | 0.1057 | 0.0088 | 0.390 |
| 16 | Dmitri | camp1 | [3, 5, 4, 6] | 43.783 | 0.3103 | -0.1063 | 0.981 |
| 16 | Odette | camp1 | [4, 4, 4, 4] | 43.783 | 0.3103 | 0.1065 | 1.193 |
| 16 | Odette | camp1 | [4, 4, 4, 4] | 43.783 | 0.3103 | 0.1401 | 1.227 |
| 16 | Cass | camp2 | [2, 2, 4, 4] | 45.052 | 0.3818 | -0.0071 | 1.369 |
| 16 | Cass | camp2 | [2, 2, 4, 4] | 45.052 | 0.3818 | 0.0104 | 1.386 |
| 16 | Noor | camp3 | [4, 4, 4, 4] | 26.84 | 1.0 | -0.0118 | 2.135 |
| 16 | Noor | camp2 | [4, 4, 4, 4] | 45.052 | 0.0556 | 0.153 | 0.354 |
| 17 | Dmitri | camp2 | [3, 5, 4, 6] | 43.058 | 0.1057 | -0.1719 | 0.192 |
| 17 | Dmitri | camp1 | [3, 5, 4, 6] | 42.283 | 0.3103 | 0.0092 | 1.059 |
| 17 | Noor | camp3 | [4, 4, 4, 4] | 26.122 | 1.0 | -0.0462 | 2.044 |
| 17 | Noor | camp2 | [4, 4, 4, 4] | 43.058 | 0.0556 | -0.0095 | 0.182 |
| 17 | Cass | camp2 | [2, 2, 4, 4] | 43.058 | 0.3818 | -0.0327 | 1.282 |
| 17 | Cass | camp2 | [2, 2, 4, 4] | 43.058 | 0.3818 | -0.0782 | 1.237 |
| 17 | Odette | camp1 | [4, 4, 4, 4] | 42.283 | 0.3103 | 0.0687 | 1.119 |
| 17 | Odette | camp1 | [4, 4, 4, 4] | 42.283 | 0.3103 | -0.1233 | 0.927 |
| 18 | Cass | camp2 | [2, 2, 4, 4] | 41.655 | 0.3818 | -0.134 | 1.138 |
| 18 | Cass | camp2 | [2, 2, 4, 4] | 41.655 | 0.3818 | 0.057 | 1.329 |
| 18 | Odette | camp1 | [4, 4, 4, 4] | 41.062 | 0.3103 | -0.3984 | 0.621 |
| 18 | Odette | camp1 | [4, 4, 4, 4] | 41.062 | 0.3103 | -0.1122 | 0.907 |
| 18 | Noor | camp3 | [4, 4, 4, 4] | 25.47 | 1.0 | 0.0072 | 2.045 |
| 18 | Noor | camp2 | [4, 4, 4, 4] | 41.655 | 0.0556 | -0.0818 | 0.104 |
| 18 | Dmitri | camp2 | [3, 5, 4, 6] | 41.655 | 0.1057 | -0.0393 | 0.313 |
| 18 | Dmitri | camp1 | [3, 5, 4, 6] | 41.062 | 0.3103 | 0.0142 | 1.034 |
| 19 | Dmitri | camp2 | [3, 5, 4, 6] | 40.249 | 0.1057 | -0.0769 | 0.264 |
| 19 | Dmitri | camp1 | [3, 5, 4, 6] | 40.369 | 0.3103 | 0.1646 | 1.167 |
| 19 | Cass | camp2 | [2, 2, 4, 4] | 40.249 | 0.3818 | -0.063 | 1.166 |
| 19 | Cass | camp2 | [2, 2, 4, 4] | 40.249 | 0.3818 | 0.0219 | 1.251 |
| 19 | Odette | camp1 | [4, 4, 4, 4] | 40.369 | 0.3103 | 0.3976 | 1.400 |
| 19 | Odette | camp1 | [4, 4, 4, 4] | 40.369 | 0.3103 | 0.2264 | 1.229 |
| 19 | Noor | camp3 | [4, 4, 4, 4] | 24.795 | 1.0 | -0.056 | 1.928 |
| 20 | Noor | camp3 | [4, 4, 4, 4] | 24.213 | 1.0 | 0.0387 | 1.976 |
| 20 | Noor | camp2 | [4, 4, 4, 4] | 39.03 | 0.0556 | -0.0291 | 0.145 |
| 20 | Odette | camp1 | [4, 4, 4, 4] | 38.433 | 0.3103 | 0.112 | 1.066 |
| 20 | Odette | camp1 | [4, 4, 4, 4] | 38.433 | 0.3103 | 0.3216 | 1.276 |
| 20 | Cass | camp2 | [2, 2, 4, 4] | 39.03 | 0.3818 | -0.0276 | 1.164 |
| 20 | Cass | camp2 | [2, 2, 4, 4] | 39.03 | 0.3818 | 0.0283 | 1.220 |
| 20 | Dmitri | camp2 | [3, 5, 4, 6] | 39.03 | 0.1057 | -0.0706 | 0.260 |
| 20 | Dmitri | camp1 | [3, 5, 4, 6] | 38.433 | 0.3103 | -0.3389 | 0.615 |

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
