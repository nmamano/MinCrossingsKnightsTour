"""Repair defect windows with CP-SAT and lazy subtour cuts (single Hamiltonian cycle). KT Structures."""
import sys, time
from collections import defaultdict, Counter
from ortools.sat.python import cp_model
import networkx as nx
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import seg_cross
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def clusters(bad, link=6):
    G = nx.Graph(); G.add_nodes_from(bad)
    for a in bad:
        for b in bad:
            if a < b and max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= link:
                G.add_edge(a, b)
    return [sorted(c) for c in nx.connected_components(G)]

def window_cells(n, cl, rad):
    xs = [p[0] for p in cl]; ys = [p[1] for p in cl]
    return {(x, y) for x in range(max(0, min(xs) - rad), min(n, max(xs) + rad + 1))
            for y in range(max(0, min(ys) - rad), min(n, max(ys) + rad + 1))}

def repair(n, E, free, threads=2, tlimit=120, single=True, verbose=True, max_rounds=200, check_only=False, hint=None, fast_tl=None, ub=None, cuts_in=None, cuts_out=None):
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    E = set(E)
    fixed = [e for e in E if e[0] not in free and e[1] not in free]
    cand = set()
    for p in free:
        for dx, dy in MOVES:
            q = (p[0] + dx, p[1] + dy)
            if on(q):
                e = tuple(sorted([p, q]))
                if q in free or e in E:
                    cand.add(e)
    cand = sorted(cand)
    m = cp_model.CpModel()
    xv = {e: m.NewBoolVar('') for e in cand}
    inc = defaultdict(list)
    for e in cand:
        inc[e[0]].append(e); inc[e[1]].append(e)
    for p in free:
        m.Add(sum(xv[e] for e in inc[p]) == 2)
    for e in cand:
        if not (e[0] in free and e[1] in free):
            m.Add(xv[e] == 1)
    terms = []
    if not check_only:
        grid = defaultdict(list)
        for f in fixed:
            grid[(f[0][0] // 4, f[0][1] // 4)].append(f)
        for i, e in enumerate(cand):
            for f in cand[i + 1:]:
                if abs(e[0][0] - f[0][0]) <= 4 and abs(e[0][1] - f[0][1]) <= 4 and seg_cross(e[0], e[1], f[0], f[1]):
                    z = m.NewBoolVar(''); m.AddBoolOr([xv[e].Not(), xv[f].Not(), z]); terms.append(z)
            gx, gy = e[0][0] // 4, e[0][1] // 4
            for a in (-1, 0, 1):
                for b in (-1, 0, 1):
                    for f in grid.get((gx + a, gy + b), ()):
                        if seg_cross(e[0], e[1], f[0], f[1]):
                            terms.append(xv[e])
        m.Minimize(sum(terms))
        if ub is not None:
            m.Add(sum(terms) <= int(ub))
    if hint is not None:
        for e in cand:
            m.AddHint(xv[e], 1 if e in hint else 0)
    G0 = nx.Graph(); G0.add_edges_from(fixed)
    for cset in (cuts_in or []):
        cut = [e for e in cand if (e[0] in cset) != (e[1] in cset)]
        if cut: m.Add(sum(xv[e] for e in cut) >= 2)
    rounds = 0
    final = False
    while True:
        s = cp_model.CpSolver(); s.parameters.num_workers = threads
        s.parameters.max_time_in_seconds = fast_tl if (fast_tl and not final) else tlimit
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            if verbose: print('  infeasible', s.StatusName(st))
            return None, s.StatusName(st)
        chosen = [e for e in cand if s.Value(xv[e])]
        G = G0.copy(); G.add_edges_from(chosen)
        cs = list(nx.connected_components(G))
        if verbose: print(f'  round {rounds}: {s.StatusName(st)} obj {s.ObjectiveValue() if terms else 0} comps {len(cs)}', flush=True)
        if len(cs) == 1 or not single or check_only:
            if fast_tl and not final and not check_only:
                final = True
                for e in cand:
                    m.AddHint(xv[e], 1 if e in set(chosen) else 0) if False else None
                continue
            repair.last_obj = s.ObjectiveValue() if terms else 0
            return set(fixed) | set(chosen), s.StatusName(st)
        for c in cs:
            cut = [e for e in cand if (e[0] in c) != (e[1] in c)]
            if not cut:
                if verbose: print('  component without free edges: cannot merge', len(c))
                return None, 'stuck'
            m.Add(sum(xv[e] for e in cut) >= 2)
            if cuts_out is not None: cuts_out.append(set(c))
        rounds += 1
        if rounds > max_rounds:
            return None, 'rounds'
