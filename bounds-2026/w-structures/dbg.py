from seam import Seam, solve
for w in (2,3,4):
    st = Seam(T=(4,4), hv=(-1,1), w1=w, w2=w, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=4)
    t1 = [u for u in st.terminals if any(sd==1 for _,sd in st.fixed_inc[u])]
    t2 = [u for u in st.terminals if any(sd==2 for _,sd in st.fixed_inc[u])]
    col = lambda u: (u[0]+u[1])%2
    print(w, len(st.base), len(t1), len(t2), sum(col(u) for u in st.base), [col(u) for u in t1], [col(u) for u in t2])
    print(solve(st, time_limit=10, lanes=False)['status'])
