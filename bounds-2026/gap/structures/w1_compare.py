# Dictionary check with LB W1 (STRUCTURE.md 5b). Hypothesis of T1-T3 only: the 16 unit squares around a 3x3 block of
# lattice points are good (all 64 quarters covered exactly once), and the 9 points have degree 2.
# Count the distinct central maps (each point -> its two edge directions). W1 counts 156 fold-stack maps.
from ortools.sat.python import cp_model
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import wall_check as W
import sys
RING = int(sys.argv[1]) if len(sys.argv) > 1 else 1
SQ = [(i, j) for i in range(-RING, 2+RING) for j in range(-RING, 2+RING)]
PTS = [(x, y) for x in range(3) for y in range(3)]
DEG = [(x, y) for x in range(1-RING, 2+RING) for y in range(1-RING, 2+RING)]
cand = []
for x in range(-5-RING, 8+RING):
    for y in range(-5-RING, 8+RING):
        for d in W.MOV:
            e = ((x, y), (x+d[0], y+d[1]))
            if any((i, j) in SQ for (i, j, _) in W.quarters(e)) or any(p in DEG for p in e): cand.append(e)
m = cp_model.CpModel(); X = {e: m.NewBoolVar('') for e in cand}
for (i, j) in SQ:
    for nm in 'BRTL':
        m.Add(sum(X[e] for e in cand if (i, j, nm) in W.quarters(e)) == 1)
for p in DEG: m.Add(sum(X[e] for e in cand if p in e) == 2)
maps = set()
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(s):
        sel = [e for e in cand if s.Value(X[e])]
        key = tuple(sorted((p, tuple(sorted((q[0]-p[0], q[1]-p[1]) for e in sel if p in e for q in e if q != p))) for p in PTS))
        maps.add(key)
s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
st = s.Solve(m, CB())
print(s.StatusName(st), 'distinct central 3x3 maps:', len(maps))

# fold-stack maps (W1 definition), generated directly
import itertools
FS = {(1,0): [(1,2),(1,-2)], (0,1): [(2,1),(-2,1)], (1,1): [(2,-1),(-1,2)], (1,-1): [(2,1),(-1,-2)]}
stack = set()
for (fa, fb), mv in FS.items():
    f = lambda p: fa*p[0] + fb*p[1]
    levels = sorted({f(p) + k for p in PTS for k in (-1, 0)})
    for ch in itertools.product(mv, repeat=len(levels)):
        c = dict(zip(levels, ch))
        key = tuple(sorted((p, tuple(sorted([tuple(-v for v in c[f(p)-1]), c[f(p)]]))) for p in PTS))
        stack.add(key)
print('fold-stack maps:', len(stack), ' good-square maps:', len(maps), ' stack subset of good:', stack <= maps)
extra = sorted(maps - stack)
import collections
def kinds(key):
    return collections.Counter(d for _, ds in key for d in ds if d[1] > 0 or (d[1] == 0 and d[0] > 0))
print('example extra maps (direction multiset):')
for k in extra[:6]: print(dict(kinds(k)), k)
