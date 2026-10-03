#!/usr/bin/env python3
"""Item (a), joint strip test: does strip excess pay for every row whose STRONG end test fails?

Same periodic side cylinder and hypothesis H as side_end.py (no crossing outside S*, quarters at depth >= 4
perfect). Strong test at row r: up test value F(r) = 2 mod 3, the inward exception pair at r absent, and the
end-zone flux E(r) = 0 mod 3. Free indicator g_r <= [strong test fails at r]. Objective (rate a/b):
    minimise  b * (S* crossings - P)  -  a * sum_r g_r,   subject to sum_r g_r >= 1.
A minimum >= 0 means: in every P-periodic configuration, excess >= (a/b) * (#rows failing the strong test).
usage: side_ratio.py P W a/b [TIME] [GMIN]
"""
import sys, time, json
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, '..')
from check_frac_obstruction import crosses
from w3_quarters import tile, inside, quarters
from w3_flux import edge_flux, grid_term
from side_end import build, components, TAB


def main():
    P, W = int(sys.argv[1]), int(sys.argv[2]); a, b = map(int, sys.argv[3].split('/'))
    T = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    GMIN = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    cells, edges, lift, ends = build(P, W)
    eid = {e: e for e in edges}
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
                M.AddBoolOr([v[e].Not(), v[f].Not(), c]); xs.append(c)
            else:
                M.AddBoolOr([v[e].Not(), v[f].Not()])
    tiles = {(e, k): tile(lift(e, k)) for e in edges for k in (-1, 0, 1)}
    for x in range(4, W):
        for y in range(P):
            for q, pt in quarters(x, y).items():
                M.Add(sum(v[e] for e in edges if any(inside(tiles[(e, k)], pt) for k in (-1, 0, 1))) == 1)

    def canon(a_, b_):
        if a_[0] > b_[0]: a_, b_ = b_, a_
        return ((a_[0], a_[1] % P), (b_[0] - a_[0], b_[1] - a_[1]))
    g = []
    for r in range(P):
        const = 0; c = {}
        for x in range(2, W):
            st = ((2 * x - 1, 2 * r + 1), (2 * x + 1, 2 * r + 1))
            const += grid_term(st)
            for e in edges:
                for k in (-1, 0, 1):
                    fl = edge_flux(lift(e, k), st)
                    if fl: c[e] = c.get(e, 0) + fl
        zE = M.NewIntVar(-500, 500, ''); rE = M.NewIntVar(0, 2, '')
        M.Add(const + sum(c[e] * v[e] for e in c) == 3 * zE + rE)
        fs = [cf * v[canon((p[0], p[1] + r), (q[0], q[1] + r))] for (p, q), cf in TAB.items()]
        zF = M.NewIntVar(-10, 10, ''); rF = M.NewIntVar(0, 2, '')
        M.Add(sum(fs) == 3 * zF + 2 + rF)      # rF = (F - 2) mod 3
        ex = [v[canon((0, r), (2, r + 1))], v[canon((0, r + 1), (2, r))]]
        eb, fb, xb = M.NewBoolVar(''), M.NewBoolVar(''), M.NewBoolVar('')
        M.Add(rE >= 1).OnlyEnforceIf(eb); M.Add(rF >= 1).OnlyEnforceIf(fb)
        M.AddBoolAnd(ex).OnlyEnforceIf(xb)
        gr = M.NewBoolVar(''); M.AddBoolOr([eb, fb, xb]).OnlyEnforceIf(gr); g.append(gr)
    M.Add(sum(g) >= GMIN)
    M.Minimize(b * (sum(xs) - P) - a * sum(g))
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
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f'P={P} W={W} rate {a}/{b} gmin={GMIN}: {s.StatusName(st)} (cuts {cuts})', flush=True); return
    X = sum(s.Value(c) for c in xs) - P; G = sum(s.Value(x) for x in g)
    print(f'P={P} W={W} rate {a}/{b} gmin={GMIN}: {s.StatusName(st)} min {s.ObjectiveValue():.0f} '
          f'(bound {s.BestObjectiveBound():.0f}); excess {X}, strong failures {G}; cuts {cuts}; '
          f'{time.time() - t0:.0f}s', flush=True)
    json.dump({'P': P, 'W': W, 'rows': [], 'edges': [lift(e) for e in sel]},
              open(f'side_ratio_P{P}_W{W}_{a}_{b}.json', 'w'))


if __name__ == '__main__':
    main()
