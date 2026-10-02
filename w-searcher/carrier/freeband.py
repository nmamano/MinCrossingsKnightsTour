"""CP-SAT for a periodic band with NO terminal requirement (KT Edge Searcher, 2026-10-02).
Geometry: Seam/Band (cps_band.py). Model: degree 2 per band cell (fixed edges count), crossings
as AND variables, optional colour-current target (cps_band.cur_terms), and lazy cuts that forbid
finite cycles (quotient cycles with winding 0). Strands from terminal to terminal are allowed.
usage: freeband.py KIND p W rel tl     (rel = current relative to the plain-field current; 'none' = no target)
KINDS: c1 = band of whole lines |x - 2y| <= W in the pure (2,1) field, period T = p*(2,1), p even."""
import sys, json, time
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-searcher/carrier')
from cps_band import Band, cur_terms, chi
from seam import cell_moves
from ortools.sat.python import cp_model
KINDS = {'c1': ((1, -2), (2, 1), (2, 1), lambda p: (2 * p, p))}

def components(st, chosen):
    """quotient components: list of (is_cycle, winding, edge ids)."""
    adj = {u: [] for u in st.base}
    for i in chosen:
        u, v = st.var_edges[i]; vb, k = st.canon(v)
        adj[u].append((i, vb, k)); adj[vb].append((i, u, -k))
    seen_e, out = set(), []
    for s in st.base:
        for (i0, _, _) in adj[s]:
            if i0 in seen_e: continue
            # walk both directions from edge i0
            es, wind, cyc = [i0], 0, False
            seen_e.add(i0)
            u, v = st.var_edges[i0]; vb, k = st.canon(v)
            # forward from vb
            cur, prev, w = vb, i0, k
            while True:
                nx = [t for t in adj[cur] if t[0] != prev]
                if not nx: break
                i, nb, kk = nx[0]
                if i in seen_e:
                    cyc = True; w += kk; break
                seen_e.add(i); es.append(i); w += kk; cur, prev = nb, i
            if not cyc:   # backward from u
                cur, prev = u, i0
                while True:
                    nx = [t for t in adj[cur] if t[0] != prev]
                    if not nx: break
                    i, nb, kk = nx[0]
                    seen_e.add(i); es.append(i); cur, prev = nb, i
            out.append((cyc, w if cyc else None, es))
    return out

def run(kind, p, W, rel, tl, workers=2):
    hv, f1, f2, T = KINDS[kind]
    st = Band(T(p), hv, W, W, f1, f2)
    m = cp_model.CpModel()
    x = [m.NewBoolVar('x%d' % i) for i in range(len(st.var_edges))]
    for u in st.base:
        m.Add(sum(x[e] for e, _ in st.inc[u]) == 2 - len(st.fixed_inc[u]))
    obj, const = [], 0
    for ((ka, ia), (kb, ib)), c in st.cross.items():
        if ka == 'f' and kb == 'f': const += c
        elif ka == 'f': obj.append(c * x[ib])
        elif kb == 'f' or ia == ib: obj.append(c * x[ia])
        else:
            z = m.NewBoolVar(''); m.AddBoolOr([x[ia].Not(), x[ib].Not(), z]); obj.append(c * z)
    m.Minimize(sum(obj))
    terms, cc = cur_terms(st, x)
    # plain-field current: every line straight; for c1 there are no fixed edges, compute from the plain field
    plain = [i for i, (u, v) in enumerate(st.var_edges) if (v[0] - u[0], v[1] - u[1]) == f1]
    t0, c0 = cur_terms(st, [1 if i in set(plain) else 0 for i in range(len(x))]); cur0 = sum(t0) + c0
    if rel is not None: m.Add(sum(terms) + cc == cur0 + rel)
    t_start = time.time(); cuts = 0; hint = None
    while True:
        s = cp_model.CpSolver(); s.parameters.num_workers = workers
        s.parameters.max_time_in_seconds = max(1.0, tl - (time.time() - t_start))
        r = s.Solve(m)
        st_name = s.StatusName(r)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
        ch = [i for i in range(len(x)) if s.Value(x[i])]
        bad = [es for cyc, w, es in components(st, ch) if cyc and w == 0]
        if not bad: break
        for es in bad: m.AddBoolOr([x[i].Not() for i in es]); cuts += 1
        if time.time() - t_start > tl: st_name = 'TIMEOUT_IN_CUTS'; break
    out = dict(kind=kind, p=p, W=W, rel=rel, plain_current=cur0, status=st_name, cuts=cuts,
               secs=round(time.time() - t_start, 1), stamp=time.strftime('%Y-%m-%d %H:%M'))
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) and st_name != 'TIMEOUT_IN_CUTS':
        X, Tn = st.evaluate(ch)
        tt, c2 = cur_terms(st, [1 if i in set(ch) else 0 for i in range(len(x))])
        out.update(X=X + 0, bound=s.BestObjectiveBound() + const, rate_per_step=X / p, current=sum(tt) + c2,
                   windings=sorted(w for cyc, w, es in components(st, ch) if cyc),
                   cells={f'{u[0]},{u[1]}': ds for u, ds in cell_moves(st, ch).items()})
    return out

if __name__ == '__main__':
    kind, p, W, rel, tl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], float(sys.argv[5])
    r = run(kind, p, W, None if rel == 'none' else int(rel), tl)
    print(json.dumps({k: v for k, v in r.items() if k != 'cells'}), flush=True)
    with open('freeband.jsonl', 'a') as f: f.write(json.dumps(r) + '\n')
