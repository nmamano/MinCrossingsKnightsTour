"""Render checked search results. Run after the search jobs end."""
import json
from pathlib import Path

p=Path(__file__).parent
files=['lanes-8-4.json']
files += sorted(x.name for x in p.glob('lanes-P*-D*.json') if 'template' not in x.name)
files += sorted(x.name for x in p.glob('free-P*-D*.json') if 'template' not in x.name)
files += sorted(x.name for x in p.glob('lex-*.json') if 'template' not in x.name)
files += sorted(x.name for x in p.glob('tiled-free-*.json') if 'template' not in x.name)
out=['\n## Search results, 2026-10-02\n',
     'Each run used one CP-SAT worker. Time limits do not prove that a better gadget is impossible.\n',
     '| Result file | Status | T | X | Objective bound | Seconds |',
     '| --- | --- | ---: | ---: | ---: | ---: |']
results=[]
for name in files:
    r=json.loads((p/name).read_text())
    results.append((name,r))
    out.append(f"| `{name}` | {r['status']} | {r.get('T','—')} | {r.get('X','—')} | {r.get('bound','—')} | {r['time']} |")
out += ['\nA bound in a `lex-` row applies to crossings at the fixed turn count. All other bounds apply to turns.',
        'Negative turn bounds are weak solver bounds. They have no geometric meaning.\n',
        'For UNKNOWN rows, T and X describe the independently checked input seed. The main solver did not return a solution.\n',
        'VERIFIED TILING rows use no solver; their zero time entry means no solve was run.\n',
        'For each result, the full JSON records the solver status and independent checks. The adjacent `-template.json` file holds the row list for the assembler.\n',
        '### Exact templates and line pairings\n',
        'Each offset entry `[r, d]` means line c joins line c+d when c mod P = r. All offsets are signed.\n']
for name,r in results:
    if 'independent' not in r: continue
    out += [f"#### {name}\n",'```text',*r['template'],'```']
    offsets=r['independent'].get('pairing_offsets')
    if offsets is None:
        offsets=sorted([[a%r['P'],b-a] for a,b in r['independent']['line_pairing']])
    out += ['\nOffsets: `'+json.dumps(offsets)+'`.\n']
    if not r['lanes']:
        out += ['Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.\n']
text=(p/'FINDINGS.md').read_text().split('\n## Search results, 2026-10-02')[0]
(p/'FINDINGS.md').write_text(text+'\n'+'\n'.join(out)+'\n')
