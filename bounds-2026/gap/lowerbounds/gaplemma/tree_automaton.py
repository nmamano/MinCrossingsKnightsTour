#!/usr/bin/env python3
"""Gap Lemma, square version, for ALL tree islands: a tree-automaton (bottom-up DP) certificate.

Setting (gap/structures/GAP_LEMMA.md section 11; tree_islands.py): U is a tree polyomino of bad squares, every side
neighbour of U is a good square with a split label, every boundary side of U ends a cut. A violation needs total
excess sum_{S in U} (b(S) - 2) <= 1. We show min excess >= 2 over all finite trees.

Model (a RELAXATION of the real constraints, so a lower bound here is a proof):
- node = U square C with the types of its 3 x 3 block: side neighbours U or N/ N\\ (good, split label), diagonal
  squares U / N / O (O = unconstrained; used when no U side neighbour of C touches it).
- link variables (L1: one '/' and one '\\' knight edge per grid side). Owned constraints of C: C bad (b = number of
  quarters with m != 1, m from L1); every N square of the block good with its split (its split halves n = 1, the
  other halves n = 0); degree <= 2 at the four corners of C (edges on sides owned only by O squares dropped).
- chains: every '/' and '\\' segment through U joins two boundary sides with EQUAL labels; if the label equals the
  segment type it is a cut and must be absorbing (L2: y0 + yk + k odd).
- tree edge C-X: shared key = types of the 2 x 3 region around the shared side, the links on region sides used by
  both C and X, and the chain state (label, parity) of the '/' and '\\' segment parts on the child side.
Value(dir, key) = min excess of a finite subtree hanging below the edge; least fixed point from +infinity.
usage: tree_automaton.py [maxiter]
"""
import sys, time, itertools
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType
import os
from tree_islands import link, SPL, QH
SYNC = os.environ.get('SYNC', '1') == '1'
UNIFORM = os.environ.get('UNIFORM', '1') == '1'   # all neighbour labels '\\' (Uniformity Lemma + reflection)

DV = {'B': (0, -1), 'R': (1, 0), 'T': (0, 1), 'L': (-1, 0)}
OPP = {'B': 'T', 'T': 'B', 'L': 'R', 'R': 'L'}
HALVES = {'BR': '/', 'TL': '/', 'RT': '\\', 'LB': '\\'}
K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])


def side_id(S, d):
    i, j = S
    return {'B': ('h', i, j), 'T': ('h', i, j + 1), 'L': ('v', i, j), 'R': ('v', i + 1, j)}[d]


def side_squares(sid):
    t, i, j = sid
    return [(i, j - 1), (i, j)] if t == 'h' else [(i - 1, j), (i, j)]


