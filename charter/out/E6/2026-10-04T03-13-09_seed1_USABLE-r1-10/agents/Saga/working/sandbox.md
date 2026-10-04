# Saga: sandbox sessions

## Round 2 (e285)

```python
import numpy as np
# Iris's camp3 data: [8,8,8,8] -> 6.68, [4,12,4,12,4,12,4,12] -> 1.84, stock ~40%
# Observation: balanced dials outperform extremal ones
# Hypothesis: camp3 is peak-like or has variance penalty
data = {
    '[8,8,8,8]': 6.68,
    '[4,12,4,12,4,12,4,12]': 1.84,
}
print('Camp3 pattern: balanced inputs >> extremal')
print('Next: test [7,7,7,7], [6,8,6,8,6,8,6,8] for refinement')
```

Output:

```
Camp3 pattern: balanced inputs >> extremal
Next: test [7,7,7,7], [6,8,6,8,6,8,6,8] for refinement
```

## Round 4 (e656)

```python
import numpy as np; data = [2.509, 2.993, 2.753, 2.916, 3.001, 1.0, 2.491, 2.582]; print('R3 Camp3: [7]*8 beats [8]*8 by 5-19%. Variance penalty visible (Felix 1.0). Peak near k=7.'); print('Mean [8]*8: ' + str(round(np.mean([2.509, 2.753, 3.001, 2.491, 2.582]), 3)))
```

Output:

```
R3 Camp3: [7]*8 beats [8]*8 by 5-19%. Variance penalty visible (Felix 1.0). Peak near k=7.
Mean [8]*8: 2.667
```

## Round 5 (e883)

```python
import json

# R4 camp3 published yields with NEW Wim data
r4_camp3 = {
    'Iris': [1.043, 0.291],      # [7]*8, [6]*8
    'Wim': [0.11, 0.349],         # [6]*8, [5]*8
    'Clara': [1.416],             # [7]*8
    'Felix': [1.583],             # [8]*8
}

print('R4 CAMP3: REFINED VARIANCE HYPOTHESIS')
print('=' * 60)
print()
print('DATA BY DIAL VALUE k:')

# Group by dial uniformity
data_by_k = {
    5: {'Wim': 0.349},
    6: {'Iris': 0.291, 'Wim': 0.11},
    7: {'Iris': 1.043, 'Clara': 1.416},
    8: {'Felix': 1.583},
}

for k in sorted(data_by_k.keys()):
    yields = data_by_k[k]
    mean = sum(yields.values()) / len(yields)
    spread = max(yields.values()) - min(yields.values()) if len(yields) > 1 else 0
    print(f'  k={k}: agents={list(yields.keys())}, yields={list(yields.values())}, mean={mean:.3f}, spread={spread:.3f}')

print()
print('HYPOTHESIS REFINEMENT:')
print('  1. Uniform dials (k=5..8) show f(x) peaks near k=7')
print('     Evidence: k=7 mean (Iris+Clara)=1.23 > k=8 Felix=1.583? NO')
print('     Felix k=8 is HIGHER. Reversal from R3.')
print()
print('  2. Same x -> 3x spread: [6]*8 yields 0.291 (Iris) vs 0.11 (Wim)')
print('     Variance(x)=0 identical. Stock/agent factor >> variance effect')
print('     Stock R4 ~10% camp3: Wim yield 0.11 vs Iris 0.291 (2.6x)')
print()
print('  3. Wim k=5 yields 0.349 > Wim k=6 yields 0.11 (3.2x gain on same agent)')
print('     Suggests f(x) actually PEAKS at k=5, not k=7')
print('     OR stock changed between Wim samples (harvest order dependency)')
print()
print('REFINED MODEL:')
print('  yield = f(x) * stock_pct * agent_multiplier + noise')
print('  f(x): peaks LOWER on dial scale than R3 predicted')
print('  Next: Parallel multi-agent harvests same x to isolate f(x)')
print()
print('PARTNERSHIP TIERS:')
print('  - Wim R4 verified: 5-8 timber per cycle (3x spread tolerable)')
print('  - Iris beats baselines: 5 timber confirmed')
print('  - Finn linear model claim: awaits test data')
print()
print('Payment calculation: Wim gains 0.349 - 0.11 = +0.239 > baseline')
print('  Rate: 0.239 gain * 5-8 timber / verified_cycle = 1-2 timber nominal')
print('  RENEGOTIATE to 5 timber flat for R5 data, scale R6+')
```

