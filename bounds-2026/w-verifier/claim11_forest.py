"""Independent forest strip graph and sharp stability certificate. No worker imports."""
from itertools import combinations
from collections import deque
from fractions import Fraction
from pathlib import Path
import json
import networkx as nx
from claim10_allow_cycles import cross,pattern_states

def transitions(s):
 x,pend=s;p=(x,0)
 inc=[e for e in pend if e[1]==p];keep=[e for e in pend if e[1]!=p]
 if len(inc)>2 or len(inc)==2 and inc[0][2]==inc[1][2]:return
 possible=[(p,(xx,dy)) for xx in range(4) for dy in (1,2) if sorted((abs(xx-x),dy))==[1,2] and min(x,xx)<2]
 need=[2-len(inc)] if x<2 else range(3-len(inc))
 for k in need:
  for chosen in combinations(possible,k):
   if any(sum(e[1]==q for e in keep)+sum(e[1]==q for e in chosen)>2 for a,q in chosen):continue
   labels={e[2] for e in inc};merged=min(labels) if labels else -1
   result=[(a,b,merged if c in labels else c) for a,b,c in keep]+[(a,b,merged) for a,b in chosen]
   weight=sum(cross(e,(a,b)) for e in chosen for a,b,c in keep)+sum(cross(e,f) for e,f in combinations(chosen,2))
   shift=int(x==3);ren={};canon=[]
   for a,b,c in sorted(result):
    if c not in ren:ren[c]=len(ren)
    canon.append(((a[0],a[1]-shift),(b[0],b[1]-shift),ren[c]))
   yield ((x+1)%4,tuple(canon)),weight

def potentials(N,arcs,weights,source=None):
 d=[0 if source is None else 10**12]*N
 if source is not None:d[source]=0
 for i in range(N):
  changed=False
  for (u,v,w),c in zip(arcs,weights):
   if d[u]<10**12 and d[v]>d[u]+c:d[v]=d[u]+c;changed=True
  if not changed:return d
 raise AssertionError('negative cycle')

def main():
 states=[(0,())];ids={states[0]:0};arcs=[]
 for u,s in enumerate(states):
  seen=set()
  for t,w in transitions(s):
   if t not in ids:ids[t]=len(states);states.append(t)
   if (ids[t],w) not in seen:arcs.append((u,ids[t],w));seen.add((ids[t],w))
 N=len(states);assert (N,len(arcs))==(82516,144674)
 print('graph',N,len(arcs),flush=True)
 d=potentials(N,arcs,[4*w-1 for u,v,w in arcs],0)
 G=nx.DiGraph();G.add_nodes_from(range(N))
 G.add_edges_from((u,v) for u,v,w in arcs if 4*w-1+d[u]-d[v]==0)
 comps=[c for c in nx.strongly_connected_components(G) if len(c)>1 or any(G.has_edge(u,u) for u in c)]
 assert len(comps)==2 and all(len(c)==4 for c in comps)
 assert {frozenset((states[u][0],tuple((a,b) for a,b,c in states[u][1])) for u in c) for c in comps}=={frozenset(pattern_states(s)) for s in (1,-1)}
 critical={(u,v) for c in comps for u in c for v in G[u] if v in c};assert len(critical)==8
 for c in comps:
  root=next(u for u in c if states[u][0]==0)
  pending={tuple(sorted((a,b))) for a,b,l in states[root][1]}
  pair1=[((0,-2),(1,0)),((0,-1),(2,0))]
  pair2=[((0,1),(1,-1)),((0,0),(2,-1))]
  assert sum(all(tuple(sorted(e)) in pending for e in pair) and cross(*pair) for pair in (pair1,pair2))==1
 G.remove_edges_from(critical);assert nx.is_directed_acyclic_graph(G)
 T=nx.dag_longest_path_length(G)
 costs=[20*w-5-4*((u,v) not in critical) for u,v,w in arcs]
 h=potentials(N,arcs,costs)
 assert (min(h),max(h))==(-149,0)
 assert all(c+h[u]-h[v]>=0 for (u,v,w),c in zip(arcs,costs))
 Z=nx.DiGraph();Z.add_nodes_from(range(N))
 Z.add_edges_from((u,v) for (u,v,w),c in zip(arcs,costs) if c+h[u]-h[v]==0)
 belong={u:i for i,c in enumerate(nx.strongly_connected_components(Z)) for u in c}
 first=next((u,v) for u,v in Z.edges if (u,v) not in critical and belong[u]==belong[v])
 u,v=first;path=[u]+nx.shortest_path(Z,v,u)
 witness=list(zip(path,path[1:]));weights={(u,v):w for u,v,w in arcs}
 total=sum(weights[e] for e in witness);nc=sum(e not in critical for e in witness);steps=len(witness)
 assert Fraction(4*total-steps,4*nc)==Fraction(1,5)
 negative=sum(1000*(4*weights[e]-1)-804*(e not in critical) for e in witness)
 assert negative<0
 report={'states':N,'arcs':len(arcs),'ordinary_potential_scaled4':[min(d),max(d)],'T':T,'alpha_potential_scaled20':[min(h),max(h)],'critical_arcs':8,'sharp_cycle':{'steps':steps,'crossing_weight':total,'noncritical_steps':nc,'ratio':'1/5','weight_at_201_1000_scaled4000':negative,'states':[states[u] for u in path],'arc_weights':[weights[e] for e in witness]}}
 Path('w-verifier/claim11_forest.json').write_text(json.dumps(report,indent=1))
 print({k:v for k,v in report.items() if k!='sharp_cycle'},flush=True)
 print('sharp witness',steps,total,nc,'negative at 201/1000:',negative,flush=True)
if __name__=='__main__':main()
