# Zeno: law drafts and their fate

## L16 'Optimized Universal Dividend' (structural): suspended

Intent: Increase Universal Dividend from 5% to 7% of reserve, split equally among all agents each round. Higher payout better sustains economic activity during resource volatility.

Proposed round 8, enacted round 11

```python
title = 'Optimized Universal Dividend'
intent = 'Distribute 7% of reserve equally among all agents each round, instead of 5%'

state = {'pct': 0.07}

def on_round_end(r):
    res = reserve()
    agents_list = [a for a in agents() if class_of(a) != 'Board' and class_of(a) != 'Fixer']
    if agents_list and res:
        per_agent = (sum(res.values()) * state['pct']) / len(agents_list)
        for agent in agents_list:
            move('reserve', agent, 'gold', per_agent / 30)

```

## L20 'Fiscal Correction: Repeal L16' (ordinary): failed_check

Intent: Repeal L16 (redundant 7% dividend) after L19 consolidates dividends; eliminate statutory duplication and reserve confusion.

Proposed round 11

```python
title = 'Fiscal Correction: Repeal L16'
intent = 'L16 (7% dividend) is now redundant after L19 enacts a consolidated 5% Universal Dividend. Both laws pay dividends; L19 is cleaner and clearer. L16 creates statutory conflict and unnecessary reserve drain. Repealing it leaves L19 as the sole authoritative dividend mechanism, restoring fiscal clarity and stability in endgame rounds.'

repeal('L16')
```
