#!/usr/bin/env python
"""Precompute every demo tour (KT Integrator, 2026-10-02).

For each construction and each supported even n: build the tour with the verified regeneration
recipe (no new solve), check it (kt.core.validate + assemble.walk_check), count crossings and turns
with kt.core, and write demo/data/<key>_n<n>.json. A summary goes to demo/data/index.json.

Cell encoding: one character per cell, row-major, row 0 = top row (board.js grid g[i][j]).
The character is ALPHA[8*a + b] where a <= b are the two board.js move codes of the cell.
'solver' = flat indices (i*n + j) of the cells that a CP-SAT completion filled (corner zones,
fold windows and corridors); every other cell comes from a fixed template or field.

Usage: .venv/bin/python demo/build_data.py [--keys paper,H16a,TT16,FOLD] [--nmin 48] [--nmax 200]
       [--jobs 2] [--brute 96,120]   (brute = also run the O(E^2) independent count at these n)
"""
import argparse, json, os, sys
from fractions import Fraction
from multiprocessing import Pool

DEMO = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DEMO)
WI = os.path.join(ROOT, 'w-integrator')
sys.path.insert(0, ROOT); sys.path.insert(0, WI)
OUT = os.path.join(DEMO, 'data')
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'

# supported n (even): first n of each construction, the period of its reuse argument, and depths
SPEC = {
    'paper': dict(nmin=48, period=8, bandB=4, bandL=2, Z=6),
    'H16a': dict(nmin=48, period=24, bandB=4, bandL=2, Z=6),
    'TT16': dict(nmin=48, period=8, bandB=4, bandL=2, Z=6),
    'FOLD': dict(nmin=96, period=24),
    'orig': dict(nmin=48, period=8, bandB=4, bandL=2, Z=6),
    'heel21': dict(nmin=48, period=8, bandB=4, bandL=2, Z=6),
    'P40': dict(nmin=48, period=40, bandB=4, bandL=2, Z=6),
    'LF4': dict(nmin=96, period=48, bandB=4, bandL=2, Z=6),
    'T18': dict(nmin=48, period=24, bandB=4, bandL=2, Z=6),
}


def corner_cells(n, Z):
    out = []
    for cx, cy in ((0, 0), (n - Z, 0), (0, n - Z), (n - Z, n - Z)):
        out += [(cx + x, cy + y) for x in range(Z) for y in range(Z)]
    return out


