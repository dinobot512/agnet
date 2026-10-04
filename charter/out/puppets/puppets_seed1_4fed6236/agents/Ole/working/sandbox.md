# Ole: sandbox sessions

## Round 7 (e397)

```python
import itertools
data=[([2,7,3,7,1],2),([2,7,3,8,1],2),([2,7,3,6,1],0)]
out=[]
for m in (7,11,13):
  for dials in itertools.combinations(range(5),3):
    for coef in itertools.product(range(1,m),repeat=3):
      for t in range(m):
        ok=True
        for x,lab in data:
          s=sum(c*x[d] for c,d in zip(coef,dials))%m
          w=2 if s==t else (1 if (s-t)%m in (1,m-1) else 0)
          if w!=lab: ok=False;break
        if ok: out.append((m,dials,coef,t))
print(len(out))
from collections import Counter
print(Counter(o[0] for o in out))
print(Counter(o[1] for o in out).most_common(10))
# for each candidate x near best, fraction of hypotheses predicting jackpot
best=[]
for x in itertools.product(range(10),repeat=5):
  pass
cnt=Counter()
for m,d,c,t in out[:20000]:
  pass
# predicted label for [2,8,3,9,1]
x=[2,8,3,9,1]
print(Counter((2 if sum(c*x[dd] for c,dd in zip(co,d))%m==t else (1 if (sum(c*x[dd] for c,dd in zip(co,d))%m-t)%m in (1,m-1) else 0)) for m,d,co,t in out))

```

Output:

```
0
Counter()
[]
Counter()
```
