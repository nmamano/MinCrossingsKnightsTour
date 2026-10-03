"""Local Entry Lemma test (GAP_LEMMA.md 11). KT Structures, 2026-10-03.
Claim: for every bad square S, b(S) >= e(S), where b(S) = number of bad quarters of S and e(S) = number of absorbing
cut ends at S (sides of S across which a cut enters its first/last gap square S). This implies the Gap Lemma
(square version, Hall form): give each cut end a distinct bad quarter of its own end square.
Plane model (a relaxation of every tour, so INFEASIBLE is a proof): S = square (0,0); variables = all knight edges
with an endpoint in the point box [-R, R+1]^2; degree exactly 2 at every point of the box. e*(S) >= e(S) counts a
side s of S with good neighbour T (split sigma) as an end if the sigma-chain through s continues inside S to the
square U across the other side s' of that half and: U good with split sigma and the half is defective (a one-half
absorbing cut, L2), or U bad (absorbing status not decided locally: counted, in the adversary's favour).
CP-SAT maximises e*(S) - b(S). Claim: max <= 0.
usage: python local_entry.py [R] [time]
"""
import sys
from ortools.sat.python import cp_model
R = int(sys.argv[1]) if len(sys.argv) > 1 else 3
TLIM = float(sys.argv[2]) if len(sys.argv) > 2 else 600
MV = {'a': (2, 1), 'b': (1, 2), 'c': (1, -2), 'd': (2, -1)}
def halves(x, y, t):
    if t == 'a': return [((x, y), 'BR'), ((x+1, y), 'TL')]
    if t == 'b': return [((x, y), 'TL'), ((x, y+1), 'BR')]
    if t == 'd': return [((x, y-1), 'RT'), ((x+1, y-1), 'LB')]
    if t == 'c': return [((x, y-1), 'LB'), ((x, y-2), 'RT')]
QH = {'B': ('BR', 'LB'), 'R': ('BR', 'RT'), 'T': ('TL', 'RT'), 'L': ('TL', 'LB')}
DIRS = {'B': (0, -1), 'R': (1, 0), 'T': (0, 1), 'L': (-1, 0)}
OPP = {'B': 'T', 'T': 'B', 'L': 'R', 'R': 'L'}
HALF_SIDES = {'BR': 'BR', 'TL': 'TL', 'RT': 'RT', 'LB': 'LB'}   # a half's two sides = its two quarter letters
def run():
    m = cp_model.CpModel()
    box = [(x, y) for x in range(-R, R + 2) for y in range(-R, R + 2)]
    E = {}
    for (x, y) in box:
        for t, (dx, dy) in MV.items():
            for e in ((x, y, t), (x - dx, y - dy, t)):
                if e not in E: E[e] = m.NewBoolVar('')
    deg = {}
    for (x, y, t), v in E.items():
        dx, dy = MV[t]; deg.setdefault((x, y), []).append(v); deg.setdefault((x+dx, y+dy), []).append(v)
    for pt in box: m.Add(sum(deg[pt]) == 2)
    for pt, vs in deg.items():
        if pt not in box: m.Add(sum(vs) <= 2)
    cov = {}
    for (x, y, t), v in E.items():
        for hk in halves(x, y, t): cov.setdefault(hk, []).append(v)
    nh = lambda sq, h: sum(cov.get((sq, h), []))
    def isone(expr):
        b = m.NewBoolVar(''); m.Add(expr == 1).OnlyEnforceIf(b); m.Add(expr != 1).OnlyEnforceIf(b.Not()); return b
    sqs = [(i, j) for i in range(-2, 3) for j in range(-2, 3)]
    bad, good, slash, bsl = {}, {}, {}, {}
    for sq in sqs:
        for q, (h1, h2) in QH.items(): bad[(sq, q)] = isone(nh(sq, h1) + nh(sq, h2)).Not()
        g = m.NewBoolVar(''); qs = [bad[(sq, q)] for q in 'BRTL']
        m.AddBoolAnd([b.Not() for b in qs]).OnlyEnforceIf(g); m.AddBoolOr(qs).OnlyEnforceIf(g.Not()); good[sq] = g
        o = isone(nh(sq, 'BR'))
        sl = m.NewBoolVar(''); m.AddBoolAnd([g, o]).OnlyEnforceIf(sl); m.AddBoolOr([g.Not(), o.Not()]).OnlyEnforceIf(sl.Not())
        bs = m.NewBoolVar(''); m.AddBoolAnd([g, o.Not()]).OnlyEnforceIf(bs); m.AddBoolOr([g.Not(), o]).OnlyEnforceIf(bs.Not())
        slash[sq], bsl[sq] = sl, bs
    S = (0, 0)
    m.Add(good[S] == 0)
    ends = []
    for s, (di, dj) in DIRS.items():
        T = (di, dj)
        for sig, gsig in (('/', slash), ('\\', bsl)):
            h = [hh for hh in (('BR', 'TL') if sig == '/' else ('RT', 'LB')) if s in hh][0]   # sigma-half of S at s
            s2 = [c for c in h if c != s][0]
            U = (DIRS[s2][0], DIRS[s2][1])
            defect = isone(nh(S, h)).Not()
            # end at s: T good split sig, and (U bad) or (U good split sig and defective)
            e = m.NewBoolVar('')
            m.AddImplication(e, gsig[T])
            ok = m.NewBoolVar('')     # (U good sig and defect)
            m.AddBoolAnd([gsig[U], defect]).OnlyEnforceIf(ok)
            m.AddBoolOr([good[U].Not(), ok]).OnlyEnforceIf(e)
            ends.append(e)
    b = sum(bad[(S, q)] for q in 'BRTL')
    m.Maximize(sum(ends) - b)
    sv = cp_model.CpSolver(); sv.parameters.num_workers = 8; sv.parameters.max_time_in_seconds = TLIM
    st = sv.Solve(m)
    print(f'R={R}: {sv.StatusName(st)} max e*-b = {sv.ObjectiveValue()} bound {sv.BestObjectiveBound()}', flush=True)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and sv.ObjectiveValue() > 0:
        for j in range(2, -3, -1):
            print(' '.join(('X' if not sv.Value(good[(i, j)]) else ('/' if sv.Value(slash[(i, j)]) else '\\')) for i in range(-2, 3)))
        print('quarters of S', {q: sv.Value(nh(S, QH[q][0]) + nh(S, QH[q][1])) for q in 'BRTL'},
              'halves', {h: sv.Value(nh(S, h)) for h in ('BR', 'TL', 'RT', 'LB')}, 'ends', [sv.Value(e) for e in ends])
run()
