# KT Structures, 2026-10-03. BEYOND5 12: candidate splits on b5raw.log. Strip per side: J >= a g + c P(d0) [+ bh Hnear(d0)],
# P(0) = changed ports on non-g rows; P(d0>=1) = N_free(d0); Hnear = near changed ports on rows with a p24 port.
# C5 side: 2a g + 2c P + 2bh Hnear + BQx - 2K - 4n. Prints min per-side strip slack and C5 - 4n per tour.
import json, sys
from split_eval import KB
KB.update({'p5_LF1v3_n72.json': (84, 0), 'LF2_n96.json': (132, 0), 'LF3_n96.json': (132, 0), 'H16b_VerticalEdge_off0_n96.json': (132, 0)})
R = [json.loads(l[4:]) for l in open('b5raw.log') if l.startswith('RAW')]
def ev(a, c, d0, bh=0):
    res = []
    for r in R:
        K, BQx = KB[r['tour']]; n = r['n']; lhs = BQx - 2*K; sl = []
        for s in r['sides']:
            P = s['NS']['Nf0'] if d0 == 0 else s[f'Nf{d0}']; H = s['NS'].get(f'hnear{d0}', 0) if d0 else 0
            sl.append(s['J'] - a*s['g'] - c*P - bh*H); lhs += 2*a*s['g'] + 2*c*P + 2*bh*H
        res.append((r['tour'][:22], n, round(min(sl), 1), round(lhs - 4*n)))
    return res
forms = [(2, 1, 0), (2, 13/14, 0), (1.5, 1, 0), (2, 1, 1, 1), (2, 1, 2, 1)]
if __name__ == "__main__":
 for fm in forms:
    print('a, c, d0, bh =', [round(x, 3) for x in fm], ' (tour, n, min side strip slack, C5 - 4n)')
    print('   ', ev(*fm))
