"""Per-cut Gap Lemma adversary (GAP_LEMMA.md 9), derived from hall_torus.py. KT Structures, 2026-10-03.
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
cuts = []                                 # (ind, gap)
for nodes, links in chains:
    L = len(nodes)
    hg = [half_good(*nd) for nd in nodes]
    for u in range(L):
        for k in range(1, L - 1):
            v = (u + k + 1) % L
            gap = [nodes[(u + i) % L] for i in range(1, k + 1)]
            ind = m.NewBoolVar('')
            m.AddBoolAnd([hg[u], hg[v]] + [good[g[0]].Not() for g in gap]).OnlyEnforceIf(ind)
            s1, s2 = links[u], links[(v - 1) % L]
            eqv = m.NewBoolVar(''); m.AddBoolXOr([s1, s2, eqv])          # eqv = (s1 == s2)
            m.AddImplication(ind, eqv if k % 2 == 1 else eqv.Not())        # s1 + s2 + k odd
            cuts.append((ind, gap))
holder = {}
for ind, gap in cuts:
    for g in gap: holder.setdefault(g, []).append(ind)
ingap = {}
for g, inds in holder.items():
    v = m.NewBoolVar(''); m.AddBoolOr([v.Not()] + inds); ingap[g] = v       # v => some absorbing cut contains g
OTH = {'B': {'BR': 'LB', 'LB': 'BR'}, 'R': {'BR': 'RT', 'RT': 'BR'}, 'T': {'TL': 'RT', 'RT': 'TL'}, 'L': {'TL': 'LB', 'LB': 'TL'}}
unc = {}
def uncbad(sq, q, h):
    key = (sq, q, h)
    if key not in unc:
        u = m.NewBoolVar(''); h2 = (sq, OTH[q][h])
        lits = [bad[(sq, q)].Not(), u]
        if h2 in ingap: lits.append(ingap[h2])
        m.AddBoolOr(lits)                     # bad and not contested => u
        unc[key] = u
    return unc[key]
tgt = []
for ind, gap in cuts:
    t = m.NewBoolVar(''); m.AddImplication(t, ind)
    m.Add(sum(uncbad(g[0], q, g[1]) for g in gap for q in g[1]) <= 1).OnlyEnforceIf(t)
    tgt.append(t)
if "sanity" in sys.argv: m.Add(sum(i for i, _ in cuts) >= 1)
else: m.AddBoolOr(tgt)
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = TL_
st = s.Solve(m)
print(f'p={p} window={WS} per-cut form: {s.StatusName(st)} {"(sanity)" if "sanity" in sys.argv else ""} cuts {len(cuts)}', flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and "sanity" not in sys.argv:
    print('COUNTEREXAMPLE edges:', [k for k, v in E.items() if s.Value(v)])
    for t, (ind, gap) in zip(tgt, cuts):
        if s.Value(t): print('  target cut gap', gap)
