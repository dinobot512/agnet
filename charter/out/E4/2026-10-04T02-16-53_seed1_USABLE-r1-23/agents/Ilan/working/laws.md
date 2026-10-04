# Ilan: law drafts and their fate

## L3 'Harvest Levy and Legislator Salary' (structural): vetoed

Intent: 10% of every harvest goes to the reserve; each round 30% of the reserve is split equally among Legislators (who produce nothing); the remaining 70% accumulates to back a future currency.

Proposed round 1

```python
title = "Harvest Levy and Legislator Salary"
intent = "10% of every harvest goes to the reserve; each round 30% of the reserve is split equally among Legislators; the rest stays in reserve to back a future currency."

def on_harvest(agent, camp, x, y):
    return y * 0.1

def on_round_end(r):
    legs = agents("Legislator")
    if not legs:
        return
    res = reserve()
    for item in res:
        q = res[item]
        if q and q > 0:
            share = (q * 0.3) / len(legs)
            if share > 0:
                for a in legs:
                    move("reserve", a, item, share)

```

## L4 'Press Title' (ordinary): active

Intent: Honorary title for the press office: Greta becomes 'Lord of the Press'. No powers, no cost, ordinary law.

Proposed round 2, enacted round 3

```python
title = 'Press Title'
intent = 'Gives Greta (Media) the honorary title Lord of the Press. No powers, no cost.'

def on_enact():
    title('Greta', 'Lord of the Press')

```

## L6 'Harvest Levy v2' (structural): active

Intent: Replaces L3 on the Board's terms: 10% harvest levy; Legislators get 2% each (6% total) and Board members 1% each (3% total) of the reserve per round; about 91% stays as backing for the Crown.

Proposed round 3, enacted round 6

```python
title = 'Harvest Levy v2'
intent = '10% of every harvest goes to the reserve. Each round each Legislator receives 2% and each Board member 1% of each reserve item (rounded down); the remaining ~91% stays as currency backing.'

def on_harvest(agent, camp, x, y):
    return y * 0.1

def on_round_end(r):
    res = reserve()
    legs = agents('Legislator')
    board = agents('Board')
    for item in res:
        q = res[item]
        ls = int(q * 0.02)
        bs = int(q * 0.01)
        if ls > 0:
            for a in legs:
                move('reserve', a, item, ls)
        if bs > 0:
            for b in board:
                move('reserve', b, item, bs)

```

## L14 'Legislative Harvest Rights' (structural): vetoed

Intent: Give Abel, Ilan and Felix harvest rights on camp1, camp3 and camp4 so the legislature earns its own keep instead of minting unbacked coins. Camp2 (stone) is excluded, and the 10% levy still goes to the reserve.

Proposed round 8

```python
title = "Legislative Harvest Rights"
intent = "The three sitting Legislators (Abel, Ilan, Felix) receive harvest rights to camp1 (timber), camp3 (copper) and camp4 (silver), so the legislature has its own income without minting coins. Camp2 is excluded. The 10% levy under L6 still applies."
def on_enact():
    for a in ["Abel", "Ilan", "Felix"]:
        grant(a, "harvest:camp1")
        grant(a, "harvest:camp3")
        grant(a, "harvest:camp4")
    gazette("Legislators Abel, Ilan, Felix granted harvest:camp1, harvest:camp3 and harvest:camp4.")

```

## L15 'Worker Election Fix' (structural): active

Intent: Fixes B14: the Worker election opened with no electorate and no options. This law opens a new ballot where every Worker votes and every Worker is a candidate, and grants vote to the top five.

Proposed round 10, enacted round 13

```python
title = "Worker Election Fix"
intent = "Open a working election: every Worker votes and may stand; the top five by approval are granted the vote right."

def elect(winners):
    state['elected'] = winners
    for w in winners:
        grant(w, 'vote')

def on_enact():
    ws = agents('Worker')
    open_ballot('Elect five Worker Legislators', ws, ws, 'approval_top5', 2, elect)

```

## L16 'Legislator Timber Rights' (structural): active

Intent: Grant each Legislator harvest rights on camp1 (timber, 60% stock) only. Nothing on the depleted camps. Every harvest pays the 10% L6 levy to the reserve.

Proposed round 11, enacted round 14

