"""Gentle seam with a parity-constrained line bijection (KT Structures, 2026-10-02).
Every strand joins A-line c (side 1, index form1.u) to B-line c' (side 2, index form2.u) with c' - c = P (mod 2)
for ONE global parity P (lanes of 3 always mix parities: s_0 = D, s_1 = D+1, s_2 = D-1).
Reports min crossings per period and saves the template.
usage: seam_par.py p w P [current]"""
import sys, json
from seam import Seam, build_model
from seam_flux import cur_terms
from ortools.sat.python import cp_model
p, w, P = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
tgt = int(sys.argv[4]) if len(sys.argv) > 4 else None
st = Seam(T=(p, p), hv=(-1, 1), w1=w, w2=w, f1=(2, -1), form1=(1, 2), f2=(1, -2), form2=(2, 1), s=1)
m, x = build_model(st, lanes=False)
dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
labs1 = [dot(st.form1, u) for u in st.terminals]
lo, hi = min(labs1) - 4 * st.delta, max(labs1) + 4 * st.delta
L = {u: m.NewIntVar(lo, hi, '') for u in st.base}
for i, (u, v) in enumerate(st.var_edges):
    vb, k = st.canon(v)
    m.Add(L[u] == L[vb] + k * st.delta).OnlyEnforceIf(x[i])
net2 = {u: [] for u in st.base}
for i, (u, v) in enumerate(st.var_edges):
    gp = m.NewBoolVar(''); gn = m.NewBoolVar(''); m.Add(gp + gn <= x[i])
    vb, k = st.canon(v)
    net2[u].append(gp - gn); net2[vb].append(gn - gp)
for u in st.base:
    sup = 0
    for d, sd in st.fixed_inc[u]:
        if sd == 1:
            m.Add(L[u] == dot(st.form1, u)); sup += 1
        else:
            z = m.NewIntVar(-10 * (hi - lo), 10 * (hi - lo), '')
            m.Add(dot(st.form2, u) - L[u] == 2 * z + P); sup -= 1
    m.Add(sum(net2[u]) == sup)
if tgt is not None:
    terms, const = cur_terms(st, x); m.Add(sum(terms) + const == tgt)
s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 300
r = s.Solve(m)
ok = r in (cp_model.OPTIMAL, cp_model.FEASIBLE)
print(f'p={p} w={w} P={P} current={tgt}: {s.StatusName(r)} X/period {s.ObjectiveValue() if ok else None} '
      f'bound {s.BestObjectiveBound() if ok else None} per unit x {s.ObjectiveValue() / p if ok else None}', flush=True)
if ok:
    ch = {i for i in range(len(x)) if s.Value(x[i])}
    t, c = cur_terms(st, [1 if i in ch else 0 for i in range(len(x))])
    cells = {'%d,%d' % u: [d for (e, d) in st.inc[u] if e in ch] + [d for d, _ in st.fixed_inc[u]] for u in st.base}
    json.dump(dict(X=s.ObjectiveValue(), current=sum(t) + c, cells=cells), open(f'gentle_par_p{p}_w{w}_P{P}.json', 'w'))
    print('  current', sum(t) + c)
