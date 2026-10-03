# KT Structures, 2026-10-03. BEYOND5 13.3: straddle count s(r) of the side strip. Strip = local x < w (whole side length);
# collar paths = components of tour edges with both ends in the strip; a path's ports are its edges leaving the strip;
# s(r) = number of paths whose two port rows (strip-side endpoint rows) satisfy y1 <= r < y2. Invariant under any
# pairing-preserving patch of width <= w. Prints per side: histogram of s(r) over rows 8..n-9, and sum (s - s0)^+ for
# a reference s0. usage: collar_current.py W S0 TOUR.json...
import sys, json
from pathlib import Path
from collections import defaultdict, Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import MOVES
w = int(sys.argv[1]); s0 = int(sys.argv[2])
for f in sys.argv[3:]:
    grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
    E = [((x, n-1-y), (x+MOVES[int(v)][1], n-1-y-MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code]
    E = {tuple(sorted(e)) for e in E}
    Ts = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    out = []; offs = [Counter() for _ in range(4)]
    for sd in range(4):
        loc = [(Ts[sd](a), Ts[sd](b)) for a, b in E]
        adj = defaultdict(list); ports = defaultdict(list)
        for a, b in loc:
            ia, ib = a[0] < w, b[0] < w
            if ia and ib: adj[a].append(b); adj[b].append(a)
            elif ia: ports[a].append(b)
            elif ib: ports[b].append(a)
        seen = set(); s = Counter(); bad = 0
        for v in list(ports):
            if v in seen: continue
            st = [v]; seen.add(v); comp = [v]
            while st:
                u = st.pop()
                for x in adj[u]:
                    if x not in seen: seen.add(x); st.append(x); comp.append(x)
            pr = sorted(u[1] for u in comp for _ in ports[u])
            if len(pr) != 2: bad += 1; continue
            for r in range(pr[0], pr[1]): s[r] += 1
            if 8 <= pr[0] and pr[1] <= n-9: offs[sd][tuple(sorted((u[0], x[0]) for u in comp for x in ports[u]))+(pr[1]-pr[0],)] += 1
        rows = range(8, n-8)
        hist = Counter(s[r] for r in rows)
        out.append(dict(hist=dict(sorted(hist.items())), excess=sum(max(0, s[r]-s0) for r in rows), deficit=sum(max(0, s0-s[r]) for r in rows), bad=bad))
    if '-o' in sys.argv[0:1] or True:
        for sd in range(4): print('   side', sd, 'pair types ((strip x, outside x) of both ports, dy):', offs[sd].most_common(6))
    print(Path(f).name, n, 'w', w, 'excess sum', sum(o['excess'] for o in out), [ (o['hist'], o['excess']) for o in out], flush=True)
