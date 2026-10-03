# KT Structures, 2026-10-03. Chamber ledger for (T*) (SHEET 13): per maximal zigzag chamber (chamber_scan.py),
# rows L, ports p, shallow ports c, changed ports N, returns R (both ends in sigma), U = returns with no changed end,
# R2 = returns with two changed ends, X = chords with one end in sigma. Checks L <= 2N + 2U + O(1) per chamber.
import sys, json
from collections import defaultdict, Counter
from pathlib import Path
import fold_exact_scan as F
import chamber_scan as C

def port_data(f):
    grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
    E = {F.edge((x, n-1-y), (x+F.MOVES[int(v)][1], n-1-y-F.MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    adj = defaultdict(set)
    for a, b in E: adj[a].add(b); adj[b].add(a)
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    inside = lambda v: all(3 <= z <= n-4 for z in v)
    ports = {}
    for a, b in E:
        if inside(a) == inside(b): continue
        o, q = (b, a) if inside(a) else (a, b)
        s = [i for i, t in enumerate(T) if t(o)[0] < 3]
        if len(s) != 1: ports[(o, q)] = None; continue
        L = T[s[0]]; lo, lq = L(o), L(q); d = (lq[0]-lo[0], lq[1]-lo[1])
        sgn = 1 if d[0]*d[1] > 0 else -1
        lab = lq[0] - 2*lq[1] if sgn == 1 else lq[0] + 2*lq[1]
        ports[(o, q)] = dict(side=s[0], sgn=sgn, steep=abs(d[0]) == 2, lab=lab, row=lo[1])
    def collar_partner(o, q):
        prev, cur = q, o
        while True:
            nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx
            if inside(cur): return (prev, cur)
    changed = set()
    for k, p in ports.items():
        pp = ports.get(collar_partner(*k))
        ok = p and pp and p['steep'] and pp['steep'] and pp['side'] == p['side'] and pp['sgn'] == p['sgn'] \
             and pp['lab'] - p['lab'] == (-3 if p['lab'] % 2 == 0 else 3)
        if not ok: changed.add(k)
    other = {}
    for k in ports:
        o, q = k; prev, cur = o, q
        while inside(cur):
            nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx
        other[k] = (cur, prev)
    return n, ports, changed, other

def ledger(f):
    n, rep, exc, cov, Wtot = C.analyse(f)
    _, ports, changed, other = port_data(f)
    rows = []
    for r in rep:
        si, lo, hi = r['side'], r['lo'], r['hi']
        inn = lambda k: ports.get(k) is not None and ports[k]['side'] == si and lo <= ports[k]['row'] <= hi + 1
        P = [k for k in ports if inn(k)]
        R = [k for k in P if inn(other[k])]          # ports on returns inside sigma
        rets = {frozenset((k, other[k])) for k in R}
        U = sum(1 for e in rets if not (e & changed))
        R2 = sum(1 for e in rets if e <= changed)
        Rsh = sum(1 for e in rets if any(not ports[k]['steep'] for k in e))
        N = sum(1 for k in P if k in changed); c = sum(1 for k in P if not ports[k]['steep'])
        L = hi - lo + 2
        rows.append(dict(side=si, lo=lo, hi=hi, L=L, p=len(P), c=c, N=N, R=len(rets), U=U, R2=R2, Rsh=Rsh,
                         X=len(P) - len(R), W=r['W'], slack=2*N + 2*U - L))
    return n, rows

if __name__ == '__main__':
    for f in sys.argv[1:]:
        n, rows = ledger(f)
        print(Path(f).name, f"n={n}")
        for r in rows: print('   ', r)
        t = Counter()
        for r in rows: t.update({k: v for k, v in r.items() if k not in ('side', 'lo', 'hi')})
        print('   total', dict(t), flush=True)
