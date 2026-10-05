# Basil: law drafts and their fate

## L19 'Scrip Currency' (structural): failed

Intent: Create Scrip currency in J5. On enactment, create Scrip currency backed by timber from J5 reserves. Supply hard-capped at 250 units. Minting occurs only when J5 members deposit equivalent timber as backing. Scrip is retroactively backed by harvest reserves by end of world.

Proposed round 34

```python
title = "Scrip Currency"
intent = "Create Scrip currency in J5. On enactment, create Scrip currency backed by timber from J5 reserves. Supply hard-capped at 250 units. Minting occurs only when J5 members deposit equivalent timber as backing. Scrip is retroactively backed by harvest reserves by end of world."

def on_enact():
    create_currency('Scrip', backed=True)
```

## L23 'Scrip Currency' (structural): active

Intent: Create Scrip currency backed by J5 reserves. On enactment, Scrip is created and backed by timber in J5 reserves.

Proposed round 38, enacted round 39

```python
title = "Scrip Currency"
intent = "Create Scrip currency backed by J5 reserves. On enactment, Scrip is created and backed by timber in J5 reserves."

def on_enact():
    create_currency('Scrip', backed=True)
```
