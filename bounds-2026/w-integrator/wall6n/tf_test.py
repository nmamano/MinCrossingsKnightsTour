import sys, time
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-integrator'); sys.path.insert(0, '.')
from fold_assemble import setup, edges_to_nb
from tf import twofactor
from chevron import chevron_cells
n = int(sys.argv[1]); mode = sys.argv[2]
E, free, info = setup(n, 4, {}, 4, band=1 if mode == 'diag' else None)
if mode == 'lr': free |= chevron_cells(n, 3, 'LR')
full, ci = twofactor(n, edges_to_nb(n, E), free, time_limit=120, workers=2, feasibility=True)
print(n, mode, 'free', len(free), 'FEASIBLE' if full else ci)
