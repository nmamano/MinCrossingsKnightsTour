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


BOUND = 10 ** 9


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
    # edge index for bitmask frontier: (from, to) ordered pairs that can be pending
    eidx = {}
    def bit(a, b):
        k = (a, b)
        if k not in eidx: eidx[k] = len(eidx)
        return 1 << eidx[k]
    def cellmin(p):
        ds = [d for d in M if p[0] + d[0] >= 0 and p[1] + d[1] >= 0]
        return min(rq(p, a, b) for a, b in combinations(ds, 2))
    rem = [0] * (len(order) + 1)
    for i in range(len(order) - 1, -1, -1): rem[i] = rem[i + 1] + min(0, cellmin(order[i]))
    incoming = {}          # cell -> list of (bit, move from cell to source)
    def reg(a, b):
        bb = bit(a, b); incoming.setdefault(b, []).append((bb, (a[0] - b[0], a[1] - b[1]))); return bb
    m0 = 0
    for o, b in ext: m0 |= reg(o, b)
    for i, p in enumerate(order):
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if inblock(q) and pos[q] > i: reg(p, q)
    loadlist = {q: incoming.get(q, []) for q in order}
    front = {m0: 0}
    for i, p in enumerate(order):
        cands = [d for d in M if inblock((p[0] + d[0], p[1] + d[1])) and pos[(p[0] + d[0], p[1] + d[1])] > i]
        inbits = incoming.get(p, [])
        clear = 0
        for bb, mv in inbits: clear |= bb
        outbit = {d: bit(p, (p[0] + d[0], p[1] + d[1])) for d in cands}
        nf = {}
        for fs, c0 in front.items():
            if c0 + rem[i] > BOUND: continue
            base = [mv for bb, mv in inbits if fs & bb] + fint[p]
            if len(base) > 2: continue
            rest = fs & ~clear
            for extra in combinations([d for d in cands if d not in base], 2 - len(base)):
                mv = base + list(extra)
                fs2 = rest
                for d in extra: fs2 |= outbit[d]
                bad = False
                for d in extra:
                    q = (p[0] + d[0], p[1] + d[1])
                    if sum(1 for bb, mv2 in loadlist[q] if fs2 & bb) + len(fint[q]) > 2: bad = True; break
                if bad: continue
                c = c0 + rq(p, mv[0], mv[1])
                if c < nf.get(fs2, 10 ** 9): nf[fs2] = c
        front = nf
        if len(front) > 300000: print('   frontier', i, p, len(front), flush=True)
        if not front: return None
    return front.get(0)


if __name__ == '__main__':
    f = (int(sys.argv[1]), int(sys.argv[2])); D = int(sys.argv[3]); BOUND = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
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
