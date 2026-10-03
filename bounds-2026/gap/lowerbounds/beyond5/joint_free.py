#!/usr/bin/env python3
"""BEYOND5 request R-a (KT Lower Bounds, 2026-10-03): width-three strip, changed ports FAR from g rows.

Certifies the largest c with   X3 - rows >= #g + c * N_free(d0) - C,   where
  X3     = crossing pairs of edges that both have an end in columns 0..2 (joint_stab.py XW=3);
  g      = F1-V strong row test (up or down), as in joint_stab.py / f1v_stab.py;
  N_free = changed ports (NLOC: not on a local P / P' collar path; non-steep ports are changed) whose COLLAR ROW
           (row of the collar vertex) is at distance > d0 from every g row.
Base graph = joint_stab.py's width-three graph; each port is RESOLVED exactly once (at its collar cell, or when its
local P path completes or fails, at most two rows later) and its +1 goes to the tally of its collar row.
Augmented state = (base state, tallies of the last D+1 collar rows, g bits of the last D+d0 rows), D = max(2, d0);
the tally of row r-D is released at the end of row r with weight -c if no g row lies within distance d0.
env Q3=1: certify X3 - rows + Q3/2 >= #g + c N_free - C (BEYOND5 section 6), Q3 = quarter atoms at depth <= 4
usage: joint_free.py up|down d0 crit [c0]  |  joint_free.py up|down d0 cert a b
"""
import sys, time
from collections import deque
from fractions import Fraction
from itertools import combinations
import numpy as np
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parent / 'windows'))
import frac_stab as FS
from strip_dp import cross
from joint_stab import vis, W, UP

XW = 3
def is_wx(e): return min(e[0], e[2]) <= XW - 1
import os
Q3ON = int(os.environ.get('Q3', '0'))   # 1: add Q3/2 (quarter atoms of square row r, depth <= 4) to the left side
from f1v_stab import tile_quarters
from math import comb
Q3C = {}


def q3_of(edges):
    """Quarter-atom units in square row -1 (relative to the new row), squares x = 0..4, from the pending edges.
    Exact in squares x <= 2 (every edge whose tile meets them is in the model); x = 3, 4: W3 and X1 lower bounds,
    no holes counted. holes 1, X1 pair 1 (single overlap quarter in this row), W3 binomial(m-1, 2)."""
    key = tuple(e[:4] for e in edges)
    if key in Q3C: return Q3C[key]
    tq = {e: {t for t in tile_quarters(e) if t[1] == -1 and 0 <= t[0] <= 4} for e in key}
    full = {e: tile_quarters(e) for e in key}
    mult = {}
    for e in key:
        for t in tq[e]: mult[t] = mult.get(t, 0) + 1
    u = 0
    for x in range(5):
        for qn in 'brtl':
            m = mult.get((x, -1, qn), 0)
            if m == 0 and x <= 2: u += 1
            if m >= 3: u += comb(m - 1, 2)
    for e, f in combinations(key, 2):
        ov = full[e] & full[f]
        if len(ov) == 1:
            (x, y, qn), = ov
            if y == -1 and 0 <= x <= 4: u += 1
    Q3C[key] = u
    return u


QN = 'brtl'
COVROWS = {"r": (-1, 0, 1, 2), "b": (-1, 0, 1), "l": (0, 1), "t": (0, 1, 2)}   # column-3 rows (relative to the square row) whose outside edges can cover that quarter; only b, l are used
# square row) whose outside edges (3,y)-(4,y+-2), (3,y)-(5,y+-1) can cover that quarter of square (3, s)
U3C = {}


def u3_of(edges):
    """bitmask of the quarters of square (3, -1) that no pending model edge covers."""
    key = tuple(e[:4] for e in edges)
    if key not in U3C:
        cov = set()
        for e in key: cov |= {t[2] for t in tile_quarters(e) if t[0] == 3 and t[1] == -1}
        U3C[key] = sum(1 << i for i, qn in enumerate(QN) if qn not in cov)
    return U3C[key]


