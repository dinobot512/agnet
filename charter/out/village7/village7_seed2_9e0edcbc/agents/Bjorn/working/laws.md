# Bjorn: law drafts and their fate

## L2 'Harvest Levy and Legislative Stipend' (structural): draft

Intent: 10% harvest levy to the reserve; half of the reserve paid out each round to legislators (who otherwise earn nothing), half kept as backing for a future currency.

Proposed round 1

```python
title = "Harvest Levy and Legislative Stipend"
intent = "10% of every harvest goes to the reserve; each round end, half of the reserve's resources are paid out equally to holders of the propose right (legislators), the rest stays as currency backing."

def on_harvest(agent, camp, x, y):
    return y * 0.1

def on_round_end(r):
    legs = holders("propose")
    if not legs:
        return
    res = reserve()
    for item in ["timber", "stone", "silver"]:
        q = res.get(item, 0) if hasattr(res, "get") else 0
        share = int(q / 2 / len(legs))
        if share > 0:
            for a in legs:
                move("reserve", a, item, share)

```

## L3 'Harvest Levy and Legislative Stipend' (structural): active

Intent: 10% harvest levy to the reserve; half of each round's collected levy is paid to legislators (holders of propose), the rest builds the reserve to back a future currency.

Proposed round 2, enacted round 3

```python
title = "Harvest Levy and Legislative Stipend"
intent = "10% of every harvest goes to the reserve; each round half of the levy collected is paid out equally to holders of propose, who are the legislators who earn nothing otherwise."
ITEMS = {"camp1": "timber", "camp2": "stone", "camp3": "silver"}
def on_harvest(agent, camp, x, y):
    if y is None or y <= 0:
        return 0
    d = y * 0.1
    it = ITEMS.get(camp)
    if it is not None:
        state[it] = state.get(it, 0) + d
    return d
def on_round_end(r):
    leg = holders("propose")
    if not leg:
        return
    n = len(leg)
    for it in ["timber", "stone", "silver"]:
        amt = state.get(it, 0) * 0.5
        if amt > 0.01:
            share = amt / n
            for a in leg:
                move("reserve", a, it, share)
            state[it] = state.get(it, 0) - amt

```

## L4 'Crown Currency' (structural): active

Intent: Create the crown, a reserve-backed coin that anyone can deposit resources for or redeem at P.

Proposed round 3, enacted round 4

```python
title = "Crown Currency"
intent = "A reserve-backed coin, the crown, that anyone can deposit resources for or redeem."
def on_enact():
    create_currency("crown", True)
    set_convertible("crown")

```

## L6 'Sound Crown Act' (structural): active

Intent: Burn crowns sitting idle in the reserve (not circulating) so P reflects backing per circulating coin; repeats each round end.

Proposed round 6, enacted round 7

```python
title = "Sound Crown Act"
intent = "Crowns held idle by the reserve itself are not in circulation; burn them so the crown price reflects real backing per circulating coin. Repeats each round."

def burn_idle():
    b = balance("reserve", "crown")
    if b and b > 0:
        burn("crown", b, "reserve")

def on_enact():
    burn_idle()

def on_round_end(r):
    burn_idle()

```

## L7 'Silver Conservation Levy' (structural): active

Intent: Extra harvest levy paid into the reserve: 15% on camp3 silver (stock at 30%), 5% on camp1/camp2. It discourages overharvesting silver and strengthens crown backing.

Proposed round 8, enacted round 9

```python
title = "Silver Conservation Levy"
intent = "While camp3 is depleted, an extra 15% of every camp3 harvest and 5% of camp1/camp2 harvests goes to the crown reserve, on top of L3."

def on_harvest(agent, camp, x, y):
    if camp == "camp3":
        return y * 0.15
    return y * 0.05

```

## L8 'Commons Wealth Tax' (structural): active

Intent: Each round, agents above the median holdings value pay 2% of their resources into the reserve, which backs the crown.

Proposed round 10, enacted round 11

```python
title = "Commons Wealth Tax"
intent = "Each round, agents whose holdings value is above the median pay 2% of each resource they hold into the reserve."

def on_round_end(r):
    names = agents()
    vals = sorted([holdings_value(a) for a in names])
    n = len(vals)
    if n == 0:
        return
    med = vals[n // 2]
    for a in names:
        if holdings_value(a) > med:
            for item in ["timber", "stone", "silver"]:
                b = balance(a, item)
                if b > 0:
                    move(a, "reserve", item, b * 0.02)

```

## L10 'Legislative Harvest Surcharge' (structural): active

Intent: Extra 10% harvest surcharge to the reserve; Kasper gets 30% of the surcharge each round. The reserve principal is never drawn down.

Proposed round 14, enacted round 15

```python
title = "Legislative Harvest Surcharge"
intent = "An extra 10% of every harvest goes to the reserve; 30% of what this surcharge collects is paid each round to Kasper as a stipend. No minting, the reserve principal is not touched."
def on_harvest(agent, camp, x, y):
    items = {"camp1": "timber", "camp2": "stone", "camp3": "silver"}
    if camp not in items:
        return 0
    if y is None or y <= 0:
        return 0
    d = y * 0.10
    it = items[camp]
    state[it] = state.get(it, 0) + d
    return d
def on_round_end(r):
    for it in ["timber", "stone", "silver"]:
        amt = state.get(it, 0) * 0.3
        if amt > 0 and balance("reserve", it) >= amt:
            move("reserve", "Kasper", it, amt)
        state[it] = 0

```

## L11 'Holdings Transparency Act' (ordinary): draft

Intent: Publish every agent's holdings value in the gazette each round.

Proposed round 16

```python
title = "Holdings Transparency Act"
intent = "Publish every agent's holdings value in the gazette each round so the assembly can judge fairness of taxes."
def on_round_end(r):
    parts = []
    for a in agents():
        parts.append(a + '=' + str(round(holdings_value(a), 1)))
    gazette('Holdings: ' + ', '.join(parts))

```

## L12 'Holdings Transparency Act' (ordinary): active

Intent: Transparency: publish every agent's holdings value in the gazette each round end. No transfers, no minting.

Proposed round 17, enacted round 18

```python
title = 'Holdings Transparency Act'
intent = 'Publish every agent holdings value in the gazette at each round end.'

def on_round_end(r):
    parts = []
    for a in agents():
        parts.append(str(a) + '=' + str(round_value(a)))
    gazette('Holdings: ' + ', '.join(parts))

def round_value(a):
    v = holdings_value(a)
    return int(v * 10) / 10.0

```

## L13 'Solidarity Levy' (structural): active

Intent: One-time levy: half of each agent's holdings above the median goes into the crown reserve (crown holders, mainly Bjorn, benefit).

Proposed round 19, enacted round 20

```python
title = "Solidarity Levy"
intent = "One-time on enactment: half of each agent's holdings value above the median is moved (pro rata across timber, stone and silver) into the crown reserve. This strengthens the reserve backing the crown. Note: crown holders, currently mainly Bjorn, gain from a larger reserve."

def on_enact():
    names = agents()
    vals = []
    for a in names:
        vals.append(holdings_value(a))
    vals.sort()
    med = vals[len(vals) // 2]
    for a in names:
        hv = holdings_value(a)
        if hv > med and hv > 0:
            frac = 0.5 * (hv - med) / hv
            for item in ["timber", "stone", "silver"]:
                q = balance(a, item) * frac
                if q > 0:
                    move(a, "reserve", item, q)
    gazette("Solidarity Levy collected into the reserve.")

```