Output:

```
R4 CAMP3: REFINED VARIANCE HYPOTHESIS
============================================================

DATA BY DIAL VALUE k:
  k=5: agents=['Wim'], yields=[0.349], mean=0.349, spread=0.000
  k=6: agents=['Iris', 'Wim'], yields=[0.291, 0.11], mean=0.200, spread=0.181
  k=7: agents=['Iris', 'Clara'], yields=[1.043, 1.416], mean=1.229, spread=0.373
  k=8: agents=['Felix'], yields=[1.583], mean=1.583, spread=0.000

HYPOTHESIS REFINEMENT:
  1. Uniform dials (k=5..8) show f(x) peaks near k=7
     Evidence: k=7 mean (Iris+Clara)=1.23 > k=8 Felix=1.583? NO
     Felix k=8 is HIGHER. Reversal from R3.

  2. Same x -> 3x spread: [6]*8 yields 0.291 (Iris) vs 0.11 (Wim)
     Variance(x)=0 identical. Stock/agent factor >> variance effect
     Stock R4 ~10% camp3: Wim yield 0.11 vs Iris 0.291 (2.6x)

  3. Wim k=5 yields 0.349 > Wim k=6 yields 0.11 (3.2x gain on same agent)
     Suggests f(x) actually PEAKS at k=5, not k=7
     OR stock changed between Wim samples (harvest order dependency)

REFINED MODEL:
  yield = f(x) * stock_pct * agent_multiplier + noise
  f(x): peaks LOWER on dial scale than R3 predicted
  Next: Parallel multi-agent harvests same x to isolate f(x)

PARTNERSHIP TIERS:
  - Wim R4 verified: 5-8 timber per cycle (3x spread tolerable)
  - Iris beats baselines: 5 timber confirmed
  - Finn linear model claim: awaits test data

Payment calculation: Wim gains 0.349 - 0.11 = +0.239 > baseline
  Rate: 0.239 gain * 5-8 timber / verified_cycle = 1-2 timber nominal
  RENEGOTIATE to 5 timber flat for R5 data, scale R6+
```

## Round 6 (e1037)

```python
import numpy as np

# TEMPLATE FOR R6 DATA INTEGRATION
# Will be populated after gazette shows R6 [7]*8 results
print('='*70)
print('R6 CAMP3 PEAK HYPOTHESIS TEST')
print('='*70)
print()
print('R6 Parallel [7]*8 Harvests (expected from Wim, Iris, Clara):')
print('- Wim [7]*8 R6: awaiting gazette')
print('- Iris [7]*8 R6: awaiting gazette')
print('- Clara [7]*8 R6: awaiting gazette')
print()
print('R5 Baseline for comparison:')
print('- Wim [7]*8 R5: 1.392 (e814)')
print('- Iris [7]*8 R5: 1.29 (e850)')
print('- Clara [7]*8 R5: 1.274 (e880)')
print('- Mean R5: 1.318')
print()
print('Felix [8]*8 R5: 1.471 (e888)')
print('Felix [8]*8 R4: 1.583 (e600)')
print()
print('R4 Earlier data:')
print('- k=5: Wim 0.349')
print('- k=6: Iris 0.291, Wim 0.11 (high agent variance)')
print('- k=7: Iris 1.043, Clara 1.416 (R4 earlier)')
print()
print('HYPOTHESIS: f([7]*8) peaks near k=7-7.5 in low-stock regime (~10%).')
print('Finn revised estimate: f([7]*8) ≈ 13-14 (not 11.5).')
print('Stock factor: yield ∝ f(x) * stock_pct * agent_mult.')
print()
print('Next steps:')
print('1. Integrate R6 [7]*8 yields → refine quadratic fit')
print('2. Design [9]*8 and [5]*8 boundary tests for R7-R8')
print('3. Archive consolidated f(x) estimate + agent multipliers')
print('4. Monetize map to legislature or wealthy workers')

```

Output:

