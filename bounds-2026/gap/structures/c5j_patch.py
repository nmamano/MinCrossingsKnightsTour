# KT Structures, 2026-10-03. BEYOND5 13.4 test: is the U collar J-minimal among pairing-preserving fillings?
# Pairing / no-cycle model copied from Verifier gap/verifier/claim45_U_gadget.py. Objective: 2 J of the window =
# 2 X3 + Q3 (X3: crossing pairs whose two edges both have an end at x <= 2; Q3 in squares x = 0..4: hole 1,
# W3 binom(m-1, 2), X1 1 at the single shared quarter of a crossing pair when m = 2). Rows -4..H+3 counted.
# usage (research root): c5j_patch.py H secs
import sys,json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'));sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'verifier'))
from check import MOVES
from claim9_tiles import proper
from claim38_switch import edge,qs
from ortools.sat.python import cp_model
import os
W=int(os.environ.get('W','6'));H=int(sys.argv[1]);SECS=float(sys.argv[2])
V={(x,y) for x in range(W) for y in range(H)}
def pn(v,sign=1):
 x,y=v
 if x==0:return {(2,y+sign),(1,y-2*sign)}
 if x==1:return {(3,y+sign),(0,y+2*sign)}
 return {(x+2,y+sign),(x-2,y-sign)}
base={edge(v,w) for x in range(W+9) for y in range(-7,H+7) for v in [(x,y)] for w in pn(v)}
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

def literal(e):return ev[e] if e in ev else int(e in fixed)
Y0,Y1=-4,H+3
universe=sorted(set(ev)|{e for e in fixed if min(e[0][1],e[1][1])>=Y0-3 and max(e[0][1],e[1][1])<=Y1+3})
def tq(e):return set(qs(e))
cost=[];BASEVAL=0
def val_base(e):return int(e in base)
# X3 crossings
x3e=[e for e in universe if min(e[0][0],e[1][0])<=2]
for i,e in enumerate(x3e):
 for f in x3e[i+1:]:
  if not proper(e,f):continue
  if not any(Y0<=v[1]<=Y1 for v in e+f):continue
  if e not in ev and f not in ev:continue
  BASEVAL+=2*val_base(e)*val_base(f)
  le,lf=literal(e),literal(f)
  if isinstance(le,int) or isinstance(lf,int):
   if (le if isinstance(le,int) else lf):cost.append(2*(lf if isinstance(le,int) else le))
  else:
   z=m.NewBoolVar('');m.AddBoolOr([le.Not(),lf.Not(),z]);cost.append(2*z)
# quarters
cov=defaultdict(list)
for e in universe:
 for q in qs(e):cov[q].append(e)
quarters=[(x,y,k) for x in range(0,5) for y in range(Y0,Y1+1) for k in range(4)]
for q in quarters:
 es=cov[q]
 if not any(e in ev for e in es):continue
 mb=sum(val_base(e) for e in es)
 BASEVAL+=(mb==0)+(max(0,(mb-1)*(mb-2)//2) if mb>=3 else 0)
 mm=sum(literal(e) for e in es)
 h=m.NewBoolVar('');m.Add(mm>=1).OnlyEnforceIf(h.Not());cost.append(h)
 w3=m.NewIntVar(0,10,'');m.Add(w3>=mm-2);m.Add(w3>=2*mm-5);m.Add(w3>=3*mm-9);cost.append(w3)
 b2=m.NewBoolVar('');m.Add(mm<=2).OnlyEnforceIf(b2.Not()) if False else None
 # b2 may be 1 only if mm == 2 is false?  we need a LOWER bound on X1: y >= le + lf + [mm == 2] - 2
 eq2=m.NewBoolVar('');m.Add(mm==2).OnlyEnforceIf(eq2);m.Add(mm!=2).OnlyEnforceIf(eq2.Not())
 for i,e in enumerate(es):
  for f in es[i+1:]:
   if len(tq(e)&tq(f))!=1 or not proper(e,f):continue
   if mb==2 and val_base(e) and val_base(f):BASEVAL+=1
   y=m.NewBoolVar('');m.Add(y>=literal(e)+literal(f)+eq2-2);cost.append(y)
# deep squares (x >= 5): every bad quarter (m != 1) counts 1 (BQx units; C5-J = 2J + BQx - 2K)
for q in [(x,y,k) for x in range(5,W+3) for y in range(Y0,Y1+1) for k in range(4)]:
 es=cov[q]
 if not any(e in ev for e in es):continue
 mb=sum(val_base(e) for e in es);BASEVAL+=int(mb!=1)
 mm=sum(literal(e) for e in es)
 bad=m.NewBoolVar('');m.Add(mm==1).OnlyEnforceIf(bad.Not());cost.append(bad)
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
m.Minimize(sum(cost))
if len(sys.argv)>3:
 gj=json.loads(Path(sys.argv[3]).read_text());rem={edge(tuple(a),tuple(b)) for a,b in gj['remove']};add={edge(tuple(a),tuple(b)) for a,b in gj['add']}
 target=(basein-rem)|add
 for e,v in ev.items():m.Add(v==int(e in target))
for e,v in ev.items():m.AddHint(v,int(e in base))
s=cp_model.CpSolver();s.parameters.num_workers=2;s.parameters.max_time_in_seconds=SECS
st=s.Solve(m)
print('W',W,'H',H,s.StatusName(st),'2J new',s.ObjectiveValue(),'bound',s.BestObjectiveBound(),'2J base',BASEVAL,'change per row',(s.ObjectiveValue()-BASEVAL)/2/H,flush=True)
sel={e for e,v in ev.items() if s.Value(v)}
Path(f'gap/structures/c5j_patch_W{W}_H{H}.json').write_text(json.dumps(dict(H=H,status=s.StatusName(st),obj=s.ObjectiveValue(),base=BASEVAL,remove=sorted(basein-sel),add=sorted(sel-basein))))
