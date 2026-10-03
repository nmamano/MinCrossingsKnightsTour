import networkx as nx
from fold_complete2 import base
n=96
E,deg=base(n,ts=(-1,-1,-1,-1),ms=(0,1,0,1))
E=set(E)
def comp_count(E):
    G=nx.Graph(); G.add_edges_from(E); return nx.number_connected_components(G), G
k0,G=comp_count(E)
a=(8,30); b=(a[0]+1,a[1]+2); d=(2,1)
ad=(a[0]+d[0],a[1]+d[1]); bd=(b[0]+d[0],b[1]+d[1])
e1=tuple(sorted([a,ad])); e2=tuple(sorted([b,bd]))
print('edges present', e1 in E, e2 in E, 'same comp', nx.has_path(G,a,b))
E2=(E-{e1,e2})|{tuple(sorted([a,b])),tuple(sorted([ad,bd]))}
print('components before',k0,'after',comp_count(E2)[0])
for x0 in range(6,12):
    a=(x0,30); b=(x0+1,32)
    print(a, nx.has_path(G,a,b), len(nx.node_connected_component(G,a)))
from fold_complete import total_crossings
a=(7,30); b=(8,32)
ad=(a[0]+2,a[1]+1); bd=(b[0]+2,b[1]+1)
E2=(E-{tuple(sorted([a,ad])),tuple(sorted([b,bd]))})|{tuple(sorted([a,b])),tuple(sorted([ad,bd]))}
print('merge', comp_count(E)[0], '->', comp_count(E2)[0], 'crossings', total_crossings(E), '->', total_crossings(E2))
