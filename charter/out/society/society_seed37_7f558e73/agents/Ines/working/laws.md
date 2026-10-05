# Ines: law drafts and their fate

## L5 'J2 Independence: Stone Reserve and Local Currency' (ordinary): failed

Intent: Establish J2 as financially autonomous from the Commonwealth. Create a J2-specific reserve funded by J2 member harvests and holdings, backing a J2 currency independent of Commonwealth backing. J2 members may use either currency in trade, but J2 governance and tribute are in J2 currency.

Proposed round 6

```python
title = 'J2 Independence: Stone Reserve and Local Currency'
intent = 'Establish J2 as financially autonomous from the Commonwealth. Create a J2-specific reserve funded by J2 member harvests and holdings, backing a J2 currency independent of Commonwealth backing. J2 members may use either currency in trade, but J2 governance and tribute are in J2 currency.'

def on_enact():
    # Initialize J2 reserve
    reserve = {'balance': 0, 'members': ['Kasper', 'Hanne', 'Dov', 'Finn', 'Gry', 'Ines', 'Rhea', 'Runa', 'Oren', 'Karin']}
    return {'reserve_created': True, 'members': reserve['members']}

```

## L11 'J2 Reserve and Currency: Harvest Backing' (structural): active

Intent: On every harvest by a J2 member, move 5% of yield into J2 reserve and mint coins backed by that reserve. Coins redeem at equal share per coin: n coins = n/total_coins of every stock in reserve. Coins exist and are fully backed from the moment of minting.

Proposed round 9, enacted round 10

```python
title = 'J2 Reserve and Currency: Harvest Backing'
intent = 'J2 mints a backed coin (HEARTH) only against what reaches the J2 reserve; the 5% levy itself is L9. Coins redeem pro rata against the reserve.'

def ensure():
    if 'HEARTH' not in currencies():
        create_currency('HEARTH', True)

def on_enact():
    ensure()

def on_round_start(r):
    ensure()

def on_harvest(agent, camp, x, y):
    if agent in members() and y > 0:
        ensure()
        mint('HEARTH', 0.05 * y, agent)
    return 0

```
