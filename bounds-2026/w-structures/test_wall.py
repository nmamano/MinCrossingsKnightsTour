from seam import Seam, solve
st = Seam(T=(8,0), hv=(0,-1), w1=3, w2=0, f1=(2,-1), form1=(1,2))
print(len(st.base), len(st.var_edges), len(st.terminals))
print(solve(st, time_limit=120, workers=1))
