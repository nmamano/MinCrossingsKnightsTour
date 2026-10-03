"""Small exact checks for the R3 reduction; not a graph-certificate audit."""
from fractions import Fraction as F
from itertools import combinations

vertices = list((x, y) for x in range(6) for y in range(6))
edges = [(a, b) for a, b in combinations(vertices, 2)
         if sorted((abs(a[0]-b[0]), abs(a[1]-b[1]))) == [1, 2]]
assert len(edges) == 80
pairs = {tuple(sorted((a[0], b[0]))) for a, b in edges
         if a[0] in {0, 1, 3} or b[0] in {0, 1, 3}}
assert pairs == {(0,1), (0,2), (1,2), (1,3), (2,3), (3,4), (3,5)}
corner_budget = 4 * len(edges) * (len(edges)-1) // 2
assert corner_budget == 12640
beta, C = F(2), F(104, 4)
coefficient = 4 + 2*beta/(2*beta+1)
constant = 2 + (corner_budget-2+8*C+78*beta)/(2*beta+1)
assert coefficient == F(24,5)
assert constant == F(13012,5) <= 2603
assert corner_budget-2+8*C+156 == 13002
print('PASS: 80 corner edges, seven column pairs, budget 12640;')
print(f'X >= ({coefficient}) n - ({constant}) >= 24n/5 - 2603.')
