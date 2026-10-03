"""Independent W1 CNF reconstruction. Standard library; no worker imports."""
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[2]
core = set(product(range(9), repeat=2))
moves = [(x,y) for x in range(-2,3) for y in range(-2,3)
         if sorted((abs(x),abs(y))) == [1,2]]
edges = sorted({tuple(sorted((v,(v[0]+d[0],v[1]+d[1]))))
                for v in core for d in moves})
ids = {e:i+1 for i,e in enumerate(edges)}
inc = defaultdict(list)
for e,i in ids.items():
    for v in e: inc[v].append(i)
clauses = []
for v,vs in inc.items():
    clauses.extend(tuple(-i for i in tri) for tri in combinations(vs,3))
    if v in core:
        clauses.extend(tuple(j for j in vs if j != i) for i in vs)

def det(u,v): return u[0]*v[1]-u[1]*v[0]
def sub(u,v): return (u[0]-v[0],u[1]-v[1])
for e,f in combinations(edges,2):
    a,b = e; c,d = f
    # Solve a+t(b-a)=c+s(d-c); both parameters must be strictly interior.
    den = det(sub(b,a),sub(d,c))
    if not den: continue
    t = det(sub(c,a),sub(d,c)); s = det(sub(c,a),sub(b,a))
    if den < 0: den,t,s = -den,-t,-s
    if 0 < t < den and 0 < s < den: clauses.append((-ids[e],-ids[f]))

cells = list(product(range(3), repeat=2))
maps = set()
for a,b in [(1,0),(0,1),(1,1),(1,-1)]:
    steps = [d for d in moves if a*d[0]+b*d[1] == 1]
    assert len(steps) == 2
    levels = [a*x+b*y for x,y in cells]
    lo,hi = min(levels)-1,max(levels)
    for word in product(steps, repeat=hi-lo+1):
        maps.add(tuple(tuple(sorted((word[t-lo],tuple(-z for z in word[t-1-lo]))))
                       for t in levels))
for m in maps:
    clause = []
    for (x,y),ds in zip(cells,m):
        p = (x+3,y+3)
        for dx,dy in ds:
            clause.append(-ids[tuple(sorted((p,(p[0]+dx,p[1]+dy))))])
    clauses.append(tuple(clause))
source = root/'gap/lowerbounds/windows/w1cert_k9_b3.cnf'
actual = []
for line in source.read_text().splitlines():
    if line.startswith(('c','p')) or not line.strip(): continue
    nums = list(map(int,line.split())); assert nums[-1] == 0
    actual.append(tuple(nums[:-1]))
canon = lambda cs: Counter(tuple(sorted(c)) for c in cs)
assert canon(actual) == canon(clauses)
result = dict(date='2026-10-03', variables=len(edges), clauses=len(clauses),
              maps=len(maps), clause_multiset_match=True,
              cnf_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
assert (len(edges),len(clauses),len(maps)) == (424,7144,156)
print(json.dumps(result,indent=2))
