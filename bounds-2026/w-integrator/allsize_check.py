#!/usr/bin/env python3
"""All-size check for a corner set from allpipe.py (KT Integrator, 2026-10-04). Python standard library only.

Generalises the TT16 part of w-turnstheory/check_upper_proofs.py (audited, Claims 6, 7, 16) to any side
gadgets, phases, corner shapes and period. For each residue file pipeline/<tag>/res<r>.json:
 (1) direct checks: for every even n >= nmin in the class mod p, up to the induction base N + s, the tour
     (skeleton + anchored corner zones; or tours/<tag>_n<n>.json where the pipeline solved n directly) is one
     closed knight's tour; its turn count T(n) is recorded.
 (2) induction (s = lcm(p, w), w = line period of the bands, base N in [Nmin, Nmin + s) per class mod s):
     the three diagonal gaps between the corner zones (lines x + 2y between BL/BR, BR/TL, TL/TR) each get
     one cut slab of width w at least 6 lines away from every zone. Checks, as in the audited TT16 proof:
     slab matching M has M^(1 + s/w) = M; the slab at n + s (shifted by k*s in gap k) has the same ports and
     matching; the long slab of width w + s at n + s equals M. So the tour at n + s is the tour at n with
     s lines inserted in each gap, and it is again one closed tour.
 (3) cost: T(N + s) - T(N) = sum over the 4 bands of (s / period) * (band turns per period) (exact local
     band count, band_cost), so T(n) = T(N) + (n - N) * dT / s for every n = N mod s, n >= N.
Usage: allsize_check.py w-integrator/pipeline/<tag> [--nmin 48] [--Nmin 96]
"""
import argparse, json, sys
from math import gcd
from pathlib import Path

DIRS = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
def lcm(a, b): return a * b // gcd(a, b)

def template(rows):
    rows = [r.split() for r in rows]
    return {(x, len(rows)-1-r): tuple(DIRS[int(k)] for k in s)
            for r, row in enumerate(rows) for x, s in enumerate(row)}, len(rows[0]), len(rows)

def anchor(k, n): return ((n if k[1] == 'R' else 0), (n if k[0] == 'T' else 0))

def zone_cells(d, n):
    out = {}
    for name, ds in d['zones'].items():
        k, uv = name.split(':'); u, v = map(int, uv.split(',')); a, b = anchor(k, n)
        out[(a + u, b + v)] = (k, tuple(map(tuple, ds)))
    return out

def graph(d, n):
    B, P, D = template(d['bottom']); T, PT, DT = template(d['top'])
    L, W, Q = template(d['left']); R, WR, QR = template(d['right'])
    xb, xt, yl, yr = d['phases']
    g = {}
    for x in range(n):
        for y in range(n):
            ds = ((2,-1),(-2,1))
            if y < D: ds = B[((x-xb) % P, y)]
            if y >= n-DT: ds = tuple((-a,-b) for a,b in T[((xt-x) % PT, n-1-y)])
            if x < W: ds = L[(x, (y-yl) % Q)]
            if x >= n-WR: ds = tuple((-a,-b) for a,b in R[(n-1-x, (yr-y) % QR)])
            g[x, y] = tuple((x+a, y+b) for a,b in ds)
    for (x, y), (k, ds) in zone_cells(d, n).items():
        assert 0 <= x < n and 0 <= y < n, ('zone cell off board', n, k, x, y)
        g[x, y] = tuple((x+dx, y+dy) for dx, dy in ds)
    return g

def validate(g):
    for u, vs in g.items():
        assert len(set(vs)) == 2
        for v in vs:
            assert v in g and u in g[v], (u, v)
            assert sorted(map(abs, (v[0]-u[0], v[1]-u[1]))) == [1, 2]
    start = next(iter(g)); prev = None; u = start; seen = set()
    while u not in seen:
        seen.add(u); v = next(v for v in g[u] if v != prev); prev, u = u, v
    assert u == start and len(seen) == len(g), (len(seen), len(g))

def turns(g):
    return sum(v[0]+w[0] != 2*u[0] or v[1]+w[1] != 2*u[1] for u, (v, w) in g.items())

def tour_grid(rows):
    n = len(rows); g = {}
    for r, row in enumerate(rows):
        for x, code in enumerate(row):
            u = (x, n-1-r)
            g[u] = tuple((u[0]+DIRS[int(k)][0], u[1]+DIRS[int(k)][1]) for k in code)
    return g

