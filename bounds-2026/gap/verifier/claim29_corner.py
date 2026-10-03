"""Free outer ports, exact degree corner core; search a private-price deficit.
All retained radii 3..k-4 are charged. Count every non-B crossing in the patch.
This is a patch test, not an all-tour theorem or counterexample.
"""
from claim29_window import edge,cross
from claim26_certificate import TERMS,EXC
from collections import defaultdict
from itertools import combinations
from ortools.sat.python import cp_model
from pathlib import Path
import json,time
moves=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
def run(k):
 core={(x,y) for x in range(k) for y in range(k)}
 es=sorted({edge(a,(a[0]+dx,a[1]+dy)) for a in core for dx,dy in moves if a[0]+dx>=0 and a[1]+dy>=0})
 m=cp_model.CpModel();vs=[m.new_bool_var('') for e in es];ind={e:i for i,e in enumerate(es)};inc=defaultdict(list)
 for e,v in zip(es,vs):
  for a in e:inc[a].append(v)
 for a,lst in inc.items():m.add(sum(lst)==2) if a in core else m.add(sum(lst)<=2)
 terms=[]
 for i,e in enumerate(es):
  for j in range(i):
   f=es[j]
   if not cross(e,f):continue
   isB=any(any(a[axis]==0 for a in e) and any(a[axis]==0 for a in f) for axis in (0,1))
   if isB:continue
   v=m.new_bool_var('cross');m.add(v>=vs[i]+vs[j]-1);terms.append(v)
 radii=list(range(3,k-3))
 for r in radii:
  fs=[]
  for transpose in (False,True):
   def tr(a):
    a=(a[0],a[1]+r)
    return (a[1],a[0]) if transpose else a
   fs.append(sum(c*vs[ind[edge(tr(a),tr(b))]] for a,b,c in TERMS))
   m.add(sum(vs[ind[edge(tr(a),tr(b))]] for a,b in EXC)<=1)
  c=1-2*(r%2);q=m.new_int_var(-20,20,'q');res=m.new_int_var(1,2,'charged')
  m.add(1+c+c*(sum(fs)+4)==3*q+res)
 limit=(2*len(radii)-1)//3
 m.add(sum(terms)<=limit)
 s=cp_model.CpSolver();s.parameters.num_workers=2;s.parameters.max_time_in_seconds=15
 t=time.monotonic();st=s.solve(m)
 out=dict(k=k,radii=radii,crossing_cap=limit,status=s.status_name(st),seconds=time.monotonic()-t)
 if st in (cp_model.FEASIBLE,cp_model.OPTIMAL):
  chosen=[e for e,v in zip(es,vs) if s.value(v)]
  pairs=[(e,f) for e,f in combinations(chosen,2) if cross(e,f)]
  B=lambda e,f:any(any(a[axis]==0 for a in e) and any(a[axis]==0 for a in f) for axis in (0,1))
  I=sum(not B(e,f) for e,f in pairs);assert I<=limit
  # Diagnose finite cycles; a patch with one cannot be used in a larger tour.
  graph=defaultdict(list)
  for a,b in chosen:graph[a].append(b);graph[b].append(a)
  seen=set();cycles=0
  for a in graph:
   if a in seen:continue
   todo=[a];component=set()
   while todo:
    v=todo.pop()
    if v in component:continue
    component.add(v);todo.extend(graph[v])
   seen|=component;cycles+=all(len(graph[v])==2 for v in component)
  out.update(edges=chosen,nonB=I,finite_cycles=cycles)
 return out
results=[]
for k in (8,12):
 a=run(k);results.append(a);print({k:v for k,v in a.items() if k!='edges'},flush=True)
Path('gap/verifier/claim29_corner.json').write_text(json.dumps(results,indent=2))
