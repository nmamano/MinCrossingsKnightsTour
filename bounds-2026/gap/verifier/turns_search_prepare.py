"""Decode and independently validate the four TT16 seed cycles."""
import json
from pathlib import Path
MOVES=((-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1))
for n in (56,58,60,62):
    d=json.loads(Path(f'w-integrator/tours/certificates/TT16_n{n}.json').read_text())
    adj=[]
    for r,row in enumerate(d['tour']):
        for c,code in enumerate(row):
            ns=[]
            for k in code:
                dr,dc=MOVES[int(k)]; rr,cc=r+dr,c+dc
                assert 0<=rr<n and 0<=cc<n
                ns.append(rr*n+cc)
            assert len(set(ns))==2
            adj.append(ns)
    assert len(adj)==n*n
    for a,ns in enumerate(adj):
        assert all(a in adj[b] for b in ns)
    seq=[]; prev=-1; cur=0
    while cur not in seq:
        seq.append(cur)
        nxt=next(b for b in adj[cur] if b!=prev)
        prev,cur=cur,nxt
    assert cur==0 and len(seq)==n*n
    turns=sum((a//n+c//n!=2*(b//n) or a%n+c%n!=2*(b%n)) for a,b,c in zip(seq[-1:]+seq[:-1],seq,seq[1:]+seq[:1]))
    assert turns==8*n-14
    Path(f'gap/verifier/turns_search_seed{n}.txt').write_text(f'{n}\n'+ ' '.join(map(str,seq))+'\n')
    print(n,turns)
