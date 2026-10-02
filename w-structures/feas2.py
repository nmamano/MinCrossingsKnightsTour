import sys
n_, rad_ = sys.argv[1], sys.argv[2]
ubs = [int(a) for a in sys.argv[3:]]
sys.argv = ['x', n_, rad_, '1', '0', '0']
src = open('build_tour.py').read().split("print('n', n, 'pre:")[0]
exec(src)
from circuit import solve_circuit
from kt.core import crossing_list
for ub in ubs:
    r = solve_circuit(n, E, free, tl=300, feas_only=True, ub=ub)
    if r:
        print('ub', ub, 'tour X', len(crossing_list(r)), flush=True)
