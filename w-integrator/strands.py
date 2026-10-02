"""Strand calculus for edge gadgets on the line family x + 2y = c.

pairing(tpl, kind): unroll a periodic gadget (kind 'bottom' or 'left', board.js template, rows
  top-first) between interior lines and trace every path that enters the band from a line end.
  Returns the induced perfect matching on line ends as pairs (a, b) of LOCAL line numbers,
  with a in [0, cper) (cper = P for bottom, 2Q for left), plus checks (closed loops inside the band,
  uncovered band cells).
Global line numbers (same phases as kt.board.build_general):
  bottom: c = c' + xb          top:   c = xt + 2(n-1) - c'
  left:   c = c' + 2*yl        right: c = n - 1 + 2*yr - c'
Regions: BL = lines with ends on bottom + left (c < n), MID = left + right (n <= c <= 2n-2),
TR = right + top.  In each region the union of the two matchings must have no finite cycle.
A Hamiltonian cycle crosses every cut {c <= t} an even number of times, so in each region the
number of matching pairs spanning a cut must be EVEN (necessary condition, "cut parity").
"""
import os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kt.board import tpl_moves

def pairing(tpl, kind, K=12):
    mv, W, H = tpl_moves(tpl)
    if kind == 'bottom':
        P, D = W, H
        inband = lambda u: 0 <= u[1] < D
        local = lambda u: mv[(u[0] % P, u[1])]
        cells = [(x, y) for x in range(-K * P, K * P) for y in range(D)]
        cper = P
        mid = [(x, y) for x in range(0, P) for y in range(D)]
    else:
        D, Q = W, H
        inband = lambda u: 0 <= u[0] < D
        local = lambda u: mv[(u[0], u[1] % Q)]
        cells = [(x, y) for y in range(-K * Q, K * Q) for x in range(D)]
        cper = 2 * Q
        mid = [(x, y) for y in range(0, Q) for x in range(D)]
    nb = lambda u: [(u[0] + d[0], u[1] + d[1]) for d in local(u)]
    line = lambda u: u[0] + 2 * u[1]
    bad = []
    for u in mid:
        for v in nb(u):
            if inband(v):
                if u not in nb(v): bad.append(('asym', u, v))
            else:
                if (v[0] - u[0], v[1] - u[1]) not in ((-2, 1), (2, -1)): bad.append(('nonline', u, v))
                if (kind == 'bottom' and v[1] < 0) or (kind == 'left' and v[0] < 0): bad.append(('offboard', u, v))
    pairs, covered = set(), set()
    for u in cells:
        outs = [v for v in nb(u) if not inband(v)]
        for v0 in outs:
            prev, cur, path = v0, u, [u]
            ok = True
            while True:
                nx = [w for w in nb(cur) if w != prev]
                if len(nx) != 1: nx = nx[:1] if nx else [prev]
                prev, cur = cur, nx[0]
                if not inband(cur): break
                path.append(cur)
                if len(path) > 4 * len(cells) // K: ok = False; break
            if not ok: continue
            a, b = line(u), line(cur)
            if a == b and len(path) == 1 and v0 == cur: continue
            covered.update(path)
            k = (min(a, b) // cper) * cper
            pairs.add((min(a, b) - k, max(a, b) - k))
    uncovered = [u for u in mid if u not in covered]
    return dict(pairs=sorted(pairs), cper=cper, bad=bad[:5], uncovered=len(uncovered))

def expand(pairs, cper, shift, sign, lo, hi):
    """Global matching dict over lines in [lo, hi): c = shift + sign * c'."""
    m = {}
    for (a, b) in pairs:
        k0 = (lo - shift) // cper - 4 if sign > 0 else (shift - hi) // cper - 4
        for k in range(k0, k0 + (hi - lo) // cper + 10):
            ga, gb = shift + sign * (a + k * cper), shift + sign * (b + k * cper)
            if lo <= ga < hi and lo <= gb < hi:
                m[ga] = gb; m[gb] = ga
    return m

def union_profile(m1, m2, lo, hi):
    """Union of two matchings on lines [lo, hi): finite cycles fully inside, strands through the
    middle cut, and the set of cut counts (pairs spanning t+1/2) over the central half."""
    adj = defaultdict(list)
    for m in (m1, m2):
        for a, b in m.items():
            if a < b: adj[a].append(b); adj[b].append(a)
    seen, cycles, comps = set(), 0, []
    for c in range(lo, hi):
        if c in seen: continue
        st, comp = [c], []
        seen.add(c)
        while st:
            u = st.pop(); comp.append(u)
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        full = all(len(adj[u]) == 2 for u in comp)
        if full: cycles += 1
        comps.append(comp)
    S = max([abs(a - b) for m in (m1, m2) for a, b in m.items()] or [0])
    q1, q3 = lo + S, hi - S                     # cuts far enough from the window edges
    if q1 >= q3: q1, q3 = (lo + hi) // 2, (lo + hi) // 2 + 1
    cuts = set()
    for t in range(q1, q3):
        cnt = sum(1 for m in (m1, m2) for a, b in m.items() if a < b and a <= t < b)
        cuts.add(cnt)
    tmid = (lo + hi) // 2
    strands = sum(1 for comp in comps if min(comp) <= tmid < max(comp) and not all(len(adj[u]) == 2 for u in comp))
    return dict(cycles=cycles, strands=strands, cuts=sorted(cuts))

def region_check(pB, pL, pR, pT, n, phases):
    """pX = pairing() results (pR, pT are left/bottom-type templates placed rotated).
    Returns per-region profile using global line numbers; lines near corners are cut off."""
    xb, xt, yl, yr = phases
    N = 3 * (n - 1)
    mB = expand(pB['pairs'], pB['cper'], xb, 1, 0, N + 1)
    mL = expand(pL['pairs'], pL['cper'], 2 * yl, 1, 0, N + 1)
    mR = expand(pR['pairs'], pR['cper'], n - 1 + 2 * yr, -1, 0, N + 1)
    mT = expand(pT['pairs'], pT['cper'], xt + 2 * (n - 1), -1, 0, N + 1)
    sub = lambda m, lo, hi: {a: b for a, b in m.items() if lo <= a < hi and lo <= b < hi}
    g = 16
    out = {}
    for name, m1, m2, lo, hi in (('BL', mB, mL, g, n - g), ('MID', mL, mR, n + g, 2 * n - g),
                                 ('TR', mR, mT, 2 * n + g, N - g)):
        out[name] = union_profile(sub(m1, lo, hi), sub(m2, lo, hi), lo, hi)
    return out

def parity(pairs, cper, shift=0, sign=1):
    """Matching parity pi = (#pairs spanning the cut t | t+1) - t  (mod 2), an invariant of a
    periodic perfect matching of the integers (shift by s adds s; reflection c -> K - c adds K - 1).
    In each region the two matchings must have EQUAL parity (else every cut is crossed an odd
    number of times and no Hamiltonian cycle exists)."""
    m = expand(pairs, cper, shift, sign, -10 * cper, 10 * cper)
    t = 0
    return (sum(1 for a, b in m.items() if a < b and a <= t < b) - t) % 2

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from assemble import NAMED
    for nm in ('H16a', 'VerticalEdge'):
        print(nm, pairing(NAMED[nm], 'bottom' if nm.startswith('H') else 'left'))
    pB = pairing(NAMED['H16a'], 'bottom'); pL = pairing(NAMED['VerticalEdge'], 'left')
    for n in (64, 70):
        x0, X0, y0, Y0 = 0, (13 - 2 * n) % 8, 2, (-n // 2) % 4
        print(n, region_check(pB, pL, pL, pB, n, (x0, X0, y0, Y0)))
