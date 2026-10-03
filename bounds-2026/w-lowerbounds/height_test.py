"""Hypothesis H: for crossing-free 2-factors, the flux potential h mod 3 (relative to the pure (2,1)
family) is a local function of the configuration near the dual point (up to a constant per config)."""
import sys, itertools
from collections import defaultdict
from ortools.sat.python import cp_model
from strip_dp import cross
def enum(p, q, tl=600):
    MOV=[(1,2),(2,1),(2,-1),(1,-2)]
    E=[(x,y,d[0],d[1]) for x in range(p) for y in range(q) for d in MOV]
    m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
    inc={(x,y):[] for x in range(p) for y in range(q)}
    for e in E:
        x,y,dx,dy=e; inc[(x,y)].append(e); inc[((x+dx)%p,(y+dy)%q)].append(e)
    for c in inc: m.Add(sum(xv[e] for e in inc[c])==2)
    for e in E:
        for f in E:
            if f<=e: continue
            for sx in (-p,0,p):
                for sy in (-q,0,q):
                    x,y,dx,dy=e; a,b,c,d=f
                    if cross((x,y,x+dx,y+dy),(a+sx,b+sy,a+sx+c,b+sy+d)): m.AddBoolOr([xv[e].Not(),xv[f].Not()])
    sols=[]
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(s): sols.append([e for e in E if s.Value(xv[e])])
    s=cp_model.CpSolver(); s.parameters.enumerate_all_solutions=True; s.parameters.num_workers=1; s.parameters.max_time_in_seconds=tl
    s.Solve(m,CB()); return sols
chi=lambda x,y: 1 if (x+y)%2==0 else -1
def seg_flux(edges, A, B):
    """sum over edges (planar, unrolled copies given) crossing directed segment A->B of chi(left end)"""
    tot=0
    for (a,b) in edges:
        if cross((*A,*B),(*a,*b)):
            # left of A->B: cross product > 0
            def side(P): return (B[0]-A[0])*(P[1]-A[1])-(B[1]-A[1])*(P[0]-A[0])
            left=a if side(a)>0 else b
            tot+=chi(*left)
    return tot
def heights(sol, p, q):
    # unrolled edges near the fundamental domain
    ed=[]
    for (x,y,dx,dy) in sol:
        for sx in (-p,0,p):
            for sy in (-q,0,q):
                ed.append(((x+sx,y+sy),(x+dx+sx,y+dy+sy)))
    ref=[]
    for x in range(-p,2*p):
        for y in range(-q,2*q):
            ref.append(((x,y),(x+2,y+1)))
    # local edge lists per dual segment for speed
    def near(lst, A, B):
        cx,cy=(A[0]+B[0])/2,(A[1]+B[1])/2
        return [e for e in lst if abs(e[0][0]-cx)<3.5 and abs(e[0][1]-cy)<3.5]
    h={(0,0):0}
    order=[(i,j) for j in range(q) for i in range(p)]
    for (i,j) in order:
        if (i,j)==(0,0): continue
        if i>0: P0=(i-1,j)
        else: P0=(i,j-1)
        A=(P0[0]+0.5,P0[1]+0.5); B=(i+0.5,j+0.5)
        h[(i,j)]=h[P0]+seg_flux(near(ed,A,B),A,B)-seg_flux(near(ref,A,B),A,B)
    # consistency check around the torus (wrap) mod 3
    return h, ed
def window_key(ed, i, j, r):
    # chosen edges with both ends within the (2r)x(2r) block around dual point (i+.5,j+.5), relative
    keys=[]
    for (a,b) in ed:
        if all(i-r+1<=c[0]<=i+r and j-r+1<=c[1]<=j+r for c in (a,b)):
            keys.append(((a[0]-i,a[1]-j),(b[0]-i,b[1]-j)))
    return tuple(sorted(keys))
if __name__=='__main__':
    tori=[(6,6),(6,8),(8,8)]
    data=[]
    for (p,q) in tori:
        sols=enum(p,q); print(p,q,len(sols),flush=True)
        for k,sol in enumerate(sols):
            h,ed=heights(sol,p,q)
            data.append(((p,q,k),h,ed))
    for r in (1,2,3):
        # union-find over nodes: ('cfg',id) and ('pat',key); edge with offset value: h = L(pat) + c(cfg)
        par={}; off={}
        def find(u):
            if par[u]==u: return u,0
            r_,o=find(par[u]); par[u]=r_; off[u]=(off[u]+o)%3; return r_,off[u]
        def add(u):
            if u not in par: par[u]=u; off[u]=0
        bad=0; checked=0
        for (cid,h,ed) in data:
            p,q,_=cid
            add(('c',cid))
            for (i,j),hv in h.items():
                key=('p',(i%2+j%2*2), window_key(ed,i,j,r))   # include colour class of the dual point
                add(key)
                # constraint: hv = L(key) + c(cid)  => L(key) - (-c(cid))... use potentials: val(key)-val(cfg) = hv
                ru,ou=find(key); rv,ov=find(('c',cid))
                if ru==rv:
                    checked+=1
                    if (ou-ov-hv)%3!=0: bad+=1
                else:
                    par[ru]=rv; off[ru]=(hv+ov-ou)%3
        print('window r',r,'checked',checked,'violations',bad,flush=True)
