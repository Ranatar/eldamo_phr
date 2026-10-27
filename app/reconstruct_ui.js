// The "Реконструкция" tab: the form of the chosen word (or of a typed form) for
// another period of either branch (wordform.js: reconstruct).
(function () {
'use strict';
const WF = window.WF, QU = window.QU, QR = window.QR;
const $ = id => document.getElementById(id);
const esc = QU.esc;
const T = QU.T;

function periodSelect(sel) {
  const prev = sel.value;
  const groups = [];
  for (const b of QU.BRANCHES) {
    const g = document.createElement('optgroup');
    g.label = QU.BRANCH_NAMES[b];
    for (const era of QU.ERAS) {
      for (const l of QU.engine(b).languages.filter(x => x.era === era).sort((x, y) => x.stage - y.stage)) {
        g.appendChild(new Option(`${QU.ERA_NAMES[era]}: ${l.marker} ${l.name}`, `${b}|${era}|${l.stage}`));
      }
    }
    groups.push(g);
  }
  sel.replaceChildren(...groups);
  if (prev && [...sel.options].some(o => o.value === prev)) sel.value = prev;
}
const parse = v => { const [b, era, stage] = v.split('|'); return [b, era, Number(stage)]; };
const codeOf = ([b, era, stage]) => (QU.engine(b).languages.find(l => l.era === era && l.stage === stage) || {}).code;
const bareKey = f => QU.fold(String(f).replace(/[¹²³⁴⁵⁶⁷⁸⁹]/g, '')).replace(/^-+|-+$/g, '').trim();

// words of the lexicon for a typed form: those of the source period's language first
function lexiconHits(text) {
  const code = codeOf(parse($('rc-src').value));
  return QU.searchWords(text, null, 40)
    .map((h, k) => [h.entry.lang === code ? 0 : 1, k, h]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).map(t => t[2]);
}
function exactWord(text) {
  const code = codeOf(parse($('rc-src').value)), key = bareKey(text);
  const hits = lexiconHits(text).filter(h => h.entry.lang === code && bareKey(h.entry.form) === key);
  return hits.length === 1 ? hits[0] : null;
}
function suggest() {
  const text = $('rc-form').value, box = $('rc-r');
  if (!text.trim()) { box.innerHTML = ''; return; }
  const hits = lexiconHits(text).slice(0, 10);
  box.innerHTML = hits.map(h => QU.hitHtml(h, `data-word="${esc(h.entry.id)}" data-branch="${esc(h.branch)}"`)).join('')
    + `<p class="small muted">${T(hits.length ? 'recon.pick' : 'recon.noSuch')} ${T('recon.pickNote')}</p>`;
}

function subjectHtml(s) {
  if (!s) return `<p class="muted">${T('recon.chooseWord')}</p>`;
  if (s.kind === 'missing') return `<p class="muted">${T('recon.notFound')}</p>`;
  const [b, era, stage] = s.period;
  const name = s.kind === 'word' ? `<span class="marker">${esc(QU.marker(QU.engine(b), s.entry.lang))}</span> <span class="form">${esc(s.entry.form)}</span> <span class="muted">${esc(s.entry.gloss)}</span>`
    : `<span class="marker">${esc(QU.periodName(b, era, stage))}</span> <span class="form">${esc(s.form)}</span>`;
  return `<p>${T('recon.word')} ${name}</p>`;
}

function onSubject(s) {
  $('rc-subject').innerHTML = subjectHtml(s);
  $('rc-form').value = '';
  $('rc-r').innerHTML = '';
  if (s && s.period) $('rc-src').value = s.period.join('|');
  $('rc-output').innerHTML = '';
  updateButton();
  const dst = QR.get().get('dst');
  if (s && s.kind !== 'missing' && dst) target(dst.split('/'), true);
}
function updateButton() {
  const s = QU.subject();
  $('rc-go').disabled = !($('rc-form').value.trim() || (s && s.kind !== 'missing'));
}

function target(dst, go) {
  $('rc-dst').value = `${dst[0]}|${dst[1]}|${dst[2]}`;
  if (go) run();
}

function run() {
  const src = parse($('rc-src').value), dst = parse($('rc-dst').value);
  const typed = $('rc-form').value.trim();
  const s = QU.subject();
  let opts, note = '';
  const exact = typed && $('rc-spelled').checked ? exactWord(typed) : null;
  if (exact) {
    opts = { word: exact.entry.id };
    note = `<p class="small">${T('recon.taken')} <a href="#" data-word="${esc(exact.entry.id)}" data-branch="${esc(exact.branch)}">`
      + `<span class="marker">${esc(QU.marker(QU.engine(exact.branch), exact.entry.lang))}</span> <span class="form">${esc(exact.entry.form)}</span></a> `
      + `<span class="muted">${esc(exact.entry.gloss)}</span>.</p>`;
  } else if (typed) opts = { form: typed, spelled: $('rc-spelled').checked };
  else if (s && s.kind !== 'missing') opts = QU.sourceOf(s);
  else { $('rc-output').textContent = T('recon.chooseOrType'); return; }
  const out = $('rc-output');
  QR.set({ dst: dst.join('/') }, false);
  let vs;
  try { vs = WF.reconstruct(QU.allEngines(), src, dst, opts); } catch (err) { out.textContent = T('common.error', { msg: err.message }); throw err; }
  const head = `<p class="result-head"><span class="marker">${esc(QU.periodName(...src))}</span> → <span class="marker">${esc(QU.periodName(...dst))}</span></p>` + note;
  if (!vs.length) {
    out.innerHTML = head + `<p>${T('recon.noForms')}</p>`;
    return;
  }
  const [db, de, ds] = dst;
  // a primitive form: the roots of Eldamo it could come from
  const rootsLine = v => {
    if (ds !== 0) return '';
    const rs = QU.rootGuess(db, de, v.form);
    return rs.length ? `<div class="small">${T('recon.roots')} ${rs.map(QU.rootLink).join('/')}</div>` : '';
  };
  out.innerHTML = head + '<ol class="wf-variants">' + vs.map((v, k) => {
    const sh = QU.shown(v.form, db, de, ds);
    return `<li class="wf-variant${k === 0 ? ' main' : ''}"><div><strong class="form">${esc(sh)}</strong>
      ${sh !== QU.plainForm(v.form) ? `<span class="ipa muted">[${esc(QU.plainForm(v.form))}]</span>` : ''} <span class="small muted">${T('variant.weight', { w: v.score })}</span>
      <button type="button" class="link small" data-use="${esc(v.form)}" title="${T('variant.useTitle')}">${T('variant.use')}</button></div>
      <div class="small">${esc(QU.routeText(v.route))}</div>
      <div class="small">${QU.marksHtml(v.marks, v.problems)}</div>${rootsLine(v)}${QU.stagesHtml(v.steps, db)}</li>`;
  }).join('') + '</ol>' +
    `<p class="small muted">${T('recon.note')}</p>`;
}

periodSelect($('rc-src'));
periodSelect($('rc-dst'));
$('rc-dst').value = 'sindarin|late|3';
$('rc-form').addEventListener('input', () => { updateButton(); suggest(); });
$('rc-src').addEventListener('change', suggest);
$('rc-go').addEventListener('click', run);
$('rc-output').addEventListener('click', e => {
  const u = e.target.closest('[data-use]');
  if (!u) return;
  const [b, era, stage] = parse($('rc-dst').value);
  QU.openForm(u.dataset.use, b, era, stage);
});
QU.onSubject((s, why) => { if (why === 'subject') onSubject(s); });
window.RCUI = { run, target };
})();
