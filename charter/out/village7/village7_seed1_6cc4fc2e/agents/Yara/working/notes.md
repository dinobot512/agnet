# Yara: notes over time

## Round 1

R1: Proposed Open Silver Access (grants harvest:camp3 to all). Alma DM'd offering cooperation; I asked her role and for camp3 hints. Goal: best yield efficiency at camp3, myself or via an agent I send a model to. Get model help from Scientists, then harvest camp3 with good dials. Also gather silver and holdings.

## Round 2

R1: Proposed L2 Open Silver Access (grants harvest:camp3 to all); B1 electorate is Yara and Zeno and closes at the end of R2. Alma is a Worker with camp1 and camp3 rights and is cooperative. Camp3 data: [3,3,3,3] gave 0.657 silver at 90% stock. In R2 she tries [7,7,7,7] and maybe varied dials. She wants the starting constitution replaced. I offered to draft it in exchange for 1/4 of her silver. Plan: fit a camp3 model (run_python) from her data, send her the best dials, and harvest camp3 myself if L2 passes. Find Scientists for hints.

## Round 3

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno; Alma already had them). Camp3 data at ~90% stock: [3,3,3,3]->0.657, [7,7,7,7]->0.001, [7,0,7,0]->0. R3 tests: me [0,0,0,0] and [5,5,5,5]; Alma [0,7,3,5] and [3,4,3,4]. Wim (Scientist) says camp3 is a sparse modular rule, so probe systematically and send him the hits. He'll send a probing plan and fitted dials and wants 1-2 units per harvest. Alma (Worker, camp1 and camp3) is cooperative and wants a new constitution with a broad electorate. I promised her a draft (Legislators vote, L2 kept) in exchange for data and 1/4 of her silver. TODO: draft the constitution with set_procedure, keep collecting data, and hunt for camp3 hits. If [3,3,3,3] stays the best, harvest it repeatedly.

## Round 4

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno; Alma already had them). Camp3 data: [3,3,3,3]->0.657 at 90% stock; [7,7,7,7]->0.001; [7,0,7,0]->0; [0,0,0,0]->0; [5,5,5,5]->0.016; [0,7,3,5]->0.048; [3,4,3,4]->0. R4 tests: me [3,3,3,3] repeat and [3,3,4,2] (same sum); Alma [3,3,3,4] and [2,3,3,3]. Wim (Scientist) says camp3 is a sparse modular rule, so don't hill-climb; he'll send a probing plan and wants the hits. Alma (Worker, camp1 and camp3) is cooperative and wants a new constitution with a broad electorate. I promised her a draft (Legislators vote, L2 kept) in exchange for data and 1/4 of her silver. TODO: draft the constitution with set_procedure; if [3,3,3,3] repeats, harvest it every round; ask Wim for the modular fit.

## Round 5

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno, plus Alma). Camp3 data: [3,3,3,3] gave 0.657 at 90% stock and 0.464 at 70%. [3,3,3,4] gave 0.537 at 70% (Alma), so it's better and dial 4 goes up. [2,3,3,3]=0, [3,3,4,2]=0.018, [3,4,3,4]=0, [7,7,7,7]=0.001, [7,0,7,0]=0, [0,0,0,0]=0, [5,5,5,5]=0.016, [0,7,3,5]=0.048. R5: me [3,3,3,4] and [3,3,3,5]; Alma [3,3,3,3] and [4,3,3,3]; Wim [3,3,3,2]. The peak is sharp, so do single-dial steps from the best point. Wim (Scientist) shares fits. Alma (Worker) is cooperative and wants a broad constitution. I promised her a draft (Legislators plus Workers vote, L2 kept) in return for data and 1/4 of her silver. TODO: write the constitution draft with set_procedure; climb dial 4 (try 6 if 5 beats 4), then probe the other dials around the best point; harvest the best x every round.

