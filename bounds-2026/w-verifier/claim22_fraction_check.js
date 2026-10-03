const fs=require('fs');const rows=JSON.parse(fs.readFileSync('w-verifier/claim22_ui.json')).badFractionFormatting;
const gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a);
function fmtConst(v,b){const num=Math.round(v*b),sign=num<0?'−':'+',q=Math.abs(num),g=gcd(q,b),a=q/g,d=b/g;return `${sign} ${d===1?a:`${a}/${d}`}`;}
for(const r of rows){const b=Number(r.shown.split('/')[1]);const s=fmtConst(r.offset,b),match=s.match(/^([+−]) (\d+)(?:\/(\d+))?$/);const val=(match[1]==='−'?-1:1)*Number(match[2])/Number(match[3]||1);if(Math.abs(val-r.offset)>1e-9)throw Error(JSON.stringify(r));}
console.log('Proposed formatter passes all',rows.length,'bad displays');
console.log('H16a n50 T:',fmtConst(-26.5,4),'LF4 n98 X:',fmtConst(20+34/48,48));
