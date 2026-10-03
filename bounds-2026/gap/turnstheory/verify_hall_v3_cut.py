"""Second exact geometry/support check of the worst p=2/3 Hall cut.
Uses rational polygon clipping instead of microtiles and explicit vertex sets
instead of the main eligibility routine. No max-flow code is imported.
"""
import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'w-verifier'),str(ROOT/'gap/verifier')]
from check import check,MOVES
from claim9_tiles import quarters
from claim26_certificate import TERMS,EXC,edge
r=json.loads((ROOT/'gap/turnstheory/hall_v3_worst_2_3.json').read_text())
t=next(t for t in r['trials'] if t['p']=='2/3')
d=json.loads((ROOT/r['sources'][0]).read_text());tour=d['tour'];n=len(tour)
X,_=check(tour);assert X==r['X']
es=set()
for y,row in enumerate(tour):
 for x,code in enumerate(row):
  for ch in code:
   dy,dx=MOVES[int(ch)];es.add(edge((x,n-1-y),(x+dx,n-1-y-dy)))
es=sorted(es);selected=set(es);verts=set()
for fx,fy,radius in t['J']:
 assert 12<=radius<=n//2-4
 def phys(p):return (n-1-p[0] if fx else p[0],n-1-p[1] if fy else p[1])
 residues=[]
 for transpose in (False,True):
  def at(p):
   x,y=p[0],p[1]+radius
   return phys((y,x) if transpose else (x,y))
  assert not all(edge(at(a),at(b)) in selected for a,b in EXC)
  F=sum(c for a,b,c in TERMS if edge(at(a),at(b)) in selected)
  c=(-1)**radius;residues.append(((1+c)//2+c*(F+2))%3)
 assert sum(residues)%3
 for j in range(1,radius+1):
  for x,y in [(2*radius+1,2*j+1),(2*j+1,2*radius+1)]:
   verts.add((2*(n-1)-x if fx else x,2*(n-1)-y if fy else y))
assert t['J']==[[1,0,k] for k in range(15,127) if k%6!=2]
buckets=defaultdict(list)
for i,(a,b) in enumerate(es):
 delta=(b[0]-a[0],b[1]-a[1])
 for x,y,k in quarters(((0,0),delta)):buckets[x+a[0],y+a[1],k].append(i)
pairs=Counter()
for ids in buckets.values():
 for pair in combinations(ids,2):pairs[pair]+=1
assert len(pairs)==X
R=t['radius']
def eligible(points):
 # Enumerate each possible odd integer centre in the intersection of
 # all support-point radius boxes; require membership in actual J vertices.
 lo_x=max(x for x,y in points)-2*R;hi_x=min(x for x,y in points)+2*R
 lo_y=max(y for x,y in points)-2*R;hi_y=min(y for x,y in points)+2*R
 return any((x,y) in verts for x in range(lo_x+(lo_x%2==0),hi_x+1,2)
            for y in range(lo_y+(lo_y%2==0),hi_y+1,2))
def inS(e,f):
 return any(any(p[k]<=1 for p in e) and any(p[k]<=1 for p in f)
            or any(p[k]>=n-2 for p in e) and any(p[k]>=n-2 for p in f) for k in (0,1))
counts=Counter();geometries=defaultdict(set)
for (a,b),overlap in pairs.items():
 if eligible([(2*x,2*y) for i in (a,b) for x,y in es[i]]):
  if not inS(es[a],es[b]):counts['pair']+=1;geometries['pair'].add((es[a],es[b]))
  if overlap==1:counts['X1']+=1;geometries['X1'].add((es[a],es[b]))
CORNERS=((0,0),(2,0),(2,2),(0,2))
for x in range(n-1):
 for y in range(n-1):
  for k in range(4):
   m=len(buckets.get((x,y,k),()))
   units=1 if m==0 else (m-1)*(m-2)//2
   if not units:continue
   ps=[(2*x+a,2*y+b) for a,b in (CORNERS[k],CORNERS[(k+1)%4],(1,1))]
   if eligible(ps):
    kind='G' if m==0 else 'W3';counts[kind]+=units;geometries[kind].add((x,y,k))
assert counts==Counter(pair=21,G=217)
assert len(t['J'])==94
capacity=4*counts['pair']+counts['G']+counts['X1']+counts['W3']
assert capacity==t['neighbour_capacity_scaled']==301
assert Fraction(4*len(t['J'])-capacity,6)==Fraction(t['Delta'])==Fraction(25,2)
for a in t['neighbour_atoms']:
 g=a['geometry']
 g=tuple(tuple(map(tuple,e)) for e in g) if a['kind'] in ('pair','X1') else tuple(g)
 assert g in geometries[a['kind']]
print('PASS: independent rational tiles, explicit support centres, retained-path cut.')
print('LF5 n=260: J={(right,bottom,r): 15<=r<=126, r mod 6 !=2}, |J|=94.')
print('N(J): 21 non-S* pairs + 217 holes; no X1/W3 atoms; capacity=301/6.')
print('Demand=376/6; Hall deficit=75/6=25/2.')
