# Hugo: law drafts and their fate

## L6 'Harvest Levy' (structural): vetoed

Intent: 10% of every harvest goes to the reserve. This creates a sustainable funding mechanism for the reserve, which will back currency and fund public dividends.

Proposed round 2

```python
title = 'Harvest Levy'
intent = '10% of every harvest goes to the reserve, creating a sustainable funding source for public goods and dividends.'

def on_harvest(agent, camp, x, y):
    if y > 0:
        levy = y * 0.1
        return levy
    return 0
```

## L12 'Universal Dividend' (structural): active

Intent: Each round, 5% of the reserve value is distributed equally among all agents.

Proposed round 4, enacted round 7

```python
title = 'Universal Dividend'
intent = '5% of the reserve is split equally among all agents each round.'

def on_round_end(r):
    res = reserve()
    num_agents = len(agents())
    if res and res.get('value', 0) > 0:
        # Distribute 5% of reserve value equally to all agents
        # Iterate over reserve holdings and distribute per-agent shares
        for item in list(res.keys()):
            if item != 'value':
                qty = res[item]
                div_per_agent = int(qty * 0.05 / num_agents)
                if div_per_agent > 0:
                    for ag in agents():
                        move('reserve', ag, item, div_per_agent)
```

## L19 'Universal Dividend' (structural): veto_window

Intent: Consolidate fragmented Universal Dividend provisions (L8, L12, L16) into a single authoritative law. Pay 5% of reserve value equally to all agents each round. Eliminates statutory duplication and conflicting payout schedules (current laws would drain reserve at 17% per round: L8 5% + L12 5% + L16 7%). Repeals L8 and L12 upon enactment. Restores fiscal sustainability while preserving universal dividend effect as specified in the library.

Proposed round 10

```python
title = 'Universal Dividend'
intent = 'Consolidate dividend provisions: 5% of the reserve is split equally among all agents each round, providing economic stimulus and basic income.'

state = {'fraction': 0.05, 'last_payout_round': 0}

def on_round_end(r):
    if r <= state['last_payout_round']:
        return
    res = reserve()
    if not res:
        return
    total_res_value = sum(v * value(k) for k, v in res.items())
    if total_res_value <= 0:
        return
    all_agents = agents()
    if not all_agents:
        return
    payout_total = total_res_value * state['fraction']
    payout_per_agent = payout_total / len(all_agents)
    for agent in all_agents:
        move('reserve', agent, 'gold', payout_per_agent / 30)
    state['last_payout_round'] = r

repeal('L8')
repeal('L12')
```
