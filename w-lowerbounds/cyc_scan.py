import sys, itertools
import networkx as nx
from fold_complete2 import base
n=int(sys.argv[1]); R=range(-1,3)
res=[]
for ts in itertools.product(R,repeat=4):
  for ms in [(0,0,0,0),(1,1,1,1),(1,0,0,0),(0,0,0,1),(1,0,1,0),(0,1,0,1)]:
    E,deg=base(n,ts=ts,ms=ms)
    G=nx.Graph(); G.add_edges_from(E)
    comps=list(nx.connected_components(G))
    cyc=sum(1 for c in comps if all(deg[p]==2 for p in c))
    res.append((cyc,len(comps),ts,ms))
res.sort()
for r in res[:10]: print(r)
print('max',res[-1])
