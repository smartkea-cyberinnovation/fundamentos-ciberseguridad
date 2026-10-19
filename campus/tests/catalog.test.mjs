import test from 'node:test';
import assert from 'node:assert/strict';
import {matches, normalise} from '../assets/catalog.js';
const row={search:'M05 Teoría de permisos Linux',block:'linux',status:'pending'};
const all={query:'',block:'all',status:'all'};
test('empty filters retain all rows',()=>assert.ok(matches(row,all)));
test('independent terms and accent-insensitive search',()=>assert.ok(matches(row,{...all,query:'TEORIA linux'})));
test('all terms must match',()=>assert.ok(!matches(row,{...all,query:'linux windows'})));
test('block filter is exact',()=>assert.ok(!matches(row,{...all,block:'windows'})));
test('progress filter distinguishes pending and complete',()=>assert.ok(!matches(row,{...all,status:'complete'})));
test('combined filters work',()=>assert.ok(matches(row,{query:'M05',block:'linux',status:'pending'})));
test('html-like input is inert text',()=>assert.ok(!matches(row,{...all,query:'<img src=x>'})));
test('normalise handles accented input',()=>assert.equal(normalise('Práctica'),'practica'));

test('complete module ID does not match prerequisite mentions',()=>assert.ok(!matches({module:'M06',search:'M06 Text; prerequisite M05',block:'linux',status:'pending'},{...all,query:'M05'})));
test('exact ID is case-insensitive and combines with text',()=>assert.ok(matches({...row,module:'M05'},{...all,query:'m05 permisos'})));
test('partial ID remains a free-text query',()=>assert.ok(matches(row,{...all,query:'m0'})));