def edge_side(e):
    """grid side (short diagonal) and split of knight edge e."""
    (x0, y0), (x1, y1) = e
    if abs(x1 - x0) == 2:
        sid = ('v', (x0 + x1) // 2, min(y0, y1))
    else:
        sid = ('h', min(x0, x1), (y0 + y1) // 2)
    S = side_squares(sid)[1]; d = 'B' if sid[0] == 'h' else 'L'
    sig = '/' if link(S, d, '/') == e else '\\'
    assert link(S, d, sig) == e
    return sid, sig


def edges_at(v):
    return [tuple(sorted((v, (v[0] + dx, v[1] + dy)))) for dx, dy in K8]


def shift_edge(e, o): return tuple(sorted((sub(e[0], o), sub(e[1], o))))


BLOCK = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]
SIDEN = [DV[d] for d in 'BRTL']


def block_types():
    """all type assignments of the 8 block squares around C = (0,0)."""
    out = []
    NT = ['N\\'] if UNIFORM else ['N/', 'N\\']
    for st in itertools.product(['U'] + NT, repeat=4):
        ty = {DV[d]: st[k] for k, d in enumerate('BRTL')}
        diag_opts = []
        for dx in (-1, 1):
            for dy in (-1, 1):
                a, b = ty[(dx, 0)], ty[(0, dy)]
                if a == 'U' and b == 'U': diag_opts.append([((dx, dy), t) for t in NT])
                elif a == 'U' or b == 'U': diag_opts.append([((dx, dy), t) for t in ['U'] + NT])
                else: diag_opts.append([((dx, dy), 'O')])
        for ch in itertools.product(*diag_opts):
            t2 = dict(ty); t2.update(dict(ch)); t2[(0, 0)] = 'U'
            out.append(t2)
    return out


def used_links(center, types):
    """links (edges) used by the owned constraints of U square `center`, given types of its block (global coords)."""
    used = set()
    for d in 'BRTL':
        for sg in '/\\': used.add(link(center, d, sg))
    for off in BLOCK:
        Q = add(center, off)
        if types.get(Q, 'O').startswith('N'):
            for d in 'BRTL':
                for sg in '/\\': used.add(link(Q, d, sg))
    for v in [add(center, c) for c in ((0, 0), (1, 0), (0, 1), (1, 1))]:
        blk = [sub(v, (a, b)) for a in (0, 1) for b in (0, 1)]
        for e in edges_at(v):
            sid, sg = edge_side(e)
            owner = [q for q in side_squares(sid) if q in blk][0]
            if types.get(owner, 'O') != 'O': used.add(e)
    return used


def region(C, d):
    """2 x 3 region of squares around the side between C and X = C + d."""
    X = add(C, DV[d])
    if d in 'LR':
        return [add(C, (0, k)) for k in (-1, 0, 1)] + [add(X, (0, k)) for k in (-1, 0, 1)]
    return [add(C, (k, 0)) for k in (-1, 0, 1)] + [add(X, (k, 0)) for k in (-1, 0, 1)]


def region_sides(R):
    s = set()
    for Q in R:
        for d in 'BRTL': s.add(side_id(Q, d))
    return s


def key_links(C, d, types):
    """links shared by C and X = C + d (both computed from region types only)."""
    X = add(C, DV[d]); R = region(C, d)
    rt = {Q: types[Q] for Q in R}
    rs = region_sides(R)
    def on_region(e): return edge_side(e)[0] in rs
    uC = {e for e in used_links(C, rt) if on_region(e)}
    uX = {e for e in used_links(X, rt) if on_region(e)}
    return sorted(uC & uX), tuple(rt[Q] for Q in R)


def side_link_solutions(types):
    """feasible assignments of the 8 side links of C = (0,0) (local view: copies of all other block links are
    existentially quantified). Owned constraints: C bad, N squares of the block good, degree <= 2 at C's corners."""
    C = (0, 0)
    used = sorted(used_links(C, types))
    vid = {e: i + 1 for i, e in enumerate(used)}; top = [len(used)]
    cl = []
    for v in ((0, 0), (1, 0), (0, 1), (1, 1)):
        blk = [sub(v, (a, b)) for a in (0, 1) for b in (0, 1)]
        es = []
        for e in edges_at(v):
            sid, sg = edge_side(e)
            owner = [q for q in side_squares(sid) if q in blk][0]
            if types.get(owner, 'O') != 'O': es.append(vid[e])
        for t in itertools.combinations(es, 3): cl.append([-x for x in t])
    nv = lambda S, h: [vid[link(S, h[0], HALVES[h])], vid[link(S, h[1], HALVES[h])]]
    for off in BLOCK:
        ty = types[off]
        if not ty.startswith('N'): continue
        lam = ty[1]
        for h, sg in HALVES.items():
            a, b = nv(off, h)
            if sg == lam: cl += [[a, b], [-a, -b]]
            else: cl += [[-a], [-b]]
    dq = []
    for q, (h1, h2) in QH.items():
        ls = nv(C, h1) + nv(C, h2)
        top[0] += 1; dd = top[0]; dq.append(dd)
        for i in range(4): cl.append([-dd, -ls[i]] + [ls[j] for j in range(4) if j != i])
    cl.append(dq)
    own = [(d, sg) for d in 'BRTL' for sg in '/\\']
    proj = [vid[link(C, d, sg)] for d, sg in own]
    extra = {}      # per U neighbour side d: cross-side links and partial degree sums at the two shared corners
    for d in 'BRTL':
        if types[DV[d]] != 'U' or not SYNC: continue
        X = DV[d]; pv = PERP[d]; mv = (-pv[0], -pv[1])
        cross = []
        for w in (pv, mv):
            A, B = add(C, w), add(X, w)          # side between A and B
            dd = [k for k, vv in DV.items() if vv == sub(B, A)][0]
            for sg in '/\\': cross.append(vid[link(A, dd, sg)])
        parts = []
        sid = side_id(C, d)
        for v in set(sum([[p for p in sq_pts(C)] for _ in [0]], [])) & set(sq_pts(X)):
            blk = [sub(v, (a, b)) for a in (0, 1) for b in (0, 1)]
            cp, xp = [], []
            for e in edges_at(v):
                es, sg = edge_side(e)
                owner = [q for q in side_squares(es) if q in blk][0]
                if types.get(owner, 'O') == 'O': continue
                (cp if owner in (C, add(C, pv), add(C, mv)) else xp).append(vid[e])
            parts.append((v, cp, xp))
        parts.sort()
        extra[d] = (cross, parts)
        for x in cross: proj.append(x)
        for v, cp, xp in parts: proj += cp + xp
    proj = sorted(set(proj))
    sols = set()
    S = Minisat22(bootstrap_with=cl)
    while S.solve():
        m = set(l for l in S.get_model() if l > 0)
        val = tuple(int(vid[link(C, d, sg)] in m) for d, sg in own)
        ex = []
        for d in 'BRTL':
            if d not in extra: ex.append(None); continue
            cross, parts = extra[d]
            ex.append((tuple(int(x in m) for x in cross),
                       tuple((sum(x in m for x in cp), sum(x in m for x in xp)) for v, cp, xp in parts)))
        sols.add((val, tuple(ex)))
        S.add_clause([-p if p in m else p for p in proj])
    S.delete()
    out = []
    for val, ex in sols:
        dv = {(d, sg): x for (d, sg), x in zip(own, val)}
        dv['ex'] = dict(zip('BRTL', ex))
        out.append(dv)
    return out


def sq_pts(S): return [add(S, c) for c in ((0, 0), (1, 0), (0, 1), (1, 1))]


PERP = {'B': (1, 0), 'T': (1, 0), 'L': (0, 1), 'R': (0, 1)}
CHAIN_HALVES = {'/': [('B', 'R'), ('T', 'L')], '\\': [('R', 'T'), ('L', 'B')]}
STATES = [(lam, par) for lam in '/\\' for par in (0, 1)]
if os.environ.get('UNIFORM', '1') == '1': STATES = [('\\', 0), ('\\', 1)]


def region_types(types, dp):
    """types of the 4 region squares around the side between C and its neighbour at dp, relative to C."""
    pv = PERP[dp]; D = DV[dp]
    pos = [add(D, pv), sub(D, pv), pv, (-pv[0], -pv[1])]
    return tuple(types[p] for p in pos)


def b_val(val):
    n = lambda h: val[(h[0], HALVES[h])] + val[(h[1], HALVES[h])]
    return sum((n(h1) + n(h2)) != 1 for q, (h1, h2) in QH.items())


def combine(types, val, dp, cstates):
    """chain bookkeeping at C. dp: parent side or None. cstates: dict child side -> {'/': state, '\\': state}.
    Returns upward states {'/': st, '\\': st} (or {} at the root), or None if a completed segment is invalid."""
    up = {}
    for tau, hs in CHAIN_HALVES.items():
        for d1, d2 in hs:
            ends = []
            for d in (d1, d2):
                t = types[DV[d]]
                if d == dp: ends.append(('P', None))
                elif t == 'U': ends.append(('C', cstates[d][tau]))
                else: ends.append(('B', (t[1], val[(d, tau)])))
            kinds = [k for k, _ in ends]
            if 'P' in kinds:
                other = ends[1] if kinds[0] == 'P' else ends[0]
                lam, par = other[1]
                up[tau] = (lam, (par + 1) % 2) if lam == tau else (lam, 0)   # parity matters only on cuts
                continue
            (l1, p1), (l2, p2) = ends[0][1], ends[1][1]
            if l1 != l2: return None
            if l1 == tau and (p1 + p2 + 1) % 2 != 1: return None
    return up


def main():
    maxit = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    t0 = time.time()
    bt = block_types()
    patches = []
    for ty in bt:
        for val in side_link_solutions(ty):
            patches.append((ty, val, b_val(val) - 2))
    print(f'{len(bt)} block types, {len(patches)} patches ({time.time() - t0:.0f}s)', flush=True)
    INF = 10 ** 9
    Val = {}
    def ckey(ty, val, d, st):     # key of the edge from C to its child at side d, as seen from the child
        cd = OPP[d]
        # region relative to child X = C + d, parent direction cd: [cd+perp, cd-perp, +perp, -perp]
        pv = PERP[d]; D = DV[d]
        rel = [pv, (-pv[0], -pv[1]), add(D, pv), sub(D, pv)]   # in C coords: C+perp, C-perp, X+perp, X-perp
        ex = val['ex'][d]
        if ex is not None:   # parts: (C-part, X-part) per corner; from the child's view the roles swap
            ex = (ex[0], tuple((xp, cp) for cp, xp in ex[1]))
        return (cd, val[(d, '/')], val[(d, '\\')], tuple(ty[p] for p in rel), st['/'], st['\\'], ex)
    def pkey(ty, val, dp, up):    # key of C's parent edge, as seen from C
        return (dp, val[(dp, '/')], val[(dp, '\\')], region_types(ty, dp), up['/'], up['\\'], val['ex'][dp])
    for it in range(maxit):
        new = {}
        for ty, val, exc in patches:
            udirs = [d for d in 'BRTL' if ty[DV[d]] == 'U']
            for dp in udirs:
                ch = [d for d in udirs if d != dp]
                opts = []
                for d in ch:
                    o = []
                    for s1 in STATES:
                        for s2 in STATES:
                            st = {'/': s1, '\\': s2}
                            v = Val.get(ckey(ty, val, d, st), INF)
                            if v < INF: o.append((st, v))
                    opts.append(o)
                for combo in itertools.product(*opts):
                    cs = {d: c[0] for d, c in zip(ch, combo)}
                    up = combine(ty, val, dp, cs)
                    if up is None: continue
                    tot = exc + sum(c[1] for c in combo)
                    k = pkey(ty, val, dp, up)
                    if tot < new.get(k, INF): new[k] = tot
        changed = new != Val
        Val = new
        print(f'iter {it}: {len(Val)} keys, min value {min(Val.values()) if Val else None} ({time.time() - t0:.0f}s)', flush=True)
        if not changed: break
    best = INF; arg = None
    for ty, val, exc in patches:
        udirs = [d for d in 'BRTL' if ty[DV[d]] == 'U']
        opts = []
        for d in udirs:
            o = []
            for s1 in STATES:
                for s2 in STATES:
                    st = {'/': s1, '\\': s2}
                    v = Val.get(ckey(ty, val, d, st), INF)
                    if v < INF: o.append((st, v))
            opts.append(o)
        for combo in itertools.product(*opts):
            cs = {d: c[0] for d, c in zip(udirs, combo)}
            if combine(ty, val, None, cs) is None: continue
            tot = exc + sum(c[1] for c in combo)
            if tot < best: best, arg = tot, (ty, val, combo)
    print(f'ROOT: minimum total excess over all tree islands = {best}', flush=True)
    print('argmin root patch:', arg)


if __name__ == '__main__':
    main()
