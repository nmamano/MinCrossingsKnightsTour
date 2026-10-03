"""Finite P-collar replacement with unchanged exterior pairing. One CP-SAT worker."""
import sys,json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import MOVES
from claim9_tiles import proper
from claim38_switch import edge,qs
from ortools.sat.python import cp_model
W,H=6,int(sys.argv[1]) if len(sys.argv)>1 else 24
V={(x,y) for x in range(W) for y in range(H)}
def pn(v,sign=1):
 x,y=v
 if x==0:return {(2,y+sign),(1,y-2*sign)}
 if x==1:return {(3,y+sign),(0,y+2*sign)}
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
# Exact strong up rows; all geometric visibility templates from Claim 42.
from claim26_certificate import TERMS,EXC
vp=json.loads(Path('gap/verifier/claim42_geometry.json').read_text())['VIS_pairs']
def literal(e):return ev[e] if e in ev else int(e in fixed)
def conjunction(ls):
 if any(isinstance(v,int) and v==0 for v in ls):return 0
 ls=[v for v in ls if not isinstance(v,int)]
 if not ls:return 1
 z=m.NewBoolVar('and');m.AddBoolAnd(ls).OnlyEnforceIf(z);m.AddBoolOr([v.Not() for v in ls]+[z]);return z
g={}
for r in range(-5,H+6):
 tr=lambda p:(p[0],p[1]+r)
 ff=sum(c*literal(edge(tr(a),tr(b))) for a,b,c in TERMS)
 rem=m.NewIntVar(0,2,'rem');m.AddModuloEquality(rem,ff+12,3)
 fail=m.NewBoolVar('fail');m.Add(rem!=2).OnlyEnforceIf(fail);m.Add(rem==2).OnlyEnforceIf(fail.Not())
 ee=conjunction([literal(edge(tr(a),tr(b))) for a,b in EXC])
 vv=[conjunction([literal(edge(tr(a),tr(b))) for a,b in pair[:2]]) for pair in vp]
 z=m.NewBoolVar('g');m.AddMaxEquality(z,[fail,ee,*vv]);g[r]=z
# Minimise an upper bound: charge every strip-cut port, including unchanged ones.
# Half of C5-W, scaled by 6, at a=2 and c1=2/3.
terms=[12*z for z in g.values()]
for e in sorted(internal | fixed):
 a,b=e
 if (a[0]<3)==(b[0]<3):continue
 o=a if a[0]<3 else b
 r=o[1]
 if not -3<=r<H+4:continue
 active=literal(e)
 far=m.NewBoolVar('far');m.AddMaxEquality(far,[g[r-1],g[r],g[r+1]])
 on=conjunction([active,g[r].Not()])
 farport=conjunction([active,far.Not()])
 terms.extend([4*on,2*farport])
obj=sum(terms)
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
m.Minimize(obj)
s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=40
for attempt in range(1):
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
 out=dict(W=W,H=H,status=s.StatusName(status),objective=s.ObjectiveValue(),grows=[r for r,z in g.items() if s.Value(z)],remove=sorted(basein-selected),add=sorted(selected-basein),connections=connections)
 Path(f'gap/verifier/claim47_U_gadget_{H}.json').write_text(json.dumps(out,indent=2));print(out,flush=True);break
