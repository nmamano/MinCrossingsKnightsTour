"""Independent strip checks, local enumeration, and random 2-factors."""
import json, random
from pathlib import Path
from itertools import combinations
from check import MOVES, orient

def counts(g):
    n=len(g)
    turning={(r,c) for r in range(n) for c in range(n)
             if orient(MOVES[int(g[r][c][0])],(0,0),MOVES[int(g[r][c][1])])!=0}
    strips=[sum(c<4 for r,c in turning),sum(c>=n-4 for r,c in turning),
            sum(r<4 for r,c in turning),sum(r>=n-4 for r,c in turning)]
    assert all(t>=2*n for t in strips),(n,strips)
    assert n<8 or len(turning)>=8*n-64
    return len(turning),strips

def local():
    totals=[]
    for col in range(4):
        allowed=[d for d in MOVES if col+d[1]>=0];total=0
        for a,b in combinations(allowed,2):
            turn=int(orient(a,(0,0),b)!=0)
            if col==0: assert turn==1
            elif col in (1,2):
                p=sum(col+d[1] in (0,3) for d in (a,b));assert turn>=p-1
            else:
                q=sum(col+d[1] in (1,2) for d in (a,b));assert turn>=1-q
            total+=1
        totals.append(total)
    return totals

def matching(n,rng,banned=None):
    black=[(r,c) for r in range(n) for c in range(n) if (r+c)%2==0]
    if n*n%2:return None
    rng.shuffle(black);neighbors={}
    for p in black:
        r,c=p;ns=[(r+di,c+dj) for di,dj in MOVES if 0<=r+di<n and 0<=c+dj<n and (not banned or banned[p]!=(r+di,c+dj))]
        rng.shuffle(ns);neighbors[p]=ns
    right={}
    def augment(p,seen):
        for q in neighbors[p]:
            if q in seen:continue
            seen.add(q)
            if q not in right or augment(right[q],seen):right[q]=p;return True
        return False
    for p in black:
        if not augment(p,set()):return None
    return {p:q for q,p in right.items()}

def random_checks():
    rng=random.Random(20261002);out=[]
    code={d:str(k) for k,d in enumerate(MOVES)}
    for n in (6,8,10):
        samples=[];attempts=0;cycles=[]
        while len(samples)<100 and attempts<1000:
            attempts+=1;a=matching(n,rng)
            if a is None:continue
            b=matching(n,rng,a)
            if b is None:continue
            adj={(r,c):[] for r in range(n) for c in range(n)}
            for mat in (a,b):
                for p,q in mat.items():adj[p].append(q);adj[q].append(p)
            assert all(len(set(qs))==2 for qs in adj.values())
            assert all(p in adj[q] for p,ns in adj.items() for q in ns)
            unseen=set(adj);cc=0
            while unseen:
                cc+=1;todo=[next(iter(unseen))]
                while todo:
                    p=todo.pop()
                    if p not in unseen:continue
                    unseen.remove(p);todo.extend(adj[p])
            g=[[''.join(code[q[0]-r,q[1]-c] for q in adj[r,c]) for c in range(n)] for r in range(n)]
            t,s=counts(g);samples.append(dict(T=t,strips=s));cycles.append(cc)
        assert len(samples)==100
        out.append(dict(n=n,attempts=attempts,samples=samples,cycle_counts=sorted(set(cycles)),min_strip=min(min(s['strips']) for s in samples)))
    return out

def main():
    pairs=local();rows=[]
    for f in sorted(Path('.').rglob('*.json')):
        if any(p.startswith('.') for p in f.parts):continue
        try:d=json.loads(f.read_text())
        except (ValueError,UnicodeError):continue
        if not isinstance(d,dict) or 'tour' not in d:continue
        t,s=counts(d['tour']);rows.append(dict(file=str(f),n=len(d['tour']),T=t,strips=s,slack=min(s)-2*len(d['tour'])))
    randoms=random_checks()
    result=dict(date='2026-10-02',local_pairs_by_column=pairs,tour_files=rows,random_2factors=randoms)
    Path('w-verifier/turn_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('local pairs',pairs,'total',sum(pairs))
    print('tour files',len(rows),'minimum strip slack',min(r['slack'] for r in rows))
    for r in randoms:print('random n',r['n'],'samples',len(r['samples']),'min strip',r['min_strip'],'cycle counts',r['cycle_counts'],'attempts',r['attempts'])
if __name__=='__main__':main()
