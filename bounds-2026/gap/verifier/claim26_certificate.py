"""Independent R1 certificate. Standard library only; no worker imports.

Rebuilds the forest strip and retains every row edge, not just test edges.
All crossings, weights, potentials, and final arc checks use integers.
Run from the research root: python3 gap/verifier/claim26_certificate.py
"""
from array import array
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time

def edge(a,b):
    return tuple(sorted((a,b)))

def cross(e,f):
    def det(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    a,b=e; c,d=f
    return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

def boundary(e):
    return any(p[0]==0 for p in e)

def transitions(state):
    x,pending=state
    p=(x,0)
    incoming=[e for e in pending if e[1]==p]
    keep=[e for e in pending if e[1]!=p]
    if len(incoming)>2 or (len(incoming)==2 and incoming[0][2]==incoming[1][2]):
        return
    options=[(p,(xx,dy)) for xx in range(4) for dy in (1,2)
             if sorted((abs(xx-x),dy))==[1,2] and min(x,xx)<2]
    needs=[2-len(incoming)] if x<2 else range(3-len(incoming))
    for count in needs:
        for chosen in combinations(options,count):
            load=Counter(e[1] for e in keep)
            load.update(b for a,b in chosen)
            if any(v>2 for v in load.values()):
                continue
            labels={e[2] for e in incoming}
            merged=min(labels) if labels else -1
            result=[(a,b,merged if c in labels else c) for a,b,c in keep]
            result.extend((a,b,merged) for a,b in chosen)
            pairs=[(f,(a,b)) for f in chosen for a,b,c in keep]
            pairs.extend(combinations(chosen,2))
            hits=[(a,b) for a,b in pairs if cross(a,b)]
            w=len(hits)
            w0=sum(boundary(a) and boundary(b) for a,b in hits)
            shift=int(x==3)
            labels={}; normalized=[]
            for a,b,c in sorted(result):
                if c not in labels:
                    labels[c]=len(labels)
                normalized.append(((a[0],a[1]-shift),(b[0],b[1]-shift),labels[c]))
            yield ((x+1)%4,tuple(normalized)),w,w0

TERMS=[((0,-1),(1,1),-1),((0,0),(1,-2),-1),((0,0),(2,-1),-1),
       ((0,1),(1,-1),1),((0,1),(2,0),1),((0,2),(1,0),-1),
       ((1,0),(2,2),-1),((1,1),(2,-1),-1)]
EXC=[((0,0),(2,1)),((0,1),(2,0))]

def main():
    started=time.monotonic()
    states=[(0,())]; ids={states[0]:0}; adjacency=[]
    for u,s in enumerate(states):
        choices={}
        for t,w,w0 in transitions(s):
            if t not in ids:
                ids[t]=len(states); states.append(t)
            v=ids[t]
            if v in choices:
                assert choices[v]==(w,w0)
            choices[v]=(w,w0)
        adjacency.append([(v,w,w0) for v,(w,w0) in choices.items()])
    assert (len(states),sum(map(len,adjacency)))==(82516,144674)
    print('base',len(states),sum(map(len,adjacency)),flush=True)

    # All knight edges that touch the row and belong to the strip.
    universe=set()
    for x,y in product(range(4),range(-2,3)):
        for xx,yy in product(range(4),range(-2,3)):
            if min(x,xx)<2 and min(y,yy)<=0<=max(y,yy) and sorted((abs(x-xx),abs(y-yy)))==[1,2]:
                universe.add(edge((x,y),(xx,yy)))
    bits={e:1<<i for i,e in enumerate(sorted(universe))}
    assert len(bits)==20
    def mask(es):
        m=0
        for e in es:
            m|=bits[e]
        return m
    pending_mask=[]; previous_row_mask=[]
    for col,pend in states:
        pending_mask.append(mask(edge(a,b) for a,b,c in pend))
        previous_row_mask.append(mask(edge((a[0],a[1]+1),(b[0],b[1]+1))
                                      for a,b,c in pend) if col==0 else 0)
    tests=[]
    for sign in (1,-1):
        tr=lambda p:(p[0],sign*p[1])
        tests.append(([(bits[edge(tr(a),tr(b))],c) for a,b,c in TERMS],
                      mask(edge(tr(a),tr(b)) for a,b in EXC)))
    charge_cache={}
    def charges(seen,parity):
        key=(seen,parity)
        if key not in charge_cache:
            c=1-2*parity
            out=[]
            for terms,exmask in tests:
                f=sum(v for bit,v in terms if seen&bit)
                h=((1+c)//2+c*(f+2))%3
                out.append(2 if seen&exmask==exmask else (1,2,0)[h])
            charge_cache[key]=tuple(out)
        return charge_cache[key]

    # Seed both parities at every row-start state, including states that
    # arise inside a board. Thus the certificate covers arbitrary halves.
    nodes=[(u,0,par) for u,s in enumerate(states) if s[0]==0 for par in (0,1)]
    idx={s:i for i,s in enumerate(nodes)}
    src=array('I'); dst=array('I'); common=array('i')
    penalty_up=array('b'); penalty_down=array('b')
    raw_w=array('b'); raw_w0=array('b')
    for i,(u,seen,par) in enumerate(nodes):
        sofar=seen|pending_mask[u]
        for v,w,w0 in adjacency[u]:
            end=states[v][0]==0
            whole=sofar|(previous_row_mask[v] if end else pending_mask[v])
            t=charges(whole,par) if end else (0,0)
            key=(v,0 if end else whole,1-par if end else par)
            if key not in idx:
                idx[key]=len(nodes); nodes.append(key)
            src.append(i); dst.append(idx[key])
            common.append(3*(4*w-1)+4*(4*w0-1))
            penalty_up.append(t[0]); penalty_down.append(t[1])
            raw_w.append(w); raw_w0.append(w0)
    print('augmented',len(nodes),len(src),'row masks',len(charge_cache),flush=True)
    out={'date':'2026-10-03','base_states':len(states),
         'base_arcs':sum(map(len,adjacency)),'augmented_states':len(nodes),
         'augmented_arcs':len(src),'both_initial_parities':True,
         'retained_row_edges':len(bits),'potentials':{}}
    for orient,t,expected in [('up',penalty_up,-155),('down',penalty_down,-159)]:
        cost=array('i',(b-8*a for b,a in zip(common,t)))
        dist=[0]*len(nodes)
        for passes in range(1,len(nodes)+1):
            changed=False
            for u,v,c in zip(src,dst,cost):
                z=dist[u]+c
                if z<dist[v]:
                    dist[v]=z; changed=True
            if not changed:
                break
        else:
            raise AssertionError('negative cycle')
        interval=(min(dist),max(dist))
        assert interval==(expected,0),(orient,interval)
        reduced=[c+dist[u]-dist[v] for u,v,c in zip(src,dst,cost)]
        assert min(reduced)>=0
        # Retain an exact potential array, in the deterministic node order.
        payload=json.dumps(dist,separators=(',',':')).encode()
        import gzip
        target=Path(f'gap/verifier/claim26_potential_{orient}.json.gz')
        target.write_bytes(gzip.compress(payload,mtime=0))
        out['potentials'][orient]={'range':interval,'passes':passes,
             'checked_arcs':len(src),'minimum_reduced_cost':min(reduced),
             'C':str(Fraction(-expected,12)),
             'sha256_uncompressed':hashlib.sha256(payload).hexdigest()}
        print(orient,interval,'all arc inequalities PASS',flush=True)

    # Independent per-period check of the sharp saturated witness.
    es=set()
    for y in range(-8,12):
        es.update([edge((1,y),(0,y+2)),edge((2,y),(0,y+1)),edge((2,y),(1,y+2))])
    hits=[(e,f) for e,f in combinations(es,2) if cross(e,f)
          and 0<=max(min(p[1] for p in e),min(p[1] for p in f))<2]
    assert len(hits)==4
    assert sum(boundary(e) and boundary(f) for e,f in hits)==2
    for phase in (0,1):
        sums=[0,0]
        for y in range(2):
            seen=mask(edge((a[0],a[1]-y),(b[0],b[1]-y)) for a,b in es
                      if min(a[1],b[1])<=y<=max(a[1],b[1]))
            cs=charges(seen,(y+phase)%2)
            sums=[a+b for a,b in zip(sums,cs)]
        assert sums==[3,3]
    out['sharp_witness']={'rows':2,'X':4,'boundary_crossings':2,
                          'sum_a':'3/2','beta_limit':'4/3'}
    out['elapsed_seconds']=round(time.monotonic()-started,3)
    out['status']='PASS'
    Path('gap/verifier/claim26_certificate.json').write_text(json.dumps(out,indent=2))
    print('CERTIFICATE PASS',out['elapsed_seconds'],'seconds',flush=True)

if __name__=='__main__':
    main()
