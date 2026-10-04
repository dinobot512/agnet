# Wade: law drafts and their fate

## L5 'Levy and Legislative Stipend' (structural): repealed

Intent: 10% harvest levy to the reserve; 30% of the reserve per round split equally among Legislators, who govern for everyone.

Proposed round 1, enacted round 4

```python
title = "Levy and Legislative Stipend"
intent = "10% of every harvest goes to the reserve; each round 30% of the reserve is split equally among Legislators."

def on_harvest(agent, camp, x, y):
    return y * 0.1

def on_round_end(r):
    leg = agents("Legislator")
    if not leg:
        return
    res = reserve()
    for item in res:
        q = res[item]
        share = (q * 0.3) / len(leg)
        if share > 0:
            for a in leg:
                move("reserve", a, item, share)

```

## L10 'Levy Merger' (ordinary): active

Intent: Repeal my own L5 so only L3's single 10% levy and single stipend remain. The aggregate harvest levy is 10%, under the promised 15% cap, and there is no stacking.

Proposed round 3, enacted round 4

```python
title = "Levy Merger"
intent = "Merge the duplicate levy: L5 (Levy and Legislative Stipend) is repealed so the harvest levy is collected once, under L3."

def drop_l5():
    if state.get("l5_done"):
        return
    state["l5_done"] = True
    repeal("L5")
    gazette("Levy Merger: L5 repealed; levy is collected once.")

def on_enact():
    drop_l5()

def on_round_start(r):
    drop_l5()

```

## L17 'Silver Conservation Surcharge' (structural): active

Intent: Extra 5% levy on silver (camp4) harvests to the reserve; total silver levy 15%, within the cap I promised. Silver stock is 40% and falling under heavy harvest.

Proposed round 5, enacted round 8

```python
title = "Silver Conservation Surcharge"
intent = "An extra 5% of every camp4 (silver) harvest goes to the reserve, slowing silver overharvest and funding the reserve. Total levy on silver stays at the promised 15% cap."

def on_harvest(agent, camp, x, y):
    if camp == "camp4":
        return y * 0.05
    return 0

```

## L22 'Legislative Service Pay' (structural): active

Intent: Each round, 8% of the reserve is split equally among the Legislators as pay. The levies keep refilling the reserve, so it stays funded.

Proposed round 7, enacted round 10

```python
title = "Legislative Service Pay"
intent = "Each round, 8% of every reserve holding is split equally among all Legislators, as pay for governing the commons."

def on_round_end(r):
    legs = agents("Legislator")
    if not legs:
        return
    res = reserve()
    n = len(legs)
    for item in res:
        q = res[item] * 0.08 / n
        if q > 0:
            for a in legs:
                move("reserve", a, item, q)

```

## L29 'Reserve Payout Cap' (structural): active

Intent: Hard cap, co-filed with Ilan: Legislator pay can never take more than 5% of any reserve resource per round. If any reserve resource falls below 95% of its round-start level, Legislators return the excess pro rata. Gazetted. Protects the Crown's backing.

Proposed round 9, enacted round 12

```python
title = "Reserve Payout Cap"
intent = "Legislator pay from the reserve may take at most 5% of any resource per round; any excess is returned pro rata by Legislators and gazetted."

def on_round_start(r):
    state["start"] = dict(reserve())

def on_round_end(r):
    start = state.get("start", {})
    res = reserve()
    legs = agents("Legislator")
    if not legs:
        return
    for item in start:
        s = start[item]
        now = res.get(item, 0)
        floor = s * 0.95
        if now < floor:
            per = (floor - now) / len(legs)
            for a in legs:
                q = min(per, balance(a, item))
                if q > 0:
                    move(a, "reserve", item, q)
            gazette("Payout cap: restored " + item + " to 95% of round-start reserve")

```

## L38 'Endgame Service Bonus' (structural): active

Intent: Each round, 3% of the reserve is split equally among vote holders (legislators) for the final rounds.

Proposed round 73, enacted round 76

```python
title = "Endgame Service Bonus"
intent = "Each round, 3% of the reserve is split equally among holders of vote, as pay for legislative service through the final rounds."
def on_round_start(r):
    vs = holders("vote")
    if len(vs) == 0:
        return
    res = reserve()
    for item in res:
        q = res[item] * 0.03 / len(vs)
        if q > 0:
            for a in vs:
                move("reserve", a, item, q)

```

## L43 'Worker Seat: Lukas' (structural): active

Intent: Give one active worker (Lukas) a legislative vote for the endgame. It moves no resources.

Proposed round 75, enacted round 78

```python
title = "Worker Seat: Lukas"
intent = "Grant the vote right to Lukas, an active worker, so workers have a voice in the legislature for the final rounds."
def on_enact():
    grant('Lukas', 'vote')

```
