"""Exact S* union counts on the five audited Claim 36 FOLD tours.
N_re=2n+2 and BQ data come from Structures' saved census; this does not
re-audit its port-partner definition or prove an infinite-family formula.
"""
import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
from collections import defaultdict
from itertools import combinations
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'w-verifier'))
sys.path.insert(0,str(ROOT/'w-turnstheory'))
from check import MOVES,proper
from check_knight_tiles import microtiles
TILES={d:microtiles(((0,0),d)) for d in ((1,2),(1,-2),(2,1),(2,-1))}
files=['w-integrator/tours/FOLD24_n96.json']+[f'gap/verifier/claim36_FOLD_n{n}.json' for n in (144,192,240,288)]
out=[]
for file in files:
 data=json.loads((ROOT/file).read_text());grid=data['tour'];n=len(grid)
 def mask(e):
  return sum(1<<(2*k+side) for k in (0,1) for side in (0,1)
             if any((p[k]<=1 if side==0 else p[k]>=n-2) for p in e))
 es=set()
 for y,row in enumerate(grid):
  for x,code in enumerate(row):
   if 3<=x<n-3 and 3<=y<n-3:continue
   for ch in code:
    dy,dx=MOVES[int(ch)]
    e=tuple(sorted(((x,n-1-y),(x+dx,n-1-y-dy))))
    if mask(e):es.add(e)
 es=sorted(es);masks=list(map(mask,es));buckets=defaultdict(list)
 for i,(a,b) in enumerate(es):
  for x,y,k in TILES[b[0]-a[0],b[1]-a[1]]:buckets[x+a[0],y+a[1],k].append(i)
 pairs={tuple(sorted((a,b))) for ids in buckets.values() for a,b in combinations(ids,2) if masks[a]&masks[b]}
 assert all(proper(es[a],es[b]) for a,b in pairs)
 s=len(pairs);T=s-4*n+2;Nre=2*n+2
 row=dict(source=file,n=n,S_union=s,T=T,N_re_reported=Nre,T_minus_N_re=T-Nre)
 out.append(row);print(json.dumps(row))
(ROOT/'gap/turnstheory/shared_dstar_check.json').write_text(json.dumps(out,indent=2)+'\n')
