// The word at the centre of Quettamin: one search over both branches, the
// card of the chosen word, the panorama of its forms in every period, the
// tabs of the tools. Shared helpers for the tools are exported as window.QU.
(function () {
'use strict';
const WF = window.WF, QR = window.QR;
const WDATA = JSON.parse(document.getElementById('wordform-data').textContent);
// the index of roots (shared/root_index.py): id -> {f, l, g, m, w, instead, see, into, merged, under, here, canon, from, to, words, listed}
const ROOTS = JSON.parse(document.getElementById('roots-data').textContent);
WF.setRoots(ROOTS);           // the engine's roots of a conception (wordform.js: conceptionRoots)
const ROOT_MARKERS = { p: '√', mp: 'ᴹ√', ep: 'ᴱ√', np: 'N√' };
const SITE = 'https://eldamo.org/content/';
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fold = s => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
const BRANCHES = Object.keys(WDATA);
const T = window.I18N.t, TN = window.I18N.tn;
const BRANCH_NAMES = window.I18N.labels({ quenya: 'branch.quenya', sindarin: 'branch.sindarin' });
const ERAS = ['late', 'middle', 'early'];
const ERA_NAMES = window.I18N.labels({ late: 'era.late', middle: 'era.middle', early: 'era.early' });
const NEO_ERA = { nq: 'late', ns: 'late', np: 'late', van: 'late', norths: 'late' };
const NEO_MARKERS = { nq: 'NQ.', ns: 'NS.', np: 'N✶', van: 'Van.', norths: 'NS.' };
const MARKS = window.I18N.labels({
  attested: ['●', 'mark.attested'],
  link: ['↔', 'mark.link'],
  unchanged: ['=', 'mark.unchanged'],
  reconstructed: ['○', 'mark.reconstructed'],
  root: ['√', 'mark.root'],
  stem: ['⊢', 'mark.stem'],
  elements: ['⊕', 'mark.elements'],
  partial: ['⇋', 'mark.partial'],
  irregular: ['!', 'mark.irregular'],
  unconfirmed: ['?', 'mark.unconfirmed'],
  cognate: ['⇄', 'mark.cognate'],
  'near-cognate': ['≈', 'mark.near-cognate'],
  'primitive-attested': ['✶', 'mark.primitive-attested'],
  joint: ['⋈', 'mark.joint'],
  neologism: ['◇', 'mark.neologism'],
  phonotactics: ['⚠', 'mark.phonotactics'],
  main: ['', 'mark.main'],
});
const LINK_NAMES = window.I18N.labels({ combine: 'link.combine', deprecated: 'link.deprecated', cognate: 'link.cognate', see: 'link.see' });

// ---------------------------------------------------------------- engines and lookup
const engines = {};
const engine = b => engines[b] || (engines[b] = WF.makeEngine(b, WDATA[b]));
const allEngines = () => Object.fromEntries(BRANCHES.map(b => [b, engine(b)]));
// where no background thread can be made, the reconstructions run here (compute.js)
const WQ = window.WQ;
WQ.setLocal((src, dst, opts) => WF.reconstruct(allEngines(), src, dst, opts));
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
  return `<a href="#" data-rule="${esc(id)}" data-branch="${esc(info ? info.branch : prefer || '')}" title="${T('rule.inReference')}">${esc(name)}</a>`
    + ` <a href="${SITE}words/word-${esc(id)}.html" target="_blank" rel="noopener" class="ext" title="${T('common.eldamoPage')}" aria-label="${T('common.eldamoPage')}">↗</a>`;
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
  const sk = skipped.length ? `<p class="small muted">${T('stages.skipped')} ${skipped.map(t => ruleLink(t[0], prefer)).join('; ')}.</p>` : '';
  return `${chain}<details class="stages"><summary>${T('stages.title', { n: applied.length })}</summary><ol class="stage-list">${list}</ol>${sk}</details>`;
}
function marksHtml(marks, problems) {
  return marks.filter(m => MARKS[m] && MARKS[m][0]).map(m => `<span class="tag mark-${esc(m)}" title="${esc(MARKS[m][1])}">${esc(MARKS[m][0])} ${esc(MARKS[m][1])}</span>`).join(' ')
    + (problems && problems.length ? ` <span class="muted small">(${esc(problems.map(([k, x]) => T('problem.' + k, { x })).join(', '))})</span>` : '');
}
// a route of the reconstruction: segments [key, params] (wordform.js) -> text
function routeText(route) {
  if (!Array.isArray(route)) return String(route || '');
  // a remark on the step before follows it after a semicolon; what the primitive is, after a colon
  const remark = new Set(['irregularLaw', 'agreedCognate', 'byCognate']);
  return route.map(([k, params], i) => (i === 0 ? '' : route[i - 1][0] === 'sharedPrimitive' ? ': ' : remark.has(k) ? '; ' : T('route.then'))
    + T('route.' + k, params)).join('');
}

// ---------------------------------------------------------------- the subject: a word or a form
let started = false;
let subject = null;          // {kind: 'word'|'form', branch, period, entry?, form?, key}
const listeners = [];
function subjectFrom(p) {
  const rid = p.get('r');
  if (rid) return ROOTS[rid] ? { kind: 'root', key: 'r:' + rid, id: rid, root: ROOTS[rid] } : { kind: 'missing', key: 'r:' + rid, id: rid };
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
    // the elements it was made of in word formation (wordform_ui.js), so that its etymology goes on with it
    const lex = engine(where[0]).lexicon;
    const of = (p.get('of') || '').split(',').filter(Boolean);
    const elements = of.length >= 2 && of.every(x => lex.has(x)) ? of.map(x => lex.get(x)) : [];
    return { kind: 'form', key: `f:${f}@${where.join('/')}${elements.length ? '<' + of.join(',') : ''}`, form: f, branch: where[0], elements,
      period: [where[0], where[1], Number.isFinite(stage) ? stage : lastStage(engine(where[0]), where[1])] };
  }
  return null;
}
// what WF.reconstruct takes for the subject
function sourceOf(s) {
  if (!s) return null;
  if (s.kind === 'form') return (s.elements || []).length ? { form: s.form, elements: s.elements.map(e => e.id) } : { form: s.form };
  // a word of the branch's languages, Neo-Quenya and Neo-Sindarin too (wordform.js: ownLang); another
  // neologism by its spelling at the latest stage
  if (language(engine(s.branch), s.entry.lang) || s.entry.lang === { quenya: 'nq', sindarin: 'ns' }[s.branch]) return { word: s.id };
  return { form: s.entry.form, spelled: true };
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
  return `<button type="button" ${attrs}><span class="marker">${esc(marker(E, e.lang))}</span>${e.alt_lang ? `<span class="marker muted">[${esc(marker(E, e.alt_lang))}]</span>` : ''} <span class="form">${esc(e.form)}</span>`
    + `${e.neo ? ` <span class="tag">${T('tag.neologism')}</span>` : ''}${kind ? ` <span class="tag">${T('tag.' + kind)}</span>` : ''}`
    + ` <span class="muted">${esc(e.gloss)}</span></button>`;
}
function renderSearch() {
  const q = $('q').value;
  const box = $('q-results');
  const hits = searchWords(q, null, 14);
  box.innerHTML = q.trim() ? (hits.map(h => hitHtml(h, `data-word="${esc(h.entry.id)}" data-branch="${esc(h.branch)}"`)).join('')
    || `<p class="muted">${T(neo() ? 'search.none' : 'search.noneHidden')}</p>`) : '';
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
  QR.set({ w: id, b: branch || null, r: null, rp: null, f: null, in: null, of: null, dst: null }, true);
  $('word-section').scrollIntoView({ block: 'start' });
}
function openForm(form, b, era, stage, elements) {
  QR.set({ w: null, r: null, rp: null, f: form, in: `${b}/${era}/${stage}`, of: (elements || []).length ? elements.join(',') : null, dst: null }, true);
  $('word-section').scrollIntoView({ block: 'start' });
}

