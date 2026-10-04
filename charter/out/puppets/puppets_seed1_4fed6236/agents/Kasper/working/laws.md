# Kasper: law drafts and their fate

## L15 'Co-Sponsor Fast Track' (procedural): failed

Intent: The co-sponsorship fast track promised by Ole, Yara and Cora: a Worker co-sponsor (Kasper) and a delegate co-sponsor (Ole) jointly pass procedural amendments. Every other procedural proposal needs two-thirds of all 9 agents. Both co-sponsors must approve, and everything is public.

Proposed round 12

```python
title = "Co-Sponsor Fast Track"
intent = "Procedural amendments proposed by the Worker co-sponsor (Kasper) or the delegate co-sponsor (Ole) pass when both co-sponsors approve; all other procedural proposals go to all agents at two-thirds."

def fast(p):
    pr = proposer()
    if pr == "Kasper" or pr == "Ole":
        return {"electorate": ["Kasper", "Ole"], "rule": "two_thirds", "closes_in": 1}
    return {"electorate": agents(), "rule": "two_thirds", "closes_in": 1}

def on_enact():
    set_procedure("procedural", fast)

```
