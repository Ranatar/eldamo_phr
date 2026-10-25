// "Словотворчество" panel of the atlas: pick two words, a stage of formation,
// get ranked variants with the rules that produced them (engine: wordform.js).
(function () {
'use strict';
const WF = window.WF;
const WDATA = JSON.parse(document.getElementById('wordform-data').textContent);
const SITE = 'https://eldamo.org/content/';
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const engines = {};
const engine = b => engines[b] || (engines[b] = WF.makeEngine(b, WDATA[b]));
const NEO_ERA = { nq: 'late', ns: 'late', np: 'late', van: 'late', norths: 'late' };
const MARKERS = { nq: 'NQ.', ns: 'NS.', np: 'N✶', van: 'Van.', norths: 'NS.' };
const SOURCE = {
  attested: 'форма засвидетельствована в деривации Eldamo', stem: 'основа', dictionary: 'словарная форма',
  primitive: 'праформа Eldamo', computed: 'праформа Eldamo, прогнанная до выбранной стадии',
  reconstructed: 'восстановленная праформа, гипотеза', 'soft-mutation': 'с мягкой мутацией',
};
const ADJUST = {
  reduction: 'сокращение конца длинного сложения (учебник §6.1.2.1; Толкин, PE17/106, PE21/32)',
  lengthening: 'просодическое удлинение на стыке (учебник §6.1.3; правила сформулированы Страком)',
  shortening: 'сокращение долгого гласного перед суффиксом (§6.1.2.2; Страк, по примерам)',
};
const state = { branch: null, picked: [null, null] };

function currentBranch() {
  let raw = location.hash.slice(1);
  try { raw = decodeURIComponent(raw); } catch (_e) { /* as is */ }
  const name = raw.split('?')[0];
  return WDATA[name] ? name : null;
}
const era = () => $('era-select').value || 'late';
function eraOf(E, code) {
  const l = E.languages.find(x => x.code === code);
  return l ? l.era : NEO_ERA[code] || null;
}
const marker = (E, code) => { const l = E.languages.find(x => x.code === code); return l ? l.marker : MARKERS[code] || code; };
const fold = s => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();

// Tolkien's spelling for a phonetic form (the inverse of toPhonetic, approximately)
const plainForm = form => form.normalize('NFD').replace(/\u0306/g, '').normalize('NFC');   // no breves
function spelling(form, branch) {
  let f = plainForm(form);
  const acute = { 'ā': 'á', 'ē': 'é', 'ī': 'í', 'ō': 'ó', 'ū': 'ú', 'ȳ': 'ý' };
  if (branch === 'quenya') {
    for (const [a, b] of [['ŋkw', 'nqu'], ['ŋgw', 'ngw'], ['kw', 'qu'], ['ks', 'x'], ['ŋk', 'nc'], ['ŋg', 'ng'], ['ŋ', 'ñ'],
      ['j̊', 'hy'], ['w̥', 'hw'], ['l̥', 'hl'], ['r̥', 'hr'], ['xt', 'ht'], ['x', 'h'], ['k', 'c'], ['j', 'y'], ['θ', 'þ']]) f = f.split(a).join(b);
    f = f.replace(/[āēīōūȳ]/g, c => acute[c]);
    return f.replace(/e$/, 'ë');
  }
  for (const [a, b] of [['x', 'ch'], ['θ', 'th'], ['ð', 'dh'], ['l̥', 'lh'], ['r̥', 'rh'], ['m̥', 'mh'], ['ŋg', 'ng'], ['ŋk', 'nc'],
    ['ff', 'ph'], ['k', 'c']]) f = f.split(a).join(b);
  f = f.replace(/ŋ$/, 'ng').replace(/ŋ/g, 'n').replace(/v$/, 'f').replace(/^j/, 'i');
  const mono = (f.match(/[aeiouyáéíóúýāēīōūȳ]+/g) || []).length === 1;
  const circ = { 'ā': 'â', 'ē': 'ê', 'ī': 'î', 'ō': 'ô', 'ū': 'û', 'ȳ': 'ŷ' };
  return f.replace(/[āēīōūȳ]/g, c => (mono ? circ : acute)[c]);
}

function search(slot) {
  const E = engine(state.branch);
  const q = fold($('wf-q' + slot).value.trim());
  const box = $('wf-r' + slot);
  if (!q) { box.innerHTML = ''; return; }
  const neo = $('wf-neo').checked, want = era();
  const hits = [];
  for (const e of E.lexiconList) {
    if ((e.neo && !neo) || eraOf(E, e.lang) !== want) continue;
    const f = fold(e.form), g = fold(e.gloss || '');
    const score = f === q ? 0 : f.startsWith(q) ? 1 : g.split(/[^\p{L}]+/u).includes(q) ? 2 : f.includes(q) ? 3 : g.includes(q) ? 4 : -1;
    if (score >= 0) hits.push([score, e]);
  }
  hits.sort((a, b) => a[0] - b[0] || a[1].form.length - b[1].form.length);
  box.innerHTML = hits.slice(0, 12).map(([, e]) => `<button type="button" data-id="${esc(e.id)}" data-slot="${slot}">
    <span class="marker">${esc(marker(E, e.lang))}</span> <span class="form">${esc(e.form)}</span>${e.neo ? ' <span class="tag">неологизм</span>' : ''}
    <span class="muted">${esc(e.gloss)}</span></button>`).join('') || '<p class="muted">Ничего не найдено.</p>';
}

function describe(E, e) {
  const bits = [];
  if (e.stems) bits.push('основа ' + e.stems.map(s => `<span class="form">${esc(s)}</span>`).join(', '));
  const pr = e.starts || (e.stages && (e.stages.p || e.stages.mp));
  if (pr) bits.push('праформа ' + pr.map(s => `<span class="form">${esc(s)}</span>`).join(', '));
  else bits.push('праформы в Eldamo нет — для ранних стадий она восстанавливается');
  if (e.mark && e.mark !== '#') bits.push(`пометка Eldamo «${esc(e.mark)}»`);
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

function ruleName(E, id) { return E.ruleNames.get(id) || id; }
function traceHtml(E, trace) {
  const steps = trace.filter(t => t[2] != null);
  const skipped = trace.filter(t => t[2] == null);
  if (!steps.length && !skipped.length) return '';
  const li = steps.map(t => `<li><span class="form">${esc(t[1])}</span> → <span class="form">${esc(t[2])}</span>
    <a href="${SITE}words/word-${esc(t[0])}.html" target="_blank" rel="noopener">${esc(ruleName(E, t[0]))}</a></li>`).join('');
  const sk = skipped.length ? `<p class="small muted">Не применены необязательные правила: ${skipped.map(t => esc(ruleName(E, t[0]))).join('; ')}.</p>` : '';
  return `<details><summary>Правила (${steps.length})</summary><ol class="steps">${li}</ol>${sk}</details>`;
}
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
  return out.length ? out.join('; ') + ' — как в засвидетельствованных сложениях' : 'без изменений на стыке';
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
      ${v.score != null ? `<span class="small muted">вес ${v.score}</span>` : ''}${v.stem ? ` <span class="small">основа <span class="form">${esc(v.stem)}-</span></span>` : ''}</div>
      <div class="small">из ${src}</div>
      ${ops ? `<div class="small">${ops}</div>` : ''}${adj ? `<div class="small">${adj}</div>` : ''}
      ${traceHtml(E, v.trace || [])}</li>`;
  }).join('');
  let analog = '';
  if (stage >= last && vs[0].elements) {
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
    <p class="small muted">${stage >= last
      ? 'На последней стадии исторические законы уже отработали: стык и конец сложения подбираются по засвидетельствованным сложениям (частота — «вес»)' + (state.branch === 'quenya' ? ', плюс правила §6.1 учебника Страка.' : ', плюс мягкая мутация второго элемента и правила для многосложных слов.')
      : 'Элементы взяты в формах выбранной стадии и соединены через границу морфем; дальше действуют все последующие правила ветви в порядке Eldamo. Первый вариант — основное чтение (необязательные правила применены).'}
    ${reconstructed ? ' Хотя бы одна праформа восстановлена по соответствиям в деривациях — это гипотеза, а не форма Толкина.' : ''}
    Результат — предсказание формы, а не засвидетельствованное слово.</p>`;
}

function render() {
  const b = currentBranch();
  if (!b) return;
  if (b !== state.branch) {
    state.branch = b; state.picked = [null, null];
    for (const s of [1, 2]) { $('wf-q' + s).value = ''; $('wf-r' + s).innerHTML = ''; $('wf-chosen' + s).innerHTML = ''; }
    $('wf-output').innerHTML = ''; $('wf-go').disabled = true;
  }
  stageOptions();
}

for (const s of [1, 2]) {
  $('wf-q' + s).addEventListener('input', () => search(s));
  $('wf-r' + s).addEventListener('click', e => { const t = e.target.closest('[data-id]'); if (t) pick(s, t.dataset.id); });
}
$('wf-neo').addEventListener('change', () => { search(1); search(2); });
$('wf-go').addEventListener('click', compose);
$('era-select').addEventListener('change', () => { if (state.branch) { stageOptions(); search(1); search(2); } });
window.addEventListener('hashchange', render);
render();
window.WFUI = { pick, compose, spelling, engine };
})();
