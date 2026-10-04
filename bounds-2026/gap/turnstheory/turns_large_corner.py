"""Integer rerun of w-turnstheory/corner_integer_large.py; lazy internal-cycle cuts.
Adds the audited redundant residual >= -7 bound. Saves raw status and witnesses.
"""
import argparse,json,time
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import ortools
from ortools.sat.python import cp_model
M=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
def lower(x,ds):
 if x==0:return 1
 if x in (1,2):return sum(x+d in (0,3) for d in ds)-1
 if x==3:return 1-sum(x+d in (1,2) for d in ds)
 return 0
ap=argparse.ArgumentParser();ap.add_argument('K',type=int);ap.add_argument('--seconds',type=float,default=120);ap.add_argument('--workers',type=int,default=2);ap.add_argument('--trials',type=int,default=10);ap.add_argument('--tight',action='store_true');args=ap.parse_args();K=args.K
alpha={(0,0):-1,(0,3):-1,(1,1):1,(1,3):-1,(2,3):-1,(3,0):-1,(3,1):-1,(3,2):-1,(3,3):-1}
beta={((0,1),(1,3)):-1,((0,2),(2,3)):-1,((0,3),(1,1)):1,((1,0),(3,1)):-1,((1,1),(3,0)):-1,((1,2),(3,3)):-1,((2,0),(3,2)):-1,((2,1),(3,3)):-1,((2,2),(3,0)):-1}
C={(x,y) for x in range(K) for y in range(K)};m=cp_model.CpModel();pv={};inc=defaultdict(list);cost=[]
for p in sorted(C):
 opts=[]
 for a,b in combinations([d for d in M if p[0]+d[0]>=0 and p[1]+d[1]>=0],2):
  t=int((a[0]+b[0],a[1]+b[1])!=(0,0))
  r=t-lower(p[0],[a[0],b[0]])-lower(p[1],[a[1],b[1]])
  base=alpha.get(p,0) if max(p)<4 else 0
  if max(p)<4:
   for d in (a,b):
    q=p[0]+d[0],p[1]+d[1];e=tuple(sorted((p,q)));base+=beta.get(e,0)*(1 if p<q else -1)
  assert r>=base
  if args.tight and r!=base:continue
  z=m.NewBoolVar('');pv[p,a,b]=z;opts.append(z)
  for d in (a,b):inc[p,(p[0]+d[0],p[1]+d[1])].append(z)
  t=int((a[0]+b[0],a[1]+b[1])!=(0,0))
  cost.append((t-lower(p[0],[a[0],b[0]])-lower(p[1],[a[1],b[1]]))*z)
 m.AddExactlyOne(opts)
for p,q in sorted({tuple(sorted((p,q))) for p,q in inc if q in C}):
 m.Add(sum(inc[p,q])==sum(inc[q,p]))
m.Add(sum(cost)>=-7);m.Minimize(sum(cost))
report=dict(date='2026-10-04',K=K,workers=args.workers,seconds_per_trial=args.seconds,ortools_version=ortools.__version__,redundant_audited_bound=-7,tight=args.tight,trials=[],cycle_cuts=0)
out=Path(__file__).with_name(f'turns_corner_integer_K{K}'+('_tight' if args.tight else '')+'.json');start=time.monotonic()
for trial in range(args.trials):
 s=cp_model.CpSolver();s.parameters.num_workers=args.workers;s.parameters.max_time_in_seconds=args.seconds
 st=s.Solve(m);record=dict(trial=trial,status=s.StatusName(st),objective=s.ObjectiveValue(),bound=s.BestObjectiveBound(),seconds=s.WallTime());report['trials'].append(record)
 if st not in (cp_model.FEASIBLE,cp_model.OPTIMAL):
  print(json.dumps(record),flush=True);break
 chosen=[(p,a,b) for (p,a,b),v in pv.items() if s.Value(v)];adj={p:[] for p in C}
 for p,a,b in chosen:
  for dx,dy in (a,b):
   q=p[0]+dx,p[1]+dy
   if q in C:adj[p].append(q)
 seen=set();cycles=[]
 for p in sorted(C):
  if p in seen:continue
  stack=[p];cc=set()
  while stack:
   v=stack.pop()
   if v in cc:continue
   cc.add(v);stack.extend(adj[v])
  seen|=cc
  if all(len(adj[v])==2 for v in cc):cycles.append(cc)
 record['internal_cycle_lengths']=list(map(len,cycles));print(json.dumps(record),flush=True)
 if not cycles:
  report.update(chosen=chosen,residual=s.ObjectiveValue(),status=s.StatusName(st),bound=s.BestObjectiveBound())
  if s.ObjectiveValue()==-7 or st==cp_model.OPTIMAL:break
 else:
  for cc in cycles:
   es=[sum(inc[p,q]) for p in cc for q in adj[p] if p<q]
   m.Add(sum(es)<=len(cc)-1);report['cycle_cuts']+=1
 report['elapsed_seconds']=time.monotonic()-start;out.write_text(json.dumps(report,indent=2))
report['elapsed_seconds']=time.monotonic()-start;out.write_text(json.dumps(report,indent=2))
print('SAVED',out,'elapsed',report['elapsed_seconds'],flush=True)
