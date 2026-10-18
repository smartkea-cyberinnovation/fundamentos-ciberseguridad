/** Pure, dependency-free engine for the formative computing quiz.
 * Correctness is always derived from the current bank, never from stored scores.
 * The saved attempt is a convenience for study, not evidence of certification.
 */
export const BANK_SIZE = 100;
export const SESSION_LENGTH = 20;
export const STORAGE_KEY = 'fundamentos-ciberseguridad:exam:v1';
const STATE_SCHEMA = 1;
const MAX_STORED_LENGTH = 50_000;
const DIFFICULTIES = new Set(['basico', 'intermedio', 'aplicacion']);
const isRecord = value => value !== null && typeof value === 'object' && !Array.isArray(value)
  && [Object.prototype, null].includes(Object.getPrototypeOf(value));
const has = (object, key) => Object.hasOwn(object, key);

function requireValue(condition, message) {
  if (!condition) throw new Error(message);
}

function cleanText(value, maximum, name) {
  requireValue(typeof value === 'string' && value.trim().length > 0 && value.length <= maximum,
    `El campo ${name} debe contener texto válido.`);
  return value.trim();
}

/** Validate and copy the entire public bank before allowing an attempt. */
export function validateBank(input) {
  requireValue(isRecord(input) && input.schemaVersion === 1, 'Formato del banco no compatible.');
  const version = cleanText(input.version, 64, 'versión');
  const title = cleanText(input.title, 200, 'título');
  requireValue(Array.isArray(input.topics) && input.topics.length > 0 && input.topics.length <= BANK_SIZE,
    'El banco debe definir sus temas.');
  const topicIds = new Set();
  const topics = input.topics.map(topic => {
    requireValue(isRecord(topic) && typeof topic.id === 'string'
      && /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$/.test(topic.id) && !topicIds.has(topic.id),
    'Los identificadores de tema deben ser válidos y únicos.');
    topicIds.add(topic.id);
    return Object.freeze({ id: topic.id, title: cleanText(topic.title, 200, 'tema') });
  });
  requireValue(Array.isArray(input.questions) && input.questions.length === BANK_SIZE,
    `El banco debe contener exactamente ${BANK_SIZE} preguntas.`);
  const questionIds = new Set();
  const questions = input.questions.map(question => {
    requireValue(isRecord(question) && typeof question.id === 'string'
      && /^INF-\d{3}$/.test(question.id) && !questionIds.has(question.id),
    'Los identificadores de pregunta deben ser válidos y únicos.');
    questionIds.add(question.id);
    requireValue(topicIds.has(question.topic), `Tema desconocido en ${question.id}.`);
    requireValue(DIFFICULTIES.has(question.difficulty), `Dificultad inválida en ${question.id}.`);
    requireValue(Array.isArray(question.options) && question.options.length === 4,
      `${question.id} debe tener cuatro opciones.`);
    const optionIds = new Set();
    const optionTexts = new Set();
    const options = question.options.map(option => {
      requireValue(isRecord(option) && ['a', 'b', 'c', 'd'].includes(option.id) && !optionIds.has(option.id),
        `Las opciones de ${question.id} deben tener identificadores únicos de a a d.`);
      const text = cleanText(option.text, 2000, 'opción');
      const comparisonText = text.normalize('NFKC').toLocaleLowerCase('es').replace(/\s+/g, ' ');
      requireValue(!optionTexts.has(comparisonText), `Hay opciones repetidas en ${question.id}.`);
      optionIds.add(option.id);
      optionTexts.add(comparisonText);
      return Object.freeze({ id: option.id, text });
    });
    requireValue(optionIds.has(question.correctOptionId),
      `${question.id} debe identificar exactamente una opción correcta.`);
    requireValue(isRecord(question.study) && typeof question.study.url === 'string'
      && /^\.\.\/#\/(?:recurso|modulo)\/[A-Za-z0-9_-]{1,64}$/.test(question.study.url),
    `El enlace de estudio de ${question.id} debe apuntar a un recurso interno del campus.`);
    return Object.freeze({
      id: question.id,
      topic: question.topic,
      difficulty: question.difficulty,
      prompt: cleanText(question.prompt, 3000, 'pregunta'),
      options: Object.freeze(options),
      correctOptionId: question.correctOptionId,
      explanation: cleanText(question.explanation, 5000, 'explicación'),
      study: Object.freeze({ label: cleanText(question.study.label, 200, 'enlace de estudio'), url: question.study.url }),
    });
  });
  return Object.freeze({ schemaVersion: 1, version, title, topics: Object.freeze(topics), questions: Object.freeze(questions) });
}

