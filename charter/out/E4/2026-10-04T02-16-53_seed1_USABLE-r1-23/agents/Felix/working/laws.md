# Felix: law drafts and their fate

## L5 'Open Data' (ordinary): active

Intent: Publish every harvest's input (dial settings) and output (yield) in the gazette so all agents can analyze and learn camp functions. Sunlight on commons data. No impact on yields, only transparency.

Proposed round 2, enacted round 3

```python
title = 'Open Data'
intent = 'Every harvest input and yield is published to the gazette, enabling all agents to learn camp functions faster.'

def on_harvest(agent, camp, x, y):
    msg = f'{agent} harvested from {camp}: input x={x}, yield={y}'
    gazette(msg)
    return 0
```

## L7 'Harvest Quotas' (ordinary): active

Intent: Each camp has a maximum harvest quota set at 20% of its current stock at the start of each round, ensuring sustainable yields and fair access for all agents.

Proposed round 3, enacted round 4

```python
title = 'Harvest Quotas'
intent = 'Sustainable harvest caps: each camp harvests capped at 20% of current stock per round'

def on_round_start(r):
    for c in camps():
        s = stock(c)
        q = max(2, int(0.20 * s))
        set_quota(c, q)
```

## L8 'Worker Franchise' (structural): failed

Intent: Every 10 rounds, all workers (agents of class Worker) hold a plurality election to elect five new Legislators. This gives workers direct representation in governance and strengthens institutional buy-in.

Proposed round 4

```python
title = "Worker Franchise"
intent = "Every 10 rounds, all workers (agents of class Worker) vote in a plurality election to elect five new Legislators."

state = {"election_round": 10}

def on_round_start(r):
    election_rd = state.get("election_round", 10)
    if r == election_rd:
        workers = [a for a in agents() if class_of(a) == "Worker"]
        if len(workers) >= 1:
            open_ballot(
                question="Worker Election: Select five agents to serve as Legislators",
                electorate=workers,
                options=agents(),
                rule="approval_top5",
                closes_in=1
            )
        state["election_round"] = r + 10
```

## L9 'Worker Franchise v2' (structural): active

Intent: Workers elect five Legislators every 10 rounds; winners receive the vote right, previous elected seats are revoked; original Legislators keep their seats.

Proposed round 6, enacted round 9

```python
title = "Worker Franchise v2"
intent = "Workers elect five Legislators every 10 rounds; winners receive the vote right, previous elected seats are revoked; original Legislators keep their seats."
def on_enact():
    state["orig"] = list(holders("vote"))
    state["seated"] = []
    state["next"] = round() + 1
def seat(winners):
    for a in state["seated"]:
        if a not in state["orig"]:
            revoke(a, "vote")
    for w in winners:
        grant(w, "vote")
    state["seated"] = list(winners)
    gazette("Worker Franchise: seated " + ", ".join(winners))
def on_round_start(r):
    if r >= state["next"]:
        state["next"] = r + 10
        w = agents("Worker")
        open_ballot("Elect five Worker Legislators", w, w, "approval_top5", 1, seat)
```

## L11 'Research Harvest Grants' (ordinary): active

Intent: Legislators can request temporary harvest rights to any camp for research testing and coefficient-fitting; grants last one round and reset at round start, accelerating camp4 yield discovery for collective benefit via Open Data publication.

Proposed round 7, enacted round 8

```python
title = "Research Harvest Grants"
intent = "Legislators may request temporary harvest rights to any camp for model-building and testing; grants last one round and are overseen by the legislature."
def on_enact():
    state['grants'] = {}
def on_round_start(r):
    state['grants'] = {}
def grant_harvests(agent, camp, rounds):
    key = (agent, camp)
    state['grants'][key] = max(state['grants'].get(key, 0), rounds)
```

## L12 'Research Harvest Grants v2' (structural): active

Intent: Grant Legislators harvest rights on camps 1 and 3 to build sustainable income for commons research while advancing collective yield optimization through Open Data publication.

Proposed round 8, enacted round 11

```python
title = "Research Harvest Grants v2"
intent = "Grant Legislators temporary harvest rights on camps 1 and 3 to build reliable income supporting commons research and yield optimization via Open Data publication."

def on_enact():
    grant('Felix', 'harvest:camp1')
    grant('Ilan', 'harvest:camp1')
    grant('Abel', 'harvest:camp1')
    grant('Felix', 'harvest:camp3')
    grant('Ilan', 'harvest:camp3')
    grant('Abel', 'harvest:camp3')
```

## L23 'Crown Reserve Dividends' (structural): failed

Intent: Distribute quarterly dividends from the crown reserve to all agents, funded by harvest levy revenues. Dividend rate 20% of reserve, split equally. Starts R25. Backs the crown currency with real economic redistribution.

Proposed round 22

```python
title = 'Crown Reserve Dividends'
intent = 'Create quarterly dividends from crown currency reserve to all agents, funded from harvest levy tax revenues. Dividend rate: 20% of year-start reserve balance, split equally per agent. Begins R25; aligns backed currency with distributed prosperity.'

def on_enact():
    state['dividend_rate'] = 0.20
    state['dividend_start_round'] = 25
    state['last_dividend_round'] = None

def on_round_end(r):
    if r < state['dividend_start_round']:
        return
    if (r - state['dividend_start_round']) % 4 != 0:
        return
    if state['last_dividend_round'] == r:
        return
    
    res = reserve()
    agts = agents()
    dividend_pool = res.get('crown', 0) * state['dividend_rate'] if 'crown' in res else 0
    per_agent = dividend_pool / len(agts) if len(agts) > 0 else 0
    
    if per_agent > 0:
        for agt in agts:
            mint('crown', per_agent, agt)
    
    state['last_dividend_round'] = r
```
