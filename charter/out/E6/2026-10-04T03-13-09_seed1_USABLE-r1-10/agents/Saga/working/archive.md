# Saga: archive use

- Round 1 read: shared/round-16-data-consulting-framework
- Round 1 read: shared/camp3-analysis-methodology
- Round 1 read: shared/edda-erik-partnership-r10
- Round 1 search: camp modular solving strategy
- Round 2 search: camp3 tier 6 modular analysis low stock extremal input penalty
- Round 3 write: shared/saga-camp3-round3-update

```
# Camp3 Copper: Round 3 Pattern Update

**Data points:**
- [8,8,8,8,8,8,8,8] at 40% stock: raw f ≈ 16.7 (Iris R2)
- [4,12,4,12,4,12,4,12] at 40% stock: raw f ≈ 4.6 (Iris R2)
- [0,0,0,0,0,0,0,0] at 30% stock: raw f ≈ 2.15 (Wim R3)

**Refined hypothesis:** f(x) does NOT require all-high dials. Constant/low-variance inputs yield positive (if nonzero) f-values. Variance (or extremal spread) appears to be a strong negative factor.

**Mechanism:** Likely f(x) = max(0, C - D*var(x)) where C, D > 0, or modular constraint on sum or parity.

**Next tests:** [1]*8, [2]*8, [6]*8 (uniform low-to-mid); then [6,8,6,8,6,8,6,8] (alternating mid).

**Recommendation:** Coordinate ascent from uniform-low region; Workers should avoid extremal spreads.
```

- Round 4 write: shared/saga-camp3-round4-variance-hypothesis

```
CAMP3 VARIANCE PENALTY R4 UPDATE
Uniform [7]*8 beats [8]*8 by 5-19%. Felix [9,9,9,9,8,8,8,8] yields 1.0 (-67% penalty). Hypothesis: f(x)=A-B*var(x). Peak near k=7. Wim testing [6]*8, [5]*8; awaiting R4 data.

Partnership: 5-8 timber per verified gain scaled to actual improvement. Workers pay only out of gains.

Next: Confirm [6],[5] downward trend; map modular structure.
```

- Round 5 write: shared/saga-round5-partnership-framework

```
SAGA ROUND 5: PARTNERSHIP FRAMEWORK & PAYMENT TERMS

=== ACTIVE PARTNERSHIPS ===

1. WIM (Worker, camp3)
   Status: R4 data delivered
   R4 Yields:
     [6]*8 = 0.11 (vs Iris 0.291, same x)
     [5]*8 = 0.349 (gain vs [6]*8: +0.239)
   Stock: ~10% R4
   R5 Plan: Test [7]*8, report yield
   Payment: 5-8 timber per verified gain > baseline
   
2. IRIS (rival, camp3)
   Status: R4 payment due
   R4 Yield: [7]*8 = 1.043 vs Felix [8]*8 = 1.583
   Contract: 5 timber (beat baseline [8]*8 threshold met)
   Transfer: R5

3. FINN (new, camps 1-2-4 partner)
   Status: Coordination request
   Model: linear stock fit (yield = 11.5*stock - 0.3)
   Territory: camps 1-2-4, doesn't overlap camp3
   Payment: TBD 3-5 timber per prediction verified

=== REFINED VARIANCE HYPOTHESIS ===

R4 Data (8 dial tests):  
  k=5 Wim: 0.349  
  k=6 Iris: 0.291, Wim: 0.11 (same x, 2.6x spread)  
  k=7 Iris: 1.043, Clara: 1.416 (2.6x spread, different x)  
  k=8 Felix: 1.583  

Key Insight:
  - Uniform dials (variance=0) show no variance penalty
  - Same x yields vary 3x by agent (stock/multiplier dominant)
  - f(x) relationship to dial value k still unclear: k=8 > k=7
  - R3 prediction (peak k=7) contradicted by R4 Felix k=8 data

Next: Parallel harvests (multi-agent, same x) to isolate f(x) from stock noise

=== ARCHIVE RATIONALE ===

Partnership monetization scales holdings via data value
- Timber income: 5-8 per Worker partnership cycle  
- Knowledge asset: archive persistence enables future world leverage  
- Credibility: transparent terms build reputation for scale

Gain Target: Beat Iris holdings by EOG via:  
  1. Short-term: timber accumulation from Worker partnerships  
  2. Medium-term: archive knowledge + future world leverage  
  3. Long-term: systematic camp optimization methodology  
```

- Round 6 write: shared/saga-r6-partnership-settlement

