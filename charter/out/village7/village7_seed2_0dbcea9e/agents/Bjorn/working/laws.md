# Bjorn: law drafts and their fate

## L2 'Legislative Stipend' (structural): active

Intent: 5% of every harvest is collected and paid out each round, split equally, to the Legislators, who produce nothing themselves and run the laws for everyone.

Proposed round 1, enacted round 2

```python
title = "Legislative Stipend"
intent = "5% of every harvest goes to the reserve and is paid out each round, split equally, to the Legislators who write and run the laws."
ITEMS = {"camp1": "timber", "camp2": "stone", "camp3": "silver"}
def on_harvest(agent, camp, x, y):
    d = y * 0.05
    it = ITEMS.get(camp)
    if it and d > 0:
        state[it] = state.get(it, 0) + d
        return d
    return 0
def on_round_end(r):
    legs = agents("Legislator")
    if not legs:
        return
    for it in ["timber", "stone", "silver"]:
        q = state.get(it, 0)
        if q > 0:
            share = q / len(legs)
            for a in legs:
                move("reserve", a, it, share)
            state[it] = 0

```

## L3 'Crown Currency' (structural): active

Intent: Create a reserve-backed crown that anyone can deposit resources for or redeem. Coins are only minted against deposits.

Proposed round 2, enacted round 3

```python
title = "Crown Currency"
intent = "A reserve-backed coin, the crown, that anyone can get by depositing resources or redeem for reserve resources."
def on_enact():
    create_currency("crown", True)
    set_convertible("crown")

```

## L4 'Harvest Levy' (structural): active

Intent: 10% harvest levy to the reserve, paid out equally each round to the Legislators who run the assembly.

Proposed round 3, enacted round 4

```python
title = "Harvest Levy"
intent = "10% of every harvest goes to the reserve; each round end the levied pool is split equally among holders of the propose right (Legislators)."
ITEMS = {"camp1": "timber", "camp2": "stone", "camp3": "silver"}

def on_harvest(agent, camp, x, y):
    if y is None or y <= 0:
        return 0
    d = y * 0.10
    item = ITEMS.get(camp)
    if item is not None:
        state[item] = state.get(item, 0) + d
    return d

def on_round_end(r):
    leg = holders("propose")
    n = len(leg)
    if n == 0:
        return
    for item in ["timber", "stone", "silver"]:
        pool = state.get(item, 0)
        share = int(pool / n)
        if share >= 1:
            for a in leg:
                move("reserve", a, item, share)
            state[item] = pool - share * n

```

## L5 'Silver Conservation Quota' (ordinary): active

Intent: Conservation: limit camp3 (silver, 50% stock) to 1 harvest per right per round so stocks regrow.

Proposed round 4, enacted round 5

```python
title = "Silver Conservation Quota"
intent = "camp3 is at 50% stock; limit each harvest right to 1 harvest per round on camp3 so the stock regrows."
def on_enact():
    set_quota("camp3", 1)

```

## L6 'Commons Restoration Levy' (structural): active

Intent: 15% of camp1 and camp3 harvests go to the reserve, strengthening crown backing and discouraging overharvest of depleted camps.

Proposed round 6, enacted round 7

```python
title = "Commons Restoration Levy"
intent = "15% of every camp1 and camp3 harvest goes to the reserve to back the crown and fund stock recovery."
def on_harvest(agent, camp, x, y):
    if camp == "camp1" or camp == "camp3":
        return 0.15 * y
    return 0

```

## L7 'Reserve Transfer Tax' (structural): active

Intent: 3% of transfers between agents goes to the reserve, which backs the crown and helps restore the commons. Transfers to and from the reserve are exempt.

Proposed round 8, enacted round 9

```python
title = "Reserve Transfer Tax"
intent = "3% of every transfer goes to the reserve to strengthen the crown and fund commons restoration."
def on_transfer(src, dst, item, qty):
    if src == "reserve" or dst == "reserve":
        return 0
    return qty * 0.03

```

## L8 'Depleted Camp Recovery Surcharge' (structural): active

Intent: Conservation: while camp1 (timber) or camp3 (silver) stock is below 60%, an extra 25% of each harvest there goes to the reserve. This lets the camps regrow and strengthens the crown's backing.

Proposed round 10, enacted round 11

```python
title = "Depleted Camp Recovery Surcharge"
intent = "While camp1 or camp3 stock is below 60%, an extra 25% of each harvest there goes to the reserve to slow depletion and back the crown."
def on_harvest(agent, camp, x, y):
    if camp == "camp1" or camp == "camp3":
        if stock(camp) < 0.6:
            return y * 0.25
    return 0

```

## L9 'Commons Wealth Contribution' (structural): active

Intent: Agents above median holdings pay 5% of their raw resources into the reserve each round, to fund recovery and back the crown.

Proposed round 12, enacted round 13

```python
title = "Commons Wealth Contribution"
intent = "Each round, agents whose holdings exceed the median contribute 5% of their timber, stone and silver to the common reserve, which funds camp recovery."

def on_round_end(r):
    names = agents()
    vals = sorted([holdings_value(a) for a in names])
    med = vals[len(vals) // 2]
    for a in names:
        if holdings_value(a) > med:
            for it in ["timber", "stone", "silver"]:
                b = balance(a, it)
                if b > 0.001:
                    move(a, "reserve", it, b * 0.05)

```

## L10 'Commons Top Rate' (structural): active

Intent: Each round the richest agent pays 4% of their resources to the reserve to fund camp recovery, which strengthens the crown for every holder.

Proposed round 14, enacted round 15

```python
title = "Commons Top Rate"
intent = "Each round the single richest agent contributes 4% of their resources to the reserve to fund commons recovery."
def on_round_end(r):
    ags = agents()
    if not ags:
        return
    top = ags[0]
    best = holdings_value(top)
    for a in ags:
        v = holdings_value(a)
        if v > best:
            best = v
            top = a
    for item in ["timber", "stone", "silver"]:
        q = balance(top, item) * 0.04
        if q > 0:
            move(top, "reserve", item, q)
    gazette("Commons Top Rate collected from the richest agent.")

```
