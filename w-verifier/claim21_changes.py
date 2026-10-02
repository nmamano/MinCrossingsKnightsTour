from pathlib import Path
import difflib,json,hashlib
out=Path('w-verifier/claim21_clean')
changes=[]
for name in ('check_crossings_lower.py','check_col0_squares.py','check_knight_tiles.py','check_corner_box.py','check_square_defects.py','check_lower_stability.py'):
 a=Path('w-verifier/claim20_clean/w-turnstheory')/name;b=Path('w-turnstheory')/name
 changes.extend(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile=str(a),tofile=str(b)))
a=Path('w-verifier/claim12_supplied.py');b=Path('w-turnstheory/check_fold_proof.py');changes.extend(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile=str(a),tofile=str(b)))
(out/'checker_changes.diff').write_text(''.join(changes))
manifest=json.loads((out/'sources.json').read_text());changed=[p for p,h in manifest.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h]
(out/'end_source_check.json').write_text(json.dumps({'changed_during_audit':changed},indent=2));print('Changed during audit:',changed)
