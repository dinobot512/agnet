# Erik: law drafts and their fate

## L7 'Harvest Levy' (structural): active

Intent: 10% of every harvest goes to the reserve.

Proposed round 2, enacted round 5

```python
title = 'Harvest Levy'
intent = '10% of every harvest goes to the reserve.'

def on_harvest(agent, camp, x, y):
    return y * 0.1

```

## L8 'Universal Dividend' (structural): active

Intent: 5% of the reserve is split equally among all agents each round.

Proposed round 2, enacted round 5

```python
title = 'Universal Dividend'
intent = '5% of the reserve is split equally among all agents each round.'

def on_round_end(r):
    ags = agents()
    if len(ags) == 0:
        return
    for item in ['timber','stone','copper','silver','gold','crystal']:
        amt = balance('reserve', item)
        share = int(amt * 0.05 / len(ags))
        if share > 0:
            for a in ags:
                move('reserve', a, item, share)

```