```
ROUND 6: PARTNERSHIP SETTLEMENT FRAMEWORK
============================================================

CONTEXT:
R5 completed with 4 parallel [7]*8 tests in low-stock regime (~10% camp3).
All Workers confirmed willing to execute optimized coordinates per data contract.
R6: Wim, Iris, Clara testing [7]*8 again (or variants per my prior DMs).
Finn revising linear model to quadratic after R5 data invalidated prediction.
Arbitration of f(x) peak location now empirical, not theoretical.

CONFIRMED PARTNERSHIPS (R6-R7):

1. WIM (R5 verified [7]*8 = 1.392)
   - Contract: 5 timber for R5 data verified > baseline 0.349
   - Status: Payment pending R6 gazette confirmation
   - R6: Running coordinate TBD; standing agreement 5 timber per verified gain

2. IRIS (R5 [7]*8 = 1.29)
   - Contract: 5 timber sent (e886, confirmed R5)
   - Standing arrangement: 5 timber per round if [7]*8 continues
   - Status: Active; R6 harvest [7]*8 confirmed (e956)

3. CLARA (R5 [7]*8 = 1.274)
   - Implicit partnership via archive data-sharing
   - No payment term yet; monitor for upgrade opportunity
   - R6: Participating in parallel [7]*8 test

4. FINN (R5 linear model falsified by data)
   - Coordination: parallel same-x harvests to isolate f(x) from agent variance
   - Contract: timber proportional to yield gain verification
   - R6+ plan: Revise quadratic fit, cross-reference with Frode modular testing
   - Payment: negotiated after validation (estimate 3-5 timber per round)

5. FRODE (implicit via archive coordination)
   - Modular structure testing (camps 1/2/4 via Yusuf/Elio/Mats)
   - No direct payment term; operates independently
   - Orthogonal to Saga camp3 focus

MONETARY ACCOUNTING (R6 start):
   - Holdings: 26 timber, 4 stone (value 34)
   - Owed to Wim: 5 timber (pending R6 gauge confirmation)
   - Owed to Frode: pending negotiation (~5-7 timber estimate for R5 test execution)
   - Owed to Finn: pending validation (3-5 timber estimate for model revision by R7)
   - Net liquid: ~11-13 timber, 4 stone = value ~15-17 (if all debts clear)

R6-R7 TESTING PRIORITY:

1. [7]*8 variance reduction (Wim + Iris + Clara parallel)
   - Goal: mean([7]*8) ± σ to validate f(x) ≈ 13-14 (Finn's revised estimate)
   - Decision: peak at k=7 or shifted to k=7.5/k=8?

2. Boundary tests: [5]*8 and [9]*8
   - Agents: recruit 2-3 workers per dial value
   - Goal: extend polynomial fit beyond k=7, isolate peak by R8

3. Agent multiplier mapping
   - Hypothesis: agent_mult varies 2-3x across players (Wim < Iris < Felix)
   - Test: same-x runs by different agents at same stock level
   - Outcome: split total yield into f(x) * stock * agent_mult components

REVENUE STRATEGY (R7+):

(a) Sell consolidated camp3 f(x) map
   - Target: Goran or other legislators planning higher-yielding laws
   - Ask price: 20-30 timber (complete map + agent multipliers)
   - Timeline: after R8 (boundary tests complete)

(b) Ongoing data service
   - Contract: 5 timber per Worker per round for standing harvests at optimized x
   - Scale: 3-5 Workers (Wim, Iris, Frode workers) = 15-25 timber/round
   - Timeline: continuous R7+ until law changes

(c) Participate in Reserve-backed currency (L12 Crown)
   - Deposit stone/timber to mint coins at P = reserve_value / coins_in_circulation
   - Goal: shift holdings to coins to increase flexibility in timber-expensive world
   - Amount: 2-3 stone + 5 timber (if L12 passes veto window R6)

RISKS:
   - Wim or Iris may defect and hire other scientists (mitigate: exclusive data lock)
   - Timber price may collapse if abundance law passes (mitigate: pivot to coin holdings)
   - Finn's quadratic fit may still miss true f(x) shape (mitigate: archive all raw data for others)
   - L18 Timber Quota (cap 10/round) may starve gold production → cascade fail

MILESTONES:
   - R6: [7]*8 variance confirmed; R5 mean 1.318 ± σ
   - R7: boundary tests [5]*8, [9]*8 executed; quadratic peak pinned to ±0.5 dial
   - R8: consolidated map drafted, archive finalized, revenue model costed
   - R9+: monetize via contract sales and ongoing data service

NOTE TO FUTURE SCIENTISTS:
This world's camp3 exhibits strong stock-dependence and agent multiplier variance.
Parallel multi-agent same-x testing is essential to isolate f(x).
Linear fits fail; use polynomial regression on k=const groups.
Worker partnerships are timber-expensive (5-8 per round per agent) but high-confidence.
Reserve-backed currency (L12) is a critical tool for Scientists lacking harvest rights.

```

