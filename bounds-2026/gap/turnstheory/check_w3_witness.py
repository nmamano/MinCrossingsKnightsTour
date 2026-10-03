"""Read-only exact check of the saved W3 corner witness (no solver)."""
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root/'gap/lowerbounds/windows'))
from w3_flux import gamma, coeffs, orient
edges = [tuple(map(tuple,e)) for e in json.loads((root/'gap/lowerbounds/windows/w3_corner_K9_R3_6_outS.json').read_text())]
assert len(set(edges)) == len(edges)
deg = Counter(p for e in edges for p in e)
parent = {}
def find(p):
    parent.setdefault(p,p)
    if parent[p] != p: parent[p] = find(parent[p])
    return parent[p]
for a,b in edges:
    assert sorted((abs(a[0]-b[0]),abs(a[1]-b[1]))) == [1,2]
    assert all(0 <= v < 11 for p in (a,b) for v in p)
    assert find(a) != find(b)
    parent[find(a)] = find(b)
assert all(deg[x,y] == 2 for x in range(9) for y in range(9))
assert all(v <= 2 for v in deg.values())
def cross(e,f):
    a,b=e; c,d=f
    return orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0
def in_strip(e,f):
    return any(min(p[k] for p in e)<=1 and min(p[k] for p in f)<=1 for k in (0,1))
pairs=[(e,f) for e,f in combinations(edges,2) if cross(e,f)]
out=sum(not in_strip(e,f) for e,f in pairs)
flux=[]
for r in range(3,7):
    c, cs=coeffs(gamma(r),edges)
    flux.append((c+sum(cs.values()))%3)
assert len(pairs)==57 and out==0 and all(flux)
print(f'PASS: forest, core degree 2; crossings={len(pairs)}, outside S*=0; flux residues={flux}')