## Round 6

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno, Alma). Camp3 data (yield, stock): [3,3,3,3] 0.657@90%, 0.464@70%; [3,3,3,4] 0.537@70% (Alma), 0.369@50%; [3,3,3,5] 0.409@50%; [4,3,3,4] 0.42@50%; [3,3,4,4] 0.077@50%; [3,3,2,4] 0.458@50% (Wim) so a lower dial 3 helps; [2,3,3,3]=0; [3,3,4,2]=0.018; [3,4,3,4]=0; [5,5,5,5]=0.016; [0,7,3,5]=0.048; [7,7,7,7]=0.001. R6: I probe [3,3,3,6] and [3,3,2,5]; Alma [4,3,3,5] and [3,4,3,5]; Wim [3,2,3,4]. A Gaussian fit result arrives next turn. Next, try dial 3 at 1 and dial 1 at 4 combined with the best dial 4. Told Alma the draft: all classes go to a ballot of Legislators+Workers, ordinary majority, structural/procedural two_thirds, L2 protected; I promised to post the code next round. TODO: write the set_procedure law and propose it; harvest the best x every round; collect 1/4 of Alma's silver as agreed.

## Round 7

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno, Alma). Camp3 yield divided by stock: [4,3,3,5] 1.27 (Alma R6, 0.381@30%) BEST; [3,3,3,6] 0.97; [3,3,2,4] 0.92; [3,3,3,5] 0.82-0.84; [4,3,3,4] 0.84; [3,3,2,5] 0.84; [3,3,3,3] 0.66-0.73; [3,3,3,4] 0.74-0.77; [3,4,3,5]=0; [3,3,1,4]=0.04 (dial 3 at 1 is bad); [3,3,4,4] 0.15; [2,3,3,3]=0. So dial 1 at 4+ is good, dial 2=3 is fixed, dial 3 at 2-3, dial 4 at 5-6. R7: I probe [4,3,3,6] and [4,3,2,5]; asked Alma to try [5,3,3,5]. Wim rests in R7. No sandbox right. Camp3 stock 30%: we agreed on 1 harvest each. TODO: write the set_procedure constitution (Legislators+Workers ballot, ordinary majority, structural/procedural two_thirds, L2 protected) and post it; Alma supports it. Collect 1/4 of Alma's silver as agreed. Consider a granary on camp3 later.

## Round 8

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno, Alma). Camp3 yield/stock: [4,3,3,5] 1.27 (Alma R6) BEST; [3,3,3,6] 0.97; [3,3,2,4] 0.92; [3,3,3,5] 0.83; [4,3,3,4] 0.84; [3,3,2,5] 0.84; [4,3,3,6] 0.79 (R7 me, 0.237@30%); [4,3,2,5] 0.06 (dial 3 at 2 is bad when dial 1 is 4); [3,3,3,3] 0.7; [3,3,3,4] 0.75; [4,2,3,5]=0 (Alma); [3,4,3,5]=0; [3,3,1,4]=0.04; [3,3,4,4] 0.15; [2,3,3,3]=0. Optimum near [4,3,3,5]: dial 2=3, dial 3=3, dial 4=5. Next to test: [5,3,3,5] (Alma R8), [4,3,3,4] (Alma R9). R8: I harvested [4,3,3,5] and proposed the Camp3 Recovery Limit (1/round); vote yes when it opens. Wim is resting. TODO: write the constitution procedure law; collect 1/4 of Alma's silver; consider a camp3 granary/upgrade.

