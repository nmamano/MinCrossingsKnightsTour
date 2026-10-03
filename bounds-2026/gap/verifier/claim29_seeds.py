"""Independent seed counts and patch verification for Claim 29."""
from claim29_window import tile,edge,cross
from claim26_certificate import TERMS,EXC
from collections import Counter
from itertools import combinations
from pathlib import Path
import json

def charge(mult,r):
 v=0
 for j in range(1,r):v+=(1-2*((r+j+1)%2))*(mult[r,j+1,0]+mult[r,j,2]+1)
 for j in range(r,1,-1):v+=(1-2*((j+r)%2))*(mult[j-1,r,1]+mult[j,r,3]+1)
 return v%3
out={}
# Recheck the acyclic two-path patch by geometric quarters, not endpoint formulas.
w=json.loads(Path('gap/verifier/claim29_corner.json').read_text())[0]
es=[edge(tuple(a),tuple(b)) for a,b in w['edges']]
deg=Counter(v for e in es for v in e)
assert all(deg[x,y]==2 for x in range(8) for y in range(8)) and max(deg.values())<=2
parent={}
def find(a):
 while a in parent:a=parent[a]
 return a
for a,b in es:
 u,v=find(a),find(b);assert u!=v;parent[u]=v
pairs=[(e,f) for e,f in combinations(es,2) if cross(e,f)]
isB=lambda e,f:any(any(a[axis]==0 for a in e) and any(a[axis]==0 for a in f) for axis in (0,1))
inside=[(e,f) for e,f in pairs if not isB(e,f)]
assert len(inside)==1
mult=Counter(q for e in es for q in tile(e))
qs=[charge(mult,r) for r in (3,4)];assert all(q!=0 for q in qs)
for r in (3,4):
 for tr in (lambda p:(p[0],p[1]+r),lambda p:(p[1]+r,p[0])):
  assert not all(edge(tr(a),tr(b)) in es for a,b in EXC)
out['acyclic_corner_patch']=dict(core=8,paths=[3,4],height_charges=qs,crossings=len(pairs),B=len(pairs)-1,nonB_pair=inside[0],status='PATCH_ONLY')
# Degree-two alternating vertical free folds. Arbitrary sign sequence works.
fold={edge((x,y),(x+1,y+2*(1 if x%3 else -1))) for x in range(-10,11) for y in range(-14,15)}
deg=Counter(v for e in fold for v in e)
assert all(deg[x,y]==2 for x in range(-8,9) for y in range(-8,9))
assert not any(cross(e,f) for e,f in combinations(fold,2))
mult=Counter(q for e in fold for q in tile(e))
assert all(mult[x,y,k]==1 for x in range(-7,8) for y in range(-7,8) for k in range(4))
out['alternating_folds']=dict(crossings=0,interior_multiplicity=1,height_charge=0)
# Audited gentle seam: one crossing, two holes and two double quarters per level.
seam={edge((x,y),(x+1,y-2) if y>=x else (x+2,y-1)) for x in range(-12,20) for y in range(-12,20)}
mult=Counter(q for e in seam for q in tile(e))
assert all([mult[x,y,k] for k in range(4)]==([0,2,2,0] if y==x-2 else [1]*4) for x in range(-8,16) for y in range(-8,16))
qs=[charge(mult,r) for r in range(4,13)];assert all(q!=0 for q in qs)
pairs=[(e,f) for e,f in combinations(seam,2) if cross(e,f) and 4<=max(min(v[0] for v in e),min(v[0] for v in f))<13]
assert len(pairs)==9
out['gentle_seam']=dict(charged_radii=list(range(4,13)),charges=qs,crossings=9,per_level=1)
# Three endpoint seeds: these have incomplete ghost degrees, not complete corner collars.
result=[]
for period in (4,6,8):
 es=set()
 for y in range(-16,32):
  if period==4:
   es.update((edge((2,y),(0,y+1)),edge((3,y),(1,y+1))))
   if y%4!=3:es.add(edge((1,y),(0,y+2)))
   if y%4==1:es.add(edge((0,y),(1,y+2)))
  else:
   es.update((edge((1,y),(0,y+2)),edge((2,y),(0,y+1))))
   if period==6:
    if y%6 in (0,4,5):es.add(edge((2,y),(1,y+2)))
    if y%6 in (2,3,4):es.add(edge((3,y),(1,y+1)))
   elif y%8!=2:es.add(edge((2,y),(1,y+2)))
   else:es.add(edge((3,y+1),(1,y+2)))
 pairs=[(e,f) for e,f in combinations(es,2) if cross(e,f) and 0<=max(min(v[1] for v in e),min(v[1] for v in f))<period]
 B=sum(any(x==0 for x,y in e) and any(x==0 for x,y in f) for e,f in pairs)
 result.append(dict(period=period,X=len(pairs),B=B,nonB=len(pairs)-B))
assert [(r['X'],r['B']) for r in result]==[(8,8),(10,6),(16,8)]
out['endpoint_seeds']=result
Path('gap/verifier/claim29_seeds.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
