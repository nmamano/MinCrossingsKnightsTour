import itertools, sys
import networkx as nx
from fold_complete2 import base
n=int(sys.argv[1])
res=[]
for ts in itertools.product(range(-1,2),repeat=4):
  for ms in itertools.product(range(-1,2),repeat=4):
    E,deg=base(n,ts=ts,ms=ms)
    bad=[(x,y) for x in range(n) for y in range(n) if deg[(x,y)]!=2]
    G=nx.Graph(); G.add_nodes_from(bad)
    for a in bad:
        for b in bad:
            if a<b and max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=8: G.add_edge(a,b)
    imb=[]
    for cl in nx.connected_components(G):
        b=sum(2-deg[p] for p in cl if (p[0]+p[1])%2==0); w=sum(2-deg[p] for p in cl if (p[0]+p[1])%2==1)
        imb.append(b-w)
    res.append((sum(abs(i) for i in imb), len(bad), ts, ms, imb))
res.sort()
for r in res[:8]: print(r)
