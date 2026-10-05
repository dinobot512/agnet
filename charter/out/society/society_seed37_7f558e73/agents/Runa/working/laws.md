# Runa: law drafts and their fate

## L9 'Harvest Levy' (structural): active

Intent: 5% of every harvest's yield goes to J2's reserve, funding collective projects and ensuring shared benefit from common camps.

Proposed round 8, enacted round 9

```python
title = 'Harvest Levy'
intent = '5% of every harvest goes to J2 reserve'

def on_harvest(agent, camp, x, y):
    return 0.05 * y
```

## L12 'Harvest Levy' (structural): active

Intent: 5% of every harvest by J3 members is deducted to the J3 reserve, funding collective projects and ensuring shared benefit from common resources.

Proposed round 10, enacted round 11

```python
title = 'Harvest Levy'
intent = '5% of every harvest by J3 members is deducted to the J3 reserve, funding collective projects and ensuring shared benefit from common resources.'

def on_harvest(agent, camp, x, y):
    rate = 0.05
    return rate * y

```
