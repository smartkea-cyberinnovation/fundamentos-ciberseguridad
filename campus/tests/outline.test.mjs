import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

// Exercise the real filter in the current single-file app without booting its
// navigation, storage, network requests or lesson views.
const source=readFileSync(new URL('../assets/app.js',import.meta.url),'utf8');
const start=source.indexOf('function filterOutline(){');
const end=source.indexOf('\nfunction ',start+1);
assert.ok(start>=0 && end>start,'The application filter must be available to test.');
const filterSource=source.slice(start,end);

function outline(language){
  const descriptions=language==='en'
    ? ['Linux files and shell','Text tools. Prerequisite: M05.','Permissions. Prerequisite: M05.','macOS. Prerequisites: M03 and M05.']
    : ['Linux: shell y ficheros','Herramientas de texto. Entrada: M05.','Permisos. Entrada: M05.','macOS. Entrada: M03, M05.'];
  const rows=['M05','M06','M07','M20'].map((module,index)=>({dataset:{module,
    search:`${module} ${descriptions[index]}`,block:index===3?'macos':'linux',status:index===0?'started':'pending'},hidden:false}));
  const fields={
    '#outline-query':{value:''},'#outline-block':{value:'all'},'#outline-status':{value:'all'},
    '#outline-count':{textContent:''},'#outline-empty':{hidden:true},
  };
  const context={q:selector=>fields[selector],main:{querySelectorAll:()=>rows},
    normalize:value=>String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase(),t:value=>value};
  runInNewContext(filterSource,context);
  return {fields,filter:context.filterOutline,visible:()=>rows.filter(row=>!row.hidden).map(row=>row.dataset.module)};
}

for(const language of ['es','en']){
  test(`${language}: a module ID selects its own row, not prerequisite references`,()=>{
    const view=outline(language);
    for(const query of ['M05','m05','  M05  ']){
      view.fields['#outline-query'].value=query;view.filter();
      assert.deepEqual(view.visible(),['M05']);
      assert.equal(view.fields['#outline-empty'].hidden,true);
      assert.match(view.fields['#outline-count'].textContent,/^1 \/ 32 /);
    }
  });
  test(`${language}: an exact module ID still respects block and progress filters`,()=>{
    const view=outline(language);view.fields['#outline-query'].value='M05';
    view.fields['#outline-block'].value='macos';view.filter();assert.deepEqual(view.visible(),[]);
    view.fields['#outline-block'].value='linux';view.fields['#outline-status'].value='pending';
    view.filter();assert.deepEqual(view.visible(),[]);
    view.fields['#outline-status'].value='started';view.filter();assert.deepEqual(view.visible(),['M05']);
  });
  test(`${language}: text search, no matches and reset retain their behavior`,()=>{
    const view=outline(language);view.fields['#outline-query'].value='macos';
    view.filter();assert.deepEqual(view.visible(),['M20']);
    view.fields['#outline-query'].value='M99';view.filter();
    assert.deepEqual(view.visible(),[]);assert.equal(view.fields['#outline-empty'].hidden,false);
    view.fields['#outline-query'].value='';view.filter();
    assert.deepEqual(view.visible(),['M05','M06','M07','M20']);
  });
}
