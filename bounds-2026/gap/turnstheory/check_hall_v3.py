#!/usr/bin/env python3
"""Exact strict-collar mixed-capacity Hall test; standard library, one process.
Run from the research root. Input inventory lists JSON files with a tour key.
Outputs own-folder JSON, TSV, and worst-cut certificates. No solver threads.
"""
import sys
sys.dont_write_bytecode = True
import json, hashlib, time, random, argparse
from pathlib import Path
from collections import Counter, defaultdict, deque
from itertools import combinations
from fractions import Fraction
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'w-verifier'), str(ROOT/'gap/verifier'), str(ROOT/'w-turnstheory')]
from check import check as validate, MOVES, proper
from claim26_certificate import TERMS, EXC, edge
from check_knight_tiles import microtiles

# Quarter index: bottom, right, top, left. All supports use doubled integers.
QUARTER = (((0,0),(2,0),(1,1)), ((2,0),(2,2),(1,1)),
           ((2,2),(0,2),(1,1)), ((0,2),(0,0),(1,1)))
TILES = {d: microtiles(((0,0),d)) for d in ((1,2),(1,-2),(2,1),(2,-1))}

def bbox(points):
    return (min(x for x,y in points), max(x for x,y in points),
            min(y for x,y in points), max(y for x,y in points))

def near(box, candidate, n, radius):
    """ALL support in radius R of ONE path vertex; exact odd-integer test."""
    fx,fy,r = candidate
    lx,hx,ly,hy = box
    if fx: lx,hx = 2*(n-1)-hx,2*(n-1)-lx
    if fy: ly,hy = 2*(n-1)-hy,2*(n-1)-ly
    # Intersect all endpoint radius boxes to find possible vertex centres.
    xl,xh,yl,yh = hx-2*radius,lx+2*radius,hy-2*radius,ly+2*radius
    fixed = 2*r+1
    def odd(lo,hi): return lo+(lo%2==0) <= hi
    return ((xl<=fixed<=xh and odd(max(yl,3),min(yh,fixed))) or
            (yl<=fixed<=yh and odd(max(xl,3),min(xh,fixed))))

class Dinic:
    def __init__(self,n): self.g=[[] for _ in range(n)]
    def arc(self,u,v,c):
        a=[v,c,None]; b=[u,0,a]; a[2]=b
        self.g[u].append(a); self.g[v].append(b)
        return a
    def solve(self,s,t):
        total=0
        while True:
            level=[-1]*len(self.g);level[s]=0;q=deque([s])
            while q:
                u=q.popleft()
                for v,c,_ in self.g[u]:
                    if c and level[v]<0:level[v]=level[u]+1;q.append(v)
            if level[t]<0:return total,{i for i,x in enumerate(level) if x>=0}
            pos=[0]*len(self.g)
            def push(u,cap):
                if u==t:return cap
                while pos[u]<len(self.g[u]):
                    a=self.g[u][pos[u]];v,c,rev=a
                    if c and level[v]==level[u]+1:
                        got=push(v,min(cap,c))
                        if got:a[1]-=got;rev[1]+=got;return got
                    pos[u]+=1
                return 0
            while True:
                f=push(s,10**15)
                if not f:break
                total+=f

def flow(adj, capacities, demand):
    k=len(adj); sink=1+k+len(capacities); D=Dinic(sink+1)
    for i,ns in enumerate(adj):
        D.arc(0,1+i,demand)
        for j in ns:D.arc(1+i,1+k+j,demand*k+1)
    for j,c in enumerate(capacities):D.arc(1+k+j,sink,c)
    value,reach=D.solve(0,sink)
    J=[i for i in range(k) if 1+i in reach]
    neighbours=set(j for i in J for j in adj[i])
    assert demand*len(J)-sum(capacities[j] for j in neighbours)==demand*k-value
    # Independently check conservation and the realized path payments.
    balances=[0]*(sink+1)
    for u in range(1,1+k):
        got=D.g[u][0][1]
        sent=sum(a[2][1] for a in D.g[u][1:])
        assert got==sent and 0<=got<=demand
    for j,c in enumerate(capacities):
        used=D.g[1+k+j][-1][2][1]
        assert used==sum(a[1] for a in D.g[1+k+j][:-1]) and used<=c
    return value,J,sorted(neighbours)

