import itertools,random
def sgn(v): return (v>0)-(v<0)
def turn(a,b,c): return sgn((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
def proper(e,f):
    a,b=e; c,d=f
    return turn(a,b,c)*turn(a,b,d)==-1 and turn(c,d,a)*turn(c,d,b)==-1
T=[(0, 0), (1, 2), (0, 4), (1, 6), (3, 7), (5, 6), (7, 7), (6, 5),
    (5, 7), (7, 6), (6, 4), (7, 2), (6, 0), (4, 1), (2, 0), (0, 1),
    (1, 3), (0, 5), (1, 7), (2, 5), (0, 6), (2, 7), (4, 6), (6, 7),
    (7, 5), (6, 3), (7, 1), (5, 0), (6, 2), (7, 0), (5, 1), (3, 0),
    (1, 1), (0, 3), (1, 5), (0, 7), (2, 6), (4, 7), (6, 6), (7, 4),
    (5, 5), (3, 6), (4, 4), (3, 2), (2, 4), (4, 5), (5, 3), (3, 4),
    (2, 2), (4, 3), (3, 5), (1, 4), (3, 3), (5, 4), (7, 3), (6, 1),
    (4, 2), (2, 3), (0, 2), (1, 0), (3, 1), (5, 2), (4, 0), (2, 1)]
def side_count(edges, n):
    for tr in range(4):
        E=[e for e in edges if e[0][0]==0 or e[1][0]==0]
        X=sum(proper(e,f) for e,f in itertools.combinations(E,2))
        print("side",tr,"edges",len(E),"crossings",X,"n+1 =",n+1)
        edges=[((n-1-a[1],a[0]),(n-1-b[1],b[0])) for a,b in edges]
edges=[(T[i],T[(i+1)%64]) for i in range(64)]
side_count(edges,8)
