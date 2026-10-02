"""Reproducible figures. Geometry/counts are independently checked; kt only generates baselines."""
import sys,json,hashlib,math
from pathlib import Path
from collections import defaultdict
from itertools import combinations
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'w-verifier')]
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle,Arc,FancyArrowPatch
from matplotlib.lines import Line2D
from check import MOVES,check,proper,orient
from kt.gentour import gen_tour
from kt import templates as K
from strand_audit import pairing
OUT=ROOT/'w-viz';DATE='2026-10-02'
import argparse
_ap=argparse.ArgumentParser();_ap.add_argument('--only',default='');_args=_ap.parse_args()
ONLY=set(_args.only.split(',')) if _args.only else set()
BG='#fbfaf7';INK='#23343c';MUTED='#637b89';FAINT='#dce4e6';RED='#cf483e';TEAL='#087f80'
STRANDS=[TEAL,'#5b68a5','#bd842f','#985785']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.labelcolor':INK,'axes.titlecolor':INK,'figure.facecolor':BG,'axes.facecolor':BG,'savefig.facecolor':BG,'svg.fonttype':'none','axes.titleweight':'bold','axes.titlesize':15})
MET={'date':DATE,'tours':{},'strips':{},'certificate':{}}

def crossings(E):
    E=sorted(E);bins=defaultdict(list);pairs=[];pts=[]
    for k,(a,b) in enumerate(E):
        keys=[(i,j) for i in range(min(a[0],b[0])//4,max(a[0],b[0])//4+1) for j in range(min(a[1],b[1])//4,max(a[1],b[1])//4+1)]
        cand={v for key in keys for v in bins[key]}
        for v in cand:
            c,d=E[v]
            if proper((a,b),(c,d)):
                u=(b[0]-a[0],b[1]-a[1]);w=(d[0]-c[0],d[1]-c[1]);den=u[0]*w[1]-u[1]*w[0]
                t=((c[0]-a[0])*w[1]-(c[1]-a[1])*w[0])/den
                pts.append((a[0]+t*u[0],a[1]+t*u[1]));pairs.append(((a,b),(c,d)))
        for key in keys:bins[key].append(k)
    return pts,pairs

def tour_data(name,g,source):
    x,t=check(g);n=len(g);E=set();turn=[]
    for r in range(n):
        for c in range(n):
            p=(c,n-1-r);ds=[(MOVES[int(k)][1],-MOVES[int(k)][0]) for k in g[r][c]]
            if orient(ds[0],(0,0),ds[1]):turn.append(p)
            for dx,dy in ds:E.add(tuple(sorted((p,(c+dx,n-1-r+dy)))))
    pts,_=crossings(E);assert len(pts)==x and len(turn)==t
    MET['tours'][name]={'n':n,'crossings':x,'turns':t,'source':source,'grid_sha256':hashlib.sha256(json.dumps(g).encode()).hexdigest()}
    return dict(name=name,g=g,n=n,E=E,turn=turn,cross=pts,X=x,T=t)

def load(name,path):
    d=json.loads((ROOT/path).read_text());z=tour_data(name,d['tour'],path)
    assert z['X']==d['crossings'] and z['T']==d['turns'];return z

def strip(tpl,length=40):
    a=[r.split() for r in tpl];h=len(a);w=len(a[0])
    def adj(p):
        x,y=p;s=a[h-1-y][x%w] if 0<=y<h else '26'
        return [(x+MOVES[int(k)][1],y-MOVES[int(k)][0]) for k in s]
    E=set();turn=[]
    for x in range(-8,length+9):
        for y in range(10):
            ns=adj((x,y))
            for q in ns:
                assert q[1]>=0
                if 0<=q[1]<10:assert (x,y) in adj(q)
                E.add(tuple(sorted(((x,y),q))))
            if 0<=x<length and y<8 and orient(ns[0],(x,y),ns[1]):turn.append((x,y))
    pts,_=crossings(E);pts=[p for p in pts if -.5<=p[0]<length-.5 and -.5<=p[1]<7.5]
    colored=[];used=set()
    for c in range(24,40):
        for x in range(-8,length+9):
            for y in range(h):
                p=(x,y)
                for q in adj(p):
                    if q[1]<h or q[0]+2*q[1]!=c:continue
                    prev=q;cur=p;path=[q,p];seen=set()
                    while cur[1]<h:
                        assert cur not in seen;seen.add(cur)
                        nxt=next(v for v in adj(cur) if v!=prev);prev,cur=cur,nxt;path.append(cur)
                    end=cur[0]+2*cur[1];key=tuple(sorted((c,end)))
                    if key in used:continue
                    used.add(key)
                    for endpoint in [path[0],path[-1]]:
                        here=endpoint
                        while here[1]<7:
                            nxt=(here[0]-2,here[1]+1);path.extend([here,nxt]);here=nxt
                    pe=[(a,b) for a,b in E if a in seen or b in seen]
                    for cc in (c,end):
                        for yy in range(h,7):pe.append(((cc-2*yy,yy),(cc-2*(yy+1),yy+1)))
                    colored.append((pe,c,end))
                    if len(colored)==4:return dict(E=E,turn=turn,cross=pts,colored=colored,length=length,h=h)
    raise AssertionError('four strands not found')

def clean(ax):
    ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
    for s in ax.spines.values():s.set_visible(False)

def points(ax,pts,**kw):
    if pts:ax.scatter(*zip(*pts),**kw)

def draw_strip(ax,s,mode='cross',color=False):
    clean(ax);ax.axhspan(-.5,s['h']-.5,color='#edf1ef',zorder=0)
    for yy in range(s['h']):ax.plot([-.5,s['length']-.5],[yy,yy],color=FAINT,lw=.5,zorder=0)
    ax.add_collection(LineCollection(list(s['E']),colors=MUTED,linewidths=.8,alpha=.65,zorder=1))
    if color:
        for ix,(E,a,b) in enumerate(s['colored']):
            ax.add_collection(LineCollection(E,colors=STRANDS[ix],linewidths=2.0,zorder=2))
            for c in (a,b):
                xx=c-14
                if 0<=xx<s['length']:ax.text(xx,7.2,str(c),ha='center',fontsize=9,color=STRANDS[ix],weight='bold')
    if mode=='cross':points(ax,s['cross'],s=14,c=RED,zorder=4,edgecolors=BG,linewidths=.22)
    else:points(ax,s['turn'],s=22,c=INK,zorder=4,edgecolors=BG,linewidths=.35)
    ax.set_xlim(-.5,s['length']-.5);ax.set_ylim(-.8,8.3)
    for x in [-.5,s['length']-.5]:ax.axvline(x,color=MUTED,lw=.7,ls=(0,(3,3)))

def board(ax,d,mode='cross'):
    clean(ax);n=d['n'];ax.add_patch(Rectangle((-.6,-.6),n+.2,n+.2,fill=False,edgecolor=FAINT,lw=.8))
    ax.add_collection(LineCollection(list(d['E']),colors=MUTED,linewidths=.48,alpha=.6,zorder=1))
    points(ax,d['cross'] if mode=='cross' else d['turn'],s=4.2 if mode=='cross' else 5.2,c=RED if mode=='cross' else INK,zorder=3,linewidths=0)
    ax.set_xlim(-1,n);ax.set_ylim(-1,n)

def title(fig,text,sub):
    fig.text(.055,.975,text,fontsize=23,weight='bold',va='top')
    fig.text(.055,.94,sub,fontsize=11,color=MUTED,va='top')
    fig.text(.945,.975,DATE,fontsize=10,ha='right',va='top',color=MUTED)

def save(fig,name,footer):
    if ONLY and name[:2] not in ONLY:
        plt.close(fig);return
    fig.text(.055,.02,footer,fontsize=9,color=MUTED,va='bottom')
    for ext in ('png','svg'):fig.savefig(OUT/f'{name}.{ext}',dpi=200)
    plt.close(fig);print(name,flush=True)

# Every concrete tour is validated and independently recounted.
paper=tour_data('paper72',gen_tour(72,72,heel=K.Sequence1Opt),'kt.gentour / Sequence1Opt')
sh=tour_data('shisheng72',gen_tour(72,72,heel=K.Sequence1Opt,block=(K.SequenceP40,40),block_top=True),'kt.gentour / SequenceP40 on BOTH horizontal sides')
h16=load('H16a72','w-integrator/tours/H16a_VerticalEdge_off0_n72.json')
lf=load('LF2_72','w-integrator/tours/LF2_n72.json')
tt16=load('TT16_56','w-integrator/tours/certificates/TT16_n56.json')
t18=load('T18_64','w-integrator/tours/certificates/T18_VerticalEdge_off0_n64.json')
small=tour_data('paper16',gen_tour(16,16,heel=K.Sequence1Opt),'kt.gentour / Sequence1Opt')
h16tpl=json.loads((ROOT/'w-integrator/tours/H16a_VerticalEdge_off0_n72.json').read_text())['bottom']
t16tpl=json.loads((ROOT/'w-turnsbuilder/lex-free-P8-D4.json').read_text())['template']
t18tpl=json.loads((ROOT/'w-turnsbuilder/T18-P8-D4.json').read_text())
strips={k:strip(v) for k,v in [('paper',K.Sequence1Opt),('Shisheng',K.SequenceP40),('H16a',h16tpl),('T18',t18tpl),('T16',t16tpl)]}
for k,s in strips.items():MET['strips'][k]={'columns':40,'crossings':len(s['cross']),'turns':len(s['turn']),'colored_terminal_pairs':[(a,b) for _,a,b in s['colored']]}
assert [len(strips[k]['cross']) for k in ['paper','Shisheng','H16a']]==[140,130,80]
assert len(strips['paper']['turn'])==110 and len(strips['T18']['turn'])==90 and len(strips['T16']['turn'])==80
assert tt16['T']==434==8*tt16['n']-14

# 1: equal-length heels.
fig,axs=plt.subplots(3,1,figsize=(17,11));fig.subplots_adjust(left=.055,right=.945,top=.885,bottom=.095,hspace=.38)
title(fig,'Crossing heels: 3.50 → 3.25 → 2.00 per column','The same 40 columns in every panel. Red dots mark crossings; four colored paths expose terminal pairing.')
for ax,key,label,per,cnt in zip(axs,['paper','Shisheng','H16a'],['Paper heel','Shisheng Li · 40-column block','H16a · permuted strands'],[8,40,8],[28,130,16]):
    s=strips[key];draw_strip(ax,s,color=True)
    ax.set_title(f'{label}   |   {len(s["cross"])} crossings / 40 columns   |   {cnt/per:.2f} per column',loc='left',pad=9)
    ax.text(1,.02,f'{cnt} per {per}-column period',transform=ax.transAxes,ha='right',fontsize=10,color=MUTED)
save(fig,'01_crossing_heels','All dots counted in a 40-column periodic window, including seam interactions. Numbers above colored ends are line labels c = x + 2y.')

# 2: four full boards.
fig,axs=plt.subplots(2,2,figsize=(16,17));fig.subplots_adjust(left=.055,right=.945,top=.88,bottom=.085,wspace=.12,hspace=.18)
title(fig,'One board size, four crossing constructions','72 × 72. Each drawing is independently checked as one closed tour; every red mark is a proper crossing.')
for ax,d,label,formula in zip(axs.flat,[paper,sh,h16,lf],['Paper heel','Shisheng Li block','H16a','Lane-free LF2'],['12n + O(1)','11.5n + O(1)','9n + 5','(22/3)n + 21']):
    board(ax,d);ax.set_title(f'{label}  ·  {d["X"]:,} crossings\n{formula}',loc='left',fontsize=16,pad=9)
save(fig,'02_crossing_boards','Shisheng block is applied to both horizontal sides. LF2 formula shown for this tested residue; a general all-size LF2 theorem is not asserted.')

# 3: four normalized boundary pieces and pairing arcs.
lfmeta=json.loads((ROOT/'w-integrator/tours/LF2_n72.json').read_text())
from periodic import count as periodic_count
fig=plt.figure(figsize=(17,14));gs=fig.add_gridspec(3,2,left=.055,right=.945,top=.875,bottom=.10,height_ratios=[1,1,.72],hspace=.36,wspace=.16)
title(fig,'LF2 anatomy: 11/6 + 5/2 + 2 + 1 = 22/3','Boundary pieces in local coordinates. Arcs show the exact pairing of the straight interior lines.')
for pos,key,label,side in [(0,'bottom','BOTTOM','B'),(1,'top','TOP · rotated on board','B'),(2,'left','LEFT','L'),(3,'right','RIGHT · rotated on board','L')]:
    cell=gs[pos//2,pos%2].subgridspec(2,1,height_ratios=[1.4,1],hspace=.20);ax=fig.add_subplot(cell[0]);ar=fig.add_subplot(cell[1]);tpl=lfmeta[key]
    rate=periodic_count(tpl,'bottom' if side=='B' else 'left')/(len(tpl[0].split()) if side=='B' else len(tpl))
    if side=='B':s=strip(tpl,24);draw_strip(ax,s,mode='cross')
    else:
        a=[r.split() for r in tpl];E=set();w=len(a[0]);h=len(a)
        for y in range(-6,31):
            for x in range(8):
                code=a[h-1-y%h][x] if x<w else '26'
                for k in code:
                    dx,dy=MOVES[int(k)][1],-MOVES[int(k)][0];E.add(tuple(sorted(((y,x),(y+dy,x+dx)))))
        cp,_=crossings(E);cp=[p for p in cp if -.5<=p[0]<23.5 and -.5<=p[1]<7.5]
        s=dict(E=E,cross=cp,turn=[],colored=[],length=24,h=w);draw_strip(ax,s)
    exact=len(s['cross']);MET['strips']['LF2_'+key]={'display_units':24,'display_crossings':exact,'rate':rate}
    assert abs(exact-24*rate)<1e-9
    rate_label={'bottom':'11/6 per column','top':'5/2 per column','left':'2 per row','right':'1 per row'}[key]
    ax.set_title(f'{label}   |   {rate_label}   |   {exact} crossings',loc='left',fontsize=13)
    mp=pairing(tpl,side);P=len(mp)
    def m(c):q,r=divmod(c,P);return q*P+mp[r]
    clean(ar);ar.set_aspect('auto');ar.set_xlim(-4.7,15.7);ar.set_ylim(-1.2,5)
    for c in range(-4,16):ar.plot(c,0,'o',ms=3,color=MUTED);ar.text(c,-.55,str(c),ha='center',fontsize=8,color=MUTED)
    for c in range(-4,16):
        d=m(c)
        if c<d and -4<=d<16:
            col=TEAL if 0<=c<4 else MUTED
            ar.add_patch(Arc(((c+d)/2,0),d-c,min(8,(d-c)*.95),theta1=0,theta2=180,color=col,lw=1.6))
    ar.text(0,1.02,'Line ends c  (arcs are pairings, not knight moves)',transform=ar.transAxes,fontsize=9,color=MUTED)
ax=fig.add_subplot(gs[2,:]);ax.axis('off')
for x,txt,sub in [(.03,'BL: 2 strands','bottom + left'),(.35,'MID: 4 strands','left + right'),(.68,'TR: 2 strands','right + top')]:
    ax.add_patch(Rectangle((x,.51),.27,.38,transform=ax.transAxes,color='#e9f1ef',lw=0));ax.text(x+.135,.73,txt,transform=ax.transAxes,ha='center',fontsize=18,weight='bold',color=TEAL);ax.text(x+.135,.58,sub,transform=ax.transAxes,ha='center',fontsize=11)
ax.text(.5,.30,'No finite cycle in any periodic region.',transform=ax.transAxes,ha='center',fontsize=16)
ax.text(.5,.08,f'Four 6 × 6 corner completions join the paths: one closed tour through {lf["n"]**2:,} cells; {lf["X"]} crossings.',transform=ax.transAxes,ha='center',fontsize=13)
save(fig,'03_lf2_anatomy','Exact periodic-state certificates establish the region counts. The full-board walk establishes one cycle; region counts alone do not guarantee corner completion.')

# 4: three heel stages plus the audited TT16 full tour.
fig=plt.figure(figsize=(17,12));gs=fig.add_gridspec(3,2,left=.055,right=.945,top=.875,bottom=.16,width_ratios=[1.2,1],hspace=.33,wspace=.13)
title(fig,'Turns: 22 → 18 → 16 per heel; TT16 reaches 8n − 14','The same 40 columns in all three strip views. Dark dots are turns; four colored paths show terminal connections.')
for row,key,label in [(0,'paper','Paper crossing-optimal heel'),(1,'T18','T18 heel'),(2,'T16','T16 heel · lane-free')]:
    ax=fig.add_subplot(gs[row,0]);st=strips[key];draw_strip(ax,st,mode='turn',color=True)
    ax.set_title(f'{label}\n{len(st["turn"])} turns / 40 columns = {len(st["turn"])/5:g} per 8',loc='left',fontsize=15)
ax=fig.add_subplot(gs[:,1]);board(ax,tt16,mode='turn');ax.set_title(f'TT16 · 56 × 56\n{tt16["T"]} turns = 8n − 14',loc='left',fontsize=18)
fig.text(.57,.185,'One closed tour. Period-eight corner reuse\nestablishes 8n − 14 for every even n ≥ 48.',fontsize=12,color=TEAL)
fig.text(.055,.10,'The paper’s 9.25n turn bound uses its separate 21-turn heel.\nThe 22-turn heel shown here is Sequence1Opt, the requested crossing-optimal baseline.',fontsize=11,color=MUTED)
save(fig,'04_turn_improvement','Every dark dot is independently recounted. T16 gives 16 turns per eight columns on each horizontal side; each vertical side contributes 2n + O(1).')

# 5: independent check of the improved corner certificate, then diagram.
alpha=[[-1,0,0,-1],[0,1,0,-1],[0,0,0,-1],[-1,-1,-1,-1]]
beta={((0,1),(1,3)):-1,((0,2),(2,3)):-1,((0,3),(1,1)):1,((1,0),(3,1)):-1,((1,1),(3,0)):-1,((1,2),(3,3)):-1,((2,0),(3,2)):-1,((2,1),(3,3)):-1,((2,2),(3,0)):-1}
def L(i,ns,axis):
    if i==0:return 1
    if i in (1,2):return sum(v[axis] in (0,3) for v in ns)-1
    if i==3:return 1-sum(v[axis] in (1,2) for v in ns)
    return 0
cases=0
for x in range(4):
    for y in range(4):
        p=(x,y);possible=[(x+dx,y+dy) for dx,dy in MOVES if x+dx>=0 and y+dy>=0]
        for ns in combinations(possible,2):
            t=int(orient(ns[0],p,ns[1])!=0);r=t-L(x,ns,0)-L(y,ns,1);D=0
            for q in ns:
                e=tuple(sorted((p,q)));D+=beta.get(e,0)*(1 if p==e[0] else -1)
            assert r>=alpha[y][x]+D;cases+=1
assert cases==209 and sum(map(sum,alpha))==-7
MET['certificate']={'local_cases_checked':cases,'sum_alpha':-7,'lower_bound':'8n-28'}
n=small['n'];ts=[sum(x==j for x,y in small['turn']) for j in range(4)]
B=sum(1 for a,b in small['E'] if (a[0]==3 and b[0] in (1,2)) or (b[0]==3 and a[0] in (1,2)))
assert sum(ts)>=2*n and ts[0]==n and ts[1]+ts[2]>=B and ts[3]>=n-B
MET['lemma']={'n':n,'column_turns':ts,'B':B,'strip_turns':sum(ts)}
fig=plt.figure(figsize=(16,12));gs=fig.add_gridspec(2,3,left=.055,right=.945,top=.865,bottom=.10,width_ratios=[.92,1.12,1.02],hspace=.28,wspace=.27)
title(fig,'Turns lower bound: four columns → 2n; four sides → 8n − 28','A real tour illustrates the strip lemma. A finite corner certificate supplies the sharper constant.')
ax=fig.add_subplot(gs[:,0]);clean(ax)
for j in range(4):ax.axvspan(j-.5,j+.5,color=TEAL,alpha=.14 if j in (0,3) else .045)
E=[e for e in small['E'] if min(p[0] for p in e)<4];BE=[e for e in E if {e[0][0],e[1][0]} in ({1,3},{2,3})]
ax.add_collection(LineCollection(E,colors=MUTED,lw=1.0,alpha=.65));ax.add_collection(LineCollection(BE,colors=TEAL,lw=2.2))
points(ax,[p for p in small['turn'] if p[0]<4],s=29,c=INK,zorder=4,edgecolors=BG,linewidths=.5)
for j in range(4):ax.text(j,n+.1,str(j),ha='center',fontsize=13,weight='bold');ax.text(j,-1.15,str(ts[j]),ha='center',fontsize=13,weight='bold')
ax.set_xlim(-.7,5.8);ax.set_ylim(-2,n+1.5);ax.set_title(f'Left strip · n = {n}\n{sum(ts)} turns ≥ {2*n}',loc='left')
ax.text(0,-1.85,'turns per column',fontsize=10,color=MUTED)
ax=fig.add_subplot(gs[0,1:]);ax.axis('off')
proof=[('COLUMN 0','Every cell turns.  T₀ = n.'),('COLUMNS 1 + 2','p(v): edges to column 0 or 3.  t(v) ≥ p(v) − 1.'),('COLUMN 3','q(v): edges to column 1 or 2.  t(v) ≥ 1 − q(v).')]
for yy,(head,txt) in zip([.94,.68,.42],proof):ax.text(0,yy,head,color=TEAL,weight='bold',fontsize=12);ax.text(0,yy-.12,txt,fontsize=13)
ax.text(0,.08,f'Teal edges: B = {B}.   T₁ + T₂ ≥ B;   T₃ ≥ n − B.',fontsize=13)
ax=fig.add_subplot(gs[1,1]);clean(ax);ax.set_xlim(-.6,3.6);ax.set_ylim(3.6,-.6)
for y in range(4):
    for x in range(4):
        ax.add_patch(Rectangle((x-.48,y-.48),.96,.96,color='#e5eeeb' if alpha[y][x]<0 else '#f0f1ed',lw=0));ax.text(x,y,str(alpha[y][x]),ha='center',va='center',fontsize=20,weight='bold',color=TEAL if alpha[y][x] else MUTED)
ax.set_title('Corner certificate α\nSum = −7',loc='left',fontsize=16,pad=14)
ax=fig.add_subplot(gs[1,2]);ax.axis('off');ax.text(0,.93,'The cancellation',color=TEAL,weight='bold',fontsize=16)
ax.text(0,.73,'One side:\nn + B + (n − B) = 2n',fontsize=14,linespacing=1.6)
ax.text(0,.40,'Four sides: 8n.\nCorner slack costs at most\n7 per corner, not 16.',fontsize=13,linespacing=1.7)
ax.text(0,.06,'T ≥ 8n − 4·7\n    = 8n − 28',fontsize=20,weight='bold',color=TEAL)
save(fig,'05_turn_lower_bound','Corner certificate: r(v) ≥ α(v) + D(v); internal edge terms D cancel. All 209 local move-pair cases were independently checked. Valid for n ≥ 8.')

# 6: intervals, with evidence status explicit.
fig,axs=plt.subplots(2,1,figsize=(16,11));fig.subplots_adjust(left=.15,right=.92,top=.84,bottom=.13,hspace=.70)
title(fig,'The remaining intervals: crossings and turns','Leading coefficients of n, with the exact new turn interval inset. Dashed lines mark a finite-size crossing result.')
for ax in axs:
    ax.spines[['top','left','right']].set_visible(False);ax.spines['bottom'].set_color(FAINT);ax.set_yticks([]);ax.tick_params(axis='x',colors=MUTED);ax.set_ylim(-.55,2.9);ax.set_xlim(3.6,12.6)
    ax.set_xticks([4,6,8,9,10,12]);ax.set_xlabel('coefficient of n',loc='right',fontsize=10,color=MUTED)
def interval(ax,y,lo,hi,col,label,dashed=False,leftlab=None,rightlab=None):
    ax.plot([lo,hi],[y,y],color=col,lw=6,solid_capstyle='round',ls=(0,(3,2)) if dashed else '-')
    ax.plot([lo,hi],[y,y],'o',ms=8,mfc=BG if dashed else col,mec=col,mew=1.6)
    ax.text(3.52,y,label,ha='right',va='center',fontsize=11)
    ax.text(lo,y+.24,leftlab or f'{lo:g}',ha='center',fontsize=13,weight='bold',color=col)
    ax.text(hi,y+.24,rightlab or f'{hi:g}',ha='center',fontsize=13,weight='bold',color=col)
axs[0].set_title('CROSSINGS   ·   9 proved; 7⅓ candidate',loc='left',pad=17,fontsize=18)
interval(axs[0],2.25,4,11.5,MUTED,'Prior best')
axs[0].plot(12,2.25,'|',color=MUTED,ms=15);axs[0].text(12,2.68,'12 paper',ha='center',fontsize=10,color=MUTED)
interval(axs[0],1.05,4,9,TEAL,'New proved')
interval(axs[0],-.12,4,22/3,TEAL,'LF2 finite sizes',True,rightlab='22/3 ≈ 7.333')
axs[0].text(.49,-.30,'LF2 verified at n = 72, 74, 76, 78, 96, 120; no all-n theorem yet.',transform=axs[0].transAxes,ha='center',fontsize=10,color=MUTED)
axs[1].set_title('TURNS   ·   the asymptotic coefficient is exactly 8',loc='left',pad=17,fontsize=18)
interval(axs[1],1.95,6,9.25,MUTED,'Paper',leftlab='6*')
axs[1].plot(8,.45,'o',ms=11,color=TEAL)
axs[1].text(3.52,.45,'New proved',ha='right',va='center',fontsize=11)
axs[1].text(8,.77,'8',ha='center',fontsize=15,weight='bold',color=TEAL)
axs[1].text(6.0,-.45,'* Paper lower: (6 − ε)n − Oε(1).',fontsize=10,color=MUTED)
ins=axs[1].inset_axes([.70,.03,.28,.47]);ins.set_facecolor('#edf3f0')
ins.set_xlim(-32,-10);ins.set_ylim(-.8,1.2);ins.set_xticks([]);ins.set_yticks([])
for sp in ins.spines.values():sp.set_visible(False)
ins.plot([-28,-14],[.1,.1],color=TEAL,lw=4);ins.plot([-28,-14],[.1,.1],'o',color=TEAL,ms=6)
ins.text(-28,.35,'−28',ha='center',color=TEAL,weight='bold',fontsize=12)
ins.text(-14,.35,'−14',ha='center',color=TEAL,weight='bold',fontsize=12)
ins.text(-21,.86,'T_min(n) − 8n',ha='center',fontsize=12,weight='bold')
ins.text(-21,-.49,'every even n ≥ 48',ha='center',fontsize=9,color=MUTED)
save(fig,'06_bound_summary','Turns: 8n − 28 ≤ T_min(n) ≤ 8n − 14. The coefficient gap is closed; the exact finite-size optimum remains open. Crossing prior best: Shisheng, both sides.')
(OUT/'counts.json').write_text(json.dumps(MET,indent=2)+'\n')
print(json.dumps(MET,indent=2),flush=True)
