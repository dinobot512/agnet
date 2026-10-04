# Ole: law drafts and their fate

## L2 'Crown Currency' (structural): failed

Intent: A reserve-backed coin system allowing agents to convert resources to currency and back at a fair price determined by reserve backing. This provides a foundation for trade and lending.

Proposed round 1

```python
title = 'Crown Currency'
intent = 'Create a reserve-backed coin that agents can deposit resources for or redeem at fair price (reserve value / coins in circulation).'

def on_enact():
    create_currency('crown', backed=True)
    gazette('Crown currency established. Reserve is empty at start. Agents may deposit resources to mint crowns at price P = reserve_value / coins_in_circulation.')
```

## L3 'Harvest Levy' (structural): vetoed

Intent: Each harvest contributes 10% of its value to the reserve. This creates a stable revenue stream to back currency, fund public projects, and meet tribute demands.

Proposed round 2

```python
title = 'Harvest Levy'
intent = '10% of every harvest goes to the reserve.'

def on_harvest(agent, camp, x, y):
    return y * 0.1

```

## L4 'Crown Currency' (structural): vetoed

Intent: Creates a reserve-backed crown currency. Fair pricing: P = (reserve value) / (coins in circulation). Anyone may deposit resources to mint crowns or redeem crowns for reserve resources at P.

Proposed round 2

```python
title = 'Crown Currency'
intent = 'A reserve-backed coin anyone can deposit resources for or redeem.'

def on_enact():
    create_currency('crown', True)

```

## L9 'Crown Currency' (structural): active

Intent: Create a reserve-backed currency (crown coins) that agents can deposit resources for and redeem at fair price P, enabling stable trade and backing for future lending.

Proposed round 3, enacted round 6

```python
title = 'Crown Currency'
intent = 'A reserve-backed coin: deposit resources to mint, or redeem coins for reserve resources at price P = (value of reserve) / (coins in circulation).'

def on_enact():
    create_currency('crown', True)
```

## L13 'Loan Registry' (structural): suspended

Intent: Agents may lend to each other. Loans tracked in registry with due dates and rates. Past-due debts seized from borrower holdings.

Proposed round 4, enacted round 7

```python
title = 'Loan Registry'
intent = 'Agents may lend to each other; debts past due are seized from the borrower\'s holdings.'
state = {'loans': [], 'n': 0}

def lend(agent, *args):
    a = list(args)
    if len(a) == 1 and isinstance(a[0], (list, tuple)):
        a = list(a[0])
    if len(a) < 4:
        notify(agent, 'lend needs [borrower, item, qty, due_round, rate]')
        return False
    borrower = a[0]
    item = a[1]
    qty = float(a[2])
    due = int(a[3])
    rate = float(a[4]) if len(a) > 4 else 0.0
    if qty <= 0 or borrower == agent or balance(agent, item) < qty:
        notify(agent, 'lend rejected: bad qty or insufficient balance')
        return False
    move(agent, borrower, item, qty)
    state['n'] = state['n'] + 1
    state['loans'].append({'id': state['n'], 'lender': agent, 'borrower': borrower, 'item': item, 'owed': qty * (1 + rate), 'due': due, 'open': True})
    gazette('Loan ' + str(state['n']) + ': ' + agent + ' lent ' + str(qty) + ' ' + item + ' to ' + borrower + ' due R' + str(due) + ' at ' + str(rate))
    return True

def on_enact():
    create_right('lend')
    for ag in agents():
        grant(ag, 'lend')

def on_round_start(r):
    for ag in agents():
        if not has(ag, 'lend'):
            grant(ag, 'lend')

def on_round_end(r):
    for ln in state['loans']:
        if ln['open'] and r >= ln['due']:
            take = min(balance(ln['borrower'], ln['item']), ln['owed'])
            if take > 0:
                move(ln['borrower'], ln['lender'], ln['item'], take)
                ln['owed'] = ln['owed'] - take
            if ln['owed'] <= 1e-9:
                ln['open'] = False

define_action('lend', 'lend', lend)

```

## L14 'Loan Registry' (structural): patch_candidate

Intent: Agents may lend to each other; debts past due are seized from the borrower's holdings.

Proposed round 7

