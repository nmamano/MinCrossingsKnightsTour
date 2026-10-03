#!/usr/bin/env python3
"""Do fold stacks tile the plane exactly (every quarter covered once)? Random level sequences, all 4 families,
both orientations; count quarters with multiplicity != 1 in an interior region."""
import random, sys
from w1_foldstack import FAM
from w3_quarters import tile, inside, quarters

def run(trials=60, N=14, seed=5):
    rnd = random.Random(seed); worst = 0; stats = {}
    for t in range(trials):
        (a, b), dA, dB = FAM[t % 4]
        if (t // 4) % 2: dA, dB, a, b = (-dA[0], -dA[1]), (-dB[0], -dB[1]), -a, -b
        f = lambda p: a * p[0] + b * p[1]
        mode = ['random', 'alternate', 'one switch'][t % 3]
        c = {}
        for lv in range(-80, 80):
            c[lv] = (rnd.choice((dA, dB)) if mode == 'random' else (dA if lv % 2 else dB) if mode == 'alternate'
                     else (dA if lv < 3 else dB))
        E = set()
        for x in range(-4, N + 4):
            for y in range(-4, N + 4):
                p = (x, y); q = (x + c[f(p)][0], y + c[f(p)][1]); E.add(tuple(sorted((p, q))))
        bad = 0
        for x in range(2, N - 2):
            for y in range(2, N - 2):
                for qq, pt in quarters(x, y).items():
                    m = sum(1 for e in E if abs(e[0][0] - x) <= 3 and abs(e[0][1] - y) <= 3 and inside(tile(e), pt))
                    bad += m != 1
        stats[mode] = max(stats.get(mode, 0), bad); worst = max(worst, bad)
    print('max bad quarters in the interior by sequence type:', stats)

if __name__ == '__main__':
    run()
