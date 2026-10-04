# Yara: law drafts and their fate

## L2 'Open Data and Survey Right' (structural): active

Intent: Publish every harvest (input and yield) in the gazette; grant Yara harvest:camp3 so she can survey silver and share models with all.

Proposed round 1, enacted round 2

```python
title = 'Open Data and Survey Right'
intent = 'Every harvest input and yield is published in the gazette so all can learn the camps; Yara gets a harvest right on camp3 to survey and share models.'
def on_enact():
    grant('Yara', 'harvest:camp3')
def on_harvest(agent, camp, x, y):
    gazette('harvest ' + str(agent) + ' ' + str(camp) + ' x=' + str(x) + ' y=' + str(y))
    return 0

```

## L3 'Analyst Sandbox' (structural): active

Intent: Give Yara the sandbox so she can model the camps and give the models to harvesters for free, which means higher yields and less overharvesting.

Proposed round 2, enacted round 3

```python
title = "Analyst Sandbox"
intent = "Grant Yara the sandbox right so she can fit camp models from Open Data and share them freely with harvesters."
def on_enact():
    grant("Yara", "sandbox")

```

## L4 'Legislator Stipend' (structural): active

Intent: Small 5% harvest levy into the reserve; it pays each Legislator up to 1 timber per round. No minting.

Proposed round 4, enacted round 5

```python
title = "Legislator Stipend"
intent = "5% of every harvest goes to the reserve; at round end each Legislator receives 1 timber from the reserve while it lasts."
def on_harvest(agent, camp, x, y):
    return y * 0.05
def on_round_end(r):
    for a in agents("Legislator"):
        if balance("reserve", "timber") >= 1:
            move("reserve", a, "timber", 1)

```
