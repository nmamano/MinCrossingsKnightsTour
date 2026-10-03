"""Gap Lemma adversary (GAP_LEMMA.md 5(d)). KT Structures, 2026-10-03.
On the p x p torus: any knight edge set with degree exactly 2 at every cell (crossings and cycles allowed).
Tiles, halves, quarters, chains, good halves and absorbing cuts exactly as in GAP_LEMMA.md (all indices mod p).
CP-SAT chooses the configuration AND a set K of absorbing cuts and maximises the Hall deficit
    2|K| - (number of bad quarters in the union of the gap squares (or gap halves) of K).
Max <= 0 means the Gap Lemma holds for every configuration of this torus; max > 0 prints a counterexample.
Absorbing cut test used here (equivalent to the bit definition, GAP_LEMMA.md): positions u (good), u+1..u+k (bad
squares), v = u+k+1 (good) on a chain, and x(link u,u+1) + x(link v-1,v) + k odd.
usage: python hall_torus.py p [half] [time]
"""
import sys
from ortools.sat.python import cp_model

p = int(sys.argv[1]); HALF = len(sys.argv) > 2 and sys.argv[2] == 'half'
TL_ = float(sys.argv[3]) if len(sys.argv) > 3 else 600
WS = sys.argv[4] if len(sys.argv) > 4 else '0'           # 'w' or 'wxh': squares outside [0,w)x[0,h) must be good
WX, WY = (int(t) for t in WS.split('x')) if 'x' in WS else (int(WS), int(WS))
WIN = WX
M = lambda a: a % p
m = cp_model.CpModel()
E = {}                                   # (x, y, t) -> var, t in a b c d
for x in range(p):
    for y in range(p):
        for t in 'abcd': E[(x, y, t)] = m.NewBoolVar(f'e{x}_{y}{t}')
MV = {'a': (2, 1), 'b': (1, 2), 'c': (1, -2), 'd': (2, -1)}
deg = {(x, y): [] for x in range(p) for y in range(p)}
for (x, y, t), v in E.items():
    dx, dy = MV[t]; deg[(x, y)].append(v); deg[(M(x+dx), M(y+dy))].append(v)
for c, vs in deg.items(): m.Add(sum(vs) == 2)
def halves(x, y, t):
    if t == 'a': return [((x, y), 'BR'), ((M(x+1), y), 'TL')]
    if t == 'b': return [((x, y), 'TL'), ((x, M(y+1)), 'BR')]
    if t == 'd': return [((x, M(y-1)), 'RT'), ((M(x+1), M(y-1)), 'LB')]
    if t == 'c': return [((x, M(y-1)), 'LB'), ((x, M(y-2)), 'RT')]
cov = {}
for (x, y, t), v in E.items():
    for hk in halves(x, y, t): cov.setdefault(hk, []).append(v)
SQ = [(i, j) for i in range(p) for j in range(p)]
nh = {}
for sq in SQ:
    for h in ('BR', 'TL', 'RT', 'LB'):
        nh[(sq, h)] = sum(cov.get((sq, h), []))
QH = {'B': ('BR', 'LB'), 'R': ('BR', 'RT'), 'T': ('TL', 'RT'), 'L': ('TL', 'LB')}
bad = {}
for sq in SQ:
    for q, (h1, h2) in QH.items():
        mq = nh[(sq, h1)] + nh[(sq, h2)]
        one = m.NewBoolVar('')
        m.Add(mq == 1).OnlyEnforceIf(one); m.Add(mq != 1).OnlyEnforceIf(one.Not())
        bad[(sq, q)] = one.Not()
good = {}
for sq in SQ:
    g = m.NewBoolVar('')
    qs = [bad[(sq, q)] for q in 'BRTL']
    m.AddBoolAnd([b.Not() for b in qs]).OnlyEnforceIf(g); m.AddBoolOr(qs).OnlyEnforceIf(g.Not())
    good[sq] = g
    if WIN and not (sq[0] < WX and sq[1] < WY): m.Add(g == 1)