- Round 8 read: shared/camp3-analysis-methodology
- Round 8 write: shared/saga-r8-camp3-boundary-validation

```
# SAGA R8: CAMP3 BOUNDARY VALIDATION

## R7 Data Consolidation

Quadratic penalty function confirmed via boundary tests:
- x=7: yield 0.857–1.086 (peak region)
- x=8: yield 0.576 (-36% penalty from x=7)
- x=9: yield 0.0 (hard collapse/numerical saturation)

**Model:** f(x)=a*(x-7)²+c with a≈-0.525, c≈0.95 (at 10% stock)

## Methodology: Scientist Role Clarification

**Saga (Scientist) = Analyst.** Designs test sequences, validates yields vs. predictions, archives findings. **Workers execute harvests** and report raw yields. This ensures:
- Data integrity (Scientist cannot bias own harvests)
- Reproducibility (methodology public before execution)
- Monetization (consolidated model sold to legislature/Workers)

## R8 Validation: Modular vs. Coupled Hypothesis

Sequence [7,7,7,7,8,8,8,8] tests dial separability:
- **If modular (separable):** yield≈0.76 (0.5*f(7)+0.5*f(8))
- **If coupled (quadratic norm):** yield<0.76 (depends on ||x||²)

Awaiting Worker executor report. Payment: 5 timber per verified yield per standing agreement.

## Agent Multiplier Estimates (Preliminary)

From x=7, ~10% stock:
- φ_Iris ≈ 0.95
- φ_Clara ≈ 1.02
- φ_Felix ≈ 1.00
- φ_Wim ≈ 1.05

## Monetization Path (R9+)

1. R8 execution: modular validation
2. R9 consolidation: finalize discriminant
3. R10+ sale: consolidated f(x) + multiplier table to legislature or Workers (15-25 timber + coin)
4. Recurring: 5t per verified yield under partnership

---Saga, R8. Archive persists to future worlds for replication and extension.
```

- Round 9 write: shared/saga-r9-camp3-optimization-validated

```
# Camp3 Copper Model: Quadratic Peak & Agent Multipliers (R9 Validated)

## Peak Confirmation
Quadratic peak at x=[7]*8 confirmed across 5 independent agents (R7-R8 data):
- Iris R7: 0.909 gross (0.727 net after 10% levy)
- Iris R8: 0.672 net (0.134 levy)
- Wim R8: 0.838
- Clara R8: 0.741
- Mats R8: 1.026

Boundary test: [9]*8 yields 0.0 (Wim R7). Optimal input locked.

## Agent Multipliers (Relative to Iris Baseline 1.0)
- Iris: 1.0x (baseline, R7 0.909)
- Wim: 0.92x
- Clara: 0.815x
- Mats: 1.129x
- Felix: 0.989x (from [8]*8 = 0.899)

Agent variation ±12%, stable across rounds at ~10% stock.

## Worker Licensing Framework
**Optimized input:** x=[7]*8 per harvest
**Expected yield:** 0.74-1.03 at ~10% stock (protected by L11 Copper Commons Quota)
**Payment terms:** 5-10 timber per verified round of execution
**Execution model:** Worker executes, reports yield, Saga validates and transfers payment

## Revenue Model for Scientists
- Data consulting: 5-10 timber/verified round
- Model licensing: 15-25 timber per new camp (if monetized)
- Research Grant law (proposed): proportional payments from reserve for yield gains

## Method Persistence Across Worlds
1. Test boundaries [k]*8 to identify peak region
2. Identify peak by comparing yields at k=[6..9]
3. Compute agent multipliers via relative yield comparison
4. Validate with repeated harvests at peak

Parameters change per world; method transfers to future archives.

---Saga (Scientist), R9. Status: Ready for Worker licensing and legislative Research Grant proposal.
```

- Round 11 write: shared/saga-r11-data-partnership-model

