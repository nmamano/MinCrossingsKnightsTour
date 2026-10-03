#!/usr/bin/env python3
"""Small exact checks for the delayed R2 history and run counter."""
from itertools import product

def emit(bits,start=0):
    state=start
    cost=[]
    for b in bits:
        cost.append(int(b and state==4))
        state=min(4,state+1) if b else 0
    return cost,state

def direct_run_cost(bits):
    runs=[]
    length=0
    for b in list(bits)+[0]:
        if b:
            length+=1
        else:
            runs.append(length)
            length=0
    return sum(max(0,l-4) for l in runs)

def delayed(g,z):
    gs=[0]*4
    zs=[0]*2
    flags=[]
    for a,b in zip(g,z):
        flags.append(gs[0]*a*zs[0])
        gs=gs[1:]+[a]
        zs=zs[1:]+[b]
    return flags

for bits in product((0,1),repeat=12):
    costs,end=emit(bits)
    assert sum(costs)==direct_run_cost(bits)
    for split in range(13):
        left,state=emit(bits[:split])
        right,state=emit(bits[split:],state)
        assert left+right==costs and state==end
print('PASS: all 4096 twelve-flag sequences; all thirteen split positions.')

cases=0
for bits in product((0,1),repeat=12):
    g,z=bits[:6],bits[6:]
    actual=delayed(g,z)
    expected=[0]*4+[g[y-2]*g[y+2]*z[y] for y in range(2,4)]
    assert actual==expected
    cases+=1
for n in (8,9,12,32,100):
    g=z=[1]*n
    flags=delayed(g,z)
    assert flags==[0]*4+[1]*(n-4)
    assert sum(emit(flags)[0])==max(0,n-8)
    for split in range(n+1):
        gs,zs=g[:split],z[:split]
        storedg=([0]*4+gs)[-4:]
        storedz=([0]*2+zs)[-2:]
        rest=[]
        for a,b in zip(g[split:],z[split:]):
            rest.append(storedg[0]*a*storedz[0])
            storedg=storedg[1:]+[a]
            storedz=storedz[1:]+[b]
        assert delayed(gs,zs)+rest==flags
print('PASS:',cases,'six-row degree-bit pairs; long blocked runs and preserved split histories.')