def half_good(sq, h):
    hg = m.NewBoolVar('')
    one = m.NewBoolVar(''); m.Add(nh[(sq, h)] == 1).OnlyEnforceIf(one); m.Add(nh[(sq, h)] != 1).OnlyEnforceIf(one.Not())
    m.AddBoolAnd([good[sq], one]).OnlyEnforceIf(hg); m.AddBoolOr([good[sq].Not(), one.Not()]).OnlyEnforceIf(hg.Not())
    return hg
# chains: list of nodes and the link variable between node k and node k+1
chains = []
for j0 in range(p):                       # '/' chains through BR(0, j0)
    nodes, links = [], []
    i, j = 0, j0
    for _ in range(p):
        nodes.append(((i, j), 'BR')); links.append(E[(i, j, 'a')])
        nodes.append(((M(i+1), j), 'TL')); links.append(E[(M(i+1), j, 'b')])
        i, j = M(i+1), M(j+1)
    chains.append((nodes, links))
for j0 in range(p):                       # '\' chains through RT(0, j0)
    nodes, links = [], []
    i, j = 0, j0
    for _ in range(p):
        nodes.append(((i, j), 'RT')); links.append(E[(i, M(j+1), 'd')])
        nodes.append(((M(i+1), j), 'LB')); links.append(E[(M(i+1), M(j+1), 'c')])
        i, j = M(i+1), M(j-1)
    chains.append((nodes, links))
# sanity: every half on exactly one chain, and links really cover both neighbours
seen = set()
for nodes, links in chains:
    L = len(nodes)
    for k in range(L):
        assert nodes[k] not in seen; seen.add(nodes[k])
assert len(seen) == 4 * p * p
cuts = []                                 # (indicator, gap squares, gap halves)
for nodes, links in chains:
    L = len(nodes)
    hg = [half_good(*nd) for nd in nodes]
    for u in range(L):
        for k in range(1, L - 1):
            v = (u + k + 1) % L
            gap = [nodes[(u + i) % L] for i in range(1, k + 1)]
            ind = m.NewBoolVar('')
            conds = [hg[u], hg[v]] + [good[g[0]].Not() for g in gap]
            m.AddBoolAnd(conds).OnlyEnforceIf(ind)
            s1, s2 = links[u], links[(v - 1) % L]
            # parity: s1 + s2 + k odd
            par = m.NewIntVar(0, 1, '')
            m.Add(s1 + s2 + k == 2 * m.NewIntVar(0, L, '') + 1).OnlyEnforceIf(ind)
            sel = m.NewBoolVar('')        # chosen into K
            m.AddImplication(sel, ind)
            cuts.append((sel, gap))
used = {}
for sel, gap in cuts:
    keys = ([(g[0], q) for g in gap for q in g[1]] if HALF else [(g[0], q) for g in gap for q in 'BRTL'])
    for kq in set(keys):
        used.setdefault(kq, []).append(sel)
ubad = []
for kq, sels in used.items():
    u = m.NewBoolVar(''); m.AddBoolOr([u.Not()] + sels) if False else None
    for s in sels: m.AddImplication(s, u)
    ub = m.NewBoolVar(''); m.AddBoolAnd([u, bad[kq]]).OnlyEnforceIf(ub)
    m.AddBoolOr([u.Not(), bad[kq].Not(), ub])          # ub >= u and bad
    ubad.append(ub)
if WIN:
    if "sanity" in sys.argv: m.Add(sum(s for s, _ in cuts) >= 1)
    else: m.Add(2 * sum(s for s, _ in cuts) - sum(ubad) >= 1)     # decision: a Hall violation
else:
    m.Maximize(2 * sum(s for s, _ in cuts) - sum(ubad))
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = TL_
st = s.Solve(m)
print(f'p={p} window={WS} {"half" if HALF else "square"} version: {s.StatusName(st)}', '' if WIN else f'max deficit {s.ObjectiveValue()} (bound {s.BestObjectiveBound()})', f'cuts {len(cuts)}', flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and (WIN or s.ObjectiveValue() > 0):
    sel_edges = [k for k, v in E.items() if s.Value(v)]
    print('COUNTEREXAMPLE edges:', sel_edges)
    for sel, gap in cuts:
        if s.Value(sel): print('  cut gap', gap)
