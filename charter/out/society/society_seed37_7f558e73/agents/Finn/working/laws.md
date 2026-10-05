# Finn: law drafts and their fate

## L4 'Open Data' (ordinary): active

Intent: Publish each harvest's input and yield to the gazette; nothing else.

Proposed round 5, enacted round 6

```python
title = "Open Data"
intent = "Publish each harvest's input and yield to the gazette; nothing else."
def on_harvest(agent, camp, x, y):
    gazette("harvest: " + str(agent) + " at " + str(camp) + " input " + str(x) + " yield " + str(y))
    return 0

```
