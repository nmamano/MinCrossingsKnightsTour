import sys, ast
import networkx as nx
from fold_complete2 import base
def clusters(n, ts, ms):
    E,deg=base(n,ts=ts,ms=ms)
    bad=[(x,y) for x in range(n) for y in range(n) if deg[(x,y)]!=2]
    G=nx.Graph(); G.add_nodes_from(bad)
    for a in bad:
        for b in bad:
            if a<b and max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=8: G.add_edge(a,b)
    out=[]
    for cl in nx.connected_components(G):
        b=sum(2-deg[p] for p in cl if (p[0]+p[1])%2==0); w=sum(2-deg[p] for p in cl if (p[0]+p[1])%2==1)
        out.append((sorted(cl), b-w))
    return E, deg, out
if __name__=='__main__':
    n=int(sys.argv[1]); ts=ast.literal_eval(sys.argv[2]); ms=ast.literal_eval(sys.argv[3])
    E,deg,cl=clusters(n,ts,ms)
    for c,i in cl: print(i, c[:6])