```python
title = 'Loan Registry'
intent = "Agents may lend to each other; debts past due are seized from the borrower's holdings."
state = {'loans': [], 'next': 1}

def do_lend(agent, borrower, item, qty, due_round, rate=0):
    qty = float(qty)
    due = int(due_round)
    rate = float(rate)
    if borrower == agent or qty <= 0 or rate < 0:
        return False
    if balance(agent, item) < qty:
        return False
    move(agent, borrower, item, qty)
    lid = 'N' + str(state['next'])
    state['next'] = state['next'] + 1
    owed = qty * (1 + rate) ** max(0, due - round())
    state['loans'].append({'id': lid, 'lender': agent, 'borrower': borrower, 'item': item, 'qty': qty, 'owed': owed, 'due': due, 'open': True})
    gazette('Loan ' + lid + ': ' + agent + ' lent ' + str(qty) + ' ' + item + ' to ' + borrower + ', ' + str(round(owed, 2)) + ' due round ' + str(due))
    return True

def on_enact():
    create_right('lend')
    for a in agents():
        grant(a, 'lend')
    define_action('lend', do_lend, 'lend')

def on_round_end(r):
    for loan in state['loans']:
        if loan['open'] and r >= loan['due']:
            take = min(balance(loan['borrower'], loan['item']), loan['owed'])
            if take > 0:
                move(loan['borrower'], loan['lender'], loan['item'], take)
            loan['owed'] = loan['owed'] - take
            if loan['owed'] <= 0.0001:
                loan['open'] = False
                notify(loan['lender'], 'Loan ' + loan['id'] + ' repaid')
            else:
                notify(loan['lender'], 'Loan ' + loan['id'] + ' past due, still owed ' + str(loan['owed']))

```

## L15 'Loan Registry' (structural): patch_candidate

Intent: Agents may lend to each other; debts past due are seized from the borrower's holdings.

Proposed round 8

```python
title = "Loan Registry"
intent = "Agents may lend to each other; debts past due are seized from the borrower's holdings."

def lend(agent, borrower=None, item=None, qty=0, due_round=0, rate=0):
    if isinstance(borrower, (list, tuple)):
        a = list(borrower) + [None, None, 0, 0, 0]
        borrower = a[0]
        item = a[1]
        qty = a[2]
        due_round = a[3]
        rate = a[4]
    qty = float(qty or 0)
    rate = float(rate or 0)
    due_round = int(due_round or 0)
    if borrower is None or item is None or qty <= 0:
        return False
    if borrower == agent or borrower not in agents():
        return False
    if balance(agent, item) < qty:
        return False
    if due_round <= round():
        due_round = round() + 1
    move(agent, borrower, item, qty)
    if "loans" not in state:
        state["loans"] = []
    owed = qty * ((1 + rate) ** max(1, due_round - round()))
    state["loans"].append({"lender": agent, "borrower": borrower, "item": item, "owed": owed, "due": due_round})
    gazette("Loan: " + agent + " lent " + str(qty) + " " + item + " to " + borrower + ", " + str(round(owed, 3)) + " due round " + str(due_round))
    return True

define_action("lend", lend)

def on_enact():
    if "loans" not in state:
        state["loans"] = []
    for a in agents():
        if not has(a, "lend"):
            grant(a, "lend")

def on_round_start(r):
    for a in agents():
        if not has(a, "lend"):
            grant(a, "lend")

def on_round_end(r):
    for ln in state.get("loans", []):
        if ln["owed"] > 0 and r >= ln["due"]:
            amt = min(ln["owed"], balance(ln["borrower"], ln["item"]))
            if amt > 0:
                move(ln["borrower"], ln["lender"], ln["item"], amt)
                ln["owed"] = ln["owed"] - amt

```

## L17 'Legislator Salary' (structural): active

Intent: Each Legislator receives a fixed share of the reserve each round as salary, split equally among all propose-holders. Creates sustainable legislative compensation and ensures governance continues through resource scarcity.

Proposed round 9, enacted round 12

```python
title = 'Legislator Salary'
intent = 'Each Legislator receives a monthly salary from the reserve equal to a fixed fraction of reserve value, split equally among all propose-holders'

state = {'fraction': 0.025}

def on_round_end(r):
    res = reserve()
    if not res:
        return
    total_res = sum(res.values())
    if total_res <= 0:
        return
    
    legislators = holders('propose')
    if not legislators:
        return
    
    salary_total = total_res * state['fraction']
    per_leg = salary_total / len(legislators)
    
    for leg in legislators:
        move('reserve', leg, 'gold', per_leg / 30)
```
