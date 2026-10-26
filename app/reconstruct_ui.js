// "Реконструкция" panel: the form of a word for another period (wordform.js: reconstruct).
(function () {
'use strict';
const WF = window.WF, UI = window.WFUI;
const $ = id => document.getElementById(id);
const SITE = 'https://eldamo.org/content/';
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fold = s => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
const BRANCHES = ['quenya', 'sindarin'];
const BRANCH_NAMES = { quenya: 'квенья', sindarin: 'синдарин' };
const ERA_NAMES = { late: 'поздняя', middle: 'средняя', early: 'ранняя' };
const MARKS = {
  attested: 'засвидетельствовано в Eldamo', link: 'связь Eldamo между статьями', unchanged: 'форма без изменений',
  reconstructed: 'восстановлено, проверено прогоном вперёд', root: 'согласуется с корнем слова',
  cognate: 'через общую праформу', 'primitive-attested': 'праформа из Eldamo', neologism: 'переэтимологизация — неологизм',
  phonotactics: 'нетипично для целевого языка', main: 'основное чтение законов',
};
const engines = () => Object.fromEntries(BRANCHES.map(b => [b, UI.engine(b)]));
const state = { word: null };

function currentBranch() {
  let raw = location.hash.slice(1);
  try { raw = decodeURIComponent(raw); } catch (_e) { /* as is */ }
  const name = raw.split('?')[0];
  return BRANCHES.includes(name) ? name : null;
}
function periodOptions(sel, branch, keep) {
  const E = UI.engine(branch);
  const prev = keep ? sel.value : null;
  const opts = [];
  for (const era of ['late', 'middle', 'early']) {
    for (const l of E.languages.filter(x => x.era === era).sort((a, b) => a.stage - b.stage)) {
      opts.push(new Option(`${ERA_NAMES[era]}: ${l.marker} ${l.name}`, `${era}|${l.stage}`));
    }
  }
  sel.replaceChildren(...opts);
  if (prev && opts.some(o => o.value === prev)) sel.value = prev;
}
function langPeriod(E, code) {
  const l = E.languages.find(x => x.code === code);
  return l ? `${l.era}|${l.stage}` : null;
}

function search() {
  const b = currentBranch();
  if (!b) return;
  const E = UI.engine(b);
  const q = fold($('rc-q').value.trim());
  const box = $('rc-r');
  if (!q) { box.innerHTML = ''; return; }
  const hits = [];
  for (const e of E.lexiconList) {
    if (e.neo || !E.languages.some(l => l.code === e.lang)) continue;
    const f = fold(e.form), g = fold(e.gloss || '');
    const score = f === q ? 0 : f.startsWith(q) ? 1 : g.split(/[^\p{L}]+/u).includes(q) ? 2 : f.includes(q) ? 3 : -1;
    if (score >= 0) hits.push([score, e]);
  }
  hits.sort((a, c) => a[0] - c[0] || a[1].form.length - c[1].form.length);
  const marker = code => (E.languages.find(l => l.code === code) || {}).marker || code;
  box.innerHTML = hits.slice(0, 10).map(([, e]) => `<button type="button" data-id="${esc(e.id)}"><span class="marker">${esc(marker(e.lang))}</span>
    <span class="form">${esc(e.form)}</span> <span class="muted">${esc(e.gloss)}</span></button>`).join('')
    || '<p class="muted">Ничего не найдено. Можно ввести форму в поле «или форма».</p>';
}
function pick(id) {
  const b = currentBranch();
  const E = UI.engine(b);
  const e = E.lexicon.get(id);
  state.word = id;
  $('rc-r').innerHTML = '';
  $('rc-form').value = '';
  const marker = (E.languages.find(l => l.code === e.lang) || {}).marker || e.lang;
  $('rc-chosen').innerHTML = `<a href="${SITE}words/word-${esc(e.id)}.html" target="_blank" rel="noopener"><span class="marker">${esc(marker)}</span>
    <span class="form">${esc(e.form)}</span></a> <span class="muted">${esc(e.gloss)}</span>`;
  const p = langPeriod(E, e.lang);
  if (p) $('rc-src').value = p;
  $('rc-go').disabled = false;
}

function run() {
  const b = currentBranch();
  const [se, ss] = $('rc-src').value.split('|');
  const db = $('rc-dst-branch').value;
  const [de, ds] = $('rc-dst').value.split('|');
  const typed = $('rc-form').value.trim();
  const opts = typed ? { form: typed, spelled: $('rc-spelled').checked } : { word: state.word };
  const out = $('rc-output');
  if (!typed && !state.word) { out.textContent = 'Выберите слово или введите форму.'; return; }
  let vs;
  try { vs = WF.reconstruct(engines(), [b, se, Number(ss)], [db, de, Number(ds)], opts); } catch (err) { out.textContent = 'Ошибка: ' + err.message; throw err; }
  if (!vs.length) {
    out.innerHTML = '<p>Форм не найдено: ни одна восстановленная форма не даёт исходную при прогоне вперёд. Попробуйте другую стадию или введите форму в фонетической записи.</p>';
    return;
  }
  const D = UI.engine(db);
  const lastStage = Math.max(...D.languages.filter(l => l.era === de).map(l => l.stage));
  const E = UI.engine(db);
  const rule = id => E.ruleNames.get(id) || UI.engine(b).ruleNames.get(id) || id;
  out.innerHTML = '<ol class="wf-variants">' + vs.map((v, k) => {
    const steps = (v.steps || []).filter(t => t[2] != null);
    const trace = steps.length ? `<details><summary>Правила (${steps.length})</summary><ol class="steps">${steps.map(t =>
      `<li><span class="form">${esc(t[1])}</span> → <span class="form">${esc(t[2])}</span> <a href="${SITE}words/word-${esc(t[0])}.html" target="_blank" rel="noopener">${esc(rule(t[0]))}</a></li>`).join('')}</ol></details>` : '';
    const shown = Number(ds) === lastStage && de !== 'early' ? UI.spelling(v.form, db) : v.form;
    return `<li class="wf-variant${k === 0 ? ' main' : ''}"><div><strong class="form">${esc(shown)}</strong>
      ${shown !== v.form ? `<span class="ipa muted">[${esc(v.form)}]</span>` : ''} <span class="small muted">вес ${v.score}</span></div>
      <div class="small">${esc(v.route)}</div>
      <div class="small">${v.marks.filter(m => MARKS[m]).map(m => `<span class="tag">${esc(MARKS[m])}</span>`).join(' ')}
      ${v.problems ? ` <span class="muted">(${esc(v.problems.join(', '))})</span>` : ''}</div>${trace}</li>`;
  }).join('') + '</ol>' +
    '<p class="small muted">Назад по стадиям форма восстанавливается по соответствиям из дериваций Eldamo, и каждая кандидатура проверяется прогоном вперёд. ' +
    'Другая ветвь — через общую праформу. Другая концепция — сначала связи Eldamo, затем форма без изменений, затем переэтимологизация (неологизм). ' +
    'Кроме засвидетельствованного, всё — гипотеза модели.</p>';
}

function render() {
  const b = currentBranch();
  if (!b) return;
  periodOptions($('rc-src'), b, true);
  periodOptions($('rc-dst'), $('rc-dst-branch').value || b, true);
}
$('rc-dst-branch').replaceChildren(...BRANCHES.map(b => new Option(BRANCH_NAMES[b], b)));
$('rc-q').addEventListener('input', search);
$('rc-r').addEventListener('click', e => { const t = e.target.closest('[data-id]'); if (t) pick(t.dataset.id); });
$('rc-form').addEventListener('input', () => { if ($('rc-form').value.trim()) { state.word = null; $('rc-chosen').innerHTML = ''; } $('rc-go').disabled = !($('rc-form').value.trim() || state.word); });
$('rc-dst-branch').addEventListener('change', () => periodOptions($('rc-dst'), $('rc-dst-branch').value, false));
$('rc-go').addEventListener('click', run);
window.addEventListener('hashchange', () => {
  const b = currentBranch();
  if (b && $('rc-dst-branch').dataset.init !== b) { $('rc-dst-branch').value = b; $('rc-dst-branch').dataset.init = b; state.word = null; $('rc-chosen').innerHTML = ''; }
  render();
});
if (currentBranch()) { $('rc-dst-branch').value = currentBranch(); $('rc-dst-branch').dataset.init = currentBranch(); }
render();
window.RCUI = { pick, run };
})();
