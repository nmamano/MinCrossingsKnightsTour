# KT Structures, 2026-10-03. BEYOND5 10.5 step 1 (P5): local search on one vertical collar of an H-regime tour.
# Sweep windows of W rows; in each window all edges at the free vertices (x <= 2 on side 0, x >= n-3 on side 1) are
# variables, other edges fixed; minimise crossings involving variable edges, degree 2, one cycle (lazy cuts). Exact per
# window (CP-SAT, 2 workers). usage: p5_lns.py TOUR.json SIDE OUT.json [W] [ylo]
import sys, json, time
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'w-verifier'))
from check import check, MOVES
from ortools.sat.python import cp_model
f, side, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
Wd = int(sys.argv[4]) if len(sys.argv) > 4 else 12; ylo = int(sys.argv[5]) if len(sys.argv) > 5 else 8
grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
ed = lambda a, b: tuple(sorted((a, b)))
E = {ed((x, n-1-y), (x+MOVES[int(v)][1], n-1-y-MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
onb = lambda v: 0 <= v[0] < n and 0 <= v[1] < n
colw = (lambda v: v[0] <= 2) if side == 0 else (lambda v: v[0] >= n-3)
KM = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
def orient(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def cross(e, g):
    a, b = e; c, d = g
    return orient(a, b, c)*orient(a, b, d) < 0 and orient(c, d, a)*orient(c, d, b) < 0
near = lambda e, g: max(abs(e[0][0]-g[0][0]), abs(e[0][1]-g[0][1])) <= 4
def ncomp(Es):
    adj = defaultdict(list)
    for a, b in Es: adj[a].append(b); adj[b].append(a)
    seen = set(); cs = []
    for v in adj:
        if v in seen: continue
        st = [v]; seen.add(v); c = set()
        while st:
            u = st.pop(); c.add(u)
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        cs.append(c)
    return cs
def window(E, y0, y1):
    inw = lambda v: colw(v) and y0 <= v[1] <= y1
    W = [(x, y) for x in range(n) for y in range(y0, y1+1) if inw((x, y))]
    cand = sorted({ed(v, (v[0]+a, v[1]+b)) for v in W for a, b in KM if onb((v[0]+a, v[1]+b))})
    fixed = [e for e in E if not (inw(e[0]) or inw(e[1]))]
    fn = [g for g in fixed if min(g[0][1], g[1][1]) >= y0-4 and max(g[0][1], g[1][1]) <= y1+4]
    m = cp_model.CpModel(); X = {e: m.NewBoolVar('') for e in cand}
    fdeg = defaultdict(int)
    for a, b in fixed: fdeg[a] += 1; fdeg[b] += 1
    inc = defaultdict(list)
    for e in cand: inc[e[0]].append(e); inc[e[1]].append(e)
    for v, es in inc.items(): m.Add(sum(X[e] for e in es) == 2 - fdeg[v])
    obj = []; cost = {}
    for e in cand:
        k = sum(1 for g in fn if near(e, g) and cross(e, g)); cost[e] = k
        if k: obj.append(k * X[e])
    pairs = [(e, g) for i, e in enumerate(cand) for g in cand[i+1:] if near(e, g) and cross(e, g)]
    for e, g in pairs:
        z = m.NewBoolVar(''); m.AddBoolOr([X[e].Not(), X[g].Not(), z]); obj.append(z)
    m.Minimize(sum(obj))
    cur = sum(cost[e] for e in cand if e in E) + sum(1 for e, g in pairs if e in E and g in E)
    for e in cand: m.AddHint(X[e], e in E)
    S = cp_model.CpSolver(); S.parameters.num_workers = 2; S.parameters.max_time_in_seconds = 120
    for it in range(100):
        st = S.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return E, cur, cur, 'fail'
        sel = [e for e in cand if S.Value(X[e])]
        cs = ncomp(fixed + sel)
        if len(cs) == 1 or NOCUT: break
        for c in cs:
            m.Add(sum(X[e] for e in cand if (e[0] in c) != (e[1] in c)) >= 2)
        for e in cand: m.AddHint(X[e], S.Value(X[e]))
    val = round(S.ObjectiveValue())
    if val < cur: return set(fixed) | set(sel), cur, val, S.StatusName(st)
    return E, cur, cur, S.StatusName(st)
import os
NOCUT = bool(os.environ.get('NOCUT'))
total = 0
for sweep in range(4):
    gain = 0; t = time.time()
    for y0 in range(ylo, n-ylo-Wd+1, Wd//2):
        E, a, b, st = window(E, y0, y0+Wd-1); gain += a-b
        if a != b: print(f'  window {y0}..{y0+Wd-1}: {a} -> {b} ({st})', flush=True)
    print(f'sweep {sweep}: gain {gain}, {time.time()-t:.0f}s', flush=True)
    total += gain
    if not gain: break
code = [['' for _ in range(n)] for _ in range(n)]
for a, b in E:
    for p, q in ((a, b), (b, a)):
        v = next(i for i, (dy, dx) in enumerate(MOVES) if (p[0]+dx, p[1]-dy) == q)
        code[n-1-p[1]][p[0]] += str(v)
Path(out).write_text(json.dumps(dict(n=n, source=Path(f).name, note=f'side {side} collar local search W={Wd}', tour=code)))
print('total gain', total, 'cycles', len(ncomp(E)))
if not NOCUT: print('checker (X, turns)', check(code))
