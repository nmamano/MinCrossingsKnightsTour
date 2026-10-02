"""Periodic finite-width fold repair. One CP-SAT worker; small model."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ortools.sat.python import cp_model
from kt.core import seg_cross
M=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]

def run(D,P,flux=1,seconds=3,zero=False,force_long=False,cap=None):
    # Cell (u,v) denotes Cartesian (u+v,v). u is the normal coordinate.
    cells=[(u,v) for u in range(D) for v in range(P)]
    edges=[];fixed=[]
    for u,v in cells:
        for dx,dy in M:
            du=dx-dy
            if du<=0 or u+du>=D:continue
            edges.append(((u,v),(u+du,v+dy)))
    # Fixed outside A edges enter the strip; B edges leave it.
    fixed=[((-1,v),(0,v+1)) for v in range(P)]+[((D-1,v),(D,v-2)) for v in range(P)]
    m=cp_model.CpModel();x=[m.NewBoolVar(f'e{i}') for i in range(len(edges))]
    if force_long:m.Add(sum(z for z,(a,b) in zip(x,edges) if b[0]-a[0]==3)>=1)
    inc={p:[] for p in cells};fc={p:0 for p in cells}
    for i,e in enumerate(edges):
        for u,v in e:inc[u,v%P].append(x[i])
    for e in fixed:
        for u,v in e:
            if (u,v%P) in fc:fc[u,v%P]+=1
    for p in cells:m.Add(sum(inc[p])+fc[p]==2)
    # Baseline uses B=(-1,-2), i.e. du=1,dv=-2 in all internal layers.
    coeff=[((-1)**a[0])*(b[1]//P) for a,b in edges]
    ref=sum(c for c,(a,b) in zip(coeff,edges) if (b[0]-a[0],b[1]-a[1])==(1,-2))
    m.Add(sum(c*z for c,z in zip(coeff,x))-ref==flux)
    def cart(p):u,v=p;return(u+v,v)
    def seg(e,k=0):return tuple(cart((u,v+k*P)) for u,v in e)
    allE=edges+fixed;terms=[];crossdata=[]
    for i,e in enumerate(allE):
        for j in range(i,len(allE)):
            f=allE[j];count=0
            for k in range(-2,3):
                if i==j and k==0:continue
                if seg_cross(*seg(e),*seg(f,k)):count+=1
            if i==j:assert count%2==0;count//=2
            if not count:continue
            crossdata.append((i,j,count))
            if i>=len(edges):
                assert j>=len(edges)
                if zero:raise AssertionError('fixed edges cross')
                terms.append(count)
            elif j>=len(edges):
                if zero:m.Add(x[i]==0)
                else:terms.append(count*x[i])
            elif i==j:
                if zero:m.Add(x[i]==0)
                else:terms.append(count*x[i])
            else:
                if zero:m.Add(x[i]+x[j]<=1)
                else:
                    z=m.NewBoolVar('cross');m.Add(z>=x[i]+x[j]-1);terms.append(count*z)
    if not zero:
        if cap is None:m.Minimize(sum(terms))
        else:m.Add(sum(terms)<=cap)
        # A single mixed layer supplies a known four-crossing solution when P=6.
        if cap is None and flux==1 and P%3==0:
            for z,(a,b) in zip(x,edges):
                du,dv=b[0]-a[0],b[1]-a[1]
                want_a=a[0]==0 and a[1]%3==0
                m.AddHint(z,int(du==1 and dv==(1 if want_a else -2)))
    s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=seconds
    st=s.Solve(m)
    out=dict(D=D,P=P,flux=flux,zero=zero,force_long=force_long,cap=cap,status=s.StatusName(st),seconds=s.WallTime())
    if st in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        out.update(crossings=0 if zero else sum(count for i,j,count in crossdata if (i>=len(edges) or s.Value(x[i])) and (j>=len(edges) or s.Value(x[j]))),bound=0 if zero else s.BestObjectiveBound(),
                   chosen=[e for e,z in zip(edges,x) if s.Value(z)],fixed=fixed)
    print(json.dumps({k:v for k,v in out.items() if k not in ('chosen','fixed')}),flush=True)
    return out
if __name__=='__main__':
    D=int(sys.argv[1]);P=int(sys.argv[2]);flux=int(sys.argv[3]) if len(sys.argv)>3 else 1
    out=run(D,P,flux,seconds=5,zero='zero' in sys.argv,force_long='long' in sys.argv)
    Path(__file__).with_name(f'corridor-D{D}-P{P}-F{flux}.json').write_text(json.dumps(out,indent=2))
