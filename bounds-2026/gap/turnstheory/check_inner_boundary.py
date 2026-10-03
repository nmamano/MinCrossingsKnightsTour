#!/usr/bin/env python3
"""Exact interval certificate for a column with no edges to its left.

States permit degree 0, 1, or 2, so intervals need no reachability
assumption at their ends. Only degree-two boundary arcs enter the
potential inequalities. Run from the research root with Python 3.
"""
from collections import deque
from itertools import combinations
import json
from pathlib import Path


def cross(e, f):
    def det(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    a, b = e
    c, d = f
    return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0


def successors(state):
    col, pending = state
    here = (col, 0)
    incoming = [e for e in pending if e[1] == here]
    rest = [e for e in pending if e[1] != here]
    if len(incoming)>2 or (len(incoming)==2 and incoming[0][2]==incoming[1][2]):
        return
    targets = [(col+dx,dy) for dx,dy in ((1,2),(-1,2),(2,1),(-2,1))
               if 0<=col+dx<3 and (col==0 or col+dx==0)]
    for count in range(3-len(incoming)):
        for chosen in combinations(targets,count):
            load = {}
            for a,b,c in rest:
                load[b]=load.get(b,0)+1
            for b in chosen:
                load[b]=load.get(b,0)+1
            if any(d>2 for d in load.values()):
                continue
            new = [(here,b) for b in chosen]
            weight = sum(cross(e,(a,b)) for e in new for a,b,c in rest)
            weight += sum(cross(e,f) for e,f in combinations(new,2))
            label = incoming[0][2] if incoming else -1
            merge = incoming[1][2] if len(incoming)==2 else None
            edges = [(a,b,label if merge is not None and c==merge else c) for a,b,c in rest]
            edges += [(a,b,label) for a,b in new]
            shift = int(col==2)
            edges = sorted(((a[0],a[1]-shift),(b[0],b[1]-shift),c) for a,b,c in edges)
            labels = {}
            canon = []
            for a,b,c in edges:
                if c not in labels:
                    labels[c]=len(labels)
                canon.append((a,b,labels[c]))
            full = col!=0 or len(incoming)+count==2
            yield ((col+1)%3,tuple(canon)), weight, full


def main():
    states = [(0,())]
    index = {states[0]:0}
    todo = deque([0])
    arcs = []
    while todo:
        u = todo.popleft()
        for target,w,full in successors(states[u]):
            if target not in index:
                index[target]=len(states)
                states.append(target)
                todo.append(index[target])
            arcs.append((u,index[target],w,full))
    hard = [(u,v,3*w-1) for u,v,w,full in arcs if full]
    potential = [0]*len(states)
    for iteration in range(len(states)+1):
        changed=False
        for u,v,w in hard:
            if potential[v]>potential[u]+w:
                potential[v]=potential[u]+w
                changed=True
        if not changed:
            break
    assert not changed, 'negative cycle in complete-row transitions'
    assert all(w+potential[u]-potential[v]>=0 for u,v,w in hard)
    phase0 = [potential[u] for u,s in enumerate(states) if s[0]==0]
    result = dict(date='2026-10-03', states=len(states), arcs=len(arcs),
                  hard_arcs=len(hard), passes=iteration+1,
                  potential_range=[min(potential),max(potential)],
                  row_boundary_potential_range=[min(phase0),max(phase0)],
                  interval_error_numerator=max(phase0)-min(phase0),
                  interval_error_denominator=3)
    print(json.dumps(result,indent=2))
    out=Path(__file__).with_name('inner_boundary_certificate.json')
    out.write_text(json.dumps(dict(result=result, states=states,
                                  potential=potential),indent=2)+'\n')


if __name__=='__main__':
    main()