def build(orient):
    coef, exc = FS.test(orient)
    def tcont(es):
        F = E = 0
        for e in es:
            k = FS.key((e[0], e[1]), (e[2], e[3])); F += coef.get(k, 0); E += k in exc
        return F, E
    start = (0, (), 0, 0, 0, 0)
    index = {start: 0}; states = [start]; q = deque([0])
    S, D, Wt, G, C0, C1, C2, RE, Q3L, SAT, U3 = [], [], [], [], [], [], [], [], [], [], []
    t0 = time.time()
    while q:
        sid = q.popleft()
        x, edges, F, E, vb, qa = states[sid]
        incoming = [e for e in edges if e[2] == x and e[3] == 0]
        rest = [e for e in edges if not (e[2] == x and e[3] == 0)]
        strip = x <= 2
        cands = []
        for dx, dy in UP:
            tx = x + dx
            if 0 <= tx < W and (strip or tx <= 2):
                cands.append((x, 0, tx, dy))
        if strip:
            r = 2 - len(incoming)
            if r < 0: continue
            need = [r]
        else:
            if len(incoming) > 2: continue
            need = range(0, 3 - len(incoming))
        tdeg0 = {}
        for e in rest: tdeg0[(e[2], e[3])] = tdeg0.get((e[2], e[3]), 0) + 1
        inv = sorted((e[0] - x, e[1]) for e in incoming)          # incoming lower ends, relative
        for r in need:
            for chosen in combinations(cands, r):
                tdeg = dict(tdeg0); ok = True
                for e in chosen:
                    k = (e[2], e[3]); tdeg[k] = tdeg.get(k, 0) + 1
                    if tdeg[k] > 2: ok = False
                if not ok: continue
                w = 0
                for i, f in enumerate(chosen):
                    if not is_wx(f): continue
                    for e in rest:
                        if is_wx(e) and cross(e[:4], f): w += 1
                    for g2 in chosen[:i]:
                        if is_wx(g2) and cross(g2, f): w += 1
                # port resolution: cc[d] = changed ports whose collar row is d rows below the current row
                cc = [0, 0, 0]
                outv = sorted((f[2] - x, f[3]) for f in chosen)
                flags = {}
                new_rest = list(rest)
                if strip:
                    for e in incoming:
                        if e[0] >= 3:                                   # port edge arriving from a ghost cell
                            steep = (e[0] - x == 2)
                            if not steep: cc[0] += 1                    # (3,y-2)-(2,y): non-steep, changed
                            elif x == 1 and inv == [(2, -1)] and outv == [(-1, 2)]:
                                flags[(1, 0, 0, 2)] = 3                 # '\\' P path, C' = (1,y-1): pending
                            elif x == 2 and inv == [(2, -1)] and outv == [(-2, 1)]:
                                flags[(2, 0, 0, 1)] = 4                 # '\\' P path, A' = (2,y): pending
                            else: cc[0] += 1
                    if x == 0:
                        fl = {e[:4]: e[4] for e in incoming if e[4] in (3, 4)}
                        both = (r == 0 and fl.get((1, -2, 0, 0)) == 3 and fl.get((2, -1, 0, 0)) == 4)
                        if not both:
                            if fl.get((1, -2, 0, 0)) == 3: cc[2] += 1       # port at C' (row -2) changed
                            if fl.get((2, -1, 0, 0)) == 4: cc[1] += 1       # port at A' (row -1) changed
                        if not incoming and outv == [(1, 2), (2, 1)]:
                            flags[(0, 0, 1, 2)] = 1                     # '/' P path, B = (0,y-1): candidate
                    if x == 2:
                        cons = inv == [(-2, -1)] and outv == [(2, 1)]
                        hit = False
                        for j, e in enumerate(new_rest):
                            if e[:4] == (0, -1, 1, 1) and e[4] == 1:
                                hit = cons; new_rest[j] = e[:4] + (2 if cons else 0,)
                        for f in chosen:
                            if f[2] >= 3:
                                if f[2] == 4 and hit: pass             # '/' port at A: pending
                                else: cc[0] += 1                        # steep '/' port without P, or non-steep
                    if x == 1:
                        fl2 = [e for e in incoming if e[:4] == (0, -2, 1, 0) and e[4] == 2]
                        done = bool(fl2) and len(incoming) == 1 and outv == [(2, 1)]
                        if fl2 and not done: cc[1] += 1                 # port at A (row -1) changed
                        for f in chosen:
                            if f[2] >= 3 and not done: cc[0] += 1       # '/' col-1 port, changed
                new_edges = new_rest + [f + (flags.get(f, 0),) for f in chosen]
                dF, dE = tcont(chosen)
                F2 = (F + dF) % 3; E2 = min(E + dE, 2)
                nx = x + 1; g = 0
                if nx == W:
                    nx = 0
                    ne = tuple(sorted((a, b - 1, c, d - 1, fl) for a, b, c, d, fl in new_edges))
                    v = vis(ne)
                    vv = v if orient == 'up' else vb
                    g = 1 if (F2 != 2 or E2 >= 2 or vv) else 0
                    F3, E3 = tcont(ne); ns = (0, ne, F3 % 3, min(E3, 2), v if orient == 'down' else 0, 0)
                else:
                    ns = (nx, tuple(sorted(new_edges)), F2, E2, vb, 0)
                if ns not in index:
                    index[ns] = len(states); states.append(ns); q.append(index[ns])
                    if len(states) % 200000 == 0:
                        print(f'  states {len(states)}, queue {len(q)}, {time.time() - t0:.0f}s', flush=True)
                S.append(sid); D.append(index[ns]); Wt.append(w); G.append(g); C0.append(cc[0]); C1.append(cc[1]); C2.append(cc[2]); RE.append(nx == 0); Q3L.append(q3_of(ns[1]) if (Q3ON and nx == 0) else 0); SAT.append(1 if (x == 3 and len(incoming) + r == 2) else 0); U3.append(u3_of(ns[1]) if (Q3ON and nx == 0) else 0)
    print(f'{orient}: states {len(states)}, arcs {len(S)}, build {time.time() - t0:.0f}s', flush=True)
    return states, np.array(S), np.array(D), np.array(Wt), np.array(G), np.array(C0), np.array(C1), np.array(C2), np.array(RE), np.array(Q3L), np.array(SAT), np.array(U3)



