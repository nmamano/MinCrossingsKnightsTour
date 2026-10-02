import sys, itertools
from imb import clusters
n=int(sys.argv[1])
def lab(c,n):
    x,y=c[0]
    def side(v): return 'L' if v<n//4 else ('H' if v>3*n//4 else 'M')
    return side(x)+side(y)
for ts in [(0,0,0,0),(1,0,0,0),(-1,0,0,0),(2,0,0,0),(1,1,0,0)]:
  for ms in [(0,0,0,0),(1,0,0,0),(0,0,0,1)]:
    E,deg,cl=clusters(n,ts,ms)
    print(ts,ms,' '.join(f'{lab(c,n)}:{i}' for c,i in sorted(cl, key=lambda t: lab(t[0],n))))
