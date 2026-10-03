import sys, time
from kt.board import build_skeleton, complete, to_grid
from kt.core import validate, num_crossings, num_turns
from kt import templates as T
tpl16 = ['46 46 56 56 56 26 46 46','14 14 14 45 45 45 45 46','05 15 15 15 15 05 05 05','01 01 01 01 01 01 01 01']
cands = {'opt-heel': T.Sequence1Opt, 'cand16': tpl16}
name = sys.argv[1]; ns = [int(a) for a in sys.argv[2:]]
for n in ns:
    t0 = time.time()
    nb, free = build_skeleton(n, cands[name], T.VerticalEdge, off_L=0, Z=14)
    full, info = complete(n, nb, free, time_limit=30, verbose=False)
    if full is None:
        print(name, n, 'FAIL', info); continue
    g = to_grid(n, full)
    print(name, n, 'valid', validate(g), 'X', num_crossings(g), 'T', num_turns(g), info, round(time.time()-t0,1), flush=True)
