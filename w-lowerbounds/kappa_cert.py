from fractions import Fraction
exec(open('kappa_star.py').read().split("lo, hi = Fraction(1, 12), Fraction(1)")[0])
for k in (Fraction(2, 15), Fraction(134, 1000)):
    good, dist = ok3(k, 20000)
    print('kappa', k, 'no negative cycle (converged):', good, ('range %d..%d units 1/(4q)' % (dist.min(), dist.max())) if good else '')
