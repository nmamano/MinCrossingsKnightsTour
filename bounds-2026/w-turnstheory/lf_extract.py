"""Extract local corner moves from a supplied full LF4 tour."""
import json
from check_upper_proofs import DIRS, ROOT

def extract(path):
    raw=json.loads(path.read_text()); n=raw['n']; z=raw['info']['Z']
    d={k:raw[k] for k in ('bottom','top','left','right')}
    d.update(n0=n,Z=z,phases=raw['info']['phases'],zones={})
    for corner,(a,b) in {'BL':(0,0),'BR':(n-z,0),'TL':(0,n-z),'TR':(n-z,n-z)}.items():
        for x in range(z):
            for y in range(z):
                d['zones'][f'{corner}:{x},{y}']=[DIRS[int(k)] for k in raw['tour'][n-1-b-y][a+x]]
    return d

if __name__=='__main__':
    from check_upper_proofs import graph,slab,power
    d=extract(ROOT/'w-integrator/tours/LF4_n96.json')
    for r in range(0,48,2):
        n=192+r; g=graph(d,n); out=[]
        for a in (36,n+36,2*n+36):
            names,M=slab(g,n,a,48)
            orders=[]
            for k in range(1,7):
                try:
                    if power(M,k+1)==M: orders.append(k)
                except AssertionError: pass
            out.append((len(names),sum(s==0 and t==1 for (s,i),(t,j) in M.items()),orders))
        print(n,out,flush=True)
