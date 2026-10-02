#!/usr/bin/env python3
"""Finite exact geometry checks for the knight-edge parallelogram."""
from itertools import product
MOV=((2,1),(1,2),(1,-2),(2,-1))
AXES=((1,0),(0,1),(1,1),(1,-1))
def tile(e):
 a,b=e; x,y=a[0]+b[0],a[1]+b[1]
 if abs(a[0]-b[0])==2: c,d=(x//2,(y-1)//2),(x//2,(y+1)//2)
 else: c,d=((x-1)//2,y//2),((x+1)//2,y//2)
 return a,b,c,d

def overlap(e,f):
 A,B=tile(e),tile(f)
 for x,y in AXES:
  aa=[x*u+y*v for u,v in A]; bb=[x*u+y*v for u,v in B]
  if max(aa)<=min(bb) or max(bb)<=min(aa): return False
 return True

def cross(e,f):
 def det(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 a,b=e;c,d=f
 return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

def microtiles(e):
 P=tile(e); result=set()
 for i in range(min(x for x,y in P),max(x for x,y in P)):
  for j in range(min(y for x,y in P),max(y for x,y in P)):
   for k,(rx,ry) in enumerate(((3,1),(5,3),(3,5),(1,3))):
    qx,qy=6*i+rx,6*j+ry
    if all(min(6*(ax*x+ay*y) for x,y in P)<ax*qx+ay*qy<
           max(6*(ax*x+ay*y) for x,y in P) for ax,ay in AXES):
     result.add((i,j,k))
 assert len(result)==4
 return result

if __name__=='__main__':
 count=0; maximum=0; counts={}
 for dx,dy in MOV:
  e=((0,0),(dx,dy))
  for x,y in product(range(-4,5),repeat=2):
   for u,v in MOV:
    f=((x,y),(x+u,y+v))
    if e==f: continue
    count+=1
    k=len(microtiles(e)&microtiles(f))
    assert bool(k)==cross(e,f)==overlap(e,f), (e,f,k)
    assert k<=2, (e,f,k)
    maximum=max(maximum,k); counts[k]=counts.get(k,0)+1
 print('PASS:',count,'edge pairs; overlap quarter-triangle counts',counts,
       '; maximum intersection area',str(maximum)+'/4')

 # The local flux identity is linear in the selected edges. Check one edge at a time.
 tests=0
 for vertical_grid_edge in (False,True):
  endpoints={(0,0),(0,1) if vertical_grid_edge else (1,0)}
  dual=((-1,1),(1,1)) if vertical_grid_edge else ((1,-1),(1,1))  # coordinates doubled
  near=((-1,0,1),(0,0,3)) if vertical_grid_edge else ((0,-1,2),(0,0,0))
  for x,y in product(range(-4,5),repeat=2):
   for dx,dy in MOV:
    e=((x,y),(x+dx,y+dy)); cells=microtiles(e)
    long=tuple((2*a,2*b) for a,b in e)
    component=dy if vertical_grid_edge else dx
    flux=(1 if (x+y)%2==0 else -1)*(1 if component>0 else -1)*int(cross(long,dual))
    short=int(set(tile(e)[2:])==endpoints)
    rhs=sum(t in cells for t in near)-3*short
    assert flux==rhs,(e,vertical_grid_edge,flux,rhs)
    tests+=1
 print('PASS:',tests,'single-edge local flux identities (both dual directions).')
