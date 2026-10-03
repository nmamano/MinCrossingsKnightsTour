import sys
from layout import solve, show, breakdown
sv = float(sys.argv[1]); sg = float(sys.argv[2])
for k in [int(a) for a in sys.argv[3:]]:
    st, cost, lab = solve(k, sv, sg, tl=120)
    print('k', k, 'sv', sv, 'sg', sg, st, round(cost, 4))
    print(show(k, lab))
    e, its = breakdown(k, lab, sv, sg)
    print('edges', round(e, 4), 'nonfree', [(w, kd, p, round(c, 4)) for (w, kd, p, r, c) in its])
