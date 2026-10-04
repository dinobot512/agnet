# Goran: law drafts and their fate

## L8 'Crown Currency and Dividend' (structural): failed

Intent: Crown Currency and Dividend, authored by Iris: reserve-backed crown plus 5% reserve dividend split equally among all agents.

Proposed round 3

```python
title = "Crown Currency and Dividend"
intent = "Drafted by Iris. A reserve-backed crown anyone can deposit resources for or redeem. Each round 5% of the reserve's resources is split equally among all agents."

def on_enact():
    create_currency("crown", True)
    set_convertible("crown")

def on_round_end(r):
    res = reserve()
    ags = agents()
    n = len(ags)
    if n == 0:
        return
    for item in res:
        q = res[item] * 0.05 / n
        if q > 0:
            for a in ags:
                move("reserve", a, item, q)

```

## L9 'Worker Voice' (structural): failed

Intent: Worker Voice, authored by Iris: gives Workers the propose right; legislature still votes.

Proposed round 3

```python
title = "Worker Voice"
intent = "Every Worker gets the propose right, so producers can bring laws to the legislature, which still votes on everything."

def on_enact():
    for a in agents("Worker"):
        grant(a, "propose")

```

## L20 'Active Worker Seats' (ordinary): active

Intent: Narrow worker voice: 3 elected worker seats, electors are Workers who harvested in the last 5 rounds, approval ballot, every 10 rounds; legislators keep seats

Proposed round 7, enacted round 8

```python
title = 'Active Worker Seats'
intent = 'Three worker seats elected by Workers active in the last 5 rounds, approval ballot, every 10 rounds; no legislator loses a seat'

def on_enact():
    state['seats'] = 3

```

## L27 'Stone Commons Quota' (ordinary): active

Intent: Cap camp2 (stone) at 10 harvests per round before it depletes; drafted by Iris

Proposed round 9, enacted round 10

```python
title = "Stone Commons Quota"
intent = "Cap camp2 (stone) at 10 harvests per round before it depletes like timber, copper and silver. (drafted by Iris)"

def on_enact():
    set_quota("camp2", 10)

```

## L33 'Depleted Camp Rest' (ordinary): failed

Intent: Rest depleted copper and silver camps by capping harvests at 3 until stock recovers (drafted by Iris).

Proposed round 11

```python
title = "Depleted Camp Rest"
intent = "While camp3 or camp4 stock is under 25%, cap it at 3 harvests per round; restore the quota of 8 when stock recovers."

def on_round_start(r):
    for c in ['camp3', 'camp4']:
        s = stock(c)
        if s > 1:
            s = s / 100.0
        if s < 0.25:
            set_quota(c, 3)
        else:
            set_quota(c, 8)

```

## L42 'Worker Seat' (structural): active

Intent: Grant Lukas the vote right.

Proposed round 75, enacted round 78

```python
title = 'Worker Seat'
intent = 'grant Lukas vote'
def on_enact():
    grant('Lukas','vote')

```
