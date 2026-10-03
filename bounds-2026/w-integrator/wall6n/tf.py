"""2-factor relaxation of kt.board.complete (degree 2 at every free cell, no single-cycle constraint).
Same crossing objective and ties. KT Integrator, 2026-10-03 (wall6n)."""
import sys, time
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from collections import defaultdict
from ortools.sat.python import cp_model
from kt.board import MOV8, seg_cross
def twofactor(n, nb, free, time_limit=60, workers=3, verbose=False, hint=True, turn_weight=0,
             crossing_weight=1000, feasibility=False, ties=()):
    """Fill the free cells so the whole graph is one Hamiltonian cycle and minimise crossings.
    The fixed part is contracted to one dummy node per fixed path, and CP-SAT AddCircuit forces a
    single Hamiltonian circuit over free cells + dummies (no lazy cuts needed).
    hint=True: hint each free cell with its tiled (skeleton) moves where they are free-free edges."""
    on = lambda c: 0 <= c[0] < n and 0 <= c[1] < n
    for c, s in nb.items():
        if c in free: continue
        for v in s:
            if not on(v): return None, f'fixed cell {c} points off board to {v}'
            if v not in free and c not in nb[v]: return None, f'fixed asym {c}->{v}'
        if len(s) != 2: return None, f'fixed cell {c} has degree {len(s)}'
    forced = defaultdict(set)
    for c, s in nb.items():
        if c in free: continue
        for v in s:
            if v in free: forced[v].add(c)
    for c in free:
        if len(forced[c]) > 2: return None, f'overforced {c}'
    var = []
    for c in sorted(free):
        for d in MOV8:
            v = (c[0] + d[0], c[1] + d[1])
            if v in free and c < v: var.append((c, v))
    m = cp_model.CpModel()
    xv = []
    inc = defaultdict(list)
    for (a_, b_) in var:
        x = m.NewBoolVar(''); xv.append(x); inc[a_].append(x); inc[b_].append(x)
    for c in free:
        m.Add(sum(inc[c]) + len(forced[c]) == 2)
    fixed_near = set()
    for c in (free if not feasibility else ()):
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                w = (c[0] + dx, c[1] + dy)
                if on(w) and w not in free:
                    for v in nb[w]:
                        fixed_near.add(tuple(sorted([w, v])))
    terms = []
    by = defaultdict(list)
    for i, e in enumerate(var): by[e[0]].append(('v', i, e))
    for e in fixed_near: by[e[0]].append(('f', None, e))
    for i, e in enumerate(var if not feasibility else ()):
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                for kind, j, f in by.get((e[0][0] + dx, e[0][1] + dy), ()):
                    if kind == 'v' and j <= i: continue
                    if seg_cross(e[0], e[1], f[0], f[1]):
                        if kind == 'f': terms.append(xv[i])
                        else:
                            z = m.NewBoolVar(''); m.AddBoolOr([xv[i].Not(), xv[j].Not(), z]); terms.append(z)
    idx = {e: i for i, e in enumerate(var)}
    for e1, e2 in ties:                       # periodicity: tie two free-free edges
        e1, e2 = tuple(sorted(e1)), tuple(sorted(e2))
        if e1 in idx and e2 in idx:
            m.Add(xv[idx[e1]] == xv[idx[e2]])
    tterms = []
    if turn_weight:
        for c in free:
            st = []
            for d in MOV8[:4]:
                ends = [(c[0] + d[0], c[1] + d[1]), (c[0] - d[0], c[1] - d[1])]
                lits, ok = [], True
                for w in ends:
                    if w in forced[c]: continue
                    e = (min(c, w), max(c, w))
                    if e in idx: lits.append(xv[idx[e]])
                    else: ok = False
                if ok:
                    s_ = m.NewBoolVar('')
                    for l in lits: m.AddImplication(s_, l)
                    st.append(s_)
            t = m.NewBoolVar(''); m.Add(sum(st) + t >= 1); tterms.append(t)
    if not feasibility:
        m.Minimize(crossing_weight * sum(terms) + turn_weight * sum(tterms))
    if hint is True:
        for i, (a, b) in enumerate(var):
            m.AddHint(xv[i], int(b in nb[a] and a in nb[b]))
    elif isinstance(hint, dict):
        for i, (a, b) in enumerate(var):
            m.AddHint(xv[i], int(b in hint.get(a, ())))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers
    if verbose: s.parameters.log_search_progress = True
    t0 = time.time()
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, f'completion {s.StatusName(r)} after {time.time() - t0:.1f}s'
    full = {c: set(v) for c, v in nb.items()}
    for c in free: full[c] = set(forced[c])
    for i, (a, b) in enumerate(var):
        if s.Value(xv[i]): full[a].add(b); full[b].add(a)
    cx = sum(s.Value(t) for t in terms)
    ct = sum(s.Value(t) for t in tterms) if tterms else None
    return full, dict(status=s.StatusName(r), corner_obj=cx, corner_turns=ct, obj=s.ObjectiveValue(),
                      bound=s.BestObjectiveBound() // max(crossing_weight, 1) if crossing_weight >= turn_weight
                      else s.BestObjectiveBound(), secs=round(time.time() - t0, 1))

