import sys
import networkx as nx
from fold_complete2 import base
from fold_complete import total_crossings
for n in map(int, sys.argv[1:]):
    E, deg = base(n)
    G = nx.Graph(); G.add_edges_from(E)
    comps = list(nx.connected_components(G))
    cyc = sum(1 for c in comps if all(deg[p]==2 for p in c))
    bad = [p for p in G if deg[p]!=2]
    print('n',n,'crossings',total_crossings(E),'per n %.3f'%(total_crossings(E)/n),'components',len(comps),'closed cycles',cyc,'paths',len(comps)-cyc,'bad cells',len(bad))
    sizes=sorted((len(c) for c in comps if all(deg[p]==2 for p in c)))
    print('  cycle sizes', sizes[:30], '...', sizes[-5:])
