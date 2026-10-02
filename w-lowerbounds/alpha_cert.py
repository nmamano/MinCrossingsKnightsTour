"""Exact certificate for alpha = 1/5: weights 20w - 5 - 4*nc (= 20*(w - 1/4 - nc/5)) have no negative cycle;
report the potential range (additive constant). Also show that alpha slightly above 1/5 fails."""
import sys
from fractions import Fraction
exec(open('alpha_star.py').read().split("lo, hi = Fraction(0), Fraction(2)")[0])
for a in (Fraction(1, 5), Fraction(201, 1000)):
    good, dist = ok(a)
    print('alpha', a, 'no negative cycle:', good, ('potential range (units of 1/(4q)): %d..%d' % (dist.min(), dist.max())) if good else '')
