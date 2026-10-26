// The word at the centre of Quettamin: one search over both branches, the
// card of the chosen word, the panorama of its forms in every period, the
// tabs of the tools. Shared helpers for the tools are exported as window.QU.
(function () {
'use strict';
const WF = window.WF, QR = window.QR;
const WDATA = JSON.parse(document.getElementById('wordform-data').textContent);
const SITE = 'https://eldamo.org/content/';
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fold = s => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
const BRANCHES = Object.keys(WDATA);
const BRANCH_NAMES = { quenya: 'квенья', sindarin: 'синдарин' };
const ERAS = ['late', 'middle', 'early'];
const ERA_NAMES = { late: 'поздняя', middle: 'средняя', early: 'ранняя' };
const NEO_ERA = { nq: 'late', ns: 'late', np: 'late', van: 'late', norths: 'late' };
const NEO_MARKERS = { nq: 'NQ.', ns: 'NS.', np: 'N✶', van: 'Van.', norths: 'NS.' };
const MARKS = {
  attested: ['●', 'засвидетельствовано в Eldamo'], link: ['↔', 'связь Eldamo между статьями'],
  unchanged: ['=', 'форма без изменений'], reconstructed: ['○', 'восстановлено, проверено прогоном вперёд'],
  root: ['√', 'согласуется с корнем слова'], cognate: ['⇄', 'через общую праформу'],
  'primitive-attested': ['✶', 'праформа из Eldamo'], neologism: ['◇', 'переэтимологизация — неологизм, не слово Толкина'],
  phonotactics: ['⚠', 'нетипично для целевого языка'], main: ['', 'основное чтение законов'],
};
const LINK_NAMES = { combine: 'объединено с', deprecated: 'заменено на', cognate: 'когнат', see: 'см.' };

// ---------------------------------------------------------------- engines and lookup
const engines = {};
const engine = b => engines[b] || (engines[b] = WF.makeEngine(b, WDATA[b]));
const allEngines = () => Object.fromEntries(BRANCHES.map(b => [b, engine(b)]));
function lookup(id, prefer) {
  for (const b of prefer ? [prefer, ...BRANCHES.filter(x => x !== prefer)] : BRANCHES) {
    const e = engine(b).lexicon.get(id);
    if (e) return { branch: b, entry: e };
  }
  return null;
}
const language = (E, code) => E.languages.find(l => l.code === code) || null;
const marker = (E, code) => { const l = language(E, code); return l ? l.marker : NEO_MARKERS[code] || code; };
function eraOf(E, code) { const l = language(E, code); return l ? l.era : NEO_ERA[code] || null; }
const lastStage = (E, era) => Math.max(...E.languages.filter(l => l.era === era).map(l => l.stage));
function periodOf(b, e) {
  // [branch, era, stage] of a word's own language; neologisms: the latest stage
  const E = engine(b), l = language(E, e.lang);
  if (l) return [b, l.era, l.stage];
  const era = NEO_ERA[e.lang];
  return era ? [b, era, lastStage(E, era)] : null;
}
function periodName(b, era, stage) {
  const l = engine(b).languages.find(x => x.era === era && x.stage === stage);
  return l ? `${l.marker} ${l.name}` : `${era} ${stage}`;
}

// ---------------------------------------------------------------- spelling
const plainForm = form => form.normalize('NFD').replace(/̆/g, '').normalize('NFC');   // no breves
function spelling(form, branch) {
  // Tolkien's spelling for a phonetic form (the inverse of toPhonetic, approximately)
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
// a form of a period as shown: Tolkien's spelling for the language itself, phonetic notation before it
function shown(form, b, era, stage) {
  const E = engine(b);
  return stage === lastStage(E, era) && era !== 'early' ? spelling(form, b) : plainForm(form);
}

// ---------------------------------------------------------------- rule steps grouped by stage
function ruleInfo(id, prefer) {
  for (const b of prefer ? [prefer, ...BRANCHES.filter(x => x !== prefer)] : BRANCHES) {
    const E = engine(b);
    if (!E.ruleInfo) E.ruleInfo = new Map(E.rules.map(r => [r.id, r]));
    const r = E.ruleInfo.get(id);
    if (r) return { branch: b, rule: r, marker: marker(E, r.lang) };
  }
  return null;
}
function ruleLink(id, prefer) {
  const info = ruleInfo(id, prefer);
  const name = info ? info.rule.name : id;
  return `<a href="#" data-rule="${esc(id)}" data-branch="${esc(info ? info.branch : prefer || '')}" title="Правило в справочнике">${esc(name)}</a>`
    + ` <a href="${SITE}words/word-${esc(id)}.html" target="_blank" rel="noopener" class="ext" title="Статья Eldamo" aria-label="Статья Eldamo">↗</a>`;
}
function stagesHtml(steps, prefer) {
  // [[rule, before, after]] -> stages in order, each with its forms and rules
  const applied = (steps || []).filter(t => t[2] != null);
  const skipped = (steps || []).filter(t => t[2] == null);
  if (!applied.length && !skipped.length) return '';
  const groups = [];
  for (const t of applied) {
    const info = ruleInfo(t[0], prefer);
    const key = info ? info.rule.lang : '?';
    let g = groups[groups.length - 1];
    if (!g || g.key !== key) { g = { key, marker: info ? info.marker : '', from: t[1], to: t[2], rules: [] }; groups.push(g); }
    g.to = t[2];
    g.rules.push(t);
  }
  const chain = groups.length ? `<div class="stage-chain"><span class="form">${esc(plainForm(groups[0].from))}</span>${groups.map(g =>
    ` <span class="arrow">→</span> <span class="marker">${esc(g.marker)}</span> <span class="form">${esc(plainForm(g.to))}</span>`).join('')}</div>` : '';
  const list = groups.map(g => `<li><span class="marker">${esc(g.marker)}</span> <span class="form">${esc(plainForm(g.from))} → ${esc(plainForm(g.to))}</span>
    <ol class="rules">${g.rules.map(t => `<li><span class="form">${esc(plainForm(t[1]))} → ${esc(plainForm(t[2]))}</span> ${ruleLink(t[0], prefer)}</li>`).join('')}</ol></li>`).join('');
  const sk = skipped.length ? `<p class="small muted">Не применены необязательные правила: ${skipped.map(t => ruleLink(t[0], prefer)).join('; ')}.</p>` : '';
  return `${chain}<details class="stages"><summary>Правила по стадиям (${applied.length})</summary><ol class="stage-list">${list}</ol>${sk}</details>`;
}
function marksHtml(marks, problems) {
  return marks.filter(m => MARKS[m] && MARKS[m][0]).map(m => `<span class="tag mark-${esc(m)}" title="${esc(MARKS[m][1])}">${esc(MARKS[m][0])} ${esc(MARKS[m][1])}</span>`).join(' ')
    + (problems && problems.length ? ` <span class="muted small">(${esc(problems.join(', '))})</span>` : '');
}

// ---------------------------------------------------------------- the subject: a word or a form
let started = false;
let subject = null;          // {kind: 'word'|'form', branch, period, entry?, form?, key}
const listeners = [];
function subjectFrom(p) {
  const id = p.get('w');
  if (id) {
    const hit = lookup(id, p.get('b'));
    if (!hit) return { kind: 'missing', key: 'w:' + id, id };
    const period = periodOf(hit.branch, hit.entry);
    return { kind: 'word', key: 'w:' + id, id, branch: hit.branch, entry: hit.entry, period };
  }
  const f = p.get('f'), where = (p.get('in') || '').split('/');
  if (f && BRANCHES.includes(where[0]) && ERAS.includes(where[1])) {
    const stage = Number(where[2]);
    return { kind: 'form', key: `f:${f}@${where.join('/')}`, form: f, branch: where[0], period: [where[0], where[1], Number.isFinite(stage) ? stage : lastStage(engine(where[0]), where[1])] };
  }
  return null;
}
// what WF.reconstruct takes for the subject
function sourceOf(s) {
  if (!s) return null;
  if (s.kind === 'form') return { form: s.form };
  if (language(engine(s.branch), s.entry.lang)) return { word: s.id };
  return { form: s.entry.form, spelled: true };       // a neologism: its spelling at the latest stage
}

// ---------------------------------------------------------------- search
const neo = () => $('neo-toggle').checked;
const folded = new Map();
function searchWords(q, filter, limit = 12) {
  const fq = fold(q.trim());
  if (!fq) return [];
  const hits = [], seen = new Set();
  for (const b of BRANCHES) {
    const E = engine(b);
    for (const e of E.lexiconList) {
      if (seen.has(e.id) || (e.neo && !neo())) continue;
      if (!language(E, e.lang) && !NEO_ERA[e.lang]) continue;
      if (filter && !filter(b, e)) continue;
      let fx = folded.get(e);
      if (!fx) { fx = [fold(e.form), fold(e.gloss || '')]; folded.set(e, fx); }
      const [f, g] = fx;
      const score = f === fq ? 0 : f.startsWith(fq) ? 1 : g.split(/[^\p{L}]+/u).includes(fq) ? 2 : f.includes(fq) ? 3 : g.includes(fq) ? 4 : -1;
      if (score >= 0) { hits.push([score, b, e]); seen.add(e.id); }
    }
  }
  hits.sort((a, c) => a[0] - c[0] || a[2].form.length - c[2].form.length);
  return hits.slice(0, limit).map(([, b, e]) => ({ branch: b, entry: e }));
}
function hitHtml({ branch, entry: e }, attrs) {
  const E = engine(branch);
  const kind = WF.affixKind(e);
  return `<button type="button" ${attrs}><span class="marker">${esc(marker(E, e.lang))}</span> <span class="form">${esc(e.form)}</span>`
    + `${e.neo ? ' <span class="tag">неологизм</span>' : ''}${kind ? ` <span class="tag">${kind === 'suffix' ? 'суффикс' : 'приставка'}</span>` : ''}`
    + ` <span class="muted">${esc(e.gloss)}</span></button>`;
}
function renderSearch() {
  const q = $('q').value;
  const box = $('q-results');
  const hits = searchWords(q, null, 14);
  box.innerHTML = q.trim() ? (hits.map(h => hitHtml(h, `data-word="${esc(h.entry.id)}" data-branch="${esc(h.branch)}"`)).join('')
    || `<p class="muted">Ничего не найдено${neo() ? '' : ' (неологизмы скрыты)'}.</p>`) : '';
  box.hidden = !q.trim();
}
$('q').addEventListener('input', renderSearch);
$('q').addEventListener('keydown', e => {
  if (e.key === 'Enter') { const first = $('q-results').querySelector('[data-word]'); if (first) first.click(); }
  else if (e.key === 'Escape') { $('q-results').hidden = true; }
  else if (e.key === 'ArrowDown') { const first = $('q-results').querySelector('button'); if (first) { e.preventDefault(); first.focus(); } }
});
$('q-results').addEventListener('keydown', e => {
  const b = e.target.closest('button');
  if (!b) return;
  if (e.key === 'ArrowDown' && b.nextElementSibling) { e.preventDefault(); b.nextElementSibling.focus(); }
  else if (e.key === 'ArrowUp') { e.preventDefault(); (b.previousElementSibling || $('q')).focus(); }
  else if (e.key === 'Escape') { $('q-results').hidden = true; $('q').focus(); }
});
document.addEventListener('click', e => { if (!e.target.closest('.search')) $('q-results').hidden = true; });
$('q').addEventListener('focus', () => { if ($('q').value.trim()) renderSearch(); });
$('neo-toggle').addEventListener('change', () => { renderSearch(); for (const l of listeners) l(subject, 'neo'); });

// any [data-word] anywhere opens that word
document.addEventListener('click', e => {
  const w = e.target.closest('[data-word]');
  if (!w) return;
  e.preventDefault();
  openWord(w.dataset.word, w.dataset.branch);
});
function openWord(id, branch) {
  $('q-results').hidden = true;
  $('q').value = '';
  QR.set({ w: id, b: branch || null, f: null, in: null, dst: null }, true);
  $('word-section').scrollIntoView({ block: 'start' });
}
function openForm(form, b, era, stage) {
  QR.set({ w: null, f: form, in: `${b}/${era}/${stage}`, dst: null }, true);
  $('word-section').scrollIntoView({ block: 'start' });
}

// ---------------------------------------------------------------- recent words
const RECENT_KEY = 'quettamin-recent';
function recent() {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]').filter(r => r && r.id); } catch (_e) { return []; }
}
function remember(s) {
  if (s.kind !== 'word') return;
  const E = engine(s.branch);
  const item = { id: s.id, b: s.branch, form: s.entry.form, marker: marker(E, s.entry.lang), gloss: s.entry.gloss || '' };
  const list = [item, ...recent().filter(r => r.id !== s.id)].slice(0, 8);
  try { localStorage.setItem(RECENT_KEY, JSON.stringify(list)); } catch (_e) { /* storage unavailable */ }
}
const chip = r => `<button type="button" class="chip" data-word="${esc(r.id)}" data-branch="${esc(r.b || '')}"><span class="marker">${esc(r.marker)}</span> <span class="form">${esc(r.form)}</span> <span class="muted">${esc(r.gloss)}</span></button>`;

// ---------------------------------------------------------------- intro, card
const EXAMPLES = [
  { id: '403686503', b: 'quenya', marker: 'Q.', form: 'lindë', gloss: 'song, air, tune' },
  { id: '4273482913', b: 'quenya', marker: 'Q.', form: 'Ambar', gloss: 'world' },
  { id: '3005081253', b: 'sindarin', marker: 'S.', form: 'galadh', gloss: 'tree' },
  { id: '3880471189', b: 'quenya', marker: 'Q.', form: 'lelya', gloss: 'delicate, beautiful and fine' },
];
function renderIntro() {
  const rec = recent();
  $('intro').innerHTML = `<h1>Quettamin — кузница слова</h1>
    <p class="lead">Найдите слово квенья или синдарина любого периода — поле поиска наверху. Quettamin покажет его формы во всех
      периодах: засвидетельствованные в лексиконе Eldamo и восстановленные по звуковым законам, — восстановит форму для
      нужной стадии, другой ветви или другой концепции Толкина и построит новые слова: сложения и производные с суффиксами и приставками.</p>
    <p>Например: ${EXAMPLES.map(chip).join(' ')}</p>
    ${rec.length ? `<p>Недавние: ${rec.map(chip).join(' ')}</p>` : ''}
    <p class="small muted">Всё, кроме засвидетельствованного, — гипотеза модели: ответ показывает, на чём он основан. Фонетический справочник
      (правила, пути между звуками, цепочки, деривации Eldamo) — внизу страницы.</p>`;
}
function cardHtml(s) {
  if (s.kind === 'missing') return `<p>Слова с идентификатором ${esc(s.id)} в лексиконе нет.</p>`;
  const [b, era, stage] = s.period;
  if (s.kind === 'form') {
    return `<div class="word-head"><span class="marker">${esc(periodName(b, era, stage))}</span> <strong class="form big">${esc(shown(s.form, b, era, stage))}</strong>
      ${shown(s.form, b, era, stage) !== s.form ? `<span class="ipa muted">[${esc(s.form)}]</span>` : ''}</div>
      <p class="small muted">Форма без статьи Eldamo: восстановленная или построенная. Всё, что выводится из неё, — гипотеза.</p>`;
  }
  const E = engine(b), e = s.entry;
  const lang = language(E, e.lang);
  const bits = [];
  if (e.stems) bits.push('основа ' + e.stems.map(x => `<span class="form">${esc(x)}</span>`).join(', '));
  if (e.roots && e.roots.length) bits.push('корень ' + e.roots.map(x => `<span class="form">${esc(x)}</span>`).join(', '));
  const pr = e.starts || (e.stages && (e.stages.p || e.stages.mp || e.stages.ep)) || e.written_origins || e.proto_forms;
  if (pr) bits.push('праформа ' + pr.map(x => `<span class="form">${esc(x)}</span>`).join(', '));
  const kind = WF.affixKind(e);
  if (kind) bits.unshift(`${kind === 'suffix' ? 'суффикс' : 'приставка'}, формы: ${WF.allomorphs(e, b).map(f => `<span class="form">${esc(f)}</span>`).join(', ')}`);
  if (e.mark && e.mark !== '#') bits.push(`пометка Eldamo «${esc(e.mark)}»`);
  const links = Object.entries(e.links || {}).map(([tag, ids]) => {
    const words = ids.map(id => lookup(id, b)).filter(Boolean);
    if (!words.length) return '';
    return `${esc(LINK_NAMES[tag] || tag)}: ${words.map(w => `<a href="#" data-word="${esc(w.entry.id)}" data-branch="${esc(w.branch)}"><span class="marker">${esc(marker(engine(w.branch), w.entry.lang))}</span> <span class="form">${esc(w.entry.form)}</span></a>`).join(', ')}`;
  }).filter(Boolean);
  return `<div class="word-head"><span class="marker" title="${esc(lang ? lang.name : e.lang)}">${esc(marker(E, e.lang))}</span>
      <strong class="form big">${esc(e.form)}</strong> <span class="gloss">${esc(e.gloss)}</span>
      ${e.neo ? '<span class="tag">неологизм</span>' : ''}
      <a href="${SITE}words/word-${esc(e.id)}.html" target="_blank" rel="noopener" class="small">статья Eldamo ↗</a></div>
    <div class="small">${esc(BRANCH_NAMES[b])}, ${esc(ERA_NAMES[era])} концепция${lang ? ', ' + esc(lang.name) : ''}${bits.length ? ' · ' + bits.join('; ') : ''}</div>
    ${links.length ? `<div class="small">${links.join(' · ')}</div>` : ''}
    ${e.starts ? `<div class="small"><a href="#" data-ref-derivations="${esc(e.id)}" data-branch="${esc(b)}">Деривации Eldamo этого слова в справочнике</a></div>` : ''}`;
}

// ---------------------------------------------------------------- panorama
let generation = 0;
function periods() {
  const rows = [];
  for (const era of ERAS) for (const b of BRANCHES) {
    const langs = engine(b).languages.filter(l => l.era === era).sort((x, y) => x.stage - y.stage);
    if (langs.length) rows.push({ b, era, langs });
  }
  return rows;
}
function cellSymbol(v) {
  for (const m of ['attested', 'link', 'neologism', 'unchanged']) if (v.marks.includes(m)) return MARKS[m][0];
  return '○';
}
function renderPanorama(s) {
  const gen = ++generation;
  const box = $('panorama');
  if (!s || s.kind === 'missing') { box.innerHTML = ''; return; }
  const src = s.period, opts = sourceOf(s);
  const rows = periods();
  const maxMid = Math.max(...rows.map(r => r.langs.length - 2));
  const head = `<tr><th scope="col"></th><th scope="col">праформа</th>${maxMid > 0 ? `<th scope="col" colspan="${maxMid}">промежуточные стадии</th>` : ''}<th scope="col">язык</th></tr>`;
  const cell = (b, era, l) => {
    const own = src[0] === b && src[1] === era && src[2] === l.stage;
    return `<td><button type="button" class="pcell${own ? ' own' : ''}" data-cell="${esc(`${b}/${era}/${l.stage}`)}" aria-label="${esc(l.marker + ' ' + l.name)}">
      <span class="marker">${esc(l.marker)}</span> <span class="pform form">…</span></button></td>`;
  };
  const body = rows.map(r => {
    const first = r.langs[0], last = r.langs[r.langs.length - 1], mid = r.langs.slice(1, -1);
    const pad = maxMid - mid.length;
    return `<tr><th scope="row">${esc(ERA_NAMES[r.era])} · ${esc(BRANCH_NAMES[r.b])}</th>${cell(r.b, r.era, first)}${mid.map(l => cell(r.b, r.era, l)).join('')}${pad > 0 ? `<td colspan="${pad}"></td>` : ''}${last !== first ? cell(r.b, r.era, last) : '<td></td>'}</tr>`;
  }).join('');
  box.innerHTML = `<h2>Панорама периодов</h2>
    <div class="table-scroll"><table class="panorama"><thead>${head}</thead><tbody>${body}</tbody></table></div>
    <p class="small muted legend">● засвидетельствовано · ↔ связь Eldamo · = без изменений · ○ восстановлено законами · ◇ неологизм (переэтимологизация) · ⚠ нетипично для языка.
      Щелчок по клетке — все варианты, маршрут и правила.</p>`;
  const cells = [...box.querySelectorAll('[data-cell]')];
  const all = allEngines();
  let k = 0;
  const step = () => {
    if (gen !== generation || k >= cells.length) return;
    const btn = cells[k++];
    const [b, era, stage] = btn.dataset.cell.split('/');
    const dst = [b, era, Number(stage)];
    let vs = [];
    try { vs = WF.reconstruct(all, src, dst, Object.assign({ limit: 4 }, opts)); } catch (err) { console.warn(err); }
    const out = btn.querySelector('.pform');
    if (!vs.length) { out.textContent = '—'; btn.classList.add('empty'); btn.title = 'Форм не найдено'; }
    else {
      const v = vs[0];
      out.textContent = shown(v.form, b, era, Number(stage));
      btn.insertAdjacentHTML('beforeend', ` <span class="sym" aria-hidden="true">${cellSymbol(v)}</span>${v.marks.includes('phonotactics') ? '<span class="sym warn" aria-hidden="true">⚠</span>' : ''}`
);
      btn.title = `${v.route} · вес ${v.score}` + (vs.length > 1 ? ` · ещё вариантов: ${vs.length - 1}` : '');
      if (v.marks.includes('attested')) btn.classList.add('attested');
      else if (v.marks.includes('neologism')) btn.classList.add('neologism');
    }
    setTimeout(step, 0);
  };
  setTimeout(step, 0);
}
$('panorama').addEventListener('click', e => {
  const c = e.target.closest('[data-cell]');
  if (!c) return;
  QR.set({ tab: 'recon', dst: c.dataset.cell }, false);
  showTab('recon');
  if (window.RCUI) window.RCUI.target(c.dataset.cell.split('/'), true);
  $('tools').scrollIntoView({ behavior: 'smooth', block: 'start' });
});

// ---------------------------------------------------------------- tabs
function showTab(name) {
  for (const t of document.querySelectorAll('[role=tab]')) {
    const on = t.dataset.tab === name;
    t.setAttribute('aria-selected', String(on));
    t.tabIndex = on ? 0 : -1;
    $(t.getAttribute('aria-controls')).hidden = !on;
  }
}
document.querySelector('[role=tablist]').addEventListener('click', e => {
  const t = e.target.closest('[role=tab]');
  if (!t) return;
  showTab(t.dataset.tab);
  QR.set({ tab: t.dataset.tab }, false);
});
document.querySelector('[role=tablist]').addEventListener('keydown', e => {
  if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
  const tabs = [...document.querySelectorAll('[role=tab]')];
  const i = tabs.indexOf(document.activeElement);
  const next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
  next.focus(); next.click();
});

// ---------------------------------------------------------------- routing
function route(p) {
  showTab(p.get('tab') === 'compose' ? 'compose' : 'recon');
  const s = subjectFrom(p);
  const key = s ? s.key : '';
  if (started && (subject ? subject.key : '') === key) return;
  started = true;
  subject = s;
  $('intro').hidden = !!s;
  $('word-card').hidden = !s;
  if (!s) { renderIntro(); renderPanorama(null); }
  else { $('word-card').innerHTML = cardHtml(s); remember(s); renderPanorama(s); }
  document.title = s && s.kind === 'word' ? `${s.entry.form} — Quettamin` : s && s.kind === 'form' ? `${s.form} — Quettamin` : 'Quettamin — кузница слова';
  for (const l of listeners) l(s, 'subject');
}
QR.on(route);

window.QU = {
  WDATA, BRANCHES, BRANCH_NAMES, ERAS, ERA_NAMES, MARKS, SITE,
  esc, fold, engine, allEngines, lookup, language, marker, eraOf, lastStage, periodOf, periodName,
  spelling, plainForm, shown, ruleLink, stagesHtml, marksHtml, searchWords, hitHtml, sourceOf,
  neo, openWord, openForm, showTab,
  subject: () => subject,
  onSubject: fn => listeners.push(fn),
  start: () => route(QR.get()),
};
window.WFUI = { engine, spelling };     // kept for the parity test
})();
