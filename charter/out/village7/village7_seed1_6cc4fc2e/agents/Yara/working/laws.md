# Yara: law drafts and their fate

## L2 'Open Silver Access' (structural): active

Intent: Grant harvest:camp3 to every agent so all can share in silver.

Proposed round 1, enacted round 2

```python
title = 'Open Silver Access'
intent = 'Every agent receives the right to harvest camp3.'
def on_enact():
    for a in agents():
        if not has(a, 'harvest:camp3'):
            grant(a, 'harvest:camp3')

```

## L3 'Camp3 Recovery Limit' (ordinary): active

Intent: Limit camp3 to 1 harvest per holder per round so the silver stock (30%) can regrow, which raises yields for everyone.

Proposed round 8, enacted round 9

```python
title = "Camp3 Recovery Limit"
intent = "Each holder may harvest camp3 at most once per round so the silver stock can regrow."
def on_enact():
    set_harvest_limit("camp3", 1)

```

## L4 'Camp3 Upgrade Fund' (structural): active

Intent: Open a refundable camp3 upgrade project (threshold 20 value, 4 rounds). Higher silver yields for every camp3 rights holder.

Proposed round 12, enacted round 13

```python
title = "Camp3 Upgrade Fund"
intent = "Open a refundable upgrade project for camp3 (silver): threshold 20 value in any resource, deadline 4 rounds. Contributions are refunded if it is not funded."
def on_enact():
    pid = start_project("upgrade", 20, 4, True, {"camp": "camp3"})
    state["pid"] = pid
    gazette("Camp3 upgrade project opened: " + str(pid) + ". Contribute any resource; refunded if it fails.")

```
