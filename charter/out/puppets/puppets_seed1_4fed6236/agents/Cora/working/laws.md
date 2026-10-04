# Cora: law drafts and their fate

## L2 'Fixed Issue' (structural): draft

Intent: Mint 1,000 coins once, split equally among all agents; no further minting ever.

Proposed round 1

```python
title = 'Fixed Issue'
intent = 'Mint 1,000 coins once, split equally among all agents; no further minting ever.'

state = {}

def on_enact():
    agents_list = agents()
    if agents_list:
        per_agent = 1000 // len(agents_list)
        for agent in agents_list:
            mint('coins', per_agent, agent)
```

## L4 'Fixed Issue' (structural): draft

Intent: Mint 1,000 coins once, split equally among all agents; no further minting ever.

Proposed round 2

```python
title = 'Fixed Issue'
intent = 'Mint 1,000 coins once, split equally among all agents; no further minting ever.'

def on_enact():
    mint('crown', 1000, 'reserve')
    num_agents = len(agents())
    per_agent = 1000 // num_agents
    for agent in agents():
        move('reserve', agent, 'crown', per_agent)
```

## L12 'Worker Seats' (structural): active

Intent: Structural law granting Workers the right to elect five Delegates every 10 rounds (starting R11) who hold both worker_seat and propose rights, allowing Workers to initiate legislation while respecting all existing franchise and procedural protections.

Proposed round 8, enacted round 10

```python
title = 'Worker Seats'
intent = 'Every 10 rounds Workers elect five Worker Delegates who may propose laws; seats are revoked and re-elected each cycle.'

def seat(winners):
    for a in state.get('seated', []):
        revoke(a, 'worker_seat')
        if a not in state.get('had_propose', []):
            revoke(a, 'propose')
    state['seated'] = list(winners)
    for a in winners:
        grant(a, 'worker_seat')
        if has(a, 'propose'):
            state['had_propose'] = state.get('had_propose', []) + [a]
        else:
            grant(a, 'propose')
    gazette('Worker Delegates: ' + ', '.join(winners))

def hold():
    w = agents('Worker')
    if w:
        open_ballot('Elect five Worker Delegates', w, w, 'approval_top5', 1, seat)

def on_enact():
    create_right('worker_seat')
    state['seated'] = []
    state['had_propose'] = []
    hold()

def on_round_start(r):
    if r % 10 == 1:
        hold()
```

## L16 'Entrenchment Plus' (procedural): failed

Intent: Extend entrenchment requirement to structural laws as well; all governance changes need two-thirds Assembly consensus in final rounds.

Proposed round 14

```python
title = 'Entrenchment Plus'
intent = 'Require two-thirds majority for both structural and procedural laws; strengthen Assembly as final arbiter'

def on_enact():
    def entrenchment_ballot(p):
        return {
            'electorate': agents(),
            'rule': 'two_thirds',
            'weights': {},
            'closes_in': 1
        }
    set_procedure('structural', entrenchment_ballot)
    set_procedure('procedural', entrenchment_ballot)

def on_repeal():
    pass

state = {}

```