def retained(es,n):
    candidates=[]
    for fx in (0,1):
        for fy in (0,1):
            def trans(a):return (n-1-a[0] if fx else a[0],n-1-a[1] if fy else a[1])
            local={edge(trans(a),trans(b)) for a,b in es}
            for r in range(12,n//2-3):
                hs=[];exception=False
                for transpose in (False,True):
                    def at(p):
                        p=(p[0],p[1]+r)
                        return (p[1],p[0]) if transpose else p
                    F=sum(c for a,b,c in TERMS if edge(at(a),at(b)) in local)
                    exception |= all(edge(at(a),at(b)) in local for a,b in EXC)
                    c=1-2*(r%2);hs.append(((1+c)//2+c*(F+2))%3)
                if not exception and sum(hs)%3:candidates.append((fx,fy,r))
    return candidates

def geometry(tour, pair_exclusion="S"):
    assert pair_exclusion in ("S", "B")
    n=len(tour); X,turns=validate(tour)
    es=set()
    for y,row in enumerate(tour):
        for x,code in enumerate(row):
            for ch in code:
                dy,dx=MOVES[int(ch)]
                es.add(edge((x,n-1-y),(x+dx,n-1-y-dy)))
    es=sorted(es); assert len(es)==n*n
    buckets=defaultdict(list)
    for i,(a,b) in enumerate(es):
        d=(b[0]-a[0],b[1]-a[1])
        for x,y,k in TILES[d]:buckets[x+a[0],y+a[1],k].append(i)
    assert sum(map(len,buckets.values()))==4*n*n
    assert all(0<=x<n-1 and 0<=y<n-1 for x,y,k in buckets)
    pairs=Counter()
    for ids in buckets.values():
        for a,b in combinations(ids,2):pairs[a,b]+=1
    assert len(pairs)==X and all(v in (1,2) for v in pairs.values())
    assert all(proper(es[a],es[b]) for a,b in pairs)
    def mask(e):
        (x,y),(u,v)=e
        return int(min(x,u)<=1)|(int(max(x,u)>=n-2)<<1)|(int(min(y,v)<=1)<<2)|(int(max(y,v)>=n-2)<<3)
    masks=list(map(mask,es)); atoms=[];s=0;b_count=0;X1=0
    def boundary_mask(e):
        return sum((1 << (2*k+side)) for k in (0,1) for side,border in enumerate((0,n-1))
                   if any(v[k]==border for v in e))
    boundary_masks=list(map(boundary_mask,es))
    # Atom record: kind, exact doubled support box, multiplicity, geometric id.
    for (a,b),overlap in sorted(pairs.items()):
        box=bbox([(2*x,2*y) for i in (a,b) for x,y in es[i]])
        in_s=bool(masks[a]&masks[b]); in_b=bool(boundary_masks[a]&boundary_masks[b])
        assert not in_b or in_s
        s+=in_s; b_count+=in_b
        if not (in_s if pair_exclusion=='S' else in_b):
            atoms.append(('pair',box,1,(es[a],es[b])))
        if overlap==1:X1+=1;atoms.append(('X1',box,1,(es[a],es[b])))
    G=W3=0
    for x in range(n-1):
        for y in range(n-1):
            for k in range(4):
                m=len(buckets.get((x,y,k),()))
                units=1 if m==0 else (m-1)*(m-2)//2
                if not units:continue
                kind='G' if m==0 else 'W3'
                if m==0:G+=1
                else:W3+=units
                box=bbox([(2*x+a,2*y+b) for a,b in QUARTER[k]])
                atoms.append((kind,box,units,(x,y,k)))
    assert 2*(X-4*n+2)==G+X1+W3
    return dict(n=n,X=X,turns=turns,E=X-4*n+2,G=G,X1=X1,W3=W3,S_union=s,B_union=b_count,
                retained=len(retained(es,n))),retained(es,n),atoms

def run(tour,radius=10):
    info,candidates,atoms=geometry(tour);n=len(tour)
    adj=[[j for j,a in enumerate(atoms) if near(a[1],c,n,radius)] for c in candidates]
    trials=[]
    for price,scale,demand,paircap in [('2/3',6,4,4),('1/2',4,2,2)]:
        capacities=[(paircap if a[0]=='pair' else 1)*a[2] for a in atoms]
        expected=Fraction(price)*(info['X']-info['S_union'])+(1-Fraction(price))*info['E']
        assert Fraction(sum(capacities),scale)==expected
        value,J,N=flow(adj,capacities,demand)
        trials.append(dict(p=price,lambda_value=price,radius=radius,scale=scale,
            demand=demand*len(candidates),flow=value,deficit_scaled=demand*len(candidates)-value,
            Delta=str(Fraction(demand*len(candidates)-value,scale)),
            J=[candidates[i] for i in J],neighbour_capacity_scaled=sum(capacities[j] for j in N),
            neighbour_atoms=[dict(kind=atoms[j][0],support_box_2=atoms[j][1],units=atoms[j][2],
                                 geometry=atoms[j][3],capacity_scaled=capacities[j]) for j in N]))
    return dict(**info,trials=trials)

def selftest():
    rnd=random.Random(2910)
    for _ in range(300):
        k=rnd.randrange(1,7);m=rnd.randrange(1,8);d=rnd.randrange(1,5)
        adj=[[j for j in range(m) if rnd.randrange(2)] for i in range(k)]
        caps=[rnd.randrange(1,5) for j in range(m)]
        value,_,_=flow(adj,caps,d)
        worst=max(d*len(J)-sum(caps[j] for j in set(j for i in J for j in adj[i]))
                  for mask in range(1<<k) for J in [[i for i in range(k) if mask>>i&1]])
        assert d*k-value==worst
    for _ in range(2000):
        n=60;c=(rnd.randrange(2),rnd.randrange(2),rnd.randrange(12,27));R=rnd.randrange(11)
        points=[(rnd.randrange(120),rnd.randrange(120)) for _ in range(rnd.randrange(1,5))]
        box=bbox(points);fx,fy,r=c
        vs=[(2*r+1,2*j+1) for j in range(1,r+1)]+[(2*j+1,2*r+1) for j in range(1,r+1)]
        vs=[(2*(n-1)-x if fx else x,2*(n-1)-y if fy else y) for x,y in vs]
        brute=any(all(max(abs(x-u),abs(y-v))<=2*R for x,y in points) for u,v in vs)
        assert near(box,c,n,R)==brute
    print('SELFTEST PASS: 300 exhaustive Hall checks; 2000 strict-support checks',flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--selftest',action='store_true');ap.add_argument('--limit',type=int);args=ap.parse_args()
    selftest()
    if args.selftest:return
    rows=json.loads((ROOT/'gap/turnstheory/hall_inventory.json').read_text())
    grouped={}
    for name,n in rows:
        d=json.loads((ROOT/name).read_text());tour=d['tour']
        h=hashlib.sha256(json.dumps(tour,separators=(',',':')).encode()).hexdigest()
        grouped.setdefault(h,dict(tour=tour,sources=[]))['sources'].append(name)
    jobs=sorted(grouped.items(),key=lambda kv:(len(kv[1]['tour']),kv[1]['sources'][0]))
    if args.limit:jobs=jobs[:args.limit]
    out=[];start=time.monotonic();folder=ROOT/'gap/turnstheory'
    for i,(h,job) in enumerate(jobs):
        try:
            result=run(job['tour']);result.update(sha256=h,sources=job['sources'],valid=True)
        except (AssertionError,ValueError,TypeError,KeyError) as e:
            result=dict(sha256=h,sources=job['sources'],n=len(job['tour']),valid=False,error=repr(e))
        out.append(result)
        print(f"{i+1}/{len(jobs)} n={result['n']} valid={result['valid']} "+
              (' '.join(f"p={t['p']} Delta={t['Delta']}" for t in result['trials']) if result['valid'] else result['error'])+
              f" {job['sources'][0]} elapsed={time.monotonic()-start:.1f}s",flush=True)
        (folder/'hall_v3_results.json').write_text(json.dumps(out,indent=2)+'\n')
    with (folder/'hall_v3_results.tsv').open('w') as f:
        f.write('source\tn\tvalid\tX\tretained\tDelta_2_3\tDelta_1_2\tsha256\n')
        for row in out:
            for source in row['sources']:
                vals=[source,row['n'],row['valid'],row.get('X',''),row.get('retained','')]
                vals += [t['Delta'] for t in row.get('trials',[])] if row['valid'] else ['','']
                vals += [row['sha256']];f.write('\t'.join(map(str,vals))+'\n')
    for price in ['2/3','1/2']:
        valid=[r for r in out if r['valid']]
        worst=max(valid,key=lambda r:(Fraction(next(t for t in r['trials'] if t['p']==price)['Delta']),r['n']))
        (folder/f"hall_v3_worst_{price.replace('/','_')}.json").write_text(json.dumps(worst,indent=2)+'\n')
    print(f'DONE {len(out)} unique boards, {sum(len(r["sources"]) for r in out)} files, {time.monotonic()-start:.1f}s',flush=True)
if __name__=='__main__':main()
