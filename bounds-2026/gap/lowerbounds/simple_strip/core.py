"""Recurrent core of the no-cycle row graph (states on cycles + states between cycles = nontrivial SCC closure)."""
import sys, pickle, numpy as np, networkx as nx
from collections import Counter
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
Gr = nx.DiGraph(); Gr.add_edges_from((u, v) for u, v, W, m in rows)
sccs = [c for c in nx.strongly_connected_components(Gr) if len(c) > 1 or Gr.has_edge(next(iter(c)), next(iter(c)))]
print('nontrivial SCCs', len(sccs), sorted(map(len, sccs), reverse=True)[:10])
cyc = set().union(*sccs)
fwd = set(cyc); 
for c in cyc: fwd |= nx.descendants(Gr, c) if False else set()
# states reachable from a cycle AND reaching a cycle
R1 = set(); 
for s in cyc: pass
desc = set(cyc); stack = list(cyc)
while stack:
    x = stack.pop()
    for y in Gr.successors(x):
        if y not in desc: desc.add(y); stack.append(y)
anc = set(cyc); stack = list(cyc)
while stack:
    x = stack.pop()
    for y in Gr.predecessors(x):
        if y not in anc: anc.add(y); stack.append(y)
core = desc & anc
print('core states', len(core), 'in cycles', len(cyc), 'total', len(bstates))
pickle.dump(core, open('gap/lowerbounds/simple_strip/core.pkl', 'wb'))
