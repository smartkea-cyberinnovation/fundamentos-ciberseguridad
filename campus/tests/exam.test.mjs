import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  BANK_SIZE, SESSION_LENGTH, STORAGE_KEY, validateBank, bankRevision, cryptoRandomInt,
  shuffle, createAttempt, answerQuestion, navigateAttempt, finishAttempt,
  restoreAttempt, summarizeAttempt, createPersistence,
} from '../exam/model.mjs';

function fixture() {
  return {
    schemaVersion: 1, version: 'test.1', title: 'Banco sintético para pruebas',
    topics: [{ id: 'T01', title: 'Sistemas' }, { id: 'T02', title: 'Redes' }],
    questions: Array.from({ length: BANK_SIZE }, (_, index) => ({
      id: `INF-${String(index + 1).padStart(3, '0')}`, topic: index % 2 ? 'T02' : 'T01',
      difficulty: ['basico', 'intermedio', 'aplicacion'][index % 3], prompt: `Pregunta sintética ${index + 1}`,
      options: ['a', 'b', 'c', 'd'].map(id => ({ id, text: `Opción ${id} de la pregunta ${index + 1}` })),
      correctOptionId: ['a', 'b', 'c', 'd'][index % 4], explanation: `Explicación sintética ${index + 1}.`,
      study: { label: 'Mapa de estudio', url: '../#/recurso/D26' },
    })),
  };
}

function randomSource(seed = 37) {
  let state = seed;
  return maximum => {
    state = (Math.imul(1664525, state) + 1013904223) >>> 0;
    return state % maximum;
  };
}

const bank = validateBank(fixture());
const options = () => ({ randomInt: randomSource(), now: new Date('2026-10-18T10:00:00.000Z') });
const copy = value => JSON.parse(JSON.stringify(value));
const questionAt = (attempt, index) => bank.questions.find(question => question.id === attempt.questionIds[index]);

test('el banco real contiene 100 preguntas válidas, cuatro opciones y una solución por pregunta', () => {
  const actual = validateBank(JSON.parse(readFileSync(new URL('../../formacion/introduccion-informatica/banco-preguntas.json', import.meta.url), 'utf8')));
  assert.equal(actual.questions.length, BANK_SIZE);
  assert.equal(new Set(actual.questions.map(question => question.id)).size, BANK_SIZE);
  assert.ok(actual.questions.every(question => question.options.filter(option => option.id === question.correctOptionId).length === 1));
  assert.ok(actual.topics.every(topic => actual.questions.some(question => question.topic === topic.id)));
});

test('validación copia y congela el banco, y rechaza bancos incompletos o preguntas repetidas', () => {
  const raw = fixture();
  const safe = validateBank(raw);
  raw.questions[0].prompt = 'Cambio posterior';
  assert.notEqual(safe.questions[0].prompt, raw.questions[0].prompt);
  assert.ok(Object.isFrozen(safe.questions[0].options));
  const short = fixture(); short.questions.pop();
  assert.throws(() => validateBank(short), /exactamente 100/);
  const repeated = fixture(); repeated.questions[1].id = repeated.questions[0].id;
  assert.throws(() => validateBank(repeated), /únicos/);
});

test('validación rechaza soluciones inexistentes, opciones duplicadas, temas y enlaces inseguros', () => {
  for (const mutation of [
    raw => { raw.questions[0].correctOptionId = 'e'; },
    raw => { raw.questions[0].correctOptionId = ['a', 'b']; },
    raw => { raw.questions[0].options[1].id = 'a'; },
    raw => { raw.questions[0].options[1].text = `  ${raw.questions[0].options[0].text.toUpperCase()}  `; },
    raw => { raw.questions[0].options.pop(); },
    raw => { raw.questions[0].topic = 'unknown'; },
    raw => { raw.questions[0].study.url = 'javascript:alert(1)'; },
    raw => { raw.questions[0].study.url = 'https://outside.example/'; },
    raw => { raw.questions[0].study.url = '../#/recurso/D26\n'; },
    raw => { raw.questions[0].explanation = ''; },
  ]) {
    const raw = fixture(); mutation(raw);
    assert.throws(() => validateBank(raw));
  }
});

test('Fisher–Yates no muta los datos y conserva todas las identidades', () => {
  const initial = ['a', 'b', 'c', 'd'];
  const shuffled = shuffle(initial, () => 0);
  assert.deepEqual(initial, ['a', 'b', 'c', 'd']);
  assert.deepEqual(shuffled, ['b', 'c', 'd', 'a']);
  assert.deepEqual([...shuffled].sort(), [...initial].sort());
  assert.throws(() => shuffle(initial, () => 8), /índice inválido/);
});