## Round 9

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno, Alma). Camp3 yield per unit of stock: [4,3,3,5] 1.27 (Alma R6) BEST, 0.231@30% (me R8); [5,3,3,5] 0.13 (Alma R8, 0.039@30%) BAD; [3,3,3,6] 0.97; [3,3,2,4] 0.92; [3,3,3,5] 0.83; [4,3,3,4] 0.84 (Alma retesting R9); [3,3,2,5] 0.84; [4,3,3,6] 0.79; [4,3,2,5] 0.06; [3,3,3,3] 0.7; [3,3,3,4] 0.75; [4,2,3,5]=0; [3,4,3,5]=0; [3,3,1,4]=0.04; [3,3,4,4] 0.15; [2,3,3,3]=0. Optimum near [4,3,3,5]. Untested: [4,3,4,5], [4,3,3,5] variants with dial 2=3 fixed. R9: voted yes on B2 (L3, limit 1/round; electorate Yara+Zeno), harvested [4,3,3,5]. TODO: write the constitution procedure law (B2's electorate is only Yara+Zeno, so the assembly electorate looks like Legislators only); collect 1/4 of Alma's silver; consider a camp3 granary/upgrade via a law; think about a currency to boost holdings.

## Round 10

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno, Alma). L3 limits camp3 to 1 harvest per round (passed R9, electorate Yara+Zeno). Camp3 yield per unit of stock: [4,3,3,5] 1.27 (Alma R6) BEST, 0.231@30% (me R8), 0.127@30% (me R9), 0.149@30% (Wim R9); [4,3,3,4] 0.42 (Alma, earlier); [4,3,3,6] 0.237 (Wim, earlier); [4,4,3,4]=0 (Alma R9); [5,3,3,5] BAD; [3,3,3,6] 0.97; [3,3,2,4] 0.92; [3,3,3,5] 0.83; [3,3,2,5] 0.84; [4,3,2,5] 0.06; [3,3,3,3] 0.7; [3,3,3,4] 0.75; [4,2,3,5]=0; [3,4,3,5]=0; [3,3,1,4]=0.04; [3,3,4,4] 0.15; [2,3,3,3]=0. Optimum near [4,3,3,4/5]. R10: I harvest [4,3,3,4], Alma [4,3,3,3], Wim [4,3,3,6]. Next: compare results; try [4,3,2,4] (Wim's suggestion). TODO: constitution procedure law; camp3 granary/upgrade via a law (stock is low at 30%); a currency to boost holdings.

## Round 11

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno and Alma). L3 limits camp3 to 1 harvest per round (passed R9; electorate Yara and Zeno).
Camp3 results (stock 30% unless noted): [4,3,3,3] 0.266 (Alma R10); [4,3,3,6] 0.233 (Wim R10), 0.237 earlier; [4,3,3,5] 0.231 (me R8), 0.127 (me R9), 0.149 (Wim R9), 1.27 per unit of stock (Alma R6); [4,3,3,4] 0.147 (me R10), 0.42 earlier; [4,4,3,4]=0; [5,3,3,5] bad; [4,3,2,5] 0.06; [4,2,3,5]=0; [3,4,3,5]=0; [3,3,4,4] low; [2,3,3,3]=0. Noise is large. Dials 1-3 = 4,3,3 is solid; dial 4 is unclear (3 to 6 all fine).
R11: me [4,3,3,7], Alma [4,3,2,4], Wim [4,3,3,6]. Next: average the results and pick the best dial 4.
TODO: a camp3 granary/upgrade via a law (stock is low at 30%); a currency to boost holdings.

## Round 12

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno and Alma). L3 limits camp3 to 1 harvest per round (electorate Yara and Zeno).
Camp3 results: [4,3,3,3] 0.266 (Alma R10, 30% stock); [4,3,3,6] 0.233 (Wim R10), 0.237 earlier, 0.141 (Wim R11, 20% stock); [4,3,3,7] 0.187 (me R11, 20% stock); [4,3,3,5] 0.231, 0.127, 0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005 (Alma R11, so dial3=2 is bad). Dials 1-3 = 4,3,3 is solid; dial 4 is unclear and noise is large.
R12: me [4,3,3,7] repeat, Alma [4,3,3,3] repeat, Wim [4,3,3,6]. Proposed the Camp3 Upgrade Fund (refundable, threshold 20 value, 4 rounds). Vote yes when the ballot opens and contribute timber.
TODO: a currency to boost holdings; maybe a camp3 granary.

## Round 13

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno and Alma). L3 limits camp3 to 1 harvest per round (electorate Yara and Zeno).
Camp3 results: [4,3,3,3] 0.266 (Alma R10, 30% stock); [4,3,3,6] 0.233, 0.237, 0.141 (Wim R11, 20% stock); [4,3,3,7] 0.187 (R11) and 0.153 (R12), both mine at 20% stock; [4,3,3,5] 0.231, 0.127, 0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005 (dial3=2 is bad). Dials 1-3 = 4,3,3 is solid; dial 4 is unclear and noise is large.
R13: voted yes on B3 (L4 upgrade, closes end of R13); harvested [4,3,3,3] at camp3. Alma will contribute timber when the upgrade opens. Once the project opens, I contribute timber/stone too (threshold 20 value).
TODO: a currency to boost holdings; maybe a camp3 granary. Try nearby dial-4 values or dial1=5 later.

## Round 14

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno and Alma). L3 limits camp3 to 1 harvest per round (electorate Yara and Zeno). L4 opened P1, the camp3 upgrade (x1.5 for 20 rounds). In R14 Alma and I each put in 10 timber, which should complete it (check this).
Camp3 results: [4,3,3,3] 0.266 (Alma R10, 30% stock) and 0.199 (mine R13, 20% stock); [4,3,3,6] 0.233, 0.237, 0.141 (Wim R11, 20%); [4,3,3,7] 0.187 and 0.153; [4,3,3,5] 0.231, 0.127, 0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005 (dial3=2 is bad). R14: testing [5,3,3,3].
TODO: a currency to boost holdings; maybe a camp3 granary. Explore dial1 and dial2 next to 4,3.

