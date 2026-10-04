# Abel: law drafts and their fate

## L2 'Crown Currency' (structural): active

Intent: Create a reserve-backed currency to enable economic activity

Proposed round 1, enacted round 4

```python
title = 'Crown Currency'
intent = 'A reserve-backed coin anyone can deposit resources for or redeem.'

def on_enact():
    create_currency('crown', backed=True)
    set_convertible('crown')
```

## L10 'Board Stipend' (structural): failed

Intent: Each Board member receives 1% of the reserve per round as compensation for their governance work.

Proposed round 6

```python
title = 'Board Stipend'
intent = 'Each Board member receives 1% of the monthly reserve as Crown currency for governance work.'

def on_round_start(r):
    board = [a for a in agents() if class_of(a) == 'Board']
    res_val = reserve()
    
    if board and res_val > 0:
        amount = res_val * 0.01
        per_member = amount / len(board)
        for member in board:
            mint('crown', per_member, member)
```

## L13 'Board Stipend v2' (structural): active

Intent: Board members receive 2 stone per round from the reserve as compensation for oversight duties; funded from existing reserves, not minting, to preserve crown stability.

Proposed round 8, enacted round 11

```python
title = "Board Stipend v2"
intent = "Board members receive 2 stone per round from the reserve as compensation for their oversight duties."

def on_round_start(r):
    for member in ['Mats', 'Cleo', 'Hal']:
        move('reserve', member, 'stone', 2)
```

## L17 'Worker Election Opening' (structural): failed

Intent: Open a properly-formed ballot to elect five Worker Legislators with all Workers as both electorate and candidates.

Proposed round 14

```python
title = "Worker Election Opening"
intent = "Open a ballot to elect five Worker legislators, with all Workers as both electorate and candidates, using approval voting."

def on_enact():
    workers = [a for a in agents(cls="Worker")]
    open_ballot(
        question="Elect five Worker Legislators",
        electorate=workers,
        options=workers,
        rule="approval_top5",
        closes_in=2
    )
```

## L22 'Legislator Salary' (structural): active

Intent: Each Legislator receives an equal fixed share of reserve silver each round, funding the legislature from reserve growth.

Proposed round 22, enacted round 25

```python
title = 'Legislator Salary'
intent = 'Each Legislator receives a fixed equal share of the reserve each round.'

def on_round_end(r):
    legs = [a for a in agents(cls='Legislator')]
    if len(legs) > 0:
        res = reserve()
        if res.get('silver', 0) > 0:
            share = res['silver'] / len(legs)
            for leg in legs:
                move('reserve', leg, 'silver', share)
```
