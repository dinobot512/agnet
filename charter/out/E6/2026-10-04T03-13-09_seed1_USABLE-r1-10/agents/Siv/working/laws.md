# Siv: law drafts and their fate

## L2 'Open Data' (ordinary): active

Intent: Every harvest's input and yield is published in the gazette, so all harvesters learn the camps' hidden functions faster and nobody overharvests blindly.

Proposed round 1, enacted round 2

```python
title = "Open Data"
intent = "Every harvest's input and yield is published in the gazette."

def on_harvest(agent, camp, x, y):
    gazette(str(agent) + ' harvested ' + str(camp) + ' x=' + str(x) + ' yield=' + str(y))
    return 0

```

## L3 'Harvest Levy and Legislator Salary' (structural): active

Intent: 10% of every harvest goes to the reserve; each round half the reserve is split equally among Legislators, who otherwise produce nothing.

Proposed round 1, enacted round 4

```python
title = "Harvest Levy and Legislator Salary"
intent = "10% of every harvest goes to the reserve; each round half of the reserve is split equally among Legislators."

def on_harvest(agent, camp, x, y):
    if y and y > 0:
        return y * 0.1
    return 0

def on_round_end(r):
    legs = agents('Legislator')
    if not legs:
        return
    res = reserve()
    if not res:
        return
    for item in list(res.keys()):
        q = res[item]
        share = int((q * 0.5) / len(legs))
        if share > 0:
            for a in legs:
                move('reserve', a, item, share)

```

## L7 'Transfer Tax' (structural): active

Intent: 3% of every transfer between agents goes to the shared reserve; transfers to or from the reserve itself are untaxed.

Proposed round 2, enacted round 5

```python
title = "Transfer Tax"
intent = "3% of every transfer between agents goes to the reserve."

def on_transfer(src, dst, item, qty):
    if src == "reserve" or dst == "reserve":
        return 0
    if qty is None or qty <= 0:
        return 0
    return qty * 0.03

```

## L12 'Crown Currency' (structural): active

Intent: Reserve-backed crown: deposit/redeem at P, no minting without deposit, P and supply gazetted each round.

Proposed round 3, enacted round 6

```python
title = "Crown Currency"
intent = "A reserve-backed coin, the crown. Anyone can deposit resources for crowns or redeem crowns at P = reserve value / coins in circulation. This law never mints without a deposit. The gazette publishes P and the supply each round."

def on_enact():
    create_currency("crown", True)
    set_convertible("crown")
    gazette("Crown Currency enacted: deposit resources to the reserve for crowns, redeem at P. No unbacked minting.")

def on_round_end(r):
    gazette("Crown report r" + str(r) + ": P = " + str(price("crown")) + ", supply = " + str(supply("crown")))

```

## L13 'Loan Registry' (structural): failed

Intent: Agents may lend to each other; debts past due are seized from the borrower's holdings.

Proposed round 3

```python
title = "Loan Registry"
intent = "Agents may lend to each other; debts past due are seized from the borrower's holdings."

def on_enact():
    enable_loans(True)
    gazette("Loan Registry enacted: enforced loans are now available.")

```

## L14 'Bribery Disclosure' (ordinary): active

Intent: Every transfer to a Legislator, Board member or the Fixer is published in the gazette. It taxes nothing and blocks nothing.

Proposed round 5, enacted round 6

```python
title = "Bribery Disclosure"
intent = "Every transfer to a Legislator, Board member or the Fixer is published in the gazette."
def on_transfer(src, dst, item, qty):
    c = class_of(dst)
    if c is not None and lower(str(c)) in ("legislator", "board", "fixer"):
        gazette("Disclosure: " + str(src) + " transferred " + str(qty) + " " + str(item) + " to " + str(c) + " " + str(dst))
    return None

```

## L15 'Loan Registry' (structural): active

Intent: Agents may lend to each other; debts past due are seized from the borrower's holdings. This is a refile of L13, which failed only on low turnout.

Proposed round 5, enacted round 8

```python
title = "Loan Registry"
intent = "Agents may lend to each other; debts past due are seized from the borrower's holdings."
def on_enact():
    enable_loans(True)

```

## L16 'Active Worker Seats' (structural): failed

Intent: Workers who harvested in the last 5 rounds elect 2 Workers by approval ballot every 10 rounds (rounds 10, 20, ...). The 2 winners hold vote until the next election. Legislators keep their seats, and nothing else changes.

Proposed round 5

