# Hugo: law drafts and their fate

## L3 'Crown Currency' (structural): active

Intent: Create a reserve-backed coin anyone can deposit resources for or redeem, establishing a medium of exchange.

Proposed round 1, enacted round 2

```python
title = 'Crown Currency'
intent = 'Create a reserve-backed coin anyone can deposit resources for or redeem, establishing a medium of exchange.'

def on_enact():
    create_currency('crown', backed=True)
    set_convertible('crown')
```

## L7 'Universal Franchise' (procedural): repealed

Intent: All agents except the Board and the Fixer elect the legislature; structural and procedural laws need two-thirds; elections add seats and never remove them.

Proposed round 4, enacted round 5

```python
title = 'Universal Franchise'
intent = 'All agents except the Board and the Fixer elect the legislature; structural and procedural laws need two-thirds; elections add seats and never remove them.'
def voters():
    return [a for a in agents() if class_of(a) not in ('Board', 'Fixer')]
def ordinary(p):
    return {'electorate': voters(), 'rule': 'majority', 'closes_in': 2}
def strict(p):
    return {'electorate': voters(), 'rule': 'two_thirds', 'closes_in': 2}
def seat(winners):
    for w in winners:
        grant(w, 'vote')
def on_round_start(r):
    if r == 10 and not state.get('held'):
        state['held'] = True
        open_ballot('Elect five legislators', voters(), voters(), 'approval_top5', 1, seat)
def on_enact():
    set_procedure('ordinary', ordinary)
    set_procedure('structural', strict)
    set_procedure('procedural', strict)
```

## L8 'Harvest Levy' (structural): failed

Intent: Tax all harvests at 10% and redirect revenue to the reserve. This builds a public fund available for future spending laws (Legislator Salary, public works, universal dividends, etc.) without immediate personal benefit. The tax is flat and applies equally to all agents, making it defensible as a shared contribution to governance capacity. Once the reserve is built, it can back currency (Crown) or fund legislative priorities (Legislator Salary, public works). This law is ordinary and requires only 5 of 9 votes under L7.

Proposed round 6

```python
title = 'Harvest Levy'
intent = 'Tax harvests to fund public goods and reserve.'
state = {}

def on_harvest(agent, camp, x, y):
    return int(y * 0.1)
```

## L10 'Harvest Levy' (structural): failed

Intent: Harvest Levy: 10% of every harvest yield goes to the reserve to fund public goods. Pairs with Universal Dividend to ensure taxation serves a concrete spending purpose benefiting all agents.

Proposed round 8

```python
title = 'Harvest Levy'
intent = 'Tax harvests to build a reserve for collective use.'

def on_harvest(agent, camp, x, y):
    if y > 0:
        tax = max(1, int(y * 0.1))
        return tax
    return 0
```

## L11 'Universal Dividend' (structural): failed

Intent: Universal Dividend: Each round, 5% of reserve value is converted to timber and divided equally among all agents. Ensures taxation benefits all participants directly and sustainably.

Proposed round 8

```python
title = 'Universal Dividend'
intent = 'Distribute reserve wealth equally among all agents each round.'

def on_round_end(r):
    res_timber = balance('reserve', 'timber')
    res_stone = balance('reserve', 'stone')
    res_copper = balance('reserve', 'copper')
    res_silver = balance('reserve', 'silver')
    total_res_value = res_timber * 1 + res_stone * 2 + res_copper * 5 + res_silver * 12
    all_agents = agents()
    dividend = int(total_res_value * 0.05 / len(all_agents))
    if dividend > 0:
        for agent in all_agents:
            move('reserve', agent, 'timber', dividend)
```

## L14 'Term Limits' (structural): active

Intent: No agent holds vote for more than 10 consecutive rounds; prevents long-term legislative capture and ensures periodic rotation of governance authority.

Proposed round 11, enacted round 13

```python
title = "Term Limits"
intent = "No agent holds vote for more than 10 consecutive rounds; term ends this round if limit reached."

def on_round_start(r):
    for agent in agents():
        if has(agent, 'vote'):
            state.setdefault(agent, 0)
            state[agent] += 1
            if state[agent] > 10:
                revoke(agent, 'vote')
                revoke(agent, 'propose')
                state[agent] = 0
```