// ---------------------------------------------------------------- recent words, intro (intro.js)
function remember(s) {
  if (s.kind !== 'word') return;
  const E = engine(s.branch);
  window.QINTRO.remember({ id: s.id, b: s.branch, form: s.entry.form, marker: marker(E, s.entry.lang), gloss: s.entry.gloss || '' });
}
const renderIntro = () => window.QINTRO.render();

// ---------------------------------------------------------------- card
function cardHtml(s) {
  if (s.kind === 'missing') return `<p>${esc(T('card.missing', { id: s.id }))}</p>`;
  const [b, era, stage] = s.period;
  if (s.kind === 'form') {
    return `<div class="word-head"><span class="marker">${esc(periodName(b, era, stage))}</span> <strong class="form big">${esc(shown(s.form, b, era, stage))}</strong>
      ${shown(s.form, b, era, stage) !== s.form ? `<span class="ipa muted">[${esc(s.form)}]</span>` : ''}</div>
      ${(s.elements || []).length ? `<p>${T('card.madeOf')} ${s.elements.map(x => `<a href="#" class="form" data-word="${esc(x.id)}" data-branch="${esc(b)}" title="${esc(x.gloss || '')}">${esc(x.form)}</a>`).join(' + ')}</p>` : ''}
      <p class="small muted">${T((s.elements || []).length ? 'card.formMade' : 'card.formOnly')}</p>`;
  }
  const E = engine(b), e = s.entry;
  const lang = language(E, e.lang);
  const bits = [];
  if (e.stems) bits.push(T('card.stem') + ' ' + e.stems.map(x => `<span class="form">${esc(x)}</span>`).join(', '));
  if (e.roots && e.roots.length) {
    const list = entryRoots(b, e);
    const parts = list.some(r => r.part != null);
    const via = parts && list.some(r => r.via) ? 'element' : (list.find(r => !r.gap) || list[0]).via;
    bits.push(T(via ? 'card.root.' + via : 'card.root') + ' ' + rootsHtml(list));
  }
  const pr = e.starts || (e.stages && (e.stages.p || e.stages.mp || e.stages.ep)) || e.written_origins || e.proto_forms;
  if (pr) bits.push(T('card.primitive') + ' ' + pr.map(x => `<span class="form">${esc(x)}</span>`).join(', '));
  const kind = WF.affixKind(e);
  if (kind) bits.unshift(`${T('tag.' + kind)}, ${T('card.forms')} ${WF.allomorphs(e, b).map(f => `<span class="form">${esc(f)}</span>`).join(', ')}`);
  if (e.mark && e.mark !== '#') bits.push(esc(T('card.mark', { mark: e.mark })));
  const links = Object.entries(e.links || {}).map(([tag, ids]) => {
    const words = ids.map(id => lookup(id, b)).filter(Boolean);
    if (!words.length) return '';
    return `${esc(LINK_NAMES[tag] || tag)}: ${words.map(w => `<a href="#" data-word="${esc(w.entry.id)}" data-branch="${esc(w.branch)}"><span class="marker">${esc(marker(engine(w.branch), w.entry.lang))}</span> <span class="form">${esc(w.entry.form)}</span></a>`).join(', ')}`;
  }).filter(Boolean);
  // the language Eldamo prints in brackets after the word's own (ᴺQ. [ᴱQ.] ulumpë): where the word comes from
  const alt = e.alt_lang ? ` <span class="marker muted" title="${esc(T('card.altLang'))}">[${esc(marker(E, e.alt_lang))}]</span>` : '';
  return `<div class="word-head"><span class="marker" title="${esc(lang ? lang.name : e.lang)}">${esc(marker(E, e.lang))}</span>${alt}
      <strong class="form big">${esc(e.form)}</strong> <span class="gloss">${esc(e.gloss)}</span>
      ${e.neo ? `<span class="tag">${T('tag.neologism')}</span>` : ''}
      <a href="${SITE}words/word-${esc(e.id)}.html" target="_blank" rel="noopener" class="small">${T('common.eldamoPageLower')} ↗</a>
      <a href="graph.html#n-${esc(e.id)}" class="small" title="${esc(T('card.graphTitle'))}">${T('card.graph')}</a></div>
    <div class="small">${esc(BRANCH_NAMES[b])}, ${esc(T('soundRules.era', { era: ERA_NAMES[era] }))}${lang ? ', ' + esc(lang.name) : ''}${bits.length ? ' · ' + bits.join('; ') : ''}</div>
    ${links.length ? `<div class="small">${links.join(' · ')}</div>` : ''}
    ${(e.unruled || []).length ? `<div class="small unruled">${T(e.unruled.length > 1 ? 'card.unruledMany' : 'card.unruledOne')} ${
      e.unruled.map(([code, a, b2]) => `<span class="marker">${esc(marker(E, code))}</span> <span class="form">${esc(a)} → ${esc(b2)}</span>`).join('; ')}.
      ${T('card.unruledNote')}</div>` : ''}
    ${e.starts ? `<div class="small"><a href="#" data-ref-derivations="${esc(e.id)}" data-branch="${esc(b)}">${T('card.derivations')}</a></div>` : ''}
    ${(e.roots || e.root_gaps) ? originTree(s, entryRoots(b, e)) : ''}`;
}

