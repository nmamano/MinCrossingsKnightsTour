"""Light local hole search, arbitrary degree-two core and degree<=2 halo."""
import sys,json,time
from pathlib import Path
from itertools import combinations
from collections import defaultdict,Counter
from ortools.sat.python import cp_model
sys.path.insert(0,'w-verifier')
from claim9_tiles import quarters
from claim26_certificate import edge,cross

def tile(e):
 a,b=e;d=(b[0]-a[0],b[1]-a[1])
 return {(x+a[0],y+a[1],k) for x,y,k in quarters(((0,0),d))}
def run(k):
 core={(x,y) for x in range(k) for y in range(k)}
 moves=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
 es=sorted({edge(a,(a[0]+dx,a[1]+dy)) for a in core for dx,dy in moves})
 m=cp_model.CpModel();vs=[m.new_bool_var('') for e in es];inc=defaultdict(list)
 for i,e in enumerate(es):
  for a in e:inc[a].append(vs[i])
 for a,lst in inc.items():m.add(sum(lst)==2) if a in core else m.add(sum(lst)<=2)
 for i,e in enumerate(es):
  for j in range(i):
   if cross(e,es[j]):m.add(vs[i]+vs[j]<=1)
 target=(k//2,k//2,0)
 for v,e in zip(vs,es):
  if target in tile(e):m.add(v==0)
 s=cp_model.CpSolver();s.parameters.num_workers=2;s.parameters.max_time_in_seconds=15
 start=time.monotonic();status=s.solve(m)
 out=dict(k=k,status=s.status_name(status),seconds=time.monotonic()-start,target=target)
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  chosen=[e for e,v in zip(es,vs) if s.value(v)]
  assert not any(cross(e,f) for e,f in combinations(chosen,2))
  assert all(sum(a in e for e in chosen)==2 for a in core)
  assert not any(target in tile(e) for e in chosen)
  out['edges']=chosen
 return out
if __name__=='__main__':
 r=[]
 for k in (6,8):
  a=run(k);r.append(a);print({k:v for k,v in a.items() if k!='edges'},flush=True)
 Path('gap/verifier/claim29_windows.json').write_text(json.dumps(r,indent=2))
