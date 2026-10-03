import sys
from kt.strip import Strip
from kt.search import solve, to_template
P, D, wX, wT, tl = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
kind = sys.argv[6] if len(sys.argv) > 6 else 'bottom'
off = int(sys.argv[7]) if len(sys.argv) > 7 else 0
st = Strip(kind, P, D, off=off)
r = solve(st, wX, wT, time_limit=tl, workers=int(sys.argv[8]) if len(sys.argv) > 8 else 2)
print(kind, 'P', P, 'D', D, 'off', off, {k: v for k, v in r.items() if k != 'chosen'})
if 'chosen' in r:
    print('\n'.join(to_template(st, r['chosen'])))
