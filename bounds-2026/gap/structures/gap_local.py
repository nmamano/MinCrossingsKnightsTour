"""Per-cut Gap Lemma for gaps of length k: local exhaustive check (GAP_LEMMA.md 9-10). KT Structures, 2026-10-03.
Plane, a '/' chain g- = node 0, gap nodes 1..k, g+ = node k+1 (start half BR(0,0) or TL(0,0)).
Region: the band squares (squares of nodes 0..k+1) and every square sharing a side with them.
Edges: every knight edge whose tile meets a region square. Degree exactly 2 at every corner of a band square,
<= 2 at other endpoints. Constraints: squares of g-, g+ good with split '/'; gap squares bad; the cut absorbs
(L2: y0 + yk + k odd, with y the chain-link edges).
Contest (relaxed in the adversary's favour): the '\\' chain crossing internal side s_i (i = 1..k-1) meets the gap in
the two quarters at s_i; the adversary may declare it contested unless one of its two outside chain neighbours is a
wall node (a half of a GOOD '/' square). Entry quarters (at s_0, s_k) are never contested (proved).
Objective: minimise the number of uncontested bad quarters in the gap halves. Claim: >= 2 for every k.
usage: python gap_local.py kmax [time]
"""
import sys, os
EXACT = os.environ.get("EXACT") == "1"
FRAC = os.environ.get("FRAC") == "1"   # objective in half units: 2 x uncontested + contested; claim >= 4
from ortools.sat.python import cp_model

def halves(e):
    (x, y), (u, w) = e
    dx, dy = u - x, w - y
    if (dx, dy) == (2, 1):   return [((x, y), 'BR'), ((x+1, y), 'TL')]
    if (dx, dy) == (1, 2):   return [((x, y), 'TL'), ((x, y+1), 'BR')]
    if (dx, dy) == (2, -1):  return [((x, y-1), 'RT'), ((x+1, y-1), 'LB')]
    if (dx, dy) == (1, -2):  return [((x, y-1), 'LB'), ((x, y-2), 'RT')]
NB = {'BR': [((1, 0), 'TL'), ((0, -1), 'TL')], 'TL': [((-1, 0), 'BR'), ((0, 1), 'BR')],
      'RT': [((1, 0), 'LB'), ((0, 1), 'LB')], 'LB': [((-1, 0), 'RT'), ((0, -1), 'RT')]}
FWD = {'BR': 0, 'TL': 1}
SIDE = {(1, 0): 'R', (-1, 0): 'L', (0, 1): 'T', (0, -1): 'B'}
OTHER = {('B', '/'): 'LB', ('R', '/'): 'RT', ('T', '/'): 'RT', ('L', '/'): 'LB'}

