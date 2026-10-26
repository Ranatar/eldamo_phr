"use strict";
(function () {
const DATA = JSON.parse(document.getElementById('atlas-data').textContent);
const SITE = 'https://eldamo.org/content/';
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const NULL = 'ø';
const ERAS = ['late', 'middle', 'early'];
const ERA_NAMES = { late: 'поздняя', middle: 'средняя', early: 'ранняя' };

// ---------- small helpers ---------------------------------------------------
function plural(n, one, few, many) {
  const a = Math.abs(n) % 100, b = a % 10;
  if (a > 10 && a < 20) return many;
  if (b === 1) return one;
  if (b >= 2 && b <= 4) return few;
  return many;
}
const count = (n, one, few, many) => `${n} ${plural(n, one, few, many)}`;
const wordUrl = id => id ? `${SITE}words/word-${id}.html` : '';
function sourceLink(src) {
  if (!src) return '';
  const book = src.split('/')[0];
  const label = src.split('.')[0];
  return `<a href="${esc(SITE + 'references/ref-' + book + '.html#' + src)}" target="_blank" rel="noopener">${esc(label)}</a>`;
}
const store = {
  get(k) { try { return localStorage.getItem(k); } catch (_e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (_e) { /* storage unavailable */ } },
};
const POSITION = { initial: 'в начале слова', final: 'в конце слова', medial: 'в середине слова' };
const TRANSITION = { stage: 'следующая языковая ступень', ordered: 'порядок подтверждён Eldamo', unknown: 'порядок не установлен' };
const STATUS = {
  reproduced: ['✓', 'формула воспроизводит шаг'],
  reproduced_partial: ['≈', 'воспроизводится применением в одной позиции'],
  mismatch: ['✗', 'формула даёт другой результат'],
  no_match: ['✗', 'формула не применима к предыдущей форме'],
  unsupported: ['?', 'нотация вне документированной'],
  unknown_rule: ['·', 'правило в Eldamo не указано'],
  unmatched_formula: ['?', 'формула не найдена среди правил'],
  identity: ['=', 'исключение правила: звук сохраняется'],
  deleted_rule: ['·', 'правило удалено Толкином'],
};
function announce(text) { $('status').textContent = text; }
const ISSUE = new Set(['mismatch', 'no_match', 'unsupported', 'unmatched_formula']);
const GRADE = DATA.grades || {
  A: 'засвидетельствована в одной деривации', B: 'шаги засвидетельствованы, порядок подтверждён',
  C: 'шаги засвидетельствованы, порядок не установлен', D: 'есть шаг без засвидетельствованных примеров',
};

// ---------- theme -----------------------------------------------------------
const THEME_KEY = 'eldamo-atlas-theme';
function applyTheme(t) { if (t) document.documentElement.setAttribute('data-theme', t); }
applyTheme(store.get(THEME_KEY));
$('theme-toggle').addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme')
    || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const next = cur === 'dark' ? 'light' : 'dark';
  applyTheme(next); store.set(THEME_KEY, next);
});

// ---------- branch indexes ----------------------------------------------------
const cache = {};
function index(name) {
  if (cache[name]) return cache[name];
  const B = DATA.branches[name];
  const X = { B, name };
  X.lang = Object.fromEntries(B.languages.map(l => [l.code, l]));
  X.edge = Object.fromEntries(B.edges.map(e => [e.id, e]));
  X.deriv = Object.fromEntries(B.derivs.map(d => [d.id, d]));
  X.adj = {}; X.radj = {}; X.states = {};
  for (const era of ERAS) { X.adj[era] = new Map(); X.radj[era] = new Map(); X.states[era] = new Set(); }
  for (const e of B.edges) {
    (X.adj[e.era].get(e.a) || X.adj[e.era].set(e.a, []).get(e.a)).push(e);
    (X.radj[e.era].get(e.b) || X.radj[e.era].set(e.b, []).get(e.b)).push(e);
    X.states[e.era].add(e.a); X.states[e.era].add(e.b);
  }
  X.before = new Set();
  for (const [id, r] of Object.entries(B.rules)) for (const t of r.b) X.before.add(id + '>' + t);
  X.occ = new Map();             // pair id -> [[derivation index, step index]]
  B.derivs.forEach((d, di) => {
    if (d.del) return;
    d.steps.forEach((s, si) => {
      const before = si === 0 ? d.st : d.steps[si - 1][4];
      // evidence: the formula reproduces the step and the form changes
      if (s[0] && (s[5] === 'reproduced' || s[5] === 'reproduced_partial') && before !== s[4]) (X.occ.get(s[0]) || X.occ.set(s[0], []).get(s[0])).push([di, si]);
    });
  });
  X.phonemes = new Set(B.phonemes);
  X.derivEra = B.derivs.map(d => {
    const eras = new Set(d.steps.map(s => X.lang[s[1]]?.era).filter(Boolean));
    return eras;
  });
  cache[name] = X;
  return X;
}

function relation(X, r1, r2) {
  if (r1 === r2) return '=';
  if (X.before.has(r1 + '>' + r2)) return '<';
  if (X.before.has(r2 + '>' + r1)) return '>';
  const o1 = X.B.rules[r1]?.o, o2 = X.B.rules[r2]?.o;
  if (o1 != null && o2 != null && o1 !== o2) return o1 < o2 ? '<' : '>';
  return '?';
}
function transition(X, e1, e2) {
  if (e2.st > e1.st) return 'stage';
  if (e2.st < e1.st) return 'contradicted';
  const rel = new Set();
  for (const a of e1.r) for (const b of e2.r) rel.add(relation(X, a, b));
  if (rel.has('<')) return 'ordered';
  if (rel.has('?')) return 'unknown';
  return 'contradicted';
}
function positionOk(cur, e) {
  if (cur === 'any' || e.p === 'any') return [true, cur === 'any' ? e.p : cur];
  return [cur === e.p, cur];
}
// derivations attesting the edges in this order
function attest(X, edges) {
  let found = null;
  for (const e of edges) {
    const pos = new Map();
    for (const p of e.pr) for (const [di, si] of X.occ.get(p) || []) (pos.get(di) || pos.set(di, []).get(di)).push(si);
    if (found === null) {
      found = new Map([...pos].map(([di, v]) => [di, Math.min(...v)]));
    } else {
      const next = new Map();
      for (const [di, prev] of found) {
        const later = (pos.get(di) || []).filter(si => si > prev);
        if (later.length) next.set(di, Math.min(...later));
      }
      found = next;
    }
    if (!found.size) return [];
  }
  return [...found.keys()];
}

// ---------- state & routing -------------------------------------------------
const state = { branch: null, era: 'late', sel: {}, mode: { from: 'phoneme', to: 'phoneme' }, chainPage: 0, derivPage: 0 };
function readHash() {
  let raw = location.hash.slice(1);
  try { raw = decodeURIComponent(raw); } catch (_e) { /* malformed escape: use as is */ }
  const [name, query] = raw.split('?');
  const params = new URLSearchParams(query || '');
  return { name, params };
}
function writeHash(push) {
  if (!state.branch) return;
  const sel = state.sel[state.branch];
  const params = new URLSearchParams({ era: state.era, from: sel.from, to: sel.to });
  const url = '#' + state.branch + '?' + params.toString();
  if (push) location.hash = url.slice(1);
  else try { history.replaceState(null, '', url); } catch (_e) { /* file:// in some browsers */ }
}
function route() {
  const { name, params } = readHash();
  if (!DATA.branches[name]) { showLanding(); return; }
  const X = index(name);
  if (!state.sel[name]) state.sel[name] = { ...X.B.defaults };
  if (ERAS.includes(params.get('era'))) state.era = params.get('era');
  for (const slot of ['from', 'to']) if (params.get(slot)) state.sel[name][slot] = params.get(slot);
  for (const slot of ['from', 'to']) state.mode[slot] = X.phonemes.has(state.sel[name][slot]) ? 'phoneme' : 'cluster';
  if (state.branch !== name) { state.chainPage = 0; state.derivPage = 0; }
  state.branch = name;
  showBranch();
}
window.addEventListener('hashchange', route);

// ---------- landing ---------------------------------------------------------------
const branchSelect = $('branch-select');
branchSelect.replaceChildren(new Option('—', ''), ...Object.entries(DATA.branches).map(([k, b]) => new Option(b.title, k)));
branchSelect.addEventListener('change', () => { location.hash = branchSelect.value || ''; });
$('era-select').addEventListener('change', e => { state.era = e.target.value; writeHash(false); renderAll(); });
$('home-link').addEventListener('click', e => { e.preventDefault(); location.hash = ''; });
$('eldamo-version').textContent = DATA.eldamo_version;
$('branch-cards').innerHTML = Object.entries(DATA.branches).map(([k, b]) => `<button type="button" data-branch="${esc(k)}">
  <strong>${esc(b.title)}</strong><span>${esc(b.path.late)}</span>
  <span>${count(b.stats.rules, 'правило', 'правила', 'правил')} · ${count(b.stats.derivations, 'засвидетельствованная деривация', 'засвидетельствованные деривации', 'засвидетельствованных дериваций')} слов ветви · ${count(b.stats.chains, 'цепочка', 'цепочки', 'цепочек')} (A: ${b.stats.grades.A})</span></button>`).join('');
$('branch-cards').addEventListener('click', e => { const b = e.target.closest('[data-branch]'); if (b) location.hash = b.dataset.branch; });

function showLanding() {
  state.branch = null;
  $('landing').hidden = false; $('app').hidden = true; branchSelect.value = '';
}
function showBranch() {
  $('landing').hidden = true; $('app').hidden = false;
  branchSelect.value = state.branch; $('era-select').value = state.era;
  renderAll();
}
function renderAll() {
  const X = index(state.branch);
  $('branch-path').textContent = `${X.B.title}: ${X.B.path[state.era]}. Правил: ${X.B.stats.rules}, переходов в графе: ${X.B.stats.edges}, формулы воспроизводят ${Math.round(100 * X.B.stats.reproduction_rate)}% засвидетельствованных шагов.`;
  for (const slot of ['from', 'to']) renderPicker(slot);
  $('output').innerHTML = '';
  findPaths();
  renderChains();
  renderDerivs();
}

// ---------- sound pickers ---------------------------------------------------------
function current(slot) { return state.sel[state.branch][slot]; }
function setSound(slot, value, keepMode) {
  const X = index(state.branch);
  state.sel[state.branch][slot] = value;
  if (!keepMode) state.mode[slot] = X.phonemes.has(value) ? 'phoneme' : 'cluster';
  renderPicker(slot);
  writeHash(false);
}
function renderPicker(slot) {
  const X = index(state.branch);
  const box = document.querySelector(`.picker[data-slot="${slot}"]`);
  const value = current(slot);
  $(slot + '-chosen').textContent = value === NULL ? 'ø (исчезновение)' : value;
  const mode = state.mode[slot];
  box.querySelectorAll('.mode-switch button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
  box.querySelector('[data-role="grid"]').hidden = mode !== 'phoneme';
  box.querySelector('[data-role="cluster"]').hidden = mode !== 'cluster';
  const live = X.states[state.era];
  if (mode === 'phoneme') box.querySelector('[data-role="grid"]').innerHTML = gridHtml(X.B.grid, value, live);
  else {
    const list = [...live].filter(s => !X.phonemes.has(s)).sort((a, b) => a.localeCompare(b));
    $(slot + '-states').replaceChildren(...list.map(s => new Option(s, s)));
    const input = $(slot + '-cluster');
    if (document.activeElement !== input) input.value = X.phonemes.has(value) ? '' : value;
  }
}
function soundButton(s, value, live) {
  const label = s === NULL ? 'ø' : s;
  const title = live.has(s) ? '' : ' title="В графе этого периода нет переходов с этим звуком"';
  return `<button type="button" class="ipa-sound${live.has(s) ? '' : ' no-edges'}" data-sound="${esc(s)}" aria-pressed="${s === value}"${title}>${esc(label)}</button>`;
}
function gridHtml(G, value, live) {
  const table = (caption, rows, cols, cells) => {
    const usedRows = rows.filter(([r]) => cells[r]);
    const usedCols = cols.filter(([c]) => usedRows.some(([r]) => cells[r][c]));
    if (!usedRows.length) return '';
    return `<table class="ipa-grid"><caption>${caption}</caption><thead><tr><th></th>${usedCols.map(([, t]) => `<th scope="col">${esc(t)}</th>`).join('')}</tr></thead><tbody>${
      usedRows.map(([r, rt]) => `<tr><th scope="row">${esc(rt)}</th>${usedCols.map(([c]) => `<td>${(cells[r][c] || []).map(s => soundButton(s, value, live)).join('')}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  };
  let html = table('Согласные', G.consonants.rows, G.consonants.cols, G.consonants.cells);
  html += table('Гласные', G.vowels.rows, G.vowels.cols, G.vowels.cells);
  if (G.diphthongs.cols.length) html += `<table class="ipa-grid"><caption>Дифтонги</caption><thead><tr>${G.diphthongs.cols.map(([, t]) => `<th scope="col">${esc(t)}</th>`).join('')}</tr></thead><tbody><tr>${G.diphthongs.cols.map(([c]) => `<td>${G.diphthongs.cells[c].map(s => soundButton(s, value, live)).join('')}</td>`).join('')}</tr></tbody></table>`;
  const extra = [...G.null, ...G.other];
  if (extra.length) html += `<table class="ipa-grid"><caption>Прочее</caption><tbody><tr><td>${extra.map(s => soundButton(s, value, live)).join('')}</td></tr></tbody></table>`;
  return html;
}
for (const slot of ['from', 'to']) {
  const box = document.querySelector(`.picker[data-slot="${slot}"]`);
  box.addEventListener('click', e => {
    const b = e.target.closest('.ipa-sound');
    if (b) { setSound(slot, b.dataset.sound, true); return; }
    const m = e.target.closest('.mode-switch button');
    if (m) { state.mode[slot] = m.dataset.mode; renderPicker(slot); }
  });
  $(slot + '-cluster').addEventListener('change', e => { const v = e.target.value.trim(); if (v) setSound(slot, v, true); });
}

// ---------- step rendering --------------------------------------------------------
function ruleLink(X, id) {
  const r = X.B.rules[id];
  return `<a href="${esc(wordUrl(id))}" target="_blank" rel="noopener">${esc(r ? r.n : id)}</a>`;
}
function exampleWords(X, e, limit = 3) {
  const seen = [];
  for (const p of e.pr) for (const [di, si] of X.occ.get(p) || []) {
    if (seen.length >= limit) break;
    const d = X.B.derivs[di], s = d.steps[si];
    const before = si === 0 ? d.st : d.steps[si - 1][4];
    seen.push(`<a href="#" data-deriv="${esc(d.id)}">${esc(d.wf || d.f)}</a> <span class="form">${esc(before)} → ${esc(s[4])}</span>`);
  }
  return seen.join('; ');
}
function stepHtml(X, e, transitionLabel) {
  const pos = e.p !== 'any' ? ` <span class="pill">${esc(POSITION[e.p] || e.p)}</span>` : '';
  const cond = [];
  if (e.cx.length) cond.push(`общая формула правила: <code>${e.cx.map(esc).join('</code>, <code>')}</code>`);
  if (e.ex.length) cond.push(`без изменения остаются: <code>${e.ex.map(esc).join('</code>, <code>')}</code>`);
  const ex = e.e
    ? `<div class="examples">${count(e.e, 'засвидетельствованный пример', 'засвидетельствованных примера', 'засвидетельствованных примеров')}, формула воспроизводит ${e.ok}: ${exampleWords(X, e)}</div>`
    : '<div class="examples">Засвидетельствованных примеров этого шага в деривациях нет.</div>';
  return `<li>${transitionLabel ? `<div class="small muted">${esc(transitionLabel)}</div>` : ''}<strong class="ipa">${esc(e.a)} → ${esc(e.b)}</strong> · ${esc(e.m)}${pos} · ${e.r.map(r => ruleLink(X, r)).join('; ')}${
    cond.length ? `<div class="cond">Условие: ${cond.join('; ')}</div>` : ''}${ex}</li>`;
}
function routeHtml(nodes) {
  return `<span class="route">${nodes.map(n => `<span>${esc(n)}</span>`).join('<span class="arrow">→</span>')}</span>`;
}
function pathCard(X, p, open) {
  const att = attest(X, p.edges);
  const attested = p.edges.filter(e => e.ok > 0).length;
  const conditional = p.edges.filter(e => e.c).length;
  const transitions = p.edges.map((e, i) => i ? transition(X, p.edges[i - 1], e) : null);
  const words = att.slice(0, 6).map(di => X.B.derivs[di]).map(d => `<a href="#" data-deriv="${esc(d.id)}">${esc(d.wf || d.f)}</a>`).join(', ');
  return `<details class="card"${open ? ' open' : ''}><summary>${routeHtml(p.nodes)}
    <span class="pill">${count(p.edges.length, 'шаг', 'шага', 'шагов')}</span>
    ${att.length ? `<span class="pill ok">засвидетельствован целиком: ${count(att.length, 'деривация', 'деривации', 'дериваций')}</span>` : `<span class="pill">${attested} из ${p.edges.length} с примерами</span>`}
    ${conditional ? `<span class="pill warn">${count(conditional, 'условный шаг', 'условных шага', 'условных шагов')}</span>` : ''}</summary>
    <div class="body"><ol class="steps">${p.edges.map((e, i) => stepHtml(X, e, transitions[i] ? TRANSITION[transitions[i]] : '')).join('')}</ol>
    ${att.length ? `<p class="small">Слова, в деривации которых путь пройден целиком: ${words}${att.length > 6 ? ' …' : ''}</p>` : ''}</div></details>`;
}

// ---------- path search -----------------------------------------------------------
function options() {
  return { depth: Number($('depth').value), chrono: $('chronology').checked, attested: $('attested').checked, uncond: $('unconditional').checked };
}
function usable(e, o) { return (!o.attested || e.ok > 0) && (!o.uncond || !e.c); }
function walk(X, root, direction, o, onPath, maxStates) {
  const adj = direction === 'forward' ? X.adj[state.era] : X.radj[state.era];
  const queue = [{ at: root, nodes: [root], edges: [], pos: 'any' }];
  let scanned = 0, truncated = false;
  for (let h = 0; h < queue.length; h++) {
    const p = queue[h];
    if (++scanned > maxStates) { truncated = true; break; }
    if (p.edges.length >= o.depth) continue;
    for (const e of adj.get(p.at) || []) {
      if (!usable(e, o)) continue;
      const next = direction === 'forward' ? e.b : e.a;
      if (p.nodes.includes(next)) continue;
      const [ok, pos] = positionOk(p.pos, e);
      if (!ok) continue;
      if (p.edges.length) {
        const prev = direction === 'forward' ? p.edges[p.edges.length - 1] : p.edges[0];
        const t = direction === 'forward' ? transition(X, prev, e) : transition(X, e, prev);
        if (o.chrono && t === 'contradicted') continue;
        if (!o.chrono && t === 'contradicted' && prev.r.some(r => e.r.includes(r))) continue;
      }
      if (direction === 'forward' && p.at === NULL) continue;
      const np = {
        at: next,
        nodes: direction === 'forward' ? p.nodes.concat(next) : [next].concat(p.nodes),
        edges: direction === 'forward' ? p.edges.concat(e) : [e].concat(p.edges),
        pos,
      };
      if (onPath(np) === false) { truncated = true; return truncated; }
      queue.push(np);
    }
  }
  return truncated;
}
function sortPaths(X, paths) {
  const score = p => [p.edges.length, attest(X, p.edges).length ? 0 : 1, -p.edges.reduce((n, e) => n + (e.ok > 0 ? 1 : 0), 0)];
  return paths.map(p => [score(p), p]).sort((a, b) => {
    for (let i = 0; i < 3; i++) if (a[0][i] !== b[0][i]) return a[0][i] - b[0][i];
    return a[1].nodes.join(' ').localeCompare(b[1].nodes.join(' '));
  }).map(x => x[1]);
}
function findPaths() {
  const X = index(state.branch), o = options();
  const src = current('from'), dst = current('to');
  const found = [];
  const seen = new Set();
  const truncated = walk(X, src, 'forward', o, p => {
    if (p.at === dst) {
      const key = p.edges.map(e => e.id).join(',');
      if (!seen.has(key)) { seen.add(key); found.push(p); }
      if (found.length >= 200) return false;
    }
    return true;
  }, 100000);
  const paths = sortPaths(X, found.filter(p => p.at === dst));
  const out = $('output');
  if (!paths.length) {
    const reach = new Map();
    walk(X, src, 'forward', { ...o, depth: o.depth }, p => { if (!reach.has(p.at)) reach.set(p.at, p.edges.length); return true; }, 20000);
    const incoming = [...new Set((X.radj[state.era].get(dst) || []).filter(e => usable(e, o)).map(e => e.a))];
    const near = [...reach].sort((a, b) => a[1] - b[1] || a[0].localeCompare(b[0])).slice(0, 24);
    announce(`Путь ${src} → ${dst} не найден`);
    out.innerHTML = `<div class="result-head"><strong>Путь ${esc(src)} → ${esc(dst)} в этой концепции не найден</strong> при заданных ограничениях.</div>
      <p class="muted">Граф связывает только литеральные подформулы правил Eldamo; контекстные правила (с классами V, C, S) в него не входят — их видно в «Правилах исходного/конечного». Можно увеличить число шагов, снять фильтры или посмотреть дерево развития.</p>
      <div>Из [${esc(src)}] достижимы:</div><div class="nearby">${near.map(([s, n]) => `<button type="button" data-target="${esc(s)}">${esc(s)} · ${count(n, 'шаг', 'шага', 'шагов')}</button>`).join('') || '<span class="muted">ничего</span>'}</div>
      <div>Непосредственно в [${esc(dst)}] переходят: ${incoming.map(s => `<button type="button" data-source="${esc(s)}">${esc(s)}</button>`).join(' ') || '<span class="muted">ничего</span>'}</div>`;
    return;
  }
  announce(`${count(paths.length, 'путь', 'пути', 'путей')} ${src} → ${dst}`);
  out.innerHTML = `<div class="result-head">${count(paths.length, 'путь', 'пути', 'путей')} ${esc(src)} → ${esc(dst)}${truncated ? ' (поиск ограничен)' : ''}; показаны первые ${Math.min(paths.length, 60)}, сначала короткие и засвидетельствованные.</div>`
    + paths.slice(0, 60).map((p, i) => pathCard(X, p, i === 0)).join('');
}
$('output').addEventListener('click', e => {
  const t = e.target.closest('[data-target]'); if (t) { setSound('to', t.dataset.target); findPaths(); return; }
  const s = e.target.closest('[data-source]'); if (s) { setSound('from', s.dataset.source); findPaths(); }
});
$('go').addEventListener('click', findPaths);
$('swap').addEventListener('click', () => {
  const sel = state.sel[state.branch];
  [sel.from, sel.to] = [sel.to, sel.from];
  [state.mode.from, state.mode.to] = [state.mode.to, state.mode.from];
  renderPicker('from'); renderPicker('to'); writeHash(false); findPaths();
});
for (const id of ['depth', 'chronology', 'attested', 'unconditional']) $(id).addEventListener('change', findPaths);

function treeSvg(paths, root, direction) {
  // layered drawing: column = number of steps from the root
  const depth = new Map([[root, 0]]);
  const links = new Map();
  for (const p of paths) {
    const seq = direction === 'forward' ? p.nodes : [...p.nodes].reverse();
    const es = direction === 'forward' ? p.edges : [...p.edges].reverse();
    seq.forEach((n, i) => { if (!depth.has(n) || depth.get(n) > i) depth.set(n, i); });
    for (let i = 1; i < seq.length; i++) {
      const key = seq[i - 1] + '\u0001' + seq[i];
      const prev = links.get(key);
      const attested = es[i - 1].e > 0;
      links.set(key, { from: seq[i - 1], to: seq[i], attested: attested || (prev && prev.attested) });
    }
  }
  if (depth.size < 2 || depth.size > 160) return '';
  const cols = [];
  for (const [n, d] of depth) (cols[d] = cols[d] || []).push(n);
  cols.forEach(c => c.sort((a, b) => a.localeCompare(b)));
  const W = 150, H = 26, pad = 16, rows = Math.max(...cols.map(c => c.length));
  const width = pad * 2 + (cols.length - 1) * W + 60, height = pad * 2 + (rows - 1) * H + 10;
  const pos = new Map();
  cols.forEach((c, d) => c.forEach((n, i) => {
    const x = direction === 'forward' ? pad + 20 + d * W : width - pad - 20 - d * W;
    const y = pad + 5 + (i + (rows - c.length) / 2) * H;
    pos.set(n, [x, y]);
  }));
  const lines = [...links.values()].filter(l => depth.get(l.to) === depth.get(l.from) + 1).map(l => {
    const [x1, y1] = pos.get(l.from), [x2, y2] = pos.get(l.to);
    const sx = direction === 'forward' ? 16 : -16;
    return `<path d="M${x1 + sx},${y1} C${(x1 + x2) / 2},${y1} ${(x1 + x2) / 2},${y2} ${x2 - sx},${y2}" class="${l.attested ? 'att' : 'unatt'}"/>`;
  }).join('');
  const labels = [...pos].map(([n, [x, y]]) => `<text x="${x}" y="${y}" class="${n === root ? 'root' : ''}">${esc(n)}</text>`).join('');
  return `<figure class="tree-svg"><svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" role="img" aria-label="Схема ${direction === 'forward' ? 'развития' : 'происхождения'} [${esc(root)}]">${lines}${labels}</svg>
    <figcaption class="small muted">Сплошная линия — переход с засвидетельствованными примерами, пунктир — без примеров.</figcaption></figure>`;
}
function tree(direction) {
  const X = index(state.branch), o = options();
  const root = current(direction === 'forward' ? 'from' : 'to');
  const found = new Map();
  const truncated = walk(X, root, direction, o, p => {
    const key = p.edges.map(e => e.id).join(',');
    if (!found.has(key)) found.set(key, p);
    return found.size < 3000;
  }, 60000);
  const paths = sortPaths(X, [...found.values()]);
  const groups = new Map();
  for (const p of paths) (groups.get(p.edges.length) || groups.set(p.edges.length, []).get(p.edges.length)).push(p);
  const shownPerGroup = 80;
  $('output').innerHTML = `<div class="result-head"><strong>${direction === 'forward' ? 'Развитие' : 'Происхождение'} [${esc(root)}]</strong>: ${count(paths.length, 'путь', 'пути', 'путей')} до ${count(o.depth, 'шага', 'шагов', 'шагов')}${truncated ? ' (поиск ограничен)' : ''}.</div>`
    + treeSvg(paths, root, direction)
    + ([...groups].map(([n, ps]) => `<h3>${count(n, 'шаг', 'шага', 'шагов')} · ${count(ps.length, 'вариант', 'варианта', 'вариантов')}${ps.length > shownPerGroup ? `, показаны первые ${shownPerGroup}` : ''}</h3>`
      + ps.slice(0, shownPerGroup).map(p => pathCard(X, p, false)).join('')).join('') || '<div class="empty">Переходов не найдено.</div>');
}
$('develop').addEventListener('click', () => tree('forward'));
$('origins').addEventListener('click', () => tree('backward'));

// ---------- rules of a sound -------------------------------------------------------
function showRules(slot) {
  const X = index(state.branch);
  const sound = current(slot);
  const isPhoneme = X.phonemes.has(sound);
  const eraCodes = new Set(X.B.languages.filter(l => l.era === state.era).map(l => l.code));
  const rows = [];
  for (const [id, p] of Object.entries(X.B.pairs)) {
    const r = X.B.rules[p.r];
    if (!eraCodes.has(r.l)) continue;
    const hit = isPhoneme
      ? (p.c.includes(sound) || p.s.includes(sound) || (sound === NULL && (p.k === 'loss' || p.k === 'insertion')))
      : (p.a === sound || p.b === sound);
    if (hit) rows.push([id, p, r]);
  }
  rows.sort((x, y) => X.lang[x[2].l].stage - X.lang[y[2].l].stage || (x[2].o ?? 1e9) - (y[2].o ?? 1e9) || x[1].f.localeCompare(y[1].f));
  const body = rows.map(([id, p, r]) => `<tr><td>${esc(X.lang[r.l].marker)}</td><td>${ruleLink(X, p.r)}${r.o != null ? `<div class="small muted">порядок ${r.o}</div>` : ''}</td>
    <td><code>${esc(p.f)} &gt; ${esc(p.t)}</code>${p.k === 'contextual' ? '<div class="small muted">контекстная, вне графа</div>' : p.k === 'identity' ? '<div class="small muted">исключение: без изменения</div>' : ''}</td>
    <td>${r.f ? `<code>${esc(r.f[0])} &gt; ${esc(r.f[1])}</code>` : ''}</td>
    <td>${p.e ? `${p.e} / ${p.ok}` : '—'}</td></tr>`).join('');
  $('output').innerHTML = `<div class="result-head"><strong>Правила со звуком [${esc(sound)}]</strong> — ${ERA_NAMES[state.era]} концепция: ${count(rows.length, 'подформула', 'подформулы', 'подформул')}${isPhoneme ? ' (по карточкам фонем Eldamo и составу формул)' : ' (сочетание стоит целиком в одной из частей формулы)'}.</div>`
    + (rows.length ? `<div class="table-scroll"><table class="data"><thead><tr><th>Язык</th><th>Правило</th><th>Подформула</th><th>Общая формула</th><th>Примеры / воспроизведено</th></tr></thead><tbody>${body}</tbody></table></div>`
      : '<div class="empty">Подформул с этим звуком нет.</div>');
}
$('rules-from').addEventListener('click', () => showRules('from'));
$('rules-to').addEventListener('click', () => showRules('to'));

// ---------- chains ------------------------------------------------------------------
const PAGE = 20;
function pager(page, pages, prefix) {
  if (pages <= 1) return '';
  return `<div class="pager"><button type="button" data-page="${prefix}:${page - 1}" ${page === 0 ? 'disabled' : ''}>← Назад</button><span>Страница ${page + 1} из ${pages}</span><button type="button" data-page="${prefix}:${page + 1}" ${page >= pages - 1 ? 'disabled' : ''}>Вперёд →</button></div>`;
}
function chainCard(X, c) {
  const edges = c.steps.map(id => X.edge[id]);
  const words = c.d.map(id => X.deriv[id]).map(d => `<a href="#" data-deriv="${esc(d.id)}">${esc(d.wf || d.f)}</a>`).join(', ');
  return `<details class="card"><summary>${routeHtml(c.s)} <span class="grade grade-${c.g}" title="${esc(GRADE[c.g])}">${c.g}</span>
    ${c.n ? `<span class="pill ok">${count(c.n, 'деривация', 'деривации', 'дериваций')}</span>` : ''}${c.v > 1 ? `<span class="pill">${count(c.v, 'вариант', 'варианта', 'вариантов')} рёбер</span>` : ''}</summary>
    <div class="body"><p class="small muted">${esc(GRADE[c.g])}.</p><ol class="steps">${edges.map((e, i) => stepHtml(X, e, i ? TRANSITION[c.t[i - 1]] : '')).join('')}</ol>
    ${c.n ? `<p class="small">Засвидетельствована в словах: ${words}${c.n > c.d.length ? ' …' : ''}</p>` : ''}</div></details>`;
}
function renderChains() {
  const X = index(state.branch);
  const q = $('chain-query').value.trim().toLowerCase();
  const g = $('chain-grade').value;
  const list = X.B.chains.filter(c => c.era === state.era && (!g || c.g === g) && (!q
    || c.s.join(' → ').toLowerCase().includes(q)
    || c.steps.some(id => X.edge[id].r.some(r => (X.B.rules[r]?.n || '').toLowerCase().includes(q)))));
  const pages = Math.max(1, Math.ceil(list.length / PAGE));
  state.chainPage = Math.min(state.chainPage, pages - 1);
  const view = list.slice(state.chainPage * PAGE, (state.chainPage + 1) * PAGE);
  announce(count(list.length, 'цепочка', 'цепочки', 'цепочек'));
  $('chains').innerHTML = `<p class="small muted">${count(list.length, 'цепочка', 'цепочки', 'цепочек')}</p>` + (view.map(c => chainCard(X, c)).join('') || '<div class="empty">Цепочек с такими условиями нет.</div>') + pager(state.chainPage, pages, 'chain');
}
$('chain-query').addEventListener('input', () => { state.chainPage = 0; renderChains(); });
$('chain-grade').addEventListener('change', () => { state.chainPage = 0; renderChains(); });

// ---------- derivations ---------------------------------------------------------
const DPAGE = 15;
function derivCard(X, d, open) {
  const lang = code => X.lang[code]?.marker || code;
  const langTitle = code => X.B.language_names[code] || code;
  const rows = d.steps.map((s, i) => {
    const before = i === 0 ? d.st : d.steps[i - 1][4];
    const pair = s[0] ? X.B.pairs[s[0]] : null;
    const rule = pair ? ruleLink(X, pair.r) : (s[3] === '?' ? '<span class="muted">не указано</span>' : `<span class="muted">${esc(s[2] || '')} &gt; ${esc(s[3])}</span>`);
    const [mark, title] = STATUS[s[5]] || ['?', s[5]];
    const inBranch = !!X.lang[s[1]];
    return `<tr${inBranch ? '' : ' class="muted"'}><td title="${esc(langTitle(s[1]))}">${esc(lang(s[1]))}</td><td>${rule}</td><td><code>${s[2] != null ? esc(s[2]) + ' &gt; ' : ''}${esc(s[3])}</code></td>
      <td class="form ipa">${esc(before)} → ${esc(s[4])}</td><td class="status-${esc(s[5])}" title="${esc(title)}">${mark} <span class="small">${esc(title)}</span></td></tr>`;
  }).join('');
  const issues = d.steps.filter(s => ISSUE.has(s[5])).length;
  return `<details class="card" id="deriv-${esc(d.id)}"${open ? ' open' : ''}><summary><span class="route${d.del ? ' deleted' : ''}">${esc(d.wf || d.f)}</span>
    ${d.g ? `<span class="muted">«${esc(d.g)}»</span>` : ''} <span class="pill" title="${esc(langTitle(d.wl))}">${esc(X.lang[d.wl] ? lang(d.wl) : langTitle(d.wl))}</span> <span class="pill">${count(d.steps.length, 'шаг', 'шага', 'шагов')}</span>${d.src ? ` <span class="small muted">${esc(d.src.split('.')[0])}</span>` : ''}
    ${issues ? `<span class="pill warn">${count(issues, 'расхождение', 'расхождения', 'расхождений')}</span>` : ''}${d.del ? '<span class="pill warn">отвергнуто Толкином</span>' : ''}</summary>
    <div class="body"><p class="small">Форма <span class="form">${esc(d.f)}</span> из <span class="form">${esc(d.st)}</span> · источник ${sourceLink(d.src)}${d.dsrc && d.dsrc !== d.src ? `, деривация ${sourceLink(d.dsrc)}` : ''} · <a href="${esc(wordUrl(d.w))}" target="_blank" rel="noopener">статья Eldamo</a></p>
    <div class="table-scroll"><table class="data steps-table"><thead><tr><th>Язык</th><th>Правило</th><th>Формула</th><th>Форма</th><th>Проверка</th></tr></thead><tbody>${rows}</tbody></table></div></div></details>`;
}
function derivText(X, d) {
  if (!d._text) {
    const rules = d.steps.map(s => s[0] && X.B.pairs[s[0]] ? (X.B.rules[X.B.pairs[s[0]].r]?.n || '') : '').join(' ');
    d._text = [d.wf, d.f, d.g, d.st, ...d.steps.map(s => s[4]), rules].join(' ').toLowerCase();
  }
  return d._text;
}
function renderDerivs() {
  const X = index(state.branch);
  const raw = $('deriv-query').value.trim();
  const q = raw.toLowerCase();
  const showDeleted = $('deriv-deleted').checked, issuesOnly = $('deriv-issues').checked, others = $('deriv-others').checked;
  let list;
  if (/^id:/.test(raw)) {
    const id = raw.slice(3).trim();
    list = X.B.derivs.filter(d => d.id === id);
  } else {
    list = X.B.derivs.filter((d, i) => X.derivEra[i].has(state.era) && (showDeleted || !d.del) && (others || d.bw)
      && (!issuesOnly || d.steps.some(s => ISSUE.has(s[5])))
      && (!q || derivText(X, d).includes(q)));
  }
  const pages = Math.max(1, Math.ceil(list.length / DPAGE));
  state.derivPage = Math.min(state.derivPage, pages - 1);
  const view = list.slice(state.derivPage * DPAGE, (state.derivPage + 1) * DPAGE);
  announce(count(list.length, 'деривация', 'деривации', 'дериваций'));
  $('derivations').innerHTML = `<p class="small muted">${count(list.length, 'деривация', 'деривации', 'дериваций')}</p>`
    + (view.map(d => derivCard(X, d, list.length === 1)).join('') || '<div class="empty">Дериваций с такими условиями нет.</div>') + pager(state.derivPage, pages, 'deriv');
}
$('deriv-query').addEventListener('input', () => { state.derivPage = 0; renderDerivs(); });
for (const id of ['deriv-deleted', 'deriv-issues', 'deriv-others']) $(id).addEventListener('change', () => { state.derivPage = 0; renderDerivs(); });

document.addEventListener('click', e => {
  const p = e.target.closest('[data-page]');
  if (p) {
    const [kind, n] = p.dataset.page.split(':');
    if (kind === 'chain') { state.chainPage = Number(n); renderChains(); $('chains-title').scrollIntoView({ block: 'start' }); }
    else { state.derivPage = Number(n); renderDerivs(); $('derivs-title').scrollIntoView({ block: 'start' }); }
    return;
  }
  const d = e.target.closest('[data-deriv]');
  if (d) {
    e.preventDefault();
    $('deriv-query').value = 'id:' + d.dataset.deriv;
    state.derivPage = 0; renderDerivs();
    $('derivations-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});

route();
})();
