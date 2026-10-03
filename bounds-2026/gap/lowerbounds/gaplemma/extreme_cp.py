"""[KT Lower Bounds copy of KT Structures tree_leaf.py, modified: S = (0,0) is an EXTREME square of U for the
functional PHI (no U square in the window has larger PHI), optional uniform split SIG for all U neighbours,
objective = bad quarters of S. usage: extreme_cp.py W PHI SIG|any RHO [time]; objective = excess of U squares within Chebyshev RHO of S   PHI in x+y, x-y, x, y]

Leaf excess test for the Tree Lemma (GAP_LEMMA.md 11). KT Structures, 2026-10-03.
Deficit scenario: U = gap squares of a cut set K, a tree polyomino (no 2x2 block), every boundary side of U an end
of a cut of K (so every non-U square next to U is good). Plane model around a leaf S = (0,0) with S' = (1,0) in U
and the left/top/bottom neighbours of S not in U. Squares in the window: inU free (S, S' fixed), no 2x2 block of U;
inU -> bad; a non-U square next to a U square -> good. For every boundary side (U square A, non-U neighbour T of
split sigma) the sigma-chain from T through A is followed while inside the window: the first non-U square reached
must be good with split sigma, and then the cut must be absorbing (L2). Variables: all knight edges with an endpoint
in the point box; degree exactly 2 on the box (a relaxation, so a lower bound found here is a proof for the window).
Objective: minimise the excess sum (b(A) - 2) over U squares A within Chebyshev distance RHO of S.
usage: python tree_leaf.py W RHO [time]
"""
import sys
from ortools.sat.python import cp_model
W = int(sys.argv[1]); PHI = sys.argv[2]; SIG = sys.argv[3]; RHO = int(sys.argv[4]); TLIM = float(sys.argv[5]) if len(sys.argv) > 5 else 600
PF = {'x+y': lambda s: s[0] + s[1], 'x-y': lambda s: s[0] - s[1], 'x': lambda s: s[0], 'y': lambda s: s[1]}[PHI]
MV = {'a': (2, 1), 'b': (1, 2), 'c': (1, -2), 'd': (2, -1)}
def halves(x, y, t):
    if t == 'a': return [((x, y), 'BR'), ((x+1, y), 'TL')]
    if t == 'b': return [((x, y), 'TL'), ((x, y+1), 'BR')]
    if t == 'd': return [((x, y-1), 'RT'), ((x+1, y-1), 'LB')]
    if t == 'c': return [((x, y-1), 'LB'), ((x, y-2), 'RT')]
