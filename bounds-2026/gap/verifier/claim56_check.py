"""Claim 56 Part 1: independent exact tour checker, no worker imports (2026-10-04)."""
from pathlib import Path
import hashlib,json,argparse
ROOT=Path('gap/searcher/turns/tours');OUT=Path('gap/verifier/claim56_run')
# Row increases downwards; codes are the eight knight moves in clockwise order.
DR=(-2,-1,1,2,2,1,-1,-2);DC=(1,2,2,1,-1,-2,-2,-1)
def inspect(rows,n):
 assert isinstance(n,int) and n>0 and len(rows)==n
 assert all(isinstance(row,list) and len(row)==n for row in rows)
 adj=[];bycode=0;bydet=0
 for r,row in enumerate(rows):
  for c,s in enumerate(row):
   assert isinstance(s,str) and len(s)==2 and s[0]!=s[1] and all(k in '01234567' for k in s)
   ns=[]
   for k in map(int,s):
    rr,cc=r+DR[k],c+DC[k]
    assert 0<=rr<n and 0<=cc<n
    assert sorted((abs(rr-r),abs(cc-c)))==[1,2]
    ns.append(rr*n+cc)
   adj.append(ns)
   u,v=map(int,s)
   bycode+=(u-v)%8!=4
   a,b=divmod(ns[0],n);x,y=divmod(ns[1],n)
   bydet+=(a-r)*(y-c)!=(b-c)*(x-r)
 assert bycode==bydet
 for u,vs in enumerate(adj):
  assert len(set(vs))==2
  assert all(u in adj[v] for v in vs)
 seen=set();cycles=[]
 for start in range(n*n):
  if start in seen:continue
  u=start;prev=-1;size=0
  while u not in seen:
   seen.add(u);size+=1
   v=adj[u][0] if adj[u][0]!=prev else adj[u][1]
   prev,u=u,v
  assert u==start
  cycles.append(size)
 assert sum(cycles)==n*n
 return dict(n=n,vertices=n*n,cycle_lengths=cycles,turns=bydet,T_minus_8n=bydet-8*n)

def extend_independent(rows,n):
 old=len(rows);split=old//2;extra=n-old
 assert extra>=0 and extra%8==0
 # Source-coordinate list for the lower part, repeated middle window, and upper part.
 coords=list(range(split))+[split+j%8 for j in range(extra)]+list(range(split,old))
 assert len(coords)==n
 return [[rows[old-1-coords[n-1-r]][coords[c]] for c in range(n)] for r in range(n)]

def main():
 global OUT
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=OUT);OUT=ap.parse_args().out
 OUT.mkdir(exist_ok=False)
 files=sorted(ROOT.glob('res[26]/*.json'));assert files
 report=dict(date='2026-10-04',supplied=[],generated=[],warning_probe={})
 for f in files:
  raw=f.read_bytes();d=json.loads(raw);n=d['n'];got=inspect(d['tour'],n)
  assert got['cycle_lengths']==[n*n]
  assert got['turns']==d['turns']
  assert n%8 in [2,6] and got['T_minus_8n']=={2:-17,6:-16}[n%8]
  got.update(file=str(f),sha256=hashlib.sha256(raw).hexdigest())
  report['supplied'].append(got)
  dest=OUT/f.parent.name;dest.mkdir(exist_ok=True);(dest/f.name).write_bytes(raw)
  print('SUPPLIED',n,got['turns'],got['T_minus_8n'],'one cycle',flush=True)
 for base,stop in [(62,206),(66,210)]:
  d=json.loads((OUT/f'res{base%8}'/f'n{base}.json').read_text())
  for n in range(base,stop+1,8):
   g=extend_independent(d['tour'],n);got=inspect(g,n)
   assert got['cycle_lengths']==[n*n] and got['T_minus_8n']=={62:-16,66:-17}[base]
   f=OUT/f'res{base%8}'/f'n{n}.json'
   if f.exists():assert g==json.loads(f.read_text())['tour']
   got['base']=base;report['generated'].append(got)
  print('GENERATED',base,'..',stop,'step 8: all 19 PASS',flush=True)
 d=json.loads((OUT/'res2/n58.json').read_text());probe=inspect(extend_independent(d['tour'],66),66)
 assert len(probe['cycle_lengths'])>1
 report['warning_probe']=probe
 print('n58 -> n66 extension has cycles',probe['cycle_lengths'],'(not used as witness)',flush=True)
 (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS:',len(report['supplied']),'supplied files and',len(report['generated']),'finite generated cases')

if __name__=='__main__':main()
