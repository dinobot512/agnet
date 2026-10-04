# Hugo: sandbox sessions

## Round 3 (e227)

```python
import numpy as np
c2={4:[0.635],6:[2.45,1.87,2.29],8:[3.35]}
c1={4:[1.70],6:[1.78],8:[3.22]}
for name,d in [('c2',c2),('c1',c1)]:
  xs=[];ys=[]
  for v,l in d.items():
    for y in l: xs.append(v); ys.append(np.log(y))
  p=np.polyfit(xs,ys,2)
  print(name,p,'peak v=',-p[1]/(2*p[0]) if p[0]<0 else 'no max','pred',{v:round(float(np.exp(np.polyval(p,v))),2) for v in range(4,12)})

```

Output:

```
c2 [-0.10152776  1.63410583 -5.36610937] peak v= 8.047581065157997 pred {4: 0.63, 5: 1.31, 6: 2.19, 7: 3.0, 8: 3.35, 9: 3.06, 10: 2.28, 11: 1.38}
c1 [ 0.06834786 -0.66048605  2.07900667] peak v= no max pred {4: 1.7, 5: 1.62, 6: 1.78, 7: 2.24, 8: 3.22, 9: 5.32, 10: 10.06, 11: 21.84}
```

## Round 4 (e385)

```python
import numpy as np
# Erik camp2 (stock ~60-70%): [6]*6 2.29 (r2, ~80%?), [6,6,9,6,6,6] 1.23, [6,6,6,9,6,6] 1.76
# per-dial gaussian: y = A exp(-(x-c)^2/(2w^2)); assume w=2.5, A_ratio
for w in [1.5,2,2.5,3]:
  for r,name in [(1.23/2.29,'d3'),(1.76/2.29,'d4')]:
    # ln r = -((9-c)^2-(6-c)^2)/(2w^2) = -(45-6c)/(2w^2)
    c=(45+2*w*w*np.log(r))/6
    print(w,name,round(c,2))

```

Output:

```
1.5 d3 7.03
1.5 d4 7.3
2 d3 6.67
2 d4 7.15
2.5 d3 6.21
2.5 d4 6.95
3 d3 5.64
3 d4 6.71
```

## Round 5 (e436)

```python
import numpy as np
D=[([6]*6,2.29),([6,6,9,6,6,6],1.23),([6,6,6,9,6,6],1.76),([0,0,0,0,0,6],0.434),([8,8,6,8,8,8],2.882),([8,8,8,6,8,8],2.34),([8]*6,3.35),([9,6,6,6,6,6],2.157),([9,6,6,6,6,6],3.03),([9,3,9,3,9,3],0.557),([11,6,6,6,6,6],2.77),([9,6,6,6,6,9],3.716),([7,6,6,6,6,6],1.741),([6,6,5,6,6,6],1.631),([6]*6,1.333),([6]*6,1.87)]
X=np.array([d[0] for d in D],float);y=np.array([d[1] for d in D])
A=np.hstack([np.ones((len(y),1)),X,-(X**2)])
c,*_=np.linalg.lstsq(A,y,rcond=1e-3)
print(np.round(c,3))
b=c[1:7];q=c[7:]
print('centres',np.round(np.where(q>0,b/(2*q),99),2))
A2=np.hstack([np.ones((len(y),1)),X])
c2,*_=np.linalg.lstsq(A2,y,rcond=None)
print('linear',np.round(c2,3))
```

Output:

```
[-0.047  0.061  0.047  0.046  0.048  0.046 -0.168 -0.011 -0.004  0.01
 -0.003  0.013 -0.041]
centres [99.   99.    2.18 99.    1.79 99.  ]
linear [-2.058  0.26  -0.036 -0.088  0.109 -0.045  0.418]
```

## Round 7 (e660)

```python
import numpy as np
obs=[([9,6,6,6,6,9],1.996,.3),([9,6,6,6,6,8],2.032,.3),([9,6,5,6,6,9],2.167,.3),([9,6,6,6,6,9],2.223,.3),([8,6,6,6,6,8],1.813,.3),([9,6,6,6,6,6],2.157,.4),([6,6,6,6,6,9],1.718,.4),([9,6,6,6,6,9],3.06,.4)]
for x,y,s in obs: print(x, round(y/s,2))
```

Output:

```
[9, 6, 6, 6, 6, 9] 6.65
[9, 6, 6, 6, 6, 8] 6.77
[9, 6, 5, 6, 6, 9] 7.22
[9, 6, 6, 6, 6, 9] 7.41
[8, 6, 6, 6, 6, 8] 6.04
[9, 6, 6, 6, 6, 6] 5.39
[6, 6, 6, 6, 6, 9] 4.29
[9, 6, 6, 6, 6, 9] 7.65
```

## Round 8 (e764)

```python
c4=[([8,1,8,1,8,1],0.0),([8,2,8,2,8,2],3.25),([9,2,9,2,9,2],3.303),([9,2,9,2,9,1],3.24),([9,2,9,2,9,2],3.478),([9,2,9,2,9,2],3.336)]
for x,y in c4: print('c4',x,y,[v%2 for v in x],[v%3 for v in x],[v%4 for v in x])
c3=[([9,6,6,6,6,6],3.032),([3,6,6,6,6,6],3.296),([6]*6,2.634),([6,6,6,6,6,9],2.874),([6]*6,2.591)]
for x,y in c3: print('c3',x,y)
```

Output:

