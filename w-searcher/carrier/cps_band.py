"""CP-SAT for straight carrier bands (any orientation), lane-free, with a colour-current target.
Uses KT Structures' Seam geometry/model (w-structures/seam.py) with the form checks relaxed
(lanes are not used). Current = sum over band+fixed edges straddling the transversal cut
(axis coordinate = -1/2) of chi(lower end)."""
import sys, json, time
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-structures')
import seam
from seam import Seam, build_model, cell_moves
from ortools.sat.python import cp_model
chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
class Band(Seam):
    def __init__(self, T, hv, w1, w2, f1, f2):
        self.T, self.hv, self.w1, self.w2 = T, hv, w1, w2
        self.f1, self.f2 = f1, f2
        self.form1 = self.form2 = None
        self.s, self.off1, self.off2, self.shift = 1, 0, 0, 0
        self.wall = f2 is None
        self.ax = 0 if T[0] != 0 else 1
        self._build()
def cur_terms(st, x):
    terms, const = [], 0; T = st.T; ax = st.ax
    def lo_if_straddle(a, b):
        lo, hi = (a, b) if a[ax] < b[ax] else (b, a)
        return lo if lo[ax] < 0 <= hi[ax] else None
    for i, (u, v) in enumerate(st.var_edges):
        for k in range(-8, 9):
            a = (u[0] + k * T[0], u[1] + k * T[1]); b = (v[0] + k * T[0], v[1] + k * T[1])
            lo = lo_if_straddle(a, b)
            if lo: terms.append(chi(lo) * x[i])
    for (u, v, sd) in st.fixed_edges:
        for k in range(-8, 9):
            a = (u[0] + k * T[0], u[1] + k * T[1]); b = (v[0] + k * T[0], v[1] + k * T[1])
            lo = lo_if_straddle(a, b)
            if lo: const += chi(lo)
    return terms, const
KINDS = {   # name: (hv, f1, f2, T(p))
    'vert21':  ((1, 0), (2, 1), (2, 1), lambda p: (0, p)),      # vertical band in the shallow family
    'vert12':  ((1, 0), (1, 2), (1, 2), lambda p: (0, p)),      # vertical band in the steep family
    'midfold': ((1, 0), (1, 2), (1, -2), lambda p: (0, p)),     # bottom vertical midline of the fold field
    'edgeA':   ((-1, 0), (2, 1), None, lambda p: (0, p)),       # left edge, field family (2,1) (A')
    'edgeB':   ((-1, 0), (1, 2), None, lambda p: (0, p)),       # left edge, field family (1,2)
    'diagfree':((-1, 1), (1, 2), (2, 1), lambda p: (p, p)),
    'diag21':  ((-1, 1), (2, 1), (2, 1), lambda p: (p, p)),     # band along (1,1) inside one family
    'diag12':  ((-1, 1), (1, 2), (1, 2), lambda p: (p, p)),
    'anti21':  ((1, 1), (2, 1), (2, 1), lambda p: (p, -p)),     # band along (1,-1)
    'anti12':  ((1, 1), (1, 2), (1, 2), lambda p: (p, -p)),
}
# bands along a direction v inside the uniform (2,1) field (KT Edge Searcher, 2026-10-02): kind 'd21_a_b', T = p*v
for _v in [(2, -1), (1, -2), (3, -1), (1, -3), (1, 2), (3, 1), (3, 2), (2, 3), (3, -2), (2, -3)]:
    KINDS['d21_%d_%d' % _v] = ((_v[1], -_v[0]), (2, 1), (2, 1), (lambda v: (lambda p: (p * v[0], p * v[1])))(_v))
def run(kind, p, w1, w2, tgt, tl):
    hv, f1, f2, T = KINDS[kind]
    st = Band(T(p), hv, w1, w2, f1, f2)
    m, x = build_model(st, lanes=False)
    if tgt is not None:
        terms, const = cur_terms(st, x); m.Add(sum(terms) + const == tgt)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = tl
    r = s.Solve(m)
    out = dict(kind=kind, p=p, w1=w1, w2=w2, current=tgt, status=s.StatusName(r), stamp=time.strftime('%Y-%m-%d %H:%M'))
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = [i for i in range(len(x)) if s.Value(x[i])]
        X, Tn = st.evaluate(ch)
        t0, c0 = cur_terms(st, [1 if i in set(ch) else 0 for i in range(len(x))]); out['current'] = sum(t0) + c0
        out.update(X=X, bound=s.BestObjectiveBound(), rate=X / p, cells={f'{u[0]},{u[1]}': ds for u, ds in cell_moves(st, ch).items()})
    return out
def sweep(kind, ps, ws, tl, rel=(1, -1, 2, -2)):
    for w1, w2 in ws:
        for p in ps:
            base = run(kind, p, w1, w2, None, tl)
            print(json.dumps({k: v for k, v in base.items() if k != 'cells'}), flush=True)
            with open('band_cps.jsonl', 'a') as f: f.write(json.dumps(dict(base, rel=0)) + '\n')
            if 'X' not in base: continue
            for d in rel:
                r = run(kind, p, w1, w2, base['current'] + d, tl); r['rel'] = d; r['base_current'] = base['current']
                print(json.dumps({k: v for k, v in r.items() if k != 'cells'}), flush=True)
                with open('band_cps.jsonl', 'a') as f: f.write(json.dumps(r) + '\n')
if __name__ == '__main__' and sys.argv[1] == 'sweep':
    kind = sys.argv[2]; ps = json.loads(sys.argv[3]); ws = json.loads(sys.argv[4]); tl = float(sys.argv[5])
    sweep(kind, ps, [tuple(w) for w in ws], tl)
elif __name__ == '__main__':
    for spec in sys.argv[1:]:
        kind, p, w1, w2, tgt, tl = spec.split(':')
        r = run(kind, int(p), int(w1), int(w2), None if tgt == 'none' else int(tgt), float(tl))
        print(json.dumps({k: v for k, v in r.items() if k != 'cells'}), flush=True)
        with open('band_cps.jsonl', 'a') as f: f.write(json.dumps(r) + '\n')
