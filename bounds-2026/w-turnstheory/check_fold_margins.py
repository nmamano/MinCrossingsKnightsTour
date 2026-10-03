#!/usr/bin/env python3
"""Exact affine inequalities for component/cut margins, for every integer k>=0.

Ported from the independent Claim 23B audit. Each pair (a,b) represents
a+b*k; nonnegative intercept and slope prove the inequality for all k>=0.
Inputs are the twelve released base files. No solver or verifier file is used.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
SHIFT=((0,6),(6,24),(18,0),(24,18),(0,0),(0,24),(24,0),(24,24),(0,12),(12,0),(12,24),(24,12),(12,12))

def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def sub(a,b):return add(a,neg(b))
def twice(a):return 2*a[0],2*a[1]
def nonnegative(a):return a[0]>=0 and a[1]>=0
def nonpositive(a):return a[0]<=0 and a[1]<=0

def side_of_mid(x,h):
 delta=sub(x,h)
 if delta[0]<0 and delta[1]<=0:return True
 assert nonnegative(delta),('quadrant changes',x,h)
 return False

def choose(a,b,want_max):
 d=sub(a,b)
 if nonnegative(d):return a if want_max else b
 assert nonpositive(d),('label branch changes',a,b)
 return b if want_max else a

def main():
 records=[]
 for n0 in range(96,120,2):
  d=json.loads((ROOT/f'w-integrator/corners/FOLD24_base_n{n0}.json').read_text())
  n=(n0,24);h=(n0//2,12);tested=0
  assert len(d['components'])==len(SHIFT)
  assert sum(len(co['cells']) for co in d['components'])==1008
  for co,(sx,sy) in zip(d['components'],SHIFT):
   for key in co['cells']:
    qx,qy=map(int,key.split(','));px=(co['offset'][0]+qx,sx);py=(co['offset'][1]+qy,sy)
    assert all(nonnegative(t) for t in (px,py,sub(sub(n,(1,0)),px),sub(sub(n,(1,0)),py)))
    for r in range(4):
     x,y=px,py
     for _ in range((-r)%4):x,y=sub(sub(n,(1,0)),y),x
     left=side_of_mid(x,h)
     bottom=side_of_mid(y,h)
     for kind in ('corner','side'):
      if not left or kind=='corner' and not bottom:continue
      if kind=='corner':
       label=choose(sub(twice(x),y),sub(twice(y),x),True);lo=(24,0);hi=(30,12)
      else:
       label=sub(twice(choose(y,sub(n,y),False)),x);lo=(n0//2+16,12);hi=(n0//2+22,24)
      if label[0]<lo[0]:assert label[1]<=lo[1]
      else:assert nonnegative(sub(label,hi)),('component enters growing block',n0,co['offset'],key,kind,r,label,lo,hi)
      tested+=1
  records.append({'n0':n0,'component_cells':1008,'active_block_margin_inequalities':tested,'valid_for_all_k_ge_0':True})
 Path(__file__).with_name('fold_margin_checks.json').write_text(json.dumps(records,indent=1))
 print('PASS all 12 bases: every component cell remains on the board and outside all growing blocks for every k>=0.')
 print('Exact affine margin inequalities:',sum(x['active_block_margin_inequalities'] for x in records))
if __name__=='__main__':main()
