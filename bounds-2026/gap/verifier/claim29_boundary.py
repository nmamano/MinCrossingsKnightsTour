"""Hole near retained endpoint: permit B crossings only, exclude inward exception."""
from claim29_window import tile,edge,cross
from collections import defaultdict
from itertools import combinations
from ortools.sat.python import cp_model
from pathlib import Path
import json,time
moves=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
core={(x,y) for x in range(6) for y in range(8)}
es=sorted({edge(a,(a[0]+dx,a[1]+dy)) for a in core for dx,dy in moves if a[0]+dx>=0})
results=[]
for quarter in range(4):
 m=cp_model.CpModel();vs=[m.new_bool_var('') for e in es];inc=defaultdict(list)
 for e,v in zip(es,vs):
  for a in e:inc[a].append(v)
 for a,lst in inc.items():m.add(sum(lst)==2) if a in core else m.add(sum(lst)<=2)
 for i,e in enumerate(es):
  for j in range(i):
   f=es[j]
   if cross(e,f) and not(any(x==0 for x,y in e) and any(x==0 for x,y in f)):m.add(vs[i]+vs[j]<=1)
 target=(1,4,quarter)
 for e,v in zip(es,vs):
  if target in tile(e):m.add(v==0)
 exc=[edge((0,4),(2,5)),edge((0,5),(2,4))]
 m.add(sum(vs[es.index(e)] for e in exc)<=1)
 s=cp_model.CpSolver();s.parameters.num_workers=2;s.parameters.max_time_in_seconds=10
 t=time.monotonic();st=s.solve(m)
 result=dict(quarter=quarter,status=s.status_name(st),seconds=time.monotonic()-t)
 if st in (cp_model.FEASIBLE,cp_model.OPTIMAL):
  chosen=[e for e,v in zip(es,vs) if s.value(v)]
  assert all(any(x==0 for x,y in e) and any(x==0 for x,y in f) for e,f in combinations(chosen,2) if cross(e,f))
  result['edges']=chosen
 results.append(result);print({k:v for k,v in result.items() if k!='edges'},flush=True)
Path('gap/verifier/claim29_boundary.json').write_text(json.dumps(results,indent=2))