test('aleatoriedad criptográfica rechaza la cola sesgada del rango Uint32', () => {
  const values = [0xffffffff, 17];
  let calls = 0;
  const crypto = { getRandomValues(buffer) { buffer[0] = values[calls++]; return buffer; } };
  assert.equal(cryptoRandomInt(10, crypto), 7);
  assert.equal(calls, 2);
  assert.throws(() => cryptoRandomInt(10, null), /aleatoriedad/);
  assert.throws(() => cryptoRandomInt(0, crypto), /Límite/);
});

test('cada intento contiene 20 preguntas distintas y opciones reordenadas sin cambiar la solución', () => {
  let differentQuestionOrders = false;
  let differentOptionOrders = false;
  const original = JSON.stringify(bank);
  const baseline = createAttempt(bank, options());
  for (let seed = 1; seed <= 30; seed += 1) {
    const attempt = createAttempt(bank, { ...options(), randomInt: randomSource(seed) });
    assert.equal(attempt.questionIds.length, SESSION_LENGTH);
    assert.equal(new Set(attempt.questionIds).size, SESSION_LENGTH);
    if (attempt.questionIds.join() !== baseline.questionIds.join()) differentQuestionOrders = true;
    for (const id of attempt.questionIds) {
      const question = bank.questions.find(item => item.id === id);
      const ordered = attempt.optionOrders[id];
      assert.deepEqual([...ordered].sort(), ['a', 'b', 'c', 'd']);
      assert.equal(ordered.filter(optionId => optionId === question.correctOptionId).length, 1);
      if (ordered.join() !== 'a,b,c,d') differentOptionOrders = true;
    }
  }
  assert.ok(differentQuestionOrders);
  assert.ok(differentOptionOrders);
  assert.equal(JSON.stringify(bank), original);
});

test('la primera respuesta queda fijada; volver, repetir eventos o elegir otra no vuelve a puntuar', () => {
  const initial = createAttempt(bank, options());
  const question = questionAt(initial, 0);
  const wrong = question.options.find(option => option.id !== question.correctOptionId).id;
  const answered = answerQuestion(bank, initial, question.id, wrong);
  assert.deepEqual(initial.answers, {});
  assert.equal(summarizeAttempt(bank, answered).incorrect, 1);
  assert.strictEqual(answerQuestion(bank, answered, question.id, question.correctOptionId), answered);
  assert.strictEqual(answerQuestion(bank, answered, question.id, wrong), answered);
  const returned = navigateAttempt(navigateAttempt(answered, 5), 0);
  assert.equal(summarizeAttempt(bank, returned).answered, 1);
  assert.equal(summarizeAttempt(bank, returned).correct, 0);
});

test('puntuación sobre 10 y desglose temático incluyen errores y preguntas pendientes', () => {
  let attempt = createAttempt(bank, options());
  const first = questionAt(attempt, 0);
  const second = questionAt(attempt, 1);
  attempt = answerQuestion(bank, attempt, first.id, first.correctOptionId);
  attempt = answerQuestion(bank, attempt, second.id, second.options.find(option => option.id !== second.correctOptionId).id);
  const summary = summarizeAttempt(bank, attempt);
  assert.equal(summary.grade, 0.5);
  assert.equal(summary.total, 20);
  assert.equal(summary.answered, 2);
  assert.equal(summary.correct, 1);
  assert.equal(summary.incorrect, 1);
  assert.equal(summary.unanswered, 18);
  for (const key of ['total', 'correct', 'incorrect', 'unanswered']) {
    assert.equal(summary.byTopic.reduce((total, topic) => total + topic[key], 0), summary[key]);
  }
  assert.equal(summary.items.filter(item => !item.correct).length, 19);
});

test('20 aciertos equivalen a 10; un intento finalizado ya no acepta respuestas', () => {
  let perfect = createAttempt(bank, options());
  for (const id of perfect.questionIds) {
    const question = bank.questions.find(item => item.id === id);
    perfect = answerQuestion(bank, perfect, id, question.correctOptionId);
  }
  assert.equal(summarizeAttempt(bank, perfect).grade, 10);
  const untouched = createAttempt(bank, options());
  const closed = finishAttempt(untouched, '2026-10-18T11:00:00.000Z');
  const question = questionAt(closed, 0);
  assert.strictEqual(answerQuestion(bank, closed, question.id, question.correctOptionId), closed);
  assert.strictEqual(finishAttempt(closed), closed);
  assert.equal(summarizeAttempt(bank, closed).unanswered, 20);
  assert.equal(untouched.status, 'active');
});

test('navegación y respuestas rechazan preguntas, opciones o posiciones ajenas al intento', () => {
  const attempt = createAttempt(bank, options());
  const absent = bank.questions.find(question => !attempt.questionIds.includes(question.id));
  assert.throws(() => answerQuestion(bank, attempt, absent.id, absent.correctOptionId));
  assert.throws(() => answerQuestion(bank, attempt, attempt.questionIds[0], 'e'));
  for (const invalid of [-1, 20, 0.5, NaN, '0']) assert.throws(() => navigateAttempt(attempt, invalid));
  assert.equal(navigateAttempt(attempt, 19).currentIndex, 19);
});

