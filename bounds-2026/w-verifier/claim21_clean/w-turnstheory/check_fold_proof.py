#!/usr/bin/env python3
"""Independent fold construction and finite insertion certificate. Standard library only."""
import json
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
MOV=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
# Anchor displacement in units of (n-n0)/4, in saved component order.
ANCHORS=((0,1),(1,4),(3,0),(4,3),(0,0),(0,4),(4,0),(4,4),
         (0,2),(2,0),(2,4),(4,2),(2,2))
def rot(p,n,r):
    for _ in range(r%4):p=(n-1-p[1],p[0])
    return p

def vec(p,r):
    for _ in range(r%4):p=(-p[1],p[0])
    return p

def field(n):
    h=n//2; g={(x,y):set() for x in range(n) for y in range(n)}
    for p in g:
        x,y=p;r=0 if x<h and y<h else 1 if x>=h and y<h else 2 if x>=h else 3
        a,b=rot(p,n,-r);d=vec((2,1) if b>a+1 else (-1,-2),r)
        q=(x+d[0],y+d[1])
        if q in g:g[p].add(q);g[q].add(p)
    for r in range(4):
        for y in range(n):
            p=rot((0,y),n,r)
            if len(g[p])!=1:continue
            nb=next(iter(g[p]));sign=next((s for s in (1,-1) if rot((2,y+s),n,r)==nb),None)
            if sign is None:continue
            if h-n//4<=y<h:sign=-sign
            q=rot((1,y+2*sign),n,r)
            if q in g and len(g[q])==1 and q not in g[p]:g[p].add(q);g[q].add(p)
    return g

