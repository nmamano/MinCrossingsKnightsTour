"""Light independent checks for Claim 25; no worker imports or solvers."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

def edge(a, b):
    return tuple(sorted((a, b)))

def field(k, lo=-8, hi=16, shift=0, cheap=False):
    out = set()
    for y in range(lo, hi):
        for x in range(k):
            out.add(edge((x, y), (x+2, y-1)))
        if cheap or (y-shift) % 4 != 3:
            out.add(edge((1, y), (0, y+2)))
        if not cheap and (y-shift) % 4 == 1:
            out.add(edge((0, y), (1, y+2)))
    return out

def cross(e, f):
    def det(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    a, b = e
    c, d = f
    return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

def forest(edges):
    parent = {}
    def root(a):
        while a in parent:
            a = parent[a]
        return a
    for a, b in edges:
        a, b = root(a), root(b)
        assert a != b
        parent[a] = b

terms = [((0,-1),(1,1),-1), ((0,0),(1,-2),-1),
         ((0,0),(2,-1),-1), ((0,1),(1,-1),1),
         ((0,1),(2,0),1), ((0,2),(1,0),-1),
         ((1,0),(2,2),-1), ((1,1),(2,-1),-1)]

def data(edges, y, sign, phase):
    def tr(p):
        return (p[0], y+sign*p[1])
    f = sum(c for a,b,c in terms if edge(tr(a),tr(b)) in edges) % 3
    exc = all(edge(tr(a),tr(b)) in edges for a,b in
              [((0,0),(2,1)), ((0,1),(2,0))])
    c = (-1)**((y+phase) % 2)
    h = ((1+c)//2+c*(f+2)) % 3
    t = 2 if exc else (1,2,0)[h]
    return (f, exc, h, t)

# Fractional penalty is bounded by the audited oriented failure flag.
for f, exc, parity in product(range(3), (0,1), (0,1)):
    c = 1-2*parity
    h = ((1+c)//2+c*(f+2)) % 3
    t = 2 if exc else (1,2,0)[h]
    assert t <= 2*int(exc or f != 2)

out = {'date':'2026-10-03', 'dominance_cases':12, 'widths':[]}
for k in range(2,9):
    e = field(k)
    forest(e)
    deg = Counter(p for q in e for p in q)
    for x,y in product(range(k+2),range(4)):
        assert deg[x,y] == (2 if x < k else 1)
    assert all(sorted((abs(a[0]-b[0]),abs(a[1]-b[1]))) == [1,2]
               for a,b in e)
    crossings = [pair for pair in combinations(e,2)
                 if 0 <= max(min(p[1] for p in q) for q in pair) < 4
                 and cross(*pair)]
    assert len(crossings) == 8
    assert sum(cross(a,b) for a,b in combinations(field(k, cheap=True),2)
               if 0 <= max(min(p[1] for p in a),min(p[1] for p in b)) < 4) == 4
    for sign, phase in product((1,-1),(0,1)):
        # Translating the field by one row handles the other fixed parity.
        shift = phase if sign == 1 else 1-phase
        q = field(k, shift=shift)
        assert all(data(q,y,sign,phase)[1:] == (False,1,2) for y in range(4))
        assert all(data(field(k,cheap=True),y,sign,phase)[1:] == (False,2,0)
                   for y in range(4))
    out['widths'].append({'k':k,'crossings_per_period':len(crossings),
                          'all_orientation_parity_cases':'PASS'})

# Short caps make both translates reachable from an empty scan.
for shift in (0,1):
    e = {q for q in field(2,lo=-4,hi=24,shift=shift)
         if min(p[1] for p in q)>=0}
    remove = [((1,2),(0,4))]
    add = [((0,0),(2,1)), ((0,0),(1,2)),
           ((0,4),(2,5)), ((1,0),(2,2))]
    if shift:
        remove.append(((1,3),(0,5)))
        add += [((1,0),(3,1)), ((0,1),(1,3)), ((0,5),(2,6))]
    for a,b in remove:
        e.remove(edge(a,b))
    for a,b in add:
        e.add(edge(a,b))
    forest(e)
    deg = Counter(p for q in e for p in q)
    for x,y in product(range(4),range(20)):
        assert deg[x,y] == 2 if x<2 else deg[x,y] <= 2
    assert all(sorted((abs(a[0]-b[0]),abs(a[1]-b[1]))) == [1,2] for a,b in e)
out['empty_start_caps'] = 'PASS: both translates; only rows 0..6 changed'

# Cheap patterns force the average penalty at residue 2 to be <=0.
# Summing the two loss inequalities a_c(1)+a_c(2)>=1 then gives
# average penalty at residue 1 >=1. This argument even permits signed tables.
out['additive_table_proof'] = [
    'a_even(2)+a_odd(2) <= 0',
    'a_even(1)+a_even(2) >= 1',
    'a_odd(1)+a_odd(2) >= 1',
    'a_even(1)+a_odd(1) >= 2',
    'beta <= 1']
paths = ['gap/lowerbounds/FINDINGS.md',
         'gap/lowerbounds/frac_stab.py','gap/lowerbounds/frac_independent.py',
         'gap/lowerbounds/check_frac_obstruction.py',
         'gap/lowerbounds/check_frac_obstruction_wide.py',
         'w-verifier/claim23b_stability.py','w-verifier/claim23b_stability.json']
out['sha256'] = {p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}
out['status'] = 'PASS'
print(json.dumps(out,indent=2))
