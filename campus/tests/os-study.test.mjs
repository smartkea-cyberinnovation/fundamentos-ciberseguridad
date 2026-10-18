import test from 'node:test';
import assert from 'node:assert/strict';
import {empty,resetRecord,parse,merge,totals,completion,createTimer,start,tick,pause,format,remainingEstimate} from '../os_classroom/model.js';
import {routeFor,guidance,HOSTS,TARGETS} from '../os_classroom/environment.js';
const course={lessons:[{id:'OS-C01',views:[{id:'OS-C01:0',kind:'concept'},{id:'OS-C01:1',kind:'lab'}]}]};
const record=()=>({lesson:'OS-C01',kind:'study',ms:2000,problemMs:1000,at:1000});
test('explicit start only',()=>{const t=createTimer();assert.equal(tick(t,500),0);assert.equal(t.elapsed,0);});
test('monotonic elapsed uses differences',()=>{const t=createTimer();start(t,100);tick(t,1400);assert.equal(t.elapsed,1300);});
test('pause stops accrual',()=>{const t=createTimer();start(t,0);pause(t,1000);tick(t,8000);assert.equal(t.elapsed,1000);});
test('resume does not count gap',()=>{const t=createTimer();start(t,0);pause(t,1000);start(t,9000);tick(t,10000);assert.equal(t.elapsed,2000);});
test('clock backwards pauses',()=>{const t=createTimer();start(t,100);tick(t,90);assert.equal(t.running,false);assert.equal(t.elapsed,0);});
test('suspension gap is excluded',()=>{const t=createTimer();start(t,0);tick(t,600000);assert.equal(t.reason,'gap');assert.equal(t.elapsed,0);});
test('focus ends capped and no automatic break',()=>{const t=createTimer('study',2000);start(t,0);tick(t,4000);assert.equal(t.elapsed,2000);assert.equal(t.remaining,0);assert.equal(t.running,false);assert.equal(t.kind,'study');});
test('problem time is a subset',()=>{const t=createTimer();start(t,0);tick(t,1000);t.problem=true;tick(t,3000);assert.equal(t.problemMs,2000);assert.equal(t.elapsed,3000);});
test('break never counts problem time',()=>{const t=createTimer('break',300000);start(t,0);t.problem=true;tick(t,1000);assert.equal(t.problemMs,0);});
test('double pause does not double count',()=>{const t=createTimer();start(t,0);pause(t,1000);pause(t,2000);assert.equal(t.elapsed,1000);});
test('bad duration rejected',()=>{assert.throws(()=>createTimer('study',-1));assert.throws(()=>createTimer('random'));});
test('clock formatting',()=>{assert.equal(format(1500000),'25:00');assert.equal(format(0),'00:00');});
test('schema roundtrip',()=>{assert.deepEqual(parse(JSON.stringify(empty()),course),empty());});
test('old schema-1 copies have a stable legacy identity and generation zero',()=>{
 const x=empty();delete x.generation;delete x.recordId;const raw=JSON.stringify(x);
 assert.deepEqual(parse(raw,course,1000),empty());assert.deepEqual(parse(raw,course,2000),empty());
});
test('reset preserves the persisted lifetime identity',()=>{
 const x={...empty(),recordId:'record-first-life',generation:5};
 const reset=resetRecord(x);assert.equal(reset.recordId,x.recordId);assert.equal(reset.generation,6);
 assert.deepEqual(parse(JSON.stringify(reset),course),reset);
});
test('generations cannot merge across different record lifetimes',()=>{
 const old={...empty(),recordId:'record-first-life',generation:8},fresh={...empty(),recordId:'record-new-life'};
 assert.throws(()=>merge(old,fresh),/RECORD_ID/);assert.throws(()=>merge(fresh,old),/RECORD_ID/);
});
test('invalid record identities are rejected',()=>{for(const recordId of ['',null,1,'a/b','x'.repeat(81)])assert.throws(()=>parse(JSON.stringify({...empty(),recordId}),course));});
test('reset removes old marks and sessions in either merge order',()=>{
 const old=empty();old.marks['OS-C01:0']={status:'done',at:Number.MAX_SAFE_INTEGER};old.sessions['session-123']=record();
 const reset=resetRecord(old);assert.equal(reset.schema,1);assert.equal(reset.generation,1);
 assert.deepEqual(merge(old,reset),reset);assert.deepEqual(merge(reset,old),reset);
 reset.marks['OS-C01:1']={status:'review',at:2000};
 assert.deepEqual(merge(reset,old),reset);assert.deepEqual(parse(JSON.stringify(reset),course,2000),reset);
});
test('invalid generations are rejected',()=>{for(const generation of [-1,1.5,'1'])assert.throws(()=>parse(JSON.stringify({...empty(),generation}),course));});
test('future marks have stable low priority across repeated saves and merges',()=>{
 const future=empty();future.marks['OS-C01:0']={status:'done',at:Number.MAX_SAFE_INTEGER};const raw=JSON.stringify(future);
 let local=parse(raw,course,2000);assert.equal(local.marks['OS-C01:0'].at,0);
 local.marks['OS-C01:0']={status:'review',at:2000};
 for(const now of [2000,2001,3000,5000]){
  local=parse(JSON.stringify(merge(local,parse(raw,course,now))),course,now);
  assert.deepEqual(local.marks['OS-C01:0'],{status:'review',at:2000});
 }
});
test('even a one-millisecond future date cannot block a local edit',()=>{
 const x=empty();x.marks['OS-C01:0']={status:'done',at:2001};
 const stored=JSON.stringify(parse(JSON.stringify(x),course,2000));const local=empty();local.marks['OS-C01:0']={status:'blocked',at:2000};
 for(const now of [2000,2001,3000])assert.equal(merge(local,parse(stored,course,now)).marks['OS-C01:0'].status,'blocked');
});
test('marks require recognized IDs',()=>{const x=empty();x.marks['OS-C99:0']={status:'done',at:1};assert.throws(()=>parse(JSON.stringify(x),course));});
test('unknown state rejected',()=>{const x=empty();x.marks['OS-C01:0']={status:'excellent',at:1};assert.throws(()=>parse(JSON.stringify(x),course));});
test('sessions must have bounded values',()=>{const x=empty();x.sessions['session-123']=record();x.sessions['session-123'].ms=-1;assert.throws(()=>parse(JSON.stringify(x),course));});
test('problem subset invariant',()=>{const x=empty();x.sessions['session-123']={...record(),problemMs:3000};assert.throws(()=>parse(JSON.stringify(x),course));});
test('unrelated imports rejected',()=>{assert.throws(()=>parse('{"course":"other"}',course));});
test('UTF8 byte size checked',()=>{assert.throws(()=>parse('é'.repeat(600000),course));});
test('timer running data not restored',()=>{const x={...empty(),running:true,lastClock:100};assert.equal(parse(JSON.stringify(x),course).running,undefined);});
test('latest mark wins',()=>{const a=empty(),b=empty();a.marks['OS-C01:0']={status:'done',at:1};b.marks['OS-C01:0']={status:'review',at:2};assert.equal(merge(a,b).marks['OS-C01:0'].status,'review');});
test('same session merges idempotently',()=>{const a=empty();a.sessions['session-123']=record();assert.deepEqual(merge(a,a),a);assert.equal(totals(merge(a,a)).study,2000);});
test('distinct sessions sum',()=>{const a=empty(),b=empty();a.sessions['session-123']=record();b.sessions['session-456']=record();assert.equal(totals(merge(a,b)).study,4000);});
test('merge preserves own resume route',()=>{const a=empty(),b=empty();a.last='OS-C01/1';assert.equal(merge(a,b).last,'OS-C01/1');});
test('blocked never completed',()=>{const a=empty();a.marks['OS-C01:0']={status:'blocked',at:1};assert.equal(completion(a,course.lessons[0]).done,0);assert.equal(completion(a,course.lessons[0]).blocked,1);});
test('remaining estimates remove only done',()=>{const a=empty(),l=course.lessons[0];assert.deepEqual(remainingEstimate(a,l),{min:4,max:14});a.marks[l.views[0].id]={status:'done',at:1};assert.deepEqual(remainingEstimate(a,l),{min:3,max:10});});
test('declared time stays distinct',()=>{const a=empty();a.sessions['session-123']={...record(),kind:'declared',problemMs:0};assert.equal(totals(a).study,0);assert.equal(totals(a).declared,2000);});
test('Mac ARM requires ARM Windows',()=>{assert.equal(routeFor('mac-arm','windows'),'windows-arm');});
test('Mac Intel uses x64 route',()=>{assert.equal(routeFor('mac-intel','windows'),'windows-x64');});
test('tablet is not a native lab',()=>{assert.equal(routeFor('tablet','windows'),'remote');});
test('macOS on non-Mac uses authorized Mac lab',()=>{assert.equal(routeFor('windows-x64','macos'),'remote-mac');});
test('unknown environment requires identification',()=>{assert.equal(routeFor('unknown','windows'),'identify');});
test('every path has bilingual steps and primary HTTPS links',()=>{for(const host of HOSTS)for(const target of TARGETS)for(const lang of ['es','en']){const g=guidance(host,target,lang);assert.ok(g.notes.length);assert.equal(g.steps.length,7);assert.ok(g.links.every(x=>x[1].startsWith('https://')));}});
