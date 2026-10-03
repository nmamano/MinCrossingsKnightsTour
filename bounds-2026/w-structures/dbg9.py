from seam import Seam
from flux_strip import current_terms
for D in (3,):
  for p in (4,):
    st = Seam(T=(0, p), hv=(-1, 0), w1=D-1, w2=0, f1=(2, 1), form1=(1, -2), s=1)
    for name, ud in (('up', (1, 2)), ('down', (1, -2))):
        want = set()
        for i, (u, v) in enumerate(st.var_edges):
            d = (v[0] - u[0], v[1] - u[1])
            if (u[0] == 0 and d == ud) or d == (2, 1):
                want.add(i)
        x = [1 if i in want else 0 for i in range(len(st.var_edges))]
        terms, const = current_terms(st, x)
        print(name, st.evaluate(want), 'current', sum(terms) + const)
