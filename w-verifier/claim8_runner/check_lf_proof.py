#!/usr/bin/env python3
"""LF4 finite certificate for PROOFS.md section 5. No solver or third-party imports.
Uses the exact graph and geometry routines in check_upper_proofs.py.
"""
import json
from fractions import Fraction
from pathlib import Path
from check_upper_proofs import graph,validate,slab,power,band_cost,crossings,template

HERE=Path(__file__).resolve().parent

def main():
    files=sorted((HERE/'lf-corners').glob('LF4_res*.json'))
    assert len(files)==24, 'Need one certificate for each even residue modulo 48'
    data=[json.loads(f.read_text()) for f in files]
    assert sorted(d['n0'] for d in data)==list(range(96,144,2))
    first=data[0]
    assert {k:template(first[k])[1:] for k in ('bottom','top','left','right')}=={
        'bottom':(6,4),'top':(16,4),'left':(2,4),'right':(2,4)}
    assert len(set(first['left']))==len(set(first['right']))==1
    costs={name:band_cost(first[name],'B' if name in ('bottom','top') else 'L')
           for name in ('bottom','top','left','right')}
    assert {k:(v[0],v[2]) for k,v in costs.items()}=={
        'bottom':(6,11),'top':(16,37),'left':(4,8),'right':(4,4)}
    assert sum(48//v[0]*v[2] for v in costs.values())==343
    report={'date':'2026-10-02','period':48,'slope':'343/48','band_costs':costs,
            'residues':[],'block_matchings':[]}
    common=[]
    for d in data:
        n=d['n0']; assert d['Z']==6 and len(d['zones'])==144
        assert d['phases']==[1,1,0,0]
        assert all(d[k]==first[k] for k in ('bottom','top','left','right'))
        g=graph(d,n); validate(g); X=crossings(g)
        h=graph(d,n+48); validate(h); X2=crossings(h); assert X2-X==343
        for j,width in enumerate((12,8,16)):
            a=j*n+36
            assert 24<a-j*n and a+width<(j+1)*n-24
            names,M=slab(g,n,a,width)
            assert len(names)==(16,4,8)[j]
            assert sum(s==0 and t==1 for (s,i),(t,k) in M.items())==(2,4,2)[j]
            # Complete port matching, including all same-side return paths.
            assert power(M,2)==M
            assert power(M,1+48//width)==M
            assert slab(h,n+48,a+j*48,width)==(names,M)
            assert slab(h,n+48,a+j*48,width+48)==(names,M)
            if n==96:
                common.append((names,M))
                report['block_matchings'].append({'region':j,'width':width,'ports':names,
                    'pairs':sorted([list(u),list(v)] for u,v in M.items() if u<v)})
            else: assert (names,M)==common[j]
        B=48*X-343*n
        report['residues'].append({'r':n%48,'n0':n,'X0':X,'b':str(Fraction(B,48)),
                                   '48b':B,'X_at_n0_plus_48':X2})
        print(f'residue {n%48:2}: n0={n}, X0={X}, b={Fraction(B,48)}; PASS',flush=True)
    (HERE/'lf_proof_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 24 residue bases, 24 enlarged tours, 72 local insertion checks; delta X=343.')

if __name__=='__main__': main()
