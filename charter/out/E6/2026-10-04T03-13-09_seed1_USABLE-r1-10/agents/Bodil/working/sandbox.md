# Bodil: sandbox sessions

## Round 74 (e15667)

```python
import hashlib
def lz(h):
    b=int.from_bytes(h,'big');return 256-b.bit_length()
for r in (75,76,77):
    best=(0,None)
    for n in range(1500000):
        z=lz(hashlib.sha256(f'Frode|{r}|{n}'.encode()).digest())
        if z>best[0]: best=(z,n)
    print(r,best)

```

Output:

```
75 (21, 95901)
76 (24, 161074)
77 (23, 208127)
```

## Round 75 (e15977)

```python
import hashlib
def lz(h):
    b=int.from_bytes(h,'big');return 256-b.bit_length()
for name,rs in [('Disa',[76,77,78,79]),('Wim',[76,77,78,79]),('Frode',[78,79])]:
    for r in rs:
        best=(0,0)
        for n in range(110000):
            z=lz(hashlib.sha256(f'{name}|{r}|{n}'.encode()).digest())
            if z>best[0]: best=(z,n)
        print(name,r,best)
```

Output:

```
Disa 76 (15, 29593)
Disa 77 (20, 61058)
Disa 78 (15, 50472)
Disa 79 (20, 3577)
Wim 76 (16, 82495)
Wim 77 (17, 94973)
Wim 78 (17, 25100)
Wim 79 (17, 26858)
Frode 78 (18, 14033)
Frode 79 (19, 68304)
```

## Round 77 (e16802)

```python
import hashlib
def lz(s):
    h=hashlib.sha256(s.encode()).digest();n=0
    for b in h:
        if b==0:
            n+=8;continue
        n+=8-b.bit_length();break
    return n
for f in ['{a}|{r}|{n}','{a}|{r}|[{n}]','{a}|{r}|{n},','{a}|{r}|({n},)']:
    print(f,[lz(f.format(a=a,r=r,n=n)) for a,r,n in [('Disa',76,29593),('Wim',76,92847),('Wim',76,82495),('Disa',77,61058)]])
for a in ['Disa','Wim','Frode']:
    for r in [78,79]:
        best=(0,0)
        for n in range(150000):
            v=lz(a+'|'+str(r)+'|['+str(n)+']')
            if v>best[0]: best=(v,n)
        print('bracket',a,r,best)

```

Output:

```
{a}|{r}|{n} [15, 4, 16, 20]
{a}|{r}|[{n}] [0, 2, 1, 0]
{a}|{r}|{n}, [4, 1, 0, 0]
{a}|{r}|({n},) [1, 0, 0, 2]
bracket Disa 78 (17, 76555)
bracket Disa 79 (17, 142468)
bracket Wim 78 (21, 38237)
bracket Wim 79 (19, 125045)
bracket Frode 78 (15, 126159)
bracket Frode 79 (18, 19906)
```

## Round 78 (e17113)

```python
import hashlib
def lz(s):
    h=hashlib.sha256(s.encode()).digest();n=0
    for b in h:
        if b==0: n+=8; continue
        n+=8-b.bit_length(); break
    return n
for a in ['Disa','Wim']:
    for fmt in ['{a}|{r}|[{n}]','{a}|{r}|{n}']:
        best=(0,0)
        for n in range(150000):
            z=lz(fmt.format(a=a,r=80,n=n))
            if z>best[0]: best=(z,n)
        print(a,fmt,80,best)
```

Output:

```
Disa {a}|{r}|[{n}] 80 (17, 22699)
Disa {a}|{r}|{n} 80 (16, 59396)
Wim {a}|{r}|[{n}] 80 (15, 76944)
Wim {a}|{r}|{n} 80 (16, 46324)
```
