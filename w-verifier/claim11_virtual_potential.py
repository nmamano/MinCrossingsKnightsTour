"""Cross-check the C++ report's alternate virtual-source ordinary potential."""
from pathlib import Path
source=Path('w-verifier/claim11_forest.py').read_text()
old='d=potentials(N,arcs,[4*w-1 for u,v,w in arcs],0)'
assert source.count(old)==1
source=source.replace(old,'d=potentials(N,arcs,[4*w-1 for u,v,w in arcs])')
source=source.replace('w-verifier/claim11_forest.json','w-verifier/claim11_virtual_potential.json')
exec(compile(source,'claim11_forest.py (virtual ordinary source)','exec'))
