"""Turning-number check for same-edge nests (KT Structures, 2026-10-03).

A nest line is a simple polyline in the board from a left-edge point A=(0,a) to a left-edge point B=(0,b).
Close it with the edge segment B->A. The closed curve is simple, so its total turning is +360 (b>a: the
segment runs down, the region is on its left) or -360 (b<a). Each exterior angle at A and B lies in
(-180,180), so it is fixed by the two directions. Thus the rotation of the arc is FIXED by (start dir,
end dir, b>a or b<a). This script lists the fixed values and compares them with all walks on the
free-fold 8-cycle (LB F10a) of length <= K.
"""
import math, itertools, sys

CYC = [(2, 1), (-2, 1), (1, -2), (1, 2), (-2, -1), (2, -1), (-1, 2), (-1, -2)]
ang = lambda d: math.degrees(math.atan2(d[1], d[0]))

def turn(d1, d2):
    t = ang(d2) - ang(d1)
    while t <= -180: t += 360
    while t > 180: t -= 360
    return t

def walk_rot(steps):
    i, rot = 0, 0.0
    for s in steps:
        j = (i + s) % 8
        rot += turn(CYC[i], CYC[j]); i = j
    return CYC[i], rot

def required(d_start, d_end, above):
    # above: B above A, the closing segment runs down (0,-1) from B to A, total +360
    seg = (0, -1) if above else (0, 1)
    total = 360 if above else -360
    return total - turn(d_end, seg) - turn(seg, d_start)

K = int(sys.argv[1]) if len(sys.argv) > 1 else 9
left = [(-2, 1), (-2, -1)]   # steep left-facing ends only (Claim 24)
print("start (2,1). Fixed rotation of a simple same-edge arc:")
for d in left:
    for above in (True, False):
        print(f"  end {d} {'above' if above else 'below'}: {required((2,1), d, above):8.2f}")
print(f"walks (steps +-1 on the 8-cycle, length <= {K}) whose rotation matches:")
hits = {}
for L in range(1, K + 1):
    for st in itertools.product((1, -1), repeat=L):
        d, r = walk_rot(st)
        if d not in left: continue
        for above in (True, False):
            if abs(r - required((2, 1), d, above)) < 1e-6:
                hits.setdefault((d, above, round(r, 2), sum(st)), 0)
                hits[(d, above, round(r, 2), sum(st))] += 1
for k, v in sorted(hits.items(), key=str):
    print(f"  end {k[0]} {'above' if k[1] else 'below'} rot {k[2]} net steps {k[3]}: {v} walks")
nets = sorted({k[3] for k in hits})
print("net step values that occur:", nets)
assert nets == [1], nets
assert all(k[0] == (-2, 1) and k[1] for k in hits), hits
print("OK: only net step +1, end (-2,1), B above A")