/** Revision checksum, not a signature or anti-tampering mechanism. */
export function bankRevision(bank) {
  const source = JSON.stringify(bank);
  let checksum = 0x811c9dc5;
  for (let index = 0; index < source.length; index += 1) {
    checksum = Math.imul(checksum ^ source.charCodeAt(index), 0x01000193) >>> 0;
  }
  return `${bank.version}:${checksum.toString(16).padStart(8, '0')}`;
}

/** Uniform bounded integer with rejection sampling to avoid modulo bias. */
export function cryptoRandomInt(maxExclusive, cryptoSource = globalThis.crypto) {
  requireValue(Number.isSafeInteger(maxExclusive) && maxExclusive > 0 && maxExclusive <= 0x100000000,
    'Límite de aleatoriedad inválido.');
  requireValue(cryptoSource && typeof cryptoSource.getRandomValues === 'function',
    'Este navegador no ofrece la aleatoriedad necesaria para preparar el intento.');
  const limit = 0x100000000 - (0x100000000 % maxExclusive);
  const buffer = new Uint32Array(1);
  do { cryptoSource.getRandomValues(buffer); } while (buffer[0] >= limit);
  return buffer[0] % maxExclusive;
}

/** Fisher–Yates; never changes the input and preserves the identity of options. */
export function shuffle(items, randomInt = cryptoRandomInt) {
  const copy = items.slice();
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const selected = randomInt(index + 1);
    requireValue(Number.isInteger(selected) && selected >= 0 && selected <= index,
      'El generador devolvió un índice inválido.');
    [copy[index], copy[selected]] = [copy[selected], copy[index]];
  }
  return copy;
}

function isoTime(value) {
  const date = value instanceof Date ? value : new Date(value);
  requireValue(Number.isFinite(date.getTime()), 'Fecha del intento inválida.');
  return date.toISOString();
}

function validStoredTime(value) {
  return typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value)
    && Number.isFinite(Date.parse(value)) && new Date(value).toISOString() === value;
}

export function createAttempt(bank, { randomInt = cryptoRandomInt, now = new Date() } = {}) {
  const selected = shuffle(bank.questions, randomInt).slice(0, SESSION_LENGTH);
  return {
    schemaVersion: STATE_SCHEMA,
    bankRevision: bankRevision(bank),
    questionIds: selected.map(question => question.id),
    optionOrders: Object.fromEntries(selected.map(question => [question.id, shuffle(question.options.map(option => option.id), randomInt)])),
    answers: {},
    currentIndex: 0,
    status: 'active',
    startedAt: isoTime(now),
    finishedAt: null,
  };
}

function findQuestion(bank, attempt, questionId) {
  requireValue(attempt.questionIds.includes(questionId), 'La pregunta no pertenece a este intento.');
  const question = bank.questions.find(item => item.id === questionId);
  requireValue(Boolean(question), 'La pregunta no pertenece a este banco.');
  return question;
}

/** Idempotent correction: an answered question or closed attempt cannot score again. */
export function answerQuestion(bank, attempt, questionId, optionId) {
  const question = findQuestion(bank, attempt, questionId);
  requireValue(question.options.some(option => option.id === optionId), 'La opción no pertenece a esta pregunta.');
  if (attempt.status !== 'active' || has(attempt.answers, questionId)) return attempt;
  return { ...attempt, answers: { ...attempt.answers, [questionId]: optionId } };
}

