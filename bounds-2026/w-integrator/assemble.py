#!/usr/bin/env python
"""Assemble full n x n closed knight's tours from periodic edge gadgets and verify them.

Usage (run from anywhere):
  .venv/bin/python w-integrator/assemble.py --bottom H16a --left VerticalEdge --off-L 0 64 66 68 70
  .venv/bin/python w-integrator/assemble.py --bottom '26 26 ...;23 36 ...;...' --left file.json 64 72

Templates: a name from NAMED below, a ';'-separated list of rows (rows top-first, board.js codes,
cells separated by spaces), or a path to a JSON file holding a list of row strings.
bottom template: P columns x D rows, local lane offset 0 (pairs start at local line c = 0 mod 8).
left template  : D columns x Q rows, local lane offset off_L (the Strip 'left' convention).

For each n: kt.board.build_skeleton tiles the bottom gadget on bottom + top (rotated 180) and the
left gadget on left + right (rotated 180), and kt.board.complete fills four Z x Z corner zones with
CP-SAT (AddCircuit, so the result is always one cycle).  If a zone size fails, the next one is tried.
Every tour is checked by kt.core.validate and by an independent walk; crossings are counted by
kt.core.num_crossings and (with --brute) by an independent all-pairs numpy counter.
Output: <out>/<tag>_n<n>.json  (board.js grid: list of n rows, each a list of 'ab' strings)
        <out>/<tag>_table.tsv  and a table on stdout with first differences per residue class.
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from kt.board import build_skeleton, build_general, complete, to_grid, fixed_paths, tpl_moves
from strands import pairing, region_check
from kt.core import validate, num_crossings, num_turns, MI, MJ
from kt import templates as T

NAMED = {
    'H16a': ['26 26 36 36 36 36 56 26', '23 36 36 36 13 23 23 23', '26 26 26 27 27 27 27 26', '67 67 67 67 67 67 67 67'],
    'H16b': ['46 46 56 56 56 26 46 46', '14 14 14 45 45 45 45 46', '05 15 15 15 15 05 05 05', '01 01 01 01 01 01 01 01'],
    'PaperHeel': T.Sequence1Opt,
    'VerticalEdge': T.VerticalEdge,
}

def load_tpl(s):
    if s in NAMED: return NAMED[s]
    if os.path.exists(s):
        return json.load(open(s))
    return [r.strip() for r in s.split(';')]

# ---------------- independent checks (do not use kt.core) ----------------
def walk_check(g):
    """Follow the tour from (0,0); True iff it is one closed knight's tour over all n*m cells."""
    h, w = len(g), len(g[0])
    def nbrs(i, j):
        return [(i + MI[int(k)], j + MJ[int(k)]) for k in g[i][j]]
    for i in range(h):
        for j in range(w):
            if len(g[i][j]) != 2: return False
            for (a, b) in nbrs(i, j):
                if not (0 <= a < h and 0 <= b < w) or (i, j) not in nbrs(a, b): return False
                if sorted((abs(a - i), abs(b - j))) != [1, 2]: return False
    prev, cur, steps = None, (0, 0), 0
    seen = set()
    while True:
        seen.add(cur)
        nx = nbrs(*cur)
        nxt = nx[0] if nx[0] != prev else nx[1]
        prev, cur = cur, nxt
        steps += 1
        if cur == (0, 0): break
        if cur in seen or steps > h * w: return False
    return steps == h * w and len(seen) == h * w

def brute_crossings(g):
    """All-pairs proper-intersection count with numpy (independent of kt.core.seg_cross)."""
    h, w = len(g), len(g[0])
    E = set()
    for i in range(h):
        for j in range(w):
            for k in g[i][j]:
                a = (i, j); b = (i + MI[int(k)], j + MJ[int(k)])
                E.add((a, b) if a < b else (b, a))
    S = np.array([[p[0], p[1], q[0], q[1]] for p, q in E], dtype=np.int64)
    P, Q = S[:, :2], S[:, 2:]
    total = 0
    def cross(o, a, b):  # z of (a-o) x (b-o), broadcast
        return (a[..., 0] - o[..., 0]) * (b[..., 1] - o[..., 1]) - (a[..., 1] - o[..., 1]) * (b[..., 0] - o[..., 0])
    B = 512
    for s0 in range(0, len(S), B):
        p1 = P[s0:s0 + B, None, :]; p2 = Q[s0:s0 + B, None, :]
        q1 = P[None, :, :]; q2 = Q[None, :, :]
        d1 = cross(p1, p2, q1); d2 = cross(p1, p2, q2)
        d3 = cross(q1, q2, p1); d4 = cross(q1, q2, p2)
        proper = (d1 * d2 < 0) & (d3 * d4 < 0)
        idx = np.arange(s0, min(s0 + B, len(S)))[:, None] < np.arange(len(S))[None, :]
        total += int((proper & idx).sum())
    return total

