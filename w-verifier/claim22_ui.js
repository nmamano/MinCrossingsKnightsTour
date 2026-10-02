const fs=require('fs'),vm=require('vm');
const elements={};const elem=(id)=>elements[id]||(elements[id]={innerHTML:'',textContent:'',classList:{toggle(){}},addEventListener(){},getContext(){return{}},querySelectorAll(){return[]}});
const ctx={document:{getElementById:elem,querySelectorAll(){return[]}},window:{addEventListener(){}},KT:{decode(){},analyse(){}},console,Set,Map,Math};
vm.createContext(ctx);let src=fs.readFileSync('demo/app.js','utf8');src=src.replace('  // ---------- start; the URL hash keeps the state shareable ----------','  globalThis.audit = {C,LOWER,KNOWN,state,fmtConst,renderCounts,slopeOf}; return;\n  // ---------- start; the URL hash keeps the state shareable ----------');vm.runInContext(src,ctx);
const a=ctx.audit,summary=JSON.parse(fs.readFileSync('demo/data/summary.json'));a.state.summary=summary;let rows=[],bad=[];
for(const[key,ns]of Object.entries(summary))for(const[n,d]of Object.entries(ns)){
 a.state.key=key;a.state.n=+n;a.state.metric=key==='heel21'||key==='T18'||key==='TT16'?'T':'X';a.state.tour={n:+n,X:{length:d.crossings},T:{length:d.turns},rec:d,ok:true};a.renderCounts();rows.push({key,n:+n,html:elem('counts').innerHTML,check:elem('check').textContent});
 for(const m of ['X','T']){const sl=a.KNOWN[m][key]||a.slopeOf(key,m);if(!sl)continue;const c=d[m==='X'?'crossings':'turns']-sl[0]*n/sl[1],num=Math.round(Math.abs(c)*sl[1]),whole=Math.floor(num/sl[1]),r=num%sl[1];if(![1,2,3].includes(sl[1])&&r&&whole)bad.push({key,n:+n,m,offset:c,shown:a.fmtConst(c,sl[1])});}
}
fs.writeFileSync('w-verifier/claim22_ui.json',JSON.stringify({rows,badFractionFormatting:bad,metadata:a.C,lower:Object.fromEntries(Object.entries(a.LOWER).map(([m,ls])=>[m,ls.map(l=>({name:l.name,at96:l.f(96)}))]))},null,2));console.log('Rendered',rows.length,'data records; ambiguous mixed fractions',bad.length);console.log(bad.slice(0,8));
