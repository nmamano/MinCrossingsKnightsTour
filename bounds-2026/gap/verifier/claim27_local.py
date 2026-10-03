"""Independent checks of history identities, obstruction and exact N1 algebra."""
from claim26_certificate import edge,cross,boundary,TERMS,EXC
from itertools import product,combinations
from fractions import Fraction
from collections import Counter
from pathlib import Path
import json

# Exhaust the raw register state and next inputs; compressed images commute.
cases=0
for g in product((0,1),repeat=4):
 for z in product((0,1),repeat=2):
  # before row r: g=(g[r-4],...,g[r-1]), z=(z[r-2],z[r-1]).
  h=(z[0]*g[0],z[1]*g[1],g[2],g[3])
  for gn,zn in product((0,1),repeat=2):
   raw=g[0]*z[0]*gn
   compressed=h[0]*gn
   assert raw==compressed
   nextg=g[1:]+(gn,);nextz=z[1:]+(zn,)
   nexth=(h[1],zn*h[2],h[3],gn)
   assert nexth==(nextz[0]*nextg[0],nextz[1]*nextg[1],nextg[2],nextg[3])
   for counter in range(5):
    assert int(raw and counter==4)==int(compressed and counter==4)
    cases+=1
# All flag words through length 12, all split locations, including a run crossing split.
for bits in product((0,1),repeat=12):
 def scan(bs,c=0):
  k=0
  for b in bs:
   k+=int(b and c==4);c=min(4,c+1) if b else 0
  return k,c
 runs=[];length=0
 for b in bits+(0,):
  if b:length+=1
  else:runs.append(length);length=0
 expected=sum(max(0,l-4) for l in runs)
 assert scan(bits)[0]==expected
 for s in range(13):
  k,c=scan(bits[:s]);kk,cc=scan(bits[s:],c)
  assert k+kk==expected and cc==scan(bits)[1]
# The stated periodic obstruction, independently enumerated.
es=set()
for y in range(-32,48):
 es.update((edge((1,y),(0,y+2)),edge((2,y),(0,y+1))))
 es.add(edge((2,y),(1,y+2)) if y%8!=2 else edge((3,y+1),(1,y+2)))
deg=Counter(v for e in es for v in e)
for y in range(-25,40):
 assert deg[0,y]==deg[1,y]==2 and deg[2,y]<=2 and deg[3,y]<=2
pairs=[(e,f) for e,f in combinations(es,2) if cross(e,f) and 0<=max(min(v[1] for v in e),min(v[1] for v in f))<8]
X=len(pairs);B=sum(boundary(e) and boundary(f) for e,f in pairs)
assert (X,B)==(16,8)
blocked=[y for y in range(8) if deg[3,y]==0 and deg[2,y-2]==deg[2,y+2]==2]
assert blocked==[1,2,5,6,7]
sums={}
for sign in (1,-1):
 co={edge((a[0],sign*a[1]),(b[0],sign*b[1])):c for a,b,c in TERMS}
 ex={edge((a[0],sign*a[1]),(b[0],sign*b[1])) for a,b in EXC}
 sums[sign]=[]
 for phase in (0,1):
  total=0
  for row in range(8):
   local={edge((a[0],a[1]-row),(b[0],b[1]-row)) for a,b in es}
   f=sum(c for e,c in co.items() if e in local)
   c=1-2*((row+phase)%2);h=((1+c)//2+c*(f+2))%3
   total+=2 if ex<=local else (1,2,0)[h]
  sums[sign].append(Fraction(total,2))
 assert max(sums[sign])==Fraction(11,2)
# Corner union and final constants.
cells=list(product(range(6),repeat=2))
edges=[(a,b) for a,b in combinations(cells,2) if sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2]]
assert len(edges)==80
overlap=4*4*len(list(combinations(edges,2)))
assert overlap==50560
beta=Fraction(16,11);C=Fraction(596,44)
boundary_error=overlap-2
AR_constant=(boundary_error+8*C)/beta
E_coefficient=4+2/beta
E_constant=2*AR_constant+156
X_coefficient=4+4/E_coefficient
X_constant=2+E_constant/E_coefficient
assert AR_constant==Fraction(557330,16)
assert X_coefficient==Fraction(204,43) and X_constant==Fraction(558664,43)
assert X_constant<=12993 and X_coefficient-Fraction(52,11)==Fraction(8,473)
result=dict(date='2026-10-03',history_transitions=cases,flag_words=4096,split_positions=13,obstruction_X=X,obstruction_B=B,blocked=blocked,penalty_sums={str(k):list(map(str,v)) for k,v in sums.items()},corner_edges=80,overcount=overlap,coefficient=str(X_coefficient),exact_constant=str(X_constant),rounded_constant=12993,status='PASS')
Path('gap/verifier/claim27_local.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
