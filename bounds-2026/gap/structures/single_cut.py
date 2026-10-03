"""Single-cut Gap Lemma test (GAP_LEMMA.md 11). KT Structures, 2026-10-03.
p x p torus, any knight edge set with degree exactly 2 at every cell (crossings and cycles allowed); no window.
One '/' chain segment g-, h1..hk, g+ is fixed (g- = BR or TL of square (1,1)); constraints: squares of g-, g+ good
with split '/', gap squares bad, cut absorbing (L2: y0 + yk + k odd). CP-SAT minimises the number of bad quarters
in the gap halves (HALF) or gap squares (SQ). The Gap Lemma for K = {C} needs the minimum >= 2.
usage: python single_cut.py p kmin kmax [time]
"""
import sys
from ortools.sat.python import cp_model
p, k0, k1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
TLIM = float(sys.argv[4]) if len(sys.argv) > 4 else 300
MODE = sys.argv[5] if len(sys.argv) > 5 else 'HALF'
M = lambda a: a % p
MV = {'a': (2, 1), 'b': (1, 2), 'c': (1, -2), 'd': (2, -1)}
def halves(x, y, t):
    if t == 'a': return [((x, y), 'BR'), ((M(x+1), y), 'TL')]
    if t == 'b': return [((x, y), 'TL'), ((x, M(y+1)), 'BR')]
    if t == 'd': return [((x, M(y-1)), 'RT'), ((M(x+1), M(y-1)), 'LB')]
    if t == 'c': return [((x, M(y-1)), 'LB'), ((x, M(y-2)), 'RT')]
QH = {'B': ('BR', 'LB'), 'R': ('BR', 'RT'), 'T': ('TL', 'RT'), 'L': ('TL', 'LB')}
NB = {'BR': ((1, 0), 'TL'), 'TL': ((0, 1), 'BR')}           # forward '/' neighbour
def run(k, start):
    m = cp_model.CpModel()
    E = {(x, y, t): m.NewBoolVar('') for x in range(p) for y in range(p) for t in 'abcd'}
    deg = {}
    for (x, y, t), v in E.items():
        dx, dy = MV[t]; deg.setdefault((x, y), []).append(v); deg.setdefault((M(x+dx), M(y+dy)), []).append(v)
    for vs in deg.values(): m.Add(sum(vs) == 2)
    cov = {}
    for (x, y, t), v in E.items():
        for hk in halves(x, y, t): cov.setdefault(hk, []).append(v)
    nh = lambda sq, h: sum(cov[(sq, h)])
    def isone(expr):
        b = m.NewBoolVar(''); m.Add(expr == 1).OnlyEnforceIf(b); m.Add(expr != 1).OnlyEnforceIf(b.Not()); return b
    bad = {}
    for i in range(p):
        for j in range(p):
            for q, (h1, h2) in QH.items(): bad[((i, j), q)] = isone(nh((i, j), h1) + nh((i, j), h2)).Not()
    nodes = [((1, 1), start)]
    for _ in range(k + 1):
        (i, j), h = nodes[-1]; (di, dj), h2 = NB[h]; nodes.append(((M(i+di), M(j+dj)), h2))
    for sq in (nodes[0][0], nodes[-1][0]):
        for q in 'BRTL': m.Add(bad[(sq, q)] == 0)
        m.Add(nh(sq, 'BR') == 1)
    for sq, _ in nodes[1:-1]: m.AddBoolOr([bad[(sq, q)] for q in 'BRTL'])
    def link(a, b):
        r = [v for kk, v in E.items() if a in halves(*kk) and b in halves(*kk)]
        assert len(r) == 1; return r[0]
    y = [link(nodes[i], nodes[i+1]) for i in range(k + 1)]
    par = m.NewIntVar(0, k + 2, ''); m.Add(y[0] + y[k] + k == 2 * par + 1)
    if MODE == 'HALF': qs = [bad[(sq, q)] for sq, h in nodes[1:-1] for q in h]
    else: qs = [bad[(sq, q)] for sq in {nd[0] for nd in nodes[1:-1]} for q in 'BRTL']
    m.Minimize(sum(qs))
    s = cp_model.CpSolver(); s.parameters.num_workers = 8; s.parameters.max_time_in_seconds = TLIM
    st = s.Solve(m)
    return s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound()
for k in range(k0, k1 + 1):
    for start in ('BR', 'TL'):
        print(f'p={p} k={k} start={start} {MODE}:', *run(k, start), flush=True)
