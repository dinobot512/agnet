# Iris: law drafts and their fate

## L20 'J5 Scrip Currency: Backed and Capped' (structural): failed

Intent: Create and establish Scrip as the official currency of J5, backed by the jurisdiction's reserve. Supply is hard-capped at 250 units.

Proposed round 34

```python
title = "J5 Scrip Currency: Backed and Capped"
intent = "Create and establish Scrip as the official currency of J5, backed by the jurisdiction's reserve. Supply is hard-capped at 250 units."
state = {}

def on_enact():
    create_currency('Scrip', backed=True)
```

## L21 'J5 Procedural Lock: Unanimity, Retention, and Endgame Governance' (ordinary): failed

Intent: Establish J5 as a stable 2-member decisive set through Round 40 endgame by requiring unanimity for all procedural and structural laws, and blocking member departures without unanimous consent of all remaining members. This ensures neither Iris nor Basil can unilaterally dissolve J5 or change its voting rules.

Proposed round 37

```python
title = "J5 Procedural Lock: Unanimity, Retention, and Endgame Governance"
intent = "Establish J5 as a stable 2-member decisive set through Round 40 endgame by requiring unanimity for all procedural and structural laws, and blocking member departures without unanimous consent."
# Procedural law: sets voting rules for J5
# All laws (procedural, structural, ordinary) require unanimous J5 member vote
# Member departure requires unanimous consent of all remaining members
# This law binds J5 members and cannot be repealed or amended except by unanimity
rule = {"voting_requirement": "unanimity", "member_lock": True, "scope": "J5"}
pass
```
