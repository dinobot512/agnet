# Rhea: sandbox sessions

## Round 17 (e2676)

```python
def sel(names,r):
    n=len(names)
    return [names[(r+i)%n] for i in range(4)]
m=sorted(['Cleo','Disa','Vidar','Gaia','Bram','Dmitri','Finn','Gry','Goran','Hanne','Quin','Sven'])
for r in range(17,23): print(r, sel(m,r))
print(sel(['A','B'],5))
try:
    sel([],3)
except Exception as e: print('empty:',e)

```

Output:

```
17 ['Gaia', 'Goran', 'Gry', 'Hanne']
18 ['Goran', 'Gry', 'Hanne', 'Quin']
19 ['Gry', 'Hanne', 'Quin', 'Sven']
20 ['Hanne', 'Quin', 'Sven', 'Vidar']
21 ['Quin', 'Sven', 'Vidar', 'Bram']
22 ['Sven', 'Vidar', 'Bram', 'Cleo']
['B', 'A', 'B', 'A']
empty: integer modulo by zero
```
