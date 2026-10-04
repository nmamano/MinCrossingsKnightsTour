"""Corner tables with CP-SAT: usage cwsat.py K D  (both fields). Saves cw_{f}_K{K}_D{D}.pkl and witness file."""
import sys, pickle
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
import gen
R = gen.R
K, D = int(sys.argv[1]), int(sys.argv[2]); TL = float(sys.argv[3]) if len(sys.argv) > 3 else 60
unknown = []
for f in ((2, -1), (2, 1)):
    sst, _, szc = pickle.load(open(R + f'fstrip_{f[0]}_{f[1]}.pkl', 'rb'))
    g = (f[1], f[0]) if f[1] > 0 else (-f[1], -f[0])
    gst, _, gzc = pickle.load(open(R + f'fstrip_{g[0]}_{g[1]}.pkl', 'rb'))
    SL = sorted(set().union(*[c for c, gg in szc])); SB = sorted(set().union(*[c for c, gg in gzc]))
    tab = {}; wit = {}
    for a in SL:
        for b in SB:
            st, v, ch = gen.corner_window_sat(f, K, D, sst[a], gst[b], tlimit=TL)
            tab[(a, b)] = v if st == 'OPTIMAL' else None
            if st not in ('OPTIMAL', 'INFEASIBLE'): unknown.append((f, a, b, st, v)); wit[(a, b)] = ch
            print('field', f, 'K', K, 'D', D, 'left', a, 'bottom', b, st, v, flush=True)
    pickle.dump(tab, open(R + f'cw_{f[0]}_{f[1]}_K{K}_D{D}.pkl', 'wb'))
    pickle.dump(wit, open(R + f'cwwit_{f[0]}_{f[1]}_K{K}_D{D}.pkl', 'wb'))
print('UNKNOWN/FEASIBLE-not-optimal pairs:', unknown)
