#!/usr/bin/env python
"""Turns-only corner re-solve for a periodic edge-gadget skeleton (KT Edge Searcher, 2026-10-04).

Free region at each corner: union of an A x B and a B x A rectangle (A >= B; A = B gives a square).
Mode 'tour' : AddCircuit over free cells + one dummy per contracted fixed path (one closed tour).
Mode '2f'   : degree 2 only (2-factor floor); corners are independent, so each corner is solved alone.
Objective: number of turns (all cells; fixed cells are constant).
Usage: csolve.py --combo w-integrator/corners/TT16_res00.json --n 56 --A 10 --B 10 --mode 2f
"""
import argparse, json, math, os, sys, time
from collections import defaultdict
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'w-integrator'))
from ortools.sat.python import cp_model
from kt.board import build_general, fixed_paths, to_grid, MOV8
from kt.core import validate, num_turns

def lower(x, ds):   # side charge of w-turnstheory/check_corner_certificate.py (sums to 8n over a tour)
    if x == 0: return 1
    if x in (1, 2): return sum(x + d in (0, 3) for d in ds) - 1
    if x == 3: return 1 - sum(x + d in (1, 2) for d in ds)
    return 0

def ls(n, c, a, b):
    dx = [a[0] - c[0], b[0] - c[0]]; dy = [a[1] - c[1], b[1] - c[1]]
    return (lower(c[0], dx) + lower(n - 1 - c[0], [-d for d in dx]) +
            lower(c[1], dy) + lower(n - 1 - c[1], [-d for d in dy]))

def region(n, A, B):
    out = {}
    for k, (sx, sy) in {'BL': (1, 1), 'BR': (-1, 1), 'TL': (1, -1), 'TR': (-1, -1)}.items():
        cells = set()
        for (w, h) in ((A, B), (B, A)):
            for i in range(w):
                for j in range(h):
                    cells.add((i if sx > 0 else n - 1 - i, j if sy > 0 else n - 1 - j))
        out[k] = cells
    return out

def two_factor_exists(free, forced):
    """Knight graph is bipartite (colour x + y): degree-2 completion exists iff a b-matching flow saturates."""
    import networkx as nx
    G = nx.DiGraph(); need = 0
    for c in free:
        r = 2 - len(forced[c])
        if (c[0] + c[1]) % 2 == 0:
            G.add_edge('s', c, capacity=r); need += r
            for d in MOV8:
                v = (c[0] + d[0], c[1] + d[1])
                if v in free: G.add_edge(c, v, capacity=1)
        else:
            G.add_edge(c, 't', capacity=r)
    if 's' not in G or 't' not in G: return need == 0
    tot = sum(2 - len(forced[c]) for c in free if (c[0] + c[1]) % 2)
    return tot == need and nx.maximum_flow_value(G, 's', 't') == need

