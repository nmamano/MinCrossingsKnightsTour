import sys; sys.path.insert(0, '.')
import fold_jog as J, fold3
from fold3 import comps
def closed_with(n, bands, d=1):
    old = fold3.field
    fold3.field = J.make_field(lambda m: bands, d=d)
    try:
        E, deg = fold3.build(n, ts=(1,) * 4)
    finally:
        fold3.field = old
    cs, cyc, bad = comps(n, E, deg)
    return len(cyc), len(bad)
def rule(h, seq):
    Ds = []
    for D in seq:
        if D < h - 2: Ds.append(D)
    return [h - D for D in Ds]
def seqgen(a, b, k=12):
    s = [a, b]
    while len(s) < k: s.append(2 * s[-1] + 3)
    return s
if __name__ == "__main__":
  for a, b in [(5, 9), (5, 13), (7, 15)]:
    res = []
    for n in range(48, 201, 8):
        h = n // 2
        Ds = [D for D in seqgen(a, b) if D <= h // 2 + 2]
        c, dft = closed_with(n, [h - D for D in Ds])
        res.append((n, c))
    print((a, b), res, flush=True)
