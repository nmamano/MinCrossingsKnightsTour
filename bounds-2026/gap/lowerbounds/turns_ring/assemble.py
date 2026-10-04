"""Ring assembly for the single-family model (field A=(2,-1) far interior).
Corners: BL, TR use the field-A corner table; TL, BR use the field-(2,1) table (reflections).
Sides are exact min-cost walks of n-2D rows in the strip graphs between zero-class cut states.
usage: assemble.py K D n1 n2 ...   (prints the ring minimum for each n and the best corner keys)"""
import sys, pickle, numpy as np
R = '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/'
K, D = int(sys.argv[1]), int(sys.argv[2]); ns = [int(a) for a in sys.argv[3:]]
TA = pickle.load(open(R + f'cw_2_-1_K{K}_D{D}.pkl', 'rb')); TD = pickle.load(open(R + f'cw_2_1_K{K}_D{D}.pkl', 'rb'))
G = {f: pickle.load(open(R + f'fstrip_{f}.pkl', 'rb')) for f in ('2_-1', '1_-2', '2_1', '1_2')}
rho = lambda s: frozenset((X + dX, -1 - YY - dY, -dX, dY) for (X, YY, dX, dY) in s)


def walker(key):
    states, arcs, zc = G[key]
    ids = {s: i for i, s in enumerate(states)}
    S = np.array([a[0] for a in arcs]); Dd = np.array([a[1] for a in arcs]); C = np.array([a[2] for a in arcs])
    cache = {}
    def walk(src, length):
        if (src, length) not in cache:
            d = np.full(len(states), 10 ** 6); d[src] = 0
            for _ in range(length):
                nd = np.full(len(states), 10 ** 6); np.minimum.at(nd, Dd, d[S] + C); d = nd
            cache[(src, length)] = d
        return cache[(src, length)]
    return states, ids, walk


steepA, gzD = walker('2_-1'), walker('1_2')
for n in ns:
    l = n - 2 * D
    best = (10 ** 6, None)
    A = [(k, v) for k, v in TA.items() if v is not None]; Dt = [(k, v) for k, v in TD.items() if v is not None]
    # precompute side costs
    def side(wk, src_state, dst_state_frame):
        states, ids, walk = wk
        t = ids.get(rho(dst_state_frame))
        if t is None: return 10 ** 6
        return int(walk(src_state, l)[t])
    sA = G['2_-1'][0]; gA = G['1_-2'][0]; sD = G['2_1'][0]; gD = G['1_2'][0]
    for (bl_L, bl_B), cbl in A:
        for (tl_L, tl_B), ctl in Dt:
            cl = side(steepA, bl_L, sD[tl_L])
            if cbl + ctl + cl >= best[0] + 0: pass
            for (tr_L, tr_B), ctr in A:
                ct = side(gzD, tl_B, gA[tr_B])
                for (br_L, br_B), cbr in Dt:
                    cr = side(steepA, tr_L, sD[br_L])
                    cb = side(gzD, br_B, gA[bl_B])
                    tot = cbl + ctl + ctr + cbr + cl + ct + cr + cb
                    if tot < best[0]: best = (tot, ((bl_L, bl_B), (tl_L, tl_B), (tr_L, tr_B), (br_L, br_B)), (cbl, ctl, ctr, cbr), (cl, ct, cr, cb))
    print('K', K, 'D', D, 'n', n, 'n mod 8', n % 8, 'ring min', best[0], 'corners', best[2] if best[1] else None, 'sides', best[3] if best[1] else None, flush=True)
