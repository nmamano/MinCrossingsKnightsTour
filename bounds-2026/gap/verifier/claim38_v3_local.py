"""Local good-point audit for section 8. No author imports."""
from collections import defaultdict,Counter
from pathlib import Path
import itertools,json
from pysat.solvers import Minisat22
from claim38_switch import edge,qs
K=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]

def check_path(path):
 forced={edge(a,b) for a,b in zip(path,path[1:])}
 goods={(x+dx,y+dy) for x,y in path[1:-1] for dx,dy in itertools.product((-1,0),repeat=2)}
 lo=min(x for x,y in path)-3;hi=max(x for x,y in path)+4
 bot=min(y for x,y in path)-3;top=max(y for x,y in path)+4
 box={(x,y) for x in range(lo,hi) for y in range(bot,top)}
 es=sorted({edge(p,(p[0]+dx,p[1]+dy)) for p in box for dx,dy in K})
 vid={e:i+1 for i,e in enumerate(es)};inc=defaultdict(list);own=defaultdict(list)
 cl=[[vid[e]] for e in forced]
 for e,v in vid.items():
  for p in e:inc[p].append(v)
  for q in qs(e):own[q].append(v)
 for p,vs in inc.items():
  cl.extend([-a,-b,-c] for a,b,c in itertools.combinations(vs,3))
  if p in box:cl.extend([v for v in vs if v!=i] for i in vs)
 for x,y in goods:
  for k in range(4):
   vs=own[x,y,k];cl.append(vs);cl.extend([-a,-b] for a,b in itertools.combinations(vs,2))
 with Minisat22(bootstrap_with=cl) as s:
  sat=s.solve();model=set(s.get_model() or [])
 selected=[e for e,v in vid.items() if v in model]
 if sat:
  deg=Counter(p for e in selected for p in e);cov=Counter(q for e in selected for q in qs(e))
  assert all(deg[p]==2 for p in box) and max(deg.values())==2
  assert all(cov[x,y,k]==1 for x,y in goods for k in range(4))
 return dict(path=path,sat=sat,goods=sorted(goods),edges=selected,box=[lo,hi,bot,top])
path=[(-2,-1),(0,0)]
for d,l in [((2,1),6),((-2,1),2),((1,-2),1),((-2,1),4)]:
 for _ in range(l):path.append((path[-1][0]+d[0],path[-1][1]+d[1]))
path.append((-1,11))
r=check_path(path);print('odd shift',r['sat'],flush=True)
# Whole-plane word field w(k)=V for k<=-1, H otherwise.
es=set()
for x in range(-10,15):
 for y in range(-10,15):
  if y-x>=0:es.add(edge((x,y),(x+2,y+1)))
  if y-x+1<=-1:es.add(edge((x,y),(x+1,y+2)))
cov=Counter(q for e in es for q in qs(e));deg=Counter(p for e in es for p in e)
shallow=[(2,-2),(3,0),(4,2),(5,4),(3,3),(1,2)]
assert all(edge(a,b) in es for a,b in zip(shallow,shallow[1:]))
assert all(deg[x,y]==2 for x in range(-5,10) for y in range(-5,10))
assert all(cov[x,y,k]==1 for x in range(-5,10) for y in range(-5,10) for k in range(4))
print('perfect-word mixed-port return PASS',shallow)
Path('gap/verifier/claim38_v3_local.json').write_text(json.dumps(dict(odd=r,shallow=shallow),indent=2))
