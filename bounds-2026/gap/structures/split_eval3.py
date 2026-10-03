# KT Structures, 2026-10-03. BEYOND5 12: per-distance port weights. Strip per side: J >= a g + c1 P1 + c2 P2 + P3,
# P1 = changed ports at distance 1 from the nearest g row, P2 = at distance 2, P3 = farther (N_free(2)); ports ON g rows
# weigh 0. Connectivity: 2 * (same) + BQx - 2K >= 4n - C. Data: b5raw.log.
import json
from split_eval2 import R, KB
def ev(a, c1, c2):
    out = {}; worst = 1e9
    for r in R:
        K, BQx = KB[r['tour']]; n = r['n']; lhs = BQx - 2*K
        for s in r['sides']:
            P1 = s['NS']['Nf0'] - s['Nf1']; P2 = s['Nf1'] - s['Nf2']; P3 = s['Nf2']
            w = a*s['g'] + c1*P1 + c2*P2 + P3
            worst = min(worst, s['J'] - w); lhs += 2*w
        out[r['tour']] = lhs - 4*n
    gad = (out['claim45_U_patched_n288.json'] - out['claim36_FOLD_n288.json']) / 8   # per copy
    var = (out['p5_LF1v0_n120.json'] - out['p5_LF1v0_n72.json']) / 48              # slope of C5 - 4n per unit n
    fold = (out['claim36_FOLD_n288.json'] - out['claim36_FOLD_n192.json']) / 96
    asym_gad = fold + gad / 24          # FOLD with copies at spacing 24: slope of C5 - 4n
    return worst, min(out.values()), gad, asym_gad, var
print('a c1 c2 | min side strip slack (data) | min C5-4n (data) | gadget per copy | gadget family slope | P5 family slope')
for a in (1, 1.5, 2):
    for c1 in (0, 0.5, 1):
        for c2 in (0.5, 1):
            w, m, g, ag, v = ev(a, c1, c2)
            print(f'{a} {c1} {c2} | {w:7.1f} | {m:6.0f} | {g:6.1f} | {ag:6.3f} | {v:6.3f}')
print('data frontier (c2 = 1): a, max c1 with strip slack >= -C per side (C = 0 and C = 5), and family slopes at that point')
for a in (1, 1.25, 1.5, 1.75, 2):
    for C in (0, 5):
        lo, hi = 0.0, 2.0
        for _ in range(30):
            mid = (lo+hi)/2
            if ev(a, mid, 1)[0] >= -C: lo = mid
            else: hi = mid
        w, m, g, ag, v = ev(a, lo, 1)
        print(f'  a={a} C={C}: c1_max={lo:.3f}  min C5-4n={m:.0f} gadget slope={ag:.3f} P5 slope={v:.3f}')
