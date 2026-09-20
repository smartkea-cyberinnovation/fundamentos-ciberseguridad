/** Filters for the canonical outline. No persistence, network or execution. */
export const normalise = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
export function matches(row, filters) {
  const terms = normalise(filters.query || '').trim().split(/\s+/).filter(Boolean).slice(0, 12);
  return (filters.block === 'all' || row.block === filters.block)
    && (filters.status === 'all' || row.status === filters.status)
    && terms.every(term => normalise(row.search).includes(term));
}
export function applyFilters(root) {
  const query = root.querySelector('#outline-query');
  if (!query) return;
  const filters = {query: query.value, block: root.querySelector('#outline-block').value,
    status: root.querySelector('#outline-status').value};
  const rows = [...root.querySelectorAll('[data-outline-row]')];
  let shown = 0;
  for (const row of rows) {
    row.hidden = !matches(row.dataset, filters);
    if (!row.hidden) shown++;
  }
  for (const section of root.querySelectorAll('[data-outline-section]')) {
    section.hidden = ![...section.querySelectorAll('[data-outline-row]')].some(row => !row.hidden);
  }
  root.querySelector('#outline-count').textContent = `${shown} de ${rows.length} módulos visibles.`;
  root.querySelector('#outline-empty').hidden = shown !== 0;
}
if (typeof document !== 'undefined') {
  const refresh = event => {
    if (['outline-query', 'outline-block', 'outline-status'].includes(event.target.id)) applyFilters(document);
  };
  document.addEventListener('input', refresh);
  document.addEventListener('change', refresh);
  document.addEventListener('click', event => {
    const jump = event.target.closest('[data-scroll^="outline-"]');
    if (jump && document.querySelector('#outline-query')) {
      const section = document.getElementById(jump.dataset.scroll);
      const block = jump.dataset.scroll.slice('outline-'.length);
      if (section && [...document.querySelector('#outline-block').options].some(option => option.value === block)) {
        event.preventDefault();
        document.querySelector('#outline-query').value = '';
        document.querySelector('#outline-block').value = block;
        document.querySelector('#outline-status').value = 'all';
        applyFilters(document);
        section.scrollIntoView({block: 'start'});
      }
      return;
    }
    if (!event.target.closest('#outline-reset')) return;
    document.querySelector('#outline-query').value = '';
    document.querySelector('#outline-block').value = 'all';
    document.querySelector('#outline-status').value = 'all';
    applyFilters(document);
    document.querySelector('#outline-query').focus();
  });
}
