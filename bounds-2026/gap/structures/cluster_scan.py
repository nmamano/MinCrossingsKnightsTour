"""R5-count pilot (PLAN.md section 5): in real tours, how many ribbon-run ends does each bad cluster absorb, and what
does it cost locally? KT Structures, 2026-10-03.
For a validated tour: quarter multiplicities from exact tile geometry; good squares and splits (STRUCTURE.md T1);
ribbon chains of halves ('/' : BR(i,j)-TL(i+1,j), TL(i,j-1); '\\' : RT(i,j)-LB(i+1,j), LB(i,j+1)); a half is good if
its square is good with that split. A RUN END is a pair (good half g, chain neighbour h) with h not good and h inside
the board; it is a WALL end if h's square is good (other split), else a DEFECT end, assigned to h's square.
Bad clusters = 4-connected components of bad squares. Per cluster: bad quarters bq, holes G, X1 and W3 charged at
their quarters (an X1 pair is charged once, at its single overlap quarter), local E-cost c = (G + X1 + W3)/2
(identity (I) of gap/searcher/PLAN.md), and defect ends. Clusters within distance 3 of the board side are reported
separately (side collar).
usage: python cluster_scan.py tourfile.json [more files]
"""
import sys, json, os
ALLCUTS = os.environ.get("ALLCUTS") == "1"
PARITY_OK = [0]
from collections import Counter as _C
ENTRY = _C()
from collections import defaultdict
sys.path.insert(0, '../../w-verifier')
from check import MOVES

def load(path):
    d = json.load(open(path)); tour = d['tour']; n = len(tour); es = set()
    for row, line in enumerate(tour):
        for col, code in enumerate(line):
            for v in code:
                dy, dx = MOVES[int(v)]
                a, b = (col, n-1-row), (col+dx, n-1-row-dy)
                es.add((min(a, b), max(a, b)))
    return n, sorted(es)

def halves(e):
    """the two (square, half) pairs of the tile of e (STRUCTURE.md Lemma 0)."""
    (x, y), (u, w) = e
    dx, dy = u-x, w-y
    if (dx, dy) == (2, 1):   return [((x, y), 'BR'), ((x+1, y), 'TL')]
    if (dx, dy) == (1, 2):   return [((x, y), 'TL'), ((x, y+1), 'BR')]
    if (dx, dy) == (2, -1):  return [((x, y-1), 'RT'), ((x+1, y-1), 'LB')]
    if (dx, dy) == (1, -2):  return [((x, y-1), 'LB'), ((x, y-2), 'RT')]
    raise ValueError(e)

QOF = {'BR': 'BR', 'TL': 'TL', 'RT': 'RT', 'LB': 'LB'}
def cross(e, f):
    def o(p, q, r):
        v = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]); return (v > 0) - (v < 0)
    p1, p2 = e; q1, q2 = f
    if len({p1, p2, q1, q2}) < 4: return False
    return o(p1, p2, q1)*o(p1, p2, q2) < 0 and o(q1, q2, p1)*o(q1, q2, p2) < 0

