/** Portable learning snapshots, not authentication. No notes, identities or credentials. */
import {emptyState, validateState, validResumeRoute} from './state.js';
export const MAX_TOKEN = 7000;
const MAX_AGE=7*24*60*60*1000;
const AAD=new TextEncoder().encode('fundamentos-ciberseguridad/progress-transfer/v1');
const layout=course=>course.modules.map(m=>m.id+':'+m.labs.map(l=>l.id).join(',')).join(';');
const plain=o=>o!==null && typeof o==='object' && !Array.isArray(o) && Object.getPrototypeOf(o)===Object.prototype;
function insist(ok){if(!ok)throw new Error('INVALID_TRANSFER');}
function b64(bytes){let text='';for(const n of bytes)text+=String.fromCharCode(n);return btoa(text).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
function bytes(value){insist(typeof value==='string' && /^[A-Za-z0-9_-]+$/.test(value));return Uint8Array.from(atob(value.replace(/-/g,'+').replace(/_/g,'/')),c=>c.charCodeAt(0));}
export function compact(course,state,language='es',now=Date.now(),ttl=86400000){
  insist(['es','en'].includes(language) && Number.isSafeInteger(now) && Number.isSafeInteger(ttl) && ttl>0 && ttl<=MAX_AGE && Number.isSafeInteger(now+ttl));
  const safe=validateState(state,course);
  return {v:1,id:course.id,layout:layout(course),issued:now,expires:now+ttl,route:safe.lastRoute,language,
    modules:course.modules.map(m=>{const x=safe.modules[m.id];return Number(x.read)+2*Number(x.quiz)+4*Number(x.bookmarked);}),
    labs:course.modules.flatMap(m=>m.labs.map(l=>{const x=safe.labs[l.id];return x.steps.reduce((n,b,i)=>n+(Number(b)<<i),0)+32*Number(x.done);}))};
}
export function unpack(value,course,now=Date.now()){
  insist(plain(value) && Object.keys(value).length===9 && ['v','id','layout','issued','expires','route','language','modules','labs'].every(k=>Object.hasOwn(value,k)));
  insist(Number.isSafeInteger(now) && value.v===1 && value.id===course.id && value.layout===layout(course) && ['es','en'].includes(value.language));
  insist(Number.isSafeInteger(value.issued) && Number.isSafeInteger(value.expires) && value.issued<=now+60000 && value.expires>now && value.expires>value.issued && value.expires-value.issued<=MAX_AGE);
  insist(validResumeRoute(value.route,course));
  const labs=course.modules.flatMap(m=>m.labs);
  insist(Array.isArray(value.modules) && value.modules.length===course.modules.length && value.modules.every(n=>Number.isInteger(n)&&n>=0&&n<=7));
  insist(Array.isArray(value.labs) && value.labs.length===labs.length && value.labs.every(n=>Number.isInteger(n)&&n>=0&&n<=63&&(!(n&32)||(n&31)===31)));
  const state=emptyState(course);state.lastRoute=value.route;
  course.modules.forEach((m,i)=>{const n=value.modules[i];state.modules[m.id]={read:!!(n&1),quiz:!!(n&2),bookmarked:!!(n&4),notes:''};});
  labs.forEach((l,i)=>{const n=value.labs[i];state.labs[l.id]={steps:[0,1,2,3,4].map(b=>!!(n&(1<<b))),done:!!(n&32)};});
  return {state:validateState(state,course),language:value.language,issued:value.issued,expires:value.expires};
}
export async function seal(course,state,language='es',now=Date.now(),ttl=86400000){
  if(!globalThis.crypto?.subtle)throw new Error('HTTPS_REQUIRED');
  const payload=new TextEncoder().encode(JSON.stringify(compact(course,state,language,now,ttl)));
  const key=await crypto.subtle.generateKey({name:'AES-GCM',length:256},true,['encrypt','decrypt']);
  const iv=crypto.getRandomValues(new Uint8Array(12));
  const cipher=await crypto.subtle.encrypt({name:'AES-GCM',iv,additionalData:AAD},key,payload);
  const token=['1',b64(new Uint8Array(await crypto.subtle.exportKey('raw',key))),b64(iv),b64(new Uint8Array(cipher))].join('.');
  insist(token.length<=MAX_TOKEN);return token;
}
export async function unseal(token,course,now=Date.now()){
  insist(typeof token==='string' && token.length<=MAX_TOKEN);
  const parts=token.split('.');insist(parts.length===4 && parts[0]==='1');
  const raw=bytes(parts[1]),iv=bytes(parts[2]),cipher=bytes(parts[3]);insist(raw.length===32 && iv.length===12 && cipher.length<=6000 && cipher.length>16);
  const key=await crypto.subtle.importKey('raw',raw,'AES-GCM',false,['decrypt']);
  const result=await crypto.subtle.decrypt({name:'AES-GCM',iv,additionalData:AAD},key,cipher);
  insist(result.byteLength<=8192);
  return unpack(JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(result)),course,now);
}
export function mergeProgress(local,incoming,course){
  const a=validateState(local,course),b=validateState(incoming,course);
  for(const id of Object.keys(a.modules))for(const k of ['read','quiz','bookmarked'])a.modules[id][k] ||= b.modules[id][k];
  for(const id of Object.keys(a.labs)){
    a.labs[id].steps=a.labs[id].steps.map((v,i)=>v||b.labs[id].steps[i]);
    a.labs[id].done=(a.labs[id].done||b.labs[id].done) && a.labs[id].steps.every(Boolean);
  }
  a.lastRoute=b.lastRoute;return validateState(a,course);
}
export function shareURL(base,route,language){
  const url=new URL(base);insist(['https:','http:'].includes(url.protocol));
  insist(url.protocol==='https:' || ['localhost','127.0.0.1','[::1]'].includes(url.hostname));
  url.username='';url.password='';url.search='';url.searchParams.set('lang',language==='en'?'en':'es');url.hash=route;return url.href;
}
