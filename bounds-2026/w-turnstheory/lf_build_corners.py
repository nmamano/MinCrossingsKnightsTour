"""Build residue certificates by reusing compatible corner squares; no solver."""
import itertools,json
from pathlib import Path
from check_upper_proofs import ROOT,graph,validate
from lf_extract import extract

OUT=Path(__file__).with_name('lf-corners')

def main():
    sources=sorted((ROOT/'w-integrator/tours').glob('LF4_n*.json'))
    sources+=sorted((Path(__file__).parent/'lf-built').glob('LF4_n*.json'))
    pool=[(str(p.relative_to(ROOT)),extract(p)) for p in sources]
    corners=('BL','BR','TL','TR')
    missing=[]
    for n in range(96,144,2):
        out=OUT/f'LF4_res{n%48:02d}.json'
        if out.exists(): continue
        d=dict(pool[0][1]); d['n0']=n; d['phases']=[1,1,0,0]
        options=[]
        for c in corners:
            opts=[]; seen=set()
            for src,base in pool:
                z={k:v for k,v in base['zones'].items() if k.startswith(c+':')}
                signature=json.dumps(z,sort_keys=True)
                if signature in seen: continue
                seen.add(signature)
                dd=dict(d); dd['zones']=dict(d['zones']); dd['zones'].update(z)
                g=graph(dd,n); a,b={'BL':(0,0),'BR':(n-6,0),'TL':(0,n-6),'TR':(n-6,n-6)}[c]
                good=all(v in g and u in g[v] for x in range(a,a+6) for y in range(b,b+6)
                         for u in [(x,y)] for v in g[u])
                if good: opts.append((src,z))
            options.append(opts)
        found=False
        for choices in itertools.product(*options):
            zones={k:v for src,z in choices for k,v in z.items()}; dd=dict(d); dd['zones']=zones
            try: validate(graph(dd,n))
            except AssertionError: continue
            dd['sources']={c:src for c,(src,z) in zip(corners,choices)}
            dd['period']=48; out.write_text(json.dumps(dd,indent=2)+'\n'); found=True; break
        print(n,[len(o) for o in options], 'OK' if found else 'MISSING',flush=True)
        if not found: missing.append(n)
    print('Missing:',missing)

if __name__=='__main__': main()
