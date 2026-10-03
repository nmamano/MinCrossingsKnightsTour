"""L1 step 2 (free-interior relaxation): min over one corner of [cost to come from a zero class along the bottom arm]
+ [corner region] + [cost to reach a zero class along the left arm]. Region = {x<K,y<W} U {x<W,y<K}, K=W+2."""
import sys, pickle, heapq
from itertools import combinations
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
from strip import M, lower
W = int(sys.argv[1]); K = W + 2
states, arcs = pickle.load(open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/strip_W{W}.pkl', 'rb'))
sccs = pickle.load(open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/zero_W{W}.pkl', 'rb'))
N = len(states); ids = {s: i for i, s in enumerate(states)}
src = set().union(*sccs)
out = [[] for _ in range(N)]; inn = [[] for _ in range(N)]
for u, v, c, ch in arcs: out[u].append((v, c)); inn[v].append((u, c))
def dijkstra(adj):
    d = [10**9]*N; h = [(0, s) for s in src]
    for s in src: d[s] = 0
    while h:
        c, x = heapq.heappop(h)
        if c > d[x]: continue
        for y, w in adj[x]:
            if c + w < d[y]: d[y] = c + w; heapq.heappush(h, (c + w, y))
    return d
din = dijkstra(out)      # zero class -> s
dout = dijkstra(inn)     # s -> zero class
print('din finite', sum(x < 10**9 for x in din), 'dout finite', sum(x < 10**9 for x in dout), flush=True)
region = [(x, y) for x in range(K-1, -1, -1) for y in range(W)] + [(x, y) for y in range(W, K) for x in range(W)]
pos = {c: i for i, c in enumerate(region)}
def rc(p, a, b):
    t = int(a[0]+b[0] != 0 or a[1]+b[1] != 0)
    return t - lower(p[0], [a[0], b[0]]) - lower(p[1], [a[1], b[1]])
# initial frontier from bottom arm states: strip (X0,Y0,dX,dY) -> abs from (K-1-Y0, X0) move (-dY, dX)
front = {}
for i, s in enumerate(states):
    if din[i] >= 10**9: continue
    fs = frozenset(((K-1-Y0, X0), (K-1-Y0-dY, X0+dX)) for (X0, Y0, dX, dY) in s)
    if any(q not in pos for p, q in fs): continue   # edge from bottom arm to non-region cell: impossible here
    front[fs] = min(front.get(fs, 10**9), din[i])
print('initial frontier states', len(front), flush=True)
TARGET = int(sys.argv[2]) if len(sys.argv) > 2 else -7
def cellmin(p):
    ds = [d for d in M if p[0]+d[0] >= 0 and p[1]+d[1] >= 0]
    return min(rc(p, a, b) for a, b in combinations(ds, 2))
rem = [0]*(len(region)+1)
for i in range(len(region)-1, -1, -1): rem[i] = rem[i+1] + min(0, cellmin(region[i]))
print('sum of per-cell minima over region', rem[0], flush=True)
done = set()
for ip, p in enumerate(region):
    front = {fs: c for fs, c in front.items() if c + rem[ip] <= TARGET}
    nf = {}
    for fs, c0 in front.items():
        forced = [(q[0]-p[0], q[1]-p[1]) for q, r in fs if r == p]   # edges q->p pending
        if len(forced) > 2: continue
        rest = frozenset(e for e in fs if e[1] != p)
        free = [d for d in M if p[0]+d[0] >= 0 and p[1]+d[1] >= 0 and d not in forced]
        ok = []
        for d in free:
            q = (p[0]+d[0], p[1]+d[1])
            if q in pos and q in done: continue           # processed region cell: only via pending
            ok.append(d)
        for extra in combinations(ok, 2-len(forced)):
            mv = forced + list(extra)
            new = [(p, (p[0]+d[0], p[1]+d[1])) for d in extra if (p[0]+d[0], p[1]+d[1]) in pos]
            fs2 = rest | frozenset(new)
            load = {}
            for a, b in fs2: load[b] = load.get(b, 0) + 1
            if any(v > 2 for v in load.values()): continue
            c = c0 + rc(p, mv[0], mv[1])
            if c < nf.get(fs2, 10**9): nf[fs2] = c
    done.add(p); front = nf
    print(ip, p, len(front), flush=True)
print('final frontier states', len(front), flush=True)
best = 10**9
for fs, c in front.items():
    # left arm state: next row K; pending edges from region (y<K) to y>=K with x<W -> strip (x0, y0-K, dx, dy)
    # edges into left-arm cells from region must have target x<W, y in {K, K+1}
    s = frozenset((a[0], a[1]-K, b[0]-a[0], b[1]-a[1]) for a, b in fs)
    if any(b not in pos and not (b[0] < W and b[1] >= K) for a, b in fs): continue
    if any(b in pos for a, b in fs): continue
    i = ids.get(s)
    if i is None or dout[i] >= 10**9: continue
    best = min(best, c + dout[i])
print('W', W, 'corner min (zero class -> corner -> zero class) =', best)
