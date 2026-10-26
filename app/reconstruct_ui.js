// The "Реконструкция" tab: the form of the chosen word (or of a typed form) for
// another period of either branch (wordform.js: reconstruct).
(function () {
'use strict';
const WF = window.WF, QU = window.QU, QR = window.QR;
const $ = id => document.getElementById(id);
const esc = QU.esc;

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

function subjectHtml(s) {
  if (!s) return '<p class="muted">Выберите слово в поиске наверху или введите форму ниже.</p>';
  if (s.kind === 'missing') return '<p class="muted">Слово не найдено.</p>';
  const [b, era, stage] = s.period;
  const name = s.kind === 'word' ? `<span class="marker">${esc(QU.marker(QU.engine(b), s.entry.lang))}</span> <span class="form">${esc(s.entry.form)}</span> <span class="muted">${esc(s.entry.gloss)}</span>`
    : `<span class="marker">${esc(QU.periodName(b, era, stage))}</span> <span class="form">${esc(s.form)}</span>`;
  return `<p>Слово: ${name}</p>`;
}

function onSubject(s) {
  $('rc-subject').innerHTML = subjectHtml(s);
  $('rc-form').value = '';
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
  let opts;
  if (typed) opts = { form: typed, spelled: $('rc-spelled').checked };
  else if (s && s.kind !== 'missing') opts = QU.sourceOf(s);
  else { $('rc-output').textContent = 'Выберите слово или введите форму.'; return; }
  const out = $('rc-output');
  QR.set({ dst: dst.join('/') }, false);
  let vs;
  try { vs = WF.reconstruct(QU.allEngines(), src, dst, opts); } catch (err) { out.textContent = 'Ошибка: ' + err.message; throw err; }
  const head = `<p class="result-head"><span class="marker">${esc(QU.periodName(...src))}</span> → <span class="marker">${esc(QU.periodName(...dst))}</span></p>`;
  if (!vs.length) {
    out.innerHTML = head + '<p>Форм не найдено: ни одна восстановленная форма не даёт исходную при прогоне вперёд. Попробуйте другую стадию или введите форму в фонетической записи.</p>';
    return;
  }
  const [db, de, ds] = dst;
  out.innerHTML = head + '<ol class="wf-variants">' + vs.map((v, k) => {
    const sh = QU.shown(v.form, db, de, ds);
    return `<li class="wf-variant${k === 0 ? ' main' : ''}"><div><strong class="form">${esc(sh)}</strong>
      ${sh !== QU.plainForm(v.form) ? `<span class="ipa muted">[${esc(QU.plainForm(v.form))}]</span>` : ''} <span class="small muted">вес ${v.score}</span>
      <button type="button" class="link small" data-use="${esc(v.form)}" title="Сделать эту форму текущим словом">работать с этой формой</button></div>
      <div class="small">${esc(v.route)}</div>
      <div class="small">${QU.marksHtml(v.marks, v.problems)}</div>${QU.stagesHtml(v.steps, db)}</li>`;
  }).join('') + '</ol>' +
    '<p class="small muted">Назад по стадиям форма восстанавливается по соответствиям из дериваций Eldamo, и каждая кандидатура проверяется прогоном вперёд. ' +
    'Другая ветвь — через общую праформу. Другая концепция — сначала связи Eldamo, затем форма без изменений, затем переэтимологизация (неологизм). ' +
    'Кроме засвидетельствованного, всё — гипотеза модели.</p>';
}

periodSelect($('rc-src'));
periodSelect($('rc-dst'));
$('rc-dst').value = 'sindarin|late|3';
$('rc-form').addEventListener('input', updateButton);
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
