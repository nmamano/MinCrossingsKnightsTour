# Check of the tiling view of crossing-free regions (PLAN.md, Theorem T).
# On the p x q torus: enumerate all crossing-free knight 2-factors (same model as
# w-lowerbounds/torus_enum.py), and for each one check by geometry:
#  (1) every quarter triangle is covered by exactly one tile;
#  (2) every square splits along one diagonal ('/' or '\'), and each tile joins two squares of equal split;
#  (3) in a single-split solution, the edges equal the ribbon form (one H/V choice per slope-+-1 ribbon).
# Also builds all 2^p ribbon fields directly and checks degree 2 + zero crossings.
import sys, itertools
sys.path.insert(0, '../../w-lowerbounds')
from collections import Counter
from ortools.sat.python import cp_model
from strip_dp import cross
p = int(sys.argv[1]); q = int(sys.argv[2])
MOV = [(1,2),(2,1),(2,-1),(1,-2)]
E = [(x,y,d[0],d[1]) for x in range(p) for y in range(q) for d in MOV]

def crossings(edges):
    n = 0
    for i, e in enumerate(edges):
        for f in edges[i+1:]:
            for sx in (-p,0,p):
                for sy in (-q,0,q):
                    x,y,dx,dy = e; a,b,c,d = f
                    if cross((x,y,x+dx,y+dy),(a+sx,b+sy,a+sx+c,b+sy+d)): n += 1
    return n

def tile_quarters(e):
    # tile = parallelogram with long diagonal e and short diagonal the unit edge with the same midpoint.
    x,y,dx,dy = e
    mx, my = x+dx/2, y+dy/2
    if abs(dx) == 2: u0, u1 = (mx, my-.5), (mx, my+.5)
    else:            u0, u1 = (mx-.5, my), (mx+.5, my)
    poly = [(x,y), u0, (x+dx,y+dy), u1]
    def inside(pt):
        s = []
        for k in range(4):
            ax,ay = poly[k]; bx,by = poly[(k+1)%4]
            s.append((bx-ax)*(pt[1]-ay)-(by-ay)*(pt[0]-ax))
        return all(v > 1e-9 for v in s) or all(v < -1e-9 for v in s)
    out = []
    for i in range(int(min(x,x+dx))-1, int(max(x,x+dx))+1):
        for j in range(int(min(y,y+dy))-1, int(max(y,y+dy))+1):
            for name,(cx,cy) in (('B',(.5,.2)),('R',(.8,.5)),('T',(.5,.8)),('L',(.2,.5))):
                if inside((i+cx, j+cy)): out.append((i%p, j%q, name))
    assert len(out) == 4, (e, out)
    return out

def analyse(edges):
    cov = Counter()
    owner = {}
    for e in edges:
        for qd in tile_quarters(e):
            cov[qd] += 1; owner[qd] = e
    assert all(cov[(i,j,nm)] == 1 for i in range(p) for j in range(q) for nm in 'BRTL'), 'cover'
    split = {}
    for i in range(p):
        for j in range(q):
            if owner[(i,j,'B')] == owner[(i,j,'R')]:
                assert owner[(i,j,'T')] == owner[(i,j,'L')]; split[(i,j)] = '/'
            else:
                assert owner[(i,j,'R')] == owner[(i,j,'T')] and owner[(i,j,'L')] == owner[(i,j,'B')]; split[(i,j)] = '\\'
    for e in edges:
        sq = {(i,j) for (i,j,_) in tile_quarters(e)}
        assert len(sq) == 2 and len({split[s] for s in sq}) == 1, 'tile joins unequal splits'
    return split

def ribbon_field(choice, slash):
    # '/' : ribbon k = diagonal y-x = k (mod p); H -> a-move (2,1) from cells on y-x=k, V -> b-move (1,2) from y-x=k-1.
    # '\' : mirror image x -> -x.
    edges = []
    for x in range(p):
        for y in range(q):
            k = (y-x) % p if slash else (y+x) % p
            if choice[k] == 'H':
                edges.append((x,y,2,1) if slash else (x,y,-2,1))
            if choice[(k+1) % p] == 'V':
                edges.append((x,y,1,2) if slash else (x,y,-1,2))
    return edges

def canon(edges):
    s = set()
    for (x,y,dx,dy) in edges:
        a = (x%p, y%q, dx, dy); b = ((x+dx)%p, (y+dy)%q, -dx, -dy)
        s.add(min(a,b))
    return frozenset(s)

assert p == q
ribbons = set()
for slash in (True, False):
    for ch in itertools.product('HV', repeat=p):
        ed = ribbon_field(ch, slash)
        deg = Counter()
        for (x,y,dx,dy) in ed: deg[(x,y)] += 1; deg[((x+dx)%p,(y+dy)%q)] += 1
        assert all(deg[(x,y)] == 2 for x in range(p) for y in range(q)), 'degree'
        assert crossings(ed) == 0, 'crossing'
        ribbons.add(canon(ed))
print('ribbon fields: %d distinct, all degree 2 and crossing-free' % len(ribbons))

m = cp_model.CpModel(); xv = {e: m.NewBoolVar('') for e in E}
inc = {(x,y): [] for x in range(p) for y in range(q)}
for e in E:
    x,y,dx,dy = e; inc[(x,y)].append(e); inc[((x+dx)%p,(y+dy)%q)].append(e)
for c in inc: m.Add(sum(xv[e] for e in inc[c]) == 2)
for i, e in enumerate(E):
    for f in E[i+1:]:
        for sx in (-p,0,p):
            for sy in (-q,0,q):
                x,y,dx,dy = e; a,b,c,d = f
                if cross((x,y,x+dx,y+dy),(a+sx,b+sy,a+sx+c,b+sy+d)):
                    m.AddBoolOr([xv[e].Not(), xv[f].Not()])
sols = []
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(s): sols.append([e for e in E if s.Value(xv[e])])
s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
st = s.Solve(m, CB())
stats = Counter(); found = set()
for ed in sols:
    sp = analyse(ed)
    kinds = frozenset(sp.values())
    if len(kinds) == 1:
        assert canon(ed) in ribbons, 'single split but not a ribbon field'
        found.add(canon(ed)); stats['single split (ribbon field)'] += 1
    else:
        stats['both splits (has walls)'] += 1
print(p, q, s.StatusName(st), 'solutions', len(sols), dict(stats))
print('every ribbon field found by the enumeration:', found == ribbons)