def run(k, start, tl):
    nodes = [((0, 0), start)]
    for _ in range(k + 1):
        (i, j), h = nodes[-1]
        (di, dj), h2 = NB[h][FWD[h]]
        nodes.append(((i+di, j+dj), h2))
    band = [nd[0] for nd in nodes]
    region = set(band)
    for (i, j) in band:
        for d in SIDE: region.add((i+d[0], j+d[1]))
    xs = [s[0] for s in region]; ys = [s[1] for s in region]
    cand = []
    for x in range(min(xs) - 3, max(xs) + 4):
        for y in range(min(ys) - 3, max(ys) + 4):
            for d in ((2, 1), (1, 2), (2, -1), (1, -2)):
                e = ((x, y), (x+d[0], y+d[1]))
                if any(sq in region for sq, _ in halves(e)): cand.append(e)
    corners = {(i+a, j+b) for (i, j) in (region if EXACT else band) for a in (0, 1) for b in (0, 1)}
    cs = set(cand)
    for (px, py) in corners:                      # every edge at a constrained point must be a candidate
        for d in ((2, 1), (1, 2), (2, -1), (1, -2)):
            for e in (((px, py), (px+d[0], py+d[1])), ((px-d[0], py-d[1]), (px, py))):
                if e not in cs: cs.add(e); cand.append(e)
    m = cp_model.CpModel(); X = {e: m.NewBoolVar('') for e in cand}
    pts = {p for e in cand for p in e}
    for p in pts:
        inc = [X[e] for e in cand if p in e]
        m.Add(sum(inc) == 2) if p in corners else m.Add(sum(inc) <= 2)
    cov = {}
    for e in cand:
        for sq, h in halves(e): cov.setdefault((sq, h), []).append(X[e])
    nh = lambda sq, h: sum(cov.get((sq, h), []))
    QH = {'B': ('BR', 'LB'), 'R': ('BR', 'RT'), 'T': ('TL', 'RT'), 'L': ('TL', 'LB')}
    bad, good, slash = {}, {}, {}
    for sq in region:
        for q, (h1, h2) in QH.items():
            one = m.NewBoolVar(''); mq = nh(sq, h1) + nh(sq, h2)
            m.Add(mq == 1).OnlyEnforceIf(one); m.Add(mq != 1).OnlyEnforceIf(one.Not())
            bad[(sq, q)] = one.Not()
        g = m.NewBoolVar('')
        m.AddBoolAnd([bad[(sq, q)].Not() for q in 'BRTL']).OnlyEnforceIf(g)
        m.AddBoolOr([bad[(sq, q)] for q in 'BRTL']).OnlyEnforceIf(g.Not())
        good[sq] = g
        sl = m.NewBoolVar('')                     # good '/' : BR covered once (then split '/')
        one_br = m.NewBoolVar(''); m.Add(nh(sq, 'BR') == 1).OnlyEnforceIf(one_br); m.Add(nh(sq, 'BR') != 1).OnlyEnforceIf(one_br.Not())
        m.AddBoolAnd([g, one_br]).OnlyEnforceIf(sl); m.AddBoolOr([g.Not(), one_br.Not()]).OnlyEnforceIf(sl.Not())
        slash[sq] = sl
    m.Add(slash[band[0]] == 1); m.Add(slash[band[-1]] == 1)
    for sq in band[1:-1]: m.Add(good[sq] == 0)
    # chain links y_0..y_k
    def link(a, b):
        for e in cand:
            hs = halves(e)
            if a in hs and b in hs: return X[e]
        raise ValueError((a, b))
    y = [link(nodes[i], nodes[i+1]) for i in range(k + 1)]
    par = m.NewIntVar(0, k + 2, ''); m.Add(y[0] + y[k] + k == 2 * par + 1)
    # quarters of the gap halves and contests
    unc = []; halfs = []
    for i in range(1, k + 1):
        sq, h = nodes[i]
        for nbi in (i - 1, i + 1):
            nsq = nodes[nbi][0]
            q = SIDE[(nsq[0] - sq[0], nsq[1] - sq[1])]
            if nbi in (0, k + 1):
                unc.append(bad[(sq, q)])                      # entry quarter: never contested
                continue
            # crossing '\' chain at the side between sq and nsq: its halves v (in sq) and w (in nsq)
            v = (sq, OTHER[(q, '/')])
            qo = SIDE[(sq[0] - nsq[0], sq[1] - nsq[1])]
            w = (nsq, OTHER[(qo, '/')])
            outs = []
            for z in (v, w):
                for (d, h2) in NB[z[1]]:
                    o = ((z[0][0] + d[0], z[0][1] + d[1]), h2)
                    if o[0] not in (sq, nsq): outs.append(o)
            assert len(outs) == 2
            c = m.NewBoolVar('')                              # contested
            for o in outs:
                if o[0] in slash: m.AddImplication(c, slash[o[0]].Not())
            u = m.NewBoolVar(''); m.AddBoolOr([bad[(sq, q)].Not(), c, u])    # bad and not contested => counted
            unc.append(u)
            cb = m.NewBoolVar(''); m.AddBoolOr([bad[(sq, q)].Not(), c.Not(), cb])   # bad and contested => half
            halfs.append(cb)
    m.Minimize(2 * sum(unc) + (sum(halfs) if FRAC else 0))
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = tl
    st = s.Solve(m)
    if os.environ.get('SHOW') == '1' and st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('  nodes', nodes)
        print('  y', [s.Value(v) for v in y])
        print('  edges', sorted(e for e in cand if s.Value(X[e])))
        rows = []
        for yy in range(max(ys), min(ys) - 1, -1):
            r = ''
            for xx in range(min(xs), max(xs) + 1):
                sq = (xx, yy)
                if sq not in region: r += '  .'; continue
                tag = ('/' if s.Value(slash[sq]) else '\\') if s.Value(good[sq]) else 'X'
                r += ('*' if sq in band else ' ') + tag.ljust(2)
            rows.append(r)
        print('\n'.join(rows))
    return s.StatusName(st), (s.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None), s.BestObjectiveBound()

if __name__ == '__main__':
    kmax = int(sys.argv[1]); tl = float(sys.argv[2]) if len(sys.argv) > 2 else 300
    for k in range(1, kmax + 1):
        for start in ('BR', 'TL'):
            print(f'k={k} start={start}:', *run(k, start, tl), flush=True)
