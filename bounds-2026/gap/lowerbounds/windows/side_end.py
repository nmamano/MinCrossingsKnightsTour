#!/usr/bin/env python3
"""Item (a): side end-zone charge with the side strip at baseline (gap/lowerbounds FINDINGS, section A).

Periodic side cylinder. Board side at x = 0 (no cells at x < 0). Cells (x, y), 0 <= x <= W+1, y in Z_P.
Core x < W: degree exactly 2; halo x in {W, W+1}: degree <= 2. Edges: knight edges with an end in the core.
No finite cycle in the lift (lazy cuts on zero-winding cycles of the quotient).
Hypothesis H (case (b) of W3): no crossing outside S* among the modelled edges (S*: both edges touch
column <= 1), and every quarter of a square [x, x+1] x [y, y+1] with 4 <= x <= W-1 has multiplicity 1.
Charge at row r: the end zone of gamma at the dual row y = r + 1/2, i.e. the exact colour flux omega summed
over the dual steps that cross the grid edges (x, r)-(x, r+1), x = 2..W-1, is nonzero mod 3; the inward
exception pair (0,r)-(2,r+1), (0,r+1)-(2,r) is absent. Under H, steps with x >= 5 have omega = 0 mod 3.
Objective: S* crossings per period minus P (the baseline is one crossing per row).
usage: side_end.py P W ROWS [TIME] [KMAX|-] [pass]   ROWS: comma list of charged rows, 'all', or 'none';
       pass: the up test value F = 2 at the charged rows (so E != 0 means a height mismatch)
       KMAX given: decision version, excess <= KMAX (feasibility, no objective)
"""
import sys, time, json
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from check_frac_obstruction import crosses
from w3_quarters import tile, inside, quarters
from w3_flux import edge_flux, grid_term

MOVES = [(1, 2), (1, -2), (2, 1), (2, -1)]
TAB = {((0, -1), (1, 1)): -1, ((0, 0), (1, -2)): -1, ((0, 0), (2, -1)): -1, ((0, 1), (1, -1)): 1,
       ((0, 1), (2, 0)): 1, ((0, 2), (1, 0)): -1, ((1, 0), (2, 2)): -1, ((1, 1), (2, -1)): -1}


def build(P, W):
    cells = [(x, y) for x in range(W + 2) for y in range(P)]
    edges = [((x, y), (dx, dy)) for x in range(W) for y in range(P) for dx, dy in MOVES if x + dx <= W + 1]
    lift = lambda e, k=0: ((e[0][0], e[0][1] + k * P), (e[0][0] + e[1][0], e[0][1] + e[1][1] + k * P))
    ends = lambda e: [e[0], (e[0][0] + e[1][0], (e[0][1] + e[1][1]) % P)]
    return cells, edges, lift, ends


def components(sel, P, lift, ends):
    """Cycles of the quotient graph (max degree 2): list of (edge list, winding in rows)."""
    adj = {}
    for e in sel:
        a, b = ends(e)
        adj.setdefault(a, []).append((e, b, +1)); adj.setdefault(b, []).append((e, a, -1))
    seen = set(); out = []
    for s in adj:
        if len(adj[s]) != 2 or adj[s][0][0] in seen: continue
        path = []; cur = s; prev = None; dy = 0
        while True:
            nxt = [t for t in adj[cur] if t[0] != prev]
            if len(adj[cur]) != 2 or not nxt: path = None; break
            e, b, sg = nxt[0]
            if e in seen: break
            seen.add(e); path.append(e); dy += sg * e[1][1]; prev = e; cur = b
            if cur == s: break
        if path is not None and cur == s: out.append((path, dy))
    return out