def line(v): return v[0] + 2*v[1]

class Ports:
    def __init__(self, dep): self.dep = dep
    def port(self, u, v, a, n):
        if line(u) > line(v): u, v = v, u
        DB, DT, WL, WR = self.dep
        sides = []
        if max(u[1], v[1]) < DB: sides.append(('B', u[1], v[1]))
        if min(u[1], v[1]) >= n-DT: sides.append(('T', n-1-u[1], n-1-v[1]))
        if max(u[0], v[0]) < WL: sides.append(('L', u[0], v[0]))
        if min(u[0], v[0]) >= n-WR: sides.append(('R', n-1-u[0], n-1-v[0]))
        assert len(sides) == 1, (u, v, sides)
        return sides[0] + (line(u)-a, line(v)-a)

    def slab(self, g, n, a, width):
        vertices = {u for u in g if a <= line(u) < a+width}
        ports = {}; names = [set(), set()]
        for u in vertices:
            for v in g[u]:
                if v not in vertices:
                    side = int(line(v) >= a+width)
                    key = self.port(u, v, a+side*width, n)
                    assert (side, key) not in ports
                    ports[side, key] = (u, v); names[side].add(key)
        assert names[0] == names[1]
        keys = sorted(names[0]); seen = set(); matching = {}
        for (side, key), (u, prev) in ports.items():
            begin = (side, keys.index(key))
            if begin in matching: continue
            while u in vertices:
                assert u not in seen, ('closed component', n, a, u)
                seen.add(u); nxt = next(v for v in g[u] if v != prev); prev, u = u, nxt
            endside = int(line(u) >= a+width)
            end = (endside, keys.index(self.port(prev, u, a+endside*width, n)))
            assert end != begin
            matching[begin] = end; matching[end] = begin
        assert seen == vertices, ('uncovered cycle', n, a, len(vertices-seen))
        return keys, matching

