# KT Structures, 2026-10-03. BEYOND5 12.3 red team: adaptation of Verifier gap/verifier/claim45_U_gadget.py (same
# pairing-preserving U-collar replacement model, exact UP strong rows, internal cycles excluded). New objective: minimise
# the (C5-W) weight of rows -3..H+2: per row 2a g + 2 p (1 on far rows, c1 at distance 1, 0 on g rows), p = ports whose
# collar end is in that row. Baseline U collar: 4 per row. usage (from the research root): c5w_gadget.py H a c1 secs
import sys,json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'));sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'verifier'))
from check import MOVES
from claim9_tiles import proper
from claim38_switch import edge,qs
from ortools.sat.python import cp_model
from fractions import Fraction as Fr
W=6;H=int(sys.argv[1]);A=Fr(sys.argv[2]);C1=Fr(sys.argv[3]);SECS=float(sys.argv[4])
# optional: BH BF = distance-1 port weights on rows with / without a p24 port (2,r)-(4,r+-1); then C1 is unused
BH=Fr(sys.argv[5]) if len(sys.argv)>5 else None;BF=Fr(sys.argv[6]) if len(sys.argv)>6 else None
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
# ports per row: edges with one end at x<=2 and the other at x>=3; collar end row r
def pedges(r):
 out=[]
 for e in set(ev)|fixed:
  a,b=e
  if (a[0]<=2)!=(b[0]<=2):
   c=a if a[0]<=2 else b
   if c[1]==r:out.append(literal(e))
 return out
S6=6  # scale: weights times 6
terms=[];BASE=0
for r in range(-3,H+3):
 ps=pedges(r);p=sum(ps)
 d1=m.NewBoolVar('d1');m.AddMaxEquality(d1,[g[r-1],g[r+1]])
 near=m.NewBoolVar('near');m.AddBoolAnd([d1,g[r].Not()]).OnlyEnforceIf(near);m.AddBoolOr([d1.Not(),g[r]]).OnlyEnforceIf(near.Not())
 pg=m.NewIntVar(0,6,'pg');pn_=m.NewIntVar(0,6,'pn')
 m.AddMultiplicationEquality(pg,[p if not isinstance(p,int) else m.NewConstant(p),g[r]]) if not isinstance(p,int) else m.Add(pg==p*g[r])
 m.AddMultiplicationEquality(pn_,[p,near]) if not isinstance(p,int) else m.Add(pn_==p*near)
 # 6 * (2a g + 2 p - 2 p g - 2 (1 - c1) p near)
 if BH is None:
  terms.append(int(12*A)*g[r]+12*p-12*pg-int(12*(1-C1))*pn_)
 else:
  hl=[literal(edge((2,r),(4,r+1))),literal(edge((2,r),(4,r-1)))]
  if any(isinstance(v,int) and v==1 for v in hl):h=1
  else:
   hl=[v for v in hl if not isinstance(v,int)]
   if not hl:h=0
   else:h=m.NewBoolVar('h');m.AddMaxEquality(h,hl)
  if isinstance(h,int):nh=near if h else 0
  else:nh=m.NewBoolVar('nh');m.AddMultiplicationEquality(nh,[near,h])
  pnh=m.NewIntVar(0,6,'pnh')
  if isinstance(nh,int):m.Add(pnh==0)
  elif isinstance(p,int):m.Add(pnh==p*nh)
  else:m.AddMultiplicationEquality(pnh,[p,nh])
  # near ports: weight BH on p24 rows, BF otherwise -> loss (1-BH) pnh + (1-BF)(pn_-pnh)
  terms.append(int(12*A)*g[r]+12*p-12*pg-int(12*(1-BH))*pnh-int(12*(1-BF))*(pn_-pnh))
 BASE+=24
obj=sum(terms)
m.Add(sum(g[r] for r in range(0,H))>=1)
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
s=cp_model.CpSolver();s.parameters.num_workers=2;s.parameters.max_time_in_seconds=SECS
for attempt in range(20):
 status=s.Solve(m)
 print(s.StatusName(status),'weight/6',s.ObjectiveValue()/6,'bound/6',s.BestObjectiveBound()/6,'U baseline/6',BASE/6,'rows',H+6,flush=True)
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
 Path(f'gap/structures/c5w_gadget_H{H}_a{A}_c{C1}_bh{BH}_bf{BF}.json'.replace('/','_').replace('gap_structures_','gap/structures/')).write_text(json.dumps(out,indent=2));print('g rows',out['grows'],'loss per row',(BASE-s.ObjectiveValue())/6/(H+6),flush=True);break