QH = {'B': ('BR', 'LB'), 'R': ('BR', 'RT'), 'T': ('TL', 'RT'), 'L': ('TL', 'LB')}
DIRS = {'B': (0, -1), 'R': (1, 0), 'T': (0, 1), 'L': (-1, 0)}
OPP = {'B': 'T', 'T': 'B', 'L': 'R', 'R': 'L'}
SPL = {'/': ('BR', 'TL'), '\\': ('RT', 'LB')}
def main():
    m = cp_model.CpModel()
    sqs = [(i, j) for i in range(-W, W + 2) for j in range(-W, W + 1)]
    SQ = set(sqs)
    lo_x, hi_x = -W - 2, W + 4; lo_y, hi_y = -W - 2, W + 3
    box = [(x, y) for x in range(lo_x, hi_x + 1) for y in range(lo_y, hi_y + 1)]
    E = {}
    for (x, y) in box:
        for t, (dx, dy) in MV.items():
            for e in ((x, y, t), (x - dx, y - dy, t)):
                if e not in E: E[e] = m.NewBoolVar('')
    deg = {}
    for (x, y, t), v in E.items():
        dx, dy = MV[t]; deg.setdefault((x, y), []).append(v); deg.setdefault((x+dx, y+dy), []).append(v)
    BOX = set(box)
    for pt, vs in deg.items(): m.Add(sum(vs) == 2) if pt in BOX else m.Add(sum(vs) <= 2)
    cov = {}
    for (x, y, t), v in E.items():
        for hk in halves(x, y, t): cov.setdefault(hk, []).append(v)
    nh = lambda sq, h: sum(cov.get((sq, h), []))
    def isone(expr):
        b = m.NewBoolVar(''); m.Add(expr == 1).OnlyEnforceIf(b); m.Add(expr != 1).OnlyEnforceIf(b.Not()); return b
    bad, good, gs = {}, {}, {}
    for sq in sqs:
        for q, (h1, h2) in QH.items(): bad[(sq, q)] = isone(nh(sq, h1) + nh(sq, h2)).Not()
        g = m.NewBoolVar(''); qs = [bad[(sq, q)] for q in 'BRTL']
        m.AddBoolAnd([b.Not() for b in qs]).OnlyEnforceIf(g); m.AddBoolOr(qs).OnlyEnforceIf(g.Not()); good[sq] = g
        o = isone(nh(sq, 'BR'))
        sl = m.NewBoolVar(''); m.AddBoolAnd([g, o]).OnlyEnforceIf(sl); m.AddBoolOr([g.Not(), o.Not()]).OnlyEnforceIf(sl.Not())
        bs = m.NewBoolVar(''); m.AddBoolAnd([g, o.Not()]).OnlyEnforceIf(bs); m.AddBoolOr([g.Not(), o]).OnlyEnforceIf(bs.Not())
        gs[(sq, '/')], gs[(sq, '\\')] = sl, bs
    inU = {sq: m.NewBoolVar('') for sq in sqs}
    S = (0, 0)
    m.Add(inU[S] == 1)
    for sq in sqs:
        if PF(sq) > PF(S): m.Add(inU[sq] == 0)
    for sq in sqs:
        m.AddImplication(inU[sq], good[sq].Not())
        for d in DIRS.values():
            nb = (sq[0] + d[0], sq[1] + d[1])
            if nb in SQ: m.AddBoolOr([inU[sq].Not(), inU[nb], good[nb]])      # U square, nb not in U -> nb good
            if nb in SQ and SIG != 'any': m.AddBoolOr([inU[sq].Not(), inU[nb], gs[(nb, SIG)]])
        blk = [(sq[0] + a, sq[1] + b) for a in (0, 1) for b in (0, 1)]
        if all(x in SQ for x in blk): m.AddBoolOr([inU[x].Not() for x in blk])
    # ends: follow chains
    def link_var(h1, h2):
        r = [v for kk, v in E.items() if h1 in halves(*kk) and h2 in halves(*kk)]
        assert len(r) == 1, (h1, h2); return r[0]
    for A in sqs:
        for s, d in DIRS.items():
            T = (A[0] + d[0], A[1] + d[1])
            if T not in SQ: continue
            for sig in ('/', '\\'):
                c = m.NewBoolVar('')       # A in U, T not in U, T good split sig
                m.AddBoolAnd([inU[A], inU[T].Not(), gs[(T, sig)]]).OnlyEnforceIf(c)
                m.AddBoolOr([inU[A].Not(), inU[T], gs[(T, sig)].Not(), c])
                hT = (T, [h for h in SPL[sig] if OPP[s] in h][0])
                nodes = [hT]; cur_sq, enter = A, s
                prefix = [c]
                while True:
                    h = [hh for hh in SPL[sig] if enter in hh][0]
                    nodes.append((cur_sq, h))
                    out = [ch for ch in h if ch != enter][0]
                    nxt = (cur_sq[0] + DIRS[out][0], cur_sq[1] + DIRS[out][1])
                    if nxt not in SQ: break
                    hn = (nxt, [hh for hh in SPL[sig] if OPP[out] in hh][0])
                    # if all so far in U and nxt not in U: nxt good split sig, and parity
                    stop = m.NewBoolVar('')
                    m.AddBoolAnd(prefix + [inU[nxt].Not()]).OnlyEnforceIf(stop)
                    m.AddBoolOr([p.Not() for p in prefix] + [inU[nxt], stop])
                    m.AddImplication(stop, gs[(nxt, sig)])
                    k = len(nodes) - 1
                    y0 = link_var(nodes[0], nodes[1]); yk = link_var(nodes[-1], hn)
                    par = m.NewIntVar(0, 2, ''); 
                    pv = m.NewBoolVar(''); m.Add(y0 + yk + k == 2 * par + 1).OnlyEnforceIf(stop)
                    nodes_next = nxt
                    prefix = prefix + [inU[nxt]]
                    cur_sq, enter = nxt, OPP[out]
    exc = []
    for A in sqs:
        if max(abs(A[0]), abs(A[1])) > RHO: continue
        b = sum(bad[(A, q)] for q in 'BRTL')
        e = m.NewIntVar(0, 2, ''); m.Add(e == b - 2).OnlyEnforceIf(inU[A]); m.Add(e == 0).OnlyEnforceIf(inU[A].Not())
        exc.append(e)
    m.Minimize(sum(exc))
    sv = cp_model.CpSolver(); sv.parameters.num_workers = 2; sv.parameters.max_time_in_seconds = TLIM
    st = sv.Solve(m)
    print(f'W={W} PHI={PHI} SIG={SIG}: {sv.StatusName(st)} RHO={RHO} min excess near S {sv.ObjectiveValue()} bound {sv.BestObjectiveBound()}', flush=True)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for j in range(W, -W - 1, -1):
            row = ''
            for i in range(-W, W + 2):
                sq = (i, j)
                if sv.Value(inU[sq]): row += str(sum(sv.Value(bad[(sq, q)]) for q in 'BRTL'))
                elif sv.Value(good[sq]): row += '/' if sv.Value(gs[(sq, '/')]) else '\\'
                else: row += 'x'
            print('  ' + row)
main()
