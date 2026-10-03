# KT Structures, 2026-10-03. BEYOND5 10.5 step 1 (P5): rebuild the collar of one vertical side of an H-regime tour.
# Free vertices: global x <= 2 (side 0) or x >= n-3 (side 1), rows ylo..n-1-ylo. All edges at free vertices are
# variables; every other tour edge is fixed. Minimise crossings that involve a variable edge, subject to degree 2 and
# one Hamiltonian cycle (lazy subtour cuts). Writes the new tour JSON. usage: p5_variant.py TOUR.json SIDE OUT.json [ylo]
import sys, json, time
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'w-verifier'))
from check import check, MOVES
from ortools.sat.python import cp_model
f, side, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]; ylo = int(sys.argv[4]) if len(sys.argv) > 4 else 8
grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
ed = lambda a, b: tuple(sorted((a, b)))
E = {ed((x, n-1-y), (x+MOVES[int(v)][1], n-1-y-MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
onb = lambda v: 0 <= v[0] < n and 0 <= v[1] < n
inw = lambda v: (v[0] <= 2 if side == 0 else v[0] >= n-3) and ylo <= v[1] <= n-1-ylo
KM = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
W = [(x, y) for x in range(n) for y in range(n) if inw((x, y))]
cand = sorted({ed(v, (v[0]+a, v[1]+b)) for v in W for a, b in KM if onb((v[0]+a, v[1]+b))})
fixed = [e for e in E if not (inw(e[0]) or inw(e[1]))]
def orient(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def cross(e, g):
    a, b = e; c, d = g
    return orient(a, b, c)*orient(a, b, d) < 0 and orient(c, d, a)*orient(c, d, b) < 0
near = lambda e, g: max(abs(e[0][0]-g[0][0]), abs(e[0][1]-g[0][1])) <= 4
m = cp_model.CpModel(); X = {e: m.NewBoolVar('') for e in cand}
fdeg = defaultdict(int)
for a, b in fixed: fdeg[a] += 1; fdeg[b] += 1
inc = defaultdict(list)
for e in cand: inc[e[0]].append(e); inc[e[1]].append(e)
for v, es in inc.items(): m.Add(sum(X[e] for e in es) == 2 - fdeg[v])
obj = []
fixed_near = [g for g in fixed if (g[0][0] <= 7 if side == 0 else g[0][0] >= n-8 or g[1][0] >= n-8)]
for e in cand:
    k = sum(1 for g in fixed_near if near(e, g) and cross(e, g))
    if k: obj.append(k * X[e])
for i, e in enumerate(cand):
    for g in cand[i+1:]:
        if near(e, g) and cross(e, g):
            z = m.NewBoolVar(''); m.AddBoolOr([X[e].Not(), X[g].Not(), z]); obj.append(z)
import os
HAM = os.environ.get('HAM')
if HAM:
    def lp(v):  # local frame of the side: (distance from side, row)
        return (v[0], v[1]) if side == 0 else (n-1-v[0], v[1])
    s0 = 1 if side == 0 else -1   # side 0 ports point down, side 1 up (LF1 local frames)
    pat = [((0, 0), (1, -2*s0)), ((0, 0), (2, -1*s0)), ((1, 0), (3, -1*s0)), ((2, 0), (4, -1*s0))]
    def glob(p): return (p[0], p[1]) if side == 0 else (n-1-p[0], p[1])
    P = set()
    for y in range(n):
        for a, b in pat:
            u, w = glob((a[0], y+a[1])), glob((b[0], y+b[1]))
            if onb(u) and onb(w): P.add(ed(u, w))
    print('P pattern edges among variables', sum(e in P for e in cand), flush=True)
    m.Minimize(int(HAM) * sum(X[e] for e in cand if e not in P) + sum(obj))
else:
    m.Minimize(sum(obj))
cur = sum(1 for e in cand if e in E)
print(n, 'free vertices', len(W), 'variables', len(cand), 'tour edges there', cur, flush=True)
def comps(sel):
    adj = defaultdict(list)
    for a, b in list(fixed) + sel: adj[a].append(b); adj[b].append(a)
    seen = set(); cs = []
    for v in adj:
        if v in seen: continue
        st = [v]; seen.add(v); c = []
        while st:
            u = st.pop(); c.append(u)
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        cs.append(set(c))
    return cs
S = cp_model.CpSolver(); S.parameters.num_workers = 2; S.parameters.max_time_in_seconds = float(sys.argv[5]) if len(sys.argv) > 5 else 600
for it in range(200):
    t = time.time(); st = S.Solve(m)
    sel = [e for e in cand if S.Value(X[e])]
    cs = comps(sel)
    print(f'iter {it} {S.StatusName(st)} nonP {sum(1 for e in sel if HAM and e not in P)} obj {S.ObjectiveValue():.0f} bound {S.BestObjectiveBound():.0f} cycles {len(cs)} {time.time()-t:.0f}s', flush=True)
    if len(cs) == 1: break
    for c in cs:
        cut = [X[e] for e in cand if (e[0] in c) != (e[1] in c)]
        if cut: m.Add(sum(cut) >= 2)
        else: print('  a cycle with no variable edge on its boundary: infeasible with this window', len(c)); sys.exit(1)
    m.ClearHints()
    for e in cand: m.AddHint(X[e], S.Value(X[e]))
# original objective for reference
orig = sum(1 for i, e in enumerate(cand) if e in E for g in fixed_near if near(e, g) and cross(e, g)) + \
       sum(1 for i, e in enumerate(cand) if e in E for g in cand[i+1:] if g in E and near(e, g) and cross(e, g))
print('original tour objective', orig)
newE = set(fixed) | set(sel)
code = [['' for _ in range(n)] for _ in range(n)]
for a, b in newE:
    for p, q in ((a, b), (b, a)):
        v = next(i for i, (dy, dx) in enumerate(MOVES) if (p[0]+dx, p[1]-dy) == q)
        code[n-1-p[1]][p[0]] += str(v)
Path(out).write_text(json.dumps(dict(n=n, source=Path(f).name, note=f'side {side} collar rebuilt rows {ylo}..{n-1-ylo}, min crossings', tour=code)))
print('checker', check(code))
