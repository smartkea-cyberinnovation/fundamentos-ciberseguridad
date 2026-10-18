import {
  BANK_SIZE, SESSION_LENGTH, validateBank, createAttempt, answerQuestion,
  navigateAttempt, finishAttempt, summarizeAttempt, createPersistence,
} from './model.mjs';

const main = document.querySelector('#main');
const restartButton = document.querySelector('#restart-attempt');
const storageNote = document.querySelector('#storage-note');
const confirmation = document.querySelector('#confirm-dialog');
const persistence = createPersistence();
const difficultyLabels = { basico: 'Básico', intermedio: 'Intermedio', aplicacion: 'Aplicación' };
const numberFormat = new Intl.NumberFormat('es-ES', { maximumFractionDigits: 2 });
let bank;
let attempt = null;
let view = 'home';
let reviewIndices = [];
let reviewPosition = 0;
let storageAvailable = true;
let pendingAction = null;
let confirmationOrigin = null;
let loading = false;

// Bank text is always inserted as text. No HTML, scripts or external resources are accepted.
function element(tag, text = '', className = '') {
  const item = document.createElement(tag);
  if (text) item.textContent = text;
  if (className) item.className = className;
  return item;
}

function button(id, label, action, secondary = false) {
  const item = element('button', label, `button${secondary ? ' secondary' : ''}`);
  item.type = 'button';
  if (id) item.id = id;
  item.addEventListener('click', action);
  return item;
}

function studyLink(question) {
  const link = element('a', `Repasar: ${question.study.label}`, 'study-link');
  link.href = question.study.url;
  return link;
}

function focusOn(id) {
  requestAnimationFrame(() => {
    const target = document.getElementById(id);
    if (target) target.focus();
  });
}

function mount(content, focusId) {
  main.replaceChildren(content);
  restartButton.hidden = !attempt || view === 'home';
  if (focusId) focusOn(focusId);
}

function showNotice(message) {
  storageNote.textContent = message;
  storageNote.hidden = !message;
}

function persist() {
  storageAvailable = persistence.save(attempt);
  showNotice(storageAvailable ? '' : 'El navegador no permite guardar este intento. Puedes practicar; se conservará mientras mantengas esta página abierta.');
}

function requestConfirmation(title, description, actionLabel, action) {
  if (typeof confirmation.showModal !== 'function') {
    if (window.confirm(`${title}\n\n${description}`)) action();
    return;
  }
  confirmationOrigin = document.activeElement;
  pendingAction = action;
  document.querySelector('#confirm-title').textContent = title;
  document.querySelector('#confirm-description').textContent = description;
  document.querySelector('#accept-confirmation').textContent = actionLabel;
  confirmation.returnValue = '';
  confirmation.showModal();
  document.querySelector('#cancel-confirmation').focus();
}

document.querySelector('#cancel-confirmation').addEventListener('click', () => confirmation.close('cancelled'));
document.querySelector('#accept-confirmation').addEventListener('click', () => {
  const action = pendingAction;
  pendingAction = null;
  confirmation.close('confirmed');
  if (action) action();
});
confirmation.addEventListener('close', () => {
  pendingAction = null;
  if (confirmation.returnValue !== 'confirmed' && confirmationOrigin?.isConnected) confirmationOrigin.focus();
});
document.querySelector('.skip-link').addEventListener('click', event => {
  event.preventDefault();
  main.focus();
});

function startAttempt() {
  try {
    const next = createAttempt(bank);
    attempt = next;
    view = 'attempt';
    persist();
    renderQuestion({ focus: true });
  } catch {
    showNotice('No se ha podido preparar la selección aleatoria. Vuelve a cargar la página en un navegador actualizado e inténtalo de nuevo.');
  }
}