test('reanudación conserva orden, respuestas y posición; ignora supuestas puntuaciones almacenadas', () => {
  const initial = createAttempt(bank, options());
  const question = questionAt(initial, 0);
  const active = navigateAttempt(answerQuestion(bank, initial, question.id, question.correctOptionId), 13);
  const candidate = { ...copy(active), correct: 100, grade: 10, certified: true };
  const restored = restoreAttempt(bank, candidate);
  assert.deepEqual(restored, active);
  assert.notStrictEqual(restored.questionIds, candidate.questionIds);
  assert.equal(summarizeAttempt(bank, restored).grade, 0.5);
  assert.ok(!Object.hasOwn(restored, 'certified'));
  const finished = finishAttempt(active, '2026-10-18T11:00:00.000Z');
  assert.deepEqual(restoreAttempt(bank, copy(finished)), finished);
});

test('estado persistido hostil o inconsistente no se reanuda', () => {
  const original = createAttempt(bank, options());
  for (const mutation of [
    state => { state.questionIds[1] = state.questionIds[0]; },
    state => { state.questionIds[0] = '__proto__'; },
    state => { state.questionIds.pop(); },
    state => { state.optionOrders[state.questionIds[0]] = ['a', 'a', 'c', 'd']; },
    state => { state.optionOrders[state.questionIds[0]] = ['a', 'b', 'c', 'e']; },
    state => { delete state.optionOrders[state.questionIds[1]]; },
    state => { state.answers[state.questionIds[0]] = 'e'; },
    state => { state.answers = JSON.parse('{"__proto__":{"polluted":true}}'); },
    state => { state.answers = []; },
    state => { state.currentIndex = 20; },
    state => { state.currentIndex = '1'; },
    state => { state.startedAt = '2026-02-30T10:00:00.000Z'; },
    state => { state.finishedAt = '2026-10-18T11:00:00.000Z'; },
    state => { state.status = 'finished'; },
    state => { state.status = 'finished'; state.finishedAt = '2026-10-17T11:00:00.000Z'; },
    state => { state.schemaVersion = 2; },
  ]) {
    const altered = copy(original); mutation(altered);
    assert.equal(restoreAttempt(bank, altered), null);
  }
  assert.equal(restoreAttempt(bank, Object.create(original)), null);
  assert.equal(restoreAttempt(bank, null), null);
  assert.equal({}.polluted, undefined);
});

test('una revisión del banco invalida el intento anterior aunque el editor no cambie su versión', () => {
  const oldAttempt = createAttempt(bank, options());
  const revisedSource = fixture();
  revisedSource.questions[0].explanation += ' Aclaración nueva.';
  const revised = validateBank(revisedSource);
  assert.notEqual(bankRevision(bank), bankRevision(revised));
  assert.equal(restoreAttempt(revised, oldAttempt), null);
});

test('almacenamiento denegado, cuota agotada o JSON corrupto no impiden practicar', () => {
  const attempt = createAttempt(bank, options());
  const denied = createPersistence(() => { throw new Error('SecurityError'); });
  assert.deepEqual(denied.load(bank), { status: 'unavailable', attempt: null });
  assert.equal(denied.save(attempt), false);
  const full = createPersistence(() => ({ getItem: () => null, setItem() { throw new Error('QuotaExceededError'); } }));
  assert.equal(full.load(bank).status, 'empty');
  assert.equal(full.save(attempt), false);
  for (const bad of ['not-json', '{}', 'null', '[1]', 'x'.repeat(50_001)]) {
    const broken = createPersistence(() => ({ getItem: () => bad }));
    assert.equal(broken.load(bank).status, 'invalid');
  }
  const question = questionAt(attempt, 0);
  assert.equal(summarizeAttempt(bank, answerQuestion(bank, attempt, question.id, question.correctOptionId)).correct, 1);
});

test('el intento utiliza su propia clave y no modifica el progreso general del campus', () => {
  const courseKey = 'fundamentos-ciberseguridad:progress:v1';
  const store = new Map([[courseKey, 'progreso existente']]);
  const persistence = createPersistence(() => ({ getItem: key => store.get(key) ?? null, setItem: (key, value) => store.set(key, value) }));
  const attempt = createAttempt(bank, options());
  assert.equal(persistence.save(attempt), true);
  assert.equal(store.get(courseKey), 'progreso existente');
  assert.deepEqual([...store.keys()].sort(), [courseKey, STORAGE_KEY].sort());
  assert.deepEqual(persistence.load(bank).attempt, attempt);
});