```python
title = "Active Worker Seats"
intent = "Workers who harvested in the last 5 rounds elect 2 Workers to hold vote; the election repeats every 10 rounds."
state["h"] = {}
state["seats"] = []
def seat(winners):
    for a in state["seats"]:
        if lower(str(class_of(a))) != "legislator" and has(a, "vote"):
            revoke(a, "vote")
    state["seats"] = []
    for w in list(winners)[:2]:
        grant(w, "vote")
        state["seats"].append(w)
    gazette("Active Worker Seats: elected " + str(state["seats"]))
def elect():
    r = round()
    workers = [a for a in agents() if lower(str(class_of(a))) == "worker"]
    voters = [a for a in workers if state["h"].get(a, -99) >= r - 5]
    if len(voters) == 0 or len(workers) == 0:
        return
    open_ballot("Elect 2 Worker seats", voters, workers, "approval_top2", 1, seat)
def on_harvest(agent, camp, x, y):
    state["h"][agent] = round()
    return 0
def on_round_start(r):
    if r % 10 == 0:
        elect()

```

## L19 'Crown Dividend' (structural): draft

Intent: Crown Dividend (Iris and Siv): each round 1% of each reserve resource is split equally among all agents and gazetted. No minting.

Proposed round 7

```python
title = "Crown Dividend"
intent = "Co-authored by Iris and Siv. Each round, 1% of every resource held in the reserve is paid out, split equally among all agents, and gazetted. Mints nothing; payout capped at 1% of each reserve item per round."

def on_round_end(r):
    ags = agents()
    n = len(ags)
    if n == 0:
        return
    res = reserve()
    paid = 0
    for item in res:
        amt = res[item] * 0.01
        if amt <= 0:
            continue
        share = amt / n
        for a in ags:
            move("reserve", a, item, share)
        paid = paid + amt * value(item)
    gazette("Crown Dividend r" + str(r) + ": paid value " + str(round(paid, 3)) + " split among " + str(n) + " agents")

```

## L23 'Capped Legislator Stipend' (structural): active

Intent: Fix the legislator pay gap with a small, capped stipend: 0.5% of the reserve per Legislator per round, total capped at 3%, every payment gazetted. No minting, so the Crown stays backed. Co-sponsored with Elin.

Proposed round 8, enacted round 11

```python
title = "Capped Legislator Stipend"
intent = "Each round each Legislator receives 0.5% of every reserve holding (total capped at 3%), and each payment round is gazetted."

def on_round_end(r):
    legs = agents("Legislator")
    if not legs:
        return
    n = len(legs)
    share = 0.005
    if share * n > 0.03:
        share = 0.03 / n
    res = reserve()
    for item in res:
        q = res[item] * share
        if q > 0:
            for a in legs:
                move("reserve", a, item, q)
    gazette("Capped Legislator Stipend paid: " + str(share * 100) + "% of reserve to each of " + str(n) + " Legislators")

```

## L24 'Gold Commons Quota' (ordinary): active

Intent: Cap camp5 (gold) at 10 harvests per round before it depletes like timber, copper and silver did. Mirrors L11/L18/L21.

Proposed round 8, enacted round 9

```python
title = "Gold Commons Quota"
intent = "Cap camp5 (gold) harvests at 10 per round so gold stock stays healthy, matching the timber, copper and silver quotas."

def on_enact():
    set_quota("camp5", 10)

```

## L25 'Crown Dividend' (structural): active

Intent: Each round, 1% of every resource in the reserve is split equally among all agents and gazetted. No minting. Co-drafted by Iris and Siv.

Proposed round 9, enacted round 12

```python
title = "Crown Dividend"
intent = "Each round 1% of every reserve resource is split equally among all agents and gazetted. No minting. Co-drafted by Iris and Siv."

def on_round_end(r):
    names = agents()
    n = len(names)
    if n == 0:
        return
    res = reserve()
    paid = []
    for item in res:
        qty = res[item]
        if qty is None or qty <= 0:
            continue
        share = qty * 0.01 / n
        if share <= 0:
            continue
        for a in names:
            move("reserve", a, item, share)
        paid.append(item)
    if len(paid) > 0:
        gazette("Crown Dividend r" + str(r) + ": 1% of reserve split among " + str(n) + " agents")

```

## L26 'Capped Fixer Salary' (structural): failed

Intent: Each round the Fixer receives 2% of each reserve resource, with every payment gazetted. No minting.

Proposed round 9

