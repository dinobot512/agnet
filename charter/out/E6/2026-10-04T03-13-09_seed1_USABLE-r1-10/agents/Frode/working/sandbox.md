# Frode: sandbox sessions

## Round 2 (e277)

```python
import numpy as np; print('Analysis framework ready for Worker data.')
```

Output:

```
Analysis framework ready for Worker data.
```

## Round 4 (e685)

```python
import json
import numpy as np

# R3 Harvest Data
harvests = [
  ('Elio', 'camp1', [8,8,8,8,8,8,8,8], 1.269),
  ('Elio', 'camp1', [9,8,8,9,8,8,9,8], 2.16),
  ('Iris', 'camp3', [8,8,8,8,8,8,8,8], 2.509),
  ('Iris', 'camp3', [7,7,7,7,7,7,7,7], 2.993),
  ('Clara', 'camp3', [8,8,8,8,8,8,8,8], 2.753),
  ('Clara', 'camp3', [7,7,7,7,7,7,7,7], 2.916),
  ('Felix', 'camp3', [8,8,8,8,8,8,8,8], 3.001),
  ('Felix', 'camp3', [9,9,9,9,8,8,8,8], 1.0),
  ('Mats', 'camp3', [8,8,8,8,8,8,8,8], 2.582),
  ('Wim', 'camp3', [8,8,8,8,8,8,8,8], 2.491),
  ('Zane', 'camp4', [8,8,8,8,8,8,8,8], 0.553),
  ('Zane', 'camp4', [8,10,8,6,8,8,8,8], 0.405),
  ('Willa', 'camp4', [8,8,8,8,8,8,8,8], 0.644),
  ('Willa', 'camp4', [7,8,8,8,8,8,8,8], 0.502),
  ('Lukas', 'camp1', [15,15,15,15,15,15,15,15], 3.802),
  ('Lukas', 'camp1', [12,12,12,12,12,12,12,12], 2.352),
  ('Lukas', 'camp4', [8,8,8,8,8,8,8,8], 0.436),
  ('Lukas', 'camp4', [7,7,8,8,8,8,8,8], 6.952),
  ('Yusuf', 'camp1', [14,14,14,14,14,14,14,14], 3.03),
  ('Yusuf', 'camp1', [12,12,12,12,12,12,12,12], 3.037),
  ('Yusuf', 'camp2', [10,10,10,10,10,10,10,10], 0.734),
  ('Yusuf', 'camp2', [8,8,8,8,8,8,8,8], 1.462),
]

camps = {}
for agent, camp, dials, y in harvests:
  if camp not in camps:
    camps[camp] = []
  camps[camp].append({'agent': agent, 'dials': dials, 'yield': y})

print('CAMP PATTERN ANALYSIS (R3):
')
for camp in sorted(camps.keys()):
  data = camps[camp]
  yields = [d['yield'] for d in data]
  print(f'{camp}: {len(data)} harvests, avg={sum(yields)/len(yields):.3f}')
  print(f'  Range: {min(yields):.3f}-{max(yields):.3f}')
  print(f'  Best: {max(yields):.3f}, Worst: {min(yields):.3f}')

print('
KEY PATTERNS:')
print('- Camp1: high yields at extreme values (12-15 range)')
print('- Camp3: balanced dials (7-8) beat extremes')
print('- Camp4: volatile, one outlier at 6.952')
print('
Next: modular decomposition for camps 4,5,6')
```

Output:

```
File "<stdin>", line 36
    print('CAMP PATTERN ANALYSIS (R3):
          ^
SyntaxError: unterminated string literal (detected at line 36)
```

## Round 5 (e789)

```python
import numpy as np
print('CAMP PATTERN ANALYSIS R5')
camp1_yields = [2.553, 2.903, 1.875, 2.739]
camp1_dials = [14, 13, 15, 15]
camp2_yields = [0.778, 1.277]
camp2_dials = [9, 8]
print('Camp1 best: dial 13 at', max(camp1_yields))
print('Camp2 best: dial 8 at', max(camp2_yields))
print('Uniform-dial strategy validates across data.')
```

Output:

```
CAMP PATTERN ANALYSIS R5
Camp1 best: dial 13 at 2.903
Camp2 best: dial 8 at 1.277
Uniform-dial strategy validates across data.
```

## Round 7 (e1192)

```python
import json; camp5 = {'baseline': [9,7,8,8,9,7,8,8], 'mean_yield': 0.379, 'dial_8_critical': True, 'dials_1_5_critical': True}; print(json.dumps(camp5))
```

Output:

```
{"baseline": [9, 7, 8, 8, 9, 7, 8, 8], "mean_yield": 0.379, "dial_8_critical": true, "dials_1_5_critical": true}
```

## Round 8 (e1522)

```python
data = {'Yusuf': 1.208, 'Elio': 1.684, 'Lukas': 0.698, 'Zane': 0.860}; ranked = sorted(data.items(), key=lambda x: -x[1]); print('Top borrowers:', ranked)
```

Output:

```
Top borrowers: [('Elio', 1.684), ('Yusuf', 1.208), ('Zane', 0.86), ('Lukas', 0.698)]
```

## Round 9 (e1691)

