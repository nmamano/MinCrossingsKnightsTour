#!/usr/bin/env python3
"""F1 pilot (R4): can deficient-pass end rows occur without strip excess, when deep defects are ALLOWED?

Periodic side cylinder P x (W + 2), side at x = 0, exact degree 2 for x < W, halo <= 2, lazy no-finite-cycle cuts.
ALL crossings allowed (no hypothesis H). Strip excess = (pairs with both edges touching column <= 1) - P.
Row indicator g_r (free, solver maximises) implies one of:
  (i) the up test fails at r (F(r) != 2 mod 3) or the exception pair is present at r;
  (ii) DEFICIENT-PASS end: E(r) != 0 mod 3 (flux over the dual steps crossing x = 2, 3, 4 on row line r + 1/2),
       squares (4, r) .. (W - 1, r) perfect (good middle), and at most ONE payable bad quarter in squares (1..3, r).
       Payable = m = 0, or m >= 3, or m = 2 with its covering pair NOT an S* pair with a two-quarter overlap.
Search for a violation of   excess >= sum_r g_r + KMAX   (KMAX = 0: rate 1).  UNSAT = no periodic violation.
usage: side_f1.py P W [KMAX]
"""
import sys, time, json
from itertools import combinations
from pysat.solvers import Glucose4
from pysat.card import CardEnc, EncType
sys.path.insert(0, '..')
from check_frac_obstruction import crosses
from w3_quarters import tile, inside, quarters
from w3_flux import edge_flux, grid_term
from side_end import build, components, TAB


def main():
    P, W = int(sys.argv[1]), int(sys.argv[2]); KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    cells, edges, lift, ends = build(P, W)
    vid = {e: i + 1 for i, e in enumerate(edges)}; top = [len(edges)]
    def new():
        top[0] += 1; return top[0]
    cl = []; inc = {}
    for e in edges:
        for p in ends(e): inc.setdefault(p, []).append(vid[e])
    for p in cells:
        l = inc.get(p, [])
        for t in combinations(l, 3): cl.append([-x for x in t])
        if p[0] < W:
            for i in l: cl.append([j for j in l if j != i])
    t1 = lambda e: e[0][0] <= 1
    tiles = {(e, k): tile(lift(e, k)) for e in edges for k in (-1, 0, 1)}
    cover = {}
    for x in range(W):
        for y in range(P):
            for q, pt in quarters(x, y).items():
                cover[(x, y, q)] = [e for e in edges if any(inside(tiles[(e, k)], pt) for k in (-1, 0, 1))]
    qset = {}
    for key, l in cover.items():
        for e in l: qset.setdefault(e, set()).add(key)
    xs = []; spair2 = set()
    for e, f in combinations(edges, 2):
        if any(crosses(lift(e), lift(f, k)) for k in (-1, 0, 1)):
            if t1(e) and t1(f):
                c = new(); cl.append([-vid[e], -vid[f], c]); xs.append(c)
                if len(qset.get(e, set()) & qset.get(f, set())) == 2: spair2.add((e, f)); spair2.add((f, e))

    def mod3(const, coef):
        s = [new(), new(), new()]
        for a in range(3): cl.append([s[a]] if a == const % 3 else [-s[a]])
        for e, k in coef.items():
            k %= 3
            if k == 0: continue
            t = [new(), new(), new()]; xv = vid[e]
            for a in range(3):
                cl.append([-s[a], xv, t[a]]); cl.append([-s[a], -xv, t[(a + k) % 3]])
            for a, b in combinations(t, 2): cl.append([-a, -b])
            s = t
        return s

    def canon(a_, b_):
        if a_[0] > b_[0]: a_, b_ = b_, a_
        return ((a_[0], a_[1] % P), (b_[0] - a_[0], b_[1] - a_[1]))
    g = []
    for r in range(P):
        const = 0; c = {}
        for x in range(2, 5):
            st = ((2 * x - 1, 2 * r + 1), (2 * x + 1, 2 * r + 1))
            const += grid_term(st)
            for e in edges:
                for k in (-1, 0, 1):
                    fl = edge_flux(lift(e, k), st)
                    if fl: c[e] = c.get(e, 0) + fl
        sE = mod3(const, c)
        fc = {}
        for (p, q), cf in TAB.items():
            e = canon((p[0], p[1] + r), (q[0], q[1] + r)); fc[e] = fc.get(e, 0) + cf
        sF = mod3(0, fc)
        ea, eb = vid[canon((0, r), (2, r + 1))], vid[canon((0, r + 1), (2, r))]
        xr = new(); cl += [[-xr, ea], [-xr, eb]]
        dr = new()                                   # deficient-pass end at r
        cl.append([-dr, sE[1], sE[2]])               # E != 0
        for x in range(4, W):                        # good middle
            for q in 'brtl':
                cov = [vid[e] for e in cover[(x, r, q)]]
                cl.append([-dr] + cov)
                for a, b in combinations(cov, 2): cl.append([-dr, -a, -b])
        pays = []
        for x in range(1, 4):
            for q in 'brtl':
                cov = cover[(x, r, q)]; pq = new(); pays.append(pq)
                cl.append([vid[e] for e in cov] + [pq])                       # m = 0
                for a, b, d in combinations(cov, 3): cl.append([-vid[a], -vid[b], -vid[d], pq])   # m >= 3
                for a, b in combinations(cov, 2):
                    if (a, b) not in spair2: cl.append([-vid[a], -vid[b], pq])  # m = 2, payable pair
        card = CardEnc.atmost(lits=pays, bound=1, top_id=top[0], encoding=EncType.seqcounter)
        top[0] = max(top[0], card.nv)
        for cc in card.clauses: cl.append([-dr] + cc)
        gr = new(); cl.append([-gr, sF[0], sF[1], xr, dr]); g.append(gr)
    card = CardEnc.atleast(lits=g + [-x for x in xs], bound=KMAX + 1 + len(xs) - P, top_id=top[0],
                           encoding=EncType.totalizer)
    cl += card.clauses; top[0] = max(top[0], card.nv)
    t0 = time.time(); cuts = 0
    S = Glucose4(bootstrap_with=cl, with_proof=False)
    while True:
        ok = S.solve()
        if not ok: break
        model = set(l for l in S.get_model() if l > 0)
        sel = [e for e in edges if vid[e] in model]
        bad = [p for p, dy in components(sel, P, lift, ends) if dy == 0]
        if not bad: break
        for p in bad: S.add_clause([-vid[e] for e in p]); cuts += 1
    tag = f'sideF1_P{P}_W{W}_K{KMAX}'
    if ok:
        X = sum(1 for c in xs if c in model) - P; G = sum(1 for x in g if x in model)
        nonS = sum(1 for e, f in combinations(sel, 2) if any(crosses(lift(e), lift(f, k)) for k in (-1, 0, 1))) - X - P
        print(f'{tag}: SAT (violation) strip excess {X}, g rows {G}, non-S* crossings {nonS} (cuts {cuts}, {time.time() - t0:.0f}s)', flush=True)
        json.dump({'P': P, 'W': W, 'rows': [], 'edges': [lift(e) for e in sel]}, open(tag + '.json', 'w'))
    else:
        print(f'{tag}: UNSAT (cuts {cuts}, {time.time() - t0:.0f}s)', flush=True)


if __name__ == '__main__':
    main()
