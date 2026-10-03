"""Independent Option C audit. Standard library only, no author/project imports.
All 256 new-edge subsets per row; exact integer tile-quarter geometry.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
import json,hashlib,time

def edge(a,b):return tuple(sorted((tuple(a),tuple(b))))
def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def cross(e,f):
 a,b=e;c,d=f
 return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

def quarters(e):
 a,b=e;mx,my=a[0]+b[0],a[1]+b[1]
 if abs(a[0]-b[0])==2:p,q=(mx//2,(my-1)//2),(mx//2,(my+1)//2)
 else:p,q=((mx-1)//2,my//2),((mx+1)//2,my//2)
 pts=sorted((a,b,p,q));lo=[];hi=[]
 for h,seq in ((lo,pts),(hi,pts[::-1])):
  for v in seq:
   while len(h)>1 and det(h[-2],h[-1],v)<=0:h.pop()
   h.append(v)
 poly=lo[:-1]+hi[:-1];poly=[(6*x,6*y) for x,y in poly]
 out=set()
 for x in range(min(a[0],b[0]),max(a[0],b[0])):
  for y in range(min(a[1],b[1]),max(a[1],b[1])):
   for k,(dx,dy) in enumerate(((3,1),(5,3),(3,5),(1,3))):
    v=(6*x+dx,6*y+dy)
    if all(det(p,q,v)>0 for p,q in zip(poly,poly[1:]+poly[:1])):out.add((x,y,k))
 assert len(out)==4
 return out

NEW=sorted({edge((x,0),(z,y)) for x,z,y in product(range(4),range(4),(1,2)) if min(x,z)<2 and sorted((abs(x-z),y))==[1,2]})
CUT=sorted({edge((x,y),(z,y+d)) for x,z,y,d in product(range(4),range(4),(-2,-1),(1,2)) if y+d>=0 and min(x,z)<2 and sorted((abs(x-z),d))==[1,2]})
assert len(NEW)==8 and len(CUT)==12
UNIV=sorted(set(NEW)|set(CUT));assert len(UNIV)==20
U={e:1<<i for i,e in enumerate(UNIV)};C={e:1<<i for i,e in enumerate(CUT)}
Q={e:quarters(e) for e in UNIV}
# Coefficients transcribed from PROOF_5N section 2, not the author checker.
raw=[((0,-1),(1,1),-1),((0,0),(1,-2),-1),((0,0),(2,-1),-1),((0,1),(1,-1),1),((0,1),(2,0),1),((0,2),(1,0),-1),((1,0),(2,2),-1),((1,1),(2,-1),-1)]
terms=[];exceptions=[];vis=[]
for sign in (1,-1):
 tr=lambda p:(p[0],sign*p[1])
 terms.append([(U[edge(tr(a),tr(b))],v) for a,b,v in raw])
 exceptions.append(U[edge(tr((0,0)),tr((2,1)))]+U[edge(tr((0,1)),tr((2,0)))])
 vv=[]
 for a,b in combinations(UNIV,2):
  common=Q[a]&Q[b]
  if len(common)==2 and any(1<=x<=3 and y==(0 if sign==1 else -1) for x,y,k in common) and not all(any(x==0 for x,y in e) for e in (a,b)):
   assert cross(a,b);vv.append(U[a]|U[b])
 vis.append(vv)
assert list(map(len,vis))==[7,7]
cache={}
def flags(mask):
 if mask not in cache:
  cache[mask]=tuple(int(sum(v for b,v in terms[k] if mask&b)%3!=2 or mask&exceptions[k]==exceptions[k] or any(mask&v==v for v in vis[k])) for k in range(2))
 return cache[mask]

subsets=[]
for m in range(256):
 es=[e for i,e in enumerate(NEW) if m>>i&1];row=[0]*4;future=Counter()
 for e in es:
  a,b=sorted(e,key=lambda p:p[1]);row[a[0]]+=1;future[b]+=1
 if max(row)>2 or any(v>2 for v in future.values()):continue
 mask=sum(U[e] for e in es);shift=sum(C[edge((a[0],a[1]-1),(b[0],b[1]-1))] for a,b in es)
 w=sum(cross(a,b) for a,b in combinations(es,2))
 subsets.append((es,row,future,mask,shift,w))

def arcs_from(s):
 pending=[e for i,e in enumerate(CUT) if s>>i&1];row=[0]*4;future=Counter();keep=0
 for e in pending:
  hi=max(e,key=lambda p:p[1])
  if hi[1]==0:row[hi[0]]+=1
  else:
   future[hi]+=1;a,b=e;keep|=C[edge((a[0],a[1]-1),(b[0],b[1]-1))]
 if max(row)>2:return
 mask=sum(U[e] for e in pending)
 for new,deg,load,nmask,shift,w0 in subsets:
  degs=[a+b for a,b in zip(row,deg)]
  if degs[:2]!=[2,2] or max(degs)>2 or any(load[v]+future[v]>2 for v in load):continue
  nxt=keep|shift;w=w0+sum(cross(a,b) for a in pending for b in new)
  yield nxt,w,*flags(mask|nmask)

def main():
 start=time.monotonic();states=[0];ids={0:0};arcs=[];byrow={}
 for s in states:
  rr=list(arcs_from(s));byrow[s]=rr
  for t,w,u,d in rr:
   if t not in ids:ids[t]=len(states);states.append(t)
   arcs.append((ids[s],ids[t],w,u,d))
 assert (len(states),len(arcs))==(3136,48510)
 # Every degree-admissible row chosen by an actual tour is included; no cycle rejection.
 pots=[];stats=[]
 for k in (3,4):
  h=[0]*len(states)
  for it in range(100):
   hh=h.copy()
   for u,v,w,gu,gd in arcs:hh[v]=min(hh[v],h[u]+4*w-4-4*(gu if k==3 else gd))
   if hh==h:break
   h=hh
  else:raise AssertionError('no fixed point')
  slacks=[4*w-4-4*(gu if k==3 else gd)+h[u]-h[v] for u,v,w,gu,gd in arcs]
  assert min(slacks)>=0;pots.append(h);stats.append(dict(passes=it+1,range=[min(h),max(h)],min_arc_slack=min(slacks)))
 assert stats==[dict(passes=8,range=[-24,0],min_arc_slack=0),dict(passes=8,range=[-28,0],min_arc_slack=0)]
 diff=[a-b for a,b in zip(*pots)];assert (min(diff),max(diff))==(0,4)
 # Actual finite strips: verify each row maps to an arc, weights sum to brute crossings, K exactly.
 tourchecks=[]
 for file in ['gap/verifier/claim36_FOLD_n144.json','gap/verifier/claim47_patched_n288.json','w-integrator/tours/FJOG_n132.json']:
  g=json.loads(Path(file).read_text())['tour'];n=len(g)
  moves=((-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1))
  allE={edge((x,n-1-y),(x+moves[int(z)][1],n-1-y-moves[int(z)][0])) for y,row in enumerate(g) for x,code in enumerate(row) for z in code}
  for side,T in enumerate((lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0]))):
   es={edge(T(a),T(b)) for a,b in allE};es={e for e in es if min(e[0][0],e[1][0])<2};s=0;ws=0;gs=0
   for r in range(n):
    local={edge((a[0],a[1]-r),(b[0],b[1]-r)) for a,b in es if min(a[1],b[1])<=r<=max(a[1],b[1])}
    t=sum(C[edge((a[0],a[1]-1),(b[0],b[1]-1))] for a,b in local if max(a[1],b[1])>0)
    fresh=[e for e in local if min(p[1] for p in e)==0];pending=[e for e in local if min(p[1] for p in e)<0]
    w=sum(cross(a,b) for a in fresh for b in pending)+sum(cross(a,b) for a,b in combinations(fresh,2));gu,gd=flags(sum(U[e] for e in local))
    assert (t,w,gu,gd) in byrow[s];s=t;ws+=w;gs+=gu if r<n//2 else gd
   assert s==0
   xx=sum(cross(a,b) for a,b in combinations(es,2));assert xx==ws and gs<=xx-n+7
   qq={e:quarters(e) for e in es};mult=Counter(q for qs in qq.values() for q in qs)
   x1=sum(len(qq[a]&qq[b])==1 for a,b in combinations(es,2))
   holes=sum(mult[0,y,k]==0 for y in range(n-1) for k in range(4));abs1=sum(abs(mult[1,y,k]-1) for y in range(n-1) for k in range(4))
   c=sum({a[0],b[0]}=={1,2} for a,b in es)
   w3=sum((v-1)*(v-2)//2 for (x,y,k),v in mult.items() if x<=1)
   outer=sum(v*(v-1)//2 for (x,y,k),v in mult.items() if x>=2)
   rhs2=4*n+12+2*holes+2*c+abs1+2*w3+2*outer+2*x1
   assert 4*xx==rhs2 and xx>=n+3
   tourchecks.append(dict(file=file,n=n,side=side,X=xx,G=gs,K_verified=True,side_slack=xx-n+7-gs))
 out=dict(date='2026-10-03',states=len(states),arcs=len(arcs),VIS_counts=list(map(len,vis)),potentials=stats,interface=[min(diff),max(diff)],side_error_scaled4=28,empty_potentials=[h[0] for h in pots],tour_checks=tourchecks,seconds=time.monotonic()-start)
 Path('gap/verifier/claim50_check.json').write_text(json.dumps(out,indent=2));Path('gap/verifier/claim50_potentials.json').write_text(json.dumps({str(s):[pots[0][i],pots[1][i]] for i,s in enumerate(states)}));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
