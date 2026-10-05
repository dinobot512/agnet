# Yara: law drafts and their fate

## L22 'J7 Camp3 Harvest Pooling Agreement' (ordinary): failed

Intent: Record and coordinate J7 members' camp3 harvest extraction to protect stock sustainability and fair yield distribution.

Proposed round 38

```python
title = "J7 Camp3 Harvest Pooling Agreement"
intent = "Record and coordinate J7 members' camp3 harvest extraction to protect stock sustainability and fair yield distribution."

state['pooling_target'] = 0.08
state['members_list'] = list(members())

def on_round_end(r):
    gazette(f"J7 camp3 pooling active round {r}")
```
