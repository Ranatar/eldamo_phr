// "Словотворчество" panel of the atlas: pick two words, a stage of formation,
// get ranked variants with the rules that produced them (engine: wordform.js).
(function () {
'use strict';
const WF = window.WF, QU = window.QU, QR = window.QR;
const SITE = QU.SITE;
const $ = id => document.getElementById(id);
const esc = QU.esc;
const engine = QU.engine;
const SOURCE = {
  attested: 'форма засвидетельствована в деривации Eldamo', stem: 'основа', dictionary: 'словарная форма',
  primitive: 'праформа Eldamo', computed: 'праформа Eldamo, прогнанная до выбранной стадии',
  reconstructed: 'восстановленная праформа, гипотеза', 'soft-mutation': 'с мягкой мутацией',
  suffix: 'суффикс', prefix: 'приставка',
};
const ADJUST = {
  reduction: 'сокращение конца длинного сложения (учебник §6.1.2.1; Толкин, PE17/106, PE21/32)',
  lengthening: 'просодическое удлинение на стыке (учебник §6.1.3; правила сформулированы Страком)',
  shortening: 'сокращение долгого гласного перед суффиксом (§6.1.2.2; Страк, по примерам)',
};
const state = { branch: QU.BRANCHES[0], picked: [null, null] };
const era = () => $('wf-era').value || 'late';
const eraOf = QU.eraOf, marker = QU.marker;
const spelling = QU.spelling, plainForm = QU.plainForm;

function search(slot) {
  const E = engine(state.branch), want = era();
  const box = $('wf-r' + slot);
  const q = $('wf-q' + slot).value;
  if (!q.trim()) { box.innerHTML = ''; return; }
  const hits = QU.searchWords(q, (b, e) => b === state.branch && eraOf(E, e.lang) === want, 12);
  box.innerHTML = hits.map(h => QU.hitHtml(h, `data-id="${esc(h.entry.id)}" data-slot="${slot}"`)).join('')
    || `<p class="muted">Ничего не найдено в ${esc(QU.BRANCH_NAMES[state.branch])} (${esc(QU.ERA_NAMES[want])} концепция)${QU.neo() ? '' : '; неологизмы скрыты'}.</p>`;
}

function describe(E, e) {
  const bits = [];
  if (e.stems) bits.push('основа ' + e.stems.map(s => `<span class="form">${esc(s)}</span>`).join(', '));
  const pr = e.starts || (e.stages && (e.stages.p || e.stages.mp));
  if (pr) bits.push('праформа ' + pr.map(s => `<span class="form">${esc(s)}</span>`).join(', '));
  else bits.push('праформы в Eldamo нет — для ранних стадий она восстанавливается');
  if (e.mark && e.mark !== '#') bits.push(`пометка Eldamo «${esc(e.mark)}»`);
  const kind = WF.affixKind(e);
  if (kind) {
    bits.unshift(`${kind === 'suffix' ? 'суффикс' : 'приставка'}, формы: ${WF.allomorphs(e, E.branch).map(f => `<span class="form">${esc(f)}</span>`).join(', ')}`);
    const ex = (E.affixes.affix[e.id] || {}).examples || [];
    if (ex.length) bits.push('засвидетельствован в ' + ex.map(f => `<span class="form">${esc(f)}</span>`).join(', '));
  }
  return `<a href="${SITE}words/word-${esc(e.id)}.html" target="_blank" rel="noopener"><span class="marker">${esc(marker(E, e.lang))}</span> <span class="form">${esc(e.form)}</span></a>
    <span class="muted">${esc(e.gloss)}</span><br><span class="small">${bits.join('; ')}</span>`;
}

function pick(slot, id) {
  const E = engine(state.branch);
  state.picked[slot - 1] = id;
  const e = E.lexicon.get(id);
  $('wf-chosen' + slot).innerHTML = e ? describe(E, e) : '';
  $('wf-r' + slot).innerHTML = '';
  $('wf-go').disabled = !(state.picked[0] && state.picked[1]);
}

function stageOptions() {
  const E = engine(state.branch);
  const langs = E.languages.filter(l => l.era === era()).sort((a, b) => a.stage - b.stage);
  const sel = $('wf-stage'), prev = sel.value;
  sel.replaceChildren(...langs.map(l => new Option(`${l.marker} ${l.name}`, String(l.stage))));
  sel.value = langs.some(l => String(l.stage) === prev) ? prev : String(langs[langs.length - 1].stage);
}

function traceHtml(E, trace) { return QU.stagesHtml(trace, E.branch); }
const show = ph => ph.length ? ph.join('') : '∅';
function junctionText(a, b, [k, m, rep]) {
  if (!(k || m || rep)) return '';
  const ctx = b.slice(m, m + 1);
  return `${show(a.slice(a.length - k))} + ${show(b.slice(0, m).concat(ctx))} → ${show(WF.phonemes(rep).concat(ctx))}`;
}
function opText(v) {
  // the junction op [k, m, rep]: the last k sounds of the first element and the
  // first m of the second become rep; one following sound is shown as context
  const out = [];
  const a = WF.phonemes(WF.comparable(v.elements[0])), b = WF.phonemes(WF.comparable(v.elements[1]));
  const j = junctionText(a, b, v.junction || [0, 0, '']);
  if (j) out.push('на стыке ' + esc(j));
  const [ke, repe] = v.ending || [0, ''];
  if (ke || repe) out.push(`в конце -${esc(show(b.slice(b.length - ke)))} → -${esc(show(WF.phonemes(repe)))}`);
  if (v.shortened) out.push('долгий гласный второго элемента сокращён');
  if (v.lengthened) out.push('гласный основы удлинён перед суффиксом');
  return out.length ? out.join('; ') + ' — как в засвидетельствованных словах' : 'без изменений на стыке';
}

function compose() {
  const E = engine(state.branch);
  const [a, b] = state.picked;
  if (!a || !b) return;
  const stage = Number($('wf-stage').value);
  const out = $('wf-output');
  let vs;
  try { vs = WF.predict(E, [a, b], era(), stage); } catch (err) { out.textContent = 'Ошибка: ' + err.message; throw err; }
  const last = Math.max(...E.languages.filter(l => l.era === era()).map(l => l.stage));
  if (!vs.length) {
    out.innerHTML = '<p>Для этих слов на выбранной стадии форм не найдено: у элемента нет ни праформы, ни восстановленной праформы, дающей его форму.</p>';
    return;
  }
  const reconstructed = vs.some(v => (v.sources || []).includes('reconstructed'));
  let shown = vs.slice(0, 8);
  if (stage >= last) {
    // the plain join stays visible even when attested compounds prefer a change
    const plain = vs.find(v => v.junction && !v.junction[0] && !v.junction[1] && !v.junction[2] && !(v.ending || [0])[0]
      && !(v.ending || [0, ''])[1] && !v.shortened && !(v.adjustments || []).length && !(v.trace || []).length);
    if (plain && !shown.includes(plain)) shown = shown.concat([plain]);
  }
  const rows = shown.map((v, k) => {
    const src = (v.sources || []).map((h, i) => `<span class="form">${esc(v.elements[i])}</span> <span class="muted small">(${esc(SOURCE[h] || h)})</span>`).join(' + ');
    const adj = (v.adjustments || []).map(r => esc(ADJUST[r] || r)).join('; ');
    const ops = stage >= last ? opText(v) : '';
    return `<li class="wf-variant${k === 0 ? ' main' : ''}">
      <div><strong class="form">${esc(spelling(v.form, state.branch))}</strong> <span class="ipa muted">[${esc(plainForm(v.form))}]</span>
      ${v.score != null ? `<span class="small muted">вес ${v.score}</span>` : ''}${v.stem ? ` <span class="small">основа <span class="form">${esc(v.stem)}-</span></span>` : ''}
      <button type="button" class="link small" data-use="${esc(plainForm(v.form))}" title="Сделать эту форму текущим словом">работать с этой формой</button></div>
      <div class="small">из ${src}</div>
      ${ops ? `<div class="small">${ops}</div>` : ''}${adj ? `<div class="small">${adj}</div>` : ''}
      ${traceHtml(E, v.trace || [])}</li>`;
  }).join('');
  let analog = '';
  if (stage >= last && vs[0].affix) {
    const ex = (E.affixes.affix[vs[0].affix] || {}).examples || [];
    analog = ex.length ? `<p class="small">Засвидетельствованные слова с этим аффиксом: ${ex.map(f => `<span class="form">${esc(f)}</span>`).join(', ')}.</p>`
      : '<p class="small">Засвидетельствованных слов с этим аффиксом в разборе Eldamo нет — стык подобран по всем словам с аффиксами того же вида.</p>';
  } else if (stage >= last && vs[0].elements) {
    const pa = WF.phonemes(WF.comparable(vs[0].elements[0])), pb = WF.phonemes(WF.comparable(vs[0].elements[1]));
    const list = E.analogues[JSON.stringify([pa[pa.length - 1], pb[0]])] || [];
    const groups = new Map();
    for (const [f, op] of list) {
      const key = (op[0] || op[1] || op[2]) ? (op[0] <= 1 && op[1] <= 1 ? junctionText(pa, pb, op) : `«${op[2] || '∅'}» вместо ${op[0]} + ${op[1]} зв.`) : 'без изменений';
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(f);
    }
    if (list.length) analog = `<p class="small">Засвидетельствованные сложения, где первый элемент кончается на ${esc(pa[pa.length - 1])}, а второй начинается с ${esc(pb[0])}: `
      + [...groups.entries()].map(([k, fs]) => `${fs.map(f => `<span class="form">${esc(f)}</span>`).join(', ')} (${esc(k)})`).join('; ') + '.</p>';
  }
  out.innerHTML = `<ol class="wf-variants">${rows}</ol>${analog}
    <p class="small muted">${stage >= last && vs[0].affix
      ? 'Форма аффикса и изменения на стыке подобраны по засвидетельствованным словам с этим аффиксом (иначе — со всеми аффиксами того же вида)' + (state.branch === 'quenya' ? '; плюс просодическое удлинение и сокращение перед суффиксами (§6.1).' : '; приставка может вызывать мягкую мутацию основы.')
      : stage >= last
      ? 'На последней стадии исторические законы уже отработали: стык и конец сложения подбираются по засвидетельствованным сложениям (частота — «вес»)' + (state.branch === 'quenya' ? ', плюс правила §6.1 учебника Страка.' : ', плюс мягкая мутация второго элемента и правила для многосложных слов.')
      : 'Элементы взяты в формах выбранной стадии и соединены через границу морфем; дальше действуют все последующие правила ветви в порядке Eldamo. Первый вариант — основное чтение (необязательные правила применены).'}
    ${reconstructed ? ' Хотя бы одна праформа восстановлена по соответствиям в деривациях — это гипотеза, а не форма Толкина.' : ''}
    Результат — предсказание формы, а не засвидетельствованное слово.</p>`;
}

function branchOptions() {
  $('wf-branch').replaceChildren(...QU.BRANCHES.map(b => new Option(QU.BRANCH_NAMES[b], b)));
  $('wf-era').replaceChildren(...QU.ERAS.map(e => new Option(QU.ERA_NAMES[e], e)));
}
function reset() {
  state.picked = [null, null];
  for (const s of [1, 2]) { $('wf-q' + s).value = ''; $('wf-r' + s).innerHTML = ''; $('wf-chosen' + s).innerHTML = ''; }
  $('wf-output').innerHTML = ''; $('wf-go').disabled = true;
}
function setBranch(b, e) {
  const changed = b !== state.branch || e !== era();
  state.branch = b;
  $('wf-branch').value = b;
  $('wf-era').value = e;
  if (changed) reset();
  stageOptions();
}
// the chosen word becomes the first element, in its own branch and conception
function onSubject(s) {
  if (!s || s.kind !== 'word') return;
  const e = s.entry, E = engine(s.branch);
  const want = eraOf(E, e.lang);
  if (!want) return;
  setBranch(s.branch, want);
  pick(1, e.id);
}

branchOptions();
for (const s of [1, 2]) {
  $('wf-q' + s).addEventListener('input', () => search(s));
  $('wf-r' + s).addEventListener('click', e => { const t = e.target.closest('[data-id]'); if (t) pick(s, t.dataset.id); });
}
$('wf-branch').addEventListener('change', () => { state.branch = $('wf-branch').value; reset(); stageOptions(); });
$('wf-era').addEventListener('change', () => { reset(); stageOptions(); });
$('wf-go').addEventListener('click', compose);
$('wf-output').addEventListener('click', e => {
  const u = e.target.closest('[data-use]');
  if (!u) return;
  const E = engine(state.branch);
  QU.openForm(u.dataset.use, state.branch, era(), Math.max(...E.languages.filter(l => l.era === era()).map(l => l.stage)));
});
QU.onSubject((s, why) => { if (why === 'subject') onSubject(s); else if (why === 'neo') { search(1); search(2); } });
setBranch(state.branch, 'late');
window.WFCOMPOSE = { pick, compose };
})();
