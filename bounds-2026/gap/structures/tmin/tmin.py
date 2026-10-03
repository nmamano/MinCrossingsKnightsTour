# KT Structures, 2026-10-04. Exact (or bounded) minimum turn count T_min on the n x n board, by CP-SAT.
# Model: one bool per (cell, pair of on-board moves); edge bools; edge consistency; turn objective.
# Valid cuts (any 2-factor): residual r(v) = t(v) - (side lower terms of w-turnstheory/check_corner_certificate.py)
# sums to T - 8n; each 4x4 corner square has residual sum >= -7 (certificate, 209 local pairs).
# Restriction (optional, NOT exact): cells at depth >= D from every side must be straight.
# Tours: AddCircuit (mode tour) or lazy subtour cuts (mode tourlazy). 2-factors: mode 2f.
# usage: tmin.py n mode D time_s out.json [hint.json]
import sys, json, time
from itertools import combinations
from pathlib import Path
from ortools.sat.python import cp_model
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from kt.core import validate, num_turns, num_cycles

MI = [-2, -1, 1, 2, 2, 1, -1, -2]
MJ = [1, 2, 2, 1, -1, -2, -2, -1]

def lower(x, ds):
    if x == 0: return 1
    if x in (1, 2): return sum(x + d in (0, 3) for d in ds) - 1
    if x == 3: return 1 - sum(x + d in (1, 2) for d in ds)
    return 0

def build(n, mode, D, hint=None, cuts=()):
    m = cp_model.CpModel()
    on = lambda i, j: 0 <= i < n and 0 <= j < n
    E = {}  # (cell, move) -> edge var, shared by both ends
    for i in range(n):
        for j in range(n):
            for k in range(8):
                a, b = i + MI[k], j + MJ[k]
                if on(a, b) and ((i, j), k) not in E:
                    v = m.NewBoolVar('')
                    E[(i, j), k] = v; E[(a, b), (k + 4) % 8] = v
    P = {}; obj = []; res = {}
    for i in range(n):
        for j in range(n):
            ks = [k for k in range(8) if on(i + MI[k], j + MJ[k])]
            depth = min(i, j, n - 1 - i, n - 1 - j)
            prs = [p for p in combinations(ks, 2) if not (D and depth >= D and (p[1] - p[0]) != 4)]
            vs = {}
            for p in prs:
                vs[p] = m.NewBoolVar('')
            m.AddExactlyOne(vs.values())
            for k in ks:
                m.Add(E[(i, j), k] == sum(v for p, v in vs.items() if k in p))
            for p, v in vs.items():
                t = int(p[1] - p[0] != 4)
                if t: obj.append(v)
                di = [MI[k] for k in p]; dj = [MJ[k] for k in p]
                r = t - lower(j, dj) - lower(n - 1 - j, [-d for d in dj]) - lower(i, di) - lower(n - 1 - i, [-d for d in di])
                res[(i, j), p] = (r, v)
            P[i, j] = vs
    for ci in (0, n - 4):
        for cj in (0, n - 4):
            m.Add(sum(r * v for ((i, j), p), (r, v) in res.items() if ci <= i < ci + 4 and cj <= j < cj + 4) >= -7)
    T = sum(obj)
    m.Add(T >= 8 * n - 28)
    m.Minimize(T)
    if mode == 'tour':
        arcs = []; idx = lambda i, j: i * n + j
        seen = set()
        for ((i, j), k), v in E.items():
            a, b = i + MI[k], j + MJ[k]
            if (a, b, i, j) in seen: continue
            seen.add((i, j, a, b))
            f, g = m.NewBoolVar(''), m.NewBoolVar('')
            arcs += [(idx(i, j), idx(a, b), f), (idx(a, b), idx(i, j), g)]
            m.Add(f + g == v)
        m.AddCircuit(arcs)
    for S in cuts:
        Sset = set(S)
        m.Add(sum(v for ((i, j), k), v in E.items() if (i, j) in Sset and (i + MI[k], j + MJ[k]) not in Sset) >= 2)
    if hint:
        for (i, j), vs in P.items():
            c = hint[i][j]; p = tuple(sorted(int(ch) for ch in c))
            for q, v in vs.items():
                m.AddHint(v, q == p)
    return m, P, T

def grid(solver, P, n):
    g = [['' for _ in range(n)] for _ in range(n)]
    for (i, j), vs in P.items():
        for p, v in vs.items():
            if solver.Value(v): g[i][j] = '%d%d' % p
    return g

def components(g, n):
    seen = set(); comps = []
    for s in ((i, j) for i in range(n) for j in range(n)):
        if s in seen: continue
        st = [s]; seen.add(s); C = [s]
        while st:
            i, j = st.pop()
            for ch in g[i][j]:
                q = (i + MI[int(ch)], j + MJ[int(ch)])
                if q not in seen: seen.add(q); st.append(q); C.append(q)
        comps.append(C)
    return comps

def main():
    n, mode, D, tl, out = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    hint = json.loads(Path(sys.argv[6]).read_text())['grid'] if len(sys.argv) > 6 else None
    t0 = time.time(); cuts = []; best = None; it = 0; lb = None
    while True:
        it += 1
        left = tl - (time.time() - t0)
        if left < 5: break
        m, P, T = build(n, 'tour' if mode == 'tour' else '2f', D, hint, cuts)
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = left; s.parameters.cp_model_presolve = False
        st = s.Solve(m); name = s.StatusName(st)
        lb = int(round(s.BestObjectiveBound())) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else lb
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f'it {it} {name}', flush=True); break
        g = grid(s, P, n); comps = components(g, n); Tv = int(s.ObjectiveValue())
        print(f'it {it} {name} T-8n={Tv - 8 * n} bound={lb - 8 * n} cycles={len(comps)} t={time.time() - t0:.0f}s', flush=True)
        if mode != 'tourlazy' or len(comps) == 1:
            best = (g, Tv, name, len(comps)); break
        cuts += [C for C in comps]; hint = None
    if best is None:
        print('no solution'); return
    g, Tv, name, nc = best
    assert num_turns(g) == Tv
    if mode != '2f': assert validate(g)
    rec = dict(n=n, mode=mode, D=D, T=Tv, T_minus_8n=Tv - 8 * n, bound_minus_8n=lb - 8 * n, status=name,
               cycles=nc, seconds=round(time.time() - t0, 1), exact=(D == 0), date='2026-10-04', grid=g)
    Path(out).write_text(json.dumps(rec))
    print('RESULT', json.dumps({k: v for k, v in rec.items() if k != 'grid'}), flush=True)

if __name__ == '__main__':
    main()
