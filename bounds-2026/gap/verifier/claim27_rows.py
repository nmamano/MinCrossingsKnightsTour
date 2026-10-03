"""Independent complete row records for N1, using our Claim 26 forest builder.
No author implementation imports. Writes compact integer records for C++ relaxation.
"""
from claim26_certificate import transitions, edge, TERMS, EXC
from pathlib import Path
import struct,json,time

def main():
    start=time.monotonic()
    states=[(0,())]; ids={states[0]:0}; adj=[]
    for s in states:
        out=[]
        for t,w,w0 in transitions(s):
            if t not in ids:
                ids[t]=len(states); states.append(t)
            out.append((ids[t],w,w0))
        assert len({v for v,w,w0 in out})==len(out)
        adj.append(out)
    assert (len(states),sum(map(len,adj)))==(82516,144674)
    starts=[u for u,(x,es) in enumerate(states) if x==0]
    rowid={u:i for i,u in enumerate(starts)}
    tests=[]
    for sign in (1,-1):
        tr=lambda p:(p[0],sign*p[1])
        tests.append(({edge(tr(a),tr(b)):c for a,b,c in TERMS},
                      {edge(tr(a),tr(b)) for a,b in EXC}))
    rows=[]
    for u0 in starts:
        seen=frozenset(edge(a,b) for a,b,c in states[u0][1])
        todo=[(u0,seen,0,0,0,0)]
        while todo:
            u,seen,crossings,boundary,d2,d3=todo.pop()
            x,pend=states[u]
            incoming=sum(b==(x,0) for a,b,c in pend)
            for v,w,w0 in adj[u]:
                sh=int(x==3)
                new=[edge((a[0],a[1]+sh),(b[0],b[1]+sh))
                     for a,b,c in states[v][1] if a==(x,-sh)]
                whole=seen.union(new)
                degree=incoming+len(new)
                g2=degree if x==2 else d2
                g3=degree if x==3 else d3
                if x<3:
                    todo.append((v,whole,crossings+w,boundary+w0,g2,g3))
                else:
                    endpoint=[]
                    for co,ex in tests:
                        endpoint.extend([sum(c for e,c in co.items() if e in whole)%3,int(ex<=whole)])
                    rows.append((rowid[u0],rowid[v],4*(crossings+w)-4,4*(boundary+w0)-4,*endpoint,g2,g3))
    assert len(starts)==21420 and len(rows)==250990
    with Path('gap/verifier/claim27_rows.bin').open('wb') as f:
        f.write(struct.pack('<II',len(starts),len(rows)))
        for r in rows:
            f.write(struct.pack('<10i',*r))
    meta=dict(date='2026-10-03',base_states=len(states),base_arcs=sum(map(len,adj)),row_states=len(starts),row_arcs=len(rows),elapsed_seconds=time.monotonic()-start)
    Path('gap/verifier/claim27_rows.json').write_text(json.dumps(meta,indent=2))
    print(meta,flush=True)
if __name__=='__main__': main()
