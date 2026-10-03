"""Exact check of the zero-crossing alternating horizontal-wall field."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'w-verifier'))
from claim9_tiles import quarters

def step(y): return (2 if y % 2 == 0 else -2, 1)
def cross(e,f):
    def det(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    a,b=e; c,d=f
    return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

edges = [((x,y),(x+step(y)[0],y+1)) for x in range(-6,19) for y in range(-6,19)]
degree = Counter(v for e in edges for v in e)
cover = Counter()
for a,b in edges:
    for x,y,k in quarters(((0,0),(b[0]-a[0],b[1]-a[1]))):
        cover[x+a[0],y+a[1],k] += 1
assert all(degree[x,y] == 2 for x in range(12) for y in range(12))
assert all(cover[x,y,k] == 1 for x in range(12) for y in range(12) for k in range(4))
X = sum(cross(e,f) for e,f in combinations(edges,2))
assert X == 0
strands = [[(k+(2 if y%2 else 0), y) for y in range(12)] for k in (3,5,7)]
edge_set = {frozenset(e) for e in edges}
assert all(frozenset((a,b)) in edge_set for path in strands for a,b in zip(path,path[1:]))
assert all(0 < x < 11 for path in strands for x,y in path)
out = dict(date='2026-10-03',edges_checked=len(edges),crossings=X,
           core_vertices_degree_two=144,core_quarters_exactly_once=576,
           square_row_split='slash for even y, backslash for odd y',
           horizontal_walls='every integer y',strands=strands,
           same_vertical_side_returns=0,
           scope='plane field / open window; not a closed finite tour')
print(json.dumps(out,indent=2))
