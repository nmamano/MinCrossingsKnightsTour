#!/usr/bin/env python3
"""Exact bounded-degree search: a crossing-free patch must cover one sample point."""
from itertools import combinations,product
from collections import defaultdict
from check_knight_tiles import tile,cross
MOV=[(x,y) for x in (-2,-1,1,2) for y in (-2,-1,1,2) if abs(x)+abs(y)==3]

def contains(e):
 # Point (1/4,1/3), denominator 12. Tile supporting directions are axes and diagonals.
 P=tile(e)
 for x,y in ((1,0),(0,1),(1,1),(1,-1)):
  vals=[12*(x*a+y*b) for a,b in P]; q=3*x+4*y
  if q<=min(vals) or q>=max(vals): return False
 return True

def check(W):
 low=-(W-2)//2; exact=set(product(range(low,low+W),repeat=2))
 E=sorted({tuple(sorted((u,(u[0]+dx,u[1]+dy)))) for u in exact for dx,dy in MOV})
 I=defaultdict(list)
 for k,e in enumerate(E):
  for v in e:I[v].append(k)
 C=[(tuple(ids),2 if u in exact else 0,2) for u,ids in I.items()]
 C.extend(((i,j),0,1) for i,j in combinations(range(len(E)),2) if cross(E[i],E[j]))
 V=[0 if contains(e) else -1 for e in E]; nodes=0
 def search(v):
  nonlocal nodes
  nodes+=1
  if nodes>20000: raise RuntimeError('node limit')
  while True:
   changed=False
   for ids,lo,hi in C:
    yes=sum(v[k]==1 for k in ids); unset=[k for k in ids if v[k]<0]
    if yes>hi or yes+len(unset)<lo:return None
    if unset and (yes==hi or yes+len(unset)==lo):
     bit=0 if yes==hi else 1
     for k in unset:v[k]=bit
     changed=True
   if not changed:break
  choices=[]
  for ids,lo,hi in C:
   if sum(v[k]==1 for k in ids)<lo: choices.append([k for k in ids if v[k]<0])
  if not choices:return [e for k,e in enumerate(E) if v[k]==1]
  k=min(choices,key=len)[0]
  for bit in (1,0):
   w=v.copy();w[k]=bit; ans=search(w)
   if ans is not None:return ans
  return None
 ans=search(V)
 print('W',W,'edges',len(E),'nodes',nodes,'UNSAT' if ans is None else 'FEASIBLE',flush=True)
 return ans
if __name__=='__main__':
 for W in (2,3,4):
  ans=check(W)
  if ans is None:break
