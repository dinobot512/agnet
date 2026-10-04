# Ada: law drafts and their fate

## L5 'Open Majority Procedure' (procedural): active

Intent: Let ordinary and structural laws pass by simple majority ballot of all agents within one round, so currency, levy and tribute laws can be enacted.

Proposed round 2, enacted round 5

```python
title = 'Open Majority Procedure'
intent = 'Ordinary and structural laws go to a one-round majority ballot of all agents.'

def proc(p):
    return {'electorate': agents(), 'rule': 'majority_voting', 'closes_in': 1}

def on_enact():
    set_procedure('structural', proc)
    set_procedure('ordinary', proc)

```