function requestNewAttempt() {
  if (attempt?.status === 'active') {
    const result = summarizeAttempt(bank, attempt);
    requestConfirmation('¿Empezar otro intento?',
      `Tienes ${result.answered} de ${result.total} preguntas respondidas en el intento actual. Al empezar otro, se sustituirán esas respuestas por una nueva selección de ${SESSION_LENGTH} preguntas.`,
      'Sustituir y empezar', startAttempt);
  } else startAttempt();
}
restartButton.addEventListener('click', requestNewAttempt);

function statistic(value, label, id) {
  const wrapper = element('div', '', 'fact');
  const count = element('strong', String(value));
  if (id) count.id = id;
  wrapper.append(count, element('span', label));
  return wrapper;
}

function renderHome(focus = false) {
  view = 'home';
  const layout = element('div', '', 'home-layout');
  const copy = element('section', '', 'home-copy');
  const heading = element('h1', 'Introducción a la informática');
  heading.id = 'welcome-heading';
  heading.tabIndex = -1;
  copy.append(element('p', 'Autoevaluación · SmartKEA Campus', 'eyebrow'), heading,
    element('h2', 'Comprueba lo que sabes y entiende cada respuesta.'),
    element('p', 'Practica con una selección diferente en cada intento. Recibe la corrección al elegir una opción, descubre el porqué y vuelve al contenido que necesitas repasar.', 'lead'));
  const facts = element('div', '', 'facts');
  facts.append(statistic(BANK_SIZE, 'preguntas en el banco'), statistic(SESSION_LENGTH, 'preguntas por intento'), statistic('4', 'opciones · una válida'));
  copy.append(facts);
  if (attempt) {
    const result = summarizeAttempt(bank, attempt);
    const saved = element('section', '', 'resume-panel');
    saved.append(element('h2', attempt.status === 'active' ? 'Tu intento sigue aquí' : 'Tu último resultado'));
    saved.append(element('p', attempt.status === 'active'
      ? `${result.answered} de ${result.total} respondidas. Continúa con las mismas preguntas, opciones y respuestas.`
      : `${result.correct} aciertos de ${result.total} · ${numberFormat.format(result.grade)} sobre 10. Puedes revisar las explicaciones.`));
    const actions = element('div', '', 'button-row');
    actions.append(button('resume-attempt', attempt.status === 'active' ? 'Reanudar intento' : 'Ver último resultado', () => {
      if (attempt.status === 'active') { view = 'attempt'; renderQuestion({ focus: true }); }
      else renderResults();
    }));
    saved.append(actions);
    copy.append(saved);
  }
  const actions = element('div', '', 'button-row');
  actions.append(button('start-attempt', attempt?.status === 'active' ? 'Empezar otro intento' : 'Empezar · 20 preguntas', requestNewAttempt, Boolean(attempt)));
  copy.append(actions, element('p', 'Puedes avanzar a tu ritmo. Cada respuesta queda fijada tras la corrección para que el resultado refleje tu primera elección.', 'small'));

  const guide = element('aside', '', 'panel guide-panel');
  guide.setAttribute('aria-labelledby', 'guide-heading');
  const guideHeading = element('h2', 'Cómo aprovechar el test');
  guideHeading.id = 'guide-heading';
  const steps = element('ol');
  for (const text of [
    'Piensa la respuesta y selecciona una de las cuatro opciones. La corrección aparece al momento.',
    'Lee la explicación, incluso cuando aciertes. Cada pregunta enlaza con material de estudio.',
    'Navega entre preguntas o vuelve al inicio para reanudar el intento más adelante.',
    'Al terminar, consulta tu nota, el resultado por tema y el repaso de errores y preguntas pendientes.',
  ]) steps.append(element('li', text));
  guide.append(guideHeading, steps,
    element('p', 'Cada acierto suma 0,5 puntos. Los errores y las preguntas sin responder suman 0, sin penalización adicional.', 'small'),
    element('p', 'Las 20 preguntas se eligen al azar, sin repetir dentro del intento. Algunos temas pueden no aparecer en una selección concreta.', 'small'));
  const details = element('details');
  const list = element('ul', '', 'topic-list');
  for (const topic of bank.topics) list.append(element('li', topic.title));
  details.append(element('summary', `Temas del banco (${bank.topics.length})`), list);
  guide.append(details, element('p', 'Práctica personal de aprendizaje. El resultado orienta el repaso y no acredita una titulación.', 'small'));
  layout.append(copy, guide);
  mount(layout, focus ? 'welcome-heading' : null);
}

