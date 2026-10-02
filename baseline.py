import sys, time
from kt.core import validate, num_crossings, num_turns
from kt.gentour import gen_tour
from kt import templates as T
cfgs = {'default-heel': dict(heel=T.Sequence1Default), 'opt-heel': dict(), 'P40-both': dict(block=(T.SequenceP40, 40)), 'P40-bottom-only': dict(block=(T.SequenceP40, 40), block_top=False)}
for name, kw in cfgs.items():
    res = []
    for n in [80, 120, 160, 200, 240]:
        t = gen_tour(n, n, **kw)
        ok = validate(t)
        res.append((n, ok, num_crossings(t), num_turns(t)))
    print(name, res)
    # slope from n=120 -> n=200 and 160->240 (multiples of 40 apart, same residues)
    d = {r[0]: r for r in res}
    print('  slope X (120->200):', (d[200][2]-d[120][2])/80, ' (160->240):', (d[240][2]-d[160][2])/80,
          ' slope T:', (d[200][3]-d[120][3])/80, (d[240][3]-d[160][3])/80)