def gen_alg1(n, heel=None, block=None):
    """Algorithm 1 (kt.gentour) with a given heel and optional block. Two corner cases put one heel at a
    corner: top-left case 1 (n = 2 mod 4) and bottom-right case 1 (n = 6 mod 8). The optimised heels do
    not fit there, so that corner piece is the board.js default heel (an O(1) change)."""
    from kt.gentour import gen_tour
    from kt import templates as T
    heel = heel or T.Sequence1Opt
    g = gen_tour(n, n, heel=heel, block=block)
    g2 = gen_tour(n, n, heel=T.Sequence1Default, block=block)
    if heel is not T.Sequence1Default:
        if (3 - n) % 4 == 1:
            for i in range(4):
                g[i][:8] = g2[i][:8]
        if (n // 2 + 2) % 4 == 1:
            for i in range(n - 4, n):
                g[i][n - 8:] = g2[i][n - 8:]
    return g, []


def gen_paper(n):      # paper crossing heel (28 crossings): 12n
    return gen_alg1(n)


def gen_orig(n):       # formation heel of the original demo (32 crossings): 13n crossings, 9.5n turns
    from kt import templates as T
    return gen_alg1(n, heel=T.Sequence1Default)


def gen_heel21(n):     # paper turn heel (21 turns, 31 crossings), rebuilt by w-integrator/heel21.py: 9.25n turns
    tpl = json.load(open(os.path.join(WI, 'gadgets', 'heel21.json')))['template']
    return gen_alg1(n, heel=tpl)


def gen_P40(n):        # Shisheng Li 4x40 block on the bottom and top bands: 11.5n
    from kt import templates as T
    return gen_alg1(n, block=(T.SequenceP40, 40))


def gen_LF4(n):        # lane-free LF4 (w-turnstheory/PROOFS.md section 5): 343n/48
    from kt.board import to_grid
    from periodic import Combo
    r = (n - 96) % 48
    d = json.load(open(os.path.join(ROOT, 'w-turnstheory', 'lf-corners', f'LF4_res{r:02d}.json')))
    assert n >= d['n0'] and (n - d['n0']) % 48 == 0
    C = Combo(d['bottom'], d['top'], d['left'], d['right'], tuple(d['phases']), d['Z'])
    return to_grid(n, C.apply(n, d['zones'])), corner_cells(n, d['Z'])


def gen_T18(n):        # T18 heel with the paper's VerticalEdge (period24.py, lane rule): 8.5n turns
    import period24
    from kt.board import to_grid
    d = json.load(open(os.path.join(WI, 'corners', f'T18_res{n % 24:02d}.json')))
    assert n >= d['n0'] and (n - d['n0']) % 24 == 0
    period24.B, period24.L = d['bottom'], d['left']
    try:
        return to_grid(n, period24.apply_zone(n, d['zones'])), corner_cells(n, 6)
    finally:
        period24.B, period24.L = period24.NAMED['H16a'], period24.NAMED['VerticalEdge']


def gen_H16a(n):
    import period24
    d = json.load(open(os.path.join(WI, 'corners', f'H16a_VE_res{n % 24:02d}.json')))
    assert d['bottom'] == period24.B and d['left'] == period24.L
    assert n >= d['n0'] and (n - d['n0']) % 24 == 0
    from kt.board import to_grid
    return to_grid(n, period24.apply_zone(n, d['zones'])), corner_cells(n, 6)


def gen_TT16(n):
    from kt.board import to_grid
    if n < 56:   # n = 48..54 were solved directly (no reuse base below 56)
        g = json.load(open(os.path.join(WI, 'tours', f'TT16_n{n}.json')))['tour']
        return g, corner_cells(n, 6)
    from periodic import Combo
    from assemble import load_tpl
    d = json.load(open(os.path.join(WI, 'corners', f'TT16_res{n % 8:02d}.json')))
    assert n >= d['n0'] and (n - d['n0']) % 8 == 0
    C = Combo(d['bottom'], d['top'], d['left'], d['right'], tuple(d['phases']), d['Z'])
    return to_grid(n, C.apply(n, d['zones'])), corner_cells(n, d['Z'])


def gen_FOLD(n):
    """fold_period.py transplant (step 24) from the base at n0 = 96 + (n - 96) % 24."""
    from fold_assemble import setup, edges_to_nb
    from fold_period import rotv, mid_cells, components, Rot
    from kt.board import to_grid
    n0 = 96 + (n - 96) % 24
    d = json.load(open(os.path.join(WI, 'corners', f'FOLD24_base_n{n0}.json')))
    p, lo, band, rad = d['p'], d['lo'], d['band'], d['rad']
    tpl = {}
    for k, v in d['template'].items():
        r, rest = k.split(':'); a, b = rest.split(',')
        tpl[(int(r), int(a), int(b))] = [tuple(x) for x in v]
    content0 = []
    for comp in d['components']:
        cells = {tuple(map(int, q.split(','))): [tuple(x) for x in v] for q, v in comp['cells'].items()}
        content0.append((tuple(comp['offset']), frozenset(cells), cells))
    E, free, info = setup(n, rad, {}, 4, band=band)
    full = {c: set(v) for c, v in edges_to_nb(n, E).items()}
    mid = mid_cells(n, lo, band, inner=3)
    hi = n // 2 - lo - 3
    for r in range(4):
        for x in range(lo + 3, hi):
            for y in range(x + 1 - band, x + 1 + band + 1):
                c = Rot((x, y), n, r)
                ds = tpl[(r, (x - lo) % p, y - x)]
                full[c] = {(c[0] + dd[0], c[1] + dd[1]) for dd in (rotv(dd, r) for dd in ds)}
    comps = components(free - mid)
    assert len(comps) == len(content0), (len(comps), len(content0))
    used = set()
    for off, shape, cells in comps:
        best = min((j for j, b in enumerate(content0) if b[1] == shape and j not in used),
                   key=lambda j: abs(off[0] / n - content0[j][0][0] / n0) + abs(off[1] / n - content0[j][0][1] / n0))
        used.add(best)
        for q, ds in content0[best][2].items():
            c = (off[0] + q[0], off[1] + q[1])
            full[c] = {(c[0] + dd[0], c[1] + dd[1]) for dd in ds}
    return to_grid(n, full), sorted(free)


GEN = dict(paper=gen_paper, H16a=gen_H16a, TT16=gen_TT16, FOLD=gen_FOLD, orig=gen_orig, heel21=gen_heel21,
           P40=gen_P40, LF4=gen_LF4, T18=gen_T18)


def encode(g):
    s = []
    for row in g:
        for c in row:
            a, b = sorted(int(ch) for ch in c)
            s.append(ALPHA[8 * a + b])
    return ''.join(s)


def job(arg):
    key, n, brute = arg
    from kt.core import validate, num_crossings, num_turns
    from assemble import walk_check, brute_crossings
    g, solver_xy = GEN[key](n)
    ok = bool(validate(g) and walk_check(g))
    X, T = num_crossings(g), num_turns(g)
    Xb = brute_crossings(g) if brute else None
    solver = sorted((n - 1 - y) * n + x for (x, y) in solver_xy)
    rec = dict(key=key, n=n, valid=ok, crossings=X, turns=T, brute_crossings=Xb, cells=encode(g), solver=solver)
    json.dump(rec, open(os.path.join(OUT, f'{key}_n{n}.json'), 'w'), separators=(',', ':'))
    return dict(key=key, n=n, valid=ok, crossings=X, turns=T, brute_crossings=Xb)


def slopes(rows, period):
    """exact slope per metric from n -> n + period (same residue); returns (Fraction or None) per metric."""
    by = {r['n']: r for r in rows}
    out = {}
    for m in ('crossings', 'turns'):
        vals = {Fraction(by[n + period][m] - by[n][m], period) for n in by if n + period in by}
        out[m] = vals
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--keys', default='orig,paper,heel21,P40,H16a,LF4,FOLD,T18,TT16')
    ap.add_argument('--nmin', type=int, default=48); ap.add_argument('--nmax', type=int, default=200)
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--brute', default='96,120')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    keys = a.keys.split(',')
    brute = {int(v) for v in a.brute.split(',') if v}
    tasks = [(k, n, n in brute) for k in keys for n in range(max(a.nmin, SPEC[k]['nmin']), a.nmax + 1, 2)]
    idx_path = os.path.join(OUT, 'summary.json')
    summary = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
    with Pool(a.jobs) as pool:
        for r in pool.imap_unordered(job, tasks):
            print(f"{r['key']:>5} n={r['n']:>3} valid={r['valid']} X={r['crossings']} T={r['turns']}"
                  + (f" brute={r['brute_crossings']}" if r['brute_crossings'] is not None else ''), flush=True)
            summary.setdefault(r['key'], {})[str(r['n'])] = r
    json.dump(summary, open(idx_path, 'w'), indent=1)
    for k in keys:
        rows = list(summary[k].values())
        bad = [r['n'] for r in rows if not r['valid']]
        bmis = [r['n'] for r in rows if r['brute_crossings'] is not None and r['brute_crossings'] != r['crossings']]
        print(f'{k}: {len(rows)} tours, invalid {bad}, brute mismatches {bmis}, '
              f'slopes per {SPEC[k]["period"]}: { {m: sorted(str(v) for v in s) for m, s in slopes(rows, SPEC[k]["period"]).items()} }')


if __name__ == '__main__':
    main()