function navigate(index) {
  if (view === 'review') reviewPosition = index;
  else { attempt = navigateAttempt(attempt, index); persist(); }
  renderQuestion({ focus: true });
}

function acceptAnswer(questionId, optionId) {
  if (view !== 'attempt') return;
  const next = answerQuestion(bank, attempt, questionId, optionId);
  if (next === attempt) return;
  attempt = next;
  persist();
  renderQuestion({ feedbackFocus: true });
}

function feedbackFor(question, selectedOptionId) {
  const correct = selectedOptionId === question.correctOptionId;
  const unanswered = selectedOptionId === null;
  const feedback = element('section', '', `feedback${unanswered ? ' unanswered' : correct ? '' : ' incorrect'}`);
  feedback.id = 'answer-feedback';
  feedback.tabIndex = -1;
  feedback.setAttribute('role', 'status');
  feedback.setAttribute('aria-live', 'polite');
  feedback.setAttribute('aria-atomic', 'true');
  feedback.append(element('h3', unanswered ? 'Sin responder · consulta la solución' : correct ? 'Respuesta correcta' : 'Esta vez no es correcta'));
  if (!correct) feedback.append(element('p', `La respuesta correcta es: ${question.options.find(option => option.id === question.correctOptionId).text}`));
  const explanation = element('p', question.explanation);
  explanation.id = 'answer-explanation';
  feedback.append(explanation, studyLink(question));
  return feedback;
}

