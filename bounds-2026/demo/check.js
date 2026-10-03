// Independent JS check of every demo data file: one closed tour, and the JS counts equal the Python counts.
// Usage: node demo/check.js
const fs = require('fs'), path = require('path');
const { decode, analyse } = require('./tourlib.js');
const dir = path.join(__dirname, 'data');
let bad = 0, n = 0;
for (const f of fs.readdirSync(dir).filter((f) => /_n\d+\.json$/.test(f)).sort()) {
  const rec = JSON.parse(fs.readFileSync(path.join(dir, f)));
  const t = decode(rec), a = analyse(t);
  const ok = a.ok && rec.valid && a.X.length === rec.crossings && a.T.length === rec.turns &&
    (rec.brute_crossings == null || rec.brute_crossings === rec.crossings);
  n++; if (!ok) { bad++; console.log('MISMATCH', f, a.ok, rec.valid, a.X.length, rec.crossings, a.T.length, rec.turns, rec.brute_crossings); }
}
console.log(`${n} files checked, ${bad} problems`);
process.exit(bad ? 1 : 0);