def main():
    P, W, rows = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    T = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    KMAX = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != '-' else None
    PASS = len(sys.argv) > 6 and sys.argv[6] == 'pass'
    rows = list(range(P)) if rows == 'all' else [] if rows == 'none' else [int(r) for r in rows.split(',')]
    cells, edges, lift, ends = build(P, W)
    M = cp_model.CpModel(); v = {e: M.NewBoolVar('') for e in edges}
    inc = {}
    for e in edges:
        for p in ends(e): inc.setdefault(p, []).append(v[e])
    for p in cells:
        l = inc.get(p, [])
        M.Add(sum(l) == 2) if p[0] < W else M.Add(sum(l) <= 2)
    t1 = lambda e: e[0][0] <= 1
    xs = []
    for e, f in combinations(edges, 2):
        if any(crosses(lift(e), lift(f, k)) for k in (-1, 0, 1)):
            if t1(e) and t1(f):
                c = M.NewBoolVar(''); M.AddBoolAnd([v[e], v[f]]).OnlyEnforceIf(c)
                M.AddBoolOr([v[e].Not(), v[f].Not(), c]); xs.append((c, e, f))
            else:
                M.AddBoolOr([v[e].Not(), v[f].Not()])
    tiles = {(e, k): tile(lift(e, k)) for e in edges for k in (-1, 0, 1)}

    def cover(x, y, q):
        pt = quarters(x, y)[q]
        return [e for e in edges if any(inside(tiles[(e, k)], pt) for k in (-1, 0, 1))]
    mult = {(x, y, q): cover(x, y, q) for x in range(W) for y in range(P) for q in 'brtl'}
    for (x, y, q), l in mult.items():
        if x >= 4: M.Add(sum(v[e] for e in l) == 1)
    for r in rows:
        const = 0; c = {}
        for x in range(2, W):
            st = ((2 * x - 1, 2 * r + 1), (2 * x + 1, 2 * r + 1))
            const += grid_term(st)
            for e in edges:
                for k in (-1, 0, 1):
                    a, b = lift(e, k)
                    fl = edge_flux(((a[0], a[1]), (b[0], b[1])), st)
                    if fl: c[e] = c.get(e, 0) + fl
        z = M.NewIntVar(-500, 500, ''); rr = M.NewIntVar(1, 2, '')
        M.Add(const + sum(c[e] * v[e] for e in c) == 3 * z + rr)
        ex = [e for e in edges if e[0] == (0, r) and e[1] == (2, 1)] + \
             [e for e in edges if e[0] == (0, (r + 1) % P) and e[1] == (2, -1)]
        M.AddBoolOr([v[e].Not() for e in ex])
        if PASS:   # up test value F(r) = 2 mod 3 (audited coefficient table, translated by r)
            fsum = []
            for (a, b), cf in TAB.items():
                a, b = (a[0], a[1] + r), (b[0], b[1] + r)
                if a[0] > b[0]: a, b = b, a
                e = ((a[0], a[1] % P), (b[0] - a[0], b[1] - a[1]))
                fsum.append(cf * v[e])
            zf = M.NewIntVar(-10, 10, ''); M.Add(sum(fsum) == 3 * zf + 2)
    if KMAX is None: M.Minimize(sum(c for c, _, _ in xs))
    else: M.Add(sum(c for c, _, _ in xs) <= P + KMAX)
    t0 = time.time(); cuts = 0
    while True:
        s = cp_model.CpSolver(); s.parameters.num_workers = 2
        s.parameters.max_time_in_seconds = max(5, T - (time.time() - t0))
        st = s.Solve(M)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
        sel = [e for e in edges if s.Value(v[e])]
        bad = [p for p, dy in components(sel, P, lift, ends) if dy == 0]
        if not bad or time.time() - t0 > T: break
        for p in bad: M.AddBoolOr([v[e].Not() for e in p]); cuts += 1
    name = s.StatusName(st)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f'P={P} W={W} rows={rows} KMAX={KMAX}: {name} pass={PASS} (cuts {cuts}, {time.time() - t0:.0f}s)', flush=True); return
    X = sum(s.Value(c) for c, _, _ in xs)
    m = {k: sum(s.Value(v[e]) for e in l) for k, l in mult.items()}
    holes = sorted(k for k, val in m.items() if val == 0)
    w3 = sum((val - 1) * (val - 2) // 2 for val in m.values() if val >= 3)
    x1 = 0
    for c, e, f in xs:
        if s.Value(c):
            common = [k for k, l in mult.items() if e in l and f in l]
            x1 += len(common) == 1
    print(f'P={P} W={W} rows={rows} pass={PASS}: {name} excess per period = {X - P} (bound {s.BestObjectiveBound() - P if KMAX is None else 'decision'}); '
          f'holes {len(holes)} {holes[:8]}; X1 {x1}; W3 {w3}; cuts {cuts}; {time.time() - t0:.0f}s', flush=True)
    json.dump({'P': P, 'W': W, 'rows': rows, 'edges': [lift(e) for e in sel]},
              open(f'side_end_P{P}_W{W}_{"-".join(map(str, rows)) or "none"}.json', 'w'))


if __name__ == '__main__':
    main()
