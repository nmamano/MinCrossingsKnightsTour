#!/usr/bin/env python3
"""Gap Lemma, square version: exhaustive check of tree islands (gap/structures/GAP_LEMMA.md section 11).

By the Structures reduction, a violation needs a 4-component U of gap squares that is a TREE polyomino (no 2x2
block, no hole), off the board sides, with ALL 2|U| + 2 boundary sides cut ends (so every side neighbour of U is a
good square), |U| + 1 cuts, and at most 2|U| + 1 bad quarters in U.

Step 1 (combinatorial). Each side neighbour N of U gets the split lambda(N) of its good square. The cut that ends
at a boundary side e is the lambda(N_e)-chain from e through U; it must leave U at a side e' with the same label.
So labels are constant on the classes of the two chain pairings ('/' and '\\' segments through U), merged over
sides with the same neighbour. Every square of U must lie in a cut (a segment whose two ends carry its split).
Step 2 (SAT, Glucose4, DRUP on UNSAT). Knight edges with an endpoint in a point box around U (margin M); degree
exactly 2 in the box, <= 2 outside (a relaxation of any tour; no cycle constraint). Links (L1): each grid side
carries one '/' and one '\\' knight edge; n_h = sum of the two links of half h; m_B = n_BR + n_LB, m_R = n_BR +
n_RT, m_T = n_TL + n_RT, m_L = n_TL + n_LB. Neighbour N good with split lambda(N): its lambda halves n = 1, the
other two n = 0. Every U square bad. Every cut absorbing: y0 + yk + k odd (L2). At most 2|U| + 1 bad quarters in U.
UNSAT for every labelling = no violation with this island shape.
usage: tree_islands.py SMAX [M]
"""
import sys, time
from itertools import combinations
from pysat.solvers import Glucose4
from pysat.card import CardEnc, EncType

import os
NODEG = os.environ.get('NODEG') == '1'   # drop all degree constraints (pure link model)
DEGMODE = os.environ.get('DEGMODE', 'full')   # full | corners (exact degree only at corners of U) | le
NOABS = os.environ.get('NOABS') == '1'   # drop the absorbing (parity) condition of the cuts
SLACK = int(os.environ.get('SLACK', '0'))   # sanity runs: allow 2|U| + 1 + SLACK bad quarters
DIRS = {'B': (0, -1), 'R': (1, 0), 'T': (0, 1), 'L': (-1, 0)}
OPP = {'B': 'T', 'T': 'B', 'L': 'R', 'R': 'L'}
HALF = {'/': {'BR': 'BR', 'TL': 'TL'}, '\\': {'RT': 'RT', 'LB': 'LB'}}
SPL = {'/': ('BR', 'TL'), '\\': ('RT', 'LB')}
QH = {'B': ('BR', 'LB'), 'R': ('BR', 'RT'), 'T': ('TL', 'RT'), 'L': ('TL', 'LB')}


def link(S, d, sig):
    """knight edge (sorted endpoint pair) of the sig-link across side d of square S."""
    i, j = S
    if d == 'L': i, d = i - 1, 'R'
    if d == 'B': j, d = j - 1, 'T'
    if d == 'R':
        e = ((i, j), (i + 2, j + 1)) if sig == '/' else ((i, j + 1), (i + 2, j))
    else:
        e = ((i, j), (i + 1, j + 2)) if sig == '/' else ((i, j + 2), (i + 1, j))
    return tuple(sorted(e))


def half_of(sig, side):
    return [h for h in SPL[sig] if side in h][0]


# ---------- tree polyominoes up to D4 (grow by leaves: removing a leaf of a tree polyomino leaves one) ----------
def tree_polyominoes(nmax):
    levels = {1: {((0, 0),)}}
    for n in range(2, nmax + 1):
        nxt = set()
        for P in levels[n - 1]:
            Ps = set(P)
            for (x, y) in P:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    c = (x + dx, y + dy)
                    if c in Ps: continue
                    if sum((c[0] + a, c[1] + b) in Ps for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) != 1: continue
                    nxt.add(canon(Ps | {c}))
        levels[n] = nxt
    return levels


def canon(P):
    best = None
    for t in range(8):
        Q = []
        for x, y in P:
            if t & 4: x, y = y, x
            if t & 1: x = -x
            if t & 2: y = -y
            Q.append((x, y))
        mx = min(q[0] for q in Q); my = min(q[1] for q in Q)
        Q = tuple(sorted((x - mx, y - my) for x, y in Q))
        if best is None or Q < best: best = Q
    return best


def is_tree(P):
    P = set(P)
    adj = sum(1 for (x, y) in P for d in ((1, 0), (0, 1)) if (x + d[0], y + d[1]) in P)
    return adj == len(P) - 1


# ---------- step 1 ----------
def segments(U, sig):
    """pair boundary sides along sig-chains through U. returns dict side -> (partner side, list of halves)."""
    pair = {}
    for S in U:
        for d, (dx, dy) in DIRS.items():
            if (S[0] + dx, S[1] + dy) in U or (S, d) in pair: continue
            cur, enter, hs = S, d, []
            while True:
                h = half_of(sig, enter); hs.append((cur, h))
                out = [c for c in h if c != enter][0]
                nx = (cur[0] + DIRS[out][0], cur[1] + DIRS[out][1])
                if nx not in U: break
                cur, enter = nx, OPP[out]
            pair[(S, d)] = ((cur, out), hs); pair[(cur, out)] = ((S, d), hs[::-1])
    return pair


