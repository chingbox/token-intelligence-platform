// Node regression checks for calculation & CSV handling; no browser required.
const fs=require('fs'), vm=require('vm'),assert=require('assert');
let source=fs.readFileSync(__dirname+'/app.js','utf8').replace(/init\(\);\s*$/,'');
source+='\n;globalThis.__test={phaseTotals,parseCSV,csvEscape,importActual,state,skillText};';
const store={};const ctx={localStorage:{getItem:()=>null,setItem:(k,v)=>store[k]=v},document:{getElementById:()=>({})},Math,Number,JSON,Date,console};vm.createContext(ctx);vm.runInContext(source,ctx);
const t=ctx.__test;
let actual=t.phaseTotals();
assert(actual.input>0&&actual.output>0);
assert(Math.abs(actual.adjustedInput-actual.input*1.3)<0.001);
assert(Math.abs(actual.adjustedOutput-actual.output*1.3)<0.001);
let rows=t.parseCSV('phase,input_tokens,output_tokens\r\n"測試,階段",1,2\r\n"含""引號",3,4\r\n');
assert.equal(rows.length,3);assert.equal(rows[1][0],'測試,階段');assert.equal(rows[2][0],'含"引號');
assert(t.csvEscape('=SUM(1,2)').startsWith('"\'=SUM'));
assert(t.csvEscape('普通文字')==='"普通文字"');
assert(t.skillText.includes('name: token-budget-planning'));
console.log('PASS: phase totals, buffer, CSV quote handling, CSV formula mitigation, SKILL template');