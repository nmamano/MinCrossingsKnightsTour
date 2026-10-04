# KT Structures, 2026-10-04. Window repair: free the cells of given rectangles, fix every other cell, minimise turns in
# the free cells, add lazy subtour cuts until the whole grid is one cycle. CP-SAT, 2 workers.
# usage: repair.py in.json out.json time_s i0,j0,h,w [i0,j0,h,w ...]
import sys, json, time
from itertools import combinations
from pathlib import Path
from ortools.sat.python import cp_model
from tmin import MI, MJ, components
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from kt.core import validate, num_turns

def solve(g, W, cuts, tl):
    n = len(g); m = cp_model.CpModel(); on = lambda i, j: 0 <= i < n and 0 <= j < n
    E = {}; P = {}; obj = []
    def ev(c, k):
        i, j = c; a, b = i + MI[k], j + MJ[k]
        if (a, b) not in W:  # neighbour fixed: edge is a constant
            return int(str((k + 4) % 8) in g[a][b])
        key = (c, k) if c < (a, b) else ((a, b), (k + 4) % 8)
        if key not in E: E[key] = m.NewBoolVar('')
        return E[key]
    for c in W:
        i, j = c; ks = [k for k in range(8) if on(i + MI[k], j + MJ[k])]
        vs = {p: m.NewBoolVar('') for p in combinations(ks, 2)}; P[c] = vs
        m.AddExactlyOne(vs.values())
        for k in ks:
            m.Add(ev(c, k) == sum(v for p, v in vs.items() if k in p))
        obj += [v for p, v in vs.items() if p[1] - p[0] != 4]
    for S in cuts:
        terms = []
        for c in W:
            if c not in S: continue
            for k in range(8):
                q = (c[0] + MI[k], c[1] + MJ[k])
                if on(*q) and q not in S:
                    e = ev(c, k)
                    if not isinstance(e, int): terms.append(e)
        for c in S:  # fixed cell in S with a variable edge to a window cell outside S
            if c in W: continue
            for k in range(8):
                q = (c[0] + MI[k], c[1] + MJ[k])
                if q in W and q not in S:
                    e = ev(q, (k + 4) % 8)
                    if not isinstance(e, int): terms.append(e)
        m.Add(sum(terms) >= 2)
    m.Minimize(sum(obj))
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tl
    s.parameters.cp_model_presolve = False
    st = s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return None, s.StatusName(st)
    h = [row[:] for row in g]
    for c, vs in P.items():
        for p, v in vs.items():
            if s.Value(v): h[c[0]][c[1]] = '%d%d' % p
    return h, s.StatusName(st)

def main():
    src, out, tl = sys.argv[1], sys.argv[2], float(sys.argv[3])
    g = json.loads(Path(src).read_text())['grid']; n = len(g); T0 = num_turns(g)
    W = set()
    for r in sys.argv[4:]:
        i0, j0, hh, ww = map(int, r.split(','))
        W |= {(i, j) for i in range(i0, i0 + hh) for j in range(j0, j0 + ww)}
    cuts = []; t0 = time.time(); h = g
    while True:
        left = tl - (time.time() - t0)
        if left < 2: print('time out'); return
        h2, st = solve(g, W, cuts, left)
        if h2 is None: print('no solution', st); return
        comps = components(h2, n)
        print(f'{st} T-8n={num_turns(h2) - 8 * n} cycles={len(comps)} t={time.time() - t0:.0f}s', flush=True)
        if len(comps) == 1: h = h2; break
        cuts += [set(C) for C in comps]
    assert validate(h)
    T = num_turns(h)
    Path(out).write_text(json.dumps(dict(n=n, T=T, T_minus_8n=T - 8 * n, src=src, windows=sys.argv[4:], status=st,
                                         date='2026-10-04', grid=h)))
    print(f'RESULT {src} n={n} 2f {T0 - 8 * n} -> tour {T - 8 * n} ({st} inside the windows)')

if __name__ == '__main__':
    main()