export function navigateAttempt(attempt, index) {
  requireValue(Number.isInteger(index) && index >= 0 && index < attempt.questionIds.length,
    'La posición está fuera del intento.');
  return index === attempt.currentIndex ? attempt : { ...attempt, currentIndex: index };
}

export function finishAttempt(attempt, now = new Date()) {
  if (attempt.status === 'finished') return attempt;
  const timestamp = isoTime(now);
  return { ...attempt, status: 'finished', finishedAt: timestamp < attempt.startedAt ? attempt.startedAt : timestamp };
}

/** Stable identity from existing immutable fields; saved v1 attempts need no migration. */
export function sameAttempt(left, right) {
  return Boolean(left && right && left.bankRevision === right.bankRevision && left.startedAt === right.startedAt
    && Array.isArray(left.questionIds) && Array.isArray(right.questionIds)
    && left.questionIds.length === right.questionIds.length
    && left.questionIds.every((id, index) => id === right.questionIds[index]
      && Array.isArray(left.optionOrders?.[id]) && Array.isArray(right.optionOrders?.[id])
      && left.optionOrders[id].join(',') === right.optionOrders[id].join(',')));
}

/** Stored answers win conflicts; a committed finish never accepts late answers. */
export function reconcileAttempts(stored, proposed) {
  requireValue(sameAttempt(stored, proposed), 'No se pueden combinar intentos distintos.');
  if (stored.status === 'finished') return stored;
  const answers = { ...stored.answers };
  for (const [id, optionId] of Object.entries(proposed.answers)) {
    if (!has(answers, id)) answers[id] = optionId;
  }
  return { ...proposed, answers };
}

/** Build a fresh trusted shape. Reject malformed, stale or inconsistent persisted state. */
export function restoreAttempt(bank, candidate) {
  if (!isRecord(candidate) || candidate.schemaVersion !== STATE_SCHEMA || candidate.bankRevision !== bankRevision(bank)) return null;
  const known = new Map(bank.questions.map(question => [question.id, question]));
  if (!Array.isArray(candidate.questionIds) || candidate.questionIds.length !== SESSION_LENGTH
    || candidate.questionIds.some(id => typeof id !== 'string' || !known.has(id))
    || new Set(candidate.questionIds).size !== SESSION_LENGTH) return null;
  if (!isRecord(candidate.optionOrders) || Object.keys(candidate.optionOrders).length !== SESSION_LENGTH
    || !isRecord(candidate.answers) || Object.keys(candidate.answers).length > SESSION_LENGTH) return null;
  for (const id of candidate.questionIds) {
    if (!has(candidate.optionOrders, id)) return null;
    const order = candidate.optionOrders[id];
    if (!Array.isArray(order) || order.length !== 4 || new Set(order).size !== 4
      || order.some(optionId => !known.get(id).options.some(option => option.id === optionId))) return null;
  }
  for (const [id, optionId] of Object.entries(candidate.answers)) {
    if (!candidate.questionIds.includes(id) || !known.get(id).options.some(option => option.id === optionId)) return null;
  }
  if (!Number.isInteger(candidate.currentIndex) || candidate.currentIndex < 0 || candidate.currentIndex >= SESSION_LENGTH
    || !['active', 'finished'].includes(candidate.status) || !validStoredTime(candidate.startedAt)) return null;
  if (candidate.status === 'active' && candidate.finishedAt !== null) return null;
  if (candidate.status === 'finished' && (!validStoredTime(candidate.finishedAt) || candidate.finishedAt < candidate.startedAt)) return null;
  return {
    schemaVersion: STATE_SCHEMA,
    bankRevision: candidate.bankRevision,
    questionIds: candidate.questionIds.slice(),
    optionOrders: Object.fromEntries(candidate.questionIds.map(id => [id, candidate.optionOrders[id].slice()])),
    answers: Object.fromEntries(Object.entries(candidate.answers)),
    currentIndex: candidate.currentIndex,
    status: candidate.status,
    startedAt: candidate.startedAt,
    finishedAt: candidate.finishedAt,
  };
}

