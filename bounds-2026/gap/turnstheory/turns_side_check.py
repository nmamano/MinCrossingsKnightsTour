"""Check saved zero-side graph labels and classify the exact-two-turn subset.
This checks labels, not the exhaustive generation of the input graph.
"""
import collections,json,math,pickle
from pathlib import Path
import networkx as nx
from turns_gap_scan import sidecost,turn,M
ROOT=Path(__file__).resolve().parents[2]
states,arcs=pickle.load(open(ROOT/'gap/lowerbounds/turns_ring/strip_W4.pkl','rb'))
Z=nx.DiGraph();Q=nx.DiGraph();labels={};localcount=0
for u,v,c,ch in arcs:
 if c:continue
 ds=dict(ch);assert set(ds)==set(range(4));forced=collections.defaultdict(set)
 for x,y,dx,dy in states[u]:
  if y+dy==0:forced[x+dx].add((-dx,-dy))
 new=[]
 for x,pair in ch:
  assert len(set(pair))==2 and all(d in M and x+d[0]>=0 for d in pair)
  assert {d for d in pair if x+d[0]<4 and d[1]<0}==forced[x]
  assert sidecost(x,pair)==0
  new.extend((x,0,dx,dy) for dx,dy in pair if x+dx<4 and dy>0)
 keep=[e for e in states[u] if e[1]+e[3]>0]
 nxt=frozenset((x,y-1,dx,dy) for x,y,dx,dy in new+keep)
 assert nxt==states[v]
 Z.add_edge(u,v);labels[u,v]=ch;localcount+=1
 if sum(turn(pair) for x,pair in ch)==2:Q.add_edge(u,v)
def classes(G):
 out=[]
 for cc in nx.strongly_connected_components(G):
  if len(cc)==1 and not G.has_edge(next(iter(cc)),next(iter(cc))):continue
  H=G.subgraph(cc);q=[min(cc)];lev={q[0]:0};g=0
  for u in q:
   for v in H[u]:
    if v not in lev:q.append(v);lev[v]=lev[u]+1
    g=math.gcd(g,lev[u]+1-lev[v])
  out.append(dict(states=len(cc),arcs=H.number_of_edges(),period=g))
 return sorted(out,key=lambda c:(c['states'],c['arcs']))
C=max(nx.strongly_connected_components(Z),key=len);H=Z.subgraph(C)
for u,v in H.edges:
 if sum(turn(ds) for x,ds in labels[u,v])==3:
  path=[u]+nx.shortest_path(H,v,u);break
profile=[labels[a,b] for a,b in zip(path,path[1:])]
counts=[sum(turn(ds) for x,ds in ch) for ch in profile]
assert sum(counts)==2*len(counts)
# Cut current: orient edges {0,3}->{1,2}. Its divergence equals sum L - 2.
def flux(s):return sum(1 if x in (0,3) else -1 for x,y,dx,dy in s if (x in (0,3)) != (x+dx in (0,3)))
for u,v in Z.edges:
 assert sum(turn(ds) for x,ds in labels[u,v])==2+flux(states[u])-flux(states[v])
report=dict(date='2026-10-04',checked_zero_arcs=localcount,zero_classes=classes(Z),exact_two_classes=classes(Q),nonconstant_periodic_witness=dict(states=path,rows=profile,row_turns=counts),flux_range=sorted(set(map(flux,states))))
(ROOT/'gap/turnstheory/turns_side_check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
