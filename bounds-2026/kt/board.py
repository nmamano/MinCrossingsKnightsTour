"""Assemble a full n x n tour from periodic edge gadgets + CP-SAT corner completion.

Board coords (x, y): x column (right), y row (up), 0..n-1.  Interior: lines x+2y=c ('26').
bottom_tpl: rows top-first (like Sequence1), period P_B = width, depth D_B = #rows, local off 0.
left_tpl  : rows top-first, columns x=0..D_L-1, period Q = #rows, local lane offset off_L.
Lane-pair alignment: bottom/right pairs start at c = off_L (mod 8); left/top at off_L+4.
Checked 2026-10-02 (Integrator): with global line c = x + 2y,
  bottom cell x <- local x' = x - x0:            c = c' + x0            -> pair start x0 = off_L
  left   cell y <- local y' = y - y0:            c = c' + 2*y0          -> pair start off_L + 2*y0 = off_L + 4
  top    (x,y) = (X0 - x', n-1-y'):              c = X0 + 2n - 2 - c'   -> pair start X0 + 2n - 1 = off_L + 4
  right  (x,y) = (n-1-x', Y0 - y'):              c = n - 1 + 2*Y0 - c'  -> pair start n + 2*Y0 - off_L = off_L
(all mod 8; a reflected pair [a, a+8) maps to (K-a-8, K-a]).  Full tours confirm it (w-integrator/).
The corner zones are filled by complete(): CP-SAT AddCircuit over the free cells plus one dummy node
per contracted fixed path, so every solution is one Hamiltonian cycle.
"""
import time
from collections import defaultdict
from ortools.sat.python import cp_model
from .core import MI, MJ, seg_cross

def tpl_moves(tpl):
    rows = [r.split(' ') for r in tpl]
    H = len(rows)
    out = {}
    for r, row in enumerate(rows):
        for x, code in enumerate(row):
            out[(x, H - 1 - r)] = [(MJ[int(m)], -MI[int(m)]) for m in code]
    return out, len(rows[0]), H

