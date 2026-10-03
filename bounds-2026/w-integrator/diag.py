"""Per-region diagnosis of a gadget combo: for each region, which phase pairs pass (no finite
cycle, even cuts), with strand counts."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strands import pairing, expand, union_profile
from kt.board import tpl_moves

def region_table(p1, s1, sg1, p2, s2, sg2, lo, hi):
    m1 = expand(p1['pairs'], p1['cper'], s1, sg1, lo, hi)
    m2 = expand(p2['pairs'], p2['cper'], s2, sg2, lo, hi)
    return union_profile(m1, m2, lo, hi)

def diag(B, L, R, T, n, verbose=True):
    pB, pL, pR, pT = pairing(B, 'bottom'), pairing(L, 'left'), pairing(R, 'left'), pairing(T, 'bottom')
    PB, PT, QL, QR = tpl_moves(B)[1], tpl_moves(T)[1], tpl_moves(L)[2], tpl_moves(R)[2]
    N = 3 * (n - 1); g = 12
    res = {}
    res['BL'] = {(xb, yl): region_table(pB, xb, 1, pL, 2 * yl, 1, g, n - g) for xb in range(PB) for yl in range(QL)}
    res['MID'] = {(yl, yr): region_table(pL, 2 * yl, 1, pR, n - 1 + 2 * yr, -1, n + g, 2 * n - g) for yl in range(QL) for yr in range(QR)}
    res['TR'] = {(yr, xt): region_table(pR, n - 1 + 2 * yr, -1, pT, xt + 2 * (n - 1), -1, 2 * n + g, N - g) for yr in range(QR) for xt in range(PT)}
    good = {k: {ph: (p['strands'], p['cuts']) for ph, p in v.items() if not p['cycles'] and not any(c % 2 for c in p['cuts'])} for k, v in res.items()}
    if verbose:
        for k, v in res.items():
            print(k, 'pass:', good[k])
            bad = {ph: (p['cycles'], p['cuts']) for ph, p in v.items() if ph not in good[k]}
            print('   fail (cycles, cuts):', dict(list(bad.items())[:6]))
    return good

if __name__ == '__main__':
    menu = {g['name']: g for g in json.load(open(sys.argv[1]))}
    from assemble import NAMED
    get = lambda s: menu[s]['tpl'] if s in menu else NAMED[s]
    B, L, R, T = (get(s) for s in sys.argv[2:6])
    n = int(sys.argv[6]) if len(sys.argv) > 6 else 96
    diag(B, L, R, T, n)
