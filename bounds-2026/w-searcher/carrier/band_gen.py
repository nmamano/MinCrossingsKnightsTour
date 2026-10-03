"""Generate band.cpp input for a straight band between two knight-line fields (KT Edge Searcher).
Band: -w1 <= hv.c <= w2. Side 1 (hv.c < -w1): lines along f1; side 2 (hv.c > w2): lines along f2
(f2 = None: wall, i.e. off board). Sweep coordinate a = sv.c. t0 = minimal colour-preserving
translation along the band (hv.t0 = 0, sv.t0 > 0)."""
import sys, itertools
KN = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
def gen(path, hv, w1, w2, f1, f2, sv, t0, units_per_t0=1):
    assert dot(hv, t0) == 0 and dot(sv, t0) > 0 and (t0[0] + t0[1]) % 2 == 0
    det = sv[0] * hv[1] - sv[1] * hv[0]
    # c = (1/det) * [[hv1, -sv1], [-hv0, sv0]] (a, b)  -> scaled coords M = adjugate
    M = (hv[1], -sv[1], -hv[0], sv[0])
    PA = dot(sv, t0)
    side = lambda c: 1 if dot(hv, c) < -w1 else (2 if dot(hv, c) > w2 else 0)
    R = 4 * (abs(w1) + abs(w2) + PA + 4)
    cols = {r: [] for r in range(PA)}
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            c = (x, y); a = dot(sv, c)
            if side(c) != 0 or not (0 <= a < PA): continue
            b = dot(hv, c)
            fix = []
            for d in KN:
                v = (c[0] + d[0], c[1] + d[1]); sd = side(v)
                if sd == 1 and d in (f1, (-f1[0], -f1[1])): fix.append(d)
                if sd == 2 and f2 is not None and d in (f2, (-f2[0], -f2[1])): fix.append(d)
            chi = 1 if (x + y) % 2 == 0 else -1
            cols[a].append((b, chi, [(dot(sv, d), dot(hv, d)) for d in fix]))
    for r in cols:
        bs = [c[0] for c in cols[r]]; assert len(bs) == len(set(bs)), 'depth not unique in a column'
        cols[r].sort()
    fm = sorted({(dot(sv, d), dot(hv, d)) for d in KN if dot(sv, d) > 0})
    assert all(da != 0 for d in KN for da in [dot(sv, d)])
    maxda = max(da for da, db in fm)
    with open(path, 'w') as f:
        f.write('%d %d %d\n%d %d %d %d\n' % (PA, maxda, PA // units_per_t0 if PA % units_per_t0 == 0 else PA, *M))
        for r in range(PA):
            f.write('%d\n' % len(cols[r]))
            for b, chi, fx in cols[r]:
                f.write('%d %d %d %s\n' % (b, chi, len(fx), ' '.join('%d %d' % d for d in fx)))
        f.write('%d\n' % len(fm))
        for d in fm: f.write('%d %d\n' % d)
    return PA, maxda, sum(len(v) for v in cols.values())
KINDS = {
    # Structures' kinds (w-structures/seam_flux.py, run_seam.py): T=(p,p), hv=(-1,1)
    'diagfree': dict(hv=(-1, 1), f1=(1, 2), f2=(2, 1), sv=(1, 1), t0=(1, 1)),
    'gentle':   dict(hv=(-1, 1), f1=(2, -1), f2=(1, -2), sv=(1, 1), t0=(1, 1)),
    # C1 (Structures S5): band of whole lines |x - 2y| <= w in the pure (2,1) field; rate per (2,1) step
    # left edges (cps_band.py edgeA/edgeB): cells 0 <= x <= w, wall at x < 0; rate per row
    'edgeA':    dict(hv=(-1, 0), f1=(2, 1), f2=None, sv=(0, 1), t0=(0, 2), u=2, wall=True),
    'edgeB':    dict(hv=(-1, 0), f1=(1, 2), f2=None, sv=(0, 1), t0=(0, 2), u=2, wall=True),
    # vertical interior bands (cps_band.py vert12/midfold/vert21): |x| <= w, rate per row
    'vert12':   dict(hv=(1, 0), f1=(1, 2), f2=(1, 2), sv=(0, 1), t0=(0, 2), u=2),
    'midfold':  dict(hv=(1, 0), f1=(1, 2), f2=(1, -2), sv=(0, 1), t0=(0, 2), u=2),
    'vert21':   dict(hv=(1, 0), f1=(2, 1), f2=(2, 1), sv=(0, 1), t0=(0, 2), u=2),
    'c1':       dict(hv=(1, -2), f1=(2, 1), f2=(2, 1), sv=(1, 0), t0=(4, 2), u=2),
}
if __name__ == '__main__':
    kind, w, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    k = KINDS[kind]
    print(gen(out, k['hv'], w, 0 if k.get('wall') else w, k['f1'], k['f2'], k['sv'], k['t0'], k.get('u', 1)))
