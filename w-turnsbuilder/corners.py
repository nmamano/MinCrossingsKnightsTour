"""Corner search through Integrator assemble(), with checked tour hints."""
import json
import re
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'w-integrator'))
import assemble as asm
from kt.core import validate,num_turns,num_crossings,MI,MJ
from kt.board import build_general,fixed_paths,to_grid
from strands import pairing,region_check

OUT=Path(__file__).parent
TDIR=OUT/'corner_tours'
TDIR.mkdir(exist_ok=True)
MENU={r['name']:r for r in json.loads((ROOT/'w-integrator/menu_turns.json').read_text())}
COMBOS=[]
for line in (ROOT/'w-integrator/runs/combos2_turns.txt').read_text().splitlines():
    if line.startswith('slope 8.000 '):
        COMBOS.append(tuple(re.search(r'B=(\S+) T=(\S+) L=(\S+) R=(\S+)',line).groups()))
UNIQUE={}
for names in COMBOS:
    key=tuple(tuple(MENU[name]['tpl']) for name in names)
    UNIQUE.setdefault(key,[]).append(names)
GROUPS=list(UNIQUE.items())

def graph(g):
    n=len(g)
    return {(x,n-1-r):{(x+MJ[int(k)],n-1-r-MI[int(k)]) for k in code}
            for r,row in enumerate(g) for x,code in enumerate(row)}

def initial():
    for n in (56,58,60,62):
        source=ROOT/f'w-integrator/tours/certificates/TT16_n{n}.json'
        r=json.loads(source.read_text());g=r['tour']
        assert validate(g) and asm.walk_check(g)
        assert num_turns(g)==r['turns']==8*n-14
        target=TDIR/f'baseline_n{n}.json'
        if not target.exists():
            r.update(source=str(source.relative_to(ROOT)),validated=True,date='2026-10-02')
            target.write_text(json.dumps(r)+'\n')

def phase_list(n,group,Z=8):
    (B,T,L,R),_=GROUPS[group]
    # Both left templates have constant rows. Reduce only their row period.
    if all(row==L[0] for row in L):L=L[:1]
    if all(row==R[0] for row in R):R=R[:1]
    return [tuple(p) for p,_ in asm.phase_candidates(n,list(B),list(L),list(T),list(R),Zmin=Z)]

_complete=asm.complete
SEEDS=[]
def with_hint(n,nb,free,**kw):
    for h in SEEDS:
        if all(c in free or h[c]==vs for c,vs in nb.items()):
            kw['hint']=h;break
    return _complete(n,nb,free,**kw)
asm.complete=with_hint