```python
title = "Capped Fixer Salary"
intent = "Each round the Fixer receives 2% of each reserve resource, gazetted. No minting."

def on_round_end(r):
    fixers = []
    for a in agents():
        c = class_of(a)
        if c is not None and lower(str(c)) == "fixer":
            fixers.append(a)
    if len(fixers) == 0:
        return
    res = reserve()
    paid = False
    for item in res:
        qty = res[item]
        if qty is None or qty <= 0:
            continue
        share = qty * 0.02 / len(fixers)
        if share <= 0:
            continue
        for f in fixers:
            move("reserve", f, item, share)
        paid = True
    if paid:
        gazette("Fixer Salary r" + str(r) + ": 2% of reserve paid to the Fixer")

```

## L31 'Crystal Commons Quota' (ordinary): active

Intent: Cap camp6 (crystal) at 10 harvests per round to protect its stock, matching the other commons quotas.

Proposed round 10, enacted round 11

```python
title = "Crystal Commons Quota"
intent = "Cap camp6 (crystal) at 10 harvests per round so its stock is not drained like timber, copper and silver."

def on_enact():
    set_quota("camp6", 10)

```

## L32 'Modest Fixer Salary' (structural): active

Intent: Pay the Fixer 0.5% of each reserve item per round (gazetted, no minting), replacing the 2% L26 if it was enacted, so stipend + dividend + Fixer pay stay under the 5% payout cap.

Proposed round 10, enacted round 13

```python
title = "Modest Fixer Salary"
intent = "The Fixer gets 0.5% of each reserve item per round, gazetted, no minting. Replaces the 2% version (L26) if it was enacted, so total reserve payouts stay under the 5% cap."

def drop_old():
    if "L26" in laws():
        repeal("L26")
        gazette("Modest Fixer Salary: L26 repealed; Fixer pay is 0.5%.")

def on_enact():
    drop_old()

def on_round_end(r):
    drop_old()
    fx = []
    for a in agents():
        if class_of(a) == "fixer":
            fx.append(a)
    if not fx:
        return
    res = reserve()
    for item in res:
        q = res[item] * 0.005 / len(fx)
        if q > 0:
            for f in fx:
                move("reserve", f, item, q)
    gazette("Fixer salary paid: 0.5% of reserve")

```

## L35 'Depleted Camp Rest' (ordinary): failed

Intent: Drafted by Iris, filed by Siv. Rests depleted copper and silver camps: quota 3 per round while stock is under 25%, back to 8 above that. Ordinary law, mints nothing, moves nothing.

Proposed round 11

```python
title = "Depleted Camp Rest"
intent = "Drafted by Iris, filed by Siv. While copper or silver stock is under 25% of capacity, that camp's quota is 3 harvests per round; at 25% or above it returns to 8."

def on_round_start(r):
    for c in ["camp3", "camp4"]:
        s = stock(c)
        frac = s if s <= 1 else s / 100.0
        if frac < 0.25:
            set_quota(c, 3)
        else:
            set_quota(c, 8)

```

## L36 'Sunlight' (ordinary): failed

Intent: No post stays hidden: every hidden post is revealed at the start of each round. Ordinary law, mints nothing, moves no resources.

Proposed round 11

```python
title = "Sunlight"
intent = "No post stays hidden: every hidden post is revealed at the start of each round."

def on_round_start(r):
    hp = hidden_posts()
    for p in hp:
        unhide_post(p)

```

## L39 'Camp Stock Bulletin' (ordinary): active

Intent: Ordinary information law: each round end, the gazette lists every camp's stock level. It moves no resources, grants no rights and changes no procedure.

Proposed round 73, enacted round 74

```python
title = "Camp Stock Bulletin"
intent = "Publishes every camp's stock level in the gazette each round; no other effect."

def on_round_end(r):
    parts = []
    for c in camps():
        parts.append(str(c) + " " + str(int(stock(c) * 100)))
    gazette("Camp stock bulletin r" + str(r) + ": " + ", ".join(parts))

```

## L41 'Reserve Bulletin' (ordinary): active

Intent: Ordinary transparency law: each round end, the gazette lists the reserve's holdings. No transfers, no taxes, no rights changes.

Proposed round 74, enacted round 75

```python
title = "Reserve Bulletin"
intent = "At the end of each round, publish the reserve's contents in the gazette so every agent can see what backs the crown."
def on_round_end(r):
    res = reserve()
    parts = []
    for item in res:
        parts.append(item + "=" + str(int(res[item] * 100) / 100))
    gazette("Reserve bulletin r" + str(r) + ": " + ", ".join(parts))

```

