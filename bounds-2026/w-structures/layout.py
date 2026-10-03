"""Coarse layout search (KT Structures, 2026-10-02).
Board = k x k squares, each cut by both diagonals into 4 triangles (S,E,N,W).
Each triangle gets a line family: 0=A (x+2y=c, dir (2,-1)), 1=A' (x-2y, dir (2,1)),
2=B (2x+y, dir (1,-2)), 3=B' (2x-y, dir (1,2)).
Seam rates (crossings per unit of the seam's x-extent, or y-extent for vertical seams):
  horizontal: A|A' 0 (free), B|B' sv ; vertical: B|B' 0, A|A' sv
  diag (1,1): A'|B' 0, A|B sg ; anti (1,-1): A|B 0, A'|B' sg ; other pairs: forbidden (densities differ)
Board edges per unit: shallow family 2.0, steep 2.5.
Total cost in units of n (board side = 1)."""
import sys
from ortools.sat.python import cp_model
A, Ap, B, Bp = 0, 1, 2, 3
NAMES = ['A', "A'", 'B', "B'"]

def rates(sv, sg):
    INF = None
    R = {}
    def setr(kind, a, b, r):
        R[(kind, a, b)] = r; R[(kind, b, a)] = r
    for kind in ('h', 'v', 'd', 'a'):
        for a in range(4):
            for b in range(4):
                R[(kind, a, b)] = 0 if a == b else INF
    setr('h', A, Ap, 0); setr('h', B, Bp, sv)
    setr('v', B, Bp, 0); setr('v', A, Ap, sv)
    setr('d', Ap, Bp, 0); setr('d', A, B, sg)
    setr('a', A, B, 0); setr('a', Ap, Bp, sg)
    return R

def solve(k, sv, sg=1.0, tl=60, workers=1, SCALE=None, forbid_steep=False):
    SC = 4 * k * 100  # cost units: 1/(4k*100) of n... use length units of 1/(2k)
    m = cp_model.CpModel()
    # lab[i][j][t][f]
    L = {}
    for i in range(k):
        for j in range(k):
            for t in range(4):
                v = [m.NewBoolVar('') for _ in range(4)]
                m.AddExactlyOne(v)
                L[i, j, t] = v
    R = rates(sv, sg)
    obj = []
    def pair(c1, c2, kind, length):  # length in units of 1/(2k)
        for a in range(4):
            for b in range(4):
                r = R[(kind, a, b)]
                if r is None:
                    m.AddBoolOr([L[c1][a].Not(), L[c2][b].Not()])
                elif r > 0:
                    z = m.NewBoolVar('')
                    m.AddBoolOr([L[c1][a].Not(), L[c2][b].Not(), z])
                    obj.append(int(round(r * 100)) * length * z)
    S, E, N, W = 0, 1, 2, 3
    for i in range(k):          # i = column (x), j = row (y)
        for j in range(k):
            pair((i, j, S), (i, j, E), 'a', 1)
            pair((i, j, E), (i, j, N), 'd', 1)
            pair((i, j, N), (i, j, W), 'a', 1)
            pair((i, j, W), (i, j, S), 'd', 1)
            if i + 1 < k:
                pair((i, j, E), (i + 1, j, W), 'v', 2)
            if j + 1 < k:
                pair((i, j, N), (i, j + 1, S), 'h', 2)
    def edge(c, shallow):
        for f in range(4):
            r = 2.0 if f in shallow else 2.5
            if forbid_steep and f not in shallow:
                m.Add(L[c][f] == 0)
            obj.append(int(round(r * 100)) * 2 * L[c][f])
    for i in range(k):
        edge((i, 0, S), (A, Ap)); edge((i, k - 1, N), (A, Ap))
        edge((0, i, W), (B, Bp)); edge((k - 1, i, E), (B, Bp))
    m.Minimize(sum(obj))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = workers
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return s.StatusName(r), None, None
    lab = {c: [f for f in range(4) if s.Value(L[c][f])][0] for c in L}
    return s.StatusName(r), s.ObjectiveValue() / (100 * 2 * k), lab

def show(k, lab):
    # print each square as 'S E N W'
    rows = []
    for j in reversed(range(k)):
        rows.append(' | '.join(''.join('aAbB'[lab[i, j, t]] for t in range(4)) for i in range(k)))
    return '\n'.join(rows)

if __name__ == '__main__':
    k = int(sys.argv[1]); sv = float(sys.argv[2]); sg = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    st, cost, lab = solve(k, sv, sg, tl=float(sys.argv[4]) if len(sys.argv) > 4 else 60)
    print(k, sv, sg, st, cost)
    if lab: print(show(k, lab))

def breakdown(k, lab, sv, sg=1.0):
    R = rates(sv, sg)
    items = []
    S, E, N, W = 0, 1, 2, 3
    def chk(c1, c2, kind, length, where):
        a, b = lab[c1], lab[c2]
        r = R[(kind, a, b)]
        if a != b:
            items.append((where, kind, NAMES[a] + '|' + NAMES[b], r, r * length / (2 * k)))
    for i in range(k):
        for j in range(k):
            chk((i, j, S), (i, j, E), 'a', 1, (i, j, 'SE'))
            chk((i, j, E), (i, j, N), 'd', 1, (i, j, 'EN'))
            chk((i, j, N), (i, j, W), 'a', 1, (i, j, 'NW'))
            chk((i, j, W), (i, j, S), 'd', 1, (i, j, 'WS'))
            if i + 1 < k: chk((i, j, E), (i + 1, j, W), 'v', 2, (i, j, 'E|W'))
            if j + 1 < k: chk((i, j, N), (i, j + 1, S), 'h', 2, (i, j, 'N|S'))
    edge = 0
    for i in range(k):
        for c, sh in (((i, 0, S), (A, Ap)), ((i, k - 1, N), (A, Ap)), ((0, i, W), (B, Bp)), ((k - 1, i, E), (B, Bp))):
            edge += (2.0 if lab[c] in sh else 2.5) / k
    return edge, [it for it in items if it[3]]
