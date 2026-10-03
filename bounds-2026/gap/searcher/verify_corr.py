"""Independent unrolled check of a corr.cpp witness (KT Edge Searcher, gap mission).
Reads JSON lines from corr output; for each witness it rebuilds the band from the field definition
(not from corr.cpp code), unrolls K periods, and checks: band cells have degree 2, edges with an
outside end are base edges, no finite cycle, crossings per period, and the colour current through
horizontal cuts relative to the plain field.
usage: python3 verify_corr.py FILE.jsonl [K]"""
import sys, json

KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def field(kind):
    if kind == 'diag': return lambda x, y: (2, 1) if x - y <= -1 else (-1, -2)
    if kind == 'mid': return lambda x, y: (1, 2) if x <= -1 else (1, -2)
    uni = {'diag21': (2, 1), 'diag12': (1, 2), 'anti21': (2, 1), 'anti12': (1, 2), 'vert12': (1, 2), 'vert21': (2, 1)}
    if kind in uni: return lambda x, y, v=uni[kind]: v
    if kind == 'edge': return lambda x, y: (2, 1)
    if kind == 'edgeB': return lambda x, y: (1, 2)
    if kind.startswith('d21_'): return lambda x, y: (2, 1)
    if kind.startswith('d12_'): return lambda x, y: (1, 2)
    raise ValueError(kind)


def orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def cross(e, f):
    a, b = e; c, d = f
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def check(d, K=10):
    A, W, OFF, R = d['A'], d['W'], d['OFF'], d['rows']
    F = field(d['kind'])
    u = lambda c: c[0] - A * c[1] - OFF
    band = lambda c: 0 <= u(c) < W
    T = (A * R, R)
    free = [((e[0], e[1]), (e[2], e[3])) for e in d['edges']]
    for e in free:
        assert band(e[0]) and band(e[1]), ('free edge leaves band', e)
    E = set()
    y0, y1 = -2 * R, (K + 2) * R
    for k in range(-3, K + 4):
        for a, b in free:
            p = (a[0] + k * T[0], a[1] + k * T[1]); q = (b[0] + k * T[0], b[1] + k * T[1])
            E.add(tuple(sorted((p, q))))
    # base edges with at least one end in the band, rows in a wide window
    wall = d['kind'] in ('edge', 'edgeB'); uturn = d['kind'] == 'edge'
    def base_edges(c):
        out = set()
        if wall and c[0] < 0: return out
        v = F(*c); out.add(tuple(sorted((c, (c[0] + v[0], c[1] + v[1])))))
        for dx, dy in KM:
            q = (c[0] - dx, c[1] - dy)
            if F(*q) == (dx, dy): out.add(tuple(sorted((q, c))))
        if wall:
            out = {e for e in out if e[0][0] >= 0 and e[1][0] >= 0}
            if uturn and c[0] == 0: out.add(tuple(sorted((c, (1, c[1] + 2)))))
            if uturn and c[0] == 1: out.add(tuple(sorted((c, (0, c[1] - 2)))))
        return out
    cells = [(uu + OFF + A * y, y) for y in range(y0 - 6, y1 + 6) for uu in range(W)]
    forced = set()
    for c in cells:
        for e in base_edges(c):
            o = e[0] if e[1] == c else e[1]
            if not band(o): forced.add(e)
    E |= forced
    deg = {}
    for a, b in E:
        deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
    for c in cells:
        if y0 <= c[1] < y1:
            assert deg.get(c, 0) == 2, ('degree', c, deg.get(c, 0))
    # finite cycles: components fully inside the window rows with all degrees 2 and no outside end
    adj = {}
    for a, b in E:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen = set()
    for s in adj:
        if s in seen or not (y0 <= s[1] < y1) or not band(s): continue
        comp = [s]; seen.add(s); i = 0
        while i < len(comp):
            for t in adj[comp[i]]:
                if t not in seen: seen.add(t); comp.append(t)
            i += 1
        if all(band(c) and y0 + 2 <= c[1] < y1 - 2 and len(adj[c]) == 2 for c in comp):
            raise AssertionError(('finite cycle', comp[:6]))
    # crossings per period: pairs where the edge with the smaller (lower y, x) endpoint key starts in rows [R0, R0+R)
    R0 = (K // 2) * R
    EL = sorted(E, key=lambda e: (min(e[0][1], e[1][1]), e))
    key = lambda e: (min(e[0][1], e[1][1]), min(e))
    X = 0
    for i, e in enumerate(EL):
        for f in EL[i + 1:]:
            if min(f[0][1], f[1][1]) > max(e[0][1], e[1][1]): break
            if cross(e, f):
                k0 = min(key(e), key(f))
                if R0 <= k0[0] < R0 + R: X += 1
    # current through the cut below row Y, window over x, relative to the plain field
    def cur(edges, Y):
        s = 0
        for a, b in edges:
            lo, hi = (a, b) if a[1] < b[1] else (b, a)
            if lo[1] < Y <= hi[1] and abs(lo[0] - (OFF + A * Y)) < W + 12:
                s += 1 if (lo[0] + lo[1]) % 2 == 0 else -1
        return s
    plain = set()
    for y in range(y0 - 8, y1 + 8):
        for xx in range(OFF + A * y - W - 20, OFF + A * y + 2 * W + 20):
            plain |= base_edges((xx, y))
    full = set(E)
    for e in plain:
        if not band(e[0]) and not band(e[1]): full.add(e)
    rel = []
    for Y in range(R0, R0 + R):
        c1 = cur(full, Y); c0 = cur(plain, Y)
        if A % 2 == 0 and Y % 2: c1, c0 = -c1, -c0
        rel.append(c1 - c0)
    return X, rel


if __name__ == '__main__':
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if 'edges' not in d: continue
        X, rel = check(d, K)
        ok = X == d['crossings']
        print(f"{d['kind']} W={d['W']} current={d['current']} rows={d['rows']} solver X={d['crossings']} check X={X} "
              f"{'OK' if ok else 'MISMATCH'} rel.current per cut={sorted(set(rel))}")
