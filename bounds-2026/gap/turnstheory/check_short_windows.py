#!/usr/bin/env python3
"""Exact short-run and period-eight window limits in the soft strip."""
import json
from pathlib import Path
from check_run_credit import first_graph,second_graph,rows

def minimum(states,arcs,flags):
    phase0=[u for u,s in enumerate(states) if s[0]==0]
    reverse={}
    for u,v,w,full in arcs:
        reverse.setdefault(v,[]).append(u)
    empty=states.index((0,()))
    finishable={empty}
    todo=[empty]
    while todo:
        for u in reverse.get(todo.pop(),[]):
            if u not in finishable:
                finishable.add(u)
                todo.append(u)
    dist={u:0 for u in phase0}
    for flag in flags:
        nxt=dict.fromkeys(phase0,10**9)
        for u,v,w,full in arcs:
            if full or not flag:
                nxt[v]=min(nxt[v],dist[u]+w)
        dist=nxt
    value=min(dist.values())
    # A minimising walk must also extend to a finite forest. Reachable
    # but doomed states can contain a cycle that the scan rejects later.
    assert min(dist[u] for u in finishable)==value
    return value

def main():
    s,a=first_graph();r=rows(s,a)
    s2,a2=second_graph();r2=rows(s2,a2)
    full=[]
    for n in range(1,17):
        value=minimum(s,r,[1]*n)
        assert value==minimum(s2,r2,[1]*n)==max(0,n-4)
        full.append(value)
    pattern=[int(y in (1,2,5,6,7)) for y in range(8)]
    windows=[]
    for phase in range(8):
        flags=[pattern[(phase+y)%8] for y in range(16)]
        value=minimum(s,r,flags)
        assert value==minimum(s2,r2,flags)>=1
        windows.append(value)
    assert windows==[2,2,2,3,3,2,1,1]
    result=dict(date='2026-10-03',full_run_minima_1_through_16=full,
                period8_mask=pattern,window_length=16,phase_minima=windows,
                uniform_window_credit=1,
                scope='assigned crossing minima in the soft width-one strip')
    Path(__file__).with_name('short_window_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print('PASS: two builders; zero assigned crossings possible in runs of length 1..4; every listed 16-row window costs at least one.')

if __name__=='__main__':main()
