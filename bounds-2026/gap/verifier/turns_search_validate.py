"""Independent checker for sequence witnesses."""
from pathlib import Path
import json, hashlib

def read(path):
    data=list(map(int,path.read_text().split()));n=data[0];p=data[1:]
    assert len(p)==n*n and set(p)==set(range(n*n))
    xy=[divmod(v,n) for v in p]
    assert all(sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2] for a,b in zip(xy,xy[1:]+xy[:1]))
    t=sum((a[0]+c[0],a[1]+c[1])!=(2*b[0],2*b[1]) for a,b,c in zip(xy[-1:]+xy[:-1],xy,xy[1:]+xy[:1]))
    return n,p,t

out=[]
for path in sorted(Path('gap/verifier').glob('turns_search_*.txt')):
    n,p,t=read(path)
    edges={tuple(sorted((a,b))) for a,b in zip(p,p[1:]+p[:1])}
    _,seed,st=read(Path(f'gap/verifier/turns_search_seed{n}.txt'))
    se={tuple(sorted((a,b))) for a,b in zip(seed,seed[1:]+seed[:1])}
    out.append(dict(path=str(path),n=n,turns=t,removed_edges=len(se-edges),added_edges=len(edges-se),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    assert t<=st
Path('gap/verifier/turns_search_validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
