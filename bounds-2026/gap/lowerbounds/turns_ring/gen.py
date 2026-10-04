"""Instance generator for regiondp (C++). Corner-window model CW(K, D, f), BL corner, quadrant board:
 region = arms {x<4, y<D} U {y<4, x<D} plus window interior {4<=x<K, 4<=y<K} (free, cost t);
 every other cell with x>=4 and y>=4 is straight in field f (forced); arm cells beyond D enter only through the
 given cut states sL (left arm, steep frame, next row D) and sB (bottom arm, grazing frame, next column D)."""
import sys, subprocess, pickle
from itertools import combinations
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
from strip import M, lower
R = '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/'
EXE = R + 'regiondp'


def rq(p, a, b):
    t = int(a[0] + b[0] != 0 or a[1] + b[1] != 0)
    return t - lower(p[0], [a[0], b[0]]) - lower(p[1], [a[1], b[1]])


def left_edges(s, D):
    out = []
    for (x, yy, dx, dy) in s:
        lo, hi = (x, D + yy), (x + dx, D + yy + dy)
        out.append((hi, lo) if hi[1] >= D else (lo, hi))
    return out


def bottom_edges(s, D):
    out = []
    for (X, YY, dX, dY) in s:
        lo, hi = (D + YY, X), (D + YY + dY, X + dX)
        out.append((hi, lo) if hi[0] >= D else (lo, hi))
    return out


def run_region(order, inregion, forced_dirs, external, cost, bound, rem_bound=None, mode=1):
    """order: cells; forced_dirs(q) -> (d1,d2) moves of a forced straight cell or None if q is not forced;
    external: list of (outside cell, region cell) edges fixed present. cost(p, a, b)."""
    pos = {p: i for i, p in enumerate(order)}
    n = len(order)
    # potential edges: (earlier region cell -> later region cell) and external
    life = []          # (start, end, key)
    for i, p in enumerate(order):
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if q in pos and pos[q] > i: life.append((i, pos[q], (p, q)))
    for o, b in external: life.append((-1, pos[b], (o, b)))
    life.sort()
    free = list(range(128)); busy = []; slot = {}
    import heapq
    for s, e, key in life:
        while busy and busy[0][0] <= s:
            free.append(heapq.heappop(busy)[1])
        if not free: raise RuntimeError('more than 128 live edge slots')
        free.sort(); b = free.pop(0); slot[key] = b; heapq.heappush(busy, (e, b))
    # forced edges into region cells from forced cells
    fint = {}
    for p in order:
        fl = []
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            fd = forced_dirs(q)
            if fd is not None and (-d[0], -d[1]) in fd: fl.append(d)
        fint[p] = fl
    ext_in = {}
    for o, b in external: ext_in.setdefault(b, []).append(o)
    lines = []
    init = 0
    for o, b in external: init |= 1 << slot[(o, b)]
    cells = []
    for i, p in enumerate(order):
        inmask = 0
        earlier = {}
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if q in pos and pos[q] < i: earlier[d] = slot[(q, p)]; inmask |= 1 << slot[(q, p)]
        for o in ext_in.get(p, []):
            d = (o[0] - p[0], o[1] - p[1]); earlier[d] = slot[(o, p)]; inmask |= 1 << slot[(o, p)]
        opts = []
        allowed = [d for d in M if (p[0] + d[0], p[1] + d[1]) in pos or d in earlier or d in fint[p]]
        for a, b in combinations(allowed, 2):
            if not all(d in (a, b) for d in fint[p]): continue
            req = 0; add = 0; ok = True
            for d in (a, b):
                q = (p[0] + d[0], p[1] + d[1])
                if d in fint[p]: continue
                if d in earlier: req |= 1 << earlier[d]
                elif q in pos and pos[q] > i: add |= 1 << slot[(p, q)]
                else: ok = False
            if ok: opts.append((req, add, cost(p, a, b)))
        cells.append((inmask, opts))
    if rem_bound is None:
        rem = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            rem[i] = rem[i + 1] + min([0] + [c for r_, a_, c in cells[i][1]])
    else: rem = rem_bound
    out = [f'128 {n} {init >> 64} {init & (2**64 - 1)} {bound}']
    for (inmask, opts), r in zip(cells, rem):
        out.append(f'{inmask >> 64} {inmask & (2**64 - 1)} {r} {len(opts)}')
        for req, add, c in opts: out.append(f'{req >> 64} {req & (2**64 - 1)} {add >> 64} {add & (2**64 - 1)} {c}')
    out.append(str(mode))
    res = subprocess.run([EXE, str(mode)], input='\n'.join(out), capture_output=True, text=True)
    peak = [l for l in res.stderr.splitlines() if l.startswith('peak')]
    return res.stdout.strip(), peak[0] if peak else res.stderr[-300:]


