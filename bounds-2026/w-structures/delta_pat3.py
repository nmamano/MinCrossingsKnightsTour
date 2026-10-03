import sys
from seam import Seam, build_model, cell_moves
from flux_strip import current_terms
from unroll import unroll
from ortools.sat.python import cp_model
p, D = int(sys.argv[1]), int(sys.argv[2])
st = Seam(T=(0, p), hv=(-1, 0), w1=D - 1, w2=0, f1=(2, 1), form1=(1, -2), s=1)
for cur in (-1, 1):
    m, x = build_model(st, lanes=False)
    terms, const = current_terms(st, x); m.Add(sum(terms) + const == cur)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 60
    r = s.Solve(m); ch = [i for i in range(len(x)) if s.Value(x[i])]
    adj, band = unroll(st, ch, K=8)
    # trace from side-1 entries in middle
    pairs = []
    for c in sorted(band, key=lambda c: (c[1], c[0])):
        if not (3 * p <= c[1] < 4 * p): continue
        for v in adj[c]:
            if st.side(v) == 1:
                prev, cur_ = v, c
                while st.side(cur_) == 0:
                    nx = [w for w in adj[cur_] if w != prev][0]; prev, cur_ = cur_, nx
                a = c[0] - 2 * c[1]; b = prev[0] - 2 * prev[1]
                pairs.append((a, b - a))
    print('cur', cur, 'X', s.ObjectiveValue(), 'pairs (c, partner-c):', sorted(pairs))
    dirs = cell_moves(st, ch)
    names = {(1,2):'a',(2,1):'b',(2,-1):'c',(1,-2):'d',(-1,-2):'e',(-2,-1):'f',(-2,1):'g',(-1,2):'h'}
    for y in range(p - 1, -1, -1):
        print('   ', ' '.join(''.join(sorted(names[d] for d in dirs[(xx, y)])) for xx in range(D)))