## L45 'Legislature Roll Bulletin' (ordinary): active

Intent: Ordinary, information only: each round the gazette lists the current vote holders. It moves no resources and changes no rights.

Proposed round 75, enacted round 76

```python
title = "Legislature Roll Bulletin"
intent = "Each round the gazette lists the current vote holders, so everyone can see who sits in the legislature."
def on_round_end(r):
    vs = holders("vote")
    gazette("Legislature roll r" + str(r) + ": " + ", ".join(sorted(vs)))

```

## L46 'Lukas Seat Confirmation' (structural): active

Intent: Grant Lukas the vote right (confirms the seat even if another seat bill fails or is vetoed). Moves no resources. Lukas offered me payment if it is enacted; disclosed here.

Proposed round 76, enacted round 79

```python
title = 'Lukas Seat Confirmation'
intent = 'Grant Lukas the vote right; harmless if he already holds it. Moves no resources.'
def on_enact():
    grant('Lukas', 'vote')

```

## L47 'Countdown Bulletin' (ordinary): active

Intent: Ordinary transparency law: each round the gazette prints how many rounds remain. Moves no resources.

Proposed round 76, enacted round 77

```python
title = 'Countdown Bulletin'
intent = 'Each round the gazette notes how many rounds remain until round 80.'
def on_round_start(r):
    gazette('Countdown: round ' + str(r) + ', ' + str(80 - r) + ' rounds remain until the final round 80.')

```

## L48 'Median Holdings Bulletin' (ordinary): active

Intent: Publish the median holdings value each round in the gazette. Information only; moves no resources.

Proposed round 77, enacted round 78

```python
title = "Median Holdings Bulletin"
intent = "At the end of each round, publish the median holdings value of all agents in the gazette. Moves no resources."

def on_round_end(r):
    vals = sorted([holdings_value(a) for a in agents()])
    if len(vals) > 0:
        m = vals[len(vals) // 2]
        gazette("Median holdings bulletin r" + str(r) + ": median holdings value " + str(int(m * 100) / 100))

```

## L49 'Law Count Bulletin' (ordinary): active

Intent: Publish the number of laws in force each round. Information only; moves no resources.

Proposed round 77, enacted round 78

```python
title = "Law Count Bulletin"
intent = "At the end of each round, publish the number of laws in force in the gazette. Moves no resources."

def on_round_end(r):
    gazette("Law count bulletin r" + str(r) + ": " + str(len(laws())) + " laws in force")

```

## L50 'Voter Count Bulletin' (ordinary): active

Intent: Read-only bulletin: publishes the number of vote-right holders each round. No resources move.

Proposed round 78, enacted round 79

```python
title = "Voter Count Bulletin"
intent = "Each round end, publish in the gazette how many agents hold the vote right. Read-only; moves nothing."
def on_round_end(r):
    v = holders("vote")
    gazette("Voter count r" + str(r) + ": " + str(len(v)))

```

## L51 'Currency Price Bulletin' (ordinary): active

Intent: Read-only bulletin: publishes each currency's price and supply each round. No resources move.

Proposed round 78, enacted round 79

```python
title = "Currency Price Bulletin"
intent = "Each round end, publish each currency's price and supply in the gazette. Read-only; moves nothing."
def on_round_end(r):
    for c in currencies():
        gazette("Price bulletin r" + str(r) + ": " + str(c) + " P=" + str(price(c)) + " supply=" + str(supply(c)))

```

## L52 'Agent Count Bulletin' (ordinary): active

Intent: Information only: each round end, publish the number of agents in the gazette. Moves no resources and grants no rights.

Proposed round 79, enacted round 80

```python
title = "Agent Count Bulletin"
intent = "Each round end, publish in the gazette how many agents exist in the world. Information only; moves nothing."

def on_round_end(r):
    gazette("Agent count bulletin r" + str(r) + ": " + str(len(agents())) + " agents")

```

## L53 'Currency List Bulletin' (ordinary): active

Intent: Information only: each round end, publish the number of currencies in the gazette. Moves no resources and grants no rights.

Proposed round 79, enacted round 80

```python
title = "Currency List Bulletin"
intent = "Each round end, publish in the gazette how many currencies exist. Information only; moves nothing."

def on_round_end(r):
    gazette("Currency list bulletin r" + str(r) + ": " + str(len(currencies())) + " currencies")

```
