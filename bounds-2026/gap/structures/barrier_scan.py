# KT Structures, 2026-10-03. Run-end decomposition for (B') (SHEET section 9).
# In each side frame (local left side), every interior boundary square (3, j), 3 <= j <= n-5, is either BAD or good;
# if good, exactly one of its halves touches the left edge (TL for split '/', LB for '\'), and that half is a run end.
# Follow the run along its ribbon into the interior until the next half is
#   OUT   (the run reaches the interior boundary again: a THROUGH run),
#   OTHER (the next square is good with the other split: the run ends at a WALL face),
#   BAD   (the next square is bad).
# Bit of the run: H if the boundary half is covered by an a / d tile (|dx| = 2), V otherwise (T2(a): one bit per run;
# asserted). A vertical side wants H, a horizontal side wants V; the far end of a run from the left side is on the
# top (for '/') or bottom (for '\') side, so every through run has exactly one frustrated end.
# Identity: 4 (n-7) = bdry_bad + 2 T + W' + D'  (summed over sides; T = through runs).
import sys, json
from collections import defaultdict, Counter
from pathlib import Path
import fold_exact_scan as F
import nre_scan

def scan(f):
    grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
    E = {F.edge((x, n-1-y), (x+F.MOVES[int(v)][1], n-1-y-F.MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    QS = {'TL': (2, 3), 'BR': (0, 1), 'RT': (1, 2), 'LB': (3, 0)}
    NXT = {'TL': lambda x, y: (x, y+1, 'BR'), 'BR': lambda x, y: (x+1, y, 'TL'),
           'LB': lambda x, y: (x, y-1, 'RT'), 'RT': lambda x, y: (x+1, y, 'LB')}
    res = {}
    for si, L in enumerate(T):
        own = defaultdict(list)
        for a, b in E:
            a, b = sorted((L(a), L(b)))
            for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: own[x+a[0], y+a[1], k].append((a, b))
        inside_sq = lambda x, y: 3 <= x <= n-5 and 3 <= y <= n-5
        good = lambda x, y: all(len(own[x, y, k]) == 1 for k in range(4))
        def state(h):
            x, y, s = h
            if not inside_sq(x, y): return 'OUT'
            if not good(x, y): return 'BAD'
            q = QS[s]
            if own[x, y, q[0]] != own[x, y, q[1]]: return 'OTHER'
            a, b = own[x, y, q[0]][0]
            return 'H' if abs(b[0]-a[0]) == 2 else 'V'
        c = Counter(); far = Counter()
        for j in range(3, n-4):
            if not good(3, j): c['bdry_bad'] += 1; continue
            h = (3, j, 'TL') if state((3, j, 'TL')) in 'HV' else (3, j, 'LB')
            bit = state(h); assert bit in ('H', 'V'), (si, j, bit)
            cur = h
            while True:
                nx = NXT[cur[2]](cur[0], cur[1]); st = state(nx)
                if st in ('H', 'V'):
                    assert st == bit, ('bit change inside a run', si, j); cur = nx; continue
                break
            if st == 'OUT':
                c['T_end'] += 1
                c['frustrated_here' if bit == 'V' else 'frustrated_far'] += 1
            elif st == 'OTHER': c['W'] += 1; c['W_' + bit] += 1
            else: c['D'] += 1
        res[si] = dict(c)
    return n, res

if __name__ == '__main__':
    for f in sys.argv[1:]:
        n, res = scan(f)
        nr = nre_scan.scan(f)
        tot = Counter()
        for si in res: tot.update(res[si])
        lhs = nr['BQ'] + 2*nr['RET_clean'] + 2*nr['Nre_prime']
        print(f"{Path(f).name} n={n} segments={4*(n-7)} totals={dict(tot)}")
        print(f"   identity check: bdry_bad + T_end + W + D = {tot['bdry_bad']+tot['T_end']+tot['W']+tot['D']}")
        print(f"   RET_clean={nr['RET_clean']} N_re={nr['N_re']} N_re'={nr['Nre_prime']} BQ={nr['BQ']}  (B') lhs={lhs} vs 4n={4*n}")
        print(f"   W' - 2 RET_clean = {tot['W'] - 2*nr['RET_clean']};  frustrated ends F = {tot['frustrated_here']} (here) ; N_re' = {nr['Nre_prime']}")
        for si in range(4):
            r = res[si]; cl = nr['clean_ends_by_side'].get(si, 0); dr = nr['dirty_by_side'].get(si, 0)
            print(f"   side {si}: W'={r.get('W',0)} 2RET_clean={cl} 2RET_dirty={2*dr}  W'-2RET_clean-2RET_dirty={r.get('W',0)-cl-2*dr}")
            print(f"   side {si}: {res[si]}  N_re'={nr['Nre_prime_by_side'].get(si,0)} changed={nr['changed_by_side'].get(si,0)} clean_ends={nr['clean_ends_by_side'].get(si,0)}")
