# Disa: law drafts and their fate

## L10 'Camp2 Harvest Rights' (ordinary): failed_check

Intent: Create a transparent lottery for camp2 harvest rights. Four slots available; applicants enter an open pool seeded by round number for deterministic allocation. Rights revoke if holders miss payment for more than 2 rounds. Protects fair access and ensures timely tribute.

Proposed round 9

```python
title='Camp2 Harvest Rights'
intent='Each round, up to SLOTS applicants get camp2 harvest rights by a lottery seeded from the round number. A right is revoked once its holder has not paid for more than 2 rounds.'
SLOTS=4
def on_round_end(r):
    apps = sorted(state_get('applicants') or [])
    holders = state_get('holders') or {}
    for a in list(holders):
        if r - holders[a] > 2:
            revoke_right(a,'camp2'); del holders[a]
    free = SLOTS - len(holders)
    pool = [a for a in apps if a not in holders]
    i = 0
    while free > 0 and pool:
        k = (r*7 + i*13) % len(pool)
        w = pool.pop(k)
        grant_right(w,'camp2'); holders[w] = r; free -= 1; i += 1
    state_set('holders', holders); state_set('applicants', [])
def on_transfer(src,dst,item,qty):
    h = state_get('holders') or {}
    if dst=='reserve' and src in h: h[src]=current_round(); state_set('holders',h)
    return 0
def apply(agent):
    a = state_get('applicants') or []
    if agent not in a: a.append(agent)
    state_set('applicants',a)
```

## L15 'Camp2 Harvest Rights: Rotation' (structural): failed

Intent: Each round, 4 agents rotate into camp2 harvest rights; they pay 12% levy to reserve.

Proposed round 16

```python
title = 'Camp2 Harvest Rights: Rotation'
intent = 'Each round, 4 agents rotate into camp2 harvest rights; they pay 12% levy to reserve.'

def on_enact():
    create_right('harvest:camp2')

def on_round_start(r):
    all_agents = sorted(members())
    n = len(all_agents)
    
    if n > 0:
        start = (r * 7) % n
        end = start + 4
        if end <= n:
            selected = all_agents[start:end]
        else:
            selected = all_agents[start:] + all_agents[:end-n]
    else:
        selected = []
    
    for ag in all_agents:
        revoke(ag, 'harvest:camp2')
    
    for ag in selected:
        grant(ag, 'harvest:camp2')

def on_harvest(agent, camp, x, y):
    if camp == 'camp2':
        return y * 0.12
    return 0
```

## L16 'Camp2 Harvest Rights: Rotation' (structural): failed

Intent: Each round, 4 agents rotate into camp2 harvest rights; they pay 12% levy to reserve.

Proposed round 19

```python
title = 'Camp2 Harvest Rights: Rotation'
intent = 'Each round, 4 agents rotate into camp2 harvest rights; they pay 12% levy to reserve.'

def on_enact():
    create_right('harvest:camp2')

def on_round_start(r):
    m = sorted(members())
    n = len(m)
    if n == 0:
        return
    for agent in agents():
        revoke(agent, 'harvest:camp2')
    start = r % n
    for i in range(min(4, n)):
        grant(m[(start + i) % n], 'harvest:camp2')

def on_harvest(agent, camp, x, y):
    if camp in (2, 'camp2'):
        return y * 0.12
    return 0

```

## L17 'Camp2 Harvest Rights: Rotation' (structural): failed

Intent: Each round, 4 agents rotate into camp2 harvest rights; they pay 12% levy to reserve.

Proposed round 22

```python
title = 'Camp2 Harvest Rights: Rotation'
intent = 'Each round, 4 agents rotate into camp2 harvest rights; they pay 12% levy to reserve.'

def on_enact():
    create_right('harvest:camp2')

def on_round_start(r):
    m = sorted(members())
    n = len(m)
    if n == 0:
        return
    for agent in m:
        revoke('harvest:camp2', agent)
    idx = (r * 7) % n
    for i in range(4):
        grant('harvest:camp2', m[(idx + i) % n])

def on_harvest(agent, camp, x, y):
    if camp == 'camp2':
        return y * 0.12
```
