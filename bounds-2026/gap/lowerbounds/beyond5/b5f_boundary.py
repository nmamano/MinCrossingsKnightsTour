# KT Lower Bounds, 2026-10-03, B5f design input: per side row, the width-3 straddle count s3(r) (collar_current.py
# definition), the width-6 ports (strip cell x <= 5 -> outside cell, booked on the strip-cell row) and the edges inside
# columns 0..5 that start on the row (lower end). usage: b5f_boundary.py TOUR.json side r0 r1
import sys, json
from pathlib import Path
from collections import defaultdict, Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'w-verifier'))
from check import MOVES
f, sd, r0, r1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
E = {tuple(sorted(((x, n-1-y), (x+MOVES[int(v)][1], n-1-y-MOVES[int(v)][0])))) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])][sd]
loc = [tuple(sorted((T(a), T(b)), key=lambda p: (p[1], p[0]))) for a, b in E]
def straddle(w):
    adj = defaultdict(list); ports = defaultdict(list)
    for a, b in loc:
        ia, ib = a[0] < w, b[0] < w
        if ia and ib: adj[a].append(b); adj[b].append(a)
        elif ia: ports[a].append(b)
        elif ib: ports[b].append(a)
    seen = set(); s = Counter(); pair = {}
    for v in list(ports):
        if v in seen: continue
        st = [v]; seen.add(v); comp = [v]
        while st:
            u = st.pop()
            for x in adj[u]:
                if x not in seen: seen.add(x); st.append(x); comp.append(x)
        pr = sorted((u[1], u[0], p[0]-u[0], p[1]-u[1]) for u in comp for p in ports[u])
        for r in range(pr[0][0], pr[-1][0]): s[r] += 1
        pair[pr[0]] = (pr[1], len(comp))
    return s, pair
s3, _ = straddle(3); s6, pair6 = straddle(6)
for r in range(r0, r1):
    inner = sorted((a[0], b[0]-a[0], b[1]-a[1]) for a, b in loc if a[1] == r and a[0] < 6 and b[0] < 6)
    pts = sorted((a, p) for a, p in pair6.items() if a[0] == r)
    print(r, 's3', s3[r], 's6', s6[r], 'inner', inner, 'paths6', pts)
