#!/usr/bin/env python3
"""Item (a), pure SAT version of side_end.py (decision, DRUP proof on UNSAT).

Periodic side cylinder P x (W + 2), hypothesis H (no crossing outside S*; quarters at depth 4..W-1 perfect),
no finite cycle (lazy cuts; every cut is valid for a forest). For each row in ROWS: end-zone flux E(r) != 0
mod 3 and no inward exception; with 'pass' also the up test value F(r) = 2 mod 3. Cardinality: S* crossings
per period <= P + KMAX (sequential counter). UNSAT: such a periodic strip needs excess > KMAX.
usage: side_sat.py P W ROWS KMAX [pass]     ROWS: comma list or 'all'
       side_sat.py P W all KMAX joint    JOINT test: is there a configuration with
       (#rows failing the strong test: E != 0 or F != 2 or exception) - (excess) >= KMAX + 1 ?
       UNSAT at KMAX = 0 means excess >= #strong failures for every P-periodic strip under H.
"""
import sys, time
from itertools import combinations
from pysat.solvers import Glucose4
from pysat.card import CardEnc, EncType
sys.path.insert(0, '..')
from check_frac_obstruction import crosses
from w3_quarters import tile, inside, quarters
from w3_flux import edge_flux, grid_term
from side_end import build, components, TAB


def main():
    P, W = int(sys.argv[1]), int(sys.argv[2])
    rows = list(range(P)) if sys.argv[3] == 'all' else [int(r) for r in sys.argv[3].split(',')]
    KMAX = int(sys.argv[4]); PASS = len(sys.argv) > 5 and sys.argv[5] == 'pass'
    cells, edges, lift, ends = build(P, W)
    vid = {e: i + 1 for i, e in enumerate(edges)}; top = [len(edges)]

    def new():
        top[0] += 1; return top[0]
    cl = []
    inc = {}
    for e in edges:
        for p in ends(e): inc.setdefault(p, []).append(vid[e])
    for p in cells:
        l = inc.get(p, [])
        for t in combinations(l, 3): cl.append([-x for x in t])
        if p[0] < W:
            for i in l: cl.append([j for j in l if j != i])
    t1 = lambda e: e[0][0] <= 1
    xs = []
    for e, f in combinations(edges, 2):
        if any(crosses(lift(e), lift(f, k)) for k in (-1, 0, 1)):
            if t1(e) and t1(f):
                c = new(); cl.append([-vid[e], -vid[f], c]); xs.append(c)
            else:
                cl.append([-vid[e], -vid[f]])
    tiles = {(e, k): tile(lift(e, k)) for e in edges for k in (-1, 0, 1)}
    for x in range(4, W):
        for y in range(P):
            for q, pt in quarters(x, y).items():
                cov = [vid[e] for e in edges if any(inside(tiles[(e, k)], pt) for k in (-1, 0, 1))]
                cl.append(cov)
                for a, b in combinations(cov, 2): cl.append([-a, -b])

    def mod3(const, coef, allowed):
        """clauses: (const + sum coef[e] x_e) mod 3 in allowed; one-hot chain."""
        s = [new(), new(), new()]
        cl.append([s[const % 3]]);
        for a in range(3):
            if a != const % 3: cl.append([-s[a]])
        for e, k in coef.items():
            k %= 3
            if k == 0: continue
            t = [new(), new(), new()]; xv = vid[e]
            for a in range(3):
                cl.append([-s[a], xv, t[a]]); cl.append([-s[a], -xv, t[(a + k) % 3]])
            for a, b in combinations(t, 2): cl.append([-a, -b])
            s = t
        for a in range(3):
            if allowed is not None and a not in allowed: cl.append([-s[a]])
        return s

    def canon(a_, b_):
        if a_[0] > b_[0]: a_, b_ = b_, a_
        return ((a_[0], a_[1] % P), (b_[0] - a_[0], b_[1] - a_[1]))
    JOINT = len(sys.argv) > 5 and sys.argv[5] == 'joint'
    if JOINT: rows = list(range(P))
    g = []
    for r in rows:
        const = 0; c = {}
        for x in range(2, W):
            st = ((2 * x - 1, 2 * r + 1), (2 * x + 1, 2 * r + 1))
            const += grid_term(st)
            for e in edges:
                for k in (-1, 0, 1):
                    fl = edge_flux(lift(e, k), st)
                    if fl: c[e] = c.get(e, 0) + fl
        if JOINT:   # g_r -> (E != 0) or (F != 2) or exception
            sE = mod3(const, c, None)
            fc = {}
            for (p, q), cf in TAB.items():
                e = canon((p[0], p[1] + r), (q[0], q[1] + r)); fc[e] = fc.get(e, 0) + cf
            sF = mod3(0, fc, None)
            xr = new(); ea, eb = vid[canon((0, r), (2, r + 1))], vid[canon((0, r + 1), (2, r))]
            cl.append([-xr, ea]); cl.append([-xr, eb])
            gr = new(); cl.append([-gr, sE[1], sE[2], sF[0], sF[1], xr]); g.append(gr)
            continue
        mod3(const, c, (1, 2))
        cl.append([-vid[canon((0, r), (2, r + 1))], -vid[canon((0, r + 1), (2, r))]])
        if PASS:
            fc = {}
            for (p, q), cf in TAB.items():
                e = canon((p[0], p[1] + r), (q[0], q[1] + r)); fc[e] = fc.get(e, 0) + cf
            mod3(0, fc, (2,))
    if JOINT:   # violation of: excess >= (#strong failures) + KMAX, i.e. sum g - (sum xs - P) >= KMAX + 1
        card = CardEnc.atleast(lits=g + [-x for x in xs], bound=KMAX + 1 + len(xs) - P, top_id=top[0],
                               encoding=EncType.totalizer)
    else:
        card = CardEnc.atmost(lits=xs, bound=P + KMAX, top_id=top[0], encoding=EncType.seqcounter)
    cl += card.clauses; top[0] = max(top[0], card.nv)
    t0 = time.time(); cuts = 0
    S = Glucose4(bootstrap_with=cl, with_proof=True)
    while True:
        ok = S.solve()
        if not ok: break
        model = set(l for l in S.get_model() if l > 0)
        sel = [e for e in edges if vid[e] in model]
        bad = [p for p, dy in components(sel, P, lift, ends) if dy == 0]
        if not bad: break
        for p in bad:
            cut = [-vid[e] for e in p]; S.add_clause(cut); cl.append(cut); cuts += 1
    tag = f'sideSAT_P{P}_W{W}_{sys.argv[3].replace(",", "-")}_K{KMAX}{"_pass" if PASS else ""}{"_joint" if JOINT else ""}'
    if ok:
        X = sum(1 for c in xs if c in model) - P
        G = sum(1 for x in g if x in model)
        print(f'{tag}: SAT excess {X} strong failures {G} (cuts {cuts}, {time.time() - t0:.0f}s)', flush=True)
        import json
        json.dump({'P': P, 'W': W, 'rows': rows, 'edges': [lift(e) for e in sel]}, open(tag + '.json', 'w'))
    else:
        with open(tag + '.cnf', 'w') as f:
            f.write(f'p cnf {top[0]} {len(cl)}\n')
            for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
        open(tag + '.drup', 'w').write('\n'.join(S.get_proof()) + '\n')
        print(f'{tag}: UNSAT (cuts {cuts}, {time.time() - t0:.0f}s; vars {top[0]}, clauses {len(cl)})', flush=True)


if __name__ == '__main__':
    main()