def augment(base, d0):
    states, S, D, Wt, G, C0, C1, C2, RE, Q3L, SAT, U3 = base
    Dn = max(2, d0)
    order = np.argsort(S, kind='stable'); S, D, Wt, G, C0, C1, C2, RE, Q3L, SAT, U3 = (a[order] for a in (S, D, Wt, G, C0, C1, C2, RE, Q3L, SAT, U3))
    ptr = np.searchsorted(S, np.arange(len(states) + 1))
    D, Wt, G, C0, C1, C2, RE, Q3L, SAT, U3 = (a.tolist() for a in (D, Wt, G, C0, C1, C2, RE, Q3L, SAT, U3)); ptr = ptr.tolist()
    def canon(tl, gb):
        # tl[j] = tally of row R-j (j = 0..Dn), gb[i] = g of row R-1-i (i = 0..Dn+d0-1); R = current row
        tl = list(tl)
        for j in range(1, Dn + 1):
            if tl[j] and any(gb[i] for i in range(len(gb)) if abs(1 + i - j) <= d0): tl[j] = 0
        keep = [0] * len(gb)
        for i in range(len(gb)):
            # rows R-2..R can still receive tallies, so g bits near them are always kept
            if gb[i] and (1 + i <= d0 + 2 or any(tl[j] and abs(1 + i - j) <= d0 for j in range(1, Dn + 1))): keep[i] = 1
        return tuple(tl), tuple(keep)
    # compact keys: aug id <-> (base state, buffer code); buffer codes are interned in bufs / bufid
    from array import array
    z = (tuple([0] * (Dn + 1)), tuple([0] * (Dn + d0)), (0, 0, 0, 0))
    bufs = [z]; bufid = {z: 0}
    NBMAX = 1 << 20
    idx = {0: 0}; keyl = array('q', [0]); q = deque([0])
    AS, AD, AW, AG, AQ, AK, A3 = (array('i') for _ in range(7))
    t0 = time.time()
    while q:
        u = q.popleft(); kv = keyl[u]; s, (tl, gb, hb) = kv // NBMAX, bufs[kv % NBMAX]
        for k in range(ptr[s], ptr[s + 1]):
            t = list(tl); t[0] += C0[k]; t[1] += C1[k]; t[2] += C2[k]
            qf = 0; holes = 0
            u1, s1, s2, s0 = hb            # u1 = U of square row R-1 (b, l only); s1, s2 = sat of rows R-1, R-2; s0 = row R
            if SAT[k]: s0 = 1
            if RE[k]:
                g = G[k]
                far = all((g if j == 0 else gb[j - 1]) == 0 for j in range(Dn - d0, Dn + d0 + 1))
                qf = t[Dn] if far else 0
                # decide square row R-1: quarter b needs rows R-2, R-1, R saturated; quarter l needs R-1, R
                if u1:
                    holes = (1 if (u1 & 1 and s2 and s1 and s0) else 0) + (1 if (u1 & 2 and s1 and s0) else 0)
                uR = U3[k]
                uR = (1 if (uR & 1 and s1 and s0) else 0) | (2 if (uR & 8 and s0) else 0)   # bits b, l; known rows only
                nh = (uR, s0 if uR else 0, s1 if (uR & 1) else 0, 0)
                nb = canon([0] + t[:Dn], (g,) + gb[:-1]) + (nh,)
            else:
                nb = (tuple(t), gb, (u1, s1, s2, s0))
            b = bufid.get(nb)
            if b is None:
                b = bufid[nb] = len(bufs); bufs.append(nb); assert b < NBMAX
            kk = D[k] * NBMAX + b
            v = idx.get(kk)
            if v is None:
                v = idx[kk] = len(keyl); keyl.append(kk); q.append(v)
                if len(keyl) % 1000000 == 0: print(f'  aug states {len(keyl)}, {time.time() - t0:.0f}s', flush=True)
            AS.append(u); AD.append(v); AW.append(Wt[k]); AG.append(G[k] if RE[k] else 0); AQ.append(qf); AK.append(int(order[k])); A3.append(Q3L[k] + holes)
    del idx
    key = [(kv // NBMAX, bufs[kv % NBMAX]) for kv in keyl] if len(keyl) < 3_000_000 else None
    print(f'augmented (d0 = {d0}): states {len(keyl)}, arcs {len(AS)}, buffers {len(bufs)}, {time.time() - t0:.0f}s', flush=True)
    return len(keyl), np.frombuffer(AS, dtype=np.int32), np.frombuffer(AD, dtype=np.int32), np.frombuffer(AW, dtype=np.int32), np.frombuffer(AG, dtype=np.int32), np.frombuffer(AQ, dtype=np.int32), np.frombuffer(AK, dtype=np.int32), (key, keyl, bufs, NBMAX), np.frombuffer(A3, dtype=np.int32)


def weights(Wt, G, Qv, c, Q3v=None):
    """10b * (w - 1/5 - g + Q3/2 - c Qfar) per arc: certifies X3 - rows + Q3/2 >= #g + c N_free - C."""
    a, b = c.numerator, c.denominator
    ww = 2 * b * (W * Wt.astype(np.int64) - 1)
    ww -= 2 * W * b * G.astype(np.int64); ww -= 2 * W * a * Qv.astype(np.int64)
    if Q3v is not None: ww += W * b * Q3v.astype(np.int64)
    return ww


def main():
    orient, d0, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    base = build(orient)
    M, S, D, Wt, G, Qv, AK, key, Q3v = augment(base, d0)
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    if mode == 'cert':
        c = Fraction(int(sys.argv[4]), int(sys.argv[5]))
        res, data, it = FS.neg_cycle(S, D, weights(Wt, G, Qv, c, Q3v), M)
        print(f'c = {c}: {res} after {it} passes' + (f'; potential range {data[used].min()}..{data[used].max()} (units 1/(10b))' if res == 'ok' else ''))
        return
    c = Fraction(sys.argv[4]) if len(sys.argv) > 4 else Fraction(1)
    while True:
        res, data, it = FS.neg_cycle(S, D, weights(Wt, G, Qv, c, Q3v), M)
        if res == 'ok':
            print(f'{orient} d0={d0}: CRITICAL c* = {c} = {float(c):.6f}; potential range {data[used].min()}..{data[used].max()} '
                  f'(units 1/(10b)), {it} passes', flush=True)
            np.save(f'free_pot_{orient}_d{d0}_q{Q3ON}.npy', data); return
        num = int((2 * (W * Wt[data].astype(np.int64) - 1) - 2 * W * G[data] + W * Q3v[data]).sum()); den = int(Qv[data].sum())
        print(f'  negative cycle: {len(data)} arcs ({len(data) / W:.0f} rows), sum(10w-2-10g+5q3) = {num}, sum Q3 = {int(Q3v[data].sum())}, sum Qfar = {den}', flush=True)
        np.save(f'free_cycle_{orient}_d{d0}_q{Q3ON}.npy', np.array(data))
        bst, bS, bD = base[0], base[1], base[2]
        for a in data:
            k = AK[a]; x = bst[bS[k]][0]; sh = 1 if x == W - 1 else 0
            ch = [(e[0], e[2] - e[0], e[3] - e[1]) for e in bst[bD[k]][1] if (e[0], e[1]) == (x, -sh)]
            kv = key[1][S[a]]; print(f'    x={x} chosen {ch} w={Wt[a]} g={G[a]} c=({base[5][k]},{base[6][k]},{base[7][k]}) Qfar={Qv[a]} q3={Q3v[a]} buf={key[2][kv % key[3]]}')
        if den <= 0: print('  cycle with Qfar <= 0: g-rate-1 fails?'); return
        c = Fraction(num, 2 * W * den); print(f'  -> c <= {c} = {float(c):.6f}', flush=True)


if __name__ == '__main__':
    main()
