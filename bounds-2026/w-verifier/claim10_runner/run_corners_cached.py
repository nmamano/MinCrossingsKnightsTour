"""Run both original enumerations; cache their additive edge contributions only."""
from pathlib import Path
from functools import lru_cache
import importlib.util
source=Path('corner_charge.py').read_text()
prefix,rest=source.split('K = [(0, y)',1)
ns={};exec(compile(prefix,'corner_charge.py','exec'),ns)
original=ns['Q']
@lru_cache(None)
def baseline(R):return original([],R)
@lru_cache(None)
def edge_value(e,R):return original([e],R)-baseline(R)
def cached(E,R):return baseline(R)+sum(edge_value(e,R) for e in E)
ns['Q']=cached
exec(compile('K = [(0, y)'+rest,'corner_charge.py','exec'),ns)
print('Primary enumeration complete.',flush=True)
spec=importlib.util.spec_from_file_location('corner2','corner_charge2.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
orig2=m.path_value
tables={}
def cached2(E,segs):
 segs=tuple(segs)
 if segs not in tables:tables[segs]=(orig2([],segs),{})
 base,table=tables[segs]
 for e in E:
  if e not in table:table[e]=orig2([e],segs)-base
 return base+sum(table[e] for e in E)
m.path_value=cached2
m.main()
print('Independent Fraction enumeration complete.',flush=True)
