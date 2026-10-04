# Celia: law drafts and their fate

## L4 'Open Data' (ordinary): failed

Intent: Every harvest's input and yield is published in the gazette.

Proposed round 1

```python
title = "Open Data"
intent = "Every harvest's input and yield is published in the gazette."
def on_harvest(agent, camp, x, y):
    gazette(agent + " harvested " + camp + " x=" + str(x) + " yield=" + str(y))
    return 0

```
