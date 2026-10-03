import sys
sys.argv = ['x', sys.argv[1], sys.argv[2], '1', '0', sys.argv[3]]
src = open('build_tour.py').read().split("# phase 1")[0]
exec(src)
from circuit import solve_circuit
r = solve_circuit(n, E, free, tl=300, feas_only=True)
print('feasible' if r else 'no circuit found')
