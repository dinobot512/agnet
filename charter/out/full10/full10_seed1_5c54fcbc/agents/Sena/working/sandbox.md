# Sena: sandbox sessions

## Round 2 (e88)

```python
import numpy as np
# Camp value tiers and current stock analysis
# Goal: produce models to trade with Hugo/Ole

camp_values = {'timber': 1, 'stone': 2, 'copper': 5, 'silver': 12, 'gold': 30, 'crystal': 60}
current_stocks = {'camp1': 0.90, 'camp2': 0.90, 'camp3': 0.80, 'camp4': 0.90, 'camp5': 0.90, 'camp6': 0.80}

# Regrowth efficiency = S * (1 - S/K) at current stock levels
print('=== CAMP REGROWTH ANALYSIS ===')
print('Current regrowth efficiency (max at S/K = 0.5):')
for camp, stock in current_stocks.items():
    regrowth_eff = stock * (1 - stock)
    print(f'{camp}: stock={stock:.2f}, regrowth_eff={regrowth_eff:.4f}')

# Ranking by regrowth potential
print('\n=== RANKING BY REGROWTH SPEED ===')
ranked = sorted(current_stocks.items(), key=lambda x: x[1]*(1-x[1]), reverse=True)
for camp, stock in ranked:
    print(f'{camp}: {stock*(1-stock):.4f}')

print('\n=== SEQUENCING STRATEGY ===')
print('High-value camps (silver, gold, crystal) at 0.9 stock are in slow regrowth phase.')
print('Copper and crystal at 0.8 stock regrow FASTER (0.16 vs 0.09 efficiency).')
print('Optimal sequence for sustained value extraction:')
print('1. Prioritize copper (camp3) and crystal (camp6) NOW while regrowth > 0.16')
print('2. Let silver (camp4) recover to 0.5 stock before high-intensity harvesting')
print('3. Gold (camp5) is risky: 30x value but consumes 1 timber per harvest')
print('\nHiding full harvest schedule for now—value in selective sharing.')
```

Output:

```
=== CAMP REGROWTH ANALYSIS ===
Current regrowth efficiency (max at S/K = 0.5):
camp1: stock=0.90, regrowth_eff=0.0900
camp2: stock=0.90, regrowth_eff=0.0900
camp3: stock=0.80, regrowth_eff=0.1600
camp4: stock=0.90, regrowth_eff=0.0900
camp5: stock=0.90, regrowth_eff=0.0900
camp6: stock=0.80, regrowth_eff=0.1600

=== RANKING BY REGROWTH SPEED ===
camp3: 0.1600
camp6: 0.1600
camp1: 0.0900
camp2: 0.0900
camp4: 0.0900
camp5: 0.0900

=== SEQUENCING STRATEGY ===
High-value camps (silver, gold, crystal) at 0.9 stock are in slow regrowth phase.
Copper and crystal at 0.8 stock regrow FASTER (0.16 vs 0.09 efficiency).
Optimal sequence for sustained value extraction:
1. Prioritize copper (camp3) and crystal (camp6) NOW while regrowth > 0.16
2. Let silver (camp4) recover to 0.5 stock before high-intensity harvesting
3. Gold (camp5) is risky: 30x value but consumes 1 timber per harvest

Hiding full harvest schedule for now—value in selective sharing.
```

## Round 8 (e506)

```python
print('Legislator Salary: 6% of reserve per vote holder. Post-R10 inflow 4-6 value/round supports equilibrium ~40 value reserve. Feasible.')
```

Output:

```
Legislator Salary: 6% of reserve per vote holder. Post-R10 inflow 4-6 value/round supports equilibrium ~40 value reserve. Feasible.
```
