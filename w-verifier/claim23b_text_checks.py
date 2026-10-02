from pathlib import Path
import re,json,hashlib
from fractions import Fraction
root=Path.cwd();p=root/'w-verifier/claim23b_clean/writeup/crossings/post.mdx';text=p.read_text()
part=text.split('### B.3.')[1].split('The **up test**')[0]
F={}
for x,y,u,v,c in re.findall(r'\| `\((-?\d+),(-?\d+)\)--\((-?\d+),(-?\d+)\)` \| `([+-]?\d+)` \|',part):
 F[tuple(sorted(((int(x),int(y)),(int(u),int(v)))))]=int(c)
old=json.loads((root/'w-verifier/claim18.json').read_text())['corner'][0]['left_terms']
assert F=={tuple(sorted(map(tuple,e))):c for e,c in old}
report=json.loads((root/'w-verifier/claim23b_clean/w-turnstheory/fold_proof_checks.json').read_text())
assert max(Fraction(r['b']) for r in report['residues'])==142
assert len(next(r for r in report['residues'] if r['n0']==100)['step12_cycle_sizes'])==3
assert 4*2*10+4*2*9==152 and Fraction(152,24)==Fraction(19,3)
assert 1104-2+29==1131 and 120+44+2*1131==2426
assert Fraction(2426,6)+2==Fraction(1219,3)<407
assert Fraction(1131+132,3)==421
out={'appendix_F_coefficients_match':True,'fold_b_max':142,'exact_lower_constant':'1219/3','stated_lower_constant':407,'Lean_constant_with_C1131':421}
(root/'w-verifier/claim23b_text_checks.json').write_text(json.dumps(out,indent=2))
print(out)
