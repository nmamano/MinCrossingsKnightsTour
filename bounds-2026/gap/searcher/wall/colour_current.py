#!/usr/bin/env python3
"""Colour current of wall.cpp witnesses (KT Edge Searcher, 2026-10-03; BEYOND5_FLUX.md item B).
For a cell set S of a 2-regular graph: (sum over edges leaving S of chi(inner end)) = 2 (B_S - W_S), chi = (-1)^(x+y).
Cuts: LEFT = cells u < 0 | u >= 0, RIGHT = cells u < WM | u >= WM (scan column u = x - shift(y)); every edge that
crosses either cut has a modeled end, so it is represented. Q = sum over crossing edges with lower end in one period
of chi(left end). Reference: the same cut through a straight '/'H field ((2,1) lines everywhere). dQ = Q - Q_ref is
the current that the field injects through the cut (0 for straight fields; zigzag: 3|a-b|/2 per step (a,b)).
usage: colour_current.py LOG [LOG ...]"""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ribbon_ends import parse, analyse, fdiv

def run(path):
    SA, SB, WM, KM, secs = parse(path)
    print(f'== {path}: shear {SA}/{SB}, WM={WM}')
    for s in secs:
        cyc = s['cyc']; R = cyc['rows']; ph0 = analyse(SA, SB, WM, KM, cyc)['ph0']
        sh = lambda y: fdiv(SA * (ph0 + y), SB) - fdiv(SA * ph0, SB)
        PX = sh(R)
        per = [((u + sh(row), b), (u + sh(row) + c - a, d)) for row, u, es in cyc['lines'] for (a, b, c, d) in es]
        reps = 2 if (PX + R) % 2 else 1   # chi flips under the period shift when PX + R is odd
        E = set()
        for k in range(-3, 4):
            for p, q in per: E.add(((p[0] + k * PX, p[1] + k * R), (q[0] + k * PX, q[1] + k * R)))
        chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
        U = lambda c: c[0] - sh(c[1])
        def Q(edges, cut):
            t = 0
            for p, q in edges:
                lo = p if p[1] <= q[1] else q
                if not (0 <= lo[1] < reps * R): continue
                a, b = (p, q) if U(p) < U(q) else (q, p)
                if U(a) < cut <= U(b): t += chi(a)
            return t
        ref = set()
        for y in range(-4, reps * R + 4):
            for x in range(sh(y) - 8, sh(y) + WM + 8): ref.add(((x, y), (x + 2, y + 1)))
        QL, QR, rL, rR = Q(E, 0), Q(E, WM), Q(ref, 0), Q(ref, WM)
        rows = reps * R
        print(f"  lambda {s['lam']} ({s.get('result', '?')}): {rows} rows, crossings {cyc['X'] * reps}; "
              f"left cut Q={QL} ref={rL} dQ={QL - rL} ({(QL - rL) / rows:+.3f}/row); "
              f"right cut Q={QR} ref={rR} dQ={QR - rR} ({(QR - rR) / rows:+.3f}/row)")

for path in sys.argv[1:]: run(path)