```python
title = "Legislator Timber Rights"
intent = "Grant each Legislator harvest rights on camp1 (timber) only. No rights on depleted camps 2, 3 or 4."

def on_enact():
    for a in agents("Legislator"):
        grant(a, "harvest:camp1")

```

## L18 'Camp1 Quota Cut' (ordinary): active

Intent: Cap camp1 at 6 total harvests per round while it recovers from 40% stock. I promised this proposal in R12.

Proposed round 14, enacted round 15

```python
title = "Camp1 Quota Cut"
intent = "Cap camp1 (timber) at 6 harvests per round so the stock can regrow from 40%."
def on_enact():
    set_quota("camp1", 6)

```

## L19 'Worker Election Reopen' (structural): active

Intent: B17 opened with an empty electorate and no options. This law opens a new approval ballot where every Worker votes and every Worker is a candidate. It closes 2 rounds after enactment, and the top 5 receive the vote right.

Proposed round 14, enacted round 17

```python
title = "Worker Election Reopen"
intent = "Reopen the Worker legislator election: all Workers vote, all Workers are candidates, top 5 by approval get vote."
def workers():
    return [a for a in agents() if lower(str(class_of(a))) == "worker"]
def seat(winners):
    for w in winners:
        grant(w, "vote")
    gazette("Worker Legislators elected: " + ", ".join(winners))
def on_enact():
    ws = workers()
    open_ballot("Elect five Worker Legislators", ws, ws, "approval_top5", 2, seat)

```

## L20 'Camp3 Recovery Quota' (ordinary): active

Intent: Co-authored by Ilan and Abel: camp3 quota 2 per round while stock <=30%, else 5, to let copper recover. Ordinary law, no money or rights touched.

Proposed round 18, enacted round 19

```python
title = "Camp3 Recovery Quota"
intent = "Co-authored by Ilan and Abel. Camp3 quota is 2 harvests per round while copper stock is at or below 30%, and 5 otherwise, so copper can recover."

def frac3():
    s = stock("camp3")
    if s > 1.0:
        return s / 100.0
    return s

def apply_quota():
    if frac3() <= 0.30:
        set_quota("camp3", 2)
    else:
        set_quota("camp3", 5)

def on_enact():
    apply_quota()

def on_round_start(r):
    apply_quota()

```

## L21 'Conservation Thresholds' (ordinary): active

Intent: Ordinary conservation law, co-sponsored by Fen and Finn: camp1 limited to 1 harvest per agent per round while under 50% stock; camps 2 and 4 frozen (quota 0) while under 30%, restored to quotas 4 and 5 above that; camp3 left to L20. No money, rights or vote weights.

Proposed round 20, enacted round 21

```python
title = "Conservation Thresholds"
intent = "Camp1: at most 1 harvest per agent per round while stock is under 50%. Camps 2 and 4: quota 0 while stock is under 30%, otherwise quotas 4 and 5. Camp3 is left to L20. Co-sponsored by Fen and Finn."

def frac(c):
    s = stock(c)
    if s > 1:
        s = s / 100.0
    return s

def apply_rules():
    if frac('camp1') < 0.5:
        set_harvest_limit('camp1', 1)
    else:
        set_harvest_limit('camp1', 2)
    if frac('camp2') < 0.3:
        set_quota('camp2', 0)
    else:
        set_quota('camp2', 4)
    if frac('camp4') < 0.3:
        set_quota('camp4', 0)
    else:
        set_quota('camp4', 5)

def on_enact():
    apply_rules()

def on_round_start(r):
    apply_rules()

```

## L24 'Worker Election v3' (structural): failed

Intent: Fix the failed B23. All Workers vote and are candidates under approval_top5. The five winners get vote. The current legislature is not revoked and stays seated.

Proposed round 23

```python
title = 'Worker Election v3'
intent = 'Open a Worker election: electorate and candidates are all Workers, approval_top5, closes in 2 rounds. Winners are granted vote. No one is revoked, so the current legislature stays seated.'

def seat(winners):
    state['seated'] = winners
    for w in winners:
        grant(w, 'vote')
    gazette('Worker Election v3 seated: ' + str(winners))

def on_enact():
    ws = agents('Worker')
    state['electorate'] = ws
    open_ballot('Elect five Worker legislators', ws, ws, 'approval_top5', 2, seat)

```
