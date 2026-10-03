# C1 (PLAN.md): machine check of T3 (STRUCTURE.md). Plane, lattice point v = (0,0), its 4 unit squares.
# Candidate edges: all knight edges whose tile meets one of the 4 squares. Constraints: each of the 16 quarters of
# the 4 squares is covered exactly once; deg(v) = 2. (No other constraint, so the check is stronger than needed.)
# Enumerate all solutions; classify the splits of the 4 squares and the tile classes next to v.
import itertools
from collections import Counter
from ortools.sat.python import cp_model

SQ = [(-1,-1), (0,-1), (-1,0), (0,0)]          # lower-left corners: SW, SE, NW, NE
QC = {'B': (.5,.2), 'R': (.8,.5), 'T': (.5,.8), 'L': (.2,.5)}

def tile(e):
    (x,y),(u,w) = e; dx, dy = u-x, w-y
    mx, my = x+dx/2, y+dy/2
    if abs(dx) == 2: u0, u1 = (mx, my-.5), (mx, my+.5)
    else:            u0, u1 = (mx-.5, my), (mx+.5, my)
    return [(x,y), u0, (u,w), u1]

def inside(poly, pt):
    s = [(poly[(k+1)%4][0]-poly[k][0])*(pt[1]-poly[k][1]) - (poly[(k+1)%4][1]-poly[k][1])*(pt[0]-poly[k][0]) for k in range(4)]
    return all(v > 1e-9 for v in s) or all(v < -1e-9 for v in s)

def quarters(e):
    P = tile(e); out = []
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    for i in range(int(min(xs))-1, int(max(xs))+1):
        for j in range(int(min(ys))-1, int(max(ys))+1):
            for nm, (cx, cy) in QC.items():
                if inside(P, (i+cx, j+cy)): out.append((i, j, nm))
    assert len(out) == 4
    return out

MOV = [(1,2),(2,1),(2,-1),(1,-2)]
cand = []
for x in range(-4, 5):
    for y in range(-4, 5):
        for dx, dy in MOV:
            e = ((x,y),(x+dx,y+dy))
            if any((i,j) in SQ for (i,j,_) in quarters(e)): cand.append(e)
cls = lambda e: '/' if (e[1][0]-e[0][0])*(e[1][1]-e[0][1]) > 0 else '\\'
m = cp_model.CpModel(); X = {e: m.NewBoolVar('') for e in cand}
for (i,j) in SQ:
    for nm in 'BRTL':
        m.Add(sum(X[e] for e in cand if (i,j,nm) in quarters(e)) == 1)
m.Add(sum(X[e] for e in cand if (0,0) in e) == 2)
sols = []
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(s): sols.append([e for e in cand if s.Value(X[e])])
s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
st = s.Solve(m, CB())
print('candidates', len(cand), s.StatusName(st), 'solutions', len(sols))

def split_of(sol, sq):
    ks = {cls(e) for e in sol if any((i,j) == sq for (i,j,_) in quarters(e))}
    assert len(ks) == 1, 'T1 fails'
    return ks.pop()

pat = Counter(); forced = Counter()
for sol in sols:
    sw, se, nw, ne = (split_of(sol, q) for q in SQ)
    if sw == se == nw == ne: kind = 'no wall'
    elif sw == se and nw == ne: kind = 'horizontal wall'
    elif sw == nw and se == ne: kind = 'vertical wall'
    else: kind = 'TURN OR 4-WALL'
    pat[kind] += 1
    if kind != 'no wall':
        # the tiles whose short diagonal is a unit edge at v, and their move type
        carried = sorted({(e[1][0]-e[0][0], e[1][1]-e[0][1]) for e in sol
                          if (0,0) in [tuple(map(float, p)) for p in (tile(e)[1], tile(e)[3])]})
        forced[(kind, tuple(carried))] += 1
print(dict(pat))
for k, v in sorted(forced.items()): print(v, k)
assert pat['TURN OR 4-WALL'] == 0
print('T3 check passed: at a good point (4 good squares, deg 2) a wall is straight; no turn, no 4-wall, no end.')
# angle identity: exactly b(v) = 2 unit edges at v are short diagonals of tiles, in every solution
bs = Counter(sum(1 for e in sol if (0.0,0.0) in (tile(e)[1], tile(e)[3])) for sol in sols)
print('b(v) distribution', dict(bs)); assert set(bs) == {2}