def scan(path):
    n, es = load(path)
    owners = defaultdict(list)           # (square, quarter) -> tiles
    for e in es:
        for sq, h in halves(e):
            for qd in h: owners[(sq, qd)].append(e)
    squares = [(i, j) for i in range(n-1) for j in range(n-1)]
    m = {(sq, qd): len(owners[(sq, qd)]) for sq in squares for qd in 'BRTL'}
    good, split = {}, {}
    for sq in squares:
        g = all(m[(sq, qd)] == 1 for qd in 'BRTL')
        good[sq] = g
        if g:
            split[sq] = '/' if owners[(sq, 'B')][0] == owners[(sq, 'R')][0] else '\\'
    def half_good(sq, h):
        return sq in good and good[sq] and split[sq] == ('/' if h in ('BR', 'TL') else '\\')
    def nbrs(sq, h):
        i, j = sq
        return {'BR': [((i+1, j), 'TL'), ((i, j-1), 'TL')], 'TL': [((i-1, j), 'BR'), ((i, j+1), 'BR')],
                'RT': [((i+1, j), 'LB'), ((i, j+1), 'LB')], 'LB': [((i-1, j), 'RT'), ((i, j-1), 'RT')]}[h]
    ends = defaultdict(int); wall_ends = 0; same_bit_gaps = 0; mixed_gaps = 0; gaps = []; gaph = []
    # bit of a good half: H if its tile crosses a vertical unit edge (a or d), else V
    def bit(sq, h):
        e = owners[(sq, h[0])][0]
        return 'H' if abs(e[1][0]-e[0][0]) == 2 else 'V'
    def state(sq, h):
        if sq not in good: return 'O'
        if half_good(sq, h): return 'G'
        return 'W' if good[sq] else 'B'
    # enumerate chains: '/' chain k = j - i (BR(i,j), TL(i+1,j), ...); '\' chain from RT(i,j) -> LB(i+1,j) -> RT(i+1,j-1)...
    # simpler: build chains by union over nodes, ordering by the first neighbour
    FWD = {'BR': 0, 'TL': 1, 'RT': 0, 'LB': 1}; BWD = {h: 1-v for h, v in FWD.items()}
    visited = set()
    for sq0 in squares:
        for h0 in ('BR', 'TL', 'RT', 'LB'):
            if (sq0, h0) in visited: continue
            # go backwards to the chain start
            cur = (sq0, h0); back = []
            while True:
                b = nbrs(*cur)[BWD[cur[1]]]
                if b[0] not in good: break
                cur = b
            seq = [cur]; visited.add(cur)
            while True:
                nb = nbrs(*seq[-1])[FWD[seq[-1][1]]]
                if nb[0] not in good: break
                seq.append(nb); visited.add(nb)
            st = [state(*z) for z in seq]
            runs = []   # (start, end) indices of G runs
            k = 0
            while k < len(seq):
                if st[k] == 'G':
                    a = k
                    while k < len(seq) and st[k] == 'G': k += 1
                    runs.append((a, k-1))
                else: k += 1
            for (a1, b1), (a2, b2) in zip(runs, runs[1:]):
                gap = st[b1+1:a2]
                if all(g == 'B' for g in gap):
                    def linked(gz, hz):
                        e = owners[(gz[0], gz[1][0])][0]
                        return hz in [(sq_, h_) for sq_, h_ in halves(e)]
                    par = (linked(seq[b1], seq[b1+1]) + linked(seq[a2], seq[a2-1]) + (a2 - b1 - 1)) % 2 == 1
                    assert par == (bit(*seq[b1]) != bit(*seq[a2])), 'parity rule'
                    PARITY_OK[0] += 1
                    if bit(*seq[b1]) != bit(*seq[a2]):
                        def entry_q(gz, hz):
                            # quarter of hz's square next to the side shared with gz's square
                            (gi_, gj_), (hi_, hj_) = gz[0], hz[0]
                            side = {(1, 0): 'R', (-1, 0): 'L', (0, 1): 'T', (0, -1): 'B'}[(gi_ - hi_, gj_ - hj_)]
                            return (hz[0], side)
                        eq = [entry_q(seq[b1], seq[b1+1]), entry_q(seq[a2], seq[a2-1])]
                        ENTRY[sum(1 for kq in eq if m[kq] != 1)] += 1
                        ends[seq[b1+1][0]] += 2
                        gaps.append([z[0] for z in seq[b1+1:a2]]); gaph.append(seq[b1+1:a2])
                    else: same_bit_gaps += 1
                else: mixed_gaps += 1
            for k in range(len(seq)-1):
                if st[k] == 'G' and st[k+1] == 'W' or st[k] == 'W' and st[k+1] == 'G': wall_ends += 1
    # local costs at quarters
    G = defaultdict(int); W3 = defaultdict(int); X1 = defaultdict(int)
    for (sq, qd), k in m.items():
        if k == 0: G[sq] += 1
        if k >= 3: W3[sq] += (k-1)*(k-2)//2
    # X1: crossing pairs with a one-quarter overlap; charge at that quarter
    pairq = defaultdict(list)
    for (sq, qd), tl in owners.items():
        for a in range(len(tl)):
            for b in range(a+1, len(tl)):
                pairq[(tl[a], tl[b]) if tl[a] < tl[b] else (tl[b], tl[a])].append(sq)
    PX = defaultdict(float)                 # crossing pairs, split equally over their overlap quarters
    for pr, qs in pairq.items():
        if len(qs) == 1: X1[qs[0]] += 1
        for sq in qs: PX[sq] += 1.0 / len(qs)
    # clusters
    bad = [sq for sq in squares if not good[sq]]
    seen = set(); out = []
    for s0 in bad:
        if s0 in seen: continue
        comp = [s0]; seen.add(s0); k = 0
        while k < len(comp):
            i, j = comp[k]; k += 1
            for t in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                if t in good and not good[t] and t not in seen: seen.add(t); comp.append(t)
        side = any(min(i, j, n-2-i, n-2-j) <= 3 for (i, j) in comp)
        bq = sum(1 for sq in comp for qd in 'BRTL' if m[(sq, qd)] != 1)
        c = sum(G[sq] + X1[sq] + W3[sq] for sq in comp) / 2
        en = sum(ends[sq] for sq in comp)
        px = sum(PX[sq] for sq in comp)
        out.append(dict(side=side, size=len(comp), bq=bq, cost=c, ends=en, pairs=px,
                        c_half=0.5*px + 0.5*c, c_one=px,
                        G=sum(G[s] for s in comp), X1=sum(X1[s] for s in comp), W3=sum(W3[s] for s in comp)))
    # uncontested test: a bad quarter in a gap half of cut c is uncontested if its other-split half is in no absorbing gap
    in_gap = set(z for gh in gaph for z in gh)
    other = {'B': {'BR': 'LB', 'LB': 'BR'}, 'R': {'BR': 'RT', 'RT': 'BR'}, 'T': {'TL': 'RT', 'RT': 'TL'}, 'L': {'TL': 'LB', 'LB': 'TL'}}
    from collections import Counter as _C2
    unc = _C2(); locW = _C2(); structC = _C2()
    FWD_ = {'BR': 0, 'TL': 1, 'RT': 0, 'LB': 1}
    def reach_good(z, d):
        # walk from half z along its chain in direction d (0 fwd, 1 bwd) through bad-square halves; True if a good half is reached
        cur = z
        while True:
            idx = FWD_[cur[1]] if d == 0 else 1 - FWD_[cur[1]]
            nb = nbrs(*cur)[idx]
            if nb[0] not in good: return False
            if half_good(*nb): return True
            if good[nb[0]]: return False            # wall node
            cur = nb
    def contestable(z):
        return reach_good(z, 0) and reach_good(z, 1)
    for gh in gaph:
        if not ALLCUTS and any(min(z[0][0], z[0][1], n-2-z[0][0], n-2-z[0][1]) <= 3 for z in gh): continue
        cnt = 0
        for (sq, h) in gh:
            for qd in h:
                if m[(sq, qd)] != 1 and (sq, other[qd][h]) not in in_gap: cnt += 1
        unc[min(cnt, 3)] += 1
        cw = 0
        for (sq, h) in gh:
            for qd in h:
                if m[(sq, qd)] != 1:
                    h2 = other[qd][h]
                    if any(z[0] in good and good[z[0]] and not half_good(*z) for z in nbrs(sq, h2)): cw += 1
        locW[min(cw, 3)] += 1
        cs = 0
        for (sq, h) in gh:
            for qd in h:
                if m[(sq, qd)] != 1 and not contestable((sq, other[qd][h])): cs += 1
        structC[min(cs, 3)] += 1
    print('  cuts by number of uncontested bad quarters in own halves (0/1/2/3+):', dict(sorted(unc.items())), flush=True)
    print('  cuts by number of bad quarters whose other half touches a wall node (0/1/2/3+):', dict(sorted(locW.items())), flush=True)
    print('  cuts by number of bad quarters whose other half is NOT structurally contestable (0/1/2/3+):', dict(sorted(structC.items())), flush=True)
    # matching test: each absorbing gap needs 2 distinct bad quarters lying in its own squares
    import networkx as nx
    Gr = nx.DiGraph(); need = 0
    for gi, gsq in enumerate(gaps):
        if not ALLCUTS and any(min(q[0], q[1], n-2-q[0], n-2-q[1]) <= 3 for q in gsq): continue
        Gr.add_edge('s', ('g', gi), capacity=2); need += 2
        for sq in set(gsq):
            for qd in 'BRTL':
                if m[(sq, qd)] != 1:
                    Gr.add_edge(('g', gi), ('q', sq, qd), capacity=1); Gr.add_edge(('q', sq, qd), 't', capacity=1)
    flow = nx.maximum_flow_value(Gr, 's', 't') if need else 0
    print(f'  gap matching (interior gaps): need {need}, matched {flow}', flush=True)
    Gh = nx.DiGraph(); need2 = 0; low = 0; lens = defaultdict(int)
    for gi, gh in enumerate(gaph):
        if not ALLCUTS and any(min(z[0][0], z[0][1], n-2-z[0][0], n-2-z[0][1]) <= 3 for z in gh): continue
        lens[len(gh)] += 1
        Gh.add_edge('s', gi, capacity=2); need2 += 2; own = 0
        for (sq, h) in gh:
            for qd in h:
                if m[(sq, qd)] != 1:
                    own += 1; Gh.add_edge(gi, (sq, qd), capacity=1); Gh.add_edge((sq, qd), 't', capacity=1)
        if own < 2: low += 1
    f2 = nx.maximum_flow_value(Gh, 's', 't') if need2 else 0
    print(f'  half-local matching: need {need2}, matched {f2}; cuts with < 2 bad quarters in own halves: {low}; gap lengths {dict(lens)}', flush=True)
    global ends_sq, bqs, near_side
    ends_sq = dict(ends); bqs = {sq: sum(1 for qd in 'BRTL' if m[(sq, qd)] != 1) for sq in squares}
    near_side = lambda sq: min(sq[0], sq[1], n-2-sq[0], n-2-sq[1]) <= 3
    return n, len(es), out, (wall_ends, same_bit_gaps, mixed_gaps)

