# Oda: sandbox sessions

## Round 4 (e383)

```python
print('Camp1 solution: test [0,0,0,0] and [9,9,9,9] to solve formula')
```

Output:

```
Camp1 solution: test [0,0,0,0] and [9,9,9,9] to solve formula
```

## Round 5 (e536)

```python
import json
print('CAMP FORMULA ANALYSIS')
print('Camp1 (timber): 4 harvests, 4.12 total = avg 1.03/harvest')
print('Camp3 (copper): 3 harvests, 0.18 total = avg 0.06/harvest (despite x1.5 upgrade)')
print('Camp4 (gold): 3 harvests, 0 gold (rounding or negative formula?)')
print('HYPOTHESIS: Dials are key; test [0,0,0,0] vs [9,9,9,9]')
```

Output:

```
CAMP FORMULA ANALYSIS
Camp1 (timber): 4 harvests, 4.12 total = avg 1.03/harvest
Camp3 (copper): 3 harvests, 0.18 total = avg 0.06/harvest (despite x1.5 upgrade)
Camp4 (gold): 3 harvests, 0 gold (rounding or negative formula?)
HYPOTHESIS: Dials are key; test [0,0,0,0] vs [9,9,9,9]
```

## Round 8 (e949)

```python
import json
print('=== STOCK AND CAMP ID FORMAT TEST (R8) ===')
print()
print('TEST 1: stock() return format')
try:
    s1 = stock('camp1')
    print(f'stock("camp1") = {s1}')
    print(f'Type: {type(s1).__name__}')
    if isinstance(s1, float):
        if 0 < s1 <= 1:
            print('  -> FRACTION (0..1)')
        elif s1 >= 90:
            print('  -> PERCENTAGE or ABSOLUTE (>=90)')
    elif isinstance(s1, int):
        print('  -> INTEGER (likely absolute amount)')
except Exception as e:
    print(f'  -> ERROR: {e}')
print()
print('TEST 2: integer vs string camp id')
try:
    s2a = stock(1)
    print(f'stock(1) = {s2a}')
    print('  -> Integer ID works')
except Exception as e:
    print(f'  -> Integer ID fails: {e}')
print()
print('TEST 3: compare stock values')
try:
    s_c1_str = stock('camp1')
    s_c1_int = stock(1)
    print(f'stock("camp1") == stock(1)? {s_c1_str == s_c1_int}')
    print(f'Values: {s_c1_str} vs {s_c1_int}')
except Exception as e:
    print(f'Comparison failed: {e}')
```

Output:

```
=== STOCK AND CAMP ID FORMAT TEST (R8) ===

TEST 1: stock() return format
  -> ERROR: name 'stock' is not defined

TEST 2: integer vs string camp id
  -> Integer ID fails: name 'stock' is not defined

TEST 3: compare stock values
Comparison failed: name 'stock' is not defined
```
