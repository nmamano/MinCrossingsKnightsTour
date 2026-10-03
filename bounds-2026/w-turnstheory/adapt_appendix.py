"""Format the audited proofs for the crossings post; no mathematical edits."""
from pathlib import Path
import re, hashlib
ROOT=Path(__file__).resolve().parents[1]
post=ROOT/'writeup/crossings/post.mdx'
original=post.read_text()
assert '## Appendix: full proofs' not in original
# Preserve existing code spans. Format mathematical tokens, then join adjacent
# code spans into a single expression. The underlying text is unchanged.
variables=set('n n0 k h R r j x y c s p q o A M Li Ri i B D L E G H U V X F g t m_t m_+ m_- omega sigma b b_sigma X_sigma B_sigma Q_R A_R gamma_R phi_H rho ab a b'.split())
variables-={'a','b','i'}  # Ordinary words; their mathematical uses are handled below.
def inline(text):
    parts=re.split(r'(`[^`]*`)',text)
    for i in range(0,len(parts),2):
        def token(m):
            raw=m.group();core=raw.rstrip('.,;:')
            tail=raw[len(core):]
            if not core:return raw
            math=(bool(re.search(r'[0-9_<>=^{}]',core)) or core in variables
                  or core.startswith(('chi(','sign(','sum_','integral_','binomial(','deg_','max(','min(','floor(','bad(','p(')))
            # Do not style Markdown markers or prose file names.
            if math:return '`'+core+'`'+tail
            return raw
        parts[i]=re.sub(r'\S+',token,parts[i])
    text=''.join(parts)
    # This merge is restricted to adjacent code spans, not prose between them.
    text=re.sub(r'`[ \t]+`',' ',text)
    return text

foldchecks={1:'check_fold_proof.py',2:'check_fold_proof.py',3:'check_fold_proof.py',4:'check_fold_proof.py'}
lowerchecks={1:'check_knight_tiles.py',2:'check_knight_tiles.py;check_square_defects.py',3:'check_corner_box.py',4:'check_col0_squares.py',5:'check_lower_stability.py',6:'check_col0_squares.py;check_lower_stability.py'}
def adapt(file,label,checks):
    s=(ROOT/file).read_text()
    # The figure paragraphs are drawing instructions, not proof steps.
    s=re.sub(r'\n\*\*Figure \d+\.\*\*.*?(?=\n\n|\Z)','',s,flags=re.S)
    s=re.sub(r'^# .*\n','',s,count=1)
    s=re.sub(r'^Status:.*\n','',s,flags=re.M)
    s=s.replace('2026-10-02. ','',1)
    # Names of sections are local to their appendix.
    s=re.sub(r'Section (\d+)',lambda m:f'Section {label}.{m[1]}',s)
    chunks=re.split(r'\n\s*\n',s.strip());result=[];current=None
    for chunk in chunks:
        if chunk.startswith('## '):
            if current in checks:
                result.append('**Finite checks for this section:**\n\n```sh\n'+ '\n'.join('python3 w-turnstheory/'+c for c in checks[current].split(';'))+'\n```')
            m=re.match(r'## (\d+)\. (.*)',chunk);assert m
            current=int(m[1]);result.append('### '+label+'.'+m[1]+'. '+inline(m[2]));continue
        if chunk.startswith('```'):
            result.append(chunk);continue
        if chunk.startswith('    '):
            # Each displayed mathematical line becomes a code-span paragraph.
            result.append('\n\n'.join('`'+line.strip()+'`' for line in chunk.splitlines()));continue
        if chunk.startswith('|'):
            rows=[]
            for row in chunk.splitlines():
                if re.match(r'^\|[ :|\-]+$',row):rows.append(row);continue
                rows.append('| '+' | '.join(inline(c.strip()) for c in row.strip('|').split('|'))+' |')
            result.append('\n'.join(rows));continue
        # Prose line wrapping is irrelevant to the proof and MDX output.
        result.append(inline(' '.join(chunk.splitlines())))
    if current in checks:
        result.append('**Finite checks for this section:**\n\n```sh\n'+'\n'.join('python3 w-turnstheory/'+c for c in checks[current].split(';'))+'\n```')
    return '\n\n'.join(result)
upper=adapt('w-turnstheory/PROOF_fold.md','A',foldchecks)
lower=adapt('w-turnstheory/PROOF_crossings_lower.md','B',lowerchecks)
# Make the immediate 4n-2 consequence explicit; it is already Equation (1)'s
# preceding area argument in the audited source, not an additional assumption.
lower=lower.replace('Thus `E>=0` and `G<=2E`.', 'Thus `E>=0` and `G<=2E`. In particular, `X >= 4n - 2`. This area argument also applies to a spanning 2-factor; it does not use connectivity.')
appendix='''## Appendix: full proofs

The two proofs below include their finite certificates and the commands to check them. Run every command from the research project root. The geometric arguments explain why the finite checks cover every board size; testing a list of tours alone would not suffice.

<details id="proof-fold">
<summary>A. Full proof: tours with at most 19n/3 + 142 crossings</summary>

'''+upper+'''

</details>

<details id="proof-crossings-lower">
<summary>B. Full proof: every tour has at least 14n/3 - 407 crossings, including the 4n - 2 tile bound</summary>

'''+lower+'''

</details>
'''
a=original.index('## Details\n');b=original.index('## Open questions\n',a)
details='''## Details

The [full-proof appendix](#appendix-full-proofs) contains both arguments, including every finite certificate and its check command:

- [A. The fold construction](#proof-fold): exact placement, insertion for every even `n >= 96`, complete path matchings, and the count `X <= 19n/3 + 142`.
- [B. The lower bound](#proof-crossings-lower): the tile bound `4n - 2`, the corner charge, the exact endpoint test, strip stability, and `X >= 14n/3 - 407` for every closed tour with even `n >= 32`.

The appendices are collapsed by default. Open the relevant proof to read its definitions, finite checks, and all-size argument.

'''
new=original[:a]+details+original[b:].rstrip()+'\n\n'+appendix
assert post.read_text()==original,'Post changed while formatting; do not overwrite.'
post.write_text(new)
print('Added full appendices; preserved the text before Details and the Open questions section.')
print('Original SHA256:',hashlib.sha256(original.encode()).hexdigest())