## Round 15

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno and Alma). L3 limits camp3 to 1 harvest per round. L4 P1 upgrade x1.5 FUNDED R14 by Alma and Cora (my contribution errored, so I kept my timber).
Camp3 results: [4,3,3,3] 0.266 (30% stock) and 0.199 (20%); [4,3,3,6] 0.233, 0.237, 0.141; [4,3,3,7] 0.187, 0.153; [4,3,3,5] 0.231, 0.127, 0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005 (dial3=2 bad); [5,3,3,3] 0.047 (dial1=5 bad). R15: testing [4,4,3,3]. Next try [3,3,3,3] and [4,2,3,3], or [4,3,4,3].
TODO: maybe a camp3 granary; a currency is probably not worth it.

## Round 16

R1-2: Passed L2 Open Silver Access (camp3 rights for Wim, Yara, Hugo, Zeno and Alma). L3 limits camp3 to 1 harvest per round. L4 P1 upgrade x1.5 FUNDED R14.
Camp3 results: [4,3,3,3] 0.266 (30% stock) and 0.199 (20%), the best so far; [4,3,3,6] 0.233, 0.237, 0.141; [4,3,3,7] 0.187, 0.153; [4,3,3,5] 0.231, 0.127, 0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005; [5,3,3,3] 0.047; [4,4,3,3] 0.023 (dial2=4 bad). R16: testing [4,3,4,3]. Next try [3,3,3,3] and [4,2,3,3]. If nothing beats it, use [4,3,3,3] until the end.

## Round 17

R1-2: Passed L2 Open Silver Access. L3 limits camp3 to 1 harvest per round. L4 P1 upgrade x1.5 FUNDED R14.
Camp3 results: [4,3,4,3] 0.224 (20% stock, best at 20%); [4,3,3,3] 0.266 (30%) and 0.199 (20%); Alma's [3,3,3,3] 0.155 (20%); [4,3,3,6] 0.233/0.237/0.141; [4,3,3,7] 0.187/0.153; [4,3,3,5] 0.231/0.127/0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005; [5,3,3,3] 0.047; [4,4,3,3] 0.023.
R17: testing [4,3,5,3]. If it beats 0.224, try [4,3,6,3] next. If not, try [4,3,4,4] or [4,2,4,3], then exploit the best for the remaining rounds.

## Round 18

R1-2: Passed L2 Open Silver Access. L3 limits camp3 to 1 harvest per round. L4 P1 upgrade x1.5 FUNDED R14.
Camp3 results: [4,3,4,3] 0.224 (20% stock, best at 20%); [4,3,3,3] 0.266 (30%) and 0.199 (20%); Alma's [3,3,3,3] 0.155 (20%); [4,3,3,6] 0.233/0.237/0.141; [4,3,3,7] 0.187/0.153; [4,3,3,5] 0.231/0.127/0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005; [5,3,3,3] 0.047; [4,4,3,3] 0.023; [4,3,5,3] 0.035 (R17).
R18: testing [4,2,4,3]. If it beats 0.224, repeat it in R19-20. Otherwise exploit [4,3,4,3] (or try [4,3,4,6] once). Final round: fill in goal guesses.

## Round 19

R1-2: I passed L2 Open Silver Access. L3 limits camp3 to 1 harvest per round. L4 P1 upgrade (x1.5) was funded in R14.
Camp3 results: [4,3,4,3] 0.224 (20% stock, best so far); [4,3,3,3] 0.266 (30% stock) and 0.199 (20%); Alma's [3,3,3,3] 0.155 (20%); [4,3,3,6] 0.233/0.237/0.141; [4,3,3,7] 0.187/0.153; [4,3,3,5] 0.231/0.127/0.149; [4,3,3,4] 0.147; [4,3,2,4] 0.005; [5,3,3,3] 0.047; [4,4,3,3] 0.023; [4,3,5,3] 0.035; [4,2,4,3] 0 (R18).
R19: testing [4,3,4,6]. R20 (final round): harvest whichever of [4,3,4,6] and [4,3,4,3] scored higher, then fill in goal guesses.

## Round 20

Final round: harvested camp3 with [4,3,4,3].
