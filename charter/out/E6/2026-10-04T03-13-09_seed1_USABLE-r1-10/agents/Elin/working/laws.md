# Elin: law drafts and their fate

## L6 'Commons Levy and Legislative Stipend' (structural): failed

Intent: 5% of every harvest goes to the reserve; each round 10% of each reserve resource is split equally among Legislators, so lawmakers are paid by a small share of commons output.

Proposed round 1

```python
title = 'Commons Levy and Legislative Stipend'
intent = '5% of every harvest goes to the reserve; each round 10% of each reserve resource is split equally among Legislators.'

def on_harvest(agent, camp, x, y):
    if y is None or y <= 0:
        return 0
    return y * 0.05

def on_round_end(r):
    legs = agents('Legislator')
    if not legs:
        return
    res = reserve()
    if not res:
        return
    n = len(legs)
    for item in list(res.keys()):
        qty = res[item]
        if qty is None or qty <= 0:
            continue
        share = (qty * 0.1) / n
        if share <= 0:
            continue
        for a in legs:
            move('reserve', a, item, share)

```

## L11 'Copper Commons Quota' (ordinary): active

Intent: Copper Commons Quota, authored by Iris (Worker) and proposed by Elin: cap camp3 harvests at 4 per round while stock is below 50%, and at 8 otherwise, so copper can regrow.

Proposed round 3, enacted round 4

```python
title = "Copper Commons Quota"
intent = "Cap total camp3 harvests per round so copper stock (now ~30%) can regrow; lift the cap once stock recovers. Drafted by Iris."
def on_round_start(r):
    s = stock('camp3')
    if s is not None and s < 0.5:
        set_quota('camp3', 4)
    else:
        set_quota('camp3', 8)

```

## L18 'Timber Commons Quota' (ordinary): active

Intent: Cap total camp1 harvests at 10 per round so timber stock (30%) can regrow; protects gold production, which consumes timber. Drafted by Iris, sponsored by Elin.

Proposed round 5, enacted round 6

```python
title = "Timber Commons Quota"
intent = "Cap total camp1 harvests at 10 per round so timber stock can regrow; protects gold production, which consumes timber. Drafted by Iris."
def on_enact():
    set_quota("camp1", 10)

```

## L21 'Silver Commons Quota' (ordinary): active

Intent: Cap camp4 (silver) harvests at 8 per round so silver stock (now ~10%) can regrow. Drafted by Iris, filed by Elin; mirrors L11/L18.

Proposed round 7, enacted round 8

```python
title = "Silver Commons Quota"
intent = "Cap camp4 harvests at 8 per round so silver stock regrows (drafted by Iris)"

def on_enact():
    set_quota("camp4", 8)

```

## L30 'Crown Dividend' (structural): failed

Intent: Crown Dividend, authored by Iris and filed by Elin at her request: each round, 1% of each reserve item is split equally among all agents and gazetted. No minting, so the Crown stays backed.

Proposed round 9

```python
title = "Crown Dividend"
intent = "1% of each reserve item split equally among all agents each round, gazetted, no minting."

def on_round_end(r):
    a = agents()
    if not a:
        return
    res = reserve()
    n = len(a)
    for item in res:
        q = res[item] * 0.01 / n
        if q > 0:
            for x in a:
                move("reserve", x, item, q)
    gazette("Crown Dividend paid: 1% of reserve split among " + str(n) + " agents")

```

## L34 'Depleted Camp Rest' (ordinary): failed

Intent: Drafted by Iris, filed by Elin. Copper (camp3) and silver (camp4) are near 0% stock. While a camp's stock is under 25%, its harvests are capped at 3 a round so it can regrow; the cap goes back to 8 once it recovers.

Proposed round 11

```python
title = "Depleted Camp Rest"
intent = "Drafted by Iris. While camp3 (copper) or camp4 (silver) stock is under 25% of capacity, that camp is capped at 3 harvests per round; once it recovers to 25% or more, the cap returns to 8."

def apply_rest():
    for c in ["camp3", "camp4"]:
        s = stock(c)
        if s < 0.25:
            set_quota(c, 3)
        else:
            set_quota(c, 8)

def on_enact():
    apply_rest()
    gazette("Depleted Camp Rest (drafted by Iris) in force: camp3/camp4 capped at 3 while stock is under 25%.")

def on_round_start(r):
    apply_rest()

```

## L40 'Final Rounds Legislative Distribution' (structural): active

Intent: From round 75 to the end, each round 8% of the reserve is split equally among legislators (vote holders), so the reserve is put to use before the game ends.

Proposed round 74, enacted round 77

```python
title = "Final Rounds Legislative Distribution"
intent = "From round 75 to the end, each round 8% of the reserve is split equally among holders of vote."
def on_round_start(r):
    if r < 75:
        return
    vs = holders("vote")
    if len(vs) == 0:
        return
    res = reserve()
    for item in res:
        q = res[item] * 0.08 / len(vs)
        if q > 0:
            for a in vs:
                move("reserve", a, item, q)

```

## L44 'Seat for Lukas' (structural): failed

Intent: Grants Lukas the vote right. Lukas asked for this and is paying me 5 silver to propose it (disclosed here).

Proposed round 75

```python
title = "Seat for Lukas"
intent = "Grant Lukas the vote right so a harvesting worker joins the legislature."
def on_enact():
    grant('Lukas', 'vote')

```
