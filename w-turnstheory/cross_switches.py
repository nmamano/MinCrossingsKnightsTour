"""Find exact crossing-cost 2-edge switches in the F3 near-2-factor."""
import sys
from pathlib import Path
from collections import defaultdict,Counter
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'w-lowerbounds')]
from fold_complete2 import base,MOVES
from kt.core import seg_cross
import networkx as nx

def edge(a,b):return tuple(sorted((a,b)))
def switches(n):
    E,deg=base(n);G=nx.Graph();G.add_edges_from(E)
    comps=list(nx.connected_components(G));ci={v:i for i,c in enumerate(comps) for v in c}
    closed={i for i,c in enumerate(comps) if all(deg[v]==2 for v in c)}
    near=defaultdict(set)
    for e in E:
        for p in e:near[p].add(e)
    def crossset(e):
        possible=set()
        for p in e:
            for dx in range(-4,5):
                for dy in range(-4,5):possible.update(near.get((p[0]+dx,p[1]+dy),()))
        return {f for f in possible if seg_cross(*e,*f)}
    cache={}
    def cs(e):
        if e not in cache:cache[e]=crossset(e)
        return cache[e]
    hist=Counter();candidates={};zero_comp=nx.Graph();zero_comp.add_nodes_from(closed)
    for e in sorted(E):
        a,b=e
        for dx,dy in MOVES:
            c=(a[0]+dx,a[1]+dy)
            for f in near.get(c,()):
                if e>=f or len(set(e+f))<4:continue
                d=f[0] if f[1]==c else f[1]
                if (d[0]-b[0],d[1]-b[1]) not in MOVES:continue
                g,h=edge(a,c),edge(b,d)
                if g in E or h in E:continue
                i,j=ci[a],ci[c]
                if i==j or i not in closed or j not in closed:continue
                old=len(cs(e))+len(cs(f))-int(f in cs(e))
                new=len(cs(g)-{e,f})+len(cs(h)-{e,f})+int(seg_cross(*g,*h))
                delta=new-old
                hist[delta]+=1
                if delta<=0:
                    zero_comp.add_edge(i,j);candidates[e,f]=(g,h,delta)
    print('n',n,'closed cycles',len(closed),'all components',len(comps),'switch histogram',sorted(hist.items()),flush=True)
    print('zero-cost cycle component sizes',sorted([len(c) for c in nx.connected_components(zero_comp)],reverse=True)[:15],flush=True)
    for (e,f),(g,h,d) in list(candidates.items())[:3]:print('example',e,f,'->',g,h,'delta',d,flush=True)
    return candidates
if __name__=='__main__':
    switches(int(sys.argv[1]) if len(sys.argv)>1 else 48)
