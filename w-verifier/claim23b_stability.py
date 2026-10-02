"""Independent exact endpoint-state certificate using complete edge masks."""
from pathlib import Path
from itertools import product,combinations
from collections import defaultdict
from fractions import Fraction
import json
from claim11_forest import transitions,potentials
from claim11_corner import canon,M
from claim9_tiles import proper

def main():
 terms=json.loads(Path('w-verifier/claim18.json').read_text())['corner'][0]['left_terms']
 tests=[]
 for sign in (1,-1):
  tr=lambda p:(p[0],sign*p[1])
  coef={canon(tr(a),tr(b)):v for (a,b),v in terms}
  exc={canon(tr((0,0)),tr((2,1))),canon(tr((0,1)),tr((2,0)))}
  tests.append((coef,exc))
 universe=set()
 for x,y in product(range(4),range(-2,3)):
  for dx,dy in M:
   q=x+dx,y+dy
   if 0<=q[0]<4 and min(x,q[0])<2 and min(y,q[1])<=0<=max(y,q[1]):universe.add(canon((x,y),q))
 es=sorted(universe);bits={e:1<<i for i,e in enumerate(es)};assert len(es)==20
 def mask(edges):
  out=0
  for e in edges:out|=bits[e]
  return out
 def failures(seen):
  return tuple(int(sum(c for e,c in coef.items() if seen&bits[e])%3!=2 or all(seen&bits[e] for e in exc)) for coef,exc in tests)
 states=[(0,())];ids={states[0]:0};adj=[]
 for u,s in enumerate(states):
  best={}
  for t,w in transitions(s):
   if t not in ids:ids[t]=len(states);states.append(t)
   v=ids[t];best[v]=min(best.get(v,w),w)
  adj.append(list(best.items()))
 N=len(states);assert (N,sum(map(len,adj)))==(82516,144674)
 pm=[];last=[]
 for col,pend in states:
  pm.append(mask(canon(a,b) for a,b,c in pend))
  last.append(mask(canon((a[0],a[1]+1),(b[0],b[1]+1)) for a,b,c in pend) if col==0 else 0)
 nodes=[(u,0) for u in range(N) if states[u][0]==0];idx={s:i for i,s in enumerate(nodes)};arcs=[];charges=[]
 for i,(u,seen) in enumerate(nodes):
  sofar=seen|pm[u]
  for v,w in adj[u]:
   final=states[v][0]==0
   whole=sofar|(last[v] if final else pm[v])
   fail=failures(whole) if final else (0,0)
   key=(v,0 if final else whole)
   if key not in idx:idx[key]=len(nodes);nodes.append(key)
   arcs.append((i,idx[key],w));charges.append(fail)
 print('graphs',N,len(nodes),len(arcs),flush=True)
 out={'date':'2026-10-02','base_states':N,'base_arcs':sum(map(len,adj)),'augmented_states':len(nodes),'augmented_arcs':len(arcs),'potentials':{}}
 for orient in ('up','down','joint'):
  bs=[a if orient=='up' else b if orient=='down' else max(a,b) for a,b in charges]
  cost=[4*w-1-4*b for (u,v,w),b in zip(arcs,bs)]
  h=potentials(len(nodes),arcs,cost)
  assert min(h)>=-29 and max(h)==0
  assert all(c+h[u]-h[v]>=0 for (u,v,w),c in zip(arcs,cost))
  out['potentials'][orient]=[min(h),max(h)]
  print('potential',orient,min(h),max(h),flush=True)
 # Enumerate all possible local masks: F is the only selected-edge term in the charge.
 # All 2^20 masks are unnecessary: only the union of coefficients and exceptional pairs matters.
 watch=set().union(*(set(c)|e for c,e in tests));watch=sorted(watch)
 passcounts=[0,0,0]
 for selection in range(1<<len(watch)):
  selected={e for i,e in enumerate(watch) if selection>>i&1}
  fail=failures(mask(selected))
  for j,(coef,exc) in enumerate(tests):
   if not fail[j]:
    assert sum(coef.get(e,0) for e in selected)%3==2 and not exc<=selected
    passcounts[j]+=1
  passcounts[2]+=not any(fail)
 out['test_masks']={'watched_edges':len(watch),'masks':1<<len(watch),'pass_up_down_joint':passcounts}
 # Exact period-one witness, with pending connectivity independently derived from finite unroll.
 edges=set()
 for y in range(-12,13):
  for a,b in [((1,y),(0,y+2)),((2,y),(0,y+1)),((2,y),(1,y+2))]:edges.add(canon(a,b))
 deg=defaultdict(set)
 for a,b in edges:deg[a].add(b);deg[b].add(a)
 assert all(len(deg[x,y])==2 for x in (0,1,2) for y in range(-8,9))
 H={};compid={}
 for a,bs in deg.items():H[a]=bs
 # For each scan cut, include already processed edges and determine their path connectivity.
 cycle=[]
 for col in range(5):
  cut=col
  processed=[e for e in edges if min(4*a[1]+a[0] for a in e)<cut]
  parent={e:e for e in processed}
  def root(e):
   while parent[e]!=e:e=parent[e]
   return e
  at=defaultdict(list)
  for e in processed:
   for p in e:
    if 4*p[1]+p[0]<cut:at[p].append(e)
  for incident in at.values():
   if len(incident)==2:
    a,b=incident;ra,rb=root(a),root(b);assert ra!=rb;parent[ra]=rb
  pending=[]
  for e in processed:
   a,b=sorted(e,key=lambda p:(p[1],p[0]))
   if 4*a[1]+a[0]<cut<=4*b[1]+b[0]:pending.append((a,b,root(e)))
  labels={};canonical=[];shift=col//4
  for a,b,r in sorted(pending):
   if r not in labels:labels[r]=len(labels)
   canonical.append(((a[0],a[1]-shift),(b[0],b[1]-shift),labels[r]))
  state=(col%4,tuple(canonical));assert state in ids
  cycle.append(ids[state])
 assert cycle[0]==cycle[-1]
 ws=[dict(adj[u])[v] for u,v in zip(cycle,cycle[1:])];assert sum(ws)==2
 front={e for e in edges if min(p[1] for p in e)<=0<=max(p[1] for p in e)}
 Fs=[sum(c for e,c in coef.items() if e in front) for coef,exc in tests]
 assert [v%3 for v in Fs]==[1,1] and failures(mask(front))==(1,1)
 # Independent periodic crossing ownership: charge by minimum source-row of the two edges.
 crossing=sum(proper(e,f) for e,f in combinations(edges,2) if min(min(p[1] for p in e),min(p[1] for p in f))==0)
 assert crossing==2
 out['sharp_witness']={'steps':4,'arc_weights':ws,'crossings_per_row':crossing,'F_up_down':Fs,'failures_per_row':1,'ratio':'1','negative_cost_at_1001_1000_scaled4000':4000*(2-1)-4004,'states':[states[u] for u in cycle]}
 assert out['sharp_witness']['negative_cost_at_1001_1000_scaled4000']==-4
 Path('w-verifier/claim23b_stability.json').write_text(json.dumps(out,indent=1));print('WITNESS AND ALL CHECKS PASS',flush=True)
if __name__=='__main__':main()
