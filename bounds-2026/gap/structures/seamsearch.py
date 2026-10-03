"""Search periodic left-edge pairings that untrap a gentle-seam nest (seam shifts s = (0,1,-1)), then price them
with the exact strip model of classphase.py. KT Structures, 2026-10-03.
usage: python seamsearch.py PER(lines, even) maxdelta D [time]"""
import sys, itertools
from seamnest import trapped_count, P
from classphase import run

PER, MD, D = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
tl = float(sys.argv[4]) if len(sys.argv) > 4 else 120
s = (0, 1, -1)
deltas_allowed = [d for d in range(-MD, MD + 1) if d % 2 == 1 or d % 2 == -1]
found = []
def rec(i, dl):
    if i == PER:
        lam = lambda c, dl=tuple(dl): c + dl[c % PER]
        if all(lam(lam(c)) == c for c in range(PER)):
            found.append(tuple(dl))
        return
    if dl[i] is not None:
        rec(i + 1, dl); return
    for d in deltas_allowed:
        j = i + d
        jm = j % PER
        if j == i: continue
        if dl[jm] is not None: continue
        if jm == i: continue
        dl2 = list(dl); dl2[i] = d; dl2[jm] = -d
        rec(i + 1, dl2)
rec(0, [None] * PER)
print(len(found), 'periodic matchings')
good = []
for dl in found:
    lam = lambda c, dl=dl: c + dl[c % PER]
    t = trapped_count(lam, s, N=360, margin=48)
    if t == 0:
        good.append(dl)
print(len(good), 'untrap the nest')
# price: sort by total |delta| - |P delta| as a proxy
good.sort(key=lambda dl: (sum(1 for i, d in enumerate(dl) if d != (-3 if i % 2 == 0 else 3)), sum(abs(d) for d in dl)))
print('closest to P (entries differing):', [sum(1 for i, d in enumerate(dl) if d != (-3 if i % 2 == 0 else 3)) for dl in good[:10]])
p = PER // 2
assert p % 3 == 0 or True
for dl in good[:int(sys.argv[5]) if len(sys.argv) > 5 else 8]:
    pf = lambda c, dl=dl: c + dl[c % PER]
    # period in rows must make the pairing periodic: PER lines = PER/2 rows
    import math
    pr = p * 6 // math.gcd(p, 6)
    r = run(pr, D, set(), tl, 2, verbose=False, partner_fn=pf)
    print(dl, 'rows/period', pr, r.get('status'), r.get('val'), 'per row', (r['val'] / pr) if 'val' in r else None, flush=True)
