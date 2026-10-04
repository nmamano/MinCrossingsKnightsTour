"""Exact corner lower bound: rational local dual + exhaustive consistency check of its equality face.
Standard library only; no optimizer or worker code is imported.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter,deque
from fractions import Fraction
import json,sys,time
MOVES=[(a,b) for a in [-2,-1,1,2] for b in [-2,-1,1,2] if abs(a*b)==2]
def L(x,ds):
 if x==0:return 1
 if x in (1,2):return sum(x+d in (0,3) for d in ds)-1
 if x==3:return 1-sum(x+d in (1,2) for d in ds)
 return 0

def run(A,scale):
 cert=json.loads(Path(f'gap/verifier/claim57_run/corner_A{A}_S{scale}_dual.json').read_text())
 cells=[(x,y) for y in range(A) for x in range(A) if min(x,y)<6];cs=set(cells);idx={p:i for i,p in enumerate(cells)}
 edges=sorted({tuple(sorted((p,(p[0]+dx,p[1]+dy)))) for p in cells for dx,dy in MOVES if (p[0]+dx,p[1]+dy) in cs})
 assert cert['cells']==[list(p) for p in cells] and cert['edges']==[[list(p),list(q)] for p,q in edges]
 dual=list(map(Fraction,cert['dual']));assert len(dual)==len(cells)+len(edges)
 alpha=dict(zip(cells,dual[:len(cells)]));beta=dict(zip(edges,dual[len(cells):]));bound=sum(alpha.values(),Fraction())
 expected=-38 if A==10 else -19
 assert bound==expected
 slots=[tuple(map(int,s.split())) for s in Path('gap/verifier/claim57_run/source_z6_slots.txt').read_text().splitlines()]
 raw=list(map(int,Path(f'gap/verifier/claim57_run/source_cert_A{10 if A==10 else 14}_w.txt').read_text().split()))
 assert raw[0]==scale;weights=dict(zip(slots,raw[1:]));cut={}
 for (x,y,X,Y),w in weights.items():
  mirror=(X,-1-Y,x,-1-y);assert weights[mirror]==-w
  cut[((x,A+y),(X,A+Y))]=-w
  cut[((A+y,x),(A+Y,X))]=weights[mirror]
 domains=[];neighbors=[];checks=0
 for p in cells:
  ns=[(p[0]+dx,p[1]+dy) for dx,dy in MOVES if (p[0]+dx,p[1]+dy) in cs]
  neighbors.append([(idx[q],1<<ns.index(q)) for q in ns])
  masks=set()
  legal=[(dx,dy) for dx,dy in MOVES if p[0]+dx>=0 and p[1]+dy>=0]
  for a,b in combinations(legal,2):
   chosen=[(p[0]+dx,p[1]+dy) for dx,dy in [a,b]]
   turn=int((a[0]+b[0],a[1]+b[1])!=(0,0))
   cost=scale*(turn-L(p[0],[a[0],b[0]])-L(p[1],[a[1],b[1]]))+sum(cut.get((p,q),0) for q in chosen)
   rhs=alpha[p]+sum((beta[tuple(sorted((p,q)))]*(1 if p<q else -1) for q in chosen if q in cs),Fraction())
   slack=Fraction(cost)-rhs;assert slack>=0,(p,a,b,cost,rhs);checks+=1
   if slack==0:masks.add(sum(1<<ns.index(q) for q in chosen if q in cs))
  assert masks
  domains.append(tuple(sorted(masks)))
 arcs=[]
 for i,ns in enumerate(neighbors):
  arcs.append([(j,bit,next(b for k,b in neighbors[j] if k==i)) for j,bit in ns])
 print('A',A,'bound',bound,'exact inequalities',checks,'domain counts',dict(sorted(Counter(map(len,domains)).items())),flush=True)
 nodes=0;fails=0;start=time.monotonic()
 def dfs(ds):
  nonlocal nodes,fails
  nodes+=1
  if nodes%10000==0:print('nodes',nodes,'seconds',round(time.monotonic()-start,2),flush=True)
  queue=deque(range(len(ds)));pending=set(queue)
  while queue:
   i=queue.popleft();pending.discard(i)
   if not ds[i]:fails+=1;return False
   for j,bi,bj in arcs[i]:
    vals={bool(v&bi) for v in ds[i]}
    if len(vals)==2:continue
    val=next(iter(vals));new=tuple(v for v in ds[j] if bool(v&bj)==val)
    if new!=ds[j]:
     ds[j]=new
     if not new:fails+=1;return False
     if j not in pending:queue.append(j);pending.add(j)
  choices=[(len(v),i) for i,v in enumerate(ds) if len(v)>1]
  if not choices:return True
  _,i=min(choices)
  for v in ds[i]:
   nxt=ds.copy();nxt[i]=(v,)
   if dfs(nxt):return True
  return False
 feasible=dfs(domains.copy())
 assert not feasible,'LP equality face has an integer assignment'
 result=dict(A=A,scale=scale,dual_bound=str(bound),checked_local_inequalities=checks,equality_face_feasible=feasible,search_nodes=nodes,contradiction_leaves=fails,proved_integer_lower_bound=expected+1,seconds=time.monotonic()-start)
 Path(f'gap/verifier/claim57_run/corner_A{A}_exact.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',result,flush=True)

if __name__=='__main__':run(int(sys.argv[1]),int(sys.argv[2]))