def solve(n, nb, free, mode='tour', time_limit=120, workers=2, hint=None, log=False, res=False, ties=(), cuts=(), ub=None):
    forced = defaultdict(set)
    for c, s in nb.items():
        if c in free: continue
        for v in s:
            if v in free: forced[v].add(c)
    for c in free:
        if len(forced[c]) > 2: return None, 'overforced'
    if not two_factor_exists(free, forced): return None, 'no 2-factor (b-matching flow)'
    var = []
    for c in sorted(free):
        for d in MOV8:
            v = (c[0] + d[0], c[1] + d[1])
            if v in free and c < v: var.append((c, v))
    idx = {e: i for i, e in enumerate(var)}
    m = cp_model.CpModel()
    # pair formulation: each free cell picks one pair of neighbours (forced ones included)
    opt = defaultdict(list)      # (c, w) -> option literals at c that use neighbour w
    optd = defaultdict(dict)     # c -> {(da, db): literal}, directions relative to c
    tt = []
    for c in sorted(free):
        nbrs = [(c[0] + d[0], c[1] + d[1]) for d in MOV8]
        cand = [w for w in nbrs if w in free or w in forced[c]]
        lits = []
        for i in range(len(cand)):
            for j in range(i + 1, len(cand)):
                a, b = cand[i], cand[j]
                if any(f not in (a, b) for f in forced[c]): continue
                z = m.NewBoolVar(''); lits.append(z)
                opt[c, a].append(z); opt[c, b].append(z)
                optd[c][tuple(sorted([(a[0] - c[0], a[1] - c[1]), (b[0] - c[0], b[1] - c[1])]))] = z
                t = int(a[0] + b[0] != 2 * c[0] or a[1] + b[1] != 2 * c[1])
                k = t - ls(n, c, a, b) if res else t
                if k: tt.append(k * z)
        if not lits: return None, f'no option at {c}'
        m.AddExactlyOne(lits)
    for c1, c2 in ties:          # periodicity: c2 copies the move pair of c1
        if c1 not in free or c2 not in free: continue
        for k in set(optd[c1]) | set(optd[c2]):
            z1, z2 = optd[c1].get(k), optd[c2].get(k)
            if z1 is None: m.Add(z2 == 0)
            elif z2 is None: m.Add(z1 == 0)
            else: m.Add(z1 == z2)
    xv = []
    for (a, b) in var:
        x = m.NewBoolVar(''); xv.append(x)
        m.Add(sum(opt[a, b]) == x); m.Add(sum(opt[b, a]) == x)
    for S in cuts:               # subtour cut: a closed cycle on cell set S needs 2 free edges leaving S
        lv = [xv[i] for i, (a, b) in enumerate(var) if (a in S) != (b in S)]
        m.Add(sum(lv) >= 2)
    if mode == 'tour':
        paths, closed = fixed_paths(n, nb, free)
        if closed: return None, 'closed fixed cycles'
        node = {c: i for i, c in enumerate(sorted(free))}; N = len(node); arcs = []
        for i, (a, b) in enumerate(var):
            f, r = m.NewBoolVar(''), m.NewBoolVar('')
            arcs += [(node[a], node[b], f), (node[b], node[a], r)]; m.Add(xv[i] == f + r)
        for k, (u, v, cells) in enumerate(paths):
            d = N + k
            l1, l2, l3, l4 = [m.NewBoolVar('') for _ in range(4)]
            arcs += [(node[u], d, l1), (d, node[v], l2), (node[v], d, l3), (d, node[u], l4)]
            m.Add(l1 + l3 == 1); m.Add(l1 == l2); m.Add(l3 == l4)
        m.AddCircuit(arcs)
    if ub is not None: m.Add(sum(tt) <= ub)
    m.Minimize(sum(tt))
    if hint:
        for i, (a, b) in enumerate(var): m.AddHint(xv[i], int(b in hint.get(a, ())))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = workers
    s.parameters.log_search_progress = log; s.parameters.linearization_level = 2
    t0 = time.time(); r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return None, s.StatusName(r)
    full = {c: set(v) for c, v in nb.items()}
    for c in free: full[c] = set(forced[c])
    for i, (a, b) in enumerate(var):
        if s.Value(xv[i]): full[a].add(b); full[b].add(a)
    return full, dict(status=s.StatusName(r), turns=int(s.ObjectiveValue()), bound=int(s.BestObjectiveBound()),
                      secs=round(time.time() - t0, 1))

def ncycles(full):
    seen, k = set(), 0
    for c in full:
        if c in seen: continue
        k += 1; st = [c]
        while st:
            v = st.pop()
            if v in seen: continue
            seen.add(v); st.extend(full[v])
    return k