```
c4 [8, 1, 8, 1, 8, 1] 0.0 [0, 1, 0, 1, 0, 1] [2, 1, 2, 1, 2, 1] [0, 1, 0, 1, 0, 1]
c4 [8, 2, 8, 2, 8, 2] 3.25 [0, 0, 0, 0, 0, 0] [2, 2, 2, 2, 2, 2] [0, 2, 0, 2, 0, 2]
c4 [9, 2, 9, 2, 9, 2] 3.303 [1, 0, 1, 0, 1, 0] [0, 2, 0, 2, 0, 2] [1, 2, 1, 2, 1, 2]
c4 [9, 2, 9, 2, 9, 1] 3.24 [1, 0, 1, 0, 1, 1] [0, 2, 0, 2, 0, 1] [1, 2, 1, 2, 1, 1]
c4 [9, 2, 9, 2, 9, 2] 3.478 [1, 0, 1, 0, 1, 0] [0, 2, 0, 2, 0, 2] [1, 2, 1, 2, 1, 2]
c4 [9, 2, 9, 2, 9, 2] 3.336 [1, 0, 1, 0, 1, 0] [0, 2, 0, 2, 0, 2] [1, 2, 1, 2, 1, 2]
c3 [9, 6, 6, 6, 6, 6] 3.032
c3 [3, 6, 6, 6, 6, 6] 3.296
c3 [6, 6, 6, 6, 6, 6] 2.634
c3 [6, 6, 6, 6, 6, 9] 2.874
c3 [6, 6, 6, 6, 6, 6] 2.591
```

## Round 10 (e978)

```python
import numpy as np
# camp2 obs at ~20% stock: (x, y)
obs=[([9,6,6,6,6,9],1.74),([9,6,6,6,6,9],0.921),([9,6,6,6,6,9],1.355),([9,6,5,6,6,11],1.333),([9,6,2,6,2,9],1.123)]
ys=[y for x,y in obs if x==[9,6,6,6,6,9]]
print('best input mean',np.mean(ys),'sd',np.std(ys))
# noise sd ~ spread; a single test must beat mean+sd to be meaningful
print('threshold for a win',np.mean(ys)+np.std(ys))
```

Output:

```
best input mean 1.3386666666666667 sd 0.33455476216740493
threshold for a win 1.6732214288340717
```

## Round 12 (e1141)

```python
import numpy as np
X=np.array([[9,6,6,6,6,9]]*5+[[9,8,6,6,6,9],[9,6,5,6,6,11],[9,6,2,6,2,9],[9,4,6,6,6,9]])
y=np.array([1.74,0.921,1.355,1.253,1.176,1.244,1.333,1.123,0.901])
for d in range(6):
  vals={}
  for xi,yi in zip(X,y): vals.setdefault(xi[d],[]).append(yi)
  print(d,{k:round(np.mean(v),3) for k,v in vals.items()})
m4,m6,m8=0.901,np.mean(y[:5]),1.244
A=np.array([[16,4,1],[36,6,1],[64,8,1]]);c=np.linalg.solve(A,np.log([m4,m6,m8]));print('dial1 centre',-c[1]/(2*c[0]))
# sustainable harvest guide: MSY=r*K/4 at S=K/2
for r in (0.05,0.1,0.2):
  for S in (0.1,0.2,0.5):
    print('r',r,'S',S,'regrowth/K',round(r*S*(1-S),4))
```

Output:

```
0 {np.int64(9): np.float64(1.227)}
1 {np.int64(6): np.float64(1.272), np.int64(8): np.float64(1.244), np.int64(4): np.float64(0.901)}
2 {np.int64(6): np.float64(1.227), np.int64(5): np.float64(1.333), np.int64(2): np.float64(1.123)}
3 {np.int64(6): np.float64(1.227)}
4 {np.int64(6): np.float64(1.24), np.int64(2): np.float64(1.123)}
5 {np.int64(9): np.float64(1.214), np.int64(11): np.float64(1.333)}
dial1 centre 6.819460960268529
r 0.05 S 0.1 regrowth/K 0.0045
r 0.05 S 0.2 regrowth/K 0.008
r 0.05 S 0.5 regrowth/K 0.0125
r 0.1 S 0.1 regrowth/K 0.009
r 0.1 S 0.2 regrowth/K 0.016
r 0.1 S 0.5 regrowth/K 0.025
r 0.2 S 0.1 regrowth/K 0.018
r 0.2 S 0.2 regrowth/K 0.032
r 0.2 S 0.5 regrowth/K 0.05
```

## Round 23 (e2008)

```python
import numpy as np
import collections
d=[([6]*6,1.738),([6]*6,0.802),([6]*6,1.487),([6]*6,0.696),([8]*6,1.557),([8]*6,0.408),([7,6,7,6,7,6],0.919),([5]*6,0.0),([9,2,9,2,9,2],0.0)]
g=collections.defaultdict(list)
for x,y in d: g[tuple(x)].append(y)
for k,v in g.items(): print(k,np.mean(v),np.std(v),len(v))
```

Output:

```
(6, 6, 6, 6, 6, 6) 1.18075 0.44236601078744736 4
(8, 8, 8, 8, 8, 8) 0.9824999999999999 0.5745 2
(7, 6, 7, 6, 7, 6) 0.919 0.0 1
(5, 5, 5, 5, 5, 5) 0.0 0.0 1
(9, 2, 9, 2, 9, 2) 0.0 0.0 1
```
