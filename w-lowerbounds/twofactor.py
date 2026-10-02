import sys
import networkx as nx
from collections import Counter
from fold_complete2 import base, repair
from fold_complete import total_crossings
for n in map(int, sys.argv[2:]):
    E, deg = base(n)
    E2, comps = repair(n, E, rad=int(sys.argv[1]), cuts=False, tlimit=180)
    d = Counter()
    for e in E2: d[e[0]]+=1; d[e[1]]+=1
    ok = all(d[(x,y)]==2 for x in range(n) for y in range(n)) and len(E2)==n*n
    km = all(sorted((abs(e[0][0]-e[1][0]),abs(e[0][1]-e[1][1])))==[1,2] for e in E2)
    X = total_crossings(E2)
    print('n',n,'2-factor ok',ok,'knight moves',km,'crossings',X,'4n =',4*n,'excess',X-4*n,'cycles',len(comps), flush=True)
    import pickle; pickle.dump(sorted(E2), open(f'twofactor_{n}.pkl','wb'))
