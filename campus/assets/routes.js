/** Optional local self-assessment. No identity, notes, imports, network or legal decisions. */
const KEY='smartkea.learning-paths.v1';
const routes=[...document.querySelectorAll('[data-route]')];
const phases=[...document.querySelectorAll('[data-phase]')];
const allowed=new Set(phases.map(p=>p.dataset.phase));
const remember=document.querySelector('#remember-paths');
const status=document.querySelector('#path-status');
const select=document.querySelector('#route-filter');
let slide=0,session=null,knownRecordId=null,knownRaw=null,lifecycle=0,intent=0;
const pending=new Map();
const LOCK=KEY+':write';
function progress(){for(const route of routes){const checks=[...route.querySelectorAll('[data-phase]')];route.querySelector('[data-progress]').textContent=`${checks.filter(p=>p.checked).length} de ${checks.length} etapas revisadas`;}}
function read(raw){
 if(typeof raw!=='string'||raw.length>=20000)throw Error('SIZE');
 const state=JSON.parse(raw);
 if(state?.schema!==1||!Array.isArray(state.completed)||state.completed.length>allowed.size||state.completed.some(p=>typeof p!=='string'||!allowed.has(p)))throw Error('SCHEMA');
 const recordId=state.recordId===undefined?'legacy':state.recordId;
 if(typeof recordId!=='string'||!/^(?:legacy|[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})$/i.test(recordId))throw Error('IDENTITY');
 return {recordId,completed:new Set(state.completed)};
}
function apply(done){phases.forEach(p=>p.checked=pending.get(p.dataset.phase)?.checked??done.has(p.dataset.phase));progress();}
function snapshot(){return new Set(phases.filter(p=>p.checked).map(p=>p.dataset.phase));}
function load(){knownRaw=localStorage.getItem(KEY);return knownRaw===null?null:read(knownRaw);}
function canCoordinate(){try{return typeof navigator.locks?.request==='function';}catch{return false;}}
function checkpoint(){
 // Yield while holding the lock: publish writes and receive prior storage notifications.
 return new Promise(resolve=>{
  const channel=new MessageChannel();
  channel.port1.onmessage=()=>{channel.port1.close();channel.port2.close();resolve();};
  channel.port2.postMessage(null);
 });
}
function stopSaving(message){session=null;remember.checked=false;pending.clear();lifecycle++;status.textContent=message;}
function recordChanged(record){
 // A new lifetime requires a deliberate opt-in; queued work belongs to the old one.
 knownRecordId=record?.recordId??null;
 apply(record?.completed??new Set()); // Preserve this tab's pending marks as a local draft.
 stopSaving(record?'El registro se creó de nuevo en otra pestaña. Tus cambios pendientes quedan solo en esta visita; activa el guardado para incorporarlos.':'El registro se eliminó en otra pestaña. Tus cambios pendientes quedan solo en esta visita.');
}
async function save(token,change=null,draft=null){
 try{
  if(!canCoordinate())throw Error('COORDINATION');
  await navigator.locks.request(LOCK,{mode:'exclusive'},async()=>{
   await checkpoint();
   if(session!==token||!remember.checked)return;
   const current=load();
   if(change&&(!current||current.recordId!==token.recordId)){recordChanged(current);return;}
   const done=new Set(current?.completed??[]);
   if(change){if(change.checked)done.add(change.id);else done.delete(change.id);}
   else{
    // Existing v1 records keep a stable legacy identity until actually removed.
    token.recordId=current?.recordId??crypto.randomUUID();
    for(const id of draft)done.add(id);
   }
   const raw=JSON.stringify({schema:1,recordId:token.recordId,completed:phases.filter(p=>done.has(p.dataset.phase)).map(p=>p.dataset.phase)});
   localStorage.setItem(KEY,raw);knownRaw=raw;knownRecordId=token.recordId;
   await checkpoint();
   if(session!==token)return;
   if(change&&pending.get(change.id)?.intent===change.intent)pending.delete(change.id);
   apply(done);
   status.textContent=pending.size?'Guardando cambios de esta visita…':'Marcas guardadas solo en este navegador. Sin sincronización de cuenta ni datos personales.';
  });
 }
 catch{if(session===token)stopSaving('No se ha podido confirmar el guardado. El navegador no permite coordinar o guardar las marcas; puedes seguir durante esta visita.');}
}
function mark(phase){
 progress();if(!remember.checked||!session)return;
 const change={id:phase.dataset.phase,checked:phase.checked,intent:++intent};
 pending.set(change.id,change);status.textContent='Guardando cambios de esta visita…';
 void save(session,change);
}
function enableSaving(){
 lifecycle++;session={recordId:null};
 status.textContent='Guardando marcas de esta visita…';
 void save(session,null,snapshot());
}
async function disableSaving(clear=false){
 const previous=session,expectedId=previous?.recordId??knownRecordId,expectedRaw=knownRaw;
 stopSaving('Eliminando la copia guardada…');const action=lifecycle;
 if(clear)apply(new Set());
 try{
  if(!canCoordinate())throw Error('COORDINATION');
  let changed=false;
  await navigator.locks.request(LOCK,{mode:'exclusive'},async()=>{
   await checkpoint();
   const raw=localStorage.getItem(KEY);
   let record=null;try{if(raw!==null)record=read(raw);}catch{}
   const same=record?record.recordId===(previous?.recordId??expectedId):raw!==null&&raw===expectedRaw;
   if(same){localStorage.removeItem(KEY);await checkpoint();}
   else changed=raw!==null;
   if(session===null&&lifecycle===action){knownRaw=same?null:raw;knownRecordId=same?null:record?.recordId??null;}
  });
  if(session!==null||lifecycle!==action)return;
  status.textContent=changed?'Guardado desactivado para esta visita. Otra pestaña creó un registro nuevo; no se ha eliminado esa copia.':clear?'Marcas de rutas borradas. El campus no se ha modificado.':'Guardado desactivado y copia local eliminada. Marcas solo para esta visita.';
 }catch{
  if(session===null&&lifecycle===action)status.textContent='Las marcas de esta visita siguen disponibles sin guardar. No fue posible eliminar la copia local; revisa el almacenamiento del navegador.';
 }
}
function filter(id){
 if(id!=='all'&&!routes.some(r=>r.dataset.route===id))id='all';
 select.value=id;for(const r of routes)r.hidden=id!=='all'&&r.dataset.route!==id;
 history.replaceState(null,'',location.pathname+location.search+(id==='all'?'':'#ruta-'+id));
}
function showSlide(){routes.forEach((r,i)=>{r.hidden=false;r.classList.toggle('presenting',i===slide);});document.querySelector('#slide-count').textContent=`Ruta ${slide+1} de ${routes.length}`;window.scrollTo(0,0);}
function exit(){document.body.classList.remove('presentation');routes.forEach(r=>r.classList.remove('presenting'));filter(select.value);document.querySelector('#start-presentation').focus();}
try{
 const record=load();
 if(record){apply(record.completed);knownRecordId=record.recordId;if(canCoordinate()){session={recordId:record.recordId};remember.checked=true;status.textContent='Marcas recuperadas de este navegador; no son una certificación.';}}
 if(!canCoordinate())status.textContent='Este navegador no permite coordinar el guardado entre pestañas. Las marcas quedan solo durante esta visita.';
}catch{status.textContent='No se pudo leer el almacenamiento local. Puedes seguir sin guardar.';}
phases.forEach(p=>p.addEventListener('change',()=>mark(p)));
remember.addEventListener('change',()=>{if(remember.checked)enableSaving();else void disableSaving();});
document.querySelector('#clear-paths').addEventListener('click',()=>{if(!window.confirm('¿Borrar únicamente las marcas de estas rutas? Las notas y el progreso del campus no se modificarán.'))return;void disableSaving(true);});
window.addEventListener('storage',event=>{
 if((event.key!==KEY&&event.key!==null)||!remember.checked||!session||session.recordId===null)return;
 try{const record=load();if(!record||record.recordId!==session.recordId)recordChanged(record);else apply(record.completed);}
 catch{stopSaving('No se pudo leer el registro compartido. Se conservan las marcas de esta visita sin guardar.');}
});
select.addEventListener('change',()=>filter(select.value));
document.querySelectorAll('[data-route-select]').forEach(b=>b.addEventListener('click',()=>{filter(b.dataset.routeSelect);document.querySelector('#ruta-'+b.dataset.routeSelect).scrollIntoView({block:'start'});}));
document.querySelector('#print-paths').addEventListener('click',()=>window.print());
document.querySelector('#start-presentation').addEventListener('click',()=>{slide=Math.max(0,routes.findIndex(r=>r.dataset.route===select.value));document.body.classList.add('presentation');showSlide();document.querySelector('#next-route').focus();});
document.querySelector('#next-route').addEventListener('click',()=>{slide=(slide+1)%routes.length;showSlide();});
document.querySelector('#previous-route').addEventListener('click',()=>{slide=(slide+routes.length-1)%routes.length;showSlide();});
document.querySelector('#exit-presentation').addEventListener('click',exit);
document.addEventListener('keydown',e=>{if(!document.body.classList.contains('presentation')||/INPUT|SELECT|TEXTAREA/.test(e.target.tagName))return;if(e.key==='Escape'){e.preventDefault();exit();}else if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();slide=(slide+(e.key==='ArrowRight'?1:routes.length-1))%routes.length;showSlide();}});
const initial=location.hash.startsWith('#ruta-')?location.hash.slice(6):'all';filter(initial);progress();