# ---------------- assembly ----------------
def phase_candidates(n, B, L, T_, R, Zmin=6, limit=None):
    """All phases (xb, xt, yl, yr) whose region profiles have no finite cycle and even cut counts,
    then no closed fixed cycle in the real skeleton.  Returns [(phases, profile)]."""
    pB, pL, pT, pR = pairing(B, 'bottom'), pairing(L, 'left'), pairing(T_, 'bottom'), pairing(R, 'left')
    for nm, p in (('bottom', pB), ('left', pL), ('top', pT), ('right', pR)):
        if p['bad'] or p['uncovered']:
            raise ValueError(f'{nm} template is not a valid gadget: {p["bad"]} uncovered={p["uncovered"]}')
    PB, PT = tpl_moves(B)[1], tpl_moves(T_)[1]
    QL, QR = tpl_moves(L)[2], tpl_moves(R)[2]
    out = []
    for xb in range(PB):
        for xt in range(PT):
            for yl in range(QL):
                for yr in range(QR):
                    ph = (xb, xt, yl, yr)
                    prof = region_check(pB, pL, pR, pT, n, ph)
                    if any(r['cycles'] or any(c % 2 for c in r['cuts']) for r in prof.values()):
                        continue
                    nb, free = build_general(n, B, L, T_, R, phases=ph, Z=Zmin)
                    paths, closed = fixed_paths(n, nb, free)
                    if closed: continue
                    out.append((ph, prof))
                    if limit and len(out) >= limit: return out
    return out

