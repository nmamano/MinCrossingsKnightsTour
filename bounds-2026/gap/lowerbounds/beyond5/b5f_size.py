#!/usr/bin/env python3
"""B5f sizing (KT Lower Bounds, 2026-10-03): reachable state count of the width-6 pairing DP, NO weights, NO certificate.
Strip cells x = 0..5, scan order (y, x). Fixed boundary (U collar of FOLD, period 1): ports (4,y)-(6,y+1), (5,y)-(7,y+1),
so cells 4, 5 have internal degree 1, cells 0..3 degree 2. Pairing of U: the path through port (5,r) ends at port (4,r+2).
State = (x, pending internal edges (lx, ly, ux, uy, piece label), piece types); types: 'G' (no port, 2 ends), 'V' (holds
a partner pair, 2 ends), ('W', due) (holds port (5, r), 1 end, partner (4, due) with due relative to the current row).
usage: b5f_size.py CAP"""
import sys, time
from collections import deque
from itertools import combinations
CAP = int(sys.argv[1]); W = 6
NEED = [2, 2, 2, 2, 1, 1]
UPM = [(2, 1), (-2, 1), (1, 2), (-1, 2)]


def canon(x, ends, types):
    ends = sorted(ends)
    m = {}; out = []
    for e in ends:
        if e[4] not in m: m[e[4]] = len(m)
        out.append(e[:4] + (m[e[4]],))
    ty = [None] * len(m)
    for old, new in m.items(): ty[new] = types[old]
    return (x, tuple(out), tuple(ty))