def run(n,group,Z,ph,seconds=20):
    global SEEDS
    seedrows=[json.loads(f.read_text()) for f in TDIR.glob(f'*_n{n}.json')]
    seedrows.sort(key=lambda r:(r['turns'],r['crossings']))
    SEEDS=[graph(r['tour']) for r in seedrows]
    (B,T,L,R),names=GROUPS[group]
    start=time.monotonic()
    g,info=asm.assemble(n,list(B),list(L),0,[Z],seconds,1,1000,
        top=list(T),right=list(R),phases=ph,objective='turns',log=lambda s:None)
    r=dict(date='2026-10-02',n=n,residue=n%8,group=group,Z=Z,phases=ph,
           seconds=round(time.monotonic()-start,2),info=info,names=names)
    if g is not None:
        assert validate(g) and asm.walk_check(g)
        Tn,X=num_turns(g),num_crossings(g)
        r.update(T=Tn,X=X,delta=Tn-8*n,validated=True)
        tag=f'g{group}_Z{Z}_p'+''.join(map(str,ph))+f'_n{n}.json'
        target=TDIR/tag
        data=dict(n=n,bottom=B,top=T,left=L,right=R,phases=ph,turns=Tn,crossings=X,
            tour=g,info=info,date='2026-10-02',validated=True)
        target.write_text(json.dumps(data)+'\n')
        r['file']=str(target.relative_to(ROOT))
    with (OUT/'corner_results.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
    print(json.dumps(r),flush=True)
    render()
    return r

def render():
    results=[json.loads(l) for l in (OUT/'corner_results.jsonl').read_text().splitlines()] if (OUT/'corner_results.jsonl').exists() else []
    out=['# Corner turn search','', 'Date: 2026-10-02. One solver worker; all solves ran in sequence.',
         'Target: minimize T - 8n. A more negative value is better. Each listed best tour passes kt.core.validate and the independent Integrator walk.',
         'The search calls w-integrator/assemble.py through its assemble() function, with turn_weight=1000, objective="turns", and one Z value per call.',
         'The turns objective uses 1000 per corner turn and 1 per crossing. Existing compatible full tours supply edge hints. Shared code is not changed.', '',
         '## Best verified tours','', '| n mod 8 | n | T | T - 8n | X | tour file |', '| ---: | ---: | ---: | ---: | ---: | --- |']
    for n in (56,58,60,62):
        options=[]
        for f in TDIR.glob(f'*_n{n}.json'):
            r=json.loads(f.read_text());options.append((r['turns'],r['crossings'],f))
        if options:
            t,x,f=min(options)
            out.append(f'| {n%8} | {n} | {t} | {t-8*n} | {x} | `{f.relative_to(ROOT)}` |')
    out+=['','## The twelve names give two distinct template sets','']
    for i,(templates,names) in enumerate(GROUPS):
        out.append(f'Group {i}: '+ '; '.join('/'.join(ns) for ns in names)+'.')
    out+=['','All equivalences above use exact row-list equality. The left and right templates have constant rows, so their vertical phases give the same graph. Bottom and top phases are tested separately.',
          '', '## Runs','', '| n | group | Z | phases | T - 8n | status | seconds |', '| ---: | ---: | ---: | --- | ---: | --- | ---: |']
    for r in results:
        info=r['info'];status=info['status'] if isinstance(info,dict) else info
        out.append(f"| {r['n']} | {r['group']} | {r['Z']} | {r['phases']} | {r.get('delta','—')} | {status} | {r['seconds']} |")
    out+=['','No optimum across all corners or phases is claimed. Time-limited failures do not rule out a better tour. Results for four board sizes alone do not prove a formula for all larger sizes.','']
    (OUT/'CORNERS.md').write_text('\n'.join(out))

def local_pass(n,Z,seconds=10):
    """Keep three corners fixed; optimize the fourth while preserving one cycle."""
    options=[json.loads(f.read_text()) for f in TDIR.glob(f'*_n{n}.json')]
    r=min(options,key=lambda r:(r['turns'],r['crossings']))
    h=graph(r['tour'])
    for corner,(x0,y0) in enumerate(((0,0),(n-Z,0),(0,n-Z),(n-Z,n-Z))):
        free={(x,y) for x in range(x0,x0+Z) for y in range(y0,y0+Z)}
        start=time.monotonic()
        full,info=_complete(n,h,free,time_limit=seconds,workers=1,hint=h,
                            turn_weight=1000,crossing_weight=1)
        entry=dict(date='2026-10-02',n=n,residue=n%8,group='local',corner=corner,Z=Z,
                   phases=r.get('phases'),info=info,seconds=round(time.monotonic()-start,2))
        if full:
            g=to_grid(n,full)
            assert validate(g) and asm.walk_check(g)
            t,x=num_turns(g),num_crossings(g)
            entry.update(T=t,X=x,delta=t-8*n,validated=True)
            target=TDIR/f'local_Z{Z}_c{corner}_n{n}.json'
            data=dict(r,tour=g,turns=t,crossings=x,info=info,validated=True,date='2026-10-02')
            target.write_text(json.dumps(data)+'\n')
            entry['file']=str(target.relative_to(ROOT))
            if (t,x)<=(r['turns'],r['crossings']):r=data;h=full
        with (OUT/'corner_results.jsonl').open('a') as f:f.write(json.dumps(entry)+'\n')
        print(json.dumps(entry),flush=True);render()

if __name__=='__main__':
    initial();render()
    mode=sys.argv[1]
    if mode=='baseline':
        for Z in (8,10,12):
            for n in (56,58,60,62):run(n,0,Z,(0,1,0,0),20)
    elif mode=='phases':
        for group in range(len(GROUPS)):
            for n in (56,58,60,62):
                phases=phase_list(n,group)
                print('phases',n,group,phases,flush=True)
                for ph in phases:
                    if group==0 and ph==(0,1,0,0):continue
                    run(n,group,8,ph,15)
    elif mode=='local':
        for Z in (8,10,12):
            for n in (56,58,60,62):local_pass(n,Z,10)
