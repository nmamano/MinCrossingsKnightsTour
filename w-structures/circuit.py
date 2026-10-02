"""Exact single-cycle completion with CP-SAT AddCircuit: cells outside `free` keep their edges; maximal
fixed chains are contracted to one node. Minimises crossings involving free edges. KT Structures 2026-10-02."""
import sys, time
from collections import defaultdict
from ortools.sat.python import cp_model
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import seg_cross
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def solve_circuit(n, E, free, tl=300, threads=2, hint=None, verbose=True, feas_only=False, ub=None):
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    E = set(E)
    adj = defaultdict(list)
    for a, b in E:
        adj[a].append(b); adj[b].append(a)
    # fixed chains: start from a free cell's forced neighbour, walk through non-free cells
    chains = []   # (a, b, cells) a,b free end cells
    seen_cell = set()
    for a in sorted(free):
        for q in adj[a]:
            if q in free or q in seen_cell:
                continue
            prev, cur, cells = a, q, [q]
            while cur not in free:
                nx = [w for w in adj[cur] if w != prev]
                assert len(nx) == 1, (cur, adj[cur])
                prev, cur = cur, nx[0]
                if cur not in free:
                    cells.append(cur)
            for c in cells: seen_cell.add(c)
            chains.append((a, cur, cells, (a, q), (prev, cur)))
    # sanity: every non-free cell is in a chain (no closed fixed cycles)
    nonfree = n * n - len(free)
    assert len(seen_cell) == nonfree, ('closed fixed cycle', nonfree - len(seen_cell))
    nodes = sorted(free)
    idx = {c: i for i, c in enumerate(nodes)}
    m = cp_model.CpModel()
    arcs = []
    lit = {}
    for a in nodes:
        for dx, dy in MOVES:
            b = (a[0] + dx, a[1] + dy)
            if b in free:
                v = m.NewBoolVar('')
                lit[(a, b)] = v
                arcs.append((idx[a], idx[b], v))
    N = len(nodes)
    end_edges = []   # forced edges between free cells and chains (for crossing accounting)
    for k, (a, b, cells, ea, eb) in enumerate(chains):
        P = N + k
        f = m.NewBoolVar(''); r = m.NewBoolVar('')
        m.Add(f + r == 1)
        if a == b:
            arcs.append((idx[a], P, f)); arcs.append((P, idx[a], f))
            arcs.append((idx[a], P, r)) if False else None
            m.Add(r == 0)
        else:
            arcs.append((idx[a], P, f)); arcs.append((P, idx[b], f))
            arcs.append((idx[b], P, r)); arcs.append((P, idx[a], r))
    m.AddCircuit(arcs)
    # undirected free-free edge vars
    und = {}
    for (a, b), v in lit.items():
        e = tuple(sorted([a, b]))
        und.setdefault(e, []).append(v)
    ue = sorted(und)
    xe = {}
    for e in ue:
        z = m.NewBoolVar('')
        m.Add(z == sum(und[e]))
        xe[e] = z
    # fixed segments near free region: forced edges into chains + chain edges near free cells
    fixed_near = set()
    for a, b, cells, ea, eb in chains:
        for e in (ea, eb):
            fixed_near.add(tuple(sorted(e)))
    for c in seen_cell:
        for q in adj[c]:
            fixed_near.add(tuple(sorted([c, q])))
    grid = defaultdict(list)
    for f_ in fixed_near:
        grid[(f_[0][0] // 4, f_[0][1] // 4)].append(f_)
    terms = []
    for i, e in enumerate(ue if (not feas_only or ub is not None) else []):
        for f_ in ue[i + 1:]:
            if abs(e[0][0] - f_[0][0]) <= 4 and abs(e[0][1] - f_[0][1]) <= 4 and seg_cross(e[0], e[1], f_[0], f_[1]):
                z = m.NewBoolVar(''); m.AddBoolOr([xe[e].Not(), xe[f_].Not(), z]); terms.append(z)
        gx, gy = e[0][0] // 4, e[0][1] // 4
        for a_ in (-1, 0, 1):
            for b_ in (-1, 0, 1):
                for f_ in grid.get((gx + a_, gy + b_), ()):
                    if seg_cross(e[0], e[1], f_[0], f_[1]):
                        terms.append(xe[e])
    if ub is not None:
        m.Add(sum(terms) <= ub)
    if not feas_only:
        m.Minimize(sum(terms))
    if hint:
        for e in ue:
            m.AddHint(xe[e], 1 if e in hint else 0)
    s = cp_model.CpSolver(); s.parameters.num_workers = threads; s.parameters.max_time_in_seconds = tl
    s.parameters.log_search_progress = False
    t0 = time.time()
    st = s.Solve(m)
    if verbose:
        print('circuit ub', ub, ':', s.StatusName(st), 'obj', s.ObjectiveValue() if st in (2, 4) else None, 'bound', s.BestObjectiveBound(), round(time.time() - t0), 's', 'nodes', N, 'chains', len(chains), flush=True)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    out = {e for e in E if e[0] not in free and e[1] not in free}
    for a, b, cells, ea, eb in chains:
        out.add(tuple(sorted(ea))); out.add(tuple(sorted(eb)))
    out |= {e for e in ue if s.Value(xe[e])}
    return out