function renderQuestion({ focus = false, feedbackFocus = false } = {}) {
  const reviewing = view === 'review';
  const result = summarizeAttempt(bank, attempt);
  const indices = reviewing ? reviewIndices : attempt.questionIds.map((_, index) => index);
  const position = reviewing ? reviewPosition : attempt.currentIndex;
  const item = result.items[indices[position]];
  const question = item.question;
  const answered = item.selectedOptionId !== null;
  const locked = answered || reviewing || attempt.status === 'finished';
  const container = element('div');
  const header = element('div', '', 'session-heading');
  const introduction = element('div');
  introduction.append(element('p', reviewing ? 'Repaso con explicaciones' : 'Autoevaluación · Corrección inmediata', 'eyebrow'),
    element('h1', 'Introducción a la informática'),
    element('p', reviewing ? `Repaso ${position + 1} de ${indices.length} · Pregunta ${item.index + 1} del intento` : `Pregunta ${position + 1} de ${SESSION_LENGTH}`, 'muted'));
  header.append(introduction);
  if (!reviewing) header.append(button('pause-attempt', 'Volver al inicio', () => renderHome(true), true));
  else header.append(button('back-to-results', 'Volver al resultado', renderResults, true));
  const layout = element('div', '', 'exam-layout');
  const panel = element('section', '', 'panel question-panel');
  panel.dataset.questionId = question.id;
  const meta = element('div', '', 'question-meta');
  meta.append(element('span', bank.topics.find(topic => topic.id === question.topic).title),
    element('span', difficultyLabels[question.difficulty], 'tag'), element('span', question.id, 'tag'));
  const title = element('h2', question.prompt);
  title.id = 'question-title';
  title.tabIndex = -1;
  const help = element('p', reviewing ? 'Consulta tu primera respuesta y la explicación de la solución.'
    : answered ? 'Respuesta guardada. Puedes revisar la explicación o avanzar.'
      : 'Elige una opción. Se corrige al seleccionarla y la respuesta queda fijada.', 'small');
  help.id = 'selection-help';
  panel.append(meta, title, help);
  const options = element('fieldset', '', 'options');
  options.setAttribute('aria-labelledby', 'question-title');
  options.setAttribute('aria-describedby', 'selection-help');
  for (const optionId of attempt.optionOrders[question.id]) {
    const option = question.options.find(candidate => candidate.id === optionId);
    const isCorrect = locked && option.id === question.correctOptionId;
    const selectedWrong = locked && option.id === item.selectedOptionId && !isCorrect;
    const label = element('label', '', `answer-option${locked ? ' locked' : ''}${isCorrect ? ' correct' : selectedWrong ? ' incorrect' : ''}`);
    label.dataset.optionId = option.id;
    const radio = element('input');
    radio.type = 'radio';
    radio.name = 'answer';
    radio.value = option.id;
    radio.id = `answer-${option.id}`;
    radio.checked = option.id === item.selectedOptionId;
    radio.disabled = locked;
    radio.addEventListener('change', () => { if (radio.checked) acceptAnswer(question.id, radio.value); });
    const body = element('span', '', 'option-body');
    body.append(element('span', option.text, 'option-text'));
    if (isCorrect) body.append(element('span', option.id === item.selectedOptionId ? '✓ Tu respuesta · correcta' : '✓ Respuesta correcta', 'option-state'));
    if (selectedWrong) body.append(element('span', '× Tu respuesta · incorrecta', 'option-state'));
    label.append(radio, body);
    options.append(label);
  }
  panel.append(options);
  if (locked) panel.append(feedbackFor(question, item.selectedOptionId));
  const navigation = element('nav', '', 'question-navigation');
  navigation.setAttribute('aria-label', reviewing ? 'Navegar por el repaso' : 'Navegar por las preguntas');
  const previous = button('previous-question', 'Anterior', () => navigate(position - 1), true);
  previous.disabled = position === 0;
  const next = button('next-question', 'Siguiente', () => navigate(position + 1));
  next.disabled = position === indices.length - 1;
  navigation.append(previous, next);
  panel.append(navigation);

  const tools = element('aside', '', 'panel session-tools');
  tools.setAttribute('aria-labelledby', 'progress-heading');
  const progressHeading = element('h2', reviewing ? 'Preguntas del repaso' : 'Tu intento');
  progressHeading.id = 'progress-heading';
  const progressCopy = element('p', `${result.answered} de ${result.total} respondidas`, 'progress-copy');
  progressCopy.id = 'answered-count';
  const progress = element('progress');
  progress.max = result.total;
  progress.value = result.answered;
  progress.setAttribute('aria-label', `${result.answered} de ${result.total} preguntas respondidas`);
  tools.append(progressHeading, progressCopy, progress);
  const indexNavigation = element('nav', '', 'question-index');
  indexNavigation.setAttribute('aria-label', 'Seleccionar pregunta');
  for (const [localIndex, originalIndex] of indices.entries()) {
    const current = result.items[originalIndex];
    const status = current.selectedOptionId === null ? 'unanswered' : current.correct ? 'correct' : 'incorrect';
    const labels = { unanswered: 'sin responder', correct: 'correcta', incorrect: 'incorrecta' };
    const itemButton = element('button', String(originalIndex + 1));
    itemButton.type = 'button';
    itemButton.dataset.result = status;
    itemButton.setAttribute('aria-label', `Pregunta ${originalIndex + 1}: ${labels[status]}`);
    if (localIndex === position) itemButton.setAttribute('aria-current', 'step');
    const symbol = element('span', status === 'correct' ? '✓' : status === 'incorrect' ? '×' : '○', 'index-symbol');
    symbol.setAttribute('aria-hidden', 'true');
    itemButton.append(symbol);
    itemButton.addEventListener('click', () => navigate(localIndex));
    indexNavigation.append(itemButton);
  }
  tools.append(indexNavigation, element('p', '✓ Correcta · × Incorrecta · ○ Sin responder', 'index-legend'));
  tools.append(button('finish-attempt', reviewing ? 'Volver al resultado' : result.unanswered ? 'Finalizar intento' : 'Ver resultado', reviewing ? renderResults : requestFinish));
  tools.append(element('p', reviewing ? 'Las respuestas del intento ya están cerradas.'
    : storageAvailable ? 'Guardado en este navegador.' : 'Sesión disponible mientras esta página permanezca abierta.', 'small'));
  layout.append(panel, tools);
  container.append(header, layout);
  mount(container, feedbackFocus ? 'answer-feedback' : focus ? 'question-title' : null);
}

