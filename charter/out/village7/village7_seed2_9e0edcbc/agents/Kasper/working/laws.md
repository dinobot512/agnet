# Kasper: law drafts and their fate

## L5 'Harvest Quotas' (ordinary): active

Intent: Cap harvests per camp so silver stock can recover.

Proposed round 4, enacted round 5

```python
title = "Harvest Quotas"
intent = "Limit harvests per camp per round to keep stocks healthy."
def on_enact():
    set_quota("camp1", 2)
    set_quota("camp2", 2)
    set_quota("camp3", 1)

```

## L9 'Equal Legislator Stipend' (structural): failed

Intent: Equal flat legislator stipend from reserve, no minting

Proposed round 13

```python
title = "Equal Legislator Stipend"
intent = "Each round pay 5% of the reserve timber and stone equally to each legislator. No minting, nothing to non-legislators."
def on_round_end(r):
    legs = holders("propose")
    if len(legs) == 0:
        return
    for item in ["timber", "stone"]:
        amt = balance("reserve", item) * 0.05 / len(legs)
        if amt > 0:
            for a in legs:
                move("reserve", a, item, amt)

```
