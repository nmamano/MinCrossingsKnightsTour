#!/usr/bin/env python3
"""Interior price of a fixed collar pattern (KT Lower Bounds, 2026-10-03, beyond-5n pilot).

Cylinder: columns 0..K+1, rows Z_P. Columns 0..K-1 degree exactly 2, columns K, K+1 degree <= 2. The edges with an end
in columns 0..2 are FIXED to a period-1 collar pattern; the rest is free. Objective: crossing pairs per period among
edges with an end in columns 0..K-1 (all crossings, not only S*). Lazy cuts remove finite cycles that avoid the halo.
Patterns: P   = cheap pattern, collar path (4,y+1)-(2,y)-(0,y-1)-(1,y+1)-(3,y+2);
          U   = joint_stab.py blocking cycle, collar path (3,y-1)-(1,y)-(0,y+2)-(2,y+1)-(4,y+2) ('\\' port to '/' port).
usage: collar_cost.py P|U K PER [TIME]
"""
import sys
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from strip_dp import cross

pat, K, P = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); TL = float(sys.argv[4]) if len(sys.argv) > 4 else 300
MV = [(1, 2), (2, 1), (2, -1), (1, -2)]
PAT = {'P': [((2, 0), (0, -1)), ((0, -1), (1, 1)), ((1, 1), (3, 2)), ((2, 0), (4, 1))],
       'U': [((3, -1), (1, 0)), ((1, 0), (0, 2)), ((0, 2), (2, 1)), ((2, 1), (4, 2))]}[pat]
fixed = set()
for y in range(P):
    for a, b in PAT:
        u = (a[0], (a[1] + y) % P); v = (b[0], (b[1] + y) % P)
        fixed.add(frozenset((u, v)))
# edge orbits: lower-left representative (x, y) with move (dx, dy), dx > 0
E = []
for x in range(K + 2):
    for y in range(P):
        for dx, dy in MV:
            if x + dx <= K + 1 and (x <= K - 1 or x + dx <= K - 1):
                E.append(((x, y), (x + dx, (y + dy) % P), dy))
m = cp_model.CpModel()
xv = [m.NewBoolVar(f'e{i}') for i in range(len(E))]
inc = {}
for i, (u, v, dy) in enumerate(E):
    inc.setdefault(u, []).append(i); inc.setdefault(v, []).append(i)
    key = frozenset((u, v))
    if min(u[0], v[0]) <= 2:
        m.Add(xv[i] == (1 if key in fixed else 0))
for vtx, l in inc.items():
    if vtx[0] <= K - 1: m.Add(sum(xv[i] for i in l) == 2)
    else: m.Add(sum(xv[i] for i in l) <= 2)
# crossings per period: e in rows [0,P) lifted, f lifted by shifts
def seg(i, s=0):
    (x0, y0), (x1, _), dy = E[i]
    return (x0, y0 + s, x1, y0 + dy + s)
cr = []
for i in range(len(E)):
    for j in range(len(E)):
        for s in (-P, 0, P):
            if (j, s) <= (i, 0) and not (j == i and s < 0): continue
            if j == i and s == 0: continue
            a, b = seg(i), seg(j, s)
            if cross(a, b):
                z = m.NewBoolVar(''); m.AddBoolAnd([xv[i], xv[j]]).OnlyEnforceIf(z)
                m.AddBoolOr([xv[i].Not(), xv[j].Not()]).OnlyEnforceIf(z.Not()); cr.append(z)
m.Minimize(sum(cr))
sv = cp_model.CpSolver(); sv.parameters.num_workers = 2; sv.parameters.max_time_in_seconds = TL
for it in range(200):
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('status', sv.StatusName(st)); break
    sel = [i for i in range(len(E)) if sv.Value(xv[i])]
    adj = {}
    for i in sel:
        u, v, _ = E[i]; adj.setdefault(u, []).append((v, i)); adj.setdefault(v, []).append((u, i))
    seen = set(); cuts = 0
    for s0 in adj:
        if s0 in seen: continue
        comp, st2, ids = [], [s0], set()
        while st2:
            w = st2.pop()
            if w in seen: continue
            seen.add(w); comp.append(w)
            for nb, i in adj[w]: ids.add(i); st2.append(nb)
        if all(w[0] <= K - 1 for w in comp):
            # a closed component inside the exact region: finite cycle unless it winds around the cylinder
            wind = 0
            # winding: sum of dy along the cycle orientation
            start = comp[0]; prev = None; cur = start; tot = 0; used = set()
            while True:
                nxt = [(nb, i) for nb, i in adj[cur] if i not in used]
                if not nxt: break
                nb, i = nxt[0]; used.add(i)
                u, v, dy = E[i]; tot += dy if cur == u else -dy
                cur = nb
                if cur == start: break
            if tot == 0:
                m.AddBoolOr([xv[i].Not() for i in ids]); cuts += 1
    print(f'iter {it}: {sv.StatusName(st)} crossings/period {sv.ObjectiveValue():.0f} (bound {sv.BestObjectiveBound():.0f}), '
          f'per row {sv.ObjectiveValue() / P:.3f}, cuts {cuts}', flush=True)
    if not cuts: break