def assemble(n, bottom, left, off_L, Zs, time_limit, workers, turn_weight=0, log=print,
             top=None, right=None, phases='lane', tries=3, objective='crossings'):
    """phases: 'lane' (lane-design formula with off_L), 'auto' (search), or a tuple (xb, xt, yl, yr)."""
    top, right = top or bottom, right or left
    if phases == 'lane':
        cands = [None]
    elif phases == 'auto':
        cands = [ph for ph, _ in phase_candidates(n, bottom, left, top, right, Zmin=min(Zs))]
        if not cands: return None, 'no phase passes the strand checks'
        cands = cands[:tries]
    else:
        cands = [tuple(phases)]
    last, best = None, None
    for ph in cands:
        for Z in Zs:
            if 2 * Z > n: continue
            if ph is None: nb, free = build_skeleton(n, bottom, left, off_L=off_L, Z=Z)
            else: nb, free = build_general(n, bottom, left, top, right, phases=ph, Z=Z)
            w = dict(turn_weight=turn_weight) if objective == 'crossings' else dict(turn_weight=1000, crossing_weight=1)
            full, info = complete(n, nb, free, time_limit=time_limit, workers=workers, **w)
            if full is None:
                log(f'  n={n} phases={ph} Z={Z}: {info}'); last = info; continue
            g = to_grid(n, full)
            info['Z'] = Z; info['phases'] = ph
            key = (num_crossings(g), num_turns(g)) if objective == 'crossings' else (num_turns(g), num_crossings(g))
            if best is None or key < best[0]: best = (key, g, info)
            break
    return (best[1], best[2]) if best else (None, last)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('ns', type=int, nargs='+')
    ap.add_argument('--bottom', default='H16a')
    ap.add_argument('--left', default='VerticalEdge')
    ap.add_argument('--off-L', type=int, default=0)
    ap.add_argument('--top', default=None, help='bottom-type template placed rotated on top (default: --bottom)')
    ap.add_argument('--right', default=None, help='left-type template placed rotated on the right (default: --left)')
    ap.add_argument('--phases', default='lane', help="'lane' (formula with --off-L), 'auto' (strand search), or xb,xt,yl,yr")
    ap.add_argument('--objective', default='crossings', choices=['crossings', 'turns'], help='corner objective: which count first')
    ap.add_argument('--tries', type=int, default=3, help='auto: number of phase candidates to complete (best kept)')
    ap.add_argument('--Z', default='6,7,8,10,12', help='zone sizes to try in order')
    ap.add_argument('--time', type=float, default=60, help='CP-SAT seconds per completion')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--turn-weight', type=int, default=0, help='turn weight vs 1000 per crossing')
    ap.add_argument('--brute', action='store_true', help='also count crossings by brute force')
    ap.add_argument('--tag', default=None)
    ap.add_argument('--out', default=os.path.join(HERE, 'tours'))
    a = ap.parse_args()
    bottom, left = load_tpl(a.bottom), load_tpl(a.left)
    top = load_tpl(a.top) if a.top else None
    right = load_tpl(a.right) if a.right else None
    phases = a.phases if a.phases in ('lane', 'auto') else tuple(int(v) for v in a.phases.split(','))
    nm = lambda v, d: v if v in NAMED else d
    tag = a.tag or (f'{nm(a.bottom, "B")}_{nm(a.left, "L")}_off{a.off_L}' if a.phases == 'lane' and not (top or right)
                    else f'{nm(a.bottom, "B")}_{nm(a.left, "L")}_{nm(a.top or a.bottom, "T")}_{nm(a.right or a.left, "R")}_{a.phases.replace(",", "")}')
    os.makedirs(a.out, exist_ok=True)
    Zs = [int(z) for z in a.Z.split(',')]
    rows = []
    print('n\tvalid\tX\tT\tZ\tstatus\tcornerX\tbound\tsecs\tphases' + ('\tXbrute' if a.brute else ''), flush=True)
    for n in a.ns:
        t0 = time.time()
        g, info = assemble(n, bottom, left, a.off_L, Zs, a.time, a.workers, a.turn_weight,
                           log=lambda s: print(s, file=sys.stderr, flush=True),
                           top=top, right=right, phases=phases, tries=a.tries, objective=a.objective)
        if g is None:
            print(f'{n}\tFAIL\t-\t-\t-\t{info}', flush=True); continue
        ok = validate(g) and walk_check(g)
        X, Tn = num_crossings(g), num_turns(g)
        row = dict(n=n, valid=ok, X=X, T=Tn, **info)
        line = f"{n}\t{ok}\t{X}\t{Tn}\t{info['Z']}\t{info['status']}\t{info['corner_obj']:.0f}\t{info['bound']:.0f}\t{time.time() - t0:.0f}\t{info['phases']}"
        if a.brute:
            row['Xbrute'] = brute_crossings(g); line += f"\t{row['Xbrute']}"
        print(line, flush=True)
        rows.append(row)
        if ok:
            json.dump(dict(n=n, bottom=bottom, left=left, top=top or bottom, right=right or left, off_L=a.off_L, crossings=X, turns=Tn,
                           info={k: v for k, v in info.items()}, tour=g),
                      open(os.path.join(a.out, f'{tag}_n{n}.json'), 'w'))
    # first differences per residue class mod 8
    print('\nper residue class (n mod 8): differences per +8 in n')
    with open(os.path.join(a.out, f'{tag}_table.tsv'), 'a') as f:
        for r in rows:
            f.write('\t'.join(str(r[k]) for k in ('n', 'valid', 'X', 'T', 'Z', 'status', 'corner_obj', 'bound')) + '\n')
    for res in range(0, 8, 2):
        rs = sorted((r for r in rows if r['n'] % 8 == res and r['valid']), key=lambda r: r['n'])
        if len(rs) < 2: continue
        dif = [((b['X'] - a_['X']) / (b['n'] - a_['n']), (b['T'] - a_['T']) / (b['n'] - a_['n']))
               for a_, b in zip(rs, rs[1:])]
        print(f'  res {res}: n={[r["n"] for r in rs]} X={[r["X"] for r in rs]} T={[r["T"] for r in rs]} '
              f'dX/dn={[d[0] for d in dif]} dT/dn={[d[1] for d in dif]}')

if __name__ == '__main__':
    main()
