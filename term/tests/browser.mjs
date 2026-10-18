/** Functional acceptance against the loopback preview; never opens a real ttyd. */
import {createRequire} from 'node:module';
import {mkdir,readFile} from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
let playwright;
try{playwright=require('playwright');}catch{playwright=require(path.join(process.env.TERM_TEST_NODE_MODULES||process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/tmp/term-qa/node_modules','playwright'));}
const base=process.env.TERM_TEST_URL||'http://127.0.0.1:8791/fundamentos-ciberseguridad/term/';
const parsed=new URL(base);
if(!['127.0.0.1','localhost'].includes(parsed.hostname))throw new Error('Browser acceptance is limited to a local preview.');
const out=new URL('../qa/',import.meta.url);await mkdir(out,{recursive:true});
const data=JSON.parse(await readFile(new URL('../dist/course.json',import.meta.url),'utf8'));
async function openLesson(page,id,phase='practica',index=0){
 await page.goto(base+`#/leccion/${id}/${phase}/${index}`);
 // Hash navigation can leave the previous lesson visible until hashchange renders.
 await page.locator(`.lesson-page[data-lesson-id="${id}"][data-phase="${phase}"][data-index="${index}"]`).waitFor();
}
async function assertNoOverflow(page,engine,width,phase){
 const layout=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
 if(layout.scroll>layout.width+1){
  layout.elements=await page.evaluate(()=>[...document.querySelectorAll('body *')].map(el=>({element:el.tagName,id:el.id,className:el.getAttribute('class'),right:el.getBoundingClientRect().right})).filter(el=>el.right>innerWidth+1).slice(0,12));
  await page.screenshot({path:new URL(`overflow-${engine}-${width}-${phase}.png`,out).pathname,fullPage:true,animations:'disabled'});
 }
 assert.ok(layout.scroll<=layout.width+1,`Horizontal overflow in ${engine} at ${width} (${phase}): ${JSON.stringify(layout)}`);
}
const engines=(process.env.TERM_TEST_BROWSERS||'chromium').split(',');
const results=[];
for(const engine of engines){
 const browser=await playwright[engine].launch({headless:true});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),errors=[],external=[];
  page.on('pageerror',e=>errors.push(e.message));
  await context.route('**/*',route=>{const u=new URL(route.request().url());if(['127.0.0.1','localhost'].includes(u.hostname)||['data:','blob:'].includes(u.protocol))return route.continue();external.push(u.origin);return route.abort();});
  const response=await page.goto(base);assert.equal(response.status(),200);assert.match(response.headers()['content-security-policy'],/frame-src 'none'/);
  await page.getByRole('heading',{name:'Aprende a pensar en terminal.'}).waitFor();assert.equal(await page.locator('.module-card').count(),16);
  await page.screenshot({path:new URL('desktop-'+engine+'.png',out).pathname,fullPage:false,animations:'disabled'});
  await page.getByRole('link',{name:'Empezar la primera lección'}).click();await page.locator('.lesson-page[data-lesson-id="m01-l01"]').waitFor();
  const currentHash=new URL(page.url()).hash;
  await page.locator('#skip-content').focus();await page.locator('#skip-content').press('Enter');
  assert.equal(new URL(page.url()).hash,currentHash,'Skip link must preserve the current lesson route.');
  assert.equal(await page.locator('.lesson-page').getAttribute('data-lesson-id'),'m01-l01');
  assert.equal(await page.evaluate(()=>document.activeElement?.id),'main');
  await page.getByRole('link',{name:/Practicar$/}).click();await page.locator('.code-box').waitFor();
  assert.match(await page.locator('.demo-label').textContent(),/no ejecuta comandos/);
  await page.locator('.copy-button').click();await page.locator('#toast').waitFor({state:'visible'});
  await page.locator('#step-verified').check();
  await page.getByRole('button',{name:'Terminal real',exact:true}).click();assert.match(await page.locator('#desk-content').textContent(),/Ninguna máquina/);assert.equal(await page.locator('iframe').count(),0);
  await page.getByRole('link',{name:/Resolver$/}).click();await page.locator('#lesson-note').fill('Evidencia sintética <img src=x onerror=alert(1)>');
  await page.locator('#evidence-level').selectOption('explained');await page.reload();await page.locator('#lesson-note').waitFor();assert.match(await page.locator('#lesson-note').inputValue(),/<img/);assert.equal(await page.locator('.lesson-article img').count(),0);
  await page.getByRole('link',{name:/Comprobar$/}).click();await page.locator('[data-answer]').first().click();await page.locator('.feedback').waitFor();
  await page.getByRole('button',{name:'Marcar como aprendida',exact:true}).click();await page.getByRole('button',{name:'Lección completada'}).waitFor();
  await page.goto(base+'#/progreso');await page.locator('.metrics-grid').waitFor();assert.match(await page.locator('.metrics-grid').textContent(),/1 \/ 48/);
  const exported=page.waitForEvent('download');await page.getByRole('button',{name:'Exportar progreso',exact:true}).click();const download=await exported;const exportedPath=new URL('progress-'+engine+'.json',out).pathname;await download.saveAs(exportedPath);const raw=await readFile(exportedPath,'utf8');assert.equal(JSON.parse(raw).completed.length,1);
  await page.locator('#import-file').setInputFiles({name:'test.json',mimeType:'application/json',buffer:Buffer.from(raw)});await page.locator('#confirm-dialog').waitFor({state:'visible'});await page.locator('#confirm-accept').click();
  await page.goto(base+'#/comandos/curl');await page.locator('.command-result').first().waitFor();assert.ok(await page.locator('.command-result').count()>0);
  await page.goto(base+'#/buscar/permisos');await page.locator('.search-result').first().waitFor();
  // Rendering every lesson catches schema drift across independently authored modules.
  for(const module of data.modules){for(const lesson of module.lessons){
    await openLesson(page,lesson.id);assert.equal(await page.locator('.code-box code').textContent(),lesson.steps[0].command);
  }}
  await openLesson(page,'m12-l01');await page.screenshot({path:new URL('practice-'+engine+'.png',out).pathname,fullPage:false,animations:'disabled'});
  for(const width of [390,320,768]){
    await page.setViewportSize({width,height:844});await openLesson(page,'m01-l01','test');
    await assertNoOverflow(page,engine,width,'test');
    assert.equal(await page.locator('#sidebar').evaluate(sidebar=>sidebar.inert),true);
    assert.equal(await page.locator('#sidebar').getAttribute('aria-hidden'),'true');
    assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'false');
    await page.locator('.top-progress').focus();await page.keyboard.press('Tab');
    assert.equal(await page.locator('#sidebar').evaluate(sidebar=>sidebar.contains(document.activeElement)),false,'Closed mobile navigation must not receive keyboard focus.');
    await page.locator('#menu-toggle').click();
    assert.equal(await page.locator('#sidebar').evaluate(sidebar=>sidebar.inert),false);
    assert.equal(await page.locator('#sidebar').getAttribute('aria-hidden'),null);
    assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'true');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#sidebar').evaluate(sidebar=>sidebar.inert),true);
    assert.equal(await page.evaluate(()=>document.activeElement?.id),'menu-toggle');
    await page.locator('#menu-toggle').click();await page.locator('.sidebar .side-link').first().click();await page.getByRole('heading',{name:'Aprende a pensar en terminal.'}).waitFor();
    assert.equal(await page.locator('#sidebar').evaluate(sidebar=>sidebar.inert),true);
    await openLesson(page,'m01-l01');
    await assertNoOverflow(page,engine,width,'practica');
    if(width===390)await page.screenshot({path:new URL('mobile-'+engine+'.png',out).pathname,fullPage:false,animations:'disabled'});
  }
  // Resize alone must synchronize the accessibility state in both directions.
  await page.setViewportSize({width:1440,height:1000});
  await page.waitForFunction(()=>!document.querySelector('#sidebar').inert&&document.querySelector('#menu-toggle').getAttribute('aria-expanded')==='true');
  assert.equal(await page.locator('#menu-toggle').getAttribute('aria-label'),'Contraer menú');
  await page.setViewportSize({width:390,height:844});
  await page.waitForFunction(()=>document.querySelector('#sidebar').inert&&document.querySelector('#menu-toggle').getAttribute('aria-expanded')==='false');
  assert.equal(await page.locator('#menu-toggle').getAttribute('aria-label'),'Expandir menú');
  await page.locator('#clock-open').click();await page.locator('#timer-toggle').click();assert.equal(await page.locator('#timer-toggle').textContent(),'Pausar');await page.locator('#timer-reset').click();assert.equal(await page.locator('#timer-display').textContent(),'25:00');await page.locator('#timer-dialog [data-close-dialog]').click();
  await page.goto(base+'manual.html');await page.locator('.manual-module').first().waitFor();assert.equal(await page.locator('.manual-lesson').count(),48);assert.equal(await page.locator('.manual-quiz').count(),96);
  const bad=await page.request.get(base+'missing-asset.js');assert.equal(bad.status(),404);
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);results.push({engine,status:'passed',lessons:48,widths:[1440,768,390,320],externalRequests:0});
  await context.close();
 }finally{await browser.close();}
}
console.log(JSON.stringify({status:'passed',results},null,2));