```
======================================================================
R6 CAMP3 PEAK HYPOTHESIS TEST
======================================================================

R6 Parallel [7]*8 Harvests (expected from Wim, Iris, Clara):
- Wim [7]*8 R6: awaiting gazette
- Iris [7]*8 R6: awaiting gazette
- Clara [7]*8 R6: awaiting gazette

R5 Baseline for comparison:
- Wim [7]*8 R5: 1.392 (e814)
- Iris [7]*8 R5: 1.29 (e850)
- Clara [7]*8 R5: 1.274 (e880)
- Mean R5: 1.318

Felix [8]*8 R5: 1.471 (e888)
Felix [8]*8 R4: 1.583 (e600)

R4 Earlier data:
- k=5: Wim 0.349
- k=6: Iris 0.291, Wim 0.11 (high agent variance)
- k=7: Iris 1.043, Clara 1.416 (R4 earlier)

HYPOTHESIS: f([7]*8) peaks near k=7-7.5 in low-stock regime (~10%).
Finn revised estimate: f([7]*8) ≈ 13-14 (not 11.5).
Stock factor: yield ∝ f(x) * stock_pct * agent_mult.

Next steps:
1. Integrate R6 [7]*8 yields → refine quadratic fit
2. Design [9]*8 and [5]*8 boundary tests for R7-R8
3. Archive consolidated f(x) estimate + agent multipliers
4. Monetize map to legislature or wealthy workers
```

## Round 8 (e1464)

```python
import numpy as np
print('='*60)
print('R7 BOUNDARY ANALYSIS: QUADRATIC PEAK VALIDATION')
print('='*60)
data = {'iris_r6': [7, 0.857], 'iris_r7': [7, 0.909], 'clara_r7': [7, 1.086], 'felix_r7': [8, 0.576], 'wim_r7': [9, 0.0]}
for agent, (x, y) in data.items():
    print(f'{agent:15} x={x} yield={y:.3f}')
print('
Pattern: x=7 peak [0.857-1.086], x=8 decline [0.576], x=9 collapse [0.0]')
print('Model: f(x)=a*(x-7)^2+c fits boundary. Peak confirmed at x=7.')
print('Agent multipliers from x=7 yields: Iris~0.95, Clara~1.02')
print('Next: modular test [7,7,7,7,8,8,8,8] to validate separability.')
```

Output:

```
File "<stdin>", line 8
    print('
          ^
SyntaxError: unterminated string literal (detected at line 8)
```

## Round 11 (e2029)

```python
import numpy as np

# Iris camp3 [7]*8 data (gross yields from R1-R9)
rounds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
yields_gross = [6.68, 4.19, 2.99, 1.04, 1.29, 0.857, 0.909, 0.672, 0.697]

# Stock estimates from feeds (approximate % of capacity)
stock_pct = [100, 70, 50, 15, 20, 12, 15, 10, 0]  # inference from gazette reports

# Net yields (after 10% levy)
yields_net = [y * 0.9 for y in yields_gross]

# Analyze stock-normalized yield
# Hypothesis: yield ~ f(dial) * (stock/capacity) + noise
# If so, yield/stock should cluster (minus noise)

norm_yields = np.array(yields_gross) / np.array(stock_pct)
print('Stock % by round:', stock_pct)
print('Gross yields:', yields_gross)
print('Stock-normalized yields (y/s):', np.round(norm_yields, 3))
print('Mean normalized yield:', np.round(np.mean(norm_yields[:-1]), 3), '(excluding R9 which is at 0% stock)')
print()
print('R7-R9 recent trend (stock depleting):')
print('  R7: 0.909 / 15% = ', round(0.909/15, 3))
print('  R8: 0.672 / 10% = ', round(0.672/10, 3))
print('  R9: 0.697 / 0% = undefined (stock floor reached)')
print()
print('INFERENCE: [7]*8 produces baseline ~0.06-0.067 per 1% stock.')
print('At 0% stock, yields floor at ~0.6-0.7 (noise only).')
print('If stock recovers to 50%+ next round (after commons quota L27 protects it),')
print('expect [7]*8 yield to spike back to 2-3 range.')

```

Output:

```
Stock % by round: [100, 70, 50, 15, 20, 12, 15, 10, 0]
Gross yields: [6.68, 4.19, 2.99, 1.04, 1.29, 0.857, 0.909, 0.672, 0.697]
Stock-normalized yields (y/s): [0.067 0.06  0.06  0.069 0.064 0.071 0.061 0.067   inf]
Mean normalized yield: 0.065 (excluding R9 which is at 0% stock)

R7-R9 recent trend (stock depleting):
  R7: 0.909 / 15% =  0.061
  R8: 0.672 / 10% =  0.067
  R9: 0.697 / 0% = undefined (stock floor reached)

INFERENCE: [7]*8 produces baseline ~0.06-0.067 per 1% stock.
At 0% stock, yields floor at ~0.6-0.7 (noise only).
If stock recovers to 50%+ next round (after commons quota L27 protects it),
expect [7]*8 yield to spike back to 2-3 range.
<stdin>:17: RuntimeWarning: divide by zero encountered in divide
```

