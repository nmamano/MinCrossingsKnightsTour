from fractions import Fraction
exec(open('kappa2_star.py').read().split("lo, hi = Fraction(1, 5), Fraction(2)")[0])
for k in (Fraction(2, 7), Fraction(2862, 10000)):
    good, dist = ok3(k, 20000)
    print('kappa', k, 'no negative cycle (converged):', good, ('range %d..%d units 1/(4q)' % (dist.min(), dist.max())) if good else '')
