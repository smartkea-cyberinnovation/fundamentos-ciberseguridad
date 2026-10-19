/** User-facing data-loss regressions. Run against loopback only, never real ttyd. */
import {createRequire} from 'node:module';
import path from 'node:path';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
let playwright;
try{playwright=require('playwright');}catch{playwright=require(path.join(process.env.TERM_TEST_NODE_MODULES||'/tmp/term-qa/node_modules','playwright'));}
const base=process.env.TERM_TEST_URL||'http://127.0.0.1:8791/fundamentos-ciberseguridad/term/';
if(!['127.0.0.1','localhost'].includes(new URL(base).hostname))throw Error('Loopback preview required.');
const key='smartkea.term.progress.v1';
const results=[];
for(const engine of (process.env.TERM_TEST_BROWSERS||'chromium').split(',')){
 const browser=await playwright[engine].launch({headless:true});
 try{
  const context=await browser.newContext(),page=await context.newPage(),errors=[];
  context.on('page',p=>p.on('pageerror',e=>errors.push(e.message)));
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('.module-card').first().waitFor();
  await page.evaluate(k=>localStorage.setItem(k,'{broken-original'),key);
  await page.goto(base+'#/leccion/m02-l01/reto/0');await page.reload();
  await page.locator('#storage-warning').waitFor({state:'visible'});
  await page.locator('#lesson-note').fill('recoverable memory note');
  await page.waitForFunction(()=>document.querySelector('#note-status')?.textContent.includes('esta sesión'));
  assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),'{broken-original');
  const download=page.waitForEvent('download');await page.locator('#export-stored').click();
  const original=await download;assert.equal(original.suggestedFilename(),'SmartKEA-TERM-original.json');
  const stream=await original.createReadStream(),parts=[];for await(const chunk of stream)parts.push(chunk);
  assert.equal(Buffer.concat(parts).toString(),'{broken-original');
  // The user can recover deliberately; subsequent edits must still persist.
  await page.goto(base+'#/progreso');await page.locator('#reset-progress').click();await page.locator('#confirm-accept').click();
  await page.waitForFunction(k=>localStorage.getItem(k)?.startsWith('{"schema"'),key);
  await page.goto(base+'#/leccion/m01-l01/reto/0');await page.locator('#lesson-note').fill('first saved note');
  await page.waitForFunction(k=>JSON.parse(localStorage.getItem(k)).notes['m01-l01']==='first saved note',key);
  const second=await context.newPage();await second.goto(base+'#/leccion/m01-l01/reto/0');await second.locator('#lesson-note').waitFor();
  await page.locator('#lesson-note').fill('newer first-tab note');
  await page.waitForFunction(k=>JSON.parse(localStorage.getItem(k)).notes['m01-l01']==='newer first-tab note',key);
  await second.locator('#storage-warning').waitFor({state:'visible'});await second.locator('#lesson-note').fill('stale tab note');
  await second.waitForFunction(()=>document.querySelector('#note-status')?.textContent.includes('esta sesión'));
  assert.equal(await page.evaluate(k=>JSON.parse(localStorage.getItem(k)).notes['m01-l01'],key),'newer first-tab note');
  await second.locator('#reload-stored').click();await second.locator('#confirm-accept').click();
  await second.waitForFunction(()=>document.querySelector('#lesson-note')?.value==='newer first-tab note');
  await second.locator('#lesson-note').fill('continued after recovery');
  await second.waitForFunction(k=>JSON.parse(localStorage.getItem(k)).notes['m01-l01']==='continued after recovery',key);
  // Simulate quota exhaustion without changing the original saved bytes.
  await second.evaluate(()=>{Storage.prototype.setItem=function(){throw new DOMException('Quota exceeded','QuotaExceededError');};});
  await second.locator('#lesson-note').fill('quota memory note');
  await second.waitForFunction(()=>document.querySelector('#note-status')?.textContent.includes('esta sesión'));
  assert.equal(await second.evaluate(k=>JSON.parse(localStorage.getItem(k)).notes['m01-l01'],key),'continued after recovery');
  await second.setViewportSize({width:320,height:844});
  assert.equal(await second.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);
  assert.deepEqual(errors,[]);await context.close();results.push({engine,status:'passed',cases:['corruption','original-export','reset','two-tabs','reload-and-edit','quota','320px']});
 }finally{await browser.close();}
}
console.log(JSON.stringify({status:'passed',results},null,2));
