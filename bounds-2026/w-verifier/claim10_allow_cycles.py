"""Independent degree-only strip graph. Cycles are allowed, as in a 2-factor.
No worker imports. Exact integer geometry and quarter-unit potentials.
"""
from itertools import combinations
from collections import deque
import json
import networkx as nx

def cross(e,f):
 def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 a,b=e;c,d=f
 return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

def nexts(state):
 x,edges=state;p=(x,0)
 entering=[e for e in edges if e[1]==p]
 rem=tuple(e for e in edges if e[1]!=p)
 opts=[(p,(xx,yy)) for xx in range(4) for yy in (1,2) if sorted((abs(xx-x),yy))==[1,2] and min(x,xx)<2]
 demand=[2-len(entering)] if x<2 else range(3-len(entering))
 for k in demand:
  if k<0:continue
  for add in combinations(opts,k):
   es=rem+add
   if any(sum(e[1]==f[1] for e in es)>2 for f in add):continue
   cost=sum(cross(e,f) for e in add for f in rem)+sum(cross(e,f) for e,f in combinations(add,2))
   shift=int(x==3)
   dest=((x+1)%4,tuple(sorted(((a[0],a[1]-shift),(b[0],b[1]-shift)) for a,b in es)))
   yield dest,cost

def pattern_states(sign):
 edges=set()
 for y in range(-4,5):
  for a,b in [((0,y),(2,y+sign)),((0,y),(1,y+2*sign)),((1,y),(3,y+sign))]:
   edges.add(tuple(sorted((a,b),key=lambda p:(p[1],p[0]))))
 states=[]
 for x in range(4):
  pend=tuple(sorted((a,b) for a,b in edges if 4*a[1]+a[0]<x<=4*b[1]+b[0]))
  states.append((x,pend))
 return set(states)

def check_cycle_input():
 d=json.load(open('w-verifier/claim10_cycle_counterexample.json'))
 edges=[tuple(sorted((tuple(a),tuple(b)),key=lambda p:(p[1],p[0]))) for a,b in d['edges'] if min(a[0],b[0])<2]
 state=(0,());cost=0
 for cut in range(1,4*d['n']+1):
  y,x=divmod(cut,4)
  target=(x,tuple(sorted(((a[0],a[1]-y),(b[0],b[1]-y)) for a,b in edges if 4*a[1]+a[0]<cut<=4*b[1]+b[0])))
  possibilities=[c for t,c in nexts(state) if t==target]
  assert len(possibilities)==1
  cost+=possibilities[0];state=target
 assert state==(0,())
 assert cost==sum(cross(a,b) for a,b in combinations(edges,2))
 return cost

def main():
 witness_cost=check_cycle_input()
 start=(0,());states=[start];idx={start:0};adj=[];arcs=[]
 for i,s in enumerate(states):
  best={}
  for dest,c in nexts(s):
   if dest not in idx:idx[dest]=len(states);states.append(dest)
   v=idx[dest];best[v]=min(best.get(v,c),c)
  adj.append(list(best.items()))
  arcs.extend((i,v,c) for v,c in best.items())
 print('states',len(states),'arcs',len(arcs),flush=True)
 inf=10**12;ds=[inf]*len(states);ds[0]=0
 for it in range(len(states)+1):
  changed=False
  for u,v,c in arcs:
   if ds[u]<inf and ds[v]>ds[u]+4*c-1:
    ds[v]=ds[u]+4*c-1;changed=True
  if not changed:break
 assert not changed,'negative cycle'
 red=[4*c-1+ds[u]-ds[v] for u,v,c in arcs]
 assert min(red)>=0
 G=nx.DiGraph();G.add_nodes_from(range(len(states)))
 G.add_edges_from((u,v) for (u,v,c),r in zip(arcs,red) if r==0)
 scc=[s for s in nx.strongly_connected_components(G) if len(s)>1 or any(G.has_edge(u,u) for u in s)]
 assert {frozenset(states[u] for u in c) for c in scc} == {frozenset(pattern_states(s)) for s in (-1,1)}
 removed=[];templates=[]
 for s in scc:
  inner=[(u,v) for u in s for v in G[u] if v in s]
  assert len(inner)==len(s),'non-simple tight SCC'
  removed+=inner
  templates.append([states[u] for u in sorted(s)])
 G.remove_edges_from(removed)
 assert nx.is_directed_acyclic_graph(G)
 report={'cycle_input_crossings':witness_cost,'patterns_checked':True,'states':len(states),'arcs':len(arcs),'potential_scaled4':[min(ds),max(ds)],'rho_scaled4':min(r for r in red if r>0),'tight_cycles':[len(s) for s in scc],'T':nx.dag_longest_path_length(G),'tight_cycle_states':templates}
 print(json.dumps({k:v for k,v in report.items() if k!='tight_cycle_states'}),flush=True)
 json.dump(report,open('w-verifier/claim10_allow_cycles.json','w'),indent=1)
if __name__=='__main__':main()
