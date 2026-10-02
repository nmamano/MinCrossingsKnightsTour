import sys
from strip_dp import build, cross
from mmc import prune, howard
k = int(sys.argv[1])
states, adj, W = build(k)
alive = prune(adj)
mu, pol, eta = howard(adj, alive)
# find a cycle with mean mu in policy graph
u = next(v for v in eta if eta[v]==mu)
seen=[]
while u not in seen:
    seen.append(u); u = pol[u][0]
cyc = seen[seen.index(u):]
# rotate to phase 0
i0 = next(i for i,c in enumerate(cyc) if states[c][0]==0)
cyc = cyc[i0:]+cyc[:i0]
print('cycle len cells', len(cyc), 'rows', len(cyc)//W, 'weight', sum(pol[c][1] for c in cyc))
# reconstruct edges: the edges added at each step = edges in next state that have lower endpoint at current cell
edges=[]
for step,c in enumerate(cyc):
    x, es, _ = states[c]
    y = step//W
    nxt = states[pol[c][0]]
    shift = 1 if nxt[0]==0 else 0
    for (a,b,cc,d,comp) in nxt[1]:
        if a==x and b+shift==0:
            edges.append((a,y,cc,y+d))
R = len(cyc)//W
print(edges)
# draw 3 periods
for rep in range(1):
    pass
