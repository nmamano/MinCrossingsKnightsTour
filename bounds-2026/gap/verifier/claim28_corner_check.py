"""Independent local substitution into the audited endpoint coefficient table."""
import json
from pathlib import Path
T=[(((0,-1),(1,1)),-1),(((0,0),(1,-2)),-1),
   (((0,0),(2,-1)),-1),(((0,1),(1,-1)),1),
   (((0,1),(2,0)),1),(((0,2),(1,0)),-1),
   (((1,0),(2,2)),-1),(((1,1),(2,-1)),-1)]
def present(e,s):
    a,b=sorted(e)
    return (b[0]-a[0]==2 and b[1]-a[1]==s) or (a[0]==0 and b[0]==1 and b[1]-a[1]==2*s)
r=[]
for s in (-1,1):
    for direction in (-1,1):
        def selected(e):
            return present(tuple((x,direction*y) for x,y in e),s)
        F=sum(c for e,c in T if selected(e))
        exc=selected(((0,0),(2,1))) and selected(((0,1),(2,0)))
        assert F%3==2 and not exc
        for R in (0,1):
            Q=(1+(-1)**R+2*((-1)**R)*(F+2))%3
            gamma=(-Q)%3
            assert Q==1 and gamma==2
            r.append(dict(field_slope=s,scan=direction,row_parity=R,F=F,exception=exc,Q=Q,gamma=gamma))
Path('gap/verifier/claim28_corner_check.json').write_text(json.dumps(r,indent=2))
print('PASS: P/P-prime, both scan directions and row parities; Q=1, gamma=2 modulo 3')
