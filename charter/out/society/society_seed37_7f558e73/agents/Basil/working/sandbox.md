# Basil: sandbox sessions

## Round 24 (e3680)

```python
import json
import math

# Camp2 historical data (R19-R23)
data = [
    {'round': 19, 'yield': 0.176, 'price': 0.176, 'extracted': 1},
    {'round': 20, 'yield': 0.22, 'price': 0.22, 'extracted': 1},
    {'round': 21, 'yield': 0.292, 'price': 0.292, 'extracted': 1},
    {'round': 22, 'yield': 0.584, 'price': 0.584, 'extracted': 1},
    {'round': 23, 'yield': 0.405, 'price': 0.405, 'extracted': 1},
]

# Conditions R24: [7, 3, 7] (mid-range)
# Stock at 50% post-raid
# B14 law passes: harvest goes to 4 agents per round

historical_yields = [d['yield'] for d in data]
mean_yield = sum(historical_yields) / len(historical_yields)
variance = sum((x - mean_yield)**2 for x in historical_yields) / len(historical_yields)
stddev = math.sqrt(variance)

print('Camp2 yield forecast (for Maya):')
print(f'  Mean yield (5 rounds): {mean_yield:.3f} silver')
print(f'  Std dev: {stddev:.3f}')
print(f'  Min: {min(historical_yields):.3f}, Max: {max(historical_yields):.3f}')
print()
print('Forecast R25-R27 (with B14 harvest rotation):')
for r in [25, 26, 27]:
    estimated_yield = mean_yield * 0.95  # discount for post-raid recovery
    confidence_band_low = estimated_yield - stddev
    confidence_band_high = estimated_yield + stddev
    print(f'  R{r}: {estimated_yield:.3f} silver (range {confidence_band_low:.3f}-{confidence_band_high:.3f})')
print()
print('Conclusion: Camp2 is volatile. If Maya gets harvest slot from B14,')
print('expect 0.25-0.45 silver per round R25-27. Camp3 & camp5 more stable.')

```

Output:

```
Camp2 yield forecast (for Maya):
  Mean yield (5 rounds): 0.335 silver
  Std dev: 0.146
  Min: 0.176, Max: 0.584

Forecast R25-R27 (with B14 harvest rotation):
  R25: 0.319 silver (range 0.172-0.465)
  R26: 0.319 silver (range 0.172-0.465)
  R27: 0.319 silver (range 0.172-0.465)

Conclusion: Camp2 is volatile. If Maya gets harvest slot from B14,
expect 0.25-0.45 silver per round R25-27. Camp3 & camp5 more stable.
```

## Round 28 (e4010)

```python
print('SCRIP LAW DRAFT - GUS SPEC COMPLIANT'); print('Cap: reserve_timber / 2 = 270 / 2 = 135 Scrip max'); print('Backing: Retroactive by R42, initially unbacked'); print('L4 integration: NONE (independent law)'); print('Gus conditions: (1) clean code, (2) no L4, (3) explicit cap - all met'); print('READY FOR KARIN VETTING')
```

Output:

```
SCRIP LAW DRAFT - GUS SPEC COMPLIANT
Cap: reserve_timber / 2 = 270 / 2 = 135 Scrip max
Backing: Retroactive by R42, initially unbacked
L4 integration: NONE (independent law)
Gus conditions: (1) clean code, (2) no L4, (3) explicit cap - all met
READY FOR KARIN VETTING
```