def labellings(U):
    bsides = [(S, d) for S in U for d, (dx, dy) in DIRS.items() if (S[0] + dx, S[1] + dy) not in U]
    nbr = {e: (e[0][0] + DIRS[e[1]][0], e[0][1] + DIRS[e[1]][1]) for e in bsides}
    seg = {s: segments(U, s) for s in ('/', '\\')}
    parent = {N: N for N in nbr.values()}
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for s in seg:
        for e, (f, _) in seg[s].items(): parent[find(nbr[e])] = find(nbr[f])
    cls = sorted({find(N) for N in parent})
    res = []
    for mask in range(1 << len(cls)):
        lab = {N: ('/' if mask >> cls.index(find(N)) & 1 else '\\') for N in parent}
        cuts = []; covered = set()
        for e in bsides:
            s = lab[nbr[e]]; f, hs = seg[s][e]
            if e < f: cuts.append((s, e, f, hs)); covered |= {h[0] for h in hs}
        if covered == set(U): res.append((lab, cuts))
    return bsides, res


# ---------- step 2 ----------
def sat_check(U, lab, cuts, M=2, proof=False, block=()):
    U = set(U)
    sqs = U | set(lab)
    xs = [s[0] for s in sqs]; ys = [s[1] for s in sqs]
    box = {(x, y) for x in range(min(xs) - M, max(xs) + 2 + M) for y in range(min(ys) - M, max(ys) + 2 + M)}
    K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    edges = sorted({tuple(sorted((p, (p[0] + dx, p[1] + dy)))) for p in box for dx, dy in K8})
    vid = {e: i + 1 for i, e in enumerate(edges)}; top = [len(edges)]
    def new():
        top[0] += 1; return top[0]
    def blockcls(p):   # 1: convex, 2: straight, 4: diagonal pair, 3: reflex
        sq = [(p[0] - a, p[1] - b) for a in (0, 1) for b in (0, 1)]
        k = sum(x in U for x in sq)
        if k == 2 and ((p[0] - 1, p[1] - 1) in U) == ((p[0], p[1]) in U): return 4
        return k
    cl = []; inc = {}
    corners = {(x + a, y + b) for (x, y) in U for a in (0, 1) for b in (0, 1)}
    if DEGMODE in ('ncorners', 'lencorners'): corners |= {(x + a, y + b) for (x, y) in lab for a in (0, 1) for b in (0, 1)}; 
    for e in edges:
        for p in e: inc.setdefault(p, []).append(vid[e])
    for p, l in (inc.items() if not NODEG else []):
        if DEGMODE == 'lecorners' and p not in corners: continue
        if DEGMODE.startswith('cls') and (p not in corners or str(blockcls(p)) not in DEGMODE[3:]): continue
        if DEGMODE == 'lencorners' and p not in corners: continue
        for t in combinations(l, 3): cl.append([-x for x in t])
        if p in box and (DEGMODE == 'full' or (DEGMODE in ('corners', 'ncorners') and p in corners)):
            for i in l: cl.append([j for j in l if j != i])
    L = lambda S, d, s: vid[link(S, d, s)]
    def nlits(S, h):
        s = '/' if h in SPL['/'] else '\\'
        return [L(S, h[0], s), L(S, h[1], s)]
    # neighbours good with split
    for N, s in lab.items():
        o = '/' if s == '\\' else '\\'
        for h in SPL[o]:
            for l in nlits(N, h): cl.append([-l])
        for h in SPL[s]:
            a, b = nlits(N, h); cl.append([a, b]); cl.append([-a, -b])
    # quarters of U
    badlits = []
    for S in U:
        dq = []
        for q, (h1, h2) in QH.items():
            ls = nlits(S, h1) + nlits(S, h2)     # m_q = sum of these 4 links
            b = new(); badlits.append(b)
            cl.append(ls + [b])                                   # m = 0 -> bad
            for a, c in combinations(ls, 2): cl.append([-a, -c, b])  # m >= 2 -> bad
            d = new(); dq.append(d)                               # d -> m != 1
            for i in range(4): cl.append([-d, -ls[i]] + [ls[j] for j in range(4) if j != i])
        cl.append(dq)                                             # S bad
    for s, e, f, hs in (cuts if not NOABS else []):
        y0, yk = L(e[0], e[1], s), L(f[0], f[1], s); k = len(hs)
        if k % 2: cl += [[-y0, yk], [y0, -yk]]
        else: cl += [[y0, yk], [-y0, -yk]]
    card = CardEnc.atmost(lits=badlits, bound=2 * len(U) + 1 + SLACK, top_id=top[0], encoding=EncType.seqcounter)
    cl += card.clauses; top[0] = max(top[0], card.nv)
    cl = cl + [list(b) for b in block]
    S = Glucose4(bootstrap_with=cl, with_proof=proof)
    r = S.solve()
    out = (r, S.get_model() if r else None, (cl, S.get_proof()) if (proof and not r) else None, edges, vid)
    S.delete()
    return out


def main():
    SMAX = int(sys.argv[1]); M = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    t0 = time.time()
    tp = tree_polyominoes(SMAX)
    for s in range(1, SMAX + 1):
        free = sorted(tp[s]); assert all(is_tree(P) for P in free)
        nlab = nsat = 0
        for P in free:
            U = [(x + 10, y + 10) for x, y in P]
            bs, labs = labellings(U)
            for lab, cuts in labs:
                nlab += 1
                r, model, _, edges, vid = sat_check(U, lab, cuts, M)
                if r:
                    nsat += 1
                    print(f'  SAT: s={s} U={sorted(U)} labels={ {k: v for k, v in sorted(lab.items())} }', flush=True)
        print(f's={s}: {len(free)} free tree polyominoes, {nlab} admissible labellings, {nsat} SAT '
              f'({time.time() - t0:.0f}s)', flush=True)


if __name__ == '__main__':
    main()
