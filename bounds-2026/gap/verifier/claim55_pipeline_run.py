from pathlib import Path
import importlib.util,sys,json,shutil,os
root=Path.cwd();out=root/'gap/verifier/claim55_run'
spec=importlib.util.spec_from_file_location('allpipe',root/'w-integrator/allpipe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# Redirect only the output/menu directory; the computational code is unchanged.
m.HERE=str(out);shutil.copy2(root/'w-integrator/menu_turns.json',out/'menu_turns.json')
paths=[]
for n in [56,58,60,62]:
 d=json.loads((out/f'selftest_TT16/tours/selftest_TT16_n{n}.json').read_text());d.update(A=6,B=6)
 p=out/f'base{n}.json';p.write_text(json.dumps(d));paths.append(str(p))
os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
sys.argv=['allpipe.py','--tag','audit_TT16','--workers','2',*paths]
m.main()
