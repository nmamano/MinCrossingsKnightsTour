import sys
from seam import Seam, build_model, cell_moves
from ortools.sat.python import cp_model
from seam_flux import KIND, cur_terms
p, w, tgt = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
k = KIND['diagfree']
st = Seam(T=k['T'](p), hv=k['hv'], w1=w, w2=w, f1=k['f1'], form1=k['form1'], f2=k['f2'], form2=k['form2'], s=1)
m, x = build_model(st, lanes=False)
terms, const = cur_terms(st, x)
m.Add(sum(terms) + const == tgt)
s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 120
r = s.Solve(m)
ch = [i for i in range(len(x)) if s.Value(x[i])]
print(s.StatusName(r), st.evaluate(ch))
dirs = cell_moves(st, ch)
# draw 3 periods on a grid: show each band cell with its two moves as arrows code
names = {(1,2):'a',(2,1):'b',(2,-1):'c',(1,-2):'d',(-1,-2):'e',(-2,-1):'f',(-2,1):'g',(-1,2):'h'}
cells = {}
for kk in range(3):
    for u, ds in dirs.items():
        c = st.shiftc(u, kk)
        cells[c] = ''.join(sorted(names[d] for d in ds))
xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
for y in range(max(ys), min(ys) - 1, -1):
    print(''.join((cells.get((xx, y), '  ') + ' ') for xx in range(min(xs), max(xs) + 1)))
print("legend: a(1,2) b(2,1) c(2,-1) d(1,-2) e(-1,-2) f(-2,-1) g(-2,1) h(-1,2); free fold: above diag A' (b,f), below B' (a,e)")
