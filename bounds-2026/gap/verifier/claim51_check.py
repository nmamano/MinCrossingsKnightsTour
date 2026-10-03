"""Implementation check of the new keep rule and scalar count.
No new finite input to the proof: uses the standalone Claim 50 exact geometry.
"""
import json,time
from pathlib import Path
from collections import defaultdict,Counter
from itertools import combinations
from claim50_check import edge,quarters,U,flags
MOVES=((-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1))
def run(file):
 grid=json.loads(Path(file).read_text())['tour'];n=len(grid)
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
 own=defaultdict(list);tq={e:quarters(e) for e in es}
 for e,qq in tq.items():
  for q in qq:own[q].append(e)
 pairs={tuple(sorted((a,b))) for ls in own.values() for a,b in combinations(ls,2)}
 X=len(pairs);X1=sum(len(tq[a]&tq[b])==1 for a,b in pairs)
 S=set();gf=[]
 for T in (lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0])):
  strip={e for e in es if min(T(e[0])[0],T(e[1])[0])<=1}
  S.update((a,b) for a,b in pairs if a in strip and b in strip)
  loc={edge(T(a),T(b)) for a,b in strip};gg=[]
  for r in range(n):
   mask=sum(U[edge((a[0],a[1]-r),(b[0],b[1]-r))] for a,b in loc if min(a[1],b[1])<=r<=max(a[1],b[1]))
   gg.append(flags(mask)[0 if r<n//2 else 1])
  gf.append(gg)
 b=sum(map(sum,gf));s=len(S);E=X-4*n+2;T=s-4*n+2
 D=0;usable=set()
 for x in range(n-1):
  for y in range(n-1):
   for k in range(4):
    q=x,y,k;ls=own[q];m=len(ls);D+=(m-1)*(m-2)//2
    if m==1:continue
    forbidden=m==2 and tuple(sorted(ls)) in S and len(tq[ls[0]]&tq[ls[1]])==2
    if not forbidden:usable.add(q)
 assert D+X1==2*E and len(usable)<=D+2*(X-s)+X1==4*E-2*T
 kept=[];discarded=[];used=set();chosen=set()
 for fx in (0,1):
  for fy in (0,1):
   for r in range(12,n//2-3):
    ends=((fx,n-1-r if fy else r),(2+fy,n-1-r if fx else r))
    if any(gf[side][row] for side,row in ends):
     selected=next((side,row) for side,row in ends if gf[side][row]);assert selected not in used;used.add(selected);discarded.append((fx,fy,r));continue
    pp=[(n-2-x if fx else x,n-2-y if fy else y) for x,y in [(r,j) for j in range(1,r+1)]+[(j,r) for j in range(r-1,0,-1)]]
    bad=[(x,y,k) for x,y in pp for k in range(4) if len(own[x,y,k])!=1]
    assert len(bad)>=2 and all(q in usable for q in bad)
    assert not chosen&set(bad[:2]);chosen.update(bad[:2]);kept.append((fx,fy,r))
 N=2*n-60;M=len(kept);z=len(discarded)
 assert M+z==N and z<=b and len(chosen)==2*M and T>=b-1130
 assert 4*E>=2*M+2*T>=2*N-2320
 return dict(file=file,n=n,X=X,E=E,s=s,T=T,b=b,N=N,M=M,z=z,D=D,X1=X1,usable_quarters=len(usable),scalar_bound=4*E-2*T,chosen_quarters=len(chosen),all_checks_pass=True)
if __name__=='__main__':
 out=[run(f) for f in ['gap/verifier/claim36_FOLD_n144.json','gap/verifier/claim47_patched_n288.json','w-integrator/tours/FJOG_n132.json']]
 Path('gap/verifier/claim51_check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
