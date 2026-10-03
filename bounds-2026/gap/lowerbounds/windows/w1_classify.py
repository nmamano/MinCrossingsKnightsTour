#!/usr/bin/env python3
"""Summarise W1 central maps: straight directions present and turn types present."""
import sys, json
from collections import Counter
K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
LINE = {0: 'A(1,2)', 4: 'A(1,2)', 1: 'B(2,1)', 5: 'B(2,1)', 2: 'C(2,-1)', 6: 'C(2,-1)', 3: 'D(1,-2)', 7: 'D(1,-2)'}


def ctype(ds):
    a, b = ds
    if (a + 4) % 8 == b: return 'S' + LINE[a][0]
    assert (b - a) % 8 in (1, 7), ds
    return f'T{a}{b}'


def main():
    maps = json.load(open(sys.argv[1]))
    summ = Counter()
    for m in maps:
        ts = [ctype(ds) for ds in m.values()]
        S = ''.join(sorted({t[1] for t in ts if t[0] == 'S'}))
        T = sorted({t for t in ts if t[0] == 'T'})
        summ[(S, ' '.join(T))] += 1
    for (S, T), c in sorted(summ.items(), key=lambda z: (len(z[0][0]), z[0])):
        print(f'{c:5d}  straight={S or "-":5s} turns={T or "-"}')
    print(len(maps), 'maps,', len(summ), 'classes')


if __name__ == '__main__':
    main()
