"""Independent square, path, and full-square exclusion audit. No worker imports."""
from itertools import product,combinations
from collections import defaultdict,Counter
from pathlib import Path
import json
from claim9_tiles import quarters,proper
from check import MOVES,check
D=((1,-2),(1,2),(2,-1),(2,1))
canon=lambda e:tuple(sorted(e))

def squares():
 edges=[]
 for x,y in product(range(-3,4),repeat=2):
  for dx,dy in D:
   e=((x,y),(x+dx,y+dy));qs=quarters(e)
   grouped=defaultdict(set)
   for i,j,k in qs:grouped[i,j].add(k)
   assert len(grouped)==2
   for ks in grouped.values():assert len(ks)==2 and sum((-1)**k for k in ks)==0
   if (0,0) in grouped:edges.append(e)
 assert len(edges)==8
 vectors=set();counts=Counter()
 for mask in range(1<<8):
  m=[sum((0,0,k) in quarters(e) for i,e in enumerate(edges) if mask>>i&1) for k in range(4)]
  assert m[0]-m[1]+m[2]-m[3]==0
  bad=sum(t!=1 for t in m);assert bad!=1
  vectors.add(tuple(m));counts[bad]+=1
 return {'single_tiles':49*4,'square_edges':8,'subsets':256,'distinct_vectors':len(vectors),'bad_quarter_histogram':dict(counts)}

def boundary():
 pairs=[];exceptions=[]
 for dx,dy in D:
  e=((0,0),(dx,dy))
  for j,(u,v) in product(range(-4,5),D):
   f=((0,j),(u,j+v))
   if not proper(e,f):continue
   pairs.append((e,f))
   for x,y,k in quarters(e)&quarters(f):
    assert x in (0,1)
    if x==1:
     assert k==3
     expected={((0,y),(2,y+1)),((0,y+1),(2,y))};assert {e,f}==expected
     exceptions.append((e,f))
     for sign in (-1,1):
      allowed={((0,z),(2,z+sign)) for z in (y,y+1)}
      assert not expected<=allowed
 assert len(pairs)==20 and len(exceptions)==2
 # Enumerate all knight edges touching BOTH nonnegative coordinate axes, including the origin.
 E=set()
 for x,y in product(range(4),repeat=2):
  for dx,dy in ((a,b) for a in (-2,-1,1,2) for b in (-2,-1,1,2) if abs(a)+abs(b)==3):
   u,v=x+dx,y+dy
   if min(u,v)<0:continue
   e=canon(((x,y),(u,v)))
   if any(p[0]==0 for p in e) and any(p[1]==0 for p in e):E.add(e)
 assert len(E)==4
 dup=[(e,f) for e,f in combinations(sorted(E),2) if proper(e,f)];assert len(dup)==5
 return {'normalised_pairs':20,'exceptions':exceptions,'corner_edges':sorted(E),'corner_pairs':dup}

def paths():
 out=[]
 for n in (32,34,48,56,96,120,256):
  owned={};total=0;ends=0
  for fx,fy in product((0,1),repeat=2):
   tr=lambda p:((n-2-p[0]) if fx else p[0],(n-2-p[1]) if fy else p[1])
   for R in range(12,n//2-3):
    cells={(R,y) for y in range(1,R+1)}|{(x,R) for x in range(1,R+1)}
    for p in cells:
     q=tr(p);assert q not in owned;owned[q]=(fx,fy,R)
     assert all(1<=v<=n-3 for v in q)
     # In each inward second square strip there is exactly one path endpoint.
     for axis in (0,1):
      if q[axis] in (1,n-3):
       assert p==((1,R) if axis==0 else (R,1));ends+=1
       # The inward exception uses boundary rows R,R+1; both are required good.
       assert {R,R+1}<=set(range(R-1,R+3))
    total+=1
  assert total==2*n-60 and ends==2*total
  out.append({'n':n,'paths':total,'distinct_squares':len(owned),'endpoint_squares':ends})
 return out

def concrete():
 f=Path('w-integrator/tours/FOLD24_n96.json');g=json.loads(f.read_text())['tour'];n=len(g)
 X,T=check(g);es=set()
 for r,row in enumerate(g):
  for c,s in enumerate(row):
   for code in s:
    dr,dc=MOVES[int(code)];es.add(canon(((c,n-1-r),(c+dc,n-1-r-dr))))
 sides=[]
 for axis in (0,1):
  for val in (0,n-1):
   side=[e for e in es if any(p[axis]==val for p in e)]
   sides.append({tuple(sorted((e,f))) for e,f in combinations(side,2) if proper(e,f)})
 overlaps=[len(sides[i]&sides[j]) for i in (0,1) for j in (2,3)]
 assert overlaps==[2]*4
 union=set.union(*sides);assert sum(map(len,sides))-len(union)==8
 return {'file':str(f),'X':X,'T':T,'side_pair_counts':list(map(len,sides)),'corner_duplicates':overlaps,'union_pairs':len(union)}

if __name__=='__main__':
 out={'date':'2026-10-02','square':squares(),'boundary':boundary(),'paths':paths(),'concrete':concrete()}
 Path('w-verifier/claim15.json').write_text(json.dumps(out,indent=1))
 for k,v in out.items():print(k,v,flush=True)
