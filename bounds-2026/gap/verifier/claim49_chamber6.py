# KT Structures, 2026-10-03. Zigzag chambers for (R4) (SHEET 9.6 / 11).
# Frames: 4 sides x {plain, y-mirrored}; in each frame the side is the local left side and we start at '/' H runs
# that go from the boundary square (3, j) up-right to the LOWER face of a horizontal wall. The barrier then follows
# the run of the other split that touches the same wall edge from above, away from the wall; at each further
# horizontal wall it crosses at the edge midpoint and continues with the run above; it succeeds when a piece reaches
# the left boundary (row j2), and fails at a bad square, at the top / right boundary, or at a vertical wall.
# For each maximal chamber [j1, j2] (side rows, plain frame) it reports: W' runs starting inside (both directions),
# returns with both ports inside (clean / dirty), ports inside, collar m12 edges inside.
import sys, json
from collections import defaultdict, Counter
from pathlib import Path
import fold_exact_scan as F

QS = {'TL': (2, 3), 'BR': (0, 1), 'RT': (1, 2), 'LB': (3, 0)}

def analyse(f, verbose=False):
    grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
    E = {F.edge((x, n-1-y), (x+F.MOVES[int(v)][1], n-1-y-F.MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    adj = defaultdict(set)
    for a, b in E: adj[a].add(b); adj[b].add(a)
    cov = defaultdict(int)
    for a, b in E:
        for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: cov[x+a[0], y+a[1], k] += 1
    gsq = lambda i, j: all(cov[i, j, k] == 1 for k in range(4))
    gpt = lambda v: all(gsq(v[0]+dx, v[1]+dy) for dx in (-1, 0) for dy in (-1, 0))
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    inside = lambda v: all(6 <= z <= n-7 for z in v)
    # chords: side and local rows (plain frame) of both ports, clean flag
    ports = {}
    for a, b in E:
        if inside(a) == inside(b): continue
        o, q = (b, a) if inside(a) else (a, b)
        s = [i for i, t in enumerate(T) if t(o)[0] < 6]
        ports[(o, q)] = (s[0], T[s[0]](o)[1]) if len(s) == 1 else None
    chords = []; seen = set()
    for k in ports:
        if k in seen: continue
        o, q = k; prev, cur = o, q; path = [o, q]
        while inside(cur):
            nx = next(v for v in adj[cur] if v != prev); prev, cur = cur, nx; path.append(cur)
        k2 = (cur, prev); seen.update((k, k2))
        chords.append((ports[k], ports[k2], all(gpt(v) for v in path[1:-1])))
    out = defaultdict(list)   # side -> list of chamber records
    excess = Counter()
    wruns = defaultdict(set)  # side -> plain rows j whose boundary run ends at a wall face
    for si in range(4):
        for mir in (False, True):
            L0 = T[si]
            L = (lambda v, L0=L0: (L0(v)[0], n-1-L0(v)[1])) if mir else L0
            sqmap = {}
            for i in range(n-1):
                for j in range(n-1):
                    cs = [L((i+a, j+b)) for a in (0, 1) for b in (0, 1)]
                    sqmap[min(c[0] for c in cs), min(c[1] for c in cs)] = (i, j)
            plain_sq = lambda x, y, m=sqmap: m[x, y]
            own = defaultdict(list)
            for a, b in E:
                a, b = sorted((L(a), L(b)))
                for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: own[x+a[0], y+a[1], k].append((a, b))
            insq = lambda x, y: 6 <= x <= n-8 and 6 <= y <= n-8
            good = lambda x, y: all(len(own[x, y, k]) == 1 for k in range(4))
            def split(x, y):
                if not good(x, y): return None
                return '/' if own[x, y, 2] == own[x, y, 3] else '\\'
            def bit(x, y, h):
                a, b = own[x, y, QS[h][0]][0]; return 'H' if abs(b[0]-a[0]) == 2 else 'V'
            # run from the boundary square (3, j): returns ('W', edge info) / other
            def boundary_run(j):
                sp = split(6, j)
                if sp is None: return ('BAD', None)
                if sp == '/':
                    x, y, h = 6, j, 'TL'; step = {'TL': lambda x, y: (x, y+1, 'BR'), 'BR': lambda x, y: (x+1, y, 'TL')}
                else:
                    x, y, h = 6, j, 'LB'; step = {'LB': lambda x, y: (x, y-1, 'RT'), 'RT': lambda x, y: (x+1, y, 'LB')}
                while True:
                    nx, ny, nh = step[h](x, y)
                    if not insq(nx, ny): return ('OUT', None)
                    s2 = split(nx, ny)
                    if s2 is None: return ('BAD', None)
                    if s2 != sp: return ('W', (sp, x, y, h, nx, ny, bit(x, y, h)))
                    x, y, h = nx, ny, nh
            for j in range(6, n-7):
                kind, info = boundary_run(j)
                if kind == "W": wruns[si].add(n-2-j if mir else j)
                if kind != 'W' or info[0] != '/' or info[3] != 'TL' or info[5] != info[2]+1: continue
                # '/' run ended at the top edge of square (x, y): horizontal wall. Zigzag upward.
                x, y = info[1], info[2] + 1; sp = '\\'; res = None; pieces = 0
                bar = set(); sx, sy, sh = 6, j, 'TL'
                while True:
                    bar.add((sx, sy))
                    if (sx, sy, sh) == (info[1], info[2], info[3]): break
                    sx, sy, sh = (sx, sy+1, 'BR') if sh == 'TL' else (sx+1, sy, 'TL')
                while res is None:
                    pieces += 1
                    bar.add((x, y))
                    if sp == '\\':   # start at LB(x, y) (touches the wall below); go up-left: LB -> RT(x-1, y) -> LB(x-1, y+1)
                        h = 'LB'
                        while True:
                            if h == 'LB': nx, ny, nh = x-1, y, 'RT'
                            else: nx, ny, nh = x, y+1, 'LB'
                            if nx < 6: res = ('OK', y); break
                            if ny > n-8: res = ('TOP', None); break
                            s2 = split(nx, ny)
                            if s2 is None: res = ('BAD', None); break
                            if s2 != '\\':
                                if nh == 'LB': x, y, sp = nx, ny, '/'; break   # crossed a top edge: higher wall
                                res = ('VWALL', None); break
                            x, y, h = nx, ny, nh
                            bar.add((x, y))
                    else:            # start at BR(x, y) (touches the wall below); go up-right: BR -> TL(x+1, y) -> BR(x+1, y+1)
                        h = 'BR'
                        while True:
                            if h == 'BR': nx, ny, nh = x+1, y, 'TL'
                            else: nx, ny, nh = x, y+1, 'BR'
                            if nx > n-8 or ny > n-8: res = ('FAR', None); break
                            s2 = split(nx, ny)
                            if s2 is None: res = ('BAD', None); break
                            if s2 != '/':
                                if nh == 'BR': x, y, sp = nx, ny, '\\'; break
                                res = ('VWALL', None); break
                            x, y, h = nx, ny, nh
                            bar.add((x, y))
                if res[0] == 'OK':
                    j2 = res[1]
                    lo, hi = (j, j2) if not mir else (n-2-j2, n-2-j)
                    out[si].append((lo, hi, pieces, {plain_sq(x, y) for x, y in bar}))
                else:
                    excess[res[0]] += 1
    report = []
    for si in range(4):
        iv = sorted(set((a, b) for a, b, *_ in out[si]))
        barq = {}
        for a, b, _, bq in out[si]: barq.setdefault((a, b), bq)
        maxi = [I for I in iv if not any(J != I and J[0] <= I[0] and I[1] <= J[1] for J in iv)]
        for lo, hi in maxi:
            inn = lambda p: p is not None and p[0] == si and lo <= p[1] <= hi + 1
            rc = sum(1 for a, b, cl in chords if cl and inn(a) and inn(b))
            rd = sum(1 for a, b, cl in chords if not cl and inn(a) and inn(b))
            pc = sum(1 for k, p in ports.items() if inn(p))
            W = sum(1 for j in wruns[si] if lo <= j <= hi)
            report.append(dict(side=si, lo=lo, hi=hi, rows=hi-lo+1, W=W, RETc=rc, RETd=rd, ports=pc, barrier=barq[lo, hi]))
    covered = sum(r['W'] for r in report); Wtot = sum(len(v) for v in wruns.values())
    return n, report, excess, covered, Wtot

if __name__ == '__main__':
    for f in sys.argv[1:]:
        n, rep, exc, cov, Wtot = analyse(f)
        print(f"{Path(f).name} n={n}: W' total {Wtot}, inside maximal chambers {cov}; failed zigzags {dict(exc)}")
        tot = Counter()
        for r in rep:
            tot.update(dict(W=r['W'], c2=2*r['RETc'], d2=2*r['RETd'], ports=r['ports'], rows=r['rows']))
            print('   ', {k: v for k, v in r.items() if k != 'barrier'}, ' W-2RETc =', r['W'] - 2*r['RETc'], ' 2rows-ports =', 2*r['rows'] - r['ports'])
        print('   totals', dict(tot))