def u_state():
    """U collar frontier at the start of row 0 (cell (0,0) not yet processed)."""
    pat = [(0, 2, 1), (1, -1, 2), (1, 2, 1), (2, 2, 1), (3, 2, 1)]
    E = [(x, y, x + dx, y + dy) for y in range(-8, 0) for x, dx, dy in pat]
    par = {}
    def f(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for (a, b, c, d) in E:
        if d < 0: par[f((a, b))] = f((c, d))
    pend = [e for e in E if e[3] >= 0]
    comp = {}
    for e in pend: comp.setdefault(f((e[0], e[1])), []).append(e)
    ends, types = [], {}
    for k, (root, es) in enumerate(comp.items()):
        cells = [v for v in par if f(v) == root]
        p5 = [v for v in cells if v[0] == 5]; p4 = [v for v in cells if v[0] == 4]
        if len(es) == 2 and not p4 and not p5: types[k] = 'G'
        elif len(es) == 1 and len(p5) == 1 and not p4: types[k] = ('W', p5[0][1] + 2)
        else: raise SystemExit(f'unexpected U piece {cells} {es}')
        ends += [e + (k,) for e in es]
    return canon(0, ends, types)


def step(st):
    x, ends, types = st; types = dict(enumerate(types))
    inc = [e for e in ends if e[2] == x and e[3] == 0]
    rest = [e for e in ends if not (e[2] == x and e[3] == 0)]
    r = NEED[x] - len(inc)
    if r < 0: return
    cands = [(x, 0, x + dx, dy) for dx, dy in UPM if 0 <= x + dx < W]
    tdeg0 = {}
    for e in rest: tdeg0[(e[2], e[3])] = tdeg0.get((e[2], e[3]), 0) + 1
    labs = [e[4] for e in inc]
    if len(labs) == 2 and labs[0] == labs[1]:
        if types[labs[0]] != 'V' or x >= 4: return       # closes a G piece = cycle; a W piece has one end
        merged_closed = True
    else: merged_closed = False
    for chosen in combinations(cands, r):
        tdeg = dict(tdeg0); ok = True
        for e in chosen:
            k = (e[2], e[3]); tdeg[k] = tdeg.get(k, 0) + 1
            if tdeg[k] > NEED[e[2]]: ok = False
        if not ok: continue
        ty = dict(types); nl = max(ty, default=-1) + 1
        if merged_closed:
            del ty[labs[0]]; new_ends = rest
        else:
            ip = sorted(set(labs))
            kinds = [ty[l] for l in ip]
            others = [e for e in rest if e[4] in ip]          # remaining ends of the incoming pieces
            base = [e for e in rest if e[4] not in ip]
            for l in ip: del ty[l]
            piece_ends = [e[:4] for e in others] + list(chosen)
            nW = [k for k in kinds if k != 'G' and k != 'V']; nV = kinds.count('V')
            if x <= 3:
                if len(nW) + nV > 1: continue
                t = nW[0] if nW else ('V' if nV else 'G')
            elif x == 5:
                if nW or nV: continue
                t = ('W', 2)
            else:  # x == 4: port (4, 0) pairs with the W due 0
                wd = [l for l, k in types.items() if k == ('W', 0)]
                if len(wd) != 1: continue
                if nV or any(k != ('W', 0) for k in nW): continue
                if nW:
                    t = None                                   # path completed inside the merged piece
                    if piece_ends: continue
                else:
                    wl = wd[0]
                    piece_ends += [e[:4] for e in rest if e[4] == wl]
                    base = [e for e in base if e[4] != wl]; del ty[wl]
                    t = 'V'
            need_ends = {'G': 2, 'V': 2}.get(t, 1) if t is not None else 0
            if len(piece_ends) != need_ends: continue
            if t is None: new_ends = base
            else:
                ty[nl] = t; new_ends = base + [e + (nl,) for e in piece_ends]
        if x + 1 == W:
            sh = [(a, b - 1, c, d - 1, l) for a, b, c, d, l in new_ends]
            ty2 = {l: (('W', k[1] - 1) if isinstance(k, tuple) else k) for l, k in ty.items()}
            yield canon(0, sh, ty2)
        else:
            yield canon(x + 1, new_ends, ty)


s0 = u_state()
print('U state', s0, flush=True)
index = {s0: 0}; q = deque([s0]); arcs = 0; t0 = time.time(); pos = [0] * W
while q:
    st = q.popleft(); pos[st[0]] += 1
    for ns in step(st):
        arcs += 1
        if ns not in index:
            index[ns] = len(index); q.append(ns)
            if len(index) >= CAP: print('CAP reached', len(index), 'arcs so far', arcs, flush=True); q.clear(); break
            if len(index) % 200000 == 0: print(f'  states {len(index)}, queue {len(q)}, {time.time() - t0:.0f}s', flush=True)
print('states', len(index), 'arcs', arcs, 'per cell position (expanded)', pos, f'{time.time() - t0:.0f}s')
es = {}
for k in index: es[(k[0], tuple(e[:4] for e in k[1]))] = es.get((k[0], tuple(e[:4] for e in k[1])), 0) + 1
print('distinct edge sets among labelled states', len(es), 'ratio', len(index) / len(es), 'max labelings', max(es.values()))
print('U state back in index:', s0 in index)
# U self-check: following U's own edge choices from the U state returns to the U state after 6 cells
UCH = {0: [(0, 0, 2, 1)], 1: [(1, 0, 0, 2), (1, 0, 3, 1)], 2: [(2, 0, 4, 1)], 3: [(3, 0, 5, 1)], 4: [], 5: []}
st = s0
for x in range(W):
    keep = [n2 for n2 in step(st)]
    # pick the successor whose new pending ends from cell x are exactly U's choice
    def outs(s2): return sorted(e[:4] for e in s2[1] if (e[0], e[1]) == ((x, 0) if x + 1 < W else (x, -1)))
    want = sorted(c if x + 1 < W else (c[0], c[1] - 1, c[2], c[3] - 1) for c in UCH[x])
    cand = [n2 for n2 in keep if outs(n2) == want]
    assert len(cand) == 1, (x, len(cand)); st = cand[0]
print('U cycle closes on the U state:', st == s0)
