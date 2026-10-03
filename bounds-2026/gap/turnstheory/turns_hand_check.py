"""Standard-library checks of the local hand statements in TURNS_GAP.md."""
from itertools import combinations,product
M=tuple((a,b) for a in (-2,-1,1,2) for b in (-2,-1,1,2) if abs(a)+abs(b)==3)
def turn(ds):return int(tuple(map(sum,zip(*ds)))!=(0,0))
def lower(x,ds):
 if x==0:return 1
 if x in (1,2):return sum(x+d[0] in (0,3) for d in ds)-1
 if x==3:return 1-sum(x+d[0] in (1,2) for d in ds)
 return 0
def options(x):return [frozenset(ds) for ds in combinations([d for d in M if x+d[0]>=0],2) if turn(ds)==lower(x,ds)]
assert [len(options(x)) for x in range(5)]==[6,8,10,10,4]
def enumerate_fixed(W):
 chosen=[];out=[]
 def visit(x):
  if x==W:out.append(tuple(chosen));return
  for ds in options(x):
   if any(((dx,dy) in ds)!=((-dx,-dy) in chosen[x+dx]) for dx,dy in M if 0<=x+dx<x):continue
   chosen.append(ds);visit(x+1);chosen.pop()
 visit(0);return set(out)
def fixed(W,a,b,c):
 return tuple(frozenset(((1,2*a),(2,b))) if x==0 else frozenset(((-1,-2*a),(2,c))) if x==1 else frozenset(((2,b),(-2,-b))) if x%2==0 else frozenset(((2,c),(-2,-c))) for x in range(W))
for W in (8,12):
 actual=enumerate_fixed(W);expected={fixed(W,a,b,c) for a,b,c in product((-1,1),repeat=3)}
 assert actual==expected and len(actual)==8
print('PASS: all translation-invariant zero-slack windows at widths 8 and 12 are the eight sign patterns.')
def alternate(x,y):
 if y%2==0:
  return ((1,2),(2,-1)) if x==0 else ((-1,-2),(1,2))
 if x==0:return ((1,-2),(1,2))
 if x==1:return ((-1,-2),(-1,2))
 if x==2:return ((-2,1),(1,-2))
 return ((-1,2),(1,-2))
for x in range(10):
 for y in range(2):
  ds=alternate(x,y);assert turn(ds)==lower(x,ds)
  for dx,dy in ds:assert (-dx,-dy) in alternate(x+dx,y+dy)
assert [sum(turn(alternate(x,y)) for x in range(4)) for y in range(2)]==[1,3]
print('PASS: the alternating 1/3-turn half-plane field has reciprocal edges and zero local slack.')
