from seam import Seam, solve
from tplio import chosen_from_cells, bottom_template_cells
from unroll import check
H16a = ['26 26 36 36 36 36 56 26','23 36 36 36 13 23 23 23','26 26 26 27 27 27 27 26','67 67 67 67 67 67 67 67']
st = Seam(T=(8,0), hv=(0,-1), w1=3, w2=0, f1=(2,-1), form1=(1,2))
ch = chosen_from_cells(st, bottom_template_cells(H16a))
print(st.evaluate(ch))
print(check(st, ch))
r = solve(st, time_limit=60, workers=1, hint=set(ch))
print(r['status'], r['X'], r['T'], r['bound'])
