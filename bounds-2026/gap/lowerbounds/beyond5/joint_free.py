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


def build(orient):
    coef, exc = FS.test(orient)
    def tcont(es):
        F = E = 0
        for e in es:
            k = FS.key((e[0], e[1]), (e[2], e[3])); F += coef.get(k, 0); E += k in exc
        return F, E
    start = (0, (), 0, 0, 0, 0)
    index = {start: 0}; states = [start]; q = deque([0])
    S, D, Wt, G, C0, C1, C2, RE = [], [], [], [], [], [], [], []
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
                S.append(sid); D.append(index[ns]); Wt.append(w); G.append(g); C0.append(cc[0]); C1.append(cc[1]); C2.append(cc[2]); RE.append(nx == 0)
    print(f'{orient}: states {len(states)}, arcs {len(S)}, build {time.time() - t0:.0f}s', flush=True)
    return states, np.array(S), np.array(D), np.array(Wt), np.array(G), np.array(C0), np.array(C1), np.array(C2), np.array(RE)



def augment(base, d0):
    states, S, D, Wt, G, C0, C1, C2, RE = base
    Dn = max(2, d0)
    order = np.argsort(S, kind='stable'); S, D, Wt, G, C0, C1, C2, RE = (a[order] for a in (S, D, Wt, G, C0, C1, C2, RE))
    ptr = np.searchsorted(S, np.arange(len(states) + 1))
    D, Wt, G, C0, C1, C2, RE = (a.tolist() for a in (D, Wt, G, C0, C1, C2, RE)); ptr = ptr.tolist()
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
    z = (tuple([0] * (Dn + 1)), tuple([0] * (Dn + d0)))
    bufs = [z]; bufid = {z: 0}
    NBMAX = 1 << 20
    idx = {0: 0}; keyl = array('q', [0]); q = deque([0])
    AS, AD, AW, AG, AQ, AK = (array('i') for _ in range(6))
    t0 = time.time()
    while q:
        u = q.popleft(); kv = keyl[u]; s, (tl, gb) = kv // NBMAX, bufs[kv % NBMAX]
        for k in range(ptr[s], ptr[s + 1]):
            t = list(tl); t[0] += C0[k]; t[1] += C1[k]; t[2] += C2[k]
            qf = 0
            if RE[k]:
                g = G[k]
                far = all((g if j == 0 else gb[j - 1]) == 0 for j in range(Dn - d0, Dn + d0 + 1))
                qf = t[Dn] if far else 0
                nb = canon([0] + t[:Dn], (g,) + gb[:-1])
            else:
                nb = (tuple(t), gb)
            b = bufid.get(nb)
            if b is None:
                b = bufid[nb] = len(bufs); bufs.append(nb); assert b < NBMAX
            kk = D[k] * NBMAX + b
            v = idx.get(kk)
            if v is None:
                v = idx[kk] = len(keyl); keyl.append(kk); q.append(v)
                if len(keyl) % 1000000 == 0: print(f'  aug states {len(keyl)}, {time.time() - t0:.0f}s', flush=True)
            AS.append(u); AD.append(v); AW.append(Wt[k]); AG.append(G[k] if RE[k] else 0); AQ.append(qf); AK.append(int(order[k]))
    del idx
    key = [(kv // NBMAX, bufs[kv % NBMAX]) for kv in keyl] if len(keyl) < 3_000_000 else None
    print(f'augmented (d0 = {d0}): states {len(keyl)}, arcs {len(AS)}, buffers {len(bufs)}, {time.time() - t0:.0f}s', flush=True)
    return len(keyl), np.frombuffer(AS, dtype=np.int32).astype(np.int64), np.frombuffer(AD, dtype=np.int32).astype(np.int64), np.frombuffer(AW, dtype=np.int32).astype(np.int64), np.frombuffer(AG, dtype=np.int32).astype(np.int64), np.frombuffer(AQ, dtype=np.int32).astype(np.int64), np.frombuffer(AK, dtype=np.int32), (key, keyl, bufs, NBMAX)


def weights(Wt, G, Qv, c):
    a, b = c.numerator, c.denominator
    return b * (W * Wt - 1) - W * b * G - W * a * Qv


def main():
    orient, d0, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    base = build(orient)
    M, S, D, Wt, G, Qv, AK, key = augment(base, d0)
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    if mode == 'cert':
        c = Fraction(int(sys.argv[4]), int(sys.argv[5]))
        res, data, it = FS.neg_cycle(S, D, weights(Wt, G, Qv, c), M)
        print(f'c = {c}: {res} after {it} passes' + (f'; potential range {data[used].min()}..{data[used].max()} (units 1/(5b))' if res == 'ok' else ''))
        return
    c = Fraction(sys.argv[4]) if len(sys.argv) > 4 else Fraction(1)
    while True:
        res, data, it = FS.neg_cycle(S, D, weights(Wt, G, Qv, c), M)
        if res == 'ok':
            print(f'{orient} d0={d0}: CRITICAL c* = {c} = {float(c):.6f}; potential range {data[used].min()}..{data[used].max()} '
                  f'(units 1/(5b)), {it} passes', flush=True)
            np.save(f'free_pot_{orient}_d{d0}.npy', data); return
        num = int((W * Wt[data] - 1 - W * G[data]).sum()); den = int(Qv[data].sum())
        print(f'  negative cycle: {len(data)} arcs ({len(data) / W:.0f} rows), sum(5w-1-5g) = {num}, sum Qfar = {den}', flush=True)
        np.save(f'free_cycle_{orient}_d{d0}.npy', np.array(data))
        bst, bS, bD = base[0], base[1], base[2]
        for a in data:
            k = AK[a]; x = bst[bS[k]][0]; sh = 1 if x == W - 1 else 0
            ch = [(e[0], e[2] - e[0], e[3] - e[1]) for e in bst[bD[k]][1] if (e[0], e[1]) == (x, -sh)]
            kv = key[1][S[a]]; print(f'    x={x} chosen {ch} w={Wt[a]} g={G[a]} c=({base[5][k]},{base[6][k]},{base[7][k]}) Qfar={Qv[a]} buf={key[2][kv % key[3]]}')
        if den <= 0: print('  cycle with Qfar <= 0: g-rate-1 fails?'); return
        c = Fraction(num, W * den); print(f'  -> c <= {c} = {float(c):.6f}', flush=True)


if __name__ == '__main__':
    main()