def compose(A, B):
    adj = {}
    for matching, offset in ((A, 0), (B, 1)):
        for (s, i), (t, j) in matching.items():
            adj.setdefault((s+offset, i), []).append((t+offset, j))
    seen = set(); out = {}
    for u in adj:
        if u[0] == 1 or u in seen: continue
        prev = None; v = u
        while True:
            seen.add(v)
            nxt = [w for w in adj[v] if w != prev]
            assert len(nxt) == 1
            prev, v = v, nxt[0]
            if v[0] != 1: break
            assert v not in seen
        seen.add(v)
        a = (u[0]//2, u[1]); b = (v[0]//2, v[1]); out[a] = b; out[b] = a
    assert seen == set(adj), 'closed cycle on gluing'
    return out

def power(M, k):
    out = M
    for _ in range(k-1): out = compose(out, M)
    return out

def band_turns(rows, kind):
    """Turns per period of one infinite band (kind 'B': along x; 'L': along y)."""
    mv, W, H = template(rows); P, D = (W, H) if kind == 'B' else (H, W)
    xy = lambda s, d: (s, d) if kind == 'B' else (d, s)
    g = {}
    for s in range(-8, P+9):
        for dep in range(D+6):
            u = xy(s, dep)
            ds = mv[xy(s % P, dep)] if dep < D else ((2,-1),(-2,1))
            g[u] = tuple((u[0]+dx, u[1]+dy) for dx, dy in ds)
    for u in g:
        s, dep = (u if kind == 'B' else (u[1], u[0]))
        if 0 <= s < P and dep < D+3:
            for v in g[u]: assert v in g and u in g[v], ('band not consistent', kind, u, v)
    T = sum(1 for u, (v, w) in g.items() if 0 <= (u if kind == 'B' else (u[1], u[0]))[0] < P
            and (u if kind == 'B' else (u[1], u[0]))[1] < D and (v[0]+w[0], v[1]+w[1]) != (2*u[0], 2*u[1]))
    return P, T

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--nmin', type=int, default=48)
    ap.add_argument('--Nmin', type=int, default=96)
    a = ap.parse_args(); D = Path(a.dir)
    files = sorted(D.glob('res*.json')); assert files, 'no residue files'
    ds = [json.loads(f.read_text()) for f in files]
    d0 = ds[0]; p = d0['period']; tag = d0['tag']
    for d in ds:
        assert d['format'] == 'anchored-v2' and d['period'] == p
        assert [d[k] for k in ('bottom', 'top', 'left', 'right', 'phases')] == [d0[k] for k in ('bottom', 'top', 'left', 'right', 'phases')]
    assert sorted(d['residue'] for d in ds) == list(range(0, p, 2)), 'need one file per even residue mod p'
    for d in ds: assert d['n0'] % p == d['residue']
    _, PB, DB = template(d0['bottom']); _, PT, DT = template(d0['top'])
    _, WL, QL = template(d0['left']); _, WR, QR = template(d0['right'])
    w = lcm(lcm(PB, PT), lcm(2*QL, 2*QR)); s = lcm(p, w)
    P = Ports((DB, DT, WL, WR))
    bc = {'bottom': band_turns(d0['bottom'], 'B'), 'top': band_turns(d0['top'], 'B'),
          'left': band_turns(d0['left'], 'L'), 'right': band_turns(d0['right'], 'L')}
    dT = sum(s // per * t for per, t in bc.values())
    report = dict(tag=tag, period=p, line_period=w, step=s, band_turns=bc, dT_per_step=dT, direct=[], transfers=[])
    print(f'{tag}: period p={p}, line period w={w}, step s={s}, band turns per period {bc}, dT per +{s} = {dT}', flush=True)
    byres = {d['residue']: d for d in ds}
    const = {}
    for c in range(0, s, 2):
        d = byres[c % p]
        N = next(n for n in range(a.Nmin, a.Nmin + s, 2) if n % s == c)
        tvals = {}
        for n in range(a.nmin + ((c - a.nmin) % s), N + s + 1, s):
            tf = D / 'tours' / f'{tag}_n{n}.json'
            src = 'transplant'
            try:
                g = graph(d, n); validate(g)
            except AssertionError:
                assert tf.exists(), f'n={n}: transplant fails and no tour file'
                td = json.loads(tf.read_text()); g = tour_grid(td['tour']); validate(g); src = 'tour file'
                assert n < N, f'n={n} >= N={N} must come from the transplant'
            tvals[n] = turns(g); report['direct'].append([n, tvals[n], src])
        g = graph(d, N); g2 = graph(d, N + s)
        assert tvals[N + s] - tvals[N] == dT, ('cost step', N, tvals[N + s] - tvals[N], dT)
        spans = {}
        for (x, y), (k, _) in zone_cells(d, N).items():
            lo, hi = spans.get(k, (10**9, -1)); spans[k] = (min(lo, line((x, y))), max(hi, line((x, y))))
        gaps = [(spans['BL'][1], spans['BR'][0]), (spans['BR'][1], spans['TL'][0]), (spans['TL'][1], spans['TR'][0])]
        for k, (lo, hi) in enumerate(gaps):
            cut = None
            for a_ in range(lo + 6, hi - w - 6 + 1):
                try:
                    names, M = P.slab(g, N, a_, w)
                    assert power(M, 1 + s // w) == M
                    assert P.slab(g2, N + s, a_ + k*s, w) == (names, M)
                    assert P.slab(g2, N + s, a_ + k*s, w + s) == (names, M)
                    cut = a_; break
                except (AssertionError, StopIteration, ValueError):
                    continue
            assert cut is not None, ('no valid cut slab in gap', k, 'class', c, 'N', N, (lo, hi))
            through = sorted((i, j) for (s0, i), (t0, j) in M.items() if s0 == 0 and t0 == 1)
            report['transfers'].append(dict(cls=c, N=N, gap=k, cut=cut, ports=names, through=len(through),
                                            matching=sorted([list(u), list(v)] for u, v in M.items() if u < v)))
        cs = {n: t - 8*n for n, t in tvals.items()}
        const[c] = cs
        print(f'class n = {c} mod {s}: base N={N}; T - 8n at checked n: {cs}; 3 gaps PASS', flush=True)
    worst = max(max(v.values()) for v in const.values())
    slope = dT / s
    report['T_minus_8n'] = {str(c): v for c, v in const.items()}; report['slope'] = slope; report['worst_T_minus_8n'] = worst
    (D / 'allsize_checks.json').write_text(json.dumps(report, indent=1) + '\n')
    if slope == 8:
        print(f'PASS: T(n) <= 8n + ({worst}) for every even n >= {a.nmin} (slope {slope}); details {D / "allsize_checks.json"}')
    else:
        print(f'PASS (slope {slope}, not 8): worst T - 8n on the checked range {worst}; details {D / "allsize_checks.json"}')

if __name__ == '__main__':
    main()
