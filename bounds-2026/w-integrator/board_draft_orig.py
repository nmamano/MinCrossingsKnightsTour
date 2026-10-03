"""Assemble a full n x n tour from periodic edge gadgets + CP-SAT corner completion.

Board coords (x, y): x column (right), y row (up), 0..n-1.  Interior: lines x+2y=c ('26').
bottom_tpl: rows top-first (like Sequence1), period P_B = width, depth D_B = #rows, local off 0.
left_tpl  : rows top-first, columns x=0..D_L-1, period Q = #rows, local lane offset off_L.
Lane-pair alignment (see notes): bottom/right pairs start at c = off_L (mod 8); left/top at off_L+4.
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
    bm, PB, DB = tpl_moves(bottom_tpl)
    lm, DL, Q = tpl_moves(left_tpl)
    on = lambda c: 0 <= c[0] < n and 0 <= c[1] < n
    nb = {}
    for x in range(n):
        for y in range(n):
            nb[(x, y)] = {(x + 2, y - 1), (x - 2, y + 1)}
    beta = off_L % 8
    x0 = (beta + bx) % PB                         # bottom: pairs start at c = x0 (mod 8)
    X0 = (beta + 13 - 2 * n) % 8                  # top
    y0 = 2 % 4                                    # left
    Y0 = (off_L - n // 2) % 4                     # right
    def put(c, moves):
        nb[c] = {(c[0] + d[0], c[1] + d[1]) for d in moves}
    for x in range(n):
        for y in range(DB):
            put((x, y), bm[((x - x0) % PB, y)])                         # bottom
            xl = (X0 - x) % PB                                           # top: (x,y)=(X0-xl, n-1-yl)
            put((x, n - 1 - y), [(-d[0], -d[1]) for d in bm[(xl, y)]])
    for y in range(n):
        for x in range(DL):
            put((x, y), lm[(x, (y - y0 - 4 * ly) % Q)])                  # left
            yl = (Y0 - y) % Q                                            # right: (x,y)=(n-1-xl, Y0-yl)
            put((n - 1 - x, y), [(-d[0], -d[1]) for d in lm[(x, yl)]])
    free = set()
    for (cx, cy) in [(0, 0), (n - Z, 0), (0, n - Z), (n - Z, n - Z)]:
        for x in range(cx, cx + Z):
            for y in range(cy, cy + Z):
                free.add((x, y))
    return nb, free

MOV8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def complete(n, nb, free, time_limit=60, workers=4, max_rounds=60, verbose=False):
    on = lambda c: 0 <= c[0] < n and 0 <= c[1] < n
    # consistency of fixed part
    for c, s in nb.items():
        if c in free: continue
        for v in s:
            if not on(v): return None, f'fixed cell {c} points off board to {v}'
            if v not in free and c not in nb[v]: return None, f'fixed asym {c}->{v}'
    forced = defaultdict(set)
    for c, s in nb.items():
        if c in free: continue
        for v in s:
            if v in free: forced[v].add(c)
    var = []
    for c in sorted(free):
        for d in MOV8:
            v = (c[0] + d[0], c[1] + d[1])
            if v in free and c < v: var.append((c, v))
    m = cp_model.CpModel()
    xv = [m.NewBoolVar('') for _ in var]
    inc = defaultdict(list)
    for i, (a, b) in enumerate(var):
        inc[a].append(i); inc[b].append(i)
    for c in free:
        k = 2 - len(forced[c])
        if k < 0: return None, f'overforced {c}'
        m.Add(sum(xv[i] for i in inc[c]) == k)
    # crossings: var-var and var-fixed (fixed edges near zones)
    fixed_near = set()
    for c in free:
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
    for i, e in enumerate(var):
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                for kind, j, f in by.get((e[0][0] + dx, e[0][1] + dy), ()):
                    if kind == 'v' and j <= i: continue
                    if seg_cross(e[0], e[1], f[0], f[1]):
                        if kind == 'f': terms.append(xv[i])
                        else:
                            z = m.NewBoolVar(''); m.AddBoolOr([xv[i].Not(), xv[j].Not(), z]); terms.append(z)
    m.Minimize(sum(terms))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = workers
    for rnd in range(max_rounds):
        r = s.Solve(m)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None, f'completion infeasible ({s.StatusName(r)}) round {rnd}'
        full = {c: set(v) for c, v in nb.items()}
        for c in free: full[c] = set(forced[c])
        for i, (a, b) in enumerate(var):
            if s.Value(xv[i]): full[a].add(b); full[b].add(a)
        # components
        seen, comps = set(), []
        for c in full:
            if c in seen: continue
            comp, st = [], [c]; seen.add(c)
            while st:
                u = st.pop(); comp.append(u)
                for w in full[u]:
                    if w not in seen: seen.add(w); st.append(w)
            comps.append(comp)
        if verbose: print('round', rnd, 'components', len(comps), 'obj', s.ObjectiveValue())
        if len(comps) == 1:
            return full, dict(rounds=rnd, corner_obj=s.ObjectiveValue(), status=s.StatusName(r))
        idx = {e: i for i, e in enumerate(var)}
        for comp in comps:
            cs = set(comp)
            used = [idx[(a, b)] for a in comp for b in full[a] if a < b and (a, b) in idx]
            if not used:
                return None, f'fixed part has a closed cycle of size {len(comp)} (e.g. {comp[0]})'
            m.Add(sum(xv[i] for i in used) <= len(used) - 1)
    return None, 'too many rounds'

def to_grid(n, full):
    """convert to board.js grid (i = n-1-y, j = x) of move codes for core.validate etc."""
    code = {(MJ[k], -MI[k]): k for k in range(8)}
    g = [[None] * n for _ in range(n)]
    for (x, y), s in full.items():
        ds = sorted(code[(v[0] - x, v[1] - y)] for v in s)
        g[n - 1 - y][x] = ''.join(map(str, ds))
    return g
