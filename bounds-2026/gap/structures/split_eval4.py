# KT Structures, 2026-10-03. BEYOND5 12: split forms that separate near ports on rows with a p24 port ("happy") from the
# others. Strip per side: J >= a g + Nf(1) + bh Hnear(1) + bf (Near(1) - Hnear(1)); Near(1) = N_re - N_free(1) (ports on
# g rows included). Families: Claim 45 patch (spacing 24), c5w patch (spacing 20), P5 family.
import json
from split_eval import KB
KB.update({'p5_LF1v3_n72.json': (84, 0), 'LF2_n96.json': (132, 0), 'LF3_n96.json': (132, 0), 'H16b_VerticalEdge_off0_n96.json': (132, 0),
           'c5w_patched16_n192.json': (23, 452), 'c5w_patched16_n288.json': (43, 620)})
R = {}
for f in ('b5raw_20tours.log', 'c5w_b5.log'):
    for l in open(f):
        if l.startswith('RAW'): r = json.loads(l[4:]); R[r['tour']] = r
def ev(a, bh, bf):
    out = {}; worst = 1e9
    for name, r in R.items():
        K, BQx = KB[name]; lhs = BQx - 2*K
        for s in r['sides']:
            H = s['NS']['hnear1']; Nn = s['Nre'] - s['Nf1']
            w = a*s['g'] + s['Nf1'] + bh*H + bf*(Nn - H); lhs += 2*w; worst = min(worst, s['J'] - w)
        out[name] = lhs - 4*r['n']
    base = (out['claim36_FOLD_n288.json'] - out['claim36_FOLD_n192.json']) / 96
    g45 = (out['claim45_U_patched_n288.json'] - out['claim36_FOLD_n288.json']) / 8
    gw = (out['c5w_patched16_n288.json'] - out['claim36_FOLD_n288.json']) / 9
    p5 = (out['p5_LF1v0_n120.json'] - out['p5_LF1v0_n72.json']) / 48
    return worst, min(out.values()), base + g45/24, base + gw/20, p5
print('a bh bf | min strip slack | min C5-4n | slope C45 family | slope c5w family | slope P5 family')
for a in (1.5, 2):
    for bh in (0.5, 1, 1.5, 2):
        for bf in (0, 0.25):
            w, m, s1, s2, s3 = ev(a, bh, bf)
            print(f'{a} {bh} {bf} | {w:6.1f} | {m:5.0f} | {s1:6.3f} | {s2:6.3f} | {s3:6.3f}')
