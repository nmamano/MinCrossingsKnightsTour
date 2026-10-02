"""Run supplied figure code in isolation and export its source data for independent checks."""
from pathlib import Path
import json
root=Path.cwd(); out=root/'w-verifier/claim21_figures';out.mkdir(exist_ok=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.figure
orig=matplotlib.figure.Figure.savefig
labels={}
def save(self,name,*a,**kw):
 labels[Path(name).name]=[t.get_text() for t in self.findobj() if isinstance(t,matplotlib.text.Text) and t.get_text()]
 return orig(self,name,*a,**kw)
matplotlib.figure.Figure.savefig=save
mods={}
for file in ('cross_figs.py','lower_figs.py','heel_fig.py'):
 path=root/'writeup/crossings/figures'/file
 s=path.read_text().replace("OUT = Path(__file__).resolve().parent",'OUT = Path('+repr(str(out))+')')
 ns={'__file__':str(path),'__name__':'__main__'}
 exec(compile(s,str(path),'exec'),ns);mods[file]=ns
c=mods['cross_figs.py'];l=mods['lower_figs.py'];h=mods['heel_fig.py']
data={'paper48':h['gen_tour'](48,48),'fields':{},'strips':{},'overlaps':{},'tt16':None}
for n in (32,48):
 for flips in (False,True):data['fields'][f'{n}_{int(flips)}']=list(c['field'](n,flips)[0])
for kind in ('normal','abnormal'):data['strips'][kind]=list(l['strip_edges'](kind,(-8,20)))
for k in (1,2):data['overlaps'][str(k)]=l['find_overlap'](k)
g=l['build'](48);data['tt16']=list({tuple(sorted((u,v))) for u,vs in g.items() for v in vs})
(out/'source_data.json').write_text(json.dumps(data));(out/'labels.json').write_text(json.dumps(labels,indent=2))
print('Source data and all figure labels exported.')
