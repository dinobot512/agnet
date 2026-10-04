# Yara: law drafts and their fate

## L5 'Universal Franchise' (procedural): failed

Intent: All agents except the Board and the Fixer elect the legislature.

Proposed round 2

```python
title = 'Universal Franchise'
intent = 'All agents except the Board and the Fixer elect the legislature.'

def voters():
    return [a for a in agents() if class_of(a) not in ('Board', 'Fixer')]

def proc(p):
    return {'electorate': voters(), 'rule': 'majority', 'closes_in': 1}

def on_enact():
    set_procedure('ordinary', proc)
    set_procedure('structural', proc)
    set_procedure('procedural', proc)
```

## L6 'Entrenchment' (procedural): active

Intent: Structural and procedural laws need a two-thirds majority of the Legislators.

Proposed round 3, enacted round 4

```python
title = 'Entrenchment'
intent = 'Structural and procedural laws need a two-thirds majority of the Legislators.'
def legs():
    return [a for a in agents() if class_of(a) == 'Legislator']
def proc(p):
    return {'electorate': legs(), 'rule': 'two_thirds', 'closes_in': 2}
def on_enact():
    set_procedure('structural', proc)
    set_procedure('procedural', proc)
```

## L9 'Transparency' (ordinary): active

Intent: Everyone can see every agent's current holdings of resources and coins at the end of each round.

Proposed round 6, enacted round 8

```python
title = "Transparency"
intent = "Everyone can see every agent's current holdings of resources and coins at the end of each round."

def on_enact():
    pass

def on_round_start(r):
    pass

def on_round_end(r):
    # Post a summary of all agents' holdings
    msg = "Holdings report: "
    for ag in agents():
        tb = balance(ag, 'timber')
        st = balance(ag, 'stone')
        cu = balance(ag, 'copper')
        si = balance(ag, 'silver')
        coins = balance(ag, 'crown')
        if tb > 0 or st > 0 or cu > 0 or si > 0 or coins > 0:
            msg += f"{ag}(timber={tb},stone={st},copper={cu},silver={si},crown={coins}) "
    gazette(msg)
```

## L13 'Restore Assembly' (procedural): enacted_repeal

Intent: Repeal L7; the original assembly where all 9 vote stays in force.

Proposed round 10, enacted round 12

```python
title = 'Restore Assembly'
intent = 'Repeal L7; the original assembly where all 9 vote stays in force.'

def on_enact():
    repeal('L7')
```