def graph(d,n):
    n0=d['n0'];assert (n-n0)%12==0 and n>=n0
    assert (d['p'],d['lo'],d['band'],d['rad'])==(6,8,1,4)
    g=field(n)
    for r in range(4):
        for x in range(11,n//2-11):
            for j in range(3):
                p=rot((x,x+j),n,r)
                g[p]={(p[0]+dx,p[1]+dy) for dx,dy in (vec(z,r) for z in d['template'][f'{r}:{(x-8)%6},{j}'])}
    assert len(d['components'])==13
    for comp,anchor in zip(d['components'],ANCHORS):
        off=[comp['offset'][i]+anchor[i]*(n-n0)//4 for i in range(2)]
        for key,ds in comp['cells'].items():
            a,b=map(int,key.split(','));p=(off[0]+a,off[1]+b)
            g[p]={(p[0]+dx,p[1]+dy) for dx,dy in ds}
    return g

def validate(g):
    for p,nb in g.items():
        assert len(nb)==2,(p,nb)
        for q in nb:assert q in g and p in g[q] and sorted(map(abs,(q[0]-p[0],q[1]-p[1])))==[1,2],(p,q)
    seen=set();sizes=[]
    for p in g:
        if p in seen:continue
        todo=[p];seen.add(p);s=0
        while todo:
            q=todo.pop();s+=1
            for z in g[q]:
                if z not in seen:seen.add(z);todo.append(z)
        sizes.append(s)
    return sizes

def stored(n):
    d=json.loads((ROOT/f'w-integrator/tours/FOLD24_n{n}.json').read_text())
    return {(x,n-1-y):{(x+MOV[int(c)][0],n-1-y+MOV[int(c)][1]) for c in d['tour'][y][x]} for y in range(n) for x in range(n)}

def block(g,n,r,kind,a,w,details=False):
    # All full-board vertices in a wedge; straight vertices are traced, not omitted.
    def lab(p):
        x,y=rot(p,n,-r)
        if kind=='corner':return max(2*x-y,2*y-x) if x<n//2 and y<n//2 else None
        return 2*min(y,n-y)-x if x<n//2 else None
    S={p for p in g if (c:=lab(p)) is not None and a<=c<a+w}
    ports={};names=[[],[]]
    for p in S:
        for q in g[p]-S:
            cp,cq=lab(p),lab(q)
            assert cq is not None,(kind,p,q)
            side=0 if cq<a else 1;cut=a if side==0 else a+w
            l,h=(q,p) if cq<cp else (p,q)
            x,y=rot(l,n,-r);xx,yy=rot(h,n,-r)
            if kind=='corner':
                if max(x,xx)<=2:tag='L';depth=(x,xx)
                elif max(y,yy)<=2:tag='B';depth=(y,yy)
                else:tag='D';depth=(y-x,yy-xx)
            else:tag='lo' if y<n//2 else 'hi';depth=(x,xx)
            name=(tag,*depth,lab(l)-cut,lab(h)-cut)
            assert name not in names[side],(kind,name)
            names[side].append(name);ports[(p,q)]=(side,name)
    names=[sorted(z) for z in names]
    assert names[0]==names[1],(kind,n,r,names)
    M={};seen=set()
    for (p,q),(side,name) in ports.items():
        start=(side,names[side].index(name))
        if start in M:continue
        prev=q;cur=p
        while True:
            assert cur not in seen,(kind,'closed or reused path',cur)
            seen.add(cur);nxt=next(iter(g[cur]-{prev}))
            if nxt not in S:
                side2,name2=ports[(cur,nxt)];end=(side2,names[side2].index(name2))
                M[start]=end;M[end]=start;break
            prev,cur=cur,nxt
    assert seen==S,(kind,'hidden components',len(S-seen))
    if details:
        return names[0],M,S,{(p,q):(side,names[side].index(name)) for (p,q),(side,name) in ports.items()}
    return names[0],M

def compose(M,k):
    adj=defaultdict(list)
    def add(a,b):adj[a].append(b);adj[b].append(a)
    for j in range(k):
        for u,v in M.items():
            if u<v:add((j,*u),(j,*v))
    width=len(M)//2
    for j in range(k-1):
        for i in range(width):add((j,1,i),(j+1,0,i))
    outer={(0,0,i):(0,i) for i in range(width)}|{(k-1,1,i):(1,i) for i in range(width)}
    out={};seen=set()
    for v,start in outer.items():
        if start in out:continue
        prev=None;cur=v
        while True:
            assert cur not in seen,'closed component in composition'
            seen.add(cur)
            nxt=next((z for z in adj[cur] if z!=prev),None)
            if nxt is None:
                end=outer[cur];out[start]=end;out[end]=start;break
            prev,cur=cur,nxt
    assert seen==set(adj),'hidden closed component in composition'
    return out

def outside(g,blocks):
    inside=set();ports={}
    for ident,(_,_,S,P) in blocks.items():
        assert not inside&S,'blocks overlap'
        inside|=S
        for (p,q),port in P.items():ports[(q,p)]=(ident,*port)
    for q,p in ports:assert q not in inside,'blocks adjacent'
    S=set(g)-inside;seen=set();M={}
    for (p,q),start in ports.items():
        if start in M:continue
        cur=p;prev=q
        while True:
            assert cur not in seen,'outside closed or reused path'
            seen.add(cur);nxt=next(iter(g[cur]-{prev}))
            if nxt not in S:
                end=ports[(cur,nxt)];M[start]=end;M[end]=start;break
            prev,cur=cur,nxt
    assert seen==S,('outside hidden component',len(S-seen))
    return M

def crossing_pairs(g):
    def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    edges=sorted((p,q) for p in g for q in g[p] if p<q);buckets={}
    for a,b in edges:
        candidates=set();cells=[]
        for x in range(min(a[0],b[0]),max(a[0],b[0])+1):
            for y in range(min(a[1],b[1]),max(a[1],b[1])+1):
                cells.append((x,y));candidates.update(buckets.get((x,y),()))
        for c,d in candidates:
            if orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0:yield ((a,b),(c,d))
        for cell in cells:buckets.setdefault(cell,[]).append((a,b))

def local_cost(pairs,n,r,kind,a,w):
    total=boundary=0
    for pair in pairs:
        ps=[rot(p,n,-r) for e in pair for p in e]
        if kind=='corner':
            if any(x>=n//2 or y>=n//2 for x,y in ps):continue
            cs=[max(2*x-y,2*y-x) for x,y in ps]
        else:
            if any(x>=n//2 for x,y in ps):continue
            cs=[2*min(y,n-y)-x for x,y in ps]
        if a<=min(cs)<a+w:
            total+=1
            boundary+=any(min(x,y)<=2 for x,y in ps) if kind=='corner' else 1
    return total,boundary,total-boundary

def component_cells(d,n):
    cells=set()
    for comp,anchor in zip(d['components'],ANCHORS):
        off=[comp['offset'][i]+anchor[i]*(n-d['n0'])//4 for i in range(2)]
        for key in comp['cells']:
            x,y=map(int,key.split(','));cells.add((off[0]+x,off[1]+y))
    return cells

def matching_cycles(N,blocks,power):
    adj=defaultdict(list)
    for u,v in N.items():adj[u].append(v)
    for key,b in blocks.items():
        for u,v in compose(b[1],power).items():adj[(key,*u)].append((key,*v))
    assert all(len(v)==2 for v in adj.values())
    seen=set();count=0
    for p in adj:
        if p in seen:continue
        count+=1;todo=[p];seen.add(p)
        while todo:
            for q in adj[todo.pop()]:
                if q not in seen:seen.add(q);todo.append(q)
    return count

def pairs(M):
    return [[u,v] for u,v in sorted(M.items()) if u<v]

def main():
    from fractions import Fraction
    report={'date':'2026-10-02','size_step':24,'matching_period':48,'residues':[]}
    for n0 in range(96,120,2):
        d=json.loads((ROOT/f'w-integrator/corners/FOLD24_base_n{n0}.json').read_text())
        base_blocks=None;N=None;X0=None;residual=None
        row={'n0':n0,'blocks':[],'checks':[]}
        for k in range(3):
            n=n0+24*k;g=graph(d,n)
            assert validate(g)==[n*n]
            assert g==stored(n),('saved tour mismatch',n0,n)
            cp=list(crossing_pairs(g));blocks={};cost=0;patches=component_cells(d,n)
            for kind,a in [('corner',24),('side',n//2+16)]:
                for r in range(4):
                    key=(kind,r)
                    b=block(g,n,r,kind,a,6+12*k,True);blocks[key]=b
                    assert not b[2]&patches, (n,key,"finite patch in inserted block")
                    local=local_cost(cp,n,r,kind,a,6+12*k)
                    expected=(10,6,4) if kind=='corner' else (9,9,0)
                    assert local==tuple(v*(1+2*k) for v in expected),(n,key,local)
                    cost+=local[0]
                    if k==0:
                        # Translate one primitive block by one period: no phase change.
                        assert block(g,n,r,kind,a+6,6)==b[:2]
                        if kind=='corner':assert compose(b[1],2)==b[1]
                        else:
                            assert all(b[1][(0,i)]==(1,(i+1)%4) for i in range(4))
                            assert compose(b[1],5)==b[1]
                        row['blocks'].append({'kind':kind,'rotation':r,'ports':b[0],
                                              'matching':pairs(b[1]),'cost':local})
                    else:
                        b0=base_blocks[key]
                        assert b[0]==b0[0] and b[1]==compose(b0[1],1+2*k)
            out=outside(g,blocks)
            if k==0:
                N=out;base_blocks=blocks;X0=len(cp);residual=X0-cost
                row['outside_matching']=pairs(N)
                assert matching_cycles(N,blocks,1)==matching_cycles(N,blocks,3)==1
                row['X0']=X0;row['b']=str(Fraction(3*X0-19*n0,3))
                assert Fraction(3*X0-19*n0,3)<=142
            else:assert out==N and len(cp)==X0+152*k and len(cp)-cost==residual
            row['checks'].append({'n':n,'X':len(cp),'outside_ports':len(out),'residual_crossings':len(cp)-cost})
        # The +12 graph is a 2-factor, but need not be one cycle.
        n=n0+12;g=graph(d,n);sizes=validate(g)
        blocks={(kind,r):block(g,n,r,kind,a,12,True)
                for kind,a in [('corner',24),('side',n//2+16)] for r in range(4)}
        assert outside(g,blocks)==N
        for key,b in blocks.items():assert b[0]==base_blocks[key][0] and b[1]==compose(base_blocks[key][1],2)
        row['step12_cycle_sizes']=sizes
        report['residues'].append(row)
        print(f"PASS n0={n0}: X0={X0}, b={row['b']}; +24/+48 valid; +12 cycles={len(sizes)}",flush=True)
    path=Path(__file__).with_name('fold_proof_checks.json')
    path.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 36 saved tours; all complete block/outside matchings; no hidden component; 152=120+32.')
    print(path)

if __name__=='__main__':main()
