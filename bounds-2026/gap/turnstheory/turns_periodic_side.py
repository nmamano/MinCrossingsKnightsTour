"""Enumerate periodic zero-slack side windows; x>=4 is straight.
The y period is lifted: distinct move directions remain distinct even for P=1.
"""
import argparse,json,time
from itertools import combinations
from pathlib import Path
from ortools.sat.python import cp_model
from turns_gap_scan import M,sidecost,turn
ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=8);ap.add_argument('--period',type=int,default=1);ap.add_argument('--limit',type=int,default=200);a=ap.parse_args();W,P=a.width,a.period
m=cp_model.CpModel();pv={};inc={}
for x in range(W):
 for y in range(P):
  opts=[]
  for ds in combinations([d for d in M if x+d[0]>=0],2):
   if sidecost(x,ds):continue
   z=m.NewBoolVar('');pv[(x,y),ds]=z;opts.append(z)
   for d in ds:inc.setdefault(((x,y),d),[]).append(z)
  m.AddExactlyOne(opts)
for (p,d),vs in inc.items():
 q=p[0]+d[0],(p[1]+d[1])%P
 if q[0]<W:m.Add(sum(vs)==sum(inc.get((q,(-d[0],-d[1])),[])))
records=[];start=time.monotonic();status=''
for i in range(a.limit):
 s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=5;st=s.Solve(m);status=s.StatusName(st)
 if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
 chosen={p:ds for (p,ds),z in pv.items() if s.Value(z)}
 for p,ds in chosen.items():
  assert sidecost(p[0],ds)==0
  for dx,dy in ds:
   q=p[0]+dx,(p[1]+dy)%P
   if q in chosen:assert (-dx,-dy) in chosen[q]
 counts=[sum(turn(chosen[x,y]) for x in range(4)) for y in range(P)]
 assert sum(counts)==2*P
 records.append(dict(chosen=[[p,*ds] for p,ds in sorted(chosen.items())],row_turns=counts))
 m.Add(sum(pv[p,ds] for p,ds in chosen.items())<=len(chosen)-1)
report=dict(date='2026-10-04',width=W,period=P,count=len(records),status=status,exhaustive=status=='INFEASIBLE',seconds=time.monotonic()-start,patterns=records)
Path(__file__).with_name(f'turns_side_W{W}_P{P}.json').write_text(json.dumps(report,indent=2))
print({k:v for k,v in report.items() if k!='patterns'},flush=True)
