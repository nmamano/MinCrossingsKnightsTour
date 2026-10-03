"""Near-edge M3: left board edge x = 0, columns 0 and 1 in pattern P (or P') on all rows of the
window; every other pair of edges touching the window must not cross. Which residues mod 3 can
phi(s_j) take, for the horizontal dual segment s_j from (j-1/2, r+1/2) to (j+1/2, r+1/2)
(directed +x, left = north)?  usage: ne_m3.py PAT r j [X]"""
import sys, itertools
from ortools.sat.python import cp_model
from strip_dp import cross
PAT, r, j = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); X = int(sys.argv[4]) if len(sys.argv) > 4 else j + 5
Y0, Y1 = r - 6, r + 8          # window rows Y0..Y1-1
KM = [(1, 2), (2, 1), (2, -1), (1, -2)]
cells = [(x, y) for x in range(0, X + 2) for y in range(Y0 - 2, Y1 + 2)]; cs = set(cells)
win = {(x, y) for x in range(X) for y in range(Y0, Y1)}
E = set()
for (x, y) in cells:
    for dx, dy in KM + [(-a, -b) for a, b in KM]:
        q = (x + dx, y + dy)
        if q in cs and ((x, y) in win or q in win):
            E.add(tuple(sorted([(x, y), q])))
E = sorted(E)
s = 1 if PAT == 'P' else -1
forced = set()
for y in range(Y0 - 4, Y1 + 4):
    for a, b in [((0, y), (2, y + s)), ((0, y), (1, y + 2 * s)), ((1, y), (3, y + s))]:
        e = tuple(sorted([a, b]))
        if e in set(E): forced.add(e)
pcells = {(x, y) for (x, y) in cells if x <= 1}
chi = lambda p: 1 if (p[0] + p[1]) % 2 == 0 else -1
A, B = (j - 0.5, r + 0.5), (j + 0.5, r + 0.5)
fl = []
for e in E:
    if cross((*A, *B), (*e[0], *e[1])):
        north = e[0] if e[0][1] > e[1][1] else e[1]
        fl.append((chi(north), e))
def model():
    m = cp_model.CpModel(); xv = {e: m.NewBoolVar('') for e in E}
    inc = {c: [] for c in cells}
    for e in E: inc[e[0]].append(e); inc[e[1]].append(e)
    for c in cells:
        if c in win: m.Add(sum(xv[e] for e in inc[c]) == 2)
        else: m.Add(sum(xv[e] for e in inc[c]) <= 2)
    for e in E:
        if e in forced: m.Add(xv[e] == 1)
        elif e[0] in pcells or e[1] in pcells:
            # cells in columns 0,1 have exactly their pattern edges (inside the window range)
            if any(c in pcells and Y0 - 2 <= c[1] < Y1 + 2 for c in e): m.Add(xv[e] == 0)
    for e, f in itertools.combinations(E, 2):
        if e in forced and f in forced: continue
        if cross((*e[0], *e[1]), (*f[0], *f[1])): m.AddBoolOr([xv[e].Not(), xv[f].Not()])
    return m, xv
feas = []
for val in range(-6, 7):
    m, xv = model()
    m.Add(sum(c * xv[e] for c, e in fl) == val)
    sv = cp_model.CpSolver(); sv.parameters.num_workers = 2; sv.parameters.max_time_in_seconds = 300
    st = sv.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): feas.append(val)
    elif st != cp_model.INFEASIBLE: feas.append(f'{val}?')
print(f'PAT={PAT} r={r} j={j} X={X}: feasible phi values {feas} residues {sorted(set(v % 3 for v in feas if isinstance(v, int)))}', flush=True)
