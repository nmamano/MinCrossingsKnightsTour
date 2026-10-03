#!/usr/bin/env python
"""Region-separable combo search.  For a menu of gadgets, find all (B, T, L, R) with phases
(xb, xt, yl, yr) such that BL(B, L | xb, yl), MID(L, R | yl, yr), TR(R, T | yr, xt) all pass
(no finite cycle, even cuts).  Ranks by slope; checks n in --ns (default 96,98,100,102).
Usage: combos2.py menu.json [--ns 96,98,100,102] [--top 40]"""
import argparse, json, os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from strands import pairing, expand, union_profile
from kt.board import tpl_moves
from assemble import NAMED

def ok(p1, s1, g1, p2, s2, g2, lo, hi):
    pr = union_profile(expand(p1['pairs'], p1['cper'], s1, g1, lo, hi), expand(p2['pairs'], p2['cper'], s2, g2, lo, hi), lo, hi)
    return None if pr['cycles'] or any(c % 2 for c in pr['cuts']) else pr['strands']

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('menu'); ap.add_argument('--ns', default='96,98,100,102')
    ap.add_argument('--top', type=int, default=40); ap.add_argument('--no-builtin', action='store_true')
    ap.add_argument('--metric', default='X', choices=['X', 'T'])
    a = ap.parse_args()
    G = json.load(open(a.menu))
    if not a.no_builtin:
        for nm, X, T_ in (('H16a', 16, 25), ('VerticalEdge', 10, 8)):
            G.append(dict(name=nm, kind='left' if nm == 'VerticalEdge' else 'bottom', tpl=NAMED[nm], X=X, T=T_))
    for g in G:
        mv, W, H = tpl_moves(g['tpl']); g['per'] = W if g['kind'] == 'bottom' else H
        g['p'] = pairing(g['tpl'], g['kind']); g['unit'] = g[a.metric] / g['per']
    Bs = [g for g in G if g['kind'] == 'bottom']; Ls = [g for g in G if g['kind'] == 'left']
    ns = [int(v) for v in a.ns.split(',')]
    found = {}
    for n in ns:
        N = 3 * (n - 1); gm = 12
        BL = {}; MID = {}; TR = {}
        for B in Bs:
            for L in Ls:
                BL[B['name'], L['name']] = {(xb, yl): s for xb in range(B['per']) for yl in range(L['per'])
                    if (s := ok(B['p'], xb, 1, L['p'], 2 * yl, 1, gm, n - gm)) is not None}
        for L in Ls:
            for R in Ls:
                MID[L['name'], R['name']] = {(yl, yr): s for yl in range(L['per']) for yr in range(R['per'])
                    if (s := ok(L['p'], 2 * yl, 1, R['p'], n - 1 + 2 * yr, -1, n + gm, 2 * n - gm)) is not None}
        for R in Ls:
            for T in Bs:
                TR[R['name'], T['name']] = {(yr, xt): s for yr in range(R['per']) for xt in range(T['per'])
                    if (s := ok(R['p'], n - 1 + 2 * yr, -1, T['p'], xt + 2 * (n - 1), -1, 2 * n + gm, N - gm)) is not None}
        for B, T, L, R in itertools.product(Bs, Bs, Ls, Ls):
            bl, md, tr = BL[B['name'], L['name']], MID[L['name'], R['name']], TR[R['name'], T['name']]
            if not (bl and md and tr): continue
            sol = None
            for (xb, yl), s1 in bl.items():
                for (yl2, yr), s2 in md.items():
                    if yl2 != yl: continue
                    for (yr2, xt), s3 in tr.items():
                        if yr2 == yr: sol = ((xb, xt, yl, yr), (s1, s2, s3)); break
                    if sol: break
                if sol: break
            if sol:
                key = (B['name'], T['name'], L['name'], R['name'])
                found.setdefault(key, (B['unit'] + T['unit'] + L['unit'] + R['unit'], {}))[1][n] = sol
    rows = sorted(found.items(), key=lambda kv: kv[1][0])
    print(f'{len(rows)} feasible combos (for at least one n in {ns})')
    for key, (slope, byn) in rows[:a.top]:
        print(f'slope {slope:.3f} B={key[0]} T={key[1]} L={key[2]} R={key[3]}  ' +
              '  '.join(f'n={n}:{byn.get(n)}' for n in ns))

if __name__ == '__main__':
    main()