def corner_window(f, K, D, sL, sB, bound=7):
    fm = (f, (-f[0], -f[1]))
    inregion = lambda q: q[0] >= 0 and q[1] >= 0 and ((q[0] < 4 and q[1] < D) or (q[1] < 4 and q[0] < D) or (q[0] < K and q[1] < K))
    forced = lambda q: fm if (q[0] >= 4 and q[1] >= 4 and not (q[0] < K and q[1] < K)) else None
    order = []
    for y in range(D - 1, -1, -1):
        w = 4 if y >= K else (K if y >= 4 else K)
        order += [(x, y) for x in range(w)]
    order += [(x, y) for x in range(K, D) for y in range(4)]
    assert all(inregion(p) for p in order) and len(set(order)) == len(order)
    ext = left_edges(sL, D) + bottom_edges(sB, D)
    return run_region(order, inregion, forced, ext, rq, bound)


if __name__ == '__main__':
    f = (int(sys.argv[1]), int(sys.argv[2])); K = int(sys.argv[3]); D = int(sys.argv[4])
    sst, sarc, szc = pickle.load(open(R + f'fstrip_{f[0]}_{f[1]}.pkl', 'rb'))
    g = (f[1], f[0]) if f[1] > 0 else (-f[1], -f[0])
    gst, garc, gzc = pickle.load(open(R + f'fstrip_{g[0]}_{g[1]}.pkl', 'rb'))
    SL = sorted(set().union(*[c for c, gg in szc])); SB = sorted(set().union(*[c for c, gg in gzc]))
    tab = {}
    for a in SL:
        for b in SB:
            r, peak = corner_window(f, K, D, sst[a], gst[b])
            tab[(a, b)] = None if r == 'NONE' else int(r)
            print('field', f, 'K', K, 'D', D, 'left', a, 'bottom', b, '->', tab[(a, b)], peak, flush=True)
    pickle.dump(tab, open(R + f'cw_{f[0]}_{f[1]}_K{K}_D{D}.pkl', 'wb'))


def corner_window_sat(f, K, D, sL, sB, workers=2, tlimit=300):
    """Same model as corner_window, solved exactly with CP-SAT. Returns (status, value, chosen moves dict)."""
    from ortools.sat.python import cp_model
    fm = (f, (-f[0], -f[1]))
    inregion = lambda q: q[0] >= 0 and q[1] >= 0 and ((q[0] < 4 and q[1] < D) or (q[1] < 4 and q[0] < D) or (q[0] < K and q[1] < K))
    forced = lambda q: (q[0] >= 4 and q[1] >= 4 and not (q[0] < K and q[1] < K))
    cells = [(x, y) for x in range(D) for y in range(D) if inregion((x, y))]
    ext = {}
    for o, b in left_edges(sL, D) + bottom_edges(sB, D): ext.setdefault(b, set()).add((o[0] - b[0], o[1] - b[1]))
    m = cp_model.CpModel(); X = {}; cost = []
    for p in cells:
        fint = {d for d in M if forced((p[0] + d[0], p[1] + d[1])) and (-d[0], -d[1]) in fm}
        must = fint | ext.get(p, set())
        allowed = [d for d in M if inregion((p[0] + d[0], p[1] + d[1])) or d in must]
        opts = []
        for a, b in combinations(allowed, 2):
            if not must <= {a, b}: continue
            v = m.NewBoolVar(''); X[p, a, b] = v; opts.append(v); cost.append(rq(p, a, b) * v)
        if not opts: return ('INFEASIBLE', None, None)
        m.AddExactlyOne(opts)
    for p in cells:
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if q in set(cells) and p < q:
                lhs = [v for (pp, a, b), v in X.items() if pp == p and d in (a, b)]
                rhs = [v for (pp, a, b), v in X.items() if pp == q and (-d[0], -d[1]) in (a, b)]
                m.Add(sum(lhs) == sum(rhs))
    m.Minimize(sum(cost))
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tlimit
    st = s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return (s.StatusName(st), None, None)
    ch = {p: (a, b) for (p, a, b), v in X.items() if s.Value(v)}
    return (s.StatusName(st), int(round(s.ObjectiveValue())), ch)
