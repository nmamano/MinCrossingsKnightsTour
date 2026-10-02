"""Independent corner linear identity, enumeration, and path geometry."""
from itertools import product,combinations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json
from claim9_tiles import proper,quarters
M=[(x,y) for x in (-2,-1,1,2) for y in (-2,-1,1,2) if abs(x)+abs(y)==3]
chi=lambda v:1 if sum(v)%2==0 else -1
canon=lambda a,b:tuple(sorted((a,b)))
K={(0,y) for y in range(4)}|{(x,0) for x in range(1,4)}

def options():
 choices=[]
 for v in sorted(K):
  nb=[(v[0]+x,v[1]+y) for x,y in M if min(v[0]+x,v[1]+y)>=0]
  choices.append([set(canon(v,w) for w in p) for p in combinations(nb,2)])
 out=[]
 for opts in product(*choices):
  es=set.union(*opts)
  if all(sum(v in e for e in es)==2 for v in K):out.append(es)
 assert len(out)==2916
 return out

def coefficient(e,R):
 points=[(3,2*R+1),(1,2*R+1),(1,1),(2*R+1,1),(2*R+1,3)]
 E=tuple((2*x,2*y) for x,y in e);out=0
 for a,b in zip(points,points[1:]):
  if proper(E,(a,b)):
   v=E[0];left=(b[0]-a[0])*(v[1]-a[1])-(b[1]-a[1])*(v[0]-a[0])>0
   out+=chi(e[0] if left else e[1])
 return out

def patterns(R,L,B):
 fixed=set();es=set()
 for transpose,sign in ((False,L),(True,B)):
  f=lambda v:(v[1],v[0]) if transpose else v
  cells={f((x,y)) for x in (0,1) for y in range(R-1,R+3)}
  fixed|=cells
  for y in range(R-5,R+7):
   for a,b in [((0,y),(2,y+sign)),((0,y),(1,y+2*sign)),((1,y),(3,y+sign))]:
    a,b=f(a),f(b)
    if a in cells or b in cells:es.add(canon(a,b))
 return fixed,es

def corner():
 opts=options();out=[];normal={}
 for R in list(range(12,32))+[100,101]:
  edges=set()
  for x,y in product(range(R+5),repeat=2):
   for dx,dy in M:
    v=(x+dx,y+dy)
    if min(v)>=0:edges.add(canon((x,y),v))
  mid={(0,y) for y in range(4,R-1)}|{(y,0) for y in range(4,R-1)}
  residual={e:coefficient(e,R)+sum(chi(v) for v in e if v in mid) for e in edges}
  residual={e:c for e,c in residual.items() if c}
  base=-chi((1,R+1))-chi((R+1,1))-2*sum(chi((0,j)) for j in range(1,R+1))-2*sum(chi(v) for v in mid)
  cv=[sum(residual.get(e,0) for e in es) for es in opts]
  for L,B in product((1,-1),repeat=2):
   fixed,es=patterns(R,L,B)
   assert all(any(v in K or v in fixed for v in e) for e in residual)
   assert not any(v in K for e in es for v in e)
   values={(base+sum(residual.get(e,0) for e in es)+c)%3 for c in cv}
   assert values=={1}
  # All nonzero coefficients lie in a fixed corner part or a translated endpoint part.
  signature=[]
  for e,c in residual.items():
   if any(v in K for v in e):key=('corner',e)
   elif max(v[0] for v in e)<=3:key=('left',tuple((x,y-R) for x,y in e))
   else:key=('bottom',tuple((x-R,y) for x,y in e))
   signature.append((key,c))
  signature=(base,tuple(sorted(signature)))
  if R%2 in normal:assert signature==normal[R%2]
  else:normal[R%2]=signature
  out.append({'R':R,'patterns':4,'corner_choices':2916,'residual_edges':len(residual)})
 print('corner cases',len(out),'radii, 4 patterns, 2916 choices each',flush=True)
 return out

def paths():
 reports=[]
 for n in (32,48,64,72,96):
  seen=set();U=set();counts=Counter()
  for flipx,flipy in product((0,1),repeat=2):
   transform=lambda p:((2*(n-1)-p[0]) if flipx else p[0],(2*(n-1)-p[1]) if flipy else p[1])
   for R in range(12,n//2-3):
    pts=[(2*R+1,y) for y in range(3,2*R+2,2)]+[(x,2*R+1) for x in range(2*R-1,2,-2)]
    for a,b in zip(pts,pts[1:]):
     a,b=transform(a),transform(b);key=canon(a,b)
     assert key not in seen;seen.add(key)
     if a[1]==b[1]:
      k=(a[0]+b[0])//4;j=(a[1]-1)//2;ts=[(k-1,j,1),(k,j,3)]
     else:
      i=(a[0]-1)//2;k=(a[1]+b[1])//4;ts=[(i,k-1,2),(i,k,0)]
     for t in ts:
      assert t not in U;U.add(t)
      assert 1<=t[0]<n-2 and 1<=t[1]<n-2
    for side in (('x',flipx),('y',flipy)):
     rev=flipy if side[0]=='x' else flipx
     for y in range(R-1,R+3):counts[side,n-1-y if rev else y]+=1
  assert max(counts.values())<=4
  pairs=set()
  for axis in (0,1):
   for flip in (False,True):
    def tr(p):
     x,y=p
     if flip:x=n-1-x
     return (y,x) if axis else (x,y)
    for y in range(6,n-6):
     for s in (1,-1):
      p=([((0,y-2),(1,y)),((0,y-1),(2,y))] if s==1 else [((0,y+1),(1,y-1)),((0,y),(2,y-1))])
      p=tuple(sorted(canon(tr(a),tr(b)) for a,b in p))
      assert p not in pairs;pairs.add(p)
      assert proper(*p)
      overlap=quarters(p[0])&quarters(p[1]);assert overlap and not overlap&U
  reports.append({'n':n,'candidate_paths':2*n-60,'dual_edges':len(seen),'adjacent_quarters':len(U),'max_paths_per_bad_row':max(counts.values()),'distinct_pattern_pairs':len(pairs)})
 print('path and boundary geometry',reports,flush=True)
 return reports
if __name__=='__main__':
 r={'corner':corner(),'paths':paths()}
 Path('w-verifier/claim11_corner.json').write_text(json.dumps(r,indent=1))
