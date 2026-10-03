#!/usr/bin/env python3
"""Global run credit with cap 3, checked by two soft-strip builders."""
from collections import deque
from pathlib import Path
import json
import check_inner_boundary as C

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def first_graph():
    states=[(0,())]
    index={states[0]:0}
    adj=[]
    for state in states:
        out=[]
        for target,w,full in C.successors(state):
            if target not in index:
                index[target]=len(states)
                states.append(target)
            out.append((index[target],w,full))
        adj.append(out)
    return states,adj

def rows(states,adj):
    result=set()
    for u,s in enumerate(states):
        if s[0]!=0:continue
        for a,w,full in adj[u]:
            for b,x,_ in adj[a]:
                for v,y,_ in adj[b]:
                    result.add((u,v,w+x+y,full))
    return sorted(result)

def solve(states,rowarcs,cap):
    nodes=[(u,c) for u,s in enumerate(states) if s[0]==0 for c in range(cap+1)]
    arcs=[]
    for u,v,w,full in rowarcs:
        for c in range(cap+1):
            k=int(full and c==cap)
            nc=min(c+1,cap) if full else 0
            arcs.append(((u,c),(v,nc),w-k,(u,v,w,full,c)))
    d=dict.fromkeys(nodes,0)
    pred={}
    for iteration in range(len(nodes)):
        changed=None
        for u,v,w,meta in arcs:
            if d[v]>d[u]+w:
                d[v]=d[u]+w
                pred[v]=(u,w,meta)
                changed=v
        if changed is None:
            assert all(w+d[u]-d[v]>=0 for u,v,w,_ in arcs)
            return d,None,len(arcs)
    v=changed
    for _ in nodes:v=pred[v][0]
    start=v
    cycle=[]
    while True:
        u,w,meta=pred[v]
        cycle.append((w,meta))
        v=u
        if v==start:break
    cycle.reverse()
    assert sum(w for w,_ in cycle)<0
    return None,cycle,len(arcs)

def second_graph():
    source=(ROOT/'w-lowerbounds/strip_dp.py').read_text()
    old='need = [r] if (fam is None or warm >= 3) else list(range(0, r + 1))'
    assert source.count(old)==1
    scope={'__name__':'independent_soft_strip'}
    exec(compile(source.replace(old,'need = list(range(0, r + 1))'),
                 'softened separate strip builder','exec'),scope)
    raw,oldadj,width=scope['build'](1)
    assert width==3
    states=[(col,tuple(((a,b),(c,d),lab) for a,b,c,d,lab in edges))
            for col,edges,warm in raw]
    adj=[]
    for u,out in enumerate(oldadj):
        col,edges=states[u]
        incoming=sum(b==(col,0) for a,b,c in edges)
        newout=[]
        for v,w in out:
            shift=int(states[v][0]==0)
            chosen=sum(a==(col,-shift) for a,b,c in states[v][1])
            full=col!=0 or incoming+chosen==2
            newout.append((v,w,full))
        adj.append(newout)
    return states,adj

def main():
    states,adj=first_graph()
    rr=rows(states,adj)
    potential,cycle,numarcs=solve(states,rr,3)
    assert cycle is None and min(potential.values())==-4 and max(potential.values())==0
    saved={(states[u],c):p for (u,c),p in potential.items()}
    states2,adj2=second_graph()
    rr2=rows(states2,adj2)
    encode=lambda ss,rr:{(ss[u],ss[v],w,f) for u,v,w,f in rr}
    assert encode(states,rr)==encode(states2,rr2)
    checked=0
    for u,v,w,full in rr2:
        for c in range(4):
            k=int(full and c==3)
            nc=min(c+1,3) if full else 0
            assert w-k+saved[states2[u],c]-saved[states2[v],nc]>=0
            checked+=1
    assert checked==numarcs
    failures={}
    for cap in (0,1,2):
        p,cyc,_=solve(states,rr,cap)
        assert p is None
        failures[cap]=cyc
    result=dict(date='2026-10-03',states=len(states),row_arcs=len(rr),
                augmented_nodes=len(potential),checked_arcs=checked,
                cap=3,potential_range=[-4,0],arbitrary_subwalk_error=4,
                finite_forest_error=0,
                excluded_caps=failures)
    data=dict(result=result,potential=[dict(state=states[u],counter=c,value=p)
                                      for (u,c),p in potential.items()])
    (HERE/'run_credit_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print('PASS: two builders; cap-3 finite-forest credit with zero error; arbitrary subwalk error 4; caps 0,1,2 have negative cycles.')

if __name__=='__main__':main()
