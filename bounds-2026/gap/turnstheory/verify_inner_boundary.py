#!/usr/bin/env python3
"""Check the saved potential with a separate strip implementation.

The original strip builder stays read-only. Its boundary degree rule is
relaxed in memory; this lets every path forest start at the empty state.
No code from check_inner_boundary.py is imported.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'w-lowerbounds/strip_dp.py').read_text()
old='need = [r] if (fam is None or warm >= 3) else list(range(0, r + 1))'
assert source.count(old)==1
source=source.replace(old,'need = list(range(0, r + 1))')
module={'__name__':'independent_soft_strip'}
exec(compile(source,'read-only strip_dp.py with soft boundary rule','exec'),module)
states,adj,width=module['build'](1)
assert width==3
saved=json.loads(Path(__file__).with_name('inner_boundary_certificate.json').read_text())
def key(col,edges):
    return col,tuple((tuple(a),tuple(b),label) for a,b,label in edges)
potential={key(col,edges):p for (col,edges),p in zip(saved['states'],saved['potential'])}
assert len(potential)==len(states)==330
P=[]
for col,edges,warm in states:
    assert warm==0
    P.append(potential[key(col,[((a,b),(c,d),label) for a,b,c,d,label in edges])])
checked=0
for u,out in enumerate(adj):
    col,edges,_=states[u]
    inc=sum(c==col and d==0 for a,b,c,d,label in edges)
    for v,w in out:
        nextcol,nextedges,_=states[v]
        shift=int(nextcol==0)
        selected=sum(a==col and b==-shift for a,b,c,d,label in nextedges)
        if col==0 and inc+selected!=2:
            continue
        assert 3*w-1+P[u]-P[v]>=0,(u,v,w)
        checked+=1
phase0=[P[u] for u,(col,_,_) in enumerate(states) if col==0]
assert checked==580
assert max(phase0)-min(phase0)==12
print('PASS: separate builder, 330 states, 580 hard arcs; interval loss <= 4.')
