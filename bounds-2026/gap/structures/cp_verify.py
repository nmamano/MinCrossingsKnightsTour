"""Independent unrolled check of a classphase.py solution: degrees, strand pairing, crossings per period."""
import sys, ast
from classphase import cross, run
from collections import defaultdict

def verify(p, D, shift, sel, T=8):
    def partner(c):
        if 'F' in shift: return c + 5 if c % 2 == 0 else c - 5
        r = c % 3
        if c % 2 == 0: return c + 3 if r in shift else c - 3
        return c - 3 if (c - 3) % 3 in shift else c + 3
    E = set()
    for t in range(-T, T):
        for (a, b) in sel:
            E.add(tuple(sorted([(a[0], a[1] + t*p), (b[0], b[1] + t*p)])))
    ylo, yhi = -T*p - 10, T*p + 10
    for x in range(D - 2, D + 12):
        for y in range(ylo, yhi):
            if x + 2 >= D:
                E.add(((x, y), (x + 2, y + 1)))
    adj = defaultdict(list)
    for a, b in E:
        adj[a].append(b); adj[b].append(a)
    # degrees in the middle periods
    bad = 0
    for x in range(D):
        for y in range(-2*p, 2*p):
            if len(adj[(x, y)]) != 2: bad += 1
    # strands: from line c at x = D+10 (far), walk toward the strip, record where it comes back
    pairs_ok = 0; pairs_bad = 0
    for y0 in range(-p, p):
        for x0 in (D + 10, D + 11):
            c = x0 - 2*y0
            # go in direction of decreasing x along the line until entering the strip, then follow
            prev, cur = (x0 + 2, y0 + 1), (x0, y0)
            steps = 0
            while True:
                nx = [q for q in adj[cur] if q != prev]
                prev, cur = cur, nx[0]
                steps += 1
                if cur[0] >= D + 10 and prev[0] < cur[0]:
                    break
                if steps > 100000: break
            ce = cur[0] - 2*cur[1]
            if ce == partner(c): pairs_ok += 1
            else: pairs_bad += 1
    # crossings: edges with lower endpoint in rows [0,p) vs all
    cnt = 0
    El = list(E)
    grid = defaultdict(list)
    for e in El: grid[(e[0][0]//3, e[0][1]//3)].append(e)
    for e in El:
        if not (0 <= min(e[0][1], e[1][1]) < p) or min(e[0][0], e[1][0]) > D + 6: continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for f in grid[(e[0][0]//3 + dx, e[0][1]//3 + dy)]:
                    if cross(e, f):
                        lo_f = min(f[0][1], f[1][1])
                        # count unordered pair once: attribute to the edge with smaller (lowest y, then tuple)
                        ke = (min(e[0][1], e[1][1]), e); kf = (lo_f, f)
                        if ke < kf or not (0 <= lo_f < p):
                            if ke < kf: cnt += 1
                            elif not (0 <= lo_f < p) and ke > kf: pass
    return dict(deg_bad=bad, pairs_ok=pairs_ok, pairs_bad=pairs_bad, crossings_per_period=cnt)

if __name__ == '__main__':
    p, D = int(sys.argv[1]), int(sys.argv[2])
    shift = set() if sys.argv[3] == '-' else {(ch if ch == 'F' else int(ch)) for ch in sys.argv[3]}
    r = run(p, D, shift, 120, 2, verbose=False)
    print(r['status'], r.get('val'))
    print(verify(p, D, shift, r['sel']))
