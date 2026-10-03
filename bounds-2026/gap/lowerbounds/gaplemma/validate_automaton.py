#!/usr/bin/env python3
"""End-to-end soundness test of tree_automaton.py on real configurations.

Real configurations: SAT witnesses of tree_islands.sat_check (exact degree 2 on a point box, all island conditions,
uniform '\\' labels) with a loose bad-quarter bound (env SLACK). For each witness and each choice of root:
(a) every node's real patch (block types, 8 side links, cross links, partial degree sums) is among the automaton's
    enumerated patches for those types; (b) every parent-child pair has equal keys (parent's ckey = child's pkey);
(c) all chain completions pass. A failure would mean the automaton misses real trees (unsound).
usage: SLACK=6 validate_automaton.py SMAX
"""
import sys, os
import tree_islands as TI
import tree_automaton as A

SMAX = int(sys.argv[1]); NSOL = int(os.environ.get('NSOL', '20'))
cache = {}


def patch_set(ty):
    k = tuple(sorted(ty.items()))
    if k not in cache:
        cache[k] = [v for v in A.side_link_solutions(ty)]
    return cache[k]


def real_patch(Uset, C, on):
    ty = {}
    for off in A.BLOCK + [(0, 0)]:
        Q = A.add(C, off)
        if off == (0, 0): ty[off] = 'U'; continue
        if 0 in off and abs(off[0]) + abs(off[1]) == 1:
            ty[off] = 'U' if Q in Uset else 'N\\'
        else:
            a, b = A.add(C, (off[0], 0)), A.add(C, (0, off[1]))
            if a in Uset or b in Uset: ty[off] = 'U' if Q in Uset else 'N\\'
            else: ty[off] = 'O'
    # values in C-relative coordinates: edge e (relative) -> on(e + C)
    def val_rel(e): return on(tuple(sorted((A.add(e[0], C), A.add(e[1], C)))))
    val = {(d, sg): val_rel(A.link((0, 0), d, sg)) for d in 'BRTL' for sg in '/\\'}
    ex = {}
    for d in 'BRTL':
        if ty[A.DV[d]] != 'U': ex[d] = None; continue
        X = A.DV[d]; pv = A.PERP[d]; mv = (-pv[0], -pv[1])
        cross = []
        for w in (pv, mv):
            P1, P2 = A.add((0, 0), w), A.add(X, w)
            dd = [k for k, vv in A.DV.items() if vv == A.sub(P2, P1)][0]
            for sg in '/\\': cross.append(val_rel(A.link(P1, dd, sg)))
        parts = []
        for v in sorted(set(A.sq_pts((0, 0))) & set(A.sq_pts(X))):
            blk = [A.sub(v, (a, b)) for a in (0, 1) for b in (0, 1)]
            cp = xp = 0
            for e in A.edges_at(v):
                es, sg = A.edge_side(e)
                owner = [q for q in A.side_squares(es) if q in blk][0]
                if ty.get(owner, 'O') == 'O': continue
                if owner in ((0, 0), pv, mv): cp += val_rel(e)
                else: xp += val_rel(e)
            parts.append((cp, xp))
        ex[d] = (tuple(cross), tuple(parts))
    val['ex'] = ex
    return ty, val


def main():
    nw = nchk = 0; bad = []
    for s in range(1, SMAX + 1):
        for P in sorted(TI.tree_polyominoes(s)[s]):
            U = [(x + 10, y + 10) for x, y in P]; Uset = set(U)
            bs, labs = TI.labellings(U)
            for lab, cuts in labs:
              if set(lab.values()) != {'\\'}: continue
              blocks = []
              near = {(x + a, y + b) for (x, y) in list(U) + list(lab) for a in (-1, 0, 1, 2) for b in (-1, 0, 1, 2)}
              for rep in range(NSOL):
                r, model, _, edges, vid = TI.sat_check(U, lab, cuts, block=blocks)
                if not r: break
                nw += 1
                ms = set(l for l in model if l > 0)
                rel = [vid[e] for e in edges if e[0] in near or e[1] in near]
                blocks.append([-x if x in ms else x for x in rel])
                on = lambda e: int(e in vid and vid[e] in ms)
                pt = {C: real_patch(Uset, C, on) for C in U}
                for C, (ty, val) in pt.items():
                    if val not in patch_set(ty): bad.append(('patch', s, C)); continue
                for root in U:
                    # rooted tree
                    par = {root: None}; order = [root]
                    for C in order:
                        for d in 'BRTL':
                            X = A.add(C, A.DV[d])
                            if X in Uset and X not in par: par[X] = (C, d); order.append(X)
                    up = {}
                    for C in reversed(order):
                        ty, val = pt[C]
                        dp = None if par[C] is None else A.OPP[par[C][1]]
                        cs = {}
                        for d in 'BRTL':
                            X = A.add(C, A.DV[d])
                            if X in Uset and d != dp: cs[d] = up[X]
                        u = A.combine(ty, val, dp, cs)
                        if u is None: bad.append(('chain', s, root, C)); break
                        up[C] = u
                        nchk += 1
                    # key equality
                    for C in order:
                        if par[C] is None: continue
                        Pq, d = par[C]
                        tyP, valP = pt[Pq]; tyC, valC = pt[C]
                        dp = A.OPP[d]
                        pk = (dp, valC[(dp, '/')], valC[(dp, '\\')], A.region_types(tyC, dp), up[C]['/'], up[C]['\\'], valC['ex'][dp])
                        ex = valP['ex'][d]; ex = (ex[0], tuple((xp, cp) for cp, xp in ex[1]))
                        pv = A.PERP[d]; D = A.DV[d]
                        rel = [pv, (-pv[0], -pv[1]), A.add(D, pv), A.sub(D, pv)]
                        ck = (A.OPP[d], valP[(d, '/')], valP[(d, '\\')], tuple(tyP[p] for p in rel), up[C]['/'], up[C]['\\'], ex)
                        if pk != ck: bad.append(('key', s, root, C, pk, ck))
        print(f's={s}: witnesses {nw}, node checks {nchk}, failures {len(bad)}', flush=True)
    for b in bad[:5]: print('FAIL', b)


if __name__ == '__main__':
    main()
