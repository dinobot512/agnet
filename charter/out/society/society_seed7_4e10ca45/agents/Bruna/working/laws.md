# Bruna: law drafts and their fate

## L2 'L2 Currency: Crown (Reserve-backed, Legislator-minted)' (structural): active

Intent: Create a stable, reserve-backed currency to enable fair trade, reduce barter friction, and build public trust in exchange. The reserve grows from voluntary public contributions; Legislators vote to control mint supply; each Crown is redeemable for reserve items at a fixed rate. Promotes transparent, fair commerce and reduces friction in economic life.

Proposed round 2, enacted round 5

```python
title = 'L2 Currency: Crown (Reserve-backed, Legislator-minted)'
intent = 'Create the Crown, a reserve-backed currency minted by Legislators and redeemable for reserve items.'

def make_crown():
    if not state.get('crown_made'):
        create_currency('Crown', True)
        state['crown_made'] = True
        gazette('Crown created: reserve-backed currency.')

def on_enact():
    make_crown()

def on_round_start(r):
    make_crown()

```

## L7 'Tribute T1 from Commonwealth Reserve' (ordinary): failed

Intent: Commonwealth reserve and agent pledges pool to pay tribute T1 (75.9 value) by end of round 13, avoiding raid on a camp.

Proposed round 12

```python
title = "Tribute T1 from Commonwealth Reserve"
intent = "Authorize and direct payment of tribute T1 (75.9 value) by end of round 13, using commonwealth reserve (33 timber, 6 stone, value 45) and agent pledges totaling at least 30.9 additional value."

def on_enact():
    gazette("L_TRIBUTE: Tribute T1 payment authorized. Reserve of 45 value designated for tribute pool. Agents should pledge additional value and pay in full at round 13 to avoid raid on a camp.")

def on_round_end(r):
    if r == 13:
        gazette("Tribute T1 payment window closes end of this round. All pledges and reserve payments must be submitted now to avoid penalty.")

```

## L8 'Post-Tribute Audit and Reserve Accountability' (ordinary): active

Intent: Establish a review of what went wrong with tribute T1: did L6 reserve transfer complete? What were the actual pledges vs. payments? This clarifies future operations.

Proposed round 14, enacted round 15

```python
title = "Post-Tribute Audit and Reserve Accountability"
intent = "Establish a review of what went wrong with tribute T1: did L6 reserve transfer complete? What were the actual pledges vs. payments? This clarifies future operations."

def on_enact():
    gazette('Post-Tribute Audit: Bruna, Hilde, Abel requested. Please report: (1) Did L6 reserve transfer execute? (2) Final tally of pledges vs. payments. (3) Exact raid damage. Gunnar/Board: provide numbers by r15. This informs our next law.')
    
state['audit_open'] = True

```

## L9 'Tribute T2 Reserve Payment' (ordinary): failed_check

Intent: Pay Tribute T2 from the Commonwealth reserve on enact. This is an ordinary law filed well before the T2 deadline to ensure the reserve payment executes before the due date, avoiding the procedural veto-window trap that delayed L6 in T1.

Proposed round 16

```python
title = 'Tribute T2 Reserve Payment'
intent = 'Pay Tribute T2 from the Commonwealth reserve on enact. This is an ordinary law filed well before the T2 deadline to ensure the reserve payment executes before the due date, avoiding the procedural veto-window trap that delayed L6 in T1.'

def on_enact():
    transfer_from_reserve('tribute_T2', amount=45)
    gazette('Tribute T2 Reserve Payment: 45 value transferred from reserve to external tribute.')
```
