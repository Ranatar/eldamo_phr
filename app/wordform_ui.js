// "Словотворчество" panel of the atlas: pick two words (and a third, if needed), a stage of formation,
// get ranked variants with the rules that produced them (engine: wordform.js).
(function () {
'use strict';
const WF = window.WF, QU = window.QU, QR = window.QR;
const SITE = QU.SITE;
const $ = id => document.getElementById(id);
const esc = QU.esc;
const engine = QU.engine;
const T = QU.T;
const SOURCE = window.I18N.labels({
  attested: 'source.attested',
  stem: 'source.stem',
  dictionary: 'source.dictionary',
  primitive: 'source.primitive',
  computed: 'source.computed',
  reconstructed: 'source.reconstructed',
  'soft-mutation': 'source.soft-mutation',
  suffix: 'source.suffix',
  prefix: 'source.prefix',
});
const ADJUST = window.I18N.labels({
  reduction: 'adjust.reduction',
  lengthening: 'adjust.lengthening',
  shortening: 'adjust.shortening',
  'ima-class': 'adjust.ima-class',
});
const state = { branch: QU.BRANCHES[0], picked: [null, null, null] };
const SLOTS = [1, 2, 3];
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
    || `<p class="muted">${esc(T(QU.neo() ? 'compose.none' : 'compose.noneHidden', { branch: QU.BRANCH_NAMES[state.branch], era: QU.ERA_NAMES[want] }))}</p>`;
}

function describe(E, e) {
  const bits = [];
  if (e.stems) bits.push(T('card.stem') + ' ' + e.stems.map(s => `<span class="form">${esc(s)}</span>`).join(', '));
  const pr = e.starts || (e.stages && (e.stages.p || e.stages.mp));
  if (pr) bits.push(T('card.primitive') + ' ' + pr.map(s => `<span class="form">${esc(s)}</span>`).join(', '));
  else bits.push(T('compose.noPrimitive'));
  if (e.mark && e.mark !== '#') bits.push(esc(T('card.mark', { mark: e.mark })));
  const kind = WF.affixKind(e);
  if (kind) {
    bits.unshift(`${T('tag.' + kind)}, ${T('card.forms')} ${WF.allomorphs(e, E.branch).map(f => `<span class="form">${esc(f)}</span>`).join(', ')}`);
    const ex = (E.affixes.affix[e.id] || {}).examples || [];
    if (ex.length) bits.push(T('compose.attestedIn') + ' ' + ex.map(f => `<span class="form">${esc(f)}</span>`).join(', '));
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
  $('wf-slot3').hidden = !(state.picked[0] && state.picked[1]) && !state.picked[2];
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
  // with three elements the junction is that of the last join: the first two, joined, + the third
  const a = WF.phonemes(WF.comparable(v.head || v.elements[0])), b = WF.phonemes(WF.comparable(v.elements[v.elements.length - 1]));
  const j = junctionText(a, b, v.junction || [0, 0, '']);
  if (j) out.push(T('op.junction') + ' ' + esc(j));
  const [ke, repe] = v.ending || [0, ''];
  if (ke || repe) out.push(`${T('op.end')} -${esc(show(b.slice(b.length - ke)))} → -${esc(show(WF.phonemes(repe)))}`);
  if (v.shortened) out.push(T('op.shortened'));
  if (v.lengthened) out.push(T('op.lengthened'));
  return out.length ? out.join('; ') + T('op.asAttested') : T('op.none');
}

function compose() {
  const E = engine(state.branch);
  const ids = state.picked.filter(Boolean);
  if (!state.picked[0] || !state.picked[1]) return;
  const stage = Number($('wf-stage').value);
  const out = $('wf-output');
  let vs;
  try { vs = WF.predict(E, ids, era(), stage); } catch (err) { out.textContent = T('common.error', { msg: err.message }); throw err; }
  const last = Math.max(...E.languages.filter(l => l.era === era()).map(l => l.stage));
  if (!vs.length) {
    out.innerHTML = `<p>${T('compose.noForms')}</p>`;
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
      ${v.score != null ? `<span class="small muted">${T('variant.weight', { w: v.score })}</span>` : ''}${v.stem ? ` <span class="small">${T('card.stem')} <span class="form">${esc(v.stem)}-</span></span>` : ''}
      <button type="button" class="link small" data-use="${esc(plainForm(v.form))}" title="${T('variant.useTitle')}">${T('variant.use')}</button></div>
      <div class="small">${T('compose.from')} ${src}</div>
      ${ops ? `<div class="small">${ops}</div>` : ''}${adj ? `<div class="small">${adj}</div>` : ''}
      ${traceHtml(E, v.trace || [])}</li>`;
  }).join('');
  let analog = '';
  if (stage >= last && vs[0].affix) {
    const ex = (E.affixes.affix[vs[0].affix] || {}).examples || [];
    analog = ex.length ? `<p class="small">${T('compose.affixWords')} ${ex.map(f => `<span class="form">${esc(f)}</span>`).join(', ')}.</p>`
      : `<p class="small">${T('compose.affixNone')}</p>`;
  } else if (stage >= last && vs[0].elements) {
    const pa = WF.phonemes(WF.comparable(vs[0].head || vs[0].elements[0])), pb = WF.phonemes(WF.comparable(vs[0].elements[vs[0].elements.length - 1]));
    const list = E.analogues[JSON.stringify([pa[pa.length - 1], pb[0]])] || [];
    const groups = new Map();
    for (const [f, op] of list) {
      const key = (op[0] || op[1] || op[2]) ? (op[0] <= 1 && op[1] <= 1 ? junctionText(pa, pb, op) : T('compose.replaced', { rep: op[2] || '∅', a: op[0], b: op[1] })) : T('route.unchanged');
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(f);
    }
    if (list.length) analog = `<p class="small">${esc(T('compose.analogues', { a: pa[pa.length - 1], b: pb[0] }))} `
      + [...groups.entries()].map(([k, fs]) => `${fs.map(f => `<span class="form">${esc(f)}</span>`).join(', ')} (${esc(k)})`).join('; ') + '.</p>';
  }
  out.innerHTML = `<ol class="wf-variants">${rows}</ol>${analog}
    <p class="small muted">${stage >= last && vs[0].affix
      ? T('compose.noteAffix') + T(state.branch === 'quenya' ? 'compose.noteAffixQ' : 'compose.noteAffixS')
      : stage >= last
      ? T('compose.noteLast') + T(state.branch === 'quenya' ? 'compose.noteLastQ' : 'compose.noteLastS')
      : T('compose.noteStage')}
    ${reconstructed ? ' ' + T('compose.noteReconstructed') : ''}
    ${T('compose.notePrediction')}</p>`;
}

function branchOptions() {
  $('wf-branch').replaceChildren(...QU.BRANCHES.map(b => new Option(QU.BRANCH_NAMES[b], b)));
  $('wf-era').replaceChildren(...QU.ERAS.map(e => new Option(QU.ERA_NAMES[e], e)));
}
function reset() {
  state.picked = [null, null, null];
  $('wf-slot3').hidden = true;
  for (const s of SLOTS) { $('wf-q' + s).value = ''; $('wf-r' + s).innerHTML = ''; $('wf-chosen' + s).innerHTML = ''; }
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
for (const s of SLOTS) {
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
  QU.openForm(u.dataset.use, state.branch, era(), Math.max(...E.languages.filter(l => l.era === era()).map(l => l.stage)), state.picked.filter(Boolean));
});
QU.onSubject((s, why) => { if (why === 'subject') onSubject(s); else if (why === 'neo') SLOTS.forEach(search); });
setBranch(state.branch, 'late');
// another language: the selects, the chosen elements and the result drawn again
window.addEventListener('quettamin:lang', () => {
  const b = $('wf-branch').value, e = $('wf-era').value, st = $('wf-stage').value;
  branchOptions();
  $('wf-branch').value = b; $('wf-era').value = e;
  stageOptions();
  $('wf-stage').value = st;
  const E = engine(state.branch);
  SLOTS.forEach((slot, k) => { const x = state.picked[k] && E.lexicon.get(state.picked[k]); if (x) $('wf-chosen' + slot).innerHTML = describe(E, x); search(slot); });
  if ($('wf-output').innerHTML) compose();
});
window.WFCOMPOSE = { pick, compose };
})();
