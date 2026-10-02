from fractions import Fraction
exec(open('beta_star.py').read().split("lo, hi = Fraction(1, 5), Fraction(4)")[0].replace("CAP = 4000", "CAP = 10**7"))
good, dist = ok2(Fraction(1, 2))
print('beta 1/2: no negative cycle:', good, 'potential range (units 1/8):', dist.min(), dist.max())
