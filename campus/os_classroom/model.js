// Pure learning/timer model. Elapsed time is recorded activity, not proof of attention.
export const KEY='smartkea.os.study.v1';
export const MAX_BYTES=1024*1024;
export const STATUSES=['done','review','blocked'];
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
export function empty(){return {schema:1,course:'smartkea-os-study',marks:{},sessions:{},last:'OS-C01/0',goal:2};}
export function parse(raw,course){
  if(typeof raw!=='string'||new TextEncoder().encode(raw).length>MAX_BYTES)throw Error('SIZE');
  const x=JSON.parse(raw);if(!object(x)||x.schema!==1||x.course!=='smartkea-os-study'||!object(x.marks)||!object(x.sessions))throw Error('SCHEMA');
  const ids=new Set(course.lessons.flatMap(l=>l.views.map(v=>v.id))),lessons=new Set(course.lessons.map(l=>l.id));
  const clean=empty();
  if(Object.keys(x.marks).length>ids.size||Object.keys(x.sessions).length>1000)throw Error('LIMIT');
  for(const [k,v] of Object.entries(x.marks)){
    if(!ids.has(k)||!object(v)||!STATUSES.includes(v.status)||!Number.isSafeInteger(v.at)||v.at<0)throw Error('MARK');
    clean.marks[k]={status:v.status,at:v.at};
  }
  for(const [k,v] of Object.entries(x.sessions)){
    if(!/^[a-zA-Z0-9-]{8,80}$/.test(k)||!object(v)||!lessons.has(v.lesson)||!['study','practice','break','declared'].includes(v.kind))throw Error('SESSION');
    for(const n of ['ms','problemMs','at'])if(!Number.isSafeInteger(v[n])||v[n]<0)throw Error('TIME');
    if(v.ms>14400000||v.problemMs>v.ms)throw Error('TIME');
    clean.sessions[k]={lesson:v.lesson,kind:v.kind,ms:v.ms,problemMs:v.problemMs,at:v.at};
  }
  if(typeof x.last==='string'&&/^OS-[CLWA]\d{2}\/\d+$/.test(x.last)){
    const [id,n]=x.last.split('/');const l=course.lessons.find(l=>l.id===id);
    if(l&&Number(n)<l.views.length)clean.last=x.last;
  }
  if(Number.isInteger(x.goal)&&x.goal>=1&&x.goal<=8)clean.goal=x.goal;
  return clean;
}
export function merge(a,b){
  const out=structuredClone(a);
  for(const [k,v] of Object.entries(b.marks))if(!out.marks[k]||v.at>out.marks[k].at)out.marks[k]=structuredClone(v);
  for(const [k,v] of Object.entries(b.sessions)){
    const old=out.sessions[k];if(!old){out.sessions[k]=structuredClone(v);continue;}
    // Same immutable identity: imported duplicates cannot create a second session.
    if(old.lesson===v.lesson&&old.kind===v.kind&&old.at===v.at){old.ms=Math.max(old.ms,v.ms);old.problemMs=Math.min(old.ms,Math.max(old.problemMs,v.problemMs));}
  }
  return out;
}
export function totals(state,lesson=null,date=null){
  const t={study:0,practice:0,break:0,declared:0,problem:0};
  for(const s of Object.values(state.sessions)){
    if(lesson&&s.lesson!==lesson)continue;
    if(date&&new Date(s.at).toDateString()!==date.toDateString())continue;
    t[s.kind]+=s.ms;t.problem+=s.problemMs;
  }return t;
}
export function completion(state,lesson){
  const done=lesson.views.filter(v=>state.marks[v.id]?.status==='done').length;
  return {done,total:lesson.views.length,review:lesson.views.filter(v=>state.marks[v.id]?.status==='review').length,blocked:lesson.views.filter(v=>state.marks[v.id]?.status==='blocked').length};
}
export function createTimer(kind='study',duration=25*60000){
  if(!['study','practice','break'].includes(kind)||!Number.isFinite(duration)||duration<=0||duration>3600000)throw Error('TIMER');
  return {kind,duration,remaining:duration,elapsed:0,problemMs:0,problem:false,running:false,last:null,reason:''};
}
export function start(timer,now){if(!Number.isFinite(now)||timer.remaining<=0)return;timer.last=now;timer.running=true;timer.reason='';}
export function tick(timer,now){
  if(!timer.running)return 0;
  const delta=now-timer.last;
  if(!Number.isFinite(delta)||delta<0||delta>15000){timer.running=false;timer.last=null;timer.reason='gap';return 0;}
  const used=Math.min(delta,timer.remaining);timer.elapsed+=used;timer.remaining-=used;
  if(timer.problem&&timer.kind!=='break')timer.problemMs+=used;
  timer.last=now;if(timer.remaining===0){timer.running=false;timer.reason='finished';timer.last=null;}
  return used;
}
export function pause(timer,now,reason='manual'){tick(timer,now);timer.running=false;timer.last=null;if(timer.reason!=='finished')timer.reason=reason;}
export function format(ms){const sec=Math.max(0,Math.floor(ms/1000));return `${Math.floor(sec/60).toString().padStart(2,'0')}:${(sec%60).toString().padStart(2,'0')}`;}
export function remainingEstimate(state,lesson){
  let min=0,max=0;
  for(const v of lesson.views){if(state.marks[v.id]?.status==='done')continue;const lab=['lab','environment','evidence','recovery'].includes(v.kind);min+=lab?3:1;max+=lab?10:4;}
  return {min,max}; // Planning assumptions, not validated learning-duration predictions.
}
