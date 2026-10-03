#!/usr/bin/env python
"""Combine per-corner 2-factor floors (sweep.py output) into the best global phases per side pair.
T - 8n (2-factor floor for this side family) = BL(L, xb, yl) + BR(R, xb, yr) + TL(L, xt, yl) + TR(R, xt, yr).
Usage: combine.py sweep_Z8_n56.jsonl [--top 10]"""
import json, sys, itertools, argparse
ap = argparse.ArgumentParser(); ap.add_argument('f'); ap.add_argument('--top', type=int, default=10)
a = ap.parse_args()
R = {}
for l in open(a.f):
    r = json.loads(l)
    if r['res'] is not None: R[r['corner'], r['side'], r['xp'], r['yp']] = (r['res'], r['status'])
Q = {'A23_27': 1, 'B02_24': 1, 'C_lanes4o0': 4}
out = []
for L, Rs in itertools.product(Q, Q):
    for xb, xt, yl, yr in itertools.product(range(8), range(8), range(Q[L]), range(Q[Rs])):
        ks = [('BL', L, xb, yl), ('BR', Rs, xb, yr), ('TL', L, xt, yl), ('TR', Rs, xt, yr)]
        if all(k in R for k in ks):
            v = [R[k][0] for k in ks]
            out.append((sum(v), L, Rs, (xb, xt, yl, yr), v, all(R[k][1] == 'OPTIMAL' for k in ks)))
out.sort(key=lambda t: t[0])
print(f'{a.f}: {len(out)} feasible phase choices; best {a.top}:')
for t in out[:a.top]:
    print(f'  T-8n >= {t[0]:>4}  L={t[1]:<11} R={t[2]:<11} phases={t[3]} corners BL,BR,TL,TR={t[4]} all_optimal={t[5]}')
best = {}
for k, (v, st) in R.items():
    kk = (k[0], k[1])
    if kk not in best or v < best[kk][0]: best[kk] = (v, k[2], k[3])
print('best per corner and side:', {f'{k[0]}/{k[1]}': v for k, v in sorted(best.items())})
