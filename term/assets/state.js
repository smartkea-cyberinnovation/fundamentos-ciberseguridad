/** Local learning records. Imported input is validated and never becomes HTML. */
export const COURSE_ID = 'smartkea-term-linux';
export const STORAGE_KEY = 'smartkea.term.progress.v1';
export const MAX_IMPORT_BYTES = 2_000_000;
export const EMPTY = () => ({schema:1, course:COURSE_ID, completed:[], steps:{}, quiz:{}, notes:{}, evidence:{}, lastLesson:'m01-l01', updatedAt:null});
const plain = value => value !== null && typeof value === 'object' && !Array.isArray(value) && Object.getPrototypeOf(value) === Object.prototype;
const own = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

export function validateProgress(input, lessons, strict = true) {
  if (!plain(input) || input.schema !== 1 || input.course !== COURSE_ID) throw new Error('Este archivo no es un progreso de TERM Linux compatible.');
  const map = new Map(lessons.map(l => [l.id, l]));
  const out = EMPTY();
  if (!Array.isArray(input.completed)) throw new Error('Lista de lecciones no válida.');
  out.completed = [...new Set(input.completed.filter(id => typeof id === 'string' && map.has(id)))];
  for (const key of ['steps','quiz','notes','evidence']) {
    if (input[key] !== undefined && !plain(input[key])) throw new Error('Estructura de progreso no válida: '+key);
    for (const id of map.keys()) {
      if (!input[key] || !own(input[key], id)) continue;
      const v = input[key][id], lesson = map.get(id);
      if (key === 'notes') {
        if (typeof v !== 'string' || v.length > 6000) throw new Error('Las notas deben ser texto de hasta 6.000 caracteres.');
        out.notes[id] = v;
      } else if (key === 'steps') {
        if (!Array.isArray(v) || v.some(n => !Number.isInteger(n) || n < 0 || n >= lesson.steps.length)) throw new Error('Un paso no existe en el curso.');
        out.steps[id] = [...new Set(v)];
      } else if (key === 'quiz') {
        if (!plain(v)) throw new Error('Respuestas no válidas.');
        const answers = {};
        for (let q = 0; q < lesson.quiz.length; q++) {
          if (!own(v,String(q))) continue;
          if (!Number.isInteger(v[q]) || v[q] < 0 || v[q] >= lesson.quiz[q].options.length) throw new Error('Opción de respuesta no válida.');
          answers[q] = v[q];
        }
        out.quiz[id] = answers;
      } else if (key === 'evidence') {
        if (!['pending','practiced','explained'].includes(v)) throw new Error('Estado de evidencia no válido.');
        out.evidence[id] = v;
      }
    }
  }
  if (typeof input.lastLesson === 'string' && map.has(input.lastLesson)) out.lastLesson = input.lastLesson;
  if (typeof input.updatedAt === 'string' && input.updatedAt.length < 40 && Number.isFinite(Date.parse(input.updatedAt))) out.updatedAt = input.updatedAt;
  if (strict && input.completed.some(id => !map.has(id))) throw new Error('Hay lecciones desconocidas; comprueba la edición del curso.');
  return out;
}

export function loadProgress(storage, lessons) {
  try {
    const raw = storage.getItem(STORAGE_KEY);
    if (!raw) return {state: EMPTY(), error:null};
    if (raw.length > MAX_IMPORT_BYTES) throw new Error('Progreso demasiado grande.');
    return {state:validateProgress(JSON.parse(raw), lessons, false),error:null};
  } catch { return {state:EMPTY(),error:'No se pudo leer el progreso guardado. Puedes importar tu copia; el archivo previo no se ha borrado.'}; }
}

export function parseImport(text, lessons) {
  if (new TextEncoder().encode(text).byteLength > MAX_IMPORT_BYTES) throw new Error('El archivo supera los 2 MB.');
  return validateProgress(JSON.parse(text), lessons);
}
export function metrics(state, lessons) {
  let answered = 0, correct = 0, practiced = 0, steps = 0;
  for (const l of lessons) {
    if (['practiced','explained'].includes(state.evidence[l.id])) practiced++;
    steps += (state.steps[l.id] || []).length;
    l.quiz.forEach((q, index) => { const a = state.quiz[l.id]?.[index]; if (Number.isInteger(a)) { answered++; if (a === q.answer) correct++; } });
  }
  const total = lessons.length;
  return {completed:state.completed.length,total,percent:total ? Math.round(state.completed.length/total*100):0,answered,correct,accuracy:answered ? Math.round(correct/answered*100):0,practiced,steps};
}
export function normalizeSearch(value) {return String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();}
export function searchLessons(lessons, query) {
  const q = normalizeSearch(query).slice(0,120);
  if (!q) return [];
  return lessons.filter(l => normalizeSearch([l.title,l.summary,...l.objectives,...l.steps.map(s=>s.command)].join(' ')).includes(q));
}
export function validLabUrl(config, campusOrigin) {
  if (!config || !config.url || !Array.isArray(config.allowedOrigins)) return null;
  try {
    const u = new URL(config.url);
    if (u.protocol !== 'https:' || u.origin === campusOrigin || u.username || u.password || u.search || u.hash) return null;
    if (!config.allowedOrigins.includes(u.origin)) return null;
    return u.href;
  } catch {return null;}
}
