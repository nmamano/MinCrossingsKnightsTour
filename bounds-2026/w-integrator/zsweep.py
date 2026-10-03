import sys,time; sys.path.insert(0,'..')
from kt.board import build_skeleton, complete, to_grid
from kt.core import validate, num_crossings, num_turns
from kt import templates as T
H16a = ['26 26 36 36 36 36 56 26','23 36 36 36 13 23 23 23','26 26 26 27 27 27 27 26','67 67 67 67 67 67 67 67']
n = int(sys.argv[1]); tl = float(sys.argv[2])
for Z in map(int, sys.argv[3:]):
    nb, free = build_skeleton(n, H16a, T.VerticalEdge, Z=Z)
    full, info = complete(n, nb, free, time_limit=tl)
    if full:
        g = to_grid(n, full); info.update(valid=validate(g), X=num_crossings(g), T=num_turns(g))
    print(n, Z, info, flush=True)
