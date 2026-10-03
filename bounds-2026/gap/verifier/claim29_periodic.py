"""Search an extendible B-only endpoint-hole strip; no full-tour claim."""
from claim29_window import edge,cross,tile
from collections import defaultdict
from itertools import combinations
from ortools.sat.python import cp_model
from pathlib import Path
import json,time

def run(W,p,d):
 dx,dy=d;cells={(x,y) for x in range(W) for y in range(p)}
 es=[((x,y),(xx,y+yy)) for x,y in sorted(cells) for xx in range(x+1,W) for yy in (-2,-1,1,2) if sorted((xx-x,abs(yy)))==[1,2]]
 forced=[((x,y),(x+dx,y+dy)) for x,y in sorted(cells) if x+dx>=W]
 m=cp_model.CpModel();vs=[m.new_bool_var('') for e in es];inc=defaultdict(list)
 wrap=lambda a:(a[0],a[1]%p)
 for e,v in zip(es,vs):
  for a in e:inc[wrap(a)].append(v)
 for a in cells:m.add(sum(inc[a])==2-int(a[0]+dx>=W))
 allE=es+forced;copies=[]
 for i,e in enumerate(allE):
  for k in range(-3,4):
   f=tuple((x,y+k*p) for x,y in e)
   if -2<=min(y for x,y in f)<p:copies.append((i,f))
 for (i,e),(j,f) in combinations(copies,2):
  if 0<=max(min(y for x,y in e),min(y for x,y in f))<p and cross(e,f):
   if any(x==0 for x,y in e) and any(x==0 for x,y in f):continue
   vi=vs[i] if i<len(es) else 1;vj=vs[j] if j<len(es) else 1
   m.add(vi+vj<=1)
 target=(1,0,1)
 for i,e in copies:
  if target in tile(edge(*e)):m.add((vs[i] if i<len(es) else 1)==0)
 exc=[edge((0,0),(2,1)),edge((0,1),(2,0))]
 terms=[]
 for i,e in copies:
  if edge(*e) in exc:terms.append(vs[i] if i<len(es) else 1)
 m.add(sum(terms)<=1)
 s=cp_model.CpSolver();s.parameters.num_workers=2;s.parameters.max_time_in_seconds=5
 t=time.monotonic();st=s.solve(m)
 out=dict(W=W,p=p,d=d,status=s.status_name(st),seconds=time.monotonic()-t)
 if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  out['edges']=[e for e,v in zip(es,vs) if s.value(v)]+forced
 return out
r=[]
for d in ((2,1),(2,-1),(1,2),(1,-2)):
 a=run(4,4,d);r.append(a);print({k:v for k,v in a.items() if k!='edges'},flush=True)
Path('gap/verifier/claim29_periodic.json').write_text(json.dumps(r,indent=2))