function requestFinish() {
  const result = summarizeAttempt(bank, attempt);
  const finish = () => {
    attempt = finishAttempt(attempt);
    persist();
    renderResults();
  };
  if (result.unanswered) requestConfirmation('Finalizar con preguntas pendientes',
    `Quedan ${result.unanswered} preguntas sin responder. Sumarán 0 puntos y podrás consultar sus soluciones en el repaso. El resultado se calculará sobre las ${result.total} preguntas del intento.`,
    'Finalizar y ver resultado', finish);
  else finish();
}

function beginReview(mistakesOnly) {
  const result = summarizeAttempt(bank, attempt);
  reviewIndices = result.items.filter(item => !mistakesOnly || !item.correct).map(item => item.index);
  if (!reviewIndices.length) return;
  reviewPosition = 0;
  view = 'review';
  renderQuestion({ focus: true });
}

function renderResults() {
  view = 'results';
  const result = summarizeAttempt(bank, attempt);
  const container = element('div');
  const heading = element('h1', 'Tu resultado y el siguiente paso');
  heading.id = 'results-heading';
  heading.tabIndex = -1;
  const header = element('div', '', 'session-heading');
  const title = element('div');
  title.append(element('p', 'Intento finalizado · Autoevaluación', 'eyebrow'), heading,
    element('p', `${SESSION_LENGTH} preguntas del banco de ${BANK_SIZE} · Versión ${bank.version}`, 'small'));
  header.append(title);
  const hero = element('section', '', 'panel score-hero');
  hero.setAttribute('aria-labelledby', 'score-heading');
  const grade = element('div', '', 'grade-block');
  const gradeValue = element('strong', numberFormat.format(result.grade), 'grade');
  gradeValue.id = 'result-grade';
  grade.append(gradeValue, element('span', 'sobre 10'));
  const explanation = element('div');
  const scoreHeading = element('h2', `${result.correct} aciertos de ${result.total}`);
  scoreHeading.id = 'score-heading';
  explanation.append(scoreHeading, element('p', result.grade >= 8 ? 'Buen resultado en las preguntas de este intento. Revisa las explicaciones y prueba una nueva selección para seguir afianzando lo aprendido.'
    : result.grade >= 5 ? 'Ya tienes una base. Revisa los errores y vuelve a los contenidos que te han generado dudas antes del siguiente intento.'
      : 'Este intento te da un punto de partida para orientar el estudio. Empieza por las explicaciones y practica los temas con más dudas.'));
  const facts = element('div', '', 'result-facts');
  facts.append(statistic(result.correct, 'aciertos', 'result-correct'), statistic(result.incorrect, 'errores', 'result-incorrect'), statistic(result.unanswered, 'sin responder', 'result-unanswered'));
  explanation.append(facts);
  hero.append(grade, explanation);

  const grid = element('div', '', 'result-grid');
  const topicPanel = element('section', '', 'panel');
  topicPanel.append(element('h2', 'Resultado por tema'));
  const scroll = element('div', '', 'table-scroll');
  scroll.tabIndex = 0;
  scroll.setAttribute('role', 'region');
  scroll.setAttribute('aria-label', 'Resultados por tema; tabla desplazable en pantallas pequeñas');
  const table = element('table');
  table.id = 'topic-results';
  table.append(element('caption', 'Temas presentes en este intento. El total incluye las preguntas pendientes.'));
  const tableHead = element('thead');
  const headRow = element('tr');
  for (const label of ['Tema', 'Aciertos', 'Errores', 'Pendientes', 'Total']) {
    const cell = element('th', label);
    cell.scope = 'col';
    headRow.append(cell);
  }
  tableHead.append(headRow);
  const tableBody = element('tbody');
  for (const topic of result.byTopic) {
    const row = element('tr');
    row.dataset.topic = topic.id;
    const cell = element('th', topic.title);
    cell.scope = 'row';
    row.append(cell);
    for (const value of [topic.correct, topic.incorrect, topic.unanswered, topic.total]) row.append(element('td', String(value)));
    tableBody.append(row);
  }
  table.append(tableHead, tableBody);
  scroll.append(table);
  topicPanel.append(scroll, element('p', `Cálculo: ${result.correct} ÷ ${result.total} × 10 = ${numberFormat.format(result.grade)}. Cada acierto suma 0,5 puntos; errores y pendientes suman 0.`, 'small'));

  const study = element('section', '', 'panel');
  study.append(element('h2', 'Prepara el siguiente intento'));
  const missing = result.incorrect + result.unanswered;
  study.append(element('p', missing ? `Repasa las ${missing} preguntas que han quedado incorrectas o pendientes. Después, aplica lo aprendido a una selección nueva.`
    : 'Has acertado todas las preguntas de esta selección. Revisa el razonamiento o practica con otras preguntas del banco.', 'muted'));
  const actions = element('div', '', 'button-row');
  const reviewButton = button('review-mistakes', `Repasar errores y pendientes (${missing})`, () => beginReview(true));
  reviewButton.disabled = missing === 0;
  actions.append(reviewButton, button('review-all', 'Revisar las 20 preguntas', () => beginReview(false), true));
  study.append(actions);
  const resources = new Map();
  const priorities = result.items.filter(item => missing ? !item.correct : true);
  for (const item of priorities) if (!resources.has(item.question.study.url)) resources.set(item.question.study.url, item.question.study.label);
  const list = element('ul', '', 'study-list');
  for (const [url, label] of [...resources.entries()].slice(0, 5)) {
    const entry = element('li');
    const link = element('a', label);
    link.href = url;
    entry.append(link);
    list.append(entry);
  }
  study.append(list);
  grid.append(topicPanel, study);
  const finalActions = element('div', '', 'button-row result-actions');
  finalActions.append(button('new-attempt-result', 'Nuevo intento aleatorio', requestNewAttempt), button('return-home', 'Volver al inicio', () => renderHome(true), true));
  container.append(header, hero, grid, finalActions,
    element('p', 'Resultado orientativo de práctica. No equivale a una certificación ni a una evaluación oficial del curso.', 'small'));
  mount(container, 'results-heading');
}

