import {KEY,empty,parse,merge,totals,completion,createTimer,start,tick,pause,format,remainingEstimate} from './model.js';
import {HOSTS,TARGETS,guidance} from './environment.js';
const $=s=>document.querySelector(s),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let lang=new URL(location.href).searchParams.get('lang')==='en'?'en':'es',course,state=empty(),current,index=0,persistent=false,recoveryRaw=null,loading=0;
let timer=createTimer(),session=null,releaseLock=null,lockPending=false,lastSave=0,idleAt=performance.now(),noticeId;
let hints=0,pendingImport=null,host='unknown',quizPassed=false;
const tr=(es,en)=>lang==='es'?es:en;
const p=text=>'<p>'+esc(text)+'</p>';
const button=(id,text,cls='')=>`<button id="${id}" class="${cls}">${esc(text)}</button>`;
const link=(url,label)=>`<a href="${esc(url)}" rel="noreferrer noopener">${esc(label)}</a>`;
const groupName=g=>({common:tr('Fundamentos comunes','Shared foundations'),linux:'Linux · Bash',windows:'Windows · CMD / PowerShell',macos:'macOS · zsh'})[g];
const kindName=k=>({goal:tr('Objetivo','Goal'),concept:tr('Un concepto','One concept'),micro:tr('Micropráctica','Micropractice'),diagram:tr('Esquema','Diagram'),example:tr('Ejemplo explicado','Worked example'),environment:tr('Entorno','Environment'),lab:tr('Práctica guiada','Guided lab'),quiz:tr('Autoevaluación','Self-check'),evidence:tr('Evidencia','Evidence'),recovery:tr('Recuperación','Recovery'),handover:tr('Entrega profesional','Professional handover')})[k];
function toast(text){clearTimeout(noticeId);$('#status').textContent=text;$('#status').hidden=false;noticeId=setTimeout(()=>$('#status').hidden=true,6000);}
function download(name,text,type='application/json'){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([text],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1500);}
function readSaved(){try{return localStorage.getItem(KEY);}catch{return null;}}
function save(){
 if(!persistent||recoveryRaw||!course)return;
 try{const old=readSaved();if(old)state=merge(state,parse(old,course));const valid=parse(JSON.stringify(state),course);localStorage.setItem(KEY,JSON.stringify(valid));}
 catch{persistent=false;toast(tr('No se pudo guardar. Exporta tu copia; no se ha borrado la anterior.','Could not save. Export your record; the previous copy was not deleted.'));}
}
function route(){const raw=location.hash.slice(1);const match=/^(OS-[CLWA]\d{2})\/(\d+)$/.exec(raw||state.last);let l=course.lessons.find(l=>l.id===match?.[1]);if(!l)l=course.lessons[0];return [l,Math.min(match?Number(match[2]):0,l.views.length-1)];}
function go(id,n=0){halt('navigation');location.hash=id+'/'+n;}
function noteRoute(){state.last=current.id+'/'+index;try{sessionStorage.setItem(KEY+'.route',state.last);}catch{}save();}
function chrome(){
 document.documentElement.lang=lang;document.title=tr('Sistemas operativos · SmartKEA','Operating systems · SmartKEA');$('#language').value=lang;
 const labels={'brand-text':tr('Sistemas operativos','Operating systems'),menu:tr('Índice','Outline'),help:tr('Mi entorno','My environment'),dashboard:tr('Mi estudio','My study'),present:document.body.classList.contains('presentation')?tr('Salir de presentación','Exit presentation'):tr('Presentar','Present'),fullscreen:tr('Pantalla completa','Fullscreen'),share:tr('Compartir lección','Share lesson'),prev:tr('Anterior','Previous'),next:tr('Siguiente','Next'),pause:tr('Pausar','Pause'),break:tr('Descanso 5 min','5-minute break'),problem:tr('Me he atascado','I am stuck'),'coach-title':tr('Resolver un problema','Solve a problem'),'coach-prompt':tr('Tras 10 minutos sin información nueva, cambia de estrategia: describe el síntoma, formula dos hipótesis y consulta la ayuda. El cronómetro no mide tu capacidad.','After 10 minutes without new information, change strategy: describe the symptom, form two hypotheses and consult help. The timer does not measure ability.'),'note-label':tr('Esperado → observado → hipótesis → una prueba → resultado → siguiente acción. Solo datos ficticios.','Expected → observed → hypothesis → one check → result → next action. Fictitious data only.'),hint:tr('Pista progresiva','Progressive hint'),'download-note':tr('Descargar nota','Download note'),'close-panel':tr('Cerrar','Close'),privacy:tr('Registro local y autodeclarado. Sin cuenta ni sincronización. No guardar secretos.','Local self-reported record. No account or synchronization. Do not store secrets.'),reading:tr('Lectura continua','Continuous reading')};
 for(const [id,text] of Object.entries(labels))$('#'+id).textContent=text;
 $('#reading').href='reading.'+lang+'.html';paintTimer();
}
function outline(){
 let html=`<label class="sr" for="find">${tr('Buscar lecciones','Find lessons')}</label><input id="find" class="outline-search" type="search" maxlength="100" placeholder="${tr('Buscar lección…','Find a lesson…')}">`;
 for(const g of TARGETS){html+='<h2>'+groupName(g)+'</h2>';for(const l of course.lessons.filter(l=>l.group===g)){const c=completion(state,l);html+=`<a href="#${l.id}/0" ${l.id===current.id?'aria-current="page"':''} data-lesson="${l.id}"><span class="index-number">${l.id.replace('OS-','')}<br>${c.done}/${c.total}</span><span>${esc(l.title)}</span></a>`;}}
 $('#outline').innerHTML=html;
 $('#find').addEventListener('input',event=>{const value=event.target.value.normalize('NFD').replace(/\p{Diacritic}/gu,'').toLowerCase();for(const a of $('#outline').querySelectorAll('a[data-lesson]'))a.hidden=!a.textContent.normalize('NFD').replace(/\p{Diacritic}/gu,'').toLowerCase().includes(value);});
}
function viewBody(v){
 let out='';
 if(v.body)out+=p(v.body);
 if(v.takeaway)out+='<div class="takeaway">'+esc(v.takeaway)+'</div>';
 if(v.diagram)out+='<ol class="diagram">'+v.diagram.map((x,i)=>`<li><span>${i+1}</span>${esc(x)}</li>`).join('')+'</ol>';
 if(v.code)out+='<p class="muted">'+esc(v.shell||'')+'</p><pre><code>'+esc(v.code)+'</code></pre>'+button('copy-code',tr('Copiar código, no ejecutar','Copy code, do not execute'));
 if(v.expected)out+='<details><summary>'+tr('Resultado y criterio para comprobar','Expected result and checking criterion')+'</summary>'+p(v.expected)+'</details>';
 if(v.kind==='environment')out+=button('open-environment',tr('Necesito preparar mi equipo','I need to prepare my device'))+p(tr('Leer en otro SO es posible. Ejecutar esta práctica exige el entorno indicado. No marques ejecutado un ejercicio que solo has leído.','You can read on another OS. Running this lab requires its stated environment. Do not mark a read-only exercise as executed.'));
 if(v.kind==='quiz')out+='<div class="quiz-options">'+v.quiz.options.map((x,i)=>`<button data-answer="${i}">${esc(x)}</button>`).join('')+'</div><p id="answer-feedback" role="status"></p>';
 if(v.kind==='evidence'||v.kind==='handover')out+=button('template',tr('Descargar plantilla de entrega','Download handover template'));
 if(v.kind==='handover')out+='<details><summary>'+tr('Error frecuente que debes evitar','Common mistake to avoid')+'</summary>'+p(current.mistake)+'</details><h2>'+tr('Profundizar con las fuentes','Go deeper with sources')+'</h2><ul class="source-list">'+current.sources.map(r=>'<li>'+link(r.url,r.title)+'</li>').join('')+'</ul>';
 if(document.body.classList.contains('presentation')&&v.kind==='concept')return '<p class="lead">'+esc(v.takeaway)+'</p><details><summary>'+tr('Abrir explicación completa','Open full explanation')+'</summary>'+p(v.body)+'</details>';
 return out;
}
function render(){
 if(!course)return;
 [current,index]=route();quizPassed=false;hints=0;$('#hint-text').textContent='';
 const v=current.views[index],c=completion(state,current),mark=state.marks[v.id]?.status;
 $('#position').textContent=current.id+' · '+groupName(current.group)+' · '+(index+1)+' / '+current.views.length;
 $('#content').innerHTML='<p class="eyebrow">'+kindName(v.kind)+'</p><h1>'+esc(v.title)+'</h1>'+viewBody(v);
 const native=['lab','evidence','recovery'].includes(v.kind)&&current.group!=='common';
 $('#marks').innerHTML=(native?`<label><input type="checkbox" id="native-confirm"> ${tr('He realizado esta comprobación en el SO requerido, no solo leído el texto.','I performed this check on the required OS, not merely read the text.')}</label>`:'')+`<div class="actions">${button('done',tr('Lo he comprobado','I checked it'),'primary')}${button('review',tr('Necesito repasar','Needs review'))}${button('blocked',tr('Bloqueo de entorno','Environment blocker'))}</div><small>${tr('Marca actual: ','Current mark: ')}${esc(mark||tr('pendiente','pending'))} · ${c.done}/${c.total} ${tr('puntos comprobados por ti. No acredita dominio.','points self-checked. This does not certify mastery.')}</small>`;
 if(v.kind==='quiz')$('#done').disabled=true;
 $('#prev').disabled=index===0&&course.lessons[0].id===current.id;
 $('#next').disabled=index===current.views.length-1&&course.lessons.at(-1).id===current.id;
 $('#step-progress').value=(index+1)/current.views.length*100;
 outline();chrome();noteRoute();$('#content').scrollTop=0;
}
function mark(status){
 const v=current.views[index];
 if(status==='done'&&v.kind==='quiz'&&!quizPassed)return;
 if(status==='done'&&$('#native-confirm')&&!$('#native-confirm').checked){toast(tr('Confirma ejecución nativa o marca bloqueo de entorno.','Confirm native execution or mark an environment blocker.'));return;}
 state.marks[v.id]={status,at:Date.now()};save();render();
}
function move(delta){
 const next=index+delta,l=course.lessons.indexOf(current);
 if(next<0&&l>0)go(course.lessons[l-1].id,course.lessons[l-1].views.length-1);
 else if(next>=current.views.length&&l<course.lessons.length-1)go(course.lessons[l+1].id,0);
 else if(next>=0&&next<current.views.length)go(current.id,next);
}
function sessionRecord(){if(!session)return;state.sessions[session.id]={lesson:session.lesson,kind:timer.kind,ms:Math.floor(timer.elapsed),problemMs:Math.floor(timer.problemMs),at:session.at};}
function paintTimer(){
 $('#clock').textContent=format(timer.remaining);$('#start').textContent=timer.running?tr('En curso','Running'):timer.remaining<timer.duration&&timer.remaining>0?tr('Continuar','Resume'):tr('Iniciar 25 min','Start 25 min');
 $('#start').disabled=timer.running||lockPending;$('#pause').disabled=!timer.running;
 $('#timer-label').textContent=timer.kind==='break'?tr('Pausa','Break'):timer.kind==='practice'?tr('Práctica','Practice'):tr('Estudio','Study');
 $('#problem').setAttribute('aria-pressed',String(timer.problem));
 const t=totals(state,current?.id);$('#timer-status').textContent=tr('Registrado en esta lección: ','Recorded in this lesson: ')+format(t.study+t.practice)+tr(' · Bloqueo (parte de ese tiempo): ',' · Problem (part of that time): ')+format(t.problem)+tr(' · Al ocultar la página se pausa. La práctica fuera del navegador se declara aparte.',' · Hiding the page pauses it. Work outside the browser is declared separately.');
}
function unlock(){if(releaseLock){releaseLock();releaseLock=null;}}
function halt(reason='manual'){
 pause(timer,performance.now(),reason);sessionRecord();save();unlock();paintTimer();
}
async function begin(kind=null){
 if(timer.running||lockPending)return;
 if(Object.keys(state.sessions).length>=1000){toast(tr('Exporta el registro y comienza uno nuevo: límite de sesiones alcanzado.','Export the record and begin a new one: session limit reached.'));return;}
 const requested=kind||(['environment','lab','evidence','recovery'].includes(current.views[index].kind)?'practice':'study');
 const activate=()=>{
  if(kind||!session||timer.remaining===0||session.lesson!==current.id){timer=createTimer(requested,requested==='break'?300000:1500000);session={id:crypto.randomUUID(),lesson:current.id,at:Date.now()};}
  idleAt=performance.now();start(timer,idleAt);paintTimer();
 };
 if(navigator.locks){
  lockPending=true;paintTimer();
  try{await navigator.locks.request(KEY+'.timer',{ifAvailable:true},async lock=>{
   lockPending=false;
   if(!lock){toast(tr('Hay un temporizador activo en otra pestaña. Páusalo primero.','A timer is active in another tab. Pause it first.'));paintTimer();return;}
   activate();await new Promise(resolve=>releaseLock=resolve);
  });}catch{lockPending=false;toast(tr('No se pudo reservar el temporizador. No se ha iniciado.','Could not reserve the timer. It was not started.'));paintTimer();}
 }else{toast(tr('Este navegador no coordina temporizadores entre pestañas: utiliza solo una.','This browser cannot coordinate tab timers: use only one tab.'));activate();}
}
function show(title,body){halt('panel');$('#panel-title').textContent=title;$('#panel-body').innerHTML=body;$('#panel').showModal();}
function environment(){
 show(tr('Prepara un entorno compatible','Prepare a compatible environment'),`<label for="host-choice">${tr('Tu equipo','Your device')}</label><select id="host-choice">${HOSTS.map(x=>`<option value="${x}" ${x===host?'selected':''}>${esc(x)}</option>`).join('')}</select><label for="target-choice"> ${tr('Quiero practicar','I want to practice')}</label><select id="target-choice">${TARGETS.map(x=>`<option value="${x}" ${x===current.group?'selected':''}>${groupName(x)}</option>`).join('')}</select><div id="environment-result"></div>`);
 const update=()=>{host=$('#host-choice').value;const g=guidance(host,$('#target-choice').value,lang);$('#environment-result').innerHTML=g.notes.map(x=>'<div class="callout">'+esc(x)+'</div>').join('')+'<h3>'+tr('Preparación paso a paso','Step-by-step preparation')+'</h3><ol>'+g.steps.map(x=>'<li>'+p(x)+'</li>').join('')+'</ol><h3>'+tr('Descargas y compatibilidad oficiales','Official downloads and compatibility')+'</h3><ul class="source-list">'+g.links.map(x=>'<li>'+link(x[1],x[0])+'</li>').join('')+'</ul>'+p(tr('Guía documental revisada el 21-09-2026. Verifica versiones y licencias antes de instalar. Esta web no instala nada.','Documentation guidance reviewed 2026-09-21. Check versions and licensing before installation. This website installs nothing.'));};
 $('#host-choice').addEventListener('change',update);$('#target-choice').addEventListener('change',update);update();
}
function dashboard(){
 sessionRecord();const t=totals(state),today=totals(state,null,new Date()),c=completion(state,current),estimate=remainingEstimate(state,current),left=Math.max(0,state.goal*25*60000-today.study-today.practice);
 const stats=[[tr('Estudio registrado','Recorded study'),format(t.study)],[tr('Práctica registrada','Recorded practice'),format(t.practice)],[tr('Pausas registradas','Recorded breaks'),format(t.break)],[tr('Tiempo de bloqueo (subconjunto)','Problem time (subset)'),format(t.problem)],[tr('Práctica externa declarada','Declared external practice'),format(t.declared)],[tr('Objetivo de foco pendiente hoy','Remaining focus goal today'),format(left)]];
 const flagged=current.views.filter(v=>['review','blocked'].includes(state.marks[v.id]?.status));
 show(tr('Tu estudio, tus evidencias','Your study, your evidence'),
 p(tr('El tiempo no acredita aprendizaje. Solo medimos intervalos que inicias; desconocemos el tiempo real fuera del registro. No existe una métrica de «tiempo que no has estudiado».','Time does not prove learning. We record only intervals you start; actual time outside the record is unknown. There is no metric of “time you did not study”.'))+
 '<div class="stats">'+stats.map(([a,b])=>'<div class="stat"><strong>'+b+'</strong><span>'+a+'</span></div>').join('')+'</div>'+
 `<p><label for="goal">${tr('Plan de hoy: ciclos de 25 minutos','Today’s plan: 25-minute cycles')}</label> <select id="goal">${[1,2,3,4,6,8].map(n=>`<option ${n===state.goal?'selected':''}>${n}</option>`).join('')}</select></p>`+
 p(tr('Sugerencia inicial: un ciclo para entender y otro para practicar y explicar. Haz una pausa de 5 minutos cuando termines un ciclo; empieza el siguiente manualmente. Adaptar el ritmo es correcto. Instalar una VM puede requerir una sesión aparte.','Starting suggestion: one cycle to understand and another to practice and explain. Take a five-minute break after a cycle; start the next manually. Adjusting the pace is valid. Installing a VM may need a separate session.'))+
 `<h3>${esc(current.title)}</h3><p>${c.done}/${c.total} · ${tr('Orientación para los puntos pendientes','Guidance for remaining points')}: ${estimate.min}–${estimate.max} min.</p>`+
 p(tr('Esta estimación es una hipótesis de planificación (1–4 minutos por vista; 3–10 por paso de laboratorio), no una predicción validada. Un bloqueo de entorno puede necesitar más.','This estimate is a planning assumption (1–4 minutes per view; 3–10 per lab step), not a validated prediction. An environment blocker can take longer.'))+
 '<ul>'+flagged.map(v=>`<li><a href="#${current.id}/${current.views.indexOf(v)}" data-close-panel>${esc(v.title)}</a> · ${esc(state.marks[v.id].status)}</li>`).join('')+'</ul>'+
 '<details><summary>'+tr('Registrar trabajo fuera del navegador','Record work outside the browser')+'</summary>'+p(tr('Se conserva como declarado, separado del tiempo medido. No registres la misma sesión dos veces.','Stored as declared, separate from measured time. Do not record the same session twice.'))+`<label for="external-min">${tr('Minutos (1–240)','Minutes (1–240)')}</label> <input id="external-min" type="number" min="1" max="240" value="25"> `+button('external-add',tr('Añadir a esta lección','Add to this lesson'))+'</details>'+
 '<h3>'+tr('Guardar y continuar en otro dispositivo','Save and continue on another device')+'</h3>'+p(tr('El aula tiene su propio registro; no modifica el progreso del campus anterior. Comparte el enlace para abrir la lección; exporta/importa JSON para trasladar marcas y tiempos. No hay cuenta, OTP ni sincronización automática. Las notas de problema solo se descargan aparte y no se incluyen.','This classroom has its own record; it does not modify earlier campus progress. Share the link to open a lesson; export/import JSON to transfer marks and times. No account, OTP or automatic synchronization. Problem notes are downloaded separately and are not included.'))+
 `<label><input type="checkbox" id="remember" ${persistent?'checked':''}> ${tr('Guardar este registro en este navegador','Save this record in this browser')}</label>`+
 '<div class="actions">'+button('export',tr('Exportar mi registro','Export my record'))+button('reset',tr('Reiniciar registro','Reset record'))+'</div>'+`<p><label for="import">${tr('Importar copia JSON (máximo 1 MiB)','Import JSON record (1 MiB maximum)')}</label> <input id="import" type="file" accept="application/json,.json"></p>`+
 (recoveryRaw?'<div class="callout">'+tr('La copia anterior no es válida; se conserva sin sobrescribir.','The previous copy is invalid; it remains untouched.')+button('recover',tr('Descargar copia original','Download original copy'))+'</div>':'')+
 '<div id="import-preview"></div>');
 $('#goal').addEventListener('change',e=>{state.goal=Number(e.target.value);save();});
 $('#remember').addEventListener('change',e=>{persistent=e.target.checked;if(persistent)save();else try{localStorage.removeItem(KEY);}catch{};});
 $('#export').onclick=()=>download('smartkea-os-study.json',JSON.stringify(state,null,2));
 $('#reset').onclick=()=>{if(confirm(tr('¿Reiniciar solo el registro de esta aula? Exporta primero para conservarlo.','Reset only this classroom record? Export first to retain it.'))){state=empty();recoveryRaw=null;session=null;timer=createTimer();try{localStorage.removeItem(KEY);}catch{}$('#panel').close();go('OS-C01',0);render();}};
 $('#external-add').onclick=()=>{const n=Number($('#external-min').value);if(!Number.isInteger(n)||n<1||n>240||Object.keys(state.sessions).length>=1000){toast(tr('Valor no válido.','Invalid value.'));return;}state.sessions[crypto.randomUUID()]={lesson:current.id,kind:'declared',ms:n*60000,problemMs:0,at:Date.now()};save();dashboard();};
 $('#recover')?.addEventListener('click',()=>download('os-record-recovery.txt',recoveryRaw,'text/plain'));
 $('#import').addEventListener('change',async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>1048576)throw Error('SIZE');pendingImport=parse(await f.text(),course);$('#import-preview').innerHTML=p(tr('Copia validada. Las marcas se combinan por fecha y las sesiones duplicadas por identificador.','Validated record. Marks merge by timestamp and duplicate sessions by ID.'))+button('confirm-import',tr('Combinar esta copia','Merge this copy'));$('#confirm-import').onclick=()=>{try{state=parse(JSON.stringify(merge(state,pendingImport)),course);pendingImport=null;save();$('#panel').close();render();toast(tr('Copia combinada.','Record merged.'));}catch{toast(tr('La combinación excede los límites; conserva ambas copias.','The merge exceeds limits; keep both records.'));}};}catch{pendingImport=null;$('#import-preview').textContent=tr('Copia rechazada; no se han cambiado tus datos.','Record rejected; your data was not changed.');}});
}
async function load(next){
 halt('language');const seq=++loading;
 try{const response=await fetch('course.'+next+'.json',{credentials:'omit'});if(!response.ok)throw Error('LOAD');const data=await response.json();if(seq!==loading)return;course=data;lang=next;
  if(!current){const raw=readSaved();if(raw)try{state=parse(raw,course);persistent=true;}catch{recoveryRaw=raw;}
   try{const localRoute=sessionStorage.getItem(KEY+'.route');if(localRoute&&/^OS-[CLWA]\d{2}\/\d+$/.test(localRoute))state.last=localRoute;}catch{}
  }
  const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url);render();
 }catch{toast(tr('No se pudo cargar el aula. Usa la lectura continua; no se ha borrado el registro.','Could not load the classroom. Use continuous reading; the record was not deleted.'));}
}
function presentation(on){
 halt('presentation');document.body.classList.toggle('presentation',on);$('#outline').inert=on;$('#assistant').inert=on;$('.top').inert=on;
 if(!on&&document.fullscreenElement)document.exitFullscreen?.().catch(()=>{});render();$('#present').focus();
}
async function fullscreen(){
 if(!document.body.classList.contains('presentation'))presentation(true);
 try{if(document.fullscreenElement)await document.exitFullscreen();else if($('#lesson').requestFullscreen)await $('#lesson').requestFullscreen();else throw Error('UNAVAILABLE');}
 catch{toast(tr('Presentación a ventana completa activa; pantalla completa nativa no disponible.','Full-window presentation is active; native fullscreen is unavailable.'));}
}
$('#menu').onclick=()=>{const open=document.body.classList.toggle('menu-open');$('#menu').setAttribute('aria-expanded',String(open));};
$('#language').onchange=e=>load(e.target.value);
$('#prev').onclick=()=>move(-1);$('#next').onclick=()=>move(1);
$('#present').onclick=()=>presentation(!document.body.classList.contains('presentation'));
$('#fullscreen').onclick=fullscreen;
$('#help').onclick=environment;$('#dashboard').onclick=dashboard;
$('#close-panel').onclick=()=>$('#panel').close();
$('#panel-body').addEventListener('click',e=>{if(e.target.closest('[data-close-panel]'))$('#panel').close();});
$('#start').onclick=()=>begin();$('#pause').onclick=()=>halt();$('#break').onclick=()=>{halt();begin('break');};
$('#problem').onclick=()=>{tick(timer,performance.now());timer.problem=!timer.problem;$('#coach').open=true;paintTimer();if(!timer.running)toast(tr('Inicia el foco para registrar el tiempo de problema.','Start focus to record problem time.'));};
$('#hint').onclick=()=>{const items=[tr('Primero: '+current.lab.symptom,'First: '+current.lab.symptom),current.lab.hint,tr('Formula dos hipótesis y una prueba de bajo impacto. Si no tienes el entorno o permiso, detente y solicita el laboratorio adecuado.','Form two hypotheses and one low-impact check. If the environment or authorization is missing, stop and request the appropriate lab.')];$('#hint-text').textContent=items[Math.min(hints++,2)];};
$('#download-note').onclick=()=>download('problema-'+current.id+'.txt',current.id+'\n'+$('#problem-note').value,'text/plain');
$('#content').addEventListener('click',async e=>{
 const answer=e.target.closest('[data-answer]');if(answer){const q=current.views[index].quiz;quizPassed=Number(answer.dataset.answer)===q.correct;$('#answer-feedback').textContent=(quizPassed?tr('Correcto. ','Correct. '):tr('Revisa la explicación. ','Review the explanation. '))+q.explanation;$('#done').disabled=!quizPassed;if(!quizPassed){state.marks[current.views[index].id]={status:'review',at:Date.now()};save();}return;}
 if(e.target.id==='copy-code'){try{await navigator.clipboard.writeText(current.views[index].code);toast(tr('Copiado. Revisa contexto y permisos antes de ejecutar.','Copied. Review context and permissions before execution.'));}catch{toast(tr('Selecciona y copia el bloque manualmente.','Select and copy the block manually.'));}}
 if(e.target.id==='open-environment')environment();
 if(e.target.id==='template')download('entrega-'+current.id+'.md',`# ${current.id} · ${current.title}\n\n${tr('Objetivo / impacto:\nEntorno y versiones:\nEsperado / observado:\nHipótesis y comprobación:\nResultado y evidencia:\nAlternativas y decisión:\nLímites:\nRecuperación:\nResponsable y siguiente acción:\nUso de IA y verificación independiente:','Goal / impact:\nEnvironment and versions:\nExpected / observed:\nHypothesis and check:\nResult and evidence:\nOptions and decision:\nLimits:\nRecovery:\nOwner and next action:\nAI use and independent verification:')}\n`,'text/markdown');
});
$('#marks').addEventListener('click',e=>{if(['done','review','blocked'].includes(e.target.id))mark(e.target.id);});
$('#share').onclick=async()=>{const u=new URL(location.href);u.search='';u.searchParams.set('lang',lang);u.hash=current.id+'/'+index;try{if(navigator.share)await navigator.share({title:current.title,url:u.href});else{await navigator.clipboard.writeText(u.href);toast(tr('Enlace copiado; no incluye progreso.','Link copied; it does not include progress.'));}}catch{toast(tr('Comparte la dirección del navegador. El registro se traslada con JSON.','Share the browser address. Transfer the record with JSON.'));}};
window.addEventListener('hashchange',()=>{halt('navigation');document.body.classList.remove('menu-open');$('#menu').setAttribute('aria-expanded','false');render();});
window.addEventListener('storage',e=>{if(e.key!==KEY||!e.newValue||!course)return;try{state=merge(state,parse(e.newValue,course));if(!timer.running&&!$('#panel').open)render();}catch{/* Preserve the local record. */}});
document.addEventListener('visibilitychange',()=>{if(document.hidden)halt('hidden');});
window.addEventListener('pagehide',()=>halt('pagehide'));
for(const name of ['pointerdown','keydown','scroll','touchstart'])document.addEventListener(name,()=>idleAt=performance.now(),{passive:true,capture:true});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'&&document.body.classList.contains('presentation')){e.preventDefault();presentation(false);return;}
 if($('#panel').open||['INPUT','TEXTAREA','SELECT','BUTTON'].includes(document.activeElement?.tagName)||document.activeElement?.isContentEditable)return;
 if(document.body.classList.contains('presentation')){if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();move(1);}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();move(-1);}if(e.key==='Home'){e.preventDefault();go(current.id,0);}if(e.key==='End'){e.preventDefault();go(current.id,current.views.length-1);}if(e.key.toLowerCase()==='f'){e.preventDefault();fullscreen();}}
});
setInterval(()=>{
 if(!timer.running)return;
 const now=performance.now();
 if(timer.kind!=='break'&&now-idleAt>300000){halt('idle');toast(tr('Foco pausado tras 5 minutos sin interacción. Puedes continuar o declarar trabajo externo.','Focus paused after 5 minutes without interaction. Resume or declare external work.'));return;}
 tick(timer,now);sessionRecord();paintTimer();
 if(now-lastSave>15000){save();lastSave=now;}
 if(!timer.running){save();unlock();toast(timer.reason==='finished'?tr('Intervalo terminado. El siguiente empieza solo cuando tú lo inicies.','Interval finished. The next starts only when you start it.'):tr('Intervalo pausado por suspensión o salto del reloj. Ese hueco no se suma.','Interval paused after suspension or a clock gap. That gap is not counted.'));}
},1000);
load(lang);