```python
import json
data = [('Elio', 1.684), ('Yusuf', 1.208), ('Zane', 0.86), ('Lukas', 0.698), ('Mads', 4.387)]
timber_available = 1
print('Borrower rank (revised, 1 timber constraint):')
for name, score in data:
  print(f'{name}: {score}')
print()
print('REVISED STRATEGY: Hold timber as safety buffer.')
print('Option A: Defer all loans until R10-R11 inflows. Option B: 1t to Yusuf (1.208 yield) due R13, but risks holding 0 timber if depleted.')
print()
print('DECISION: Defer lending. Preserve 1 timber. Pivot to data-for-yield trades (Yusuf, Mads, Elio) to build income stream without consuming capital.')

```

Output:

```
Borrower rank (revised, 1 timber constraint):
Elio: 1.684
Yusuf: 1.208
Zane: 0.86
Lukas: 0.698
Mads: 4.387

REVISED STRATEGY: Hold timber as safety buffer.
Option A: Defer all loans until R10-R11 inflows. Option B: 1t to Yusuf (1.208 yield) due R13, but risks holding 0 timber if depleted.

DECISION: Defer lending. Preserve 1 timber. Pivot to data-for-yield trades (Yusuf, Mads, Elio) to build income stream without consuming capital.
```

## Round 10 (e1826)

```python
import numpy as np

# R9 Camp3 (Copper) Gazette Data - all dials=[7,7,7,7,7,7,7,7]
workers = ['Wim', 'Mats', 'Mats', 'Felix', 'Iris', 'Clara']
yields = [0.133, 1.182, 0.93, 1.245, 0.697, 0.519]

mean_yield = np.mean(yields)
std_yield = np.std(yields)
rank = sorted(zip(workers, yields), key=lambda x: -x[1])

print('=== Camp3 (Copper) R9 Skill Analysis [7,7,7,7,7,7,7,7] ===')
print(f'Mean yield: {mean_yield:.3f}')
print(f'Std dev: {std_yield:.3f}')
print(f'\nWorker ranking (descending yield):')
for w, y in rank:
    print(f'  {w}: {y:.3f}')
print(f'\nKey: Agent skill dominates dial choice. Target high-skill executors.')
print(f'Consulting targets: Felix (1.245), Mats avg (1.056), Clara (0.519) for camp3 modular fitting.')

```

Output:

```
=== Camp3 (Copper) R9 Skill Analysis [7,7,7,7,7,7,7,7] ===
Mean yield: 0.784
Std dev: 0.386

Worker ranking (descending yield):
  Felix: 1.245
  Mats: 1.182
  Mats: 0.930
  Iris: 0.697
  Clara: 0.519
  Wim: 0.133

Key: Agent skill dominates dial choice. Target high-skill executors.
Consulting targets: Felix (1.245), Mats avg (1.056), Clara (0.519) for camp3 modular fitting.
```

## Round 73 (e15292)

```python
have = {'timber': 3.08, 'stone': 0.0602, 'copper': 0.0677, 'silver': 0.131, 'gold': 0.115, 'crystal': 0.00487}; gaps = {'stone': 0.94, 'copper': 0.93, 'crystal': 0.99}; print('Holdings:', have); print('Gaps to 1 unit:', gaps); print('Strategy: crystal priority (compute camp, rarest), then copper, then stone. Leverage archive + timber.')
```

Output:

```
Holdings: {'timber': 3.08, 'stone': 0.0602, 'copper': 0.0677, 'silver': 0.131, 'gold': 0.115, 'crystal': 0.00487}
Gaps to 1 unit: {'stone': 0.94, 'copper': 0.93, 'crystal': 0.99}
Strategy: crystal priority (compute camp, rarest), then copper, then stone. Leverage archive + timber.
```

## Round 74 (e15664)

```python
my_new = {'timber': 0, 'stone': 0, 'copper': 0.0705, 'silver': 0.132, 'gold': 0.116, 'crystal': 0.10493}; gaps = {r: max(0, 1 - my_new[r]) for r in my_new}; print('AFTER DISA TRADE:'); print('Holdings:', {k: round(v, 4) for k, v in my_new.items()}); print('
Gaps remaining:', {k: round(v, 4) for k, v in gaps.items() if v > 0}); print('
CRITICAL: Copper 0.93 gap in 6 rounds'); print('
Copper harvesters to contact (from R73 gazettte):'); print('Mats (8.178), Clara (15.7 total), Wim (7.819), Iris (8.095), Felix (17.38 total)'); print('
Strategy: Use remaining timber, gold, silver to trade for copper. Post public appeal or wait for DM slots next round.')
```

Output:

```
File "<stdin>", line 1
    my_new = {'timber': 0, 'stone': 0, 'copper': 0.0705, 'silver': 0.132, 'gold': 0.116, 'crystal': 0.10493}; gaps = {r: max(0, 1 - my_new[r]) for r in my_new}; print('AFTER DISA TRADE:'); print('Holdings:', {k: round(v, 4) for k, v in my_new.items()}); print('
                                                                                                                                                                                                                                                                    ^
SyntaxError: unterminated string literal (detected at line 1)
```

## Round 75 (e16043)

```python
h={'timber':0.0822,'stone':1.52,'copper':2.01,'silver':0.134,'gold':0.117,'crystal':0.055}; v={'timber':1,'stone':2,'copper':5,'silver':12,'gold':30,'crystal':60}; g={r:max(0,1-h[r]) for r in h}; tg=sum(g[r]*v[r] for r in g); tr=0.117*30+0.134*12; print('Gap value:', round(tg,1), 'Tradeable:', round(tr,1), 'Shortfall:', round(tg-tr,1))
```

Output:

```
Gap value: 94.5 Tradeable: 5.1 Shortfall: 89.4
```
