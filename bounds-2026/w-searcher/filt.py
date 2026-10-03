"""Integrator filter: does a bottom gadget pass BL against a given left gadget (cycles 0, all cuts even)
for some shifts? Uses w-integrator/strands.py (pairing, expand, union_profile)."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'w-integrator'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from strands import pairing, expand, union_profile
L3ODD = ['23 27']
L5EVEN = ['02 24']
def bl_pass(btpl, ltpl=L3ODD, n=96):
    B, L = pairing(btpl, 'bottom'), pairing(ltpl, 'left')
    P = B['cper']; Q = L['cper'] // 2
    res = {}
    gm = 12
    for xb in range(P):
        for yl in range(Q):
            pr = union_profile(expand(B['pairs'], P, xb, 1, gm, n - gm), expand(L['pairs'], L['cper'], 2 * yl, 1, gm, n - gm), gm, n - gm)
            if pr['cycles'] == 0 and not any(c % 2 for c in pr['cuts']):
                res[(xb, yl)] = pr['strands']
    return res
def mid_pass(ltpl, rtpl=L3ODD, n=96):
    """MID region: left gadget L vs right = rotated left-type gadget R (c -> n-1+2yr - c)."""
    L, R = pairing(ltpl, 'left'), pairing(rtpl, 'left')
    gm = 12; res = {}
    for yl in range(L['cper'] // 2):
        for yr in range(R['cper'] // 2):
            pr = union_profile(expand(L['pairs'], L['cper'], 2 * yl, 1, n + gm, 2 * n - gm),
                               expand(R['pairs'], R['cper'], n - 1 + 2 * yr, -1, n + gm, 2 * n - gm), n + gm, 2 * n - gm)
            if pr['cycles'] == 0 and not any(c % 2 for c in pr['cuts']):
                res[(yl, yr)] = pr['strands']
    return res
if __name__ == '__main__':
    rows = [json.loads(l) for l in open('menu_results.jsonl')]
    seen = set()
    for r in sorted(rows, key=lambda r: r.get('rate') or 99):
        if r['kind'] != 'bottom' or r.get('rate') is None or r['rate'] >= 3.01: continue
        k = tuple(r['tpl'])
        if k in seen: continue
        seen.add(k)
        a, b = bl_pass(r['tpl'], L3ODD), bl_pass(r['tpl'], L5EVEN)
        print('%.4f P%d D%d %-22s vsL3odd %s vsL5even %s' % (r['rate'], r['P'], r['D'], r['rule'], sorted(set(a.values())) if a else 'FAIL', sorted(set(b.values())) if b else 'FAIL'))
