"""Search single-cycle two-edge switches that decrease E-BQ/4-EXC."""
import sys,json
from pathlib import Path
from collections import defaultdict,Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import MOVES,check
from claim9_tiles import quarters
TEMPLATE={d:quarters(((0,0),d)) for d in ((1,2),(2,1),(1,-2),(2,-1))}
def edge(a,b):return tuple(sorted((a,b)))
def qs(e):
 a,b=e
 return [(x+a[0],y+a[1],k) for x,y,k in TEMPLATE[b[0]-a[0],b[1]-a[1]]]
def knight(a,b):return sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2]
def run(file,limit=1000):
 grid=json.loads(Path(file).read_text())['tour'];n=len(grid)
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
 adj=defaultdict(set);own=defaultdict(set)
 for a,b in es:
  adj[a].add(b);adj[b].add(a)
  for q in qs((a,b)):own[q].add((a,b))
 transforms=[lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0])]
 def cheap(si,y):
  T=transforms[si]
  for sign in (1,-1):
   ok=True
   for j in range(y-3,y+4):
    for x in range(3):
     v=(x,j) if si==0 else (n-1-x,j) if si==1 else (j,x) if si==2 else (j,n-1-x)
     want={(2,j+sign),(1,j+2*sign)} if x==0 else {(3,j+sign),(0,j-2*sign)} if x==1 else {(4,j+sign),(0,j-sign)}
     if {T(w) for w in adj[v]}!=want:ok=False;break
    if not ok:break
   if ok:return True
  return False
 def score(rem,add):
  changed={v for e in rem for v in e};slots=set()
  for v in changed:
   for si,T in enumerate(transforms):
    x,y=T(v)
    if x<3:
     slots.update((si,j) for j in range(max(3,y-3),min(n-4,y+3)+1))
  if not slots:return None
  before=sum(cheap(*s) for s in slots)
  keys={q for e in rem+add for q in qs(e)}
  pairs0={tuple(sorted((e,f))) for e in rem for q in qs(e) for f in own[q] if e!=f}
  b0=sum(len(own[q])!=1 for q in keys if 3<=q[0]<n-4 and 3<=q[1]<n-4)
  for a,b in rem:
   adj[a].remove(b);adj[b].remove(a)
   for q in qs((a,b)):own[q].remove((a,b))
  for a,b in add:
   adj[a].add(b);adj[b].add(a)
   for q in qs((a,b)):own[q].add((a,b))
  after=sum(cheap(*s) for s in slots)
  pairs1={tuple(sorted((e,f))) for e in add for q in qs(e) for f in own[q] if e!=f}
  b1=sum(len(own[q])!=1 for q in keys if 3<=q[0]<n-4 and 3<=q[1]<n-4)
  for a,b in add:
   adj[a].remove(b);adj[b].remove(a)
   for q in qs((a,b)):own[q].remove((a,b))
  for a,b in rem:
   adj[a].add(b);adj[b].add(a)
   for q in qs((a,b)):own[q].add((a,b))
  dx=len(pairs1)-len(pairs0);db=b1-b0;de=before-after
  return (4*dx-db-4*de,dx,db,de)
 history=[]
 for iteration in range(limit):
  start=(0,0);prev=start;cur=next(iter(adj[start]));seq=[start]
  while cur!=start:
   seq.append(cur);prev,cur=cur,next(v for v in adj[cur] if v!=prev)
  assert len(seq)==n*n
  nex={a:b for a,b in zip(seq,seq[1:]+seq[:1])}
  best=None
  for a,b in nex.items():
   if min(*a,n-1-a[0],n-1-a[1],*b,n-1-b[0],n-1-b[1])>2:continue
   for dy,dx in MOVES:
    c=(a[0]+dx,a[1]+dy)
    if c not in nex:continue
    d=nex[c]
    if len({a,b,c,d})!=4 or not knight(b,d):continue
    add=[edge(a,c),edge(b,d)];rem=[edge(a,b),edge(c,d)]
    if any(e in es for e in add):continue
    sc=score(rem,add)
    if sc is not None and sc[0]<0 and (best is None or sc<best[0]):best=(sc,rem,add)
  if best is None:break
  sc,rem,add=best
  for a,b in rem:
   es.remove((a,b));adj[a].remove(b);adj[b].remove(a)
   for q in qs((a,b)):own[q].remove((a,b))
  for a,b in add:
   es.add((a,b));adj[a].add(b);adj[b].add(a)
   for q in qs((a,b)):own[q].add((a,b))
  history.append(dict(delta=sc,remove=rem,add=add))
  print(n,iteration,sc,rem,add,flush=True)
 grid=[['' for _ in range(n)] for _ in range(n)]
 for (x,y),nb in adj.items():
  grid[n-1-y][x]=''.join(str(MOVES.index((y-v,u-x))) for u,v in sorted(nb))
 X,turns=check(grid)
 out=dict(tour=grid,n=n,X=X,source=file,switches=history)
 Path(f'gap/verifier/claim38_switched_n{n}.json').write_text(json.dumps(out))
 print('FINAL',n,X,len(history),flush=True)
if __name__=='__main__':run(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 1000)
