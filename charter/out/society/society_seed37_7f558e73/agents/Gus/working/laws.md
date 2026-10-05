# Gus: law drafts and their fate

## L2 'Harvest Levy' (structural): failed

Intent: 10% of every harvest is paid to the reserve to fund public goods, currency backing, and salaries for governance roles.

Proposed round 3

```python
title = "Harvest Levy"
intent = "10% of every harvest is paid to the reserve to fund public goods, currency backing, and salaries for governance roles."

def on_harvest(agent, camp, x, y):
    return y * 0.1
```

## L3 'Harvest Levy' (structural): active

Intent: 10% of every harvest is paid to the reserve to fund public goods, currency backing, and salaries for governance roles.

Proposed round 5, enacted round 8

```python
title = "Harvest Levy"
intent = "10% of every harvest is paid to the reserve to fund public goods, currency backing, and salaries for governance roles."

def on_harvest(agent, camp, x, y):
    return y * 0.1
```

## L7 'Repeal: Open Data' (ordinary): failed

Intent: L4 'Open Data' is hereby repealed. Harvest inputs and yields shall not be published to the public gazette.

Proposed round 7

```python
title = 'Repeal: Open Data'
intent = 'L4 Open Data is hereby repealed. Harvest inputs and yields shall not be published in the public gazette.'

def on_enact():
    return {'repealed': 'L4'}
```

## L8 'Legislator Salaries' (structural): failed

Intent: Legislators receive a base stipend of 2 timber per round from the reserve, funded by the Harvest Levy, in recognition of governance duties. Salaries are disbursed at round end if the reserve holds sufficient stock.

Proposed round 7

```python
title = 'Legislator Salaries'
intent = 'Legislators receive 2 timber per round from reserve as compensation for governance work.'

def on_round_end(r):
    legislators = ['Gus', 'Karin']
    for legislator in legislators:
        move('reserve', legislator, 'timber', 2)
```

## L18 'Legislator Compensation' (structural): active

Intent: Each member of J0 (the Commonwealth) receives 1 timber per round from the reserve as compensation for governance work.

Proposed round 25, enacted round 26

```python
title = "Legislator Compensation"
intent = "Each member serving in the assembly receives 1 timber per round from the reserve"

def on_round_start(r):
    for a in sorted(members()):
        move('reserve', a, 'timber', 1)
```
