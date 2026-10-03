"""Corner segment costs: BL corner (quadrant x,y>=0), straight interior field f (cells x>=4 and y>=4).
Block = {x<4, y<D} U {y<4, x<D}. Boundary: the cut above row D-1 on the left arm is a given zero-class state of the
steep graph (field f); the cut right of column D-1 on the bottom arm is a given zero-class state of the grazing graph
(frame (X,Y)=(y,x), field (f[1],f[0])). Returns min sum r over the block for each pair (None if infeasible).
usage: cornerseg.py fx fy D"""
import sys, pickle
from itertools import combinations
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
from strip import M, lower
R = '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/'


def rq(p, a, b):
    t = int(a[0] + b[0] != 0 or a[1] + b[1] != 0)
    return t - lower(p[0], [a[0], b[0]]) - lower(p[1], [a[1], b[1]])


def left_edges(s, D):     # steep frame (x, yy, dx, dy) at next row D -> absolute (outside cell, block cell)
    out = []
    for (x, yy, dx, dy) in s:
        lo, hi = (x, D + yy), (x + dx, D + yy + dy)
        out.append((hi, lo) if hi[1] >= D else (lo, hi))
    return out


def bottom_edges(s, D):   # grazing frame (X, YY, dX, dY) at next column D -> absolute (y=X, x=D+YY)
    out = []
    for (X, YY, dX, dY) in s:
        lo, hi = (D + YY, X), (D + YY + dY, X + dX)
        out.append((hi, lo) if hi[0] >= D else (lo, hi))
    return out


def segment(f, D, sL, sB, witness=False):
    fm = [f, (-f[0], -f[1])]
    interior = lambda q: q[0] >= 4 and q[1] >= 4
    inblock = lambda q: q[0] >= 0 and q[1] >= 0 and ((q[0] < 4 and q[1] < D) or (q[1] < 4 and q[0] < D))
    order = [(x, y) for y in range(D - 1, 3, -1) for x in range(4)]          # left arm downward
    order += [(x, y) for y in range(3, -1, -1) for x in range(4)]            # corner square
    order += [(x, y) for x in range(4, D) for y in range(4)]                 # bottom arm rightward
    pos = {p: i for i, p in enumerate(order)}
    fint = {p: [d for d in M if interior((p[0] + d[0], p[1] + d[1])) and (-d[0], -d[1]) in fm] for p in order}
    ext = left_edges(sL, D) + bottom_edges(sB, D)          # (outside, block) pairs, all forced
    for o, b in ext: assert inblock(b) and not inblock(o), (o, b)
    front = {frozenset((o, b) for o, b in ext): (0, ())}
    for i, p in enumerate(order):
        cands = []
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if inblock(q) and pos[q] > i: cands.append(d)
        nf = {}
        for fs, (c0, wit) in front.items():
            inc = [(a[0] - p[0], a[1] - p[1]) for a, b in fs if b == p]
            base = inc + fint[p]
            if len(base) > 2: continue
            rest = frozenset(e for e in fs if e[1] != p)
            for extra in combinations([d for d in cands if d not in base], 2 - len(base)):
                mv = base + list(extra)
                fs2 = rest | frozenset((p, (p[0] + d[0], p[1] + d[1])) for d in extra)
                load = {}
                for a, b in fs2: load[b] = load.get(b, 0) + 1
                if any(v + len(fint[b]) > 2 for b, v in load.items()): continue
                c = c0 + rq(p, mv[0], mv[1])
                if fs2 not in nf or c < nf[fs2][0]: nf[fs2] = (c, wit + ((p, tuple(mv)),) if witness else ())
        front = nf
        if not front: return None
    r = front.get(frozenset())
    return r if witness else (None if r is None else r[0])


if __name__ == '__main__':
    f = (int(sys.argv[1]), int(sys.argv[2])); D = int(sys.argv[3])
    sst, sarc, szc = pickle.load(open(R + f'fstrip_{f[0]}_{f[1]}.pkl', 'rb'))
    g = (f[1], f[0]) if f[1] > 0 else (-f[1], -f[0])
    gst, garc, gzc = pickle.load(open(R + f'fstrip_{g[0]}_{g[1]}.pkl', 'rb'))
    SL = sorted(set().union(*[c for c, g in szc])); SB = sorted(set().union(*[c for c, g in gzc]))
    tab = {}
    for a in SL:
        for b in SB:
            tab[(a, b)] = segment(f, D, sst[a], gst[b])
            print('field', f, 'D', D, 'left', a, 'bottom', b, '->', tab[(a, b)], flush=True)
    pickle.dump(tab, open(R + f'cornerseg_{f[0]}_{f[1]}_D{D}.pkl', 'wb'))