def build_skeleton(n, bottom_tpl, left_tpl, off_L=0, Z=14, bx=0, ly=0):
    """Lane-design skeleton (bottom template at local lane offset 0, left at off_L)."""
    bm, PB, DB = tpl_moves(bottom_tpl)
    lm, DL, Q = tpl_moves(left_tpl)
    assert PB % 8 == 0 and Q % 4 == 0, 'alignment needs bottom period % 8 == 0, left period % 4 == 0'
    beta = off_L % 8
    x0 = (beta + bx) % PB                         # bottom: pairs start at c = x0 (mod 8)
    X0 = (beta + 13 - 2 * n) % 8                  # top
    y0 = 2 + 4 * ly                               # left
    Y0 = (off_L - n // 2) % 4                     # right
    return build_general(n, bottom_tpl, left_tpl, phases=(x0, X0, y0, Y0), Z=Z)

def build_general(n, bottom_tpl, left_tpl, top_tpl=None, right_tpl=None, phases=(0, 0, 0, 0), Z=14):
    """General skeleton: any four periodic edge templates, any phases.
    bottom_tpl / top_tpl are bottom-type (edge at the bottom, rows top-first); top is placed
    rotated 180.  left_tpl / right_tpl are left-type (edge at the left); right is placed rotated 180.
    top/right default to bottom/left.  phases = (xb, xt, yl, yr):
      bottom cell (x, y)        <- local ((x - xb) % P, y)
      top    cell (x, n-1-y)    <- local ((xt - x) % P, y), moves negated
      left   cell (x, y)        <- local (x, (y - yl) % Q)
      right  cell (n-1-x, y)    <- local (x, (yr - y) % Q), moves negated
    Interior cells are lines x + 2y = c.  Returns (nb, free) with free = four Z x Z corner zones."""
    top_tpl = top_tpl or bottom_tpl
    right_tpl = right_tpl or left_tpl
    bm, PB, DB = tpl_moves(bottom_tpl)
    tm, PT, DT = tpl_moves(top_tpl)
    lm, DL, QL = tpl_moves(left_tpl)
    rm, DR, QR = tpl_moves(right_tpl)
    assert Z > max(DB, DT, DL, DR) and 2 * Z <= n, 'zone must be deeper than the bands and fit the board'
    xb, xt, yl, yr = phases
    nb = {}
    for x in range(n):
        for y in range(n):
            nb[(x, y)] = {(x + 2, y - 1), (x - 2, y + 1)}
    def put(c, moves, sgn=1):
        nb[c] = {(c[0] + sgn * d[0], c[1] + sgn * d[1]) for d in moves}
    for x in range(n):
        for y in range(DB):
            put((x, y), bm[((x - xb) % PB, y)])
        for y in range(DT):
            put((x, n - 1 - y), tm[((xt - x) % PT, y)], -1)
    for y in range(n):
        for x in range(DL):
            put((x, y), lm[(x, (y - yl) % QL)])
        for x in range(DR):
            put((n - 1 - x, y), rm[(x, (yr - y) % QR)], -1)
    free = set()
    for (cx, cy) in [(0, 0), (n - Z, 0), (0, n - Z), (n - Z, n - Z)]:
        for x in range(cx, cx + Z):
            for y in range(cy, cy + Z):
                free.add((x, y))
    return nb, free

MOV8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def fixed_paths(n, nb, free):
    """Contract the fixed part: list of (u, v, cells) for each fixed path that leaves free cell u
    and re-enters the free set at v (u may equal v).  Also returns the cells on closed fixed cycles."""
    seen = set(); paths = []
    for c in sorted(nb):
        if c in free or c in seen: continue
        ends = [v for v in nb[c] if v in free]
        if not ends: continue
        prev, cur, cells = ends[0], c, []
        while True:
            seen.add(cur); cells.append(cur)
            nx = [v for v in nb[cur] if v != prev]
            nxt = nx[0] if nx else prev
            prev, cur = cur, nxt
            if cur in free: break
        paths.append((ends[0], cur, cells))
    closed = [c for c in nb if c not in free and c not in seen]
    return paths, closed

def complete(n, nb, free, time_limit=60, workers=3, verbose=False, hint=True, turn_weight=0,
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
    paths, closed = fixed_paths(n, nb, free)
    if closed: return None, f'fixed part has closed cycles ({len(closed)} cells, e.g. {closed[0]})'
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
    node = {c: i for i, c in enumerate(sorted(free))}
    N = len(node)
    arcs = []
    xv = []
    for (a, b) in var:
        f, r = m.NewBoolVar(''), m.NewBoolVar('')
        arcs += [(node[a], node[b], f), (node[b], node[a], r)]
        x = m.NewBoolVar(''); m.Add(x == f + r); xv.append(x)
    for k, (u, v, cells) in enumerate(paths):
        d = N + k
        l1, l2, l3, l4 = [m.NewBoolVar('') for _ in range(4)]
        arcs += [(node[u], d, l1), (d, node[v], l2), (node[v], d, l3), (d, node[u], l4)]
        m.Add(l1 + l3 == 1); m.Add(l1 == l2); m.Add(l3 == l4)
    m.AddCircuit(arcs)
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

def to_grid(n, full):
    """convert to board.js grid (i = n-1-y, j = x) of move codes for core.validate etc."""
    code = {(MJ[k], -MI[k]): k for k in range(8)}
    g = [[None] * n for _ in range(n)]
    for (x, y), s in full.items():
        ds = sorted(code[(v[0] - x, v[1] - y)] for v in s)
        g[n - 1 - y][x] = ''.join(map(str, ds))
    return g

def lns(n, full, region, win=8, step=4, time_limit=20, workers=3, rounds=2, turn_weight=0,
        crossing_weight=1000, log=None):
    """Large-neighbourhood improvement of a complete tour `full` (cell -> set of 2 neighbours):
    slide a win x win window over the bounding boxes of `region` cells; in each window that holds
    region cells, re-solve those cells with complete() (hint = current tour, so never worse)."""
    from kt.core import crossing_list
    full = {c: set(v) for c, v in full.items()}
    xs = [c[0] for c in region]; ys = [c[1] for c in region]
    region = set(region)
    for rnd in range(rounds):
        changed = 0
        for x0 in range(min(xs), max(xs) + 1, step):
            for y0 in range(min(ys), max(ys) + 1, step):
                W = {(x, y) for x in range(x0, x0 + win) for y in range(y0, y0 + win)} & region
                if len(W) < 4: continue
                new, info = complete(n, full, W, time_limit=time_limit, workers=workers, hint=full,
                                     turn_weight=turn_weight, crossing_weight=crossing_weight)
                if new is None: continue
                if any(new[c] != full[c] for c in W):
                    changed += 1
                full = new
        if log: log(f'lns round {rnd}: {changed} windows changed')
        if not changed: break
    return full
