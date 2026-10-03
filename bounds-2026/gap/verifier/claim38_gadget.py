"""Finite P-collar replacement with unchanged exterior pairing. One CP-SAT worker."""
import sys,json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import MOVES
from claim9_tiles import proper
from claim38_switch import edge,qs
from ortools.sat.python import cp_model
W,H=6,16
V={(x,y) for x in range(W) for y in range(H)}
def pn(v,sign=1):
 x,y=v
 if x==0:return {(2,y+sign),(1,y+2*sign)}
 if x==1:return {(3,y+sign),(0,y-2*sign)}
 return {(x+2,y+sign),(x-2,y-sign)}
base={edge(v,w) for x in range(W+5) for y in range(-7,H+7) for v in [(x,y)] for w in pn(v)}
internal={edge(v,(v[0]+dx,v[1]+dy)) for v in V for dy,dx in MOVES if (v[0]+dx,v[1]+dy) in V}
fixed={e for e in base if not all(v in V for v in e)}
basein=base&internal
adj=defaultdict(set)
for a,b in basein:adj[a].add(b);adj[b].add(a)
port=defaultdict(list)
for e in fixed:
 for v in e:
  if v in V:port[v].append(e)
seen=set();comps=[];pids={}
for v in sorted(V):
 if v in seen:continue
 stack=[v];co={v};seen.add(v)
 while stack:
  z=stack.pop()
  for w in adj[z]:
   if w not in seen:seen.add(w);co.add(w);stack.append(w)
 ps=[p for p in co for _ in port[p]];assert len(ps)==2
 for p in ps:pids[p]=len(comps)
 comps.append(co)
m=cp_model.CpModel();ev={e:m.NewBoolVar('e') for e in sorted(internal)}
inc=defaultdict(list)
for e,v in ev.items():
 for p in e:inc[p].append(v)
labels={p:m.NewIntVar(0,len(comps)-1,'label') for p in V}
for p in V:
 m.Add(sum(inc[p])==2-len(port[p]))
 if p in pids:m.Add(labels[p]==pids[p])
for (a,b),v in ev.items():m.Add(labels[a]==labels[b]).OnlyEnforceIf(v)
# Crossing count difference relative to the P field, only pairs affected by variable edges.
xe=[];xc=0
for e,v in ev.items():
 for f in fixed:
  if proper(e,f):xe.append(v);xc+=e in basein
for i,e in enumerate(sorted(ev)):
 for f in sorted(ev)[:i]:
  if proper(e,f):
   z=m.NewBoolVar('cross');m.AddMultiplicationEquality(z,[ev[e],ev[f]]);xe.append(z)
   xc+=e in basein and f in basein
# Interior bad quarters; all other affected quarters have x < 3.
own=defaultdict(list);cnt=defaultdict(int)
for e,v in ev.items():
 for q in qs(e):own[q].append(v)
for e in fixed:
 for q in qs(e):cnt[q]+=1
bq=[]
for q,vs in own.items():
 if q[0]<3:continue
 z=m.NewBoolVar('bad');m.Add(sum(vs)+cnt[q]!=1).OnlyEnforceIf(z);m.Add(sum(vs)+cnt[q]==1).OnlyEnforceIf(z.Not());bq.append(z)
# Exact P/P' slot windows, including slots just outside the replacement box.
exc=[]
for y in range(-3,H+3):
 tests=[]
 for sign in (1,-1):
  lits=[];impossible=False
  for x in range(3):
   for j in range(y-3,y+4):
    p=(x,j);want={edge(p,w) for w in pn(p,sign)}
    for e in want:
     if e not in fixed and e not in ev:impossible=True
    if any(p in e and e not in want for e in fixed):impossible=True
    for e,v in ev.items():
     if p in e:lits.append(v if e in want else v.Not())
  t=m.NewBoolVar('cheap');tests.append(t)
  if impossible:m.Add(t==0)
  else:
   m.AddBoolAnd(lits).OnlyEnforceIf(t);m.AddBoolOr([v.Not() for v in lits]+[t])
 z=m.NewBoolVar('exc');m.AddBoolAnd([v.Not() for v in tests]).OnlyEnforceIf(z);m.AddBoolOr(tests).OnlyEnforceIf(z.Not());exc.append(z)
# A rooted forest on each labelled path excludes internal cycles.
roots={min(co & set(pids)) for co in comps}
ranks={v:m.NewIntVar(0,W*H,'rank') for v in V}
parents=defaultdict(list)
for (a,b),v in ev.items():
 for child,parent in ((a,b),(b,a)):
  if child in roots:continue
  z=m.NewBoolVar('parent');m.Add(z<=v);m.Add(ranks[child]>ranks[parent]).OnlyEnforceIf(z);parents[child].append(z)
for v in V:
 if v in roots:m.Add(ranks[v]==0)
 else:m.Add(sum(parents[v])==1)
obj=4*(sum(xe)-xc)-sum(bq)-4*sum(exc)
m.Add(obj<=-1)
m.Minimize(obj)
if '--replay' in sys.argv:
 witness=json.loads(Path('gap/verifier/claim38_gadget.json').read_text())
 removed={edge(tuple(a),tuple(b)) for a,b in witness['remove']}
 added={edge(tuple(a),tuple(b)) for a,b in witness['add']}
 selected=basein-removed|added
 for e,v in ev.items():m.Add(v==int(e in selected))
s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=35
for attempt in range(5):
 status=s.Solve(m)
 print(s.StatusName(status),s.ObjectiveValue(),s.BestObjectiveBound(),flush=True)
 if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
 selected={e for e,v in ev.items() if s.Value(v)};na=defaultdict(set)
 for a,b in selected:na[a].add(b);na[b].add(a)
 vis=set();cycles=[];connections=[]
 for v in V:
  if v in vis:continue
  stack=[v];co={v};vis.add(v)
  while stack:
   z=stack.pop()
   for w in na[z]:
    if w not in vis:vis.add(w);co.add(w);stack.append(w)
  ps=[p for p in co for _ in port[p]]
  if not ps:cycles.append(co)
  else:assert len(ps)==2 and pids[ps[0]]==pids[ps[1]];connections.append(ps)
 if cycles:
  for co in cycles:m.Add(sum(ev[e] for e in selected if all(p in co for p in e))<=len(co)-1)
  continue
 out=dict(W=W,H=H,status=s.StatusName(status),objective=s.ObjectiveValue(),deltaX=sum(s.Value(v) for v in xe)-xc,BQ=sum(s.Value(v) for v in bq),EXC=sum(s.Value(v) for v in exc),remove=sorted(basein-selected),add=sorted(selected-basein),connections=connections)
 Path('gap/verifier/claim38_gadget.json').write_text(json.dumps(out,indent=2));print(out,flush=True);break
