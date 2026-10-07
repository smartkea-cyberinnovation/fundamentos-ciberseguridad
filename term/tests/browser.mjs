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
  await page.screenshot({path:new URL('desktop-'+engine+'.png',out).pathname,fullPage:false});
  await page.getByRole('link',{name:'Empezar la primera lección'}).click();await page.locator('.lesson-article h2').waitFor();
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
    await page.goto(base+`#/leccion/${lesson.id}/practica/0`);await page.locator('.code-box').waitFor();assert.equal(await page.locator('.code-box code').textContent(),lesson.steps[0].command);
  }}
  await page.goto(base+'#/leccion/m12-l01/practica/0');await page.locator('.code-box').waitFor();await page.screenshot({path:new URL('practice-'+engine+'.png',out).pathname,fullPage:false});
  for(const width of [390,320,768]){
    await page.setViewportSize({width,height:844});await page.goto(base+'#/leccion/m01-l01/test/0');await page.locator('.quiz-options').waitFor();
    const layout=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(layout.scroll<=layout.width+1,`Horizontal overflow at ${width}: ${layout.scroll}`);
    await page.locator('#menu-toggle').click();await page.locator('.sidebar .side-link').first().click();await page.getByRole('heading',{name:'Aprende a pensar en terminal.'}).waitFor();
    await page.goto(base+'#/leccion/m01-l01/practica/0');await page.locator('.code-box').waitFor();
    const check=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1);assert.equal(check,true);
    if(width===390)await page.screenshot({path:new URL('mobile-'+engine+'.png',out).pathname,fullPage:false});
  }
  await page.locator('#clock-open').click();await page.locator('#timer-toggle').click();assert.equal(await page.locator('#timer-toggle').textContent(),'Pausar');await page.locator('#timer-reset').click();assert.equal(await page.locator('#timer-display').textContent(),'25:00');await page.locator('#timer-dialog [data-close-dialog]').click();
  await page.goto(base+'manual.html');await page.locator('.manual-module').first().waitFor();assert.equal(await page.locator('.manual-lesson').count(),48);assert.equal(await page.locator('.manual-quiz').count(),96);
  const bad=await page.request.get(base+'missing-asset.js');assert.equal(bad.status(),404);
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);results.push({engine,status:'passed',lessons:48,widths:[1440,768,390,320],externalRequests:0});
  await context.close();
 }finally{await browser.close();}
}
console.log(JSON.stringify({status:'passed',results},null,2));