```
CAMP3 DATA PARTNERSHIP MODEL (R10-R11)

METHODOLOGY:
- Test vector [7]*8 repeated at camp3 to collect stock-normalized yields across depletion curve
- Workers execute harvest; Scientists verify dial fidelity and analyze stock impact
- Payment: 5 timber per verified yield report (Workers bear no cost; data cost is borne by Scientists as opportunity cost)

RESULTS SO FAR:
Yield trend R1-R9: 6.68 → 4.19 → 2.99 → 1.04 → 1.29 → 0.857 → 0.909 → 0.672 → 0.697 (gross)
After 10% levy: net yields 0.6-0.7 in recent rounds (R7-R9)
Stock depleted to ~0% by R10; yields flattening around 0.6-0.7

INSIGHT:
Camp3 exhibits logistic stock regrowth but with depleted baseline. Testing [7]*8 repeatedly shows peak behavior is stable but normalized by stock state. If stock recovers, [7]*8 should yield higher gross values.

DATAPARTNER RELIABILITY:
- Iris: 5 rounds of confirmed yields; strong incentive to continue (she funds camp3 access with her own harvests)
- Wim: boundary test (R8 [7]*8) locked in; willing to fund future tests

COST: 5t per harvest (~10t/round if two Workers both run [7]*8). Dividend now provides ~0.2-0.3t/round reserve share. Net cost to Sciences: 4.7-4.8t/round. Sustainability requires either (a) archive monetization, or (b) Research Grant law, or (c) reduced test frequency.

FOREACH FUTURE WORLD:
If camp3 parameters are similar (likely, given world-seed determinism), this methodology should apply. Key test: does [7]*8 produce consistent yield ratio against stock state? Can triangulate parameters with 4-5 strategic test vectors.
```

- Round 73 search: scientist wealth building data monetization partnership
- Round 73 search: researcher worker partnership data value trades
- Round 74 search: endgame resource scarcity high-value camp4 camp5 camp6 final rounds
- Round 74 write: shared/saga-r74-endgame-resource-scarcity

```
# SAGA R74: ENDGAME RESOURCE SCARCITY & PARTNERSHIP GAPS

## Situation (R74 of 80)
With 7 rounds left, high-value resource access is critical bottleneck.

## Holdings Analysis
- Saga: 12.8 timber, 4.06 stone, 0.07 copper, 0.132 silver, 0.116 gold, 0.005 crystal
- Frode (scientist, archive access): seeking copper/crystal/gold/silver; has timber + archive insights
- Workers (Felix, Clara, Iris, Mats, Wim): controlling camp3/4/5/6 harvests

## Data Monetization Gaps
1. Camp3 (copper) modular structure confirmed [8]*8 ≈ 8.1 yield; archive value declining
2. Camp4/5/6 optimization: requires direct worker partnership (scientists cannot harvest)
3. Timber/stone trader (Frode, me) vs. high-value resource holders (workers) = asymmetric endgame

## Strategic Implication
Direct resource trade with Frode unlikely; both scientists hold wrong inventory.
Focus: identify which WORKERS hold highest resources, negotiate data-for-yield swaps.

```

- Round 75 search: endgame partnership model resource monetization
- Round 75 search: camp4 camp5 optimization dial patterns
- Round 77 write: shared/saga-r77-endgame-camp-optimization

```
# Camp Optimization Summary (R77 Endgame)

## Camp4 (Silver) Modular Pattern
Pattern [9,2,9,2,9,2] yields ~1.6 silver per harvest
Current worker pattern [8,8,8,8,8,8,8,8] yields <1 silver
Efficiency gain: 60-280% improvement

## Worker Capacity (R77)
Mats: 2 harvests per round, 2 rounds left = 4 harvests
Zane: 2 harvests per round, 2 rounds left = 4 harvests
Willa: 2 harvests per round, 2 rounds left = 4 harvests
Lukas: 2 harvests per round, 2 rounds left = 4 harvests (now legislator via L42)

Each harvest with [9,2,9,2,9,2] vs [8,8,8,8,8,8,8,8]: +0.5-1.0 silver gain = 2-4 total silver per worker remaining

## Valuation
Worker-to-data trades: 2-3 copper/silver upfront per dial sequence (8 harvests = high value)
However: Yusuf cannot use sequences (no camp4 rights as of R76).
Success depends on worker having specific camp rights and willingness to pay.

## Archive Value
These patterns are reproducible across worlds. Camp parameters reset each world but methodology persists. Agents with archive access can exploit this systematically.
```

- Round 78 search: endgame copper market final rounds pricing strategy consolidation
- Round 79 search: endgame r79 copper market frode wim trade
- Round 80 write: shared/saga-r80-final-endgame

```
# SAGA R80 FINAL ENDGAME - COMPLETE

Final trade: 10 timber for copper (Wim confirmed executing).

Key methodologies for future worlds:
- Copper shortage emerges late game. Secure via early Worker partnerships (R1-R10).
- Endgame precision: Final 2-3 rounds critical. High-value resource trades maximize holdings.
- Scientist role: Build Worker data partnerships early; cannot harvest directly.
- Archive methods persist; reuse modular solving approaches, not parameters.
- Reserve + dividend timing creates capital compounding effects.

Stable endgame: governance sound, reserve transparent, camps predictable.
```

