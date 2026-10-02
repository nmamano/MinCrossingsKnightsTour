from seam import Seam
from flux_strip import current_terms
chi = lambda c: 1 if (c[0] + c[1]) % 2 == 0 else -1
for p in (2, 4, 6):
    st = Seam(T=(0, p), hv=(-1, 0), w1=2, w2=0, f1=(2, 1), form1=(1, -2), s=1)
    # cheap pattern: (0,y)-(1,y+2) U-turns, line edges (x,y)-(x+2,y+1) inside band
    want = set()
    for i, (u, v) in enumerate(st.var_edges):
        d = (v[0] - u[0], v[1] - u[1])
        if (u[0] == 0 and d == (1, 2)) or d == (2, 1) or (u[0] == 1 and d == (-1, -2)):
            want.add(i)
    class X: pass
    x = [1 if i in want else 0 for i in range(len(st.var_edges))]
    terms, const = current_terms(st, x)
    print(p, 'X', st.evaluate(want), 'current', sum(terms) + const, 'const', const)
p = 4
st = Seam(T=(0, p), hv=(-1, 0), w1=2, w2=0, f1=(2, 1), form1=(1, -2), s=1)
for i, (u, v) in enumerate(st.var_edges):
    for k in range(-4, 5):
        a = (u[0], u[1] + k * p); b = (v[0], v[1] + k * p)
        lo, hi = (a, b) if a[1] < b[1] else (b, a)
        if lo[1] < 0 <= hi[1]:
            print(i, u, v, k, lo, hi, chi(lo))
print(st.fixed_edges)
