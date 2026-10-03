import sys
sys.argv = ['x', '48', '3', '1', '0']
exec(open('build_tour.py').read().split("t0 = time.time()")[0].split("# phase 1")[0])
print('comps', len(cs), 'closed', len(cyc), 'bad', len(bad), [imbalance(n, E, window_cells(n, c, 3)) for c in cls], 'X(pre)', len(crossing_list(E)))
