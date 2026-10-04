"""Complete list of corner cut-state pairs (s, t) that reach reduced value == target at potential w (arms A).
Loop: solve (presolve off), record (s,t), add a nogood on the 2K cut bits, until INFEASIBLE.
Output lines: s t sigma_t (hex); last line '# DONE <count>' only when the final solve proved INFEASIBLE.
usage: enum_pairs.py W A wfile target out [workers] [tl_per_solve]"""
import sys, time
from ortools.sat.python import cp_model
import corner_pot as cp
W, A, wf, target, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]
NW = int(sys.argv[6]) if len(sys.argv) > 6 else 2; TL = float(sys.argv[7]) if len(sys.argv) > 7 else 3600
t = [int(x) for x in open(wf).read().split()]; sc, w = t[0], t[1:]
m, c, phi, S = cp.build(W, A); ev, eh = cp.LAST_EV, cp.LAST_EH; K = len(S); sg = cp.sigma_perm(S)
m.Add(sc * c + sum(wk * f for wk, f in zip(w, phi)) == target)
bits = []   # expressions are 0/1 sums (a cell uses a move at most once) -> make bool vars
for e in list(ev) + list(eh):
    b = m.NewBoolVar(''); m.Add(e == b); bits.append(b)
import os
for item in filter(None, os.environ.get('FIX', '').split(',')):   # partition: FIX="bit:val,..." (bits 0..2K-1 of s|t)
    k, val = map(int, item.split(':')); m.Add(bits[k] == val)
f = open(out, 'w'); cnt = 0; t0 = time.time()
while True:
    s = cp_model.CpSolver(); s.parameters.num_workers = NW; s.parameters.max_time_in_seconds = TL; s.parameters.cp_model_presolve = False
    st = s.Solve(m)
    if st == cp_model.INFEASIBLE: f.write(f'# DONE {cnt}\n'); break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): f.write(f'# STOPPED {s.StatusName(st)} after {cnt}\n'); break
    v = [s.Value(b) for b in bits]; sv = sum(1 << k for k in range(K) if v[k]); tv = sum(1 << k for k in range(K) if v[K + k])
    stv = sum(1 << sg[j] for j in range(K) if tv >> j & 1)
    f.write(f'{sv:x} {tv:x} {stv:x}\n'); f.flush(); cnt += 1
    m.AddBoolOr([b.Not() if x else b for b, x in zip(bits, v)])
    if cnt % 50 == 0: print(cnt, f'{time.time()-t0:.0f}s', flush=True)
f.close(); print('done', cnt, f'{time.time()-t0:.0f}s')
