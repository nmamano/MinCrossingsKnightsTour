"""Class-selective edge phase test (KT Structures, 2026-10-03).

Left edge strip x in [0, D), periodic in y with period p rows (cylinder). Cells x >= D carry pure (2,1) lines
(line index c = x - 2y). Pattern P pairs line c with c - 3 for even c. Residue class of a line = c mod 3.
Target: P for every line, except the lines of the classes in SHIFT, which pair even c with c + 3 (the other
phase of their class chain). Question: minimum crossings per period (P alone = p).
Needed for layout G (gentle-seam corners trap one or two residue classes, w-structures S10).
usage: python classphase.py p D shiftclasses(e.g. 0 or 01 or -) [time] [workers]
"""
import sys, itertools
from collections import defaultdict
from ortools.sat.python import cp_model

KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def orient(p, q, r):
    v = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    return (v > 0) - (v < 0)

def cross(e, f):
    p1, p2 = e; q1, q2 = f
    if len({p1, p2, q1, q2}) < 4: return False
    return orient(p1, p2, q1)*orient(p1, p2, q2) < 0 and orient(q1, q2, p1)*orient(q1, q2, p2) < 0

def run(p, D, shift, tlim=120, workers=2, verbose=True, partner_fn=None):
    assert p % 3 == 0
    cells = [(x, y) for x in range(D) for y in range(p)]
    # candidate strip edges, representative: lower endpoint in [0,p) rows (ties: smaller x)
    cand = []
    for (x, y) in cells:
        for dx, dy in KM:
            q = (x+dx, y+dy)
            if not (0 <= q[0] < D): continue
            if dy < 0 or (dy == 0 and dx < 0): continue
            cand.append(((x, y), q))
    # fixed edges in the cover near the strip: pure lines for x >= D (cells (x,y) -> (x+2,y+1)), all y
    def fixed_edges(ylo, yhi):
        out = []
        for x in range(D - 2, D + 4):
            for y in range(ylo, yhi):
                a, b = (x, y), (x+2, y+1)
                if b[0] >= D:   # edge with at least one endpoint outside the strip: fixed (forced if a in strip)
                    out.append((a, b))
        return out
    lineof = lambda c: c
    def partner(c):
        if partner_fn is not None:
            return partner_fn(c)
        if 'F' in shift:   # full flip: even c -> c + 5
            return c + 5 if c % 2 == 0 else c - 5
        r = c % 3
        if c % 2 == 0:
            return c + 3 if r in shift else c - 3
        else:
            return c - 3 if (c - 3) % 3 in shift else c + 3
    # sanity: partner is an involution
    for c in range(-30, 30):
        assert partner(partner(c)) == c, c
    pid = lambda c: min(c, partner(c)) % (2*p)
    # entries: strip cells (D-2,y),(D-1,y) receive forced edge from (x+2,y+1)
    fdeg = defaultdict(int); entry_label = {}
    entry_line = {}
    for y in range(p):
        for x in (D-2, D-1):
            fdeg[(x, y)] += 1
            c = x - 2*y
            entry_label[(x, y)] = pid(c); entry_line[(x, y)] = c
    m = cp_model.CpModel()
    X = {e: m.NewBoolVar('') for e in cand}
    wrap = lambda q: (q[0], q[1] % p)
    inc = defaultdict(list)
    for e in cand:
        inc[wrap(e[0])].append(X[e]); inc[wrap(e[1])].append(X[e])
    for c in cells:
        m.Add(sum(inc[c]) == 2 - fdeg[c])
    lab = {c: m.NewIntVar(0, 2*p - 1, '') for c in cells}
    for c, l in entry_label.items():
        m.Add(lab[c] == l)
    for e in cand:
        m.Add(lab[wrap(e[0])] == lab[wrap(e[1])]).OnlyEnforceIf(X[e])
    # crossings per period: e at period 0 vs every translate of every other edge
    obj = []
    fx = fixed_edges(-6, p + 6)
    tr = lambda e, t: ((e[0][0], e[0][1]+t), (e[1][0], e[1][1]+t))
    zs = {}
    for i, e in enumerate(cand):
        for j, f in enumerate(cand):
            for k in range(-2, 3):
                g = tr(f, k*p)
                if k == 0 and j <= i: continue
                if k < 0: continue
                if cross(e, g):
                    key = (i, j, k)
                    z = m.NewBoolVar('')
                    m.Add(z >= X[e] + X[f] - 1)
                    obj.append(z)
    # strip-fixed: each fixed edge orbit counted once: fixed edges with lower endpoint row in [0,p)
    fx0 = [f for f in fixed_edges(0, p)]
    for e in cand:
        for f in fx0:
            for k in range(-2, 3):
                if cross(e, tr(f, k*p)):
                    obj.append(X[e])
    # fixed-fixed crossings (constant): forced edges vs pure lines do not cross; ignore
    m.Minimize(sum(obj))
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = workers
    solver.parameters.max_time_in_seconds = tlim
    it = 0
    while True:
        it += 1
        st = solver.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return dict(status=solver.StatusName(st), it=it)
        sel = [e for e in cand if solver.Value(X[e])]
        # trace in the cover over 5 periods
        adj = defaultdict(list)
        for k in range(-3, 4):
            for e in sel:
                a, b = tr(e, k*p)
                adj[a].append(b); adj[b].append(a)
        bad = []
        # strands from entries in period 0: must end at entry of partner line (same cover copy)
        seen = set()
        for (x, y) in entry_line:
            c = x - 2*y
            prev, cur = None, (x, y)
            path = [cur]
            while True:
                nx = [q for q in adj[cur] if q != prev]
                if (len(adj[cur]) == 1 and prev is not None) or not nx:   # reached an entry (one strip edge)
                    break
                prev, cur = cur, nx[0]
                path.append(cur)
                if len(path) > 10*p*D: break
            end = cur
            if end[0] in (D-2, D-1) and len(path) > 1:
                ce = end[0] - 2*end[1]
                if ce != partner(c):
                    bad.append(path)
            elif len(path) > 1 or len(adj[(x, y)]) != 1:
                bad.append(path)
        # closed loops in period 0 copy
        incyc = set()
        for k in (0,):
            visited = set()
            for c0 in cells:
                if c0 in visited: continue
                comp = []; stck = [c0]; visited.add(c0); hasentry = False
                while stck:
                    u = stck.pop(); comp.append(u)
                    if u in entry_line: hasentry = True
                    for v in adj[u]:
                        w = wrap(v)
                        if w not in visited and 0 <= w[0] < D:
                            visited.add(w); stck.append(w)
                if not hasentry:
                    bad.append(comp)
        if verbose:
            print(f'  it {it}: {solver.StatusName(st)} obj {solver.ObjectiveValue()} bound {solver.BestObjectiveBound()} bad {len(bad)}', flush=True)
        if not bad:
            return dict(status=solver.StatusName(st), val=solver.ObjectiveValue(), bound=solver.BestObjectiveBound(), sel=sel, it=it)
        for path in bad:
            es = set()
            for a, b in zip(path, path[1:]):
                for e in cand:
                    for k in range(-3, 4):
                        g = tr(e, k*p)
                        if {g[0], g[1]} == {a, b}:
                            es.add(e)
            if es:
                m.AddBoolOr([X[e].Not() for e in es])
        if it > 300:
            return dict(status='MAXIT', it=it)

if __name__ == '__main__':
    p, D = int(sys.argv[1]), int(sys.argv[2])
    shift = set() if sys.argv[3] == '-' else {(ch if ch == 'F' else int(ch)) for ch in sys.argv[3]}
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 120
    wk = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    r = run(p, D, shift, tl, wk)
    print('p', p, 'D', D, 'shift', sorted(map(str, shift)), r.get('status'), 'val', r.get('val'), 'bound', r.get('bound'),
          'per row', (r['val'] / p) if 'val' in r else None)
    if 'sel' in r:
        print(sorted(r['sel']))
