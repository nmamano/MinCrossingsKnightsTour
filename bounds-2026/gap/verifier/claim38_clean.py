"""Clean-chord diagnostic and local clean-turn implication check."""
import json,sys,itertools
from pathlib import Path
from collections import defaultdict
from claim38_switch import edge,qs
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import MOVES
from pysat.solvers import Minisat22
ROOT=Path(__file__).resolve().parents[2]
D=[(2,1),(-2,1),(1,-2),(1,2),(-2,-1),(2,-1),(-1,2),(-1,-2)]
results=[]
for name in ['claim36_scan.json','claim36_revised_extra.json','claim36_family_scan.json']:
 for r in json.loads((ROOT/'gap/verifier'/name).read_text()):
  grid=json.loads((ROOT/r['file']).read_text())['tour'];n=len(grid)
  es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
  own=defaultdict(int)
  for e in es:
   for q in qs(e):own[q]+=1
  good=lambda sq:all(own[*sq,k]==1 for k in range(4))
  clean=[];nonfree=[]
  for ch in r['SSR_chords']:
   path=[tuple(p) for p in ch['path'][1:-1]]
   if all(good((x,y)) for a,b in zip(path,path[1:]) for x,y,k in qs(edge(a,b))):
    clean.append(ch)
    ds=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(path,path[1:])]
    if any(a!=b and (D.index(b)-D.index(a))%8 not in (1,7) for a,b in zip(ds,ds[1:])):nonfree.append(ch)
  results.append(dict(file=r['file'],n=n,SSR=r['SSR'],clean=len(clean),nonfree=len(nonfree),EXC=4*(n-6)-r['cheap_slots']))
  print(results[-1],flush=True)
# Local implication: only squares traversed by two consecutive edges are required good.
local=[]
for direction in D:
 if direction==(2,1) or (D.index(direction)-D.index((2,1)))%8 in (1,7) or direction==(-2,-1):continue
 forced=[edge((0,0),(2,1)),edge((2,1),(2+direction[0],1+direction[1]))]
 goodS={(x,y) for e in forced for x,y,k in qs(e)}
 box={(x,y) for x in range(-4,8) for y in range(-5,8)}
 es=sorted({edge(p,(p[0]+dx,p[1]+dy)) for p in box for dy,dx in MOVES});vid={e:i+1 for i,e in enumerate(es)}
 cl=[[vid[e]] for e in forced];inc=defaultdict(list);own=defaultdict(list)
 for e,v in vid.items():
  for p in e:inc[p].append(v)
  for q in qs(e):own[q].append(v)
 for p,vs in inc.items():
  cl.extend([-a,-b,-c] for a,b,c in itertools.combinations(vs,3))
  if p in box:cl.extend([v for v in vs if v!=i] for i in vs)
 for x,y in goodS:
  for k in range(4):
   vs=own[x,y,k];cl.append(vs);cl.extend([-a,-b] for a,b in itertools.combinations(vs,2))
 with Minisat22(bootstrap_with=cl) as sol:
  sat=sol.solve();selected=[e for e,v in vid.items() if sol.get_model()[v-1]>0] if sat else []
 local.append(dict(direction=direction,sat=sat,good_squares=sorted(goodS),edges=selected))
 print('local',direction,sat,flush=True)
(ROOT/'gap/verifier/claim38_clean.json').write_text(json.dumps(dict(tours=results,local=local),indent=2))
