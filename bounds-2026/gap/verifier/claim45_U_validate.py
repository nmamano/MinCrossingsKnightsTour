"""Exact, solver-free validation and insertion of the saved collar gadget."""
import json,sys
from pathlib import Path
from collections import defaultdict,Counter
from claim38_switch import edge,qs
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import check,MOVES
from claim9_tiles import proper
from claim36_scan import run as scan

def pn(v):
 x,y=v
 return {(2,y+1),(1,y-2)} if x==0 else {(3,y+1),(0,y+2)} if x==1 else {(x+2,y+1),(x-2,y-1)}
def graph(es):
 a=defaultdict(set)
 for p,q in es:a[p].add(q);a[q].add(p)
 return a

g=json.loads(Path('gap/verifier/claim45_U_gadget.json').read_text())
rem={edge(tuple(a),tuple(b)) for a,b in g['remove']};add={edge(tuple(a),tuple(b)) for a,b in g['add']}
base={edge((x,y),w) for x in range(12) for y in range(-10,27) for w in pn((x,y))}
assert rem<=base and not add&base
new=base-rem|add
oldadj=graph(base);newadj=graph(new)
changed={v for e in rem|add for v in e}
assert all(len(oldadj[v])==len(newadj[v])==2 for v in changed)
assert all(sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2] for a,b in new)
V={(x,y) for x in range(6) for y in range(16)}
def pairs(es):
 adj=graph(es);seen=set();result=[]
 for p in sorted(V):
  if p in seen:continue
  stack=[p];comp={p};seen.add(p)
  while stack:
   v=stack.pop()
   for w in adj[v]:
    if w in V and w not in seen:seen.add(w);comp.add(w);stack.append(w)
  ports=[edge(v,w) for v in comp for w in adj[v] if w not in V]
  assert len(ports)==2,('cycle or invalid component',comp)
  result.append(tuple(sorted(ports)))
 return sorted(result)
assert pairs(base)==pairs(new)
# Count every crossing involving a changed edge, each unordered pair once.
def crossing_pairs(es,changed):return {tuple(sorted((e,f))) for e in changed for f in es if e!=f and proper(e,f)}
dx=len(crossing_pairs(new,add))-len(crossing_pairs(base,rem))
def bq(es):
 counts=Counter(q for e in es for q in qs(e));keys={q for e in rem|add for q in qs(e) if q[0]>=3}
 return sum(counts[q]!=1 for q in keys)
db=bq(new)-bq(base)
assert all(q[0]<5 for e in rem|add for q in qs(e))
report=dict(deltaX=dx,deltaBQ= db,deep_quarter_changes=0,port_pairs=len(pairs(base)),no_cycles=True,unchanged_pairing=True,tours=[])
print('LOCAL',report,flush=True)
for file in sys.argv[1:]:
 grid=json.loads(Path(file).read_text())['tour'];n=len(grid)
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
 adj=graph(es);patches=[]
 for side in range(4):
  for sign in (1,-1):
   for t in range(15,n-30):
    def T(v):
     x,y=v;y=t+sign*y
     return (x,y) if side==0 else (n-1-x,y) if side==1 else (y,x) if side==2 else (y,n-1-x)
    # A large pure neighbourhood ensures every changed crossing, quarter and slot has the reference context.
    if not all(adj[T((x,y))]=={T(w) for w in pn((x,y))} for x in range(9) for y in range(-7,24)):continue
    rr={edge(T(a),T(b)) for a,b in rem};aa={edge(T(a),T(b)) for a,b in add}
    assert rr<=es and not aa&es
    for a,b in rr:es.remove((a,b));adj[a].remove(b);adj[b].remove(a)
    for a,b in aa:es.add((a,b));adj[a].add(b);adj[b].add(a)
    patches.append(dict(side=side,sign=sign,t=t))
 outgrid=[['' for _ in range(n)] for _ in range(n)]
 for (x,y),nb in adj.items():outgrid[n-1-y][x]=''.join(str(MOVES.index((y-v,u-x))) for u,v in sorted(nb))
 X,_=check(outgrid)
 out=Path(f'gap/verifier/claim45_U_patched_n{n}.json');out.write_text(json.dumps(dict(tour=outgrid,patches=patches,source=file)))
 r=dict(n=n,X=X,patches=patches,file=str(out));report['tours'].append(r);print(r,flush=True)
Path('gap/verifier/claim45_U_validation.json').write_text(json.dumps(report,indent=2))
