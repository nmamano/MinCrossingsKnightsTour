# KT Structures, 2026-10-03. N_re census: side ports whose collar partner differs from the cheap P / P' partner.
# A port = tour edge between the collar (local x<3 on exactly one side) and the interior (all coords in [3,n-4]).
# Port line label in the local side frame: '/' port (dx*dy>0): c = x - 2y of the inner vertex; '\' port: c = x + 2y.
# The P rule is hard-coded (partner c-3 for even c, c+3 for odd c); rule_conflicts_in_cheap_windows checks it on the tour.
# Also reports, for clean same-side returns, how many of their ends are changed.
import sys, json
from collections import defaultdict, Counter
from pathlib import Path
import fold_exact_scan as F

def scan(f):
    r = F.run(f)
    grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
    E = {F.edge((x, n-1-y), (x+F.MOVES[int(v)][1], n-1-y-F.MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    adj = defaultdict(set); own = defaultdict(int)
    for a, b in E:
        adj[a].add(b); adj[b].add(a)
        for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: own[x+a[0], y+a[1], k] += 1
    gs = lambda i, j: all(own[i, j, k] == 1 for k in range(4))
    gp = lambda v: all(gs(v[0]+dx, v[1]+dy) for dx in (-1, 0) for dy in (-1, 0))
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    inside = lambda v: all(3 <= z <= n-4 for z in v)
    cheap_rows = [set(s) for s in F_cheap(r)]
    ports = {}
    for a, b in E:
        if inside(a) == inside(b): continue
        o, q = (b, a) if inside(a) else (a, b)
        s = [i for i, t in enumerate(T) if t(o)[0] < 3]
        if len(s) != 1: ports[(o, q)] = None; continue
        L = T[s[0]]; lo, lq = L(o), L(q); d = (lq[0]-lo[0], lq[1]-lo[1])
        sgn = 1 if d[0]*d[1] > 0 else -1
        lab = lq[0] - 2*lq[1] if sgn == 1 else lq[0] + 2*lq[1]
        ports[(o, q)] = dict(side=s[0], sgn=sgn, steep=abs(d[0]) == 2, lab=lab, row=lo[1], cheap=lo[1] in cheap_rows[s[0]])
    def collar_partner(o, q):
        prev, cur = q, o
        while True:   # trace the collar path to completion (Claim 38H)
            nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx
            if inside(cur): return (prev, cur)
    partner = {k: collar_partner(*k) for k in ports}
    rule = Counter()
    for k, p in ports.items():
        if p and p['cheap'] and p['steep']:
            pp = ports.get(partner[k])
            if pp and pp['side'] == p['side'] and pp['sgn'] == p['sgn']:
                rule[(p['side'], p['sgn'], p['lab'] % 2, pp['lab'] - p['lab'])] += 1
    # reference P / P' rule, hard-coded (Claim 38H): partner(c) = c - 3 for even c, c + 3 for odd c, every side and sign
    exp = {(si, sg, par): (-3 if par == 0 else 3) for si in range(4) for sg in (1, -1) for par in (0, 1)}
    rule_conflicts = sum(cnt for (si, sg, par, diff), cnt in rule.items() if diff != exp[(si, sg, par)])
    changed = set()
    for k, p in ports.items():
        pp = ports.get(partner[k])
        ok = p and pp and p['steep'] and pp['steep'] and pp['side'] == p['side'] and pp['sgn'] == p['sgn'] \
             and exp.get((p['side'], p['sgn'], p['lab'] % 2)) == pp['lab'] - p['lab']
        if not ok: changed.add(k)
    changed_by_side = Counter(ports[k]['side'] for k in changed if ports[k])
    on_clean = set()
    # clean same-side returns and their changed ends
    seen = set(); ret = Counter(); dirty_by_side = Counter()
    for k, p in ports.items():
        if k in seen or p is None: continue
        o, q = k; prev, cur = o, q; path = [o, q]
        while inside(cur):
            nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx; path.append(cur)
        k2 = (cur, prev); seen.update((k, k2)); p2 = ports.get(k2)
        if not p2 or p2['side'] != p['side']: continue
        if not all(gp(v) for v in path[1:-1]): dirty_by_side[p['side']] += 1; continue
        ret[(k in changed) + (k2 in changed)] += 1
        on_clean.update((k, k2))
    nre1_by_side = Counter(ports[k]['side'] if ports[k] else 'corner' for k in changed if k not in on_clean)
    ret_by_side = Counter(ports[k]['side'] for k in on_clean)
    return dict(n=n, ports=len(ports), N_re=len(changed), rule_conflicts_in_cheap_windows=rule_conflicts, EXC=r['EXC'], rule=dict(rule), clean_returns_by_changed_ends=dict(ret), E=r['E'], BQ=r['BQ'], W=r['W'],
                changed_by_side=dict(changed_by_side), Nre_prime_by_side=dict(nre1_by_side), clean_ends_by_side=dict(ret_by_side),
                Nre_prime=sum(nre1_by_side.values()), RET_clean=len(on_clean)//2, dirty_by_side=dict(dirty_by_side))

def F_cheap(r):
    # cheap slot rows per side, recovered from the label list of fold_exact_scan.run (labels start only at cheap slots)
    s = [set() for _ in range(4)]
    for l in r['labels']: s[l['side']].add(l['row'])
    return s

if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(Path(f).name, scan(f), flush=True)
