#!/usr/bin/env python
"""Extend a tour built with periodic sides (pring.py) from n0 to n0 + 8k and verify it
(KT Edge Searcher, 2026-10-04).
The map: new cell (x, y) copies old cell (x', y'): x' = x if x < s, x - 8k if x >= s + 8k, else
s + (x - s) mod 8 (same for y), s = n0 // 2.
This is consistent because near the split every band is periodic with a period that divides 8 and the
interior is the fixed line field.  Each extended grid is checked by kt.core.validate and by the
independent walk (w-integrator/assemble.walk_check); turns by kt.core.num_turns.
Usage: extend.py grid_n58_Z8.json --K 12"""
import argparse, json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'w-integrator'))
from kt.core import validate, num_turns
from assemble import walk_check

def extend(g, k):
    n0 = len(g); s = n0 // 2; n = n0 + 8 * k
    mp = lambda v: v if v < s else (v - 8 * k if v >= s + 8 * k else s + (v - s) % 8)
    out = [[None] * n for _ in range(n)]
    for i in range(n):
        y = n - 1 - i
        for j in range(n):
            out[i][j] = g[n0 - 1 - mp(y)][mp(j)]
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('f'); ap.add_argument('--K', type=int, default=12)
    ap.add_argument('--save', help='directory for the extended tours (optional)')
    a = ap.parse_args()
    g = json.load(open(a.f))['tour']
    for k in range(a.K + 1):
        h = extend(g, k); n = len(h)
        ok = validate(h) and walk_check(h); T = num_turns(h)
        print(f'n={n} valid={ok} T={T} T-8n={T - 8 * n}', flush=True)
        if a.save and ok:
            os.makedirs(a.save, exist_ok=True)
            json.dump(dict(n=n, turns=T, source=a.f, tour=h), open(os.path.join(a.save, f'n{n}.json'), 'w'))
