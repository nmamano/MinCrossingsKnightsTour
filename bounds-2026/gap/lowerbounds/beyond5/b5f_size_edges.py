# B5f sizing helper: same scan as b5f_size.py, degree constraints only (no labels): number of pending-edge sets.
import sys
from collections import deque
from itertools import combinations
W = 6; NEED = [2, 2, 2, 2, 1, 1]; UPM = [(2, 1), (-2, 1), (1, 2), (-1, 2)]
def step(st):
    x, ends = st
    inc = [e for e in ends if e[2] == x and e[3] == 0]; rest = [e for e in ends if not (e[2] == x and e[3] == 0)]
    r = NEED[x] - len(inc)
    if r < 0: return
    cands = [(x, 0, x + dx, dy) for dx, dy in UPM if 0 <= x + dx < W]
    t0 = {}
    for e in rest: t0[(e[2], e[3])] = t0.get((e[2], e[3]), 0) + 1
    for ch in combinations(cands, r):
        t = dict(t0); ok = True
        for e in ch:
            k = (e[2], e[3]); t[k] = t.get(k, 0) + 1; ok &= t[k] <= NEED[e[2]]
        if not ok: continue
        ne = rest + list(ch)
        yield (0, tuple(sorted((a, b - 1, c, d - 1) for a, b, c, d in ne))) if x + 1 == W else (x + 1, tuple(sorted(ne)))
s0 = (0, ((0, -1, 2, 0), (1, -2, 0, 0), (1, -1, 0, 1), (1, -1, 3, 0), (2, -1, 4, 0), (3, -1, 5, 0)))
idx = {s0}; q = deque([s0]); arcs = 0; pos = [0] * W; ne_hist = {}
while q:
    st = q.popleft()
    for ns in step(st):
        arcs += 1
        if ns not in idx: idx.add(ns); q.append(ns)
for s in idx: pos[s[0]] += 1; ne_hist[len(s[1])] = ne_hist.get(len(s[1]), 0) + 1
print('edge-set states', len(idx), 'arcs', arcs, 'by cell', pos, 'by #pending', sorted(ne_hist.items()))