if __name__ == '__main__':
    for path in sys.argv[1:]:
        n, ne, out, we = scan(path)
        inner = [c for c in out if not c['side']]
        tot = lambda L, k: sum(c[k] for c in L)
        print('parity rule checked on', PARITY_OK[0], 'bad-only gaps; absorbing cuts by number of bad entry quarters (0/1/2):', dict(ENTRY))
        print(f'{path}: n={n} edges={ne} clusters={len(out)} interior={len(inner)} wall ends, same-bit bad gaps, gaps with wall/side = {we}')
        for lab, L in (('interior', inner), ('side', [c for c in out if c['side']])):
            print(f'  {lab}: bad squares {tot(L,"size")}, bad quarters {tot(L,"bq")}, G {tot(L,"G")}, X1 {tot(L,"X1")}, '
                  f'W3 {tot(L,"W3")}, cost {tot(L,"cost")}, defect ends {tot(L,"ends")}')
        worst = sorted([c for c in inner if c['ends'] > 0], key=lambda c: c['cost'] / c['ends'])[:5]
        for c in worst:
            print(f'    lowest cost/end interior cluster: {c} -> {c["cost"]/c["ends"]:.3f} per end')
        for key, lab in (('c_half', 'lambda=1/2'), ('c_one', 'lambda=1 (crossings)')):
            r = [c[key] / c['ends'] for c in inner if c['ends'] > 0]
            print(f'  {lab}: min per absorbed end over interior clusters {min(r) if r else None:.3f}; '
                  f'total {tot(inner, key):.1f} for {tot(inner, "ends")} ends')
        r = [(c['ends'] / c['bq'], c) for c in inner if c['ends'] > 0]
        if r:
            mx = max(r, key=lambda t: t[0])
            print(f'  max absorbed ends / bad quarters over interior clusters: {mx[0]:.3f}  ({mx[1]})')
        sq_r = [(ends_sq[sq] / bqs[sq], sq) for sq in ends_sq if ends_sq[sq] > 0 and not near_side(sq)]
        if sq_r: print(f'  max per-square ends / bad quarters (interior): {max(sq_r)[0]:.3f}, squares with ratio > 1: {sum(1 for t in sq_r if t[0] > 1)}')
        zero = [c for c in inner if c['ends'] > 0 and c['cost'] == 0]
        print(f'  interior clusters with ends but zero local cost: {len(zero)}')
        X = json.load(open(path)).get('crossings')
        if X is not None:
            print(f'  identity check: total cost {tot(out,"cost")} vs E = X - 4n + 2 = {X - 4*n + 2}')
