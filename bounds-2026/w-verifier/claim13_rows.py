"""Independent per-row flag extension and exact sharpness witness."""
from pathlib import Path
from fractions import Fraction
from collections import deque
import json
import networkx as nx
from claim11_forest import transitions,potentials

def main():
 states=[(0,())];index={states[0]:0};arcs=[]
 for u,s in enumerate(states):
  outgoing={}
  for t,w in transitions(s):
   if t not in index:index[t]=len(states);states.append(t)
   v=index[t];outgoing[v]=min(outgoing.get(v,w),w)
  arcs.extend((u,v,w) for v,w in outgoing.items())
 N=len(states);assert (N,len(arcs))==(82516,144674)
 d=potentials(N,arcs,[4*w-1 for u,v,w in arcs],0)
 G=nx.DiGraph();G.add_nodes_from(range(N));G.add_edges_from((u,v) for u,v,w in arcs if 4*w-1+d[u]-d[v]==0)
 comps=[c for c in nx.strongly_connected_components(G) if len(c)>1 or any(G.has_edge(u,u) for u in c)]
 critical={(u,v) for c in comps for u in c for v in G[u] if v in c};assert len(critical)==8
 augmented=[];weights=[];charges=[];adj=[[] for _ in range(2*N)]
 for u,v,w in arcs:
  assert states[v][0]==(states[u][0]+1)%4
  noncritical=(u,v) not in critical
  for flag in (0,1):
   dirty=bool(flag or noncritical)
   closing=states[u][0]==3
   charge=int(closing and dirty)
   nextflag=0 if closing else int(dirty)
   a,b=2*u+flag,2*v+nextflag
   adj[a].append(b);augmented.append((a,b,w));charges.append(charge);weights.append(8*w-2-4*charge)
 h=potentials(2*N,augmented,weights)
 assert (min(h),max(h))==(-46,0)
 assert all(c+h[a]-h[b]>=0 for (a,b,w),c in zip(augmented,weights))
 reach={0};q=deque([0])
 while q:
  for v in adj[q.popleft()]:
   if v not in reach:reach.add(v);q.append(v)
 Z=nx.DiGraph();Z.add_nodes_from(reach)
 Z.add_edges_from((a,b) for (a,b,w),c in zip(augmented,weights) if a in reach and c+h[a]-h[b]==0)
 belong={u:i for i,c in enumerate(nx.strongly_connected_components(Z)) for u in c}
 first=next((a,b) for (a,b,w),c,bad in zip(augmented,weights,charges) if bad and a in reach and c+h[a]-h[b]==0 and belong[a]==belong[b])
 a,b=first;cycle=[a]+nx.shortest_path(Z,b,a)
 lookup={(a,b):(w,bad) for (a,b,w),bad in zip(augmented,charges)}
 steps=[]
 for a,b in zip(cycle,cycle[1:]):
  w,bad=lookup[a,b];steps.append({'weight':w,'bad_row_charge':bad})
 W=sum(v['weight'] for v in steps);B=sum(v['bad_row_charge'] for v in steps);L=len(steps)
 assert L%4==0 and Fraction(4*W-L,4*B)==Fraction(1,2)
 # Rotate to the beginning of a complete row and check the flags directly.
 offset=next(i for i,a in enumerate(cycle[:-1]) if states[a//2][0]==0 and a%2==0)
 nodes=cycle[:-1];nodes=nodes[offset:]+nodes[:offset];nodes.append(nodes[0])
 direct_bad=0
 for j in range(0,L,4):
  assert [states[nodes[j+k]//2][0] for k in range(4)]==[0,1,2,3]
  direct_bad+=any((nodes[j+k]//2,nodes[j+k+1]//2) not in critical for k in range(4))
 assert direct_bad==B
 negative=1000*(4*W-L)-2004*B
 assert negative<0
 report={'date':'2026-10-02','base_states':N,'base_arcs':len(arcs),'augmented_states':2*N,'augmented_arcs':len(augmented),'reachable_augmented_states':len(reach),'potential_scaled8':[min(h),max(h)],'start_potential_scaled8':h[0],'minimum_adjusted_for_partial_row_scaled8':min(h[a]-4*(a%2) for a in reach),'sharp_cycle':{'steps':L,'crossing_weight':W,'bad_rows':B,'ratio':'1/2','negative_weight_at_501_1000_scaled4000':negative,'states':[[states[a//2],a%2] for a in nodes],'arc_weights':[lookup[a,b][0] for a,b in zip(nodes,nodes[1:])],'row_charges':[lookup[a,b][1] for a,b in zip(nodes,nodes[1:])]}}
 Path('w-verifier/claim13_rows.json').write_text(json.dumps(report,indent=1))
 print({k:v for k,v in report.items() if k!='sharp_cycle'},flush=True)
 print('EXACT sharp cycle:',L,'steps, weight',W,'bad rows',B,'ratio 1/2; 501/1000 weight',negative,flush=True)
if __name__=='__main__':main()
