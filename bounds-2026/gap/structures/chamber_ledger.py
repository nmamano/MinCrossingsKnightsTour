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
    return n, ports, changed, other, E, adj

def chord_path(k, adj, inside):
    o, q = k; prev, cur = o, q; path = [q]
    while inside(cur):
        nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx; path.append(cur)
    return path[:-1]

def ledger(f):
    n, rep, exc, cov, Wtot = C.analyse(f)
    _, ports, changed, other, E, adj = port_data(f)
    cov = defaultdict(int)
    for a, b in E:
        for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: cov[x+a[0], y+a[1], k] += 1
    bq = lambda i, j: sum(1 for k in range(4) if cov[i, j, k] != 1)
    inside = lambda v: all(3 <= z <= n-4 for z in v)
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    sqm = []
    for si in range(4):
        m = {}
        for i in range(n-1):
            for jj in range(n-1):
                cs = [T[si]((i+a, jj+b)) for a in (0, 1) for b in (0, 1)]
                m[min(c[0] for c in cs), min(c[1] for c in cs)] = (i, jj)
        sqm.append(m)
    side_sq = lambda si, j: sqm[si][3, j]   # plain square of the local boundary square (3, j) of side si
    rows = []
    for r in rep:
        si, lo, hi = r['side'], r['lo'], r['hi']
        bar = r['barrier']; reg = set(); st = [side_sq(si, j) for j in range(lo, hi+1)]
        while st:
            q = st.pop()
            if q in reg or q in bar or not (3 <= q[0] <= n-5 and 3 <= q[1] <= n-5): continue
            reg.add(q); st.extend([(q[0]+1, q[1]), (q[0]-1, q[1]), (q[0], q[1]+1), (q[0], q[1]-1)])
        rb = reg | bar
        sq4 = lambda v: [(v[0]+dx, v[1]+dy) for dx in (-1, 0) for dy in (-1, 0)]
        vin = lambda v: any(q in reg for q in sq4(v)) or all(q in rb for q in sq4(v))
        inn = lambda k: ports.get(k) is not None and ports[k]['side'] == si and lo <= ports[k]['row'] <= hi + 1
        P = [k for k in ports if inn(k)]
        R = [k for k in P if inn(other[k])]          # ports on returns inside sigma
        rets = {frozenset((k, other[k])) for k in R}
        U = sum(1 for e in rets if not (e & changed))
        rin = {e for e in rets if all(vin(v) for v in chord_path(min(e), adj, inside))}
        Uin = sum(1 for e in rin if not (e & changed)); Cin = len(rin) - Uin
        Nin = sum(len(e & changed) for e in rin)
        BQreg = sum(bq(*q) for q in reg); BQbar = sum(bq(*q) for q in bar)
        R2 = sum(1 for e in rets if e <= changed)
        Rsh = sum(1 for e in rets if any(not ports[k]['steep'] for k in e))
        N = sum(1 for k in P if k in changed); c = sum(1 for k in P if not ports[k]['steep'])
        L = hi - lo + 2
        rows.append(dict(side=si, lo=lo, hi=hi, L=L, p=len(P), c=c, N=N, R=len(rets), U=U, R2=R2, Rsh=Rsh,
                         X=len(P) - len(R), W=r['W'], slack=2*N + 2*U - L, Rin=len(rin), Uin=Uin, need=L - 2*Cin, BQreg=BQreg, BQbar=BQbar, area=len(reg), Nin=Nin))
    BQ = sum(bq(i, j) for i in range(3, n-4) for j in range(3, n-4))
    glob = dict(rows=4*(n-7), N_re=len(changed), BQ=BQ)
    return n, rows, glob

if __name__ == '__main__':
    for f in sys.argv[1:]:
        n, rows, g = ledger(f)
        print(Path(f).name, f"n={n}")
        for r in rows: print('   ', r)
        t = Counter()
        for r in rows: t.update({k: v for k, v in r.items() if k not in ('side', 'lo', 'hi')})
        print('   total', dict(t))
        out_need = g['rows'] - t['L'] - 2*(g['N_re'] - t['Nin'])
        print('   outside chambers: rows', g['rows'] - t['L'], ' need after 2 x (changed ports not on inside returns)', out_need,
              ' BQ outside regions', g['BQ'] - t['BQreg'] - t['BQbar'], ' (global', g, ')', flush=True)
