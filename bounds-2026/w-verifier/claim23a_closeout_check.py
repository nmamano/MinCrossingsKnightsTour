from pathlib import Path
import re,json,hashlib
root=Path.cwd();post=(root/'writeup/turns/post.mdx').read_text();find=(root/'w-verifier/FINDINGS.md').read_text()
report=find.split('# Claim 23A —')[1].split('# Claim 23B —')[0]
parts=re.split(r'\n### (\d+)\.',report)
which={1:[-1],2:[-1],3:[0],4:[-1],5:[-1],6:[0],7:[0],8:[-1],9:[0],10:[0],11:[1,2],12:[0],13:[-1]}
def norm(s):return ' '.join(s.replace('“','"').replace('”','"').split())
checks={}
for i in range(1,len(parts),2):
 n=int(parts[i]);quotes=re.findall(r'^> (.*)$',parts[i+1],re.M)
 if n==13:quotes=quotes[:2]
 checks[n]=all(norm(quotes[j]) in norm(post) for j in which[n])
assert len(checks)==13 and all(checks.values()),checks
old=(root/'w-verifier/claim23a_clean/writeup/turns/post.mdx').read_text()
# All code blocks include the Lean statement and every printed corner/template grid.
assert re.findall(r'```[^\n]*\n(.*?)```',old,re.S)==re.findall(r'```[^\n]*\n(.*?)```',post,re.S)
oldm=json.loads((root/'w-verifier/claim23a_clean/sources.json').read_text());changes=[]
for p,h in oldm.items():
 if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h:changes.append(p)
assert changes==['writeup/turns/post.mdx'],changes
assert post.count('https://github.com/nmamano/knights-tour-bounds')==2
assert 'and no better rate in the tested sizes' not in post
out={'date':'2026-10-02','numbered_replacements':checks,'normalization':'whitespace and curly versus straight quotation marks only','all_code_blocks_unchanged':True,'changed_since_claim23a':changes,'repository_links_present':2,'body_search_claim_removed':True}
(root/'w-verifier/claim23a_closeout_check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
