"""Exact light checks of the half-price hand kernel; no author imports."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
import sys,json,hashlib
from claim38_switch import edge,qs
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import MOVES,check

def path_squares(n,r,corner):
 # Lower-left square coordinates; rotate centres, not board vertices.
 def rot(x,y):
  for _ in range(corner):x,y=n-2-y,x
  return x,y
 return [rot(r,j) for j in range(1,r+1)]+[rot(i,r) for i in range(r-1,0,-1)]

def depth(n,s):return min(s[0],s[1],n-2-s[0],n-2-s[1])
geometry=[]
for n in (128,130,144,288):
 seen=set();small=0
 for c in range(4):
  for r in range(12,n//2-3):
   p=path_squares(n,r,c);assert len(set(p))==len(p) and not set(p)&seen;seen.update(p)
   assert all(0<=x<n-1 and 0<=y<n-1 for x,y in p)
   if r<=32:small+=1
   else:
    shallow=[s for s in p if depth(n,s)<4]
    assert Counter(depth(n,s) for s in shallow)=={1:2,2:2,3:2}
    assert len(shallow)==6
 geometry.append(dict(n=n,candidates=4*(n//2-15),small=small,squares=len(seen)))
 assert geometry[-1]['candidates']==2*n-60 and small==84
maxdist=0;covered=0
for d in ((1,2),(1,-2),(2,1),(2,-1)):
 e=((0,0),d)
 for x,y,k in qs(e):
  for u,v in e:
   dist=max(abs(2*u-(2*x+1)),abs(2*v-(2*y+1)))
   maxdist=max(maxdist,dist);assert dist<=3
  covered+=1
assert covered==16 and maxdist==3
# Enumerate one-side strip edges and their possible overlap depths.
strip={edge((x,y),(x+dx,y+dy)) for x in (0,1) for y in range(-4,5) for dy,dx in MOVES if x+dx>=0}
maxdepth=-1;overlaps=0
for a,b in combinations(sorted(strip),2):
 common=set(qs(a))&set(qs(b))
 if not common:continue
 assert len(common) in (1,2)
 overlaps+=1;maxdepth=max(maxdepth,max(x for x,y,k in common))
 assert all(x<=2 for x,y,k in common)
# Exhaustive square identity, with each of the four half multiplicities in 0..2.
for br,rt,tl,lb in product(range(3),repeat=4):
 m=(br+lb,br+rt,tl+rt,tl+lb)
 assert m[0]-m[1]+m[2]-m[3]==0
 assert sum(x!=1 for x in m)!=1

def audit(file):
 grid=json.loads(Path(file).read_text())['tour'];n=len(grid);X,_=check(grid)
 es=sorted({edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code})
 own=defaultdict(list);mask={}
 for i,(a,b) in enumerate(es):
  for q in qs((a,b)):own[q].append(i)
  mask[i]=sum(1<<s for s,ds in enumerate(((a[0],b[0]),(n-1-a[0],n-1-b[0]),(a[1],b[1]),(n-1-a[1],n-1-b[1]))) if min(ds)<=1)
 pair=Counter(z for ls in own.values() for z in combinations(sorted(ls),2))
 assert len(pair)==X and set(pair.values())<={1,2}
 S={z for z in pair if mask[z[0]]&mask[z[1]]};T=len(S)-4*n+2;E=X-4*n+2
 uses=Counter();capacity={};cases=Counter();payable=set();G=W3=0
 for x in range(n-1):
  for y in range(n-1):
   for k in range(4):
    q=x,y,k;ls=own[q];m=len(ls)
    if m==0:G+=1
    if m>=3:W3+=(m-1)*(m-2)//2
    if m==1:continue
    if m==0:atom=('hole',q);cap=1;case='hole'
    elif m>=3:atom=('W3',q);cap=(m-1)*(m-2)//2;case='W3'
    else:
     z=tuple(sorted(ls))
     if z not in S:atom=('pair',z);cap=2;case='outside_pair'
     elif pair[z]==1:atom=('X1',z);cap=1;case='X1'
     else:
      cases['unpaid']+=1
      assert depth(n,(x,y))<=2
      continue
    cases[case]+=1;uses[atom]+=1;capacity[atom]=cap;payable.add(q)
    if atom[0] in ('pair','X1'):
     assert all(max(abs(2*u-2*x-1),abs(2*v-2*y-1))<=3 for i in atom[1] for u,v in es[i])
 assert all(uses[a]<=capacity[a] for a in uses)
 X1=sum(v==1 for v in pair.values())
 assert G+X1+W3==2*E
 nu4=2*(X-len(S))+G+X1+W3
 assert nu4==4*E-2*T
 residual=Counter()
 for c in range(4):
  for r in range(33,n//2-3):
   p=path_squares(n,r,c);quota=min(2,sum((x,y,k) in payable for x,y in p for k in range(4)))
   residual[2-quota]+=1
   if quota<2:
    assert all(len(own[x,y,k])==1 for x,y in p if depth(n,(x,y))>=4 for k in range(4))
 return dict(file=file,n=n,X=X,E=E,S_union=len(S),T=T,nu_times4=nu4,cases=dict(cases),allocated_quarter_units=sum(uses.values()),residual_quarter_demands_all_candidates=dict(residual))
reports=[audit('w-integrator/tours/FOLD24_n96.json'),audit('gap/verifier/claim36_FOLD_n144.json')]
out=dict(geometry=geometry,covered_quarters=covered,max_endpoint_distance_times2=maxdist,strip_overlap_pairs=overlaps,max_strip_overlap_square_depth=maxdepth,tours=reports)
Path('gap/verifier/claim39_check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
files=['gap/turnstheory/PROOF_5N_PLAN.md','gap/turnstheory/check_quarter_payment_support.py','gap/verifier/claim39_check.py']
Path('gap/verifier/claim39_sources.json').write_text(json.dumps({f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},indent=2))
