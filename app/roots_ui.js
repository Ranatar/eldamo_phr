// "Корни" panel: the index of roots (shared/root_index.py) with a search, the roots of Eldamo's
// list, the recommended ones and those no word comes from yet; a root opens its card (word_ui.js).
(function () {
'use strict';
const QU = window.QU;
const $ = id => document.getElementById(id);
const esc = QU.esc, T = QU.T, fold = QU.fold;
const ROOTS = QU.ROOTS;
const LIMIT = 80;
const all = Object.entries(ROOTS);
const count = r => Object.values(r.words || {}).reduce((n, x) => n + x.length, 0);
const recommended = r => r.listed && !(r.w || []).length;
const keys = new Map();
const keyOf = (id, r) => { if (!keys.has(id)) keys.set(id, [fold(r.f.replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰()/]/g, ' ')), fold(r.g || '')]); return keys.get(id); };

function render() {
  const q = fold($('roots-q').value.trim());
  const which = $('roots-which').value, era = $('roots-era').value;
  const hits = [];
  for (const [id, r] of all) {
    if (era && r.l !== era) continue;
    if (which === 'listed' && !r.listed) continue;
    if (which === 'recommended' && !recommended(r)) continue;
    if (which === 'free' && !(recommended(r) && !r.words)) continue;
    let score = 0;
    if (q) {
      const [f, g] = keyOf(id, r);
      const words = f.split(/\s+/).filter(Boolean);
      score = words.includes(q) ? 0 : f.startsWith(q) ? 1 : g.split(/[^\p{L}]+/u).includes(q) ? 2 : f.includes(q) ? 3 : g.includes(q) ? 4 : -1;
      if (score < 0) continue;
    }
    hits.push([score, id, r]);
  }
  hits.sort((a, b) => a[0] - b[0] || (fold(a[2].f) < fold(b[2].f) ? -1 : fold(a[2].f) > fold(b[2].f) ? 1 : 0));
  $('roots-count').textContent = T('roots.count', { n: hits.length, shown: Math.min(hits.length, LIMIT) });
  $('roots-list').innerHTML = hits.slice(0, LIMIT).map(([, id, r]) => {
    const n = count(r);
    return `<button type="button" data-root="${esc(id)}"><span class="marker">${esc(QU.ROOT_MARKERS[r.l] || '√')}</span><span class="form">${esc(r.f)}</span>`
      + ` <span class="muted">${esc(r.g)}</span>`
      + ` <span class="small">${n ? esc(QU.TN('n.words', n)) : T('roots.noWords')}</span>`
      + `${(r.w || []).length ? ` <span class="tag warn" title="${esc(r.w.map(w => T('root.warn.' + w)).join(', '))}">⚠</span>` : ''}</button>`;
  }).join('') || `<p class="muted">${T('roots.none')}</p>`;
}
for (const id of ['roots-q', 'roots-which', 'roots-era']) $(id).addEventListener(id === 'roots-q' ? 'input' : 'change', render);
render();
window.ROOTSUI = { render };
})();
