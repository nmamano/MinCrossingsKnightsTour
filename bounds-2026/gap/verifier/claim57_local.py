"""Independent local reduction of the Claim 57 side potential."""
from itertools import combinations
from pathlib import Path
import json
MOVES=[(a,b) for a in [-2,-1,1,2] for b in [-2,-1,1,2] if abs(a*b)==2]
def lower(x,ds):
 if x==0:return 1
 if x in (1,2):return sum(x+d in (0,3) for d in ds)-1
 if x==3:return 1-sum(x+d in (1,2) for d in ds)
 return 0
def delta(x,ds):return sum((1 if d>0 else -1) for d in ds if 3<=x<=5 and 3<=x+d<=5)
rows=[]
for scale in [3,6]:
 mins=[]
 for x in range(6):
  vals=[]
  for a,b in combinations([d for d in MOVES if x+d[0]>=0],2):
   r=int(a!=(-b[0],-b[1]))-lower(x,[a[0],b[0]])
   assert r>=0
   vals.append(scale*r+delta(x,[a[0],b[0]]))
  mins.append(min(vals))
 assert sum(mins)>=0
 rows.append(dict(scale=scale,per_depth_minima=mins,row_lower_bound=sum(mins)))
for name in ['cert_A14_w.txt','cert_A10_w.txt']:
 p=Path('gap/verifier/claim57_run')/('source_'+name);scale,*weights=map(int,p.read_text().split())
 slots=[tuple(map(int,s.split())) for s in Path('gap/verifier/claim57_run/source_z6_slots.txt').read_text().splitlines()]
 assert len(weights)==len(slots)==28
 for (x,y,X,Y),w in zip(slots,weights):
  assert w==((1 if X<x else -1) if min(x,X)>=3 else 0)
  assert 0<=x<6 and 0<=X<6 and y<0<=Y and sorted([abs(X-x),abs(Y-y)])==[1,2]
print(json.dumps(rows,indent=2))
Path('gap/verifier/claim57_run/side_local.json').write_text(json.dumps(rows,indent=2)+'\n')