async function bootstrap() {
  if (loading) return;
  loading = true;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(new URL('questions.json', import.meta.url), {
      credentials: 'same-origin', cache: 'no-cache', redirect: 'error', signal: controller.signal,
    });
    if (!response.ok) throw new Error('Banco no disponible.');
    const raw = await response.text();
    if (raw.length > 1_000_000) throw new Error('Banco demasiado grande.');
    bank = validateBank(JSON.parse(raw));
    const stored = persistence.load(bank);
    attempt = stored.attempt;
    storageAvailable = stored.status !== 'unavailable';
    if (stored.status === 'unavailable') showNotice('Este navegador no permite guardar el intento. Puedes practicar mientras mantengas esta página abierta.');
    else if (stored.status === 'invalid') showNotice('El intento guardado está incompleto o pertenece a otra versión del banco. Puedes empezar uno nuevo.');
    renderHome();
  } catch {
    const error = element('section', '', 'error-panel');
    error.id = 'load-error';
    error.setAttribute('role', 'alert');
    error.append(element('h1', 'No se han podido cargar las preguntas'),
      element('p', 'No se ha podido cargar un banco de 100 preguntas válido. Comprueba la conexión y vuelve a intentarlo.'),
      button('retry-load', 'Reintentar', () => bootstrap()));
    mount(error);
  } finally {
    clearTimeout(timeout);
    loading = false;
  }
}

bootstrap();
