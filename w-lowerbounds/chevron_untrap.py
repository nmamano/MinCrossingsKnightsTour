"""Spiral/untrapping experiment (2026-10-02). Free region = the left-edge chevron region of the
fold 2-factor (cells of closed loops that touch only the left edge, plus the midpoint defect
cells, plus a margin). Outside fixed. Compare min crossings in the region (a) allowing closed
cycles inside the region, (b) forbidding any cycle that lies inside the region (lazy cuts)."""
import sys, time
from collections import defaultdict, Counter
from ortools.sat.python import cp_model
import networkx as nx
from strip_dp import cross
from fold_complete2 import base, MOVES
n = int(sys.argv[1]); margin = int(sys.argv[2]); tl = int(sys.argv[3]) if len(sys.argv) > 3 else 600
E, deg = base(n, ts=(-1, -1, -1, -1), ms=(0, 1, 0, 1))
on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
X, Y0, Y1 = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
free = {(x, y) for x in range(X) for y in range(Y0, Y1)}
G = nx.Graph(); G.add_edges_from(E)
inside0 = [c for c in nx.connected_components(G) if c <= free and all(deg[p] == 2 for p in c)]
print('base closed loops inside region:', len(inside0), sorted(len(c) for c in inside0))
fixed = [e for e in E if e[0] not in free and e[1] not in free]
cand = set()
for p in free:
    for dx, dy in MOVES:
        q = (p[0] + dx, p[1] + dy)
        if on(q):
            e = tuple(sorted([p, q]))
            if q in free or e in E:
                cand.add(e)
cand = sorted(cand)
print(f'n={n} free cells {len(free)}, cand edges {len(cand)}', flush=True)
def model():
    m = cp_model.CpModel(); xv = {e: m.NewBoolVar('') for e in cand}
    inc = defaultdict(list)
    for e in cand: inc[e[0]].append(e); inc[e[1]].append(e)
    for p in free: m.Add(sum(xv[e] for e in inc[p]) == 2)
    for e in cand:
        if not (e[0] in free and e[1] in free): m.Add(xv[e] == 1)
    seg = lambda e: (*e[0], *e[1])
    terms = []
    for i, e in enumerate(cand):
        for f in cand[i + 1:]:
            if abs(e[0][0] - f[0][0]) <= 3 and abs(e[0][1] - f[0][1]) <= 3 and cross(seg(e), seg(f)):
                z = m.NewBoolVar(''); m.AddBoolOr([xv[e].Not(), xv[f].Not(), z]); terms.append(z)
        for f in fixed:
            if abs(e[0][0] - f[0][0]) <= 3 and abs(e[0][1] - f[0][1]) <= 3 and cross(seg(e), seg(f)):
                terms.append(xv[e])
    m.Minimize(sum(terms))
    return m, xv
def run(cuts):
    m, xv = model(); t0 = time.time(); rounds = 0
    while True:
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tl
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return s.StatusName(st), None, None, None
        ch = [e for e in cand if s.Value(xv[e])]
        H = nx.Graph(); H.add_edges_from(set(ch) | set(fixed))
        inside = [c for c in nx.connected_components(H) if c <= free]
        if not cuts or not inside:
            return s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(), (len(inside), ch, rounds)
        for c in inside:
            cut = [e for e in cand if (e[0] in c) != (e[1] in c)]
            m.Add(sum(xv[e] for e in cut) >= 2)
        rounds += 1
for cuts in (False, True):
    st, obj, bd, info = run(cuts)
    print(f'cycles inside region {"FORBIDDEN" if cuts else "allowed"}: {st} crossings {obj} bound {bd} '
          f'closed cycles inside {info[0] if info else None} cut rounds {info[2] if info else None}', flush=True)
    if cuts and info:
        import pickle; pickle.dump(info[1], open(f'chevron_untrap_{n}.pkl', 'wb'))