export function summarizeAttempt(bank, attempt) {
  const byTopic = new Map(bank.topics.map(topic => [topic.id, { ...topic, total: 0, correct: 0, incorrect: 0, unanswered: 0 }]));
  const items = attempt.questionIds.map((id, index) => {
    const question = findQuestion(bank, attempt, id);
    const selectedOptionId = has(attempt.answers, id) ? attempt.answers[id] : null;
    const correct = selectedOptionId === question.correctOptionId;
    const topic = byTopic.get(question.topic);
    topic.total += 1;
    topic[selectedOptionId === null ? 'unanswered' : correct ? 'correct' : 'incorrect'] += 1;
    return { index, question, selectedOptionId, correct };
  });
  const correct = items.filter(item => item.correct).length;
  const unanswered = items.filter(item => item.selectedOptionId === null).length;
  return {
    total: items.length,
    answered: items.length - unanswered,
    correct,
    incorrect: items.length - correct - unanswered,
    unanswered,
    grade: correct * 10 / items.length,
    byTopic: [...byTopic.values()].filter(topic => topic.total > 0),
    items,
  };
}

/** Read/merge/write is one origin-wide Web Lock transaction, not a localStorage CAS.
 * Without coordination, callers keep an in-memory attempt and never write shared data.
 */
export function createPersistence(storageAccessor = () => globalThis.localStorage,
  locksAccessor = () => globalThis.navigator?.locks) {
  function load(bank) {
    let raw;
    try { raw = storageAccessor().getItem(STORAGE_KEY); }
    catch { return { status: 'unavailable', attempt: null }; }
    if (raw === null) return { status: 'empty', attempt: null };
    if (typeof raw !== 'string' || raw.length > MAX_STORED_LENGTH) return { status: 'invalid', attempt: null };
    try {
      const attempt = restoreAttempt(bank, JSON.parse(raw));
      return { status: attempt ? 'restored' : 'invalid', attempt };
    } catch { return { status: 'invalid', attempt: null }; }
  }
  function canCoordinate() {
    try { return typeof locksAccessor()?.request === 'function'; }
    catch { return false; }
  }
  return {
    load,
    canCoordinate,
    async commit(bank, proposed, { replace = false, expected = null } = {}) {
      const candidate = restoreAttempt(bank, proposed);
      requireValue(Boolean(candidate), 'El intento que se quiere guardar es inválido.');
      let localAttempt = candidate;
      const unavailable = () => ({ status: 'unavailable', attempt: localAttempt });
      if (!canCoordinate()) return unavailable();
      try {
        return await locksAccessor().request(`${STORAGE_KEY}:write`, { mode: 'exclusive' }, async () => {
          const current = load(bank);
          if (current.status === 'unavailable') return unavailable();
          const stored = current.attempt;
          if (replace ? !(sameAttempt(stored, expected) || (!stored && !expected)) : !sameAttempt(stored, candidate)) {
            return { status: 'superseded', attempt: stored };
          }
          const next = replace ? candidate : reconcileAttempts(stored, candidate);
          localAttempt = next;
          const raw = JSON.stringify(next);
          if (raw.length > MAX_STORED_LENGTH) return unavailable();
          if (raw !== JSON.stringify(stored)) {
            storageAccessor().setItem(STORAGE_KEY, raw);
            // Keep the lock across a task boundary: Firefox checkpoints localStorage at task end.
            await new Promise(resolve => {
              const channel = new MessageChannel();
              channel.port1.onmessage = () => {
                channel.port1.close(); channel.port2.close(); resolve();
              };
              channel.port2.postMessage(null);
            });
          }
          return { status: 'saved', attempt: next };
        });
      } catch { return unavailable(); }
    },
  };
}
