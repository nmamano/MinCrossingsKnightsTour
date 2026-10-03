"""Whole-arch-region test (KT Structures, 2026-10-03).

Fold field of w-structures/fold3.py (cheap U-turns everywhere, no arch flips). Free every cell of a window
around the left-edge midpoint arch. Outside cells keep their base edges; base edges that cross the window
boundary are forced. CP-SAT minimises the crossings that involve a window edge, with lazy cuts so that every
component that touches the window reaches 'root' (an outside path that ends at a defect cell, i.e. a strand
that leaves the arch region). Report: base value (no connectivity), optimum with connectivity, extra.
usage: python archwin.py n [margin] [time_per_solve] [workers]
"""
import sys, time
from collections import defaultdict
sys.path.insert(0, '../../w-structures')
from fold3 import build
from ortools.sat.python import cp_model

KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def orient(p, q, r):
    v = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    return (v > 0) - (v < 0)

def cross(e, f):
    p1, p2 = e; q1, q2 = f
    if len({p1, p2, q1, q2}) < 4: return False
    return orient(p1, p2, q1) * orient(p1, p2, q2) < 0 and orient(q1, q2, p1) * orient(q1, q2, p2) < 0

def setup(n, margin=2, window=None):
    h = n // 2
    E, deg = build(n, ts=(1, 1, 1, 1))
    if window is None:
        window = (0, h + margin, h // 2 - margin, h + h // 2 + margin)
    x0, x1, y0, y1 = window
    W = {(x, y) for x in range(x0, x1) for y in range(y0, y1)}
    adj = defaultdict(list)
    for a, b in E:
        adj[a].append(b); adj[b].append(a)
    forced = [e for e in E if (e[0] in W) != (e[1] in W)]
    fixed_out = [e for e in E if e[0] not in W and e[1] not in W]
    cand = set()
    for p in W:
        for d in KM:
            q = (p[0]+d[0], p[1]+d[1])
            if q in W:
                cand.add(tuple(sorted([p, q])))
    cand = sorted(cand)
    # boundary pairing: from each window cell with a forced edge, walk outside
    bport = {}   # window cell -> list of partner window cells or 'root'
    for e in forced:
        b, o = (e[0], e[1]) if e[0] in W else (e[1], e[0])
        prev, cur = b, o
        while True:
            nxt = [q for q in adj[cur] if q != prev]
            if len(adj[cur]) < 2 or not nxt:
                bport.setdefault(b, []).append('root'); break
            q = nxt[0]
            if q in W:
                bport.setdefault(b, []).append(q); break
            prev, cur = cur, q
    fdeg = defaultdict(int)
    for e in forced:
        for p in e:
            if p in W: fdeg[p] += 1
    return dict(n=n, W=W, E=E, cand=cand, forced=forced, fixed_out=fixed_out, bport=bport, fdeg=fdeg, window=window)

def solve(S, connect=True, tlim=60, workers=2, maxit=400, verbose=True):
    W, cand = S['W'], S['cand']
    m = cp_model.CpModel()
    x = {e: m.NewBoolVar('') for e in cand}
    inc = defaultdict(list)
    for e in cand:
        inc[e[0]].append(x[e]); inc[e[1]].append(x[e])
    for p in W:
        need = 2 - S['fdeg'][p]
        if need < 0: raise ValueError('cell with >2 forced edges')
        m.Add(sum(inc[p]) == need)
    # crossings
    grid = defaultdict(list)
    allfixed = S['forced'] + [e for e in S['fixed_out'] if min(abs(e[0][0]-a[0]) + abs(e[0][1]-a[1]) for a in ((S['window'][0], S['window'][2]),)) >= 0]
    for e in allfixed:
        grid[(e[0][0]//4, e[0][1]//4)].append(e)
    near = lambda e: [f for dx in (-1, 0, 1) for dy in (-1, 0, 1) for f in grid[(e[0][0]//4+dx, e[0][1]//4+dy)]]
    obj = []
    nfix = 0
    for e in cand:
        for f in near(e):
            if cross(e, f):
                obj.append(x[e])
    cgrid = defaultdict(list)
    zpair = {}
    for e in cand:
        cgrid[(e[0][0]//4, e[0][1]//4)].append(e)
    for e in cand:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for f in cgrid[(e[0][0]//4+dx, e[0][1]//4+dy)]:
                    if e < f and cross(e, f):
                        z = m.NewBoolVar('')
                        m.Add(z >= x[e] + x[f] - 1)
                        m.Add(z <= x[e]); m.Add(z <= x[f])
                        zpair[(e, f)] = z
                        obj.append(z)
    # quarter cuts (tile lemma of the 14n/3 proof): edges whose tiles share a quarter cross pairwise
    def quarters(e):
        (ax, ay), (bx, by) = e
        mx2, my2 = ax + bx, ay + by          # twice the midpoint
        res = []
        for i in range(min(ax, bx) - 1, max(ax, bx) + 1):
            for j in range(min(ay, by) - 1, max(ay, by) + 1):
                for qx, qy in ((2, 3), (4, 3), (3, 2), (3, 4)):
                    # centroid (i + qx/6, j + qy/6) in sixths
                    px, py = 6 * i + qx, 6 * j + qy
                    # parallelogram: |s| + |t| <= 1 in coordinates along long and short diagonal
                    ux, uy = bx - ax, by - ay
                    vx, vy = -uy, ux
                    dx, dy = px - 3 * mx2, py - 3 * my2
                    # long diag half-vector u/2, short diag half: unit grid edge, perpendicular-ish
                    sx, sy = (0, 1) if abs(ux) == 2 else (1, 0)
                    # solve d = a*(3u) + b*(3s)  (sixths: half-vectors scaled by 6)
                    det = ux * sy - uy * sx
                    a_ = (dx * sy - dy * sx) / (3 * det)
                    b_ = (ux * dy - uy * dx) / (3 * det)
                    if abs(a_) + abs(b_) < 1 - 1e-9:
                        res.append((i, j, qx, qy))
        return res
    qcov = defaultdict(list)
    for e in cand:
        for t in quarters(e): qcov[t].append(('v', e))
    for e in allfixed:
        for t in quarters(e):
            if t in qcov: qcov[t].append(('f', e))
    zmap = {}
    # rebuild z lookup
    S['_qz'] = 0
    for t, lst in qcov.items():
        vs = [e for k, e in lst if k == 'v']; fs = [e for k, e in lst if k == 'f']
        if len(vs) + len(fs) < 2: continue
        terms = []
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                terms.append(zpair[tuple(sorted([vs[i], vs[j]]))])
        for e in vs:
            for f in fs:
                terms.append(x[e])
        m.Add(sum(terms) >= sum(x[e] for e in vs) + len(fs) - 1)
        S['_qz'] += 1
    # constant: crossings between forced edges themselves (and forced vs fixed_out) touching the window
    const = 0
    fe = S['forced']
    for i, e in enumerate(fe):
        for f in near(e):
            if f in fe and fe.index(f) <= i: continue
            if cross(e, f): const += 1
    m.Minimize(sum(obj))
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = workers
    solver.parameters.max_time_in_seconds = tlim
    it = 0; cuts = 0
    t0 = time.time()
    while True:
        it += 1
        st = solver.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return dict(status=solver.StatusName(st), it=it)
        sel = [e for e in cand if solver.Value(x[e])]
        val = solver.ObjectiveValue() + const
        if not connect:
            return dict(status=solver.StatusName(st), val=val, sel=sel, it=it, bound=solver.BestObjectiveBound() + const)
        # components
        g = defaultdict(list)
        for a, b in sel:
            g[a].append(b); g[b].append(a)
        for b, lst in S['bport'].items():
            for q in lst:
                if q != 'root': g[b].append(q); g[q].append(b)
        seen = set(); bad = []
        for p in W:
            if p in seen: continue
            comp = []; st_ = [p]; seen.add(p); root = False
            while st_:
                u = st_.pop(); comp.append(u)
                if 'root' in S['bport'].get(u, []): root = True
                for v in g[u]:
                    if v not in seen:
                        seen.add(v); st_.append(v)
            if not root: bad.append(set(comp))
        if verbose:
            print(f'  it {it}: {solver.StatusName(st)} val {val} bound {solver.BestObjectiveBound()+const} closed comps {len(bad)} t={time.time()-t0:.0f}s', flush=True)
        if not bad:
            return dict(status=solver.StatusName(st), val=val, sel=sel, it=it, bound=solver.BestObjectiveBound() + const)
        for C in bad:
            cut = [x[e] for e in cand if (e[0] in C) != (e[1] in C)]
            m.Add(sum(cut) >= 1); cuts += 1
        m.ClearHints()
        for e in cand:
            m.AddHint(x[e], solver.Value(x[e]))
        if it >= maxit:
            return dict(status='MAXIT', it=it)

if __name__ == '__main__':
    n = int(sys.argv[1]); margin = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 60; wk = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    S = setup(n, margin)
    print('n', n, 'window', S['window'], 'cells', len(S['W']), 'cand', len(S['cand']), 'forced', len(S['forced']))
    r0 = solve(S, connect=False, tlim=tl, workers=wk)
    print('no-connect:', r0['status'], r0['val'], 'bound', r0['bound'])
    r1 = solve(S, connect=True, tlim=tl, workers=wk)
    print('connect:', r1.get('status'), r1.get('val'), 'bound', r1.get('bound'), 'iters', r1['it'])
    if 'val' in r1:
        print('EXTRA =', r1['val'] - r0['val'])