// ---------------------------------------------------------------- the tree of a word's origin
// the paths from the word to its roots (shared/lexicon.py: path) joined where they share a beginning:
// its elements, the words it derives from, and so on down to the roots; a derivation as the
// reference writes it, with the intermediate forms (PE17/135: galadā > ʒalaðā > ʒalðā > alda)
function nodeHtml(id, gapForm) {
  if (ROOTS[id]) return rootRef(id);
  const w = lookup(id);
  if (w) return `<a href="#" data-word="${esc(id)}" data-branch="${esc(w.branch)}" title="${esc(w.entry.gloss)}"><span class="marker">${esc(marker(engine(w.branch), w.entry.lang))}</span> <span class="form">${esc(w.entry.form)}</span></a>`;
  return `<a href="${SITE}words/word-${esc(id)}.html" target="_blank" rel="noopener"><span class="form">${esc(gapForm || id)}</span> ↗</a>`;
}
function writtenHtml(parentId, childId) {
  const w = lookup(parentId);
  const recs = w && w.entry.written ? w.entry.written[childId] || [] : [];
  return recs.map(([src, v, inter]) => ` <span class="small muted">${esc(T('tree.written', { src }))}
    <span class="form">${esc([v, ...inter, w.entry.form].join(' > '))}</span></span>`).join('');
}
function originTree(s, list) {
  const top = { kids: new Map() };
  for (const r of list) {
    for (const path of r.paths) {
      // a root named directly beside a longer way to it from the same place (through a primitive
      // form) is a shortcut of that way: Q. alda < √GAL², and < ✶galadā < √GAL²
      const shortcut = r.paths.some(q => q.length > path.length && path.slice(0, -1).every((st, k) => st[0] === q[k][0] && st[1] === q[k][1]));
      let node = top;
      path.forEach(([rel, id], k) => {
        const key = rel + ':' + id;
        if (!node.kids.has(key)) node.kids.set(key, { rel, id, kids: new Map(), gap: false, form: null, shortcut: false });
        node = node.kids.get(key);
        if (k === path.length - 1) {
          if (r.gap) { node.gap = true; node.form = r.form; }
          if (shortcut) node.shortcut = true;
        }
      });
    }
  }
  if (![...top.kids.values()].some(n => n.kids.size)) return '';       // the roots are named by the word itself
  const render = (node, parent) => `<ul class="origin-tree">${[...node.kids.values()].map(n =>
    `<li><span class="muted small">${esc(T('tree.rel.' + n.rel))}</span> ${nodeHtml(n.id, n.form)}${n.gap ? ` <span class="small muted">${T('tree.noRoot')}</span>` : ''}`
    + `${n.shortcut ? ` <span class="small muted" title="${esc(T('tree.shortcutTitle'))}">${T('tree.shortcut')}</span>` : ''}`
    + `${n.rel === 'd' ? writtenHtml(parent, n.id) : ''}${n.kids.size ? render(n, n.id) : ''}</li>`).join('')}</ul>`;
  return `<details class="origin"><summary>${T('tree.title')}</summary>${render(top, s.id)}</details>`;
}