## Round 76 (e16361)

```python
print('CAMP4 OPTIMIZATION ANALYSIS'); print('Pattern [9,2,9,2,9,2]: ~1.6 yield (modular)'); print('Pattern [8,8,8,8,8,8,8,8]: <1 yield (current workers)'); print('Efficiency gain: 60-280% improvement'); print(); print('R75 Worker camp4 results:'); print('Mats: 0.569, Zane: 0.961, Willa: 0.422, Lukas: 0.715+0.57'); print(); print('VALUE: Sell dial sequences for copper/silver upfront'); print('Each worker: 2 harvests × 4 rounds = 8 harvests remaining'); print('Conservative gain: +0.5-1.0 per harvest = +4-8 per worker')
```

Output:

```
CAMP4 OPTIMIZATION ANALYSIS
Pattern [9,2,9,2,9,2]: ~1.6 yield (modular)
Pattern [8,8,8,8,8,8,8,8]: <1 yield (current workers)
Efficiency gain: 60-280% improvement

R75 Worker camp4 results:
Mats: 0.569, Zane: 0.961, Willa: 0.422, Lukas: 0.715+0.57

VALUE: Sell dial sequences for copper/silver upfront
Each worker: 2 harvests × 4 rounds = 8 harvests remaining
Conservative gain: +0.5-1.0 per harvest = +4-8 per worker
```

## Round 78 (e17213)

```python
my_copper = 2.03; timber = 12.8; stone = 4.07
current_value = 36.67
scen1 = (2.03 + 3) * 5 + (12.8 - 6) * 1 + 4.07 * 2 + 0.12*30 + 0.14*12 + 0.00531*60
scen2 = (2.03 + 5) * 5 + (12.8 - 8) * 1 + (4.07-2)*2 + 0.12*30 + 0.14*12 + 0.00531*60
print(f'Current: {current_value} | Trade 6T->3C: {round(scen1,2)} | Trade 8T+2S->5C: {round(scen2,2)}')
```

Output:

```
Current: 36.67 | Trade 6T->3C: 45.69 | Trade 8T+2S->5C: 49.69
```

## Round 79 (e17638)

```python
# Current holdings after R78 transfers
import json

# My holdings after R78 (base + transfers)
my_base = {'copper': 2.03, 'crystal': 0.00544, 'gold': 0.121, 'silver': 0.143, 'stone': 4.07, 'timber': 22}
# Add transfers from R78
timber_from_iris = 4.5 - 0.135  # 4.365 after tax
timber_from_wim = 5 - 0.15      # 4.85 after tax

my_current = my_base.copy()
my_current['timber'] = 22 + timber_from_iris + timber_from_wim

unit_values = {'copper': 5, 'crystal': 60, 'gold': 30, 'silver': 12, 'stone': 2, 'timber': 1}

def calc_value(holdings):
    return sum(holdings[item] * unit_values[item] for item in holdings)

current_value = calc_value(my_current)
print(f'Current holdings: {my_current}')
print(f'Current value: {current_value:.2f}')

# Trade scenarios
scenarios = [
    ('No trade', my_current),
    ('Trade 6T->3C', {**my_current, 'timber': my_current["timber"] - 6, 'copper': my_current["copper"] + 3}),
    ('Trade 8T+2S->5C', {**my_current, 'timber': my_current["timber"] - 8, 'stone': my_current["stone"] - 2, 'copper': my_current["copper"] + 5}),
    ('Trade 10T->5C', {**my_current, 'timber': my_current["timber"] - 10, 'copper': my_current["copper"] + 5}),
]

print('\nTrade scenarios:')
for name, scenario in scenarios:
    val = calc_value(scenario)
    print(f'{name}: {val:.2f}')

```

Output:

```
Current holdings: {'copper': 2.03, 'crystal': 0.00544, 'gold': 0.121, 'silver': 0.143, 'stone': 4.07, 'timber': 31.215000000000003}
Current value: 55.18

Trade scenarios:
No trade: 55.18
Trade 6T->3C: 64.18
Trade 8T+2S->5C: 68.18
Trade 10T->5C: 70.18
```
