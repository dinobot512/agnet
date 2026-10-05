# Abel: law drafts and their fate

## L3 'Bribery Disclosure' (ordinary): active

Intent: Every transfer to a Legislator, Board member or the Fixer is published.

Proposed round 3, enacted round 4

```python
title = 'Bribery Disclosure'
intent = 'Every transfer to a Legislator, Board member or the Fixer is published.'

def on_transfer(src,dst,item,qty):
  r=rights_of(dst)
  if 'vote' in r or 'veto' in r or 'fix' in r or 'propose' in r:
    gazette(src+' transferred '+str(qty)+' '+item+' to '+dst)
  return 0

```

## L4 'Broad Franchise' (procedural): active

Intent: All agents of J0 vote on ordinary laws by simple majority; no new veto or agenda powers.

Proposed round 5, enacted round 8

```python
title = "Broad Franchise"
intent = "Every member of J0 may propose and vote on ordinary laws, which pass by simple majority of all members."

def ordinary_proc(p):
    return {"electorate": members(), "rule": "majority", "closes_in": 1}

def give():
    for a in members():
        if not has(a, 'propose'):
            grant(a, 'propose')
        if not has(a, 'vote'):
            grant(a, 'vote')

def on_enact():
    set_procedure('ordinary', ordinary_proc)
    give()

def on_round_start(r):
    give()

```

## L6 'Tribute From Reserve' (structural): vetoed

Intent: Pay tribute T1 from the reserve: move reserve timber and stone to the outside power before round 13 ends.

Proposed round 12

```python
title = 'Tribute From Reserve'
intent = 'Pay tribute T1 from the reserve.'

def on_enact():
    r = reserve()
    for k in r:
        q = r[k]
        if q > 0:
            move('reserve', 'tribute', k, q)

```

## L10 'T2 Reserve Payment' (structural): active

Intent: Pay the open tribute demand from the reserve, capped at the amount due and at reserve holdings. No mint, no procedure change.

Proposed round 17, enacted round 20

```python
title = "T2 Reserve Payment"
intent = "Pay the outstanding tribute from the reserve, capped at the amount due, timber first then stone, so no tribute goes unpaid while the reserve can cover it."

def pay():
    if state.get("t3_paid"):
        return
    left = 143
    res = reserve()
    for item in ["timber", "stone"]:
        if left <= 0:
            break
        v = value(item)
        if v <= 0:
            continue
        have = res.get(item, 0)
        q = min(have, int(left / v) + 1)
        if q > 0:
            pay_tribute(item, q)
            left = left - q * v
    state["t3_paid"] = True

def on_round_start(r):
    pay()

def on_round_end(r):
    pay()

```
