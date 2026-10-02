import sys, itertools
import networkx as nx
from fold_complete2 import base
from fold_complete import total_crossings
n=int(sys.argv[1])
for ts in [(0,0,0,0),(1,1,1,1),(2,2,2,2),(1,0,0,0),(-1,-1,-1,-1)]:
    E,deg=base(n,ts=ts)
    G=nx.Graph(); G.add_edges_from(E)
    comps=list(nx.connected_components(G))
    cyc=[c for c in comps if all(deg[p]==2 for p in c)]
    print(ts,'X',total_crossings(E),'comps',len(comps),'closed cycles',len(cyc),'largest',sorted(map(len,comps))[-4:])
