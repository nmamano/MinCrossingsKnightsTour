# Independent check: the explicit pattern P_k on a finite strip of rows, counting crossings
# among edges that touch columns 0..k-1, and checking degrees and acyclicity.
import sys, itertools
from strip_dp import cross
def pattern(k, R):
    E=set()
    for y in range(R):
        E.add((0,y,1,y+2)); E.add((0,y,2,y+1))
        for x in range(1,k):
            E.add((x,y,x+2,y+1))
    return E
k=int(sys.argv[1]); R=60
E=pattern(k,R)
from collections import Counter
deg=Counter()
for (a,b,c,d) in E: deg[(a,b)]+=1; deg[(c,d)]+=1
bad=[c for c,v in deg.items() if 10<=c[1]<R-10 and ((c[0]<k and v!=2) or v>2)]
cnt=0
mid=[e for e in E if 10<=e[1]<R-10]
for e,g in itertools.combinations(E,2):
    if cross(e,g) and 10<=min(e[1],g[1])<R-10: cnt+=1
import networkx as nx
G=nx.Graph(); G.add_edges_from(((a,b),(c,d)) for a,b,c,d in E)
print('k',k,'deg violations',len(bad),'crossings per row %.3f'%(cnt/(R-20)),'cycles',len(nx.cycle_basis(G)))
