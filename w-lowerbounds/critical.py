# enumerate minimum-mean cycles (critical subgraph) of the strip transfer graph
import sys
from fractions import Fraction
import networkx as nx
from strip_dp import build
from mmc import prune, howard
k=int(sys.argv[1]); fam=None if len(sys.argv)<3 else tuple(map(int,sys.argv[2].split(',')))
states,adj,W=build(k,fam=fam)
alive=prune(adj)
mu,pol,eta=howard(adj,alive)
# potentials via Bellman-Ford on reduced weights (exact fractions) restricted to alive
nodes=[u for u in range(len(states)) if alive[u]]
d={u:Fraction(0) for u in nodes}
for it in range(len(nodes)+1):
    ch=False
    for u in nodes:
        for v,w in adj[u]:
            if alive[v] and d[u]+w-mu < d[v]:
                d[v]=d[u]+w-mu; ch=True
    if not ch: break
G=nx.DiGraph()
for u in nodes:
    for v,w in adj[u]:
        if alive[v] and d[u]+w-mu==d[v]:
            G.add_edge(u,v,w=w)
sccs=[c for c in nx.strongly_connected_components(G) if len(c)>1 or any(G.has_edge(u,u) for u in c)]
print('mu*W',mu*W,'critical SCCs',len(sccs),[len(c) for c in sccs])
for c in sccs:
    H=G.subgraph(c)
    cyc=list(nx.simple_cycles(H))
    print(' scc size',len(c),'simple cycles',len(cyc),'lengths',sorted(set(len(x)//W for x in cyc)))
