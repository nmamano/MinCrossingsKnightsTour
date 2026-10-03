# KT Structures, 2026-10-03. BEYOND5.md data: route (i) payments vs N_re/2 on actual tours.
# Route (i) currency (PROOF_5N_PLAN.md 1-5, LB FINDINGS F): E = nu + T/2 exactly, nu = X_out/2 + E/2 (2E = G + X1 + W3),
# T = |S*| - 4n + 2. Route (i) spends: f0 = min(2, s_i)/4 from nu on each retained candidate with r > 32 (s_i = payable
# quarters in its squares), and (D_loss + L_def)/2 from T (D_loss = N - retained, L_def = large retained with s_i < 2).
# Residual after route (i): nu' = nu - sum f0, T' = T - D_loss - L_def; E_left = nu' + T'/2 = E - route(i).
import sys, json
from pathlib import Path
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'gap/turnstheory')); sys.path.insert(0, str(ROOT/'gap/verifier'))
from check_hall_v3 import geometry
from claim38_switch import edge, qs
from check import MOVES
import chamber_ledger as CL, fold_exact_scan as F

def run(f):
    grid = json.loads(Path(f).read_text())['tour']; info, cs, atoms = geometry(grid); n = info['n']
    es = {edge((x, n-1-y), (x+MOVES[int(v)][1], n-1-y-MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    own = defaultdict(list)
    for e in es:
        for q in qs(e): own[q].append(e)
    lookup = {(a[0], a[3]): j for j, a in enumerate(atoms)}
    def payable(q):
        ls = own[q]; m = len(ls)
        if m == 1: return None
        if not m: return lookup['G', q]
        if m >= 3: return lookup['W3', q]
        pair = tuple(sorted(ls)); return lookup.get(('pair', pair), lookup.get(('X1', pair)))
    def squares(c):
        fx, fy, r = c
        return [(n-2-x if fx else x, n-2-y if fy else y) for x, y in [(r, j) for j in range(1, r+1)] + [(i, r) for i in range(r-1, 0, -1)]]
    N = 4*len(range(12, n//2-3)); L = len(cs)
    large = cs   # all retained candidates (route (i) drops r <= 32 into its constant; here they are paid like the rest)
    s = [sum(1 for x, y in squares(c) for k in range(4) if payable((x, y, k)) is not None) for c in large]
    f0 = sum(min(2, v) for v in s)/4; Ldef = sum(1 for v in s if v < 2)
    dep = lambda x, y: min(x, y, n-2-x, n-2-y)
    deep = [sum(1 for x, y in squares(c) for k in range(4) if dep(x, y) >= 5 and payable((x, y, k)) is not None) for c in large]
    shallow_users = sum(1 for d, v in zip(deep, s) if d < 2 and v > d)     # route (i) must touch the collar zone
    deep_all = sum(1 for x in range(5, n-6) for y in range(5, n-6) for k in range(4) if dep(x, y) >= 5 and len(own[x, y, k]) != 1)
    BQx = deep_all - sum(min(2, d) for d in deep)                          # deep bad quarters route (i) leaves free
    E = info['E']; Xout = info['X'] - info['S_union']; T = info['S_union'] - 4*n + 2; nu = Xout/2 + E/2
    assert abs(E - (nu + T/2)) < 1e-9
    _, ports, changed, other, _, _ = CL.port_data(f); Nre = len(changed)
    BQ = F.run(f)['BQ']
    route = f0 + (N - L + Ldef)/2
    return dict(tour=Path(f).name, n=n, E=E, BQ4=BQ/4, T=T, nu=nu, N=N, retained=L, small_r=L-len(large), D_loss=N-L, L_def=Ldef,
                f0=f0, route_i=route, nu_left=nu - f0, T_left=T - (N - L) - Ldef, E_left=E - route, Nre_half=Nre/2,
                E_left_minus_Nre_half=E - route - Nre/2,
                shallow_users=shallow_users, BQx=BQx, C5_ratio=round((2*Nre + BQx)/n, 3))

if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(json.dumps(run(f)), flush=True)
