#!/usr/bin/env python
"""Rank gadget combinations for full tours by predicted crossing slope, using the strand calculus.

Input: a JSON file with a list of gadgets {"name", "kind": "bottom"|"left", "tpl": [rows], "X": per
period crossings, "T": per period turns (optional)}.  Built-in names from assemble.NAMED are added.
For every combination (bottom B, top T = bottom-type, left L, right R = left-type):
  slope_X = X_B/P_B + X_T/P_T + X_L/Q_L + X_R/Q_R   (crossings per unit of n, corners excluded)
and the combination is feasible at size n if some phases pass the region rules (no finite cycle,
even cut counts in BL, MID, TR).  Output: table sorted by slope, feasibility for n and n+2.
Usage: .venv/bin/python w-integrator/combos.py menu.json [--n 96] [--top 20]
"""
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from strands import pairing, region_check, parity
from assemble import NAMED
from kt.board import tpl_moves

def feasible_phases(pB, pL, pT, pR, PB, PT, QL, QR, n, first=True):
    out = []
    for xb in range(PB):
        for xt in range(PT):
            for yl in range(QL):
                for yr in range(QR):
                    prof = region_check(pB, pL, pR, pT, n, (xb, xt, yl, yr))
                    if any(r['cycles'] or any(c % 2 for c in r['cuts']) for r in prof.values()):
                        continue
                    out.append(((xb, xt, yl, yr), {k: v['strands'] for k, v in prof.items()}))
                    if first: return out
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('menu', nargs='?')
    ap.add_argument('--n', type=int, default=96)
    ap.add_argument('--top', type=int, default=30)
    ap.add_argument('--symmetric', action='store_true', help='only T = B and R = L')
    a = ap.parse_args()
    G = json.load(open(a.menu)) if a.menu else []
    known = {'H16a': (16, 25), 'H16b': (16, 27), 'PaperHeel': (28, 22), 'VerticalEdge': (10, 8)}
    for nm, (X, T_) in known.items():
        G.append(dict(name=nm, kind='left' if nm == 'VerticalEdge' else 'bottom', tpl=NAMED[nm], X=X, T=T_))
    for g in G:
        mv, W, H = tpl_moves(g['tpl'])
        g['per'] = W if g['kind'] == 'bottom' else H
        g['p'] = pairing(g['tpl'], g['kind'])
        g['unit'] = g['X'] / g['per']
        g['pi'] = parity(g['p']['pairs'], g['p']['cper'])
        ok = not g['p']['bad'] and not g['p']['uncovered']
        print(f"{g['name']:>20} {g['kind']:>6} per={g['per']} X/unit={g['unit']:.3f} pi={g['pi']} valid={ok} pairs={g['p']['pairs']}")
    Bs = [g for g in G if g['kind'] == 'bottom' and not g['p']['bad'] and not g['p']['uncovered']]
    Ls = [g for g in G if g['kind'] == 'left' and not g['p']['bad'] and not g['p']['uncovered']]
    combos = []
    for B in Bs:
        for T_ in ([B] if a.symmetric else Bs):
            for L in Ls:
                for R in ([L] if a.symmetric else Ls):
                    if L['pi'] != R['pi']: continue          # MID parity rule (even n)
                    combos.append((B['unit'] + T_['unit'] + L['unit'] + R['unit'], B, T_, L, R))
    combos.sort(key=lambda c: c[0])
    print(f'\n{len(combos)} combos pass the MID parity rule; checking phases for the best {a.top}')
    shown = 0
    for slope, B, T_, L, R in combos:
        if shown >= a.top: break
        res = []
        for n in (a.n, a.n + 2):
            f = feasible_phases(B['p'], L['p'], T_['p'], R['p'], B['per'], T_['per'], L['per'], R['per'], n)
            res.append(f[0] if f else None)
        print(f"slope {slope:.3f}  B={B['name']} T={T_['name']} L={L['name']} R={R['name']}  "
              f"n={a.n}: {res[0]}  n={a.n + 2}: {res[1]}", flush=True)
        shown += 1

if __name__ == '__main__':
    main()