def load_combo(path):
    d = json.load(open(path))
    return d['bottom'], d['left'], d['top'], d['right'], tuple(d['phases'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--combo', required=True); ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--A', type=int, default=8); ap.add_argument('--B', type=int, default=8)
    ap.add_argument('--mode', default='2f', choices=['2f', 'tour']); ap.add_argument('--time', type=float, default=120)
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--out'); ap.add_argument('--log', action='store_true'); ap.add_argument('--corners'); ap.add_argument('--res', action='store_true')
    a = ap.parse_args()
    Bt, Lt, Tt, Rt, ph = load_combo(a.combo)
    nb, _ = build_general(a.n, Bt, Lt, Tt, Rt, phases=ph, Z=6)
    reg = region(a.n, a.A, a.B)
    base = to_grid(a.n, nb)  # skeleton turns outside the free cells (inside: interior lines, ignored)
    if a.mode == '2f':
        full = {c: set(v) for c, v in nb.items()}; res = {}
        for k, cells in reg.items():
            if a.corners and k not in a.corners.split(','): continue
            f, info = solve(a.n, nb, cells, '2f', a.time, a.workers, log=a.log, res=a.res)
            if f is None: print(k, info); return
            for c in cells: full[c] = f[c]
            res[k] = info
    else:
        free = set().union(*reg.values())
        full, res = solve(a.n, nb, free, 'tour', a.time, a.workers, hint=None, log=a.log, res=a.res)
        if full is None: print('FAIL', res); return
    g = to_grid(a.n, full)
    T = num_turns(g)
    LS = sum(ls(a.n, c, *sorted(v)) for c, v in full.items())
    assert LS == 8 * a.n, ('side-charge identity fails', LS)
    print(f'n={a.n} A={a.A} B={a.B} mode={a.mode} T={T} T-8n={T - 8 * a.n} cycles={ncycles(full)} '
          f'valid_tour={validate(g)} info={res}', flush=True)
    if a.out:
        json.dump(dict(n=a.n, A=a.A, B=a.B, mode=a.mode, T=T, info=res, combo=a.combo, tour=g), open(a.out, 'w'))

if __name__ == '__main__':
    main()

def solve_mip(n, nb, free, time_limit=600, res=True, ties=(), cuts=(), ub=None, backend='SCIP', log=False):
    """Same 2f model as solve(mode='2f') on an LP-based MIP solver (pywraplp); for bound proofs."""
    from ortools.linear_solver import pywraplp
    forced = defaultdict(set)
    for c, s in nb.items():
        if c in free: continue
        for v in s:
            if v in free: forced[v].add(c)
    if any(len(forced[c]) > 2 for c in free): return None, 'overforced'
    var = []
    for c in sorted(free):
        for d in MOV8:
            v = (c[0] + d[0], c[1] + d[1])
            if v in free and c < v: var.append((c, v))
    m = pywraplp.Solver.CreateSolver(backend)
    opt = defaultdict(list); optd = defaultdict(dict); obj = []
    for c in sorted(free):
        cand = [w for w in ((c[0] + d[0], c[1] + d[1]) for d in MOV8) if w in free or w in forced[c]]
        lits = []
        for i in range(len(cand)):
            for j in range(i + 1, len(cand)):
                a, b = cand[i], cand[j]
                if any(f not in (a, b) for f in forced[c]): continue
                z = m.BoolVar(''); lits.append(z)
                opt[c, a].append(z); opt[c, b].append(z)
                optd[c][tuple(sorted([(a[0] - c[0], a[1] - c[1]), (b[0] - c[0], b[1] - c[1])]))] = z
                t = int(a[0] + b[0] != 2 * c[0] or a[1] + b[1] != 2 * c[1])
                k = t - ls(n, c, a, b) if res else t
                if k: obj.append(k * z)
        if not lits: return None, f'no option at {c}'
        m.Add(sum(lits) == 1)
    for c1, c2 in ties:
        if c1 not in free or c2 not in free: continue
        for k in set(optd[c1]) | set(optd[c2]):
            z1, z2 = optd[c1].get(k), optd[c2].get(k)
            if z1 is None: m.Add(z2 == 0)
            elif z2 is None: m.Add(z1 == 0)
            else: m.Add(z1 == z2)
    xv = []
    for (a, b) in var:
        x = m.BoolVar(''); xv.append(x)
        m.Add(sum(opt[a, b]) == x); m.Add(sum(opt[b, a]) == x)
    for S in cuts:
        m.Add(sum(xv[i] for i, (a, b) in enumerate(var) if (a in S) != (b in S)) >= 2)
    if ub is not None: m.Add(sum(obj) <= ub)
    m.Minimize(sum(obj))
    m.SetTimeLimit(int(time_limit * 1000))
    if log: m.EnableOutput()
    t0 = time.time(); r = m.Solve()
    names = {m.OPTIMAL: 'OPTIMAL', m.FEASIBLE: 'FEASIBLE', m.INFEASIBLE: 'INFEASIBLE', m.NOT_SOLVED: 'UNKNOWN'}
    st = names.get(r, str(r))
    if r not in (m.OPTIMAL, m.FEASIBLE): return None, st
    full = {c: set(v) for c, v in nb.items()}
    for c in free: full[c] = set(forced[c])
    for i, (a, b) in enumerate(var):
        if xv[i].solution_value() > 0.5: full[a].add(b); full[b].add(a)
    return full, dict(status=st, turns=int(round(m.Objective().Value())), bound=int(math.ceil(m.Objective().BestBound() - 1e-6)),
                      secs=round(time.time() - t0, 1))