// ---------------------------------------------------------------- the card of a root
// a root of the index as a link to its card
function rootRef(id) {
  const r = ROOTS[id];
  if (!r) return '';
  return `<a href="#r=${esc(id)}" data-root="${esc(id)}" class="root" title="${esc(r.g)}"><span class="marker">${esc(ROOT_MARKERS[r.l] || '√')}</span><span class="form">${esc(r.f)}</span></a>`;
}
function openRoot(id) {
  $('q-results').hidden = true;
  QR.set({ r: id, rp: null, w: null, f: null, in: null, of: null, dst: null }, true);
  $('word-section').scrollIntoView({ block: 'start' });
}
// a root clicked while a word is open is shown above its panorama, which stays (rp= in the address);
// from a root's own card, or with nothing open, the root becomes the subject
function peekRoot(id) {
  $('q-results').hidden = true;
  QR.set({ rp: id }, true);
}
function renderPeek(id) {
  const box = $('root-peek');
  const r = id && subject && subject.kind !== 'root' ? ROOTS[id] : null;
  box.hidden = !r;
  if (!r) { box.innerHTML = ''; return; }
  box.innerHTML = `<div class="peek-bar"><button type="button" class="link small" data-open-root="${esc(id)}">${T('peek.open')}</button>
      <button type="button" class="peek-close" data-close-peek aria-label="${esc(T('peek.close'))}" title="${esc(T('peek.close'))}">×</button></div>
    ${rootCardHtml({ kind: 'root', id, root: r })}`;
}
document.addEventListener('click', e => {
  const o = e.target.closest('[data-open-root]');
  if (o) { openRoot(o.dataset.openRoot); return; }
  if (e.target.closest('[data-close-peek]')) { QR.set({ rp: null }, true); return; }
  const a = e.target.closest('[data-root]');
  if (!a) return;
  e.preventDefault();
  if (subject && subject.kind !== 'root') {
    peekRoot(a.dataset.root);
    $('root-peek').scrollIntoView({ block: 'nearest' });
  } else openRoot(a.dataset.root);
});
// the words of a root by language: neologisms only with the switch on
const PRIMITIVE_CODES = ['p', 'np', 'mp', 'ep'];
function rootWordsHtml(r) {
  const out = [];
  let hidden = 0;
  const seen = new Set();
  // the words of each branch by language, latest conception first; primitive words once, apart
  const groups = BRANCHES.map(b => ({ b, title: BRANCH_NAMES[b], byLang: new Map() })).concat([{ b: null, title: T('rootCard.primitive'), byLang: new Map() }]);
  for (const b of BRANCHES) {
    const E = engine(b);
    for (const id of (r.words || {})[b] || []) {
      const e = E.lexicon.get(id);
      if (!e || seen.has(id)) continue;
      seen.add(id);
      if (e.neo && !neo()) { hidden++; continue; }
      const g = PRIMITIVE_CODES.includes(e.lang) ? groups[groups.length - 1] : groups.find(x => x.b === b);
      if (!g.byLang.has(e.lang)) g.byLang.set(e.lang, []);
      g.byLang.get(e.lang).push([b, e]);
    }
  }
  for (const g of groups) {
    if (!g.byLang.size) continue;
    const E = engine(g.b || BRANCHES[0]);
    const rank = code => {
      const l = language(E, code);
      return g.b ? ERAS.indexOf(l ? l.era : NEO_ERA[code] || 'late') * 10 - (l ? l.stage : 9) : PRIMITIVE_CODES.indexOf(code);
    };
    const rows = [...g.byLang.keys()].sort((x, y) => rank(x) - rank(y)).map(code => {
      const ws = g.byLang.get(code).sort((x, y) => fold(x[1].form) < fold(y[1].form) ? -1 : 1);
      return `<li><span class="marker">${esc(marker(E, code))}</span> ${ws.map(([b, e]) =>
        `<a href="#" data-word="${esc(e.id)}" data-branch="${esc(b)}" title="${esc(e.gloss)}"><span class="form">${esc(e.form)}</span></a>`).join(', ')}</li>`;
    }).join('');
    const n = [...g.byLang.values()].reduce((k, x) => k + x.length, 0);
    out.push(`<h3>${esc(g.title)} <span class="muted small">(${TN('n.words', n)})</span></h3><ul class="root-words">${rows}</ul>`);
  }
  if (hidden) out.push(`<p class="small muted">${esc(T('rootCard.neoHidden', { n: hidden }))}</p>`);
  return out.join('') || `<p class="muted">${T('rootCard.noWords')}</p>`;
}
function rootCardHtml(s) {
  const r = s.root, id = s.id;
  const list = ids => (ids || []).filter(x => ROOTS[x]).map(rootRef).join(', ');
  const bits = [];
  const rel = (label, ids) => { const h = list(ids); if (h) bits.push(`<li>${label} ${h}</li>`); };
  rel(T('rootCard.instead'), r.instead);
  rel(T('rootCard.see'), r.see);
  rel(T('rootCard.into'), r.into);
  rel(T('rootCard.merged'), r.merged);
  if (r.under) rel(T('rootCard.under'), [r.under]);
  rel(T('rootCard.here'), r.here);
  if (r.canon && r.canon !== r.under && !(r.into || []).includes(r.canon)) rel(T('rootCard.canon'), [r.canon]);
  rel(T('rootCard.from'), r.from);
  rel(T('rootCard.to'), r.to);
  const warn = (r.w || []).map(w => `<span class="tag warn" title="${esc(T('root.warn.' + w + '.title'))}">⚠ ${esc(T('root.warn.' + w))}</span>`).join(' ');
  const status = r.listed && !(r.w || []).length ? `<span class="tag ok" title="${esc(T('rootCard.recommendedTitle'))}">${T('rootCard.recommended')}</span>` : '';
  const free = r.listed && !(r.w || []).length && !r.words ? `<p class="small">${T('rootCard.free')}</p>` : '';
  const alt = r.al ? ` <span class="marker muted" title="${esc(T('card.altLang'))}">[${esc(ROOT_MARKERS[r.al] || r.al)}]</span>` : '';
  return `<div class="word-head"><span class="marker">${esc(ROOT_MARKERS[r.l] || '√')}</span>${alt} <strong class="form big">${esc(r.f)}</strong>
      <span class="gloss">${esc(r.g)}</span> ${status} ${warn}
      <a href="${SITE}words/word-${esc(id)}.html" target="_blank" rel="noopener" class="small">${T('common.eldamoPageLower')} ↗</a>
      <a href="graph.html#n-${esc(id)}" class="small" title="${esc(T('card.graphTitle'))}">${T('card.graph')}</a></div>
    <div class="small">${esc(T('rootCard.kind', { lang: T('rootCard.lang.' + r.l) }))}${r.m && r.m !== '#' ? ' · ' + esc(T('card.mark', { mark: r.m })) : ''}</div>
    ${bits.length ? `<ul class="small root-rels">${bits.join('')}</ul>` : ''}${free}
    <h2>${T('rootCard.words')}</h2>${rootWordsHtml(r)}`;
}
$('neo-toggle').addEventListener('change', () => {
  if (subject && subject.kind === 'root') $('word-card').innerHTML = rootCardHtml(subject);
  renderPeek(QR.get().get('rp'));
});

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
  for (const m of ['attested', 'link', 'near-cognate', 'elements', 'neologism', 'unchanged']) if (v.marks.includes(m)) return MARKS[m][0];
  return '○';
}
// roots by era: of the word itself and of the words Eldamo links to it (cognates, earlier and later
// conceptions); a root belongs to the era of the word that names it (Q. lár < ᴹ√DAR: late)
let linkIndex = null;
function linkedIds(id) {
  if (!linkIndex) {
    linkIndex = new Map();
    for (const b of BRANCHES) for (const e of engine(b).lexiconList) for (const ids of Object.values(e.links || {})) {
      for (const t of ids) {
        if (!linkIndex.has(e.id)) linkIndex.set(e.id, new Set());
        if (!linkIndex.has(t)) linkIndex.set(t, new Set());
        linkIndex.get(e.id).add(t); linkIndex.get(t).add(e.id);
      }
    }
  }
  return [...(linkIndex.get(id) || [])];
}
// the roots of an entry as records for rootsHtml
function entryRoots(b, e) {
  const E = engine(b);
  const out = (e.root_refs || []).map(([lang, id, via, part, paths], i) => ({ id, form: e.roots[i], marker: rootMarker(E, lang), via: via || '', part, paths: paths || [] }));
  // an element without a root, in its place (S. Adanel = √ATATA + ✶-iel)
  for (const [part, lang, id, form, path] of e.root_gaps || []) out.push({ id, form, marker: (language(E, lang) || {}).marker || '', part, gap: true, paths: [path || []] });
  return out.sort((x, y) => (x.part ?? -1) - (y.part ?? -1));
}
// roots by era: the word's own for its era. For another era, first the roots Eldamo puts in place of
// the word's own there -- the root advised instead of it (ᴱ√QḶÐḶ: use N√KWILID), the one it is merged
// into or filed under (root_index.py); then those of the first word Eldamo links to it in that era, an
// earlier or later conception first, in Eldamo's order (Q. Ambar: ᴱQ. irmin < ᴱ√IÐI). A cognate of the
// same era does not add its roots to the word's (S. Gwahaedir, linked to Q. palantír).
const LINK_ORDER = { combine: 0, deprecated: 1, see: 2, cognate: 3 };
const ROOT_ERA = { p: 'late', np: 'late', mp: 'middle', ep: 'early' };
// roots standing for a root in other eras: [[era, id]], nearest first (wordform.js)
const rootCounterparts = id => WF.rootCounterparts(id);
// two roots alike in sound (wordform.js: rootsAlike; ᴱ√FAKA 'cut' is not ᴹ√RIS)
const rootsAlike = (a, b) => WF.rootsAlike(a, b);
// roots of a conception by their form (√LIN² of ᴹ√LIN²), for a root the index links to nothing there
let rootsByForm = null;
const formKey = f => String(f).replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰]/g, '');      // the number of a homonym aside
function sameFormRoot(id, era) {
  if (!rootsByForm) {
    rootsByForm = new Map();
    for (const [x, r] of Object.entries(ROOTS)) {
      const k = ROOT_ERA[r.l] + '|' + formKey(r.f);
      if (!rootsByForm.has(k)) rootsByForm.set(k, []);
      rootsByForm.get(k).push(x);
    }
  }
  const r = ROOTS[id];
  if (!r) return null;
  const hits = rootsByForm.get(era + '|' + formKey(r.f)) || [];
  return hits.length === 1 ? hits[0] : null;     // homonyms (LAK¹, LAK²) of another numbering: not guessed
}
// the roots of a word in another conception, part by part: for each part of its own roots, the root
// Eldamo puts in its place there (rootCounterparts: advised instead, merged, filed under), else a root
// of the same form there, else the roots there of the element the part comes from (ᴹQ. latimbe in
// Latimberista); a part with none keeps its own root, marked as one of another conception (rather
// than a root guessed from the primitive form). {roots, complete}, or null for a word without roots.
function mappedRoots(own, era, depth = 0) {
  const parts = new Map();
  for (const r of own) if (!r.gap) { const k = r.part ?? -1; if (!parts.has(k)) parts.set(k, []); parts.get(k).push(r); }
  if (!parts.size) return null;
  const out = [];
  let found = 0;
  for (const [k, rs] of parts) {
    const part = k < 0 ? null : k;
    const mk = id => ({ id, form: ROOTS[id].f, marker: ROOT_MARKERS[ROOTS[id].l] || '√', via: 'instead', part });
    // only a root that sounds alike: Eldamo also files a root under another of the same meaning
    // (ᴱ√FAKA 'cut' under ᴹ√RIS), which would be a translation, not this root's history
    const hit = rs.flatMap(r => rootCounterparts(r.id).map(c => [...c, r])).find(([e, x, r]) => e === era && rootsAlike(ROOTS[x].f, r.form));
    if (hit) { out.push(mk(hit[1])); found++; continue; }
    const same = rs.map(r => sameFormRoot(r.id, era)).find(Boolean);
    if (same) { out.push(mk(same)); found++; continue; }
    // the word the part comes from, nearest the root (Latimberista < latimbe < imbe < ᴹ√IMBE: imbe), in that conception
    const wordOf = path => [...(path || [])].reverse().map(st => st[1]).find(x => { const w = lookup(x); return w && w.entry.speech !== 'root'; });
    const els = [...new Set(rs.map(r => wordOf((r.paths || [])[0])).filter(Boolean))];
    let byEl = null;
    if (depth < 2) for (const x of els) {
      const w = lookup(x);
      const rr = w && rootsByEra({ kind: 'word', branch: w.branch, entry: w.entry }, depth + 1)[era];
      if (rr && rr.length && !rr.some(r => r.via === 'borrowed')) { byEl = rr; break; }
    }
    if (byEl) { out.push(...byEl.map(r => ({ ...r, part }))); found++; continue; }
    out.push(...rs.map(r => ({ ...r, part, via: 'borrowed' })));
  }
  return { roots: out, complete: found === parts.size };
}
function rootsByEra(s, depth = 0) {
  const out = {};
  if (s && s.kind === 'form' && (s.elements || []).length) {
    // a word made in word formation: its elements' roots, era by era, each element a part of its own
    const per = s.elements.map(e => rootsByEra({ kind: 'word', branch: s.branch, entry: e }));
    for (const era of ERAS) {
      if (!per.every(r => (r[era] || []).length)) continue;
      out[era] = per.flatMap((r, k) => r[era].map(x => ({ ...x, part: k * 100 + (x.part ?? 0) })));
    }
    return out;
  }
  if (!s || s.kind !== 'word') return out;
  const own = eraOf(engine(s.branch), s.entry.lang);
  const ownRoots = (s.entry.roots || []).length ? entryRoots(s.branch, s.entry) : [];
  if (own && ownRoots.length) out[own] = ownRoots;
  // all parts placed in another conception first; then the roots of a word Eldamo links to the
  // word there; then what is placed in part (the rest kept from the word's own conception)
  const partial = {};
  for (const era of ERAS) {
    if (era === own || out[era]) continue;
    const m = mappedRoots(ownRoots, era, depth);
    if (m && m.complete) out[era] = m.roots;
    else if (m) partial[era] = m.roots;
  }
  const linked = [];
  linkedIds(s.entry.id).forEach((id, k) => {
    const w = lookup(id, s.branch);
    if (!w || !(w.entry.roots || []).length) return;
    const era = eraOf(engine(w.branch), w.entry.lang);
    if (!era || era === own) return;
    const tags = [...Object.entries(s.entry.links || {}), ...Object.entries(w.entry.links || {})]
      .filter(([, ids]) => ids.includes(id) || ids.includes(s.entry.id)).map(([t]) => LINK_ORDER[t] ?? 9);
    linked.push([Math.min(9, ...tags), k, era, w]);
  });
  linked.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  for (const [, , era, w] of linked) if (!out[era]) out[era] = entryRoots(w.branch, w.entry);
  for (const [era, rs] of Object.entries(partial)) if (!out[era]) out[era] = rs;
  return out;
}
// roots written as Eldamo's parts: elements joined by +, alternatives of one element by /
function rootsHtml(list) {
  const groups = [];
  for (const r of list || []) {
    const key = r.part == null ? 'own' : 'p' + r.part;
    let g = groups.find(x => x.key === key);
    if (!g) groups.push(g = { key, items: [] });
    g.items.push(rootLink(r));
  }
  return groups.map(g => g.items.join('/')).join(' + ');
}
const rootMarker = (E, lang) => { const l = language(E, lang); return ROOT_MARKERS[lang] || (l ? l.marker.replace('✶', '√') : '√'); };
// a root as a link to its Eldamo page: own, of the word's elements, of a cognate, or guessed
function rootLink(r) {
  if (r.gap) return `<a href="${SITE}words/word-${esc(r.id)}.html" target="_blank" rel="noopener" class="root gap" title="${esc(T('root.gapTitle'))}"><span class="marker">${esc(r.marker)}</span><span class="form">${esc(r.form)}</span></a>`;
  const title = T(r.guess ? 'root.guessTitle' : r.via ? 'root.via.' + r.via : 'panorama.rootTitle');
  // a root of the index opens its card here; the card links to Eldamo
  const href = ROOTS[r.id] ? `href="#r=${esc(r.id)}" data-root="${esc(r.id)}"` : `href="${SITE}words/word-${esc(r.id)}.html" target="_blank" rel="noopener"`;
  return `<a ${href} class="root${r.via ? ' via' : ''}${r.via === 'borrowed' ? ' borrowed' : ''}${r.guess ? ' guess' : ''}" title="${esc(title)}">${r.guess ? '?' : ''}<span class="marker">${esc(r.marker)}</span><span class="form">${esc(r.form)}</span></a>`;
}
// roots of Eldamo the primitive form could come from (wordform.js: rootCandidates): the best ones
function rootGuess(b, era, form) {
  const E = engine(b);
  const cs = WF.rootCandidates(E, form, era, 5);
  if (!cs.length) return [];
  return cs.filter(c => c[0] === cs[0][0]).slice(0, 3).map(([, id, lang, f]) => ({ id, form: f, marker: rootMarker(E, lang), guess: true }));
}
function rootsCell(list, key) {
  return `<td class="proots" data-roots="${esc(key)}">${rootsHtml(list)}</td>`;
}
function renderPanorama(s) {
  const gen = ++generation;
  WQ.cancel('panorama');
  const box = $('panorama');
  if (!s || s.kind === 'missing') { box.innerHTML = ''; return; }
  const src = s.period, opts = sourceOf(s);
  const rows = periods();
  const maxMid = Math.max(...rows.map(r => r.langs.length - 2));
  const roots = rootsByEra(s);
  const withRoots = true;            // Eldamo's roots, else guessed from the primitive form of the row
  const head = `<tr><th scope="col"></th>${withRoots ? `<th scope="col">${T('panorama.roots')}</th>` : ''}<th scope="col">${T('panorama.primitive')}</th>${maxMid > 0 ? `<th scope="col" colspan="${maxMid}">${T('panorama.middle')}</th>` : ''}<th scope="col">${T('panorama.language')}</th></tr>`;
  const cell = (b, era, l) => {
    const own = (src[0] === b || l.stage === 0) && src[1] === era && src[2] === l.stage;
    return `<td><button type="button" class="pcell${own ? ' own' : ''}" data-cell="${esc(`${b}/${era}/${l.stage}`)}" aria-label="${esc(l.marker + ' ' + l.name)}">
      <span class="marker">${esc(l.marker)}</span> <span class="pform form">…</span></button></td>`;
  };
  // the roots and the primitive form of a conception are one for both branches (Primitive Elvish is
  // their common ancestor; wordform.js: primitives): one cell over the rows of the conception
  const body = rows.map((r, i) => {
    const first = r.langs[0], last = r.langs[r.langs.length - 1], mid = r.langs.slice(1, -1);
    const pad = maxMid - mid.length;
    const span = rows.filter(x => x.era === r.era).length;
    const lead = i === 0 || rows[i - 1].era !== r.era;
    const pb = rows.some(x => x.era === r.era && x.b === src[0]) ? src[0] : r.b;     // the branch it is computed for
    const shared = lead ? `${withRoots ? rootsCell(roots[r.era], r.era).replace('<td', `<td rowspan="${span}"`) : ''}${cell(pb, r.era, first).replace('<td', `<td rowspan="${span}"`)}` : '';
    return `<tr${lead ? ' class="era-first"' : ''}><th scope="row">${esc(ERA_NAMES[r.era])} · ${esc(BRANCH_NAMES[r.b])}</th>${shared}${mid.map(l => cell(r.b, r.era, l)).join('')}${pad > 0 ? `<td colspan="${pad}"></td>` : ''}${last !== first ? cell(r.b, r.era, last) : '<td></td>'}</tr>`;
  }).join('');
  box.innerHTML = `<h2>${T('panorama.title')}</h2>
    <div class="table-scroll"><table class="panorama"><thead>${head}</thead><tbody>${body}</tbody></table></div>
    <p class="small muted legend">${T('panorama.legend')}</p>`;
  // the cells are computed in the background (compute.js), in order; the page answers meanwhile
  const fill = (btn, vs) => {
    const [b, era, stage] = btn.dataset.cell.split('/');
    const out = btn.querySelector('.pform');
    if (!vs.length) { out.textContent = '—'; btn.classList.add('empty'); btn.title = T('panorama.noForms'); }
    else {
      const v = vs[0];
      out.textContent = shown(v.form, b, era, Number(stage));
      btn.insertAdjacentHTML('beforeend', ` <span class="sym" aria-hidden="true">${cellSymbol(v)}</span>${v.marks.includes('phonotactics') ? '<span class="sym warn" aria-hidden="true">⚠</span>' : ''}`
);
      btn.title = `${routeText(v.route)} · ${T('variant.weight', { w: v.score })}` + (vs.length > 1 ? ` · ${T('panorama.more', { n: vs.length - 1 })}` : '');
      if (v.marks.includes('attested') || v.marks.includes('link') || v.marks.includes('near-cognate')) btn.classList.add('attested');
      else if (v.marks.includes('neologism')) btn.classList.add('neologism');
      if (Number(stage) === 0 && !(roots[era] || []).length) {
        const td = box.querySelector(`[data-roots="${era}"]`);
        if (td) td.innerHTML = rootGuess(b, era, v.form).map(rootLink).join('/');
      }
    }
  };
  for (const btn of box.querySelectorAll('[data-cell]')) {
    const [b, era, stage] = btn.dataset.cell.split('/');
    WQ.reconstruct(src, [b, era, Number(stage)], Object.assign({ limit: 4 }, opts), 'panorama')
      .then(vs => { if (gen === generation) fill(btn, vs); },
        err => { if (err === WQ.CANCELLED || gen !== generation) return; console.warn(err); fill(btn, []); });
  }
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
  showTab(['compose', 'roots'].includes(p.get('tab')) ? p.get('tab') : 'recon');
  const s = subjectFrom(p);
  const key = s ? s.key : '';
  if (started && (subject ? subject.key : '') === key) { renderPeek(p.get('rp')); return; }
  started = true;
  subject = s;
  $('intro').hidden = !!s;
  $('word-card').hidden = !s;
  if (!s) { renderIntro(); renderPanorama(null); }
  else if (s.kind === 'root') { $('word-card').innerHTML = rootCardHtml(s); renderPanorama(null); }
  else { $('word-card').innerHTML = cardHtml(s); remember(s); renderPanorama(s); }
  renderPeek(p.get('rp'));
  document.title = s && s.kind === 'word' ? `${s.entry.form} — Quettamin` : s && s.kind === 'form' ? `${s.form} — Quettamin`
    : s && s.kind === 'root' ? `${ROOT_MARKERS[s.root.l] || '√'}${s.root.f} — Quettamin` : T('page.title');
  // the tools work on words and forms; a root's card leaves them as they were
  if (s && s.kind === 'root') return;
  for (const l of listeners) l(s, 'subject');
}
QR.on(route);
// another language: the same subject drawn again (the panorama too: its titles are words of the interface)
window.addEventListener('quettamin:lang', () => {
  if (!subject) renderIntro();
  else if (subject.kind === 'root') $('word-card').innerHTML = rootCardHtml(subject);
  else { $('word-card').innerHTML = cardHtml(subject); renderPanorama(subject); }
  renderPeek(QR.get().get('rp'));
  if (!$('q-results').hidden) renderSearch();
  document.title = subject && subject.kind === 'word' ? `${subject.entry.form} — Quettamin` : subject && subject.kind === 'form' ? `${subject.form} — Quettamin`
    : subject && subject.kind === 'root' ? `${ROOT_MARKERS[subject.root.l] || '√'}${subject.root.f} — Quettamin` : T('page.title');
});

window.QU = {
  WDATA, BRANCHES, BRANCH_NAMES, ERAS, ERA_NAMES, MARKS, SITE,
  esc, fold, engine, allEngines, lookup, language, marker, eraOf, lastStage, periodOf, periodName,
  T, TN, spelling, plainForm, shown, ruleLink, rootGuess, rootLink, rootsHtml, stagesHtml, marksHtml, routeText, searchWords, hitHtml, sourceOf,
  neo, openWord, openForm, showTab,
  subject: () => (subject && subject.kind === 'root' ? null : subject),
  ROOTS, ROOT_MARKERS, rootRef, openRoot,
  onSubject: fn => listeners.push(fn),
  start: () => route(QR.get()),
};
window.WFUI = { engine, spelling };     // kept for the parity test
})();
