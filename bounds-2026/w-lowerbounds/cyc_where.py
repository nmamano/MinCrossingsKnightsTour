import sys, ast
import networkx as nx
from collections import Counter
from fold_complete2 import base
n=int(sys.argv[1]); ts=ast.literal_eval(sys.argv[2]); ms=ast.literal_eval(sys.argv[3])
E,deg=base(n,ts=ts,ms=ms)
G=nx.Graph(); G.add_edges_from(E)
lab=Counter()
for c in nx.connected_components(G):
    closed=all(deg[p]==2 for p in c)
    # which edge cells does it touch
    sides=set()
    for (x,y) in c:
        if x==0: sides.add('L'+('lo' if y<n//2 else 'hi'))
        if x==n-1: sides.add('R'+('lo' if y<n//2 else 'hi'))
        if y==0: sides.add('B'+('l' if x<n//2 else 'r'))
        if y==n-1: sides.add('T'+('l' if x<n//2 else 'r'))
    lab[(closed,tuple(sorted(sides)), len(c)>4*n)]+=1
for k,v in sorted(lab.items(), key=lambda t:-t[1]): print(v,k)
