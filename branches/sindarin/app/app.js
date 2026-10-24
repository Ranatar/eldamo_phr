"use strict";
const EDGES = window.ELDAMO_EDGES;
const RULE_CATALOG = window.ELDAMO_RULES;
const $ = x => document.getElementById(x);
const states = Array.from(new Set(EDGES.flatMap(e => [e.a, e.b]))).sort((a, b) => a.localeCompare(b));
$('numbers').textContent = `${EDGES.length} атомарных переходов · ${states.length} звуковых состояний`;
const PHONEMES = ["a", "ae", "ai", "au", "b", "d", "e", "ei", "eu", "f", "g", "h", "i", "iu", "iw", "j", "j̊", "k", "kʰ", "l", "l̥", "m", "m̥", "n", "n̥", "o", "oe", "oi", "ou", "p", "pʰ", "r", "r̥", "s", "t", "tʰ", "u", "ui", "v", "w", "w̥", "x", "y", "z", "ð", "ø", "ā", "ē", "ę̄", "ī", "ŋ", "ō", "œ", "ū", "ǣ", "ǭ", "ȳ", "ɣ", "ɸ", "β", "θ"];
const PHSET = new Set(PHONEMES);
const compound = states.filter(s => !PHSET.has(s) && s.length > 1 && !/[{}|VCS_+*?⁺⁻₁₂₃\[\]()]/.test(s));
const vals = { from: 'p', to: 'f' }, modes = { from: 'phoneme', to: 'phoneme' };
function selectState(slot, val) { vals[slot] = val; $(slot + '-chosen').textContent = val; document.querySelectorAll('.side[data-slot="' + slot + '"] .ipa-sound').forEach(b => b.classList.toggle('selected', modes[slot] === 'phoneme' && b.dataset.phoneme === val)); }
function fillCombos(slot) { let first = $(slot + '-first').value; let opts = compound.filter(s => s.startsWith(first)); let sel = $(slot + '-combo'); sel.replaceChildren(...opts.map(s => new Option(s, s))); if (opts.length) {
    selectState(slot, opts[0]);
    sel.disabled = false;
}
else {
    sel.disabled = true;
    selectState(slot, '');
} }
function setMode(slot, mode) { modes[slot] = mode; document.querySelectorAll('.mode[data-slot="' + slot + '"]').forEach(x => x.classList.toggle('active', x.dataset.mode === mode)); $(slot + '-ipa').classList.toggle('hidden', mode !== 'phoneme'); $(slot + '-cluster').classList.toggle('active', mode === 'cluster'); if (mode === 'cluster') {
    fillCombos(slot);
}
else {
    selectState(slot, PHSET.has(vals[slot]) ? vals[slot] : 'p');
} }
for (const slot of ['from', 'to']) {
    const firsts = [...new Set(compound.map(s => PHONEMES.filter(p => s.startsWith(p)).sort((a, b) => b.length - a.length)[0]).filter(Boolean))];
    $(slot + '-first').replaceChildren(...firsts.map(s => new Option(s, s)));
    $(slot + '-first').addEventListener('change', () => fillCombos(slot));
    $(slot + '-combo').addEventListener('change', () => selectState(slot, $(slot + '-combo').value));
    document.querySelectorAll('.side[data-slot="' + slot + '"]').forEach(c => c.addEventListener('click', e => { const b = e.target.closest('.ipa-sound'); if (b) {
        selectState(slot, b.dataset.phoneme);
    } }));
    setMode(slot, 'phoneme');
}
document.querySelectorAll('.mode').forEach(b => b.addEventListener('click', () => setMode(b.dataset.slot, b.dataset.mode)));
const safe = s => String(s ?? '').replace(/[&<>"']/g, x => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[x]));
function find() {
    const src = vals.from.trim(), dst = vals.to.trim(), era = $('era').value, maxD = Number($('depth').value), stage = $('stage').checked, ev = $('evidence').checked, simple = $('simple').checked;
    const adj = new Map();
    for (const e of EDGES) {
        if (e.era !== era || (ev && !e.tested))
            continue;
        if (!adj.has(e.a))
            adj.set(e.a, []);
        adj.get(e.a).push(e);
    }
    let found = [], queue = [{ at: src, nodes: [src], edges: [], st: -1, position: 'any' }], scanned = 0, truncated = false;
    const LIMIT = 70000;
    for (let head = 0; head < queue.length; head++) {
        const p = queue[head];
        if (++scanned > LIMIT) {
            truncated = true;
            break;
        }
        if (p.at === dst && p.edges.length) {
            found.push(p);
            if (found.length >= 80) {
                truncated = true;
                break;
            }
            continue;
        }
        if (p.edges.length >= maxD)
            continue;
        for (const e of (adj.get(p.at) || [])) {
            if (stage && e.stage < p.st)
                continue;
            if (simple && p.nodes.includes(e.b))
                continue;
            if (p.position !== 'any' && e.position && e.position !== 'any' && e.position !== p.position)
                continue;
            queue.push({ at: e.b, nodes: p.nodes.concat(e.b), edges: p.edges.concat(e), st: e.stage, position: p.position === 'any' ? (e.position || 'any') : p.position });
        }
    }
    const out = $('output');
    if (!found.length) {
        const reached = new Map([[src, 0]]), pending = [src];
        for (let k = 0; k < pending.length && k < 500; k++) {
            let u = pending[k];
            if (reached.get(u) >= maxD)
                continue;
            for (const e of adj.get(u) || []) {
                if (!reached.has(e.b)) {
                    reached.set(e.b, reached.get(u) + 1);
                    pending.push(e.b);
                }
            }
        }
        const near = [...reached].filter(([v]) => v !== src).sort((a, b) => a[1] - b[1]).slice(0, 14);
        const incoming = EDGES.filter(e => e.b === dst && e.era === era).map(e => e.a).filter((v, i, a) => a.indexOf(v) === i).slice(0, 14);
        out.innerHTML = '<div class="empty-info"><strong>В выбранных правилах нет пути ' + safe(src) + ' → ' + safe(dst) + '.</strong><p>Это не ошибка поиска и не доказательство невозможности развития. Поиск соединяет только документированные в индексе атомарные переходы и не подменяет один звук другим.</p><div>Из ' + safe(src) + ' достижимы (без учёта ограничения порядка ступеней):</div><div class="nearby">' + near.map(([v, n]) => '<button type="button" data-near="' + safe(v) + '">' + safe(v) + ' · ' + n + ' шаг(а)</button>').join('') + '</div><div>Непосредственно к ' + safe(dst) + ' ведут: ' + (incoming.map(safe).join(', ') || 'в этом периоде нет входящих переходов') + '</div><p class="muted">' + (false ? 'Проверьте альтернативные фонетические окружения и период.' : 'Проверяйте также период, последовательность ступеней и полные контекстные формулы в каталоге.') + '</p></div>' + (truncated ? '<p class="warn">Поиск ограничен по числу перебираемых состояний.</p>' : '');
        out.querySelectorAll('[data-near]').forEach(b => b.addEventListener('click', () => { setMode('to', 'phoneme'); selectState('to', b.dataset.near); find(); }));
        return;
    }
    found.sort((a, b) => a.edges.length - b.edges.length || b.edges.reduce((n, x) => n + (x.exact ? 1 : 0), 0) - a.edges.reduce((n, x) => n + (x.exact ? 1 : 0), 0));
    out.innerHTML = `<p class="stats">Найдено ${found.length} структурных кандидатов; отображается до 80. ${truncated ? 'Поиск был ограничен ресурсами.' : ''}</p>` + found.map((p, i) => '<article class="path"><div class="route">' + p.nodes.map(n => '<span>' + safe(n) + '</span>').join(' → ') + '</div><span class="pill">' + p.edges.length + ' перехода</span><span class="pill">' + p.edges.filter(x => x.exact).length + ' с точным примером шага</span><details ' + (i === 0 ? 'open' : '') + '><summary>Правила, источники и ограничения</summary><ol>' + p.edges.map(e => '<li><strong>' + safe(e.a) + ' → ' + safe(e.b) + '</strong> · ' + safe(e.marker) + ' · ' + (e.url ? '<a href="' + safe(e.url) + '" target="_blank" rel="noopener">' + safe(e.rule) + '</a>' : safe(e.rule)) + ' <small>(' + safe(e.cards) + ')</small>' + (e.position && e.position !== 'any' ? ' <small>позиция: ' + safe(e.position) + '</small>' : '') + (e.exact ? '<div class="muted">Есть пример с совпадающей формулой на странице правила.</div>' : '<div class="muted">Точного проверенного примера шага нет.</div>') + (e.cautions ? '<div class="warn">Условия из заметки требуют проверки: ' + safe(e.cautions) + '</div>' : '') + (e.comment ? '<details><summary>Фрагмент пояснения</summary>' + safe(e.comment) + '…</details>' : '') + '</li>').join('') + '</ol></details></article>').join('');
}
function showRules(slot) {
    const selection = vals[slot];
    const panel = $('rule-panel');
    panel.hidden = false;
    $('rule-title').textContent = 'Фонетические правила: [' + selection + ']';
    const matching = RULE_CATALOG[selection] || [];
    const isCluster = !PHSET.has(selection);
    // For clusters use exact matching at either side of an attested formula; do not infer from unrelated constituent rules.
    const norm = s => s.replace(/^-|-$/g, '').trim();
    const records = isCluster ? Object.values(RULE_CATALOG).flat().filter(r => {
        const parts = r.formula.split(/→|←/);
        return parts.length === 2 && parts.some(p => norm(p.replace(/`/g, '')) === selection);
    }) : matching;
    const uniq = [];
    const seen = new Set();
    for (const r of records) {
        const k = [r.marker, r.title, r.formula, r.url, r.langs].join('\u001f');
        if (!seen.has(k)) {
            seen.add(k);
            uniq.push(r);
        }
    }
    const ranking = { 'S.': 0, 'OS.': 1, 'AT.': 2, '✶': 3, 'N.': 4, 'ON.': 5, 'ᴹ✶': 6 };
    uniq.sort((a, b) => (ranking[a.marker] ?? 99) - (ranking[b.marker] ?? 99) || a.formula.localeCompare(b.formula));
    $('rule-count').textContent = uniq.length + ' записей по каталогу Eldamo 0.8.13' + (isCluster ? ' (строгое совпадение всей комбинации в формуле)' : '');
    if (!uniq.length) {
        $('rule-table').innerHTML = '<div class="empty-info">Для этого выбора нет отдельной записи в каталоге. Это не доказывает отсутствие контекстных преобразований в целом.</div>';
        return;
    }
    const cells = uniq.map(r => '<tr><td>' + safe(r.marker) + '</td><td>' + (r.url ? '<a href="' + safe(r.url) + '" target="_blank" rel="noopener">' + safe(r.title) + '</a>' : safe(r.title)) + '</td><td><code>' + safe(r.formula) + '</code></td><td>' + safe(r.langs) + '</td><td class="refs">' + r.sources.map(x => '<a href="' + safe(x[1]) + '" target="_blank" rel="noopener">' + safe(x[0]) + '</a>').join(' · ') + '</td></tr>').join('');
    $('rule-table').innerHTML = '<div class="rule-scroll"><table class="rule-table"><thead><tr><th>Период</th><th>Правило</th><th>Формула</th><th>Языковые карточки</th><th>Источники</th></tr></thead><tbody>' + cells + '</tbody></table></div><p class="rule-note">Это записи из полного каталога фонем. Для сочетаний показываются формулы с точно совпадающей комбинацией, без подмены правилами отдельных составляющих.</p>';
    panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
$('rules-from').addEventListener('click', () => showRules('from'));
$('rules-to').addEventListener('click', () => showRules('to'));
$('go').addEventListener('click', find);
$('swap').addEventListener('click', () => { const a = vals.from, b = vals.to; setMode('from', PHSET.has(b) ? 'phoneme' : 'cluster'); setMode('to', PHSET.has(a) ? 'phoneme' : 'cluster'); selectState('from', b); selectState('to', a); find(); });
find();

// Critical atlas: classifications apply only to manually/previously assessed chains.
const ATLAS = window.ELDAMO_CHAINS;
let atlasMode = 'all';
let atlasPage = 0;
const atlasPageSize = 20;
const gradeInfo = { A: 'Непосредственно подтверждена', B: 'Хорошо обоснована', C: 'Частично обоснована', D: 'Формально возможна', U: 'Недостаточно данных', X: 'Противоречива', '—': 'Не оценена', unassessed: 'Не оценена' };
const atlasOutput = $('atlas-results');
const atlasCount = $('atlas-count');
const phase = () => $('era').value;
const atlasLink = url => /^https:\/\/eldamo\.org\//.test(url) ? `<a class="atlas-link" href="${safe(url)}" target="_blank" rel="noopener">Eldamo ↗</a>` : '';
function atlasCard(chain) {
  const grade = chain.grade;
  const details = `<p>${safe(chain.reason)}</p><p><strong>Что проверить:</strong> ${safe(chain.action)}</p>`;
  return `<details class="atlas-card"><summary><span class="atlas-route">${chain.states.map(safe).join(' → ')}</span> <span class="atlas-grade" title="${safe(gradeInfo[grade])}">${safe(grade)} · ${safe(gradeInfo[grade])}</span></summary><div class="atlas-meta">${chain.era === 'late' ? 'Поздняя' : 'Средняя'} концепция · ${chain.kind === 'assessed' ? 'первоначальный критический атлас' : 'дополнительная оценённая цепочка'} · ${safe(chain.id)}</div>${details}${chain.evidence ? `<p><strong>Свидетельства:</strong> ${safe(chain.evidence)}</p>` : ''}${chain.markers ? `<p><strong>Маркеры:</strong> ${safe(chain.markers)}</p>` : ''}${chain.language ? `<p><strong>Языковые ступени:</strong> ${safe(chain.language)}</p>` : ''}${chain.sources ? `<p><strong>Источники:</strong> ${safe(chain.sources)}</p>` : ''}${chain.rules?.length ? `<p><strong>Правила:</strong> ${chain.rules.map(safe).join(' → ')}</p>` : ''}<div>${chain.urls.filter(Boolean).map(atlasLink).join('')}</div></details>`;
}
function atlasFiltered() {
  const q = $('atlas-query').value.trim().toLowerCase();
  const grade = $('atlas-grade').value;
  const useEra = $('atlas-period').checked;
  return ATLAS.filter(c => (!useEra || c.era === phase()) && (grade === 'all' || c.grade === grade) && (!q || c.states.join(' → ').toLowerCase().includes(q) || c.rules.some(r => r.toLowerCase().includes(q))));
}
function showAtlas() {
  atlasMode = 'all';
  const records = atlasFiltered();
  const pages = Math.max(1, Math.ceil(records.length / atlasPageSize));
  atlasPage = Math.max(0, Math.min(atlasPage, pages - 1));
  const view = records.slice(atlasPage * atlasPageSize, (atlasPage + 1) * atlasPageSize);
  atlasCount.textContent = `${records.length} цепочек · страница ${atlasPage + 1} из ${pages}. Оценки цепочек предварительны; вновь найденные пути не оценены.`;
  atlasOutput.innerHTML = (view.length ? view.map(atlasCard).join('') : '<div class="empty-info">Для этих фильтров цепочек нет.</div>') + (pages > 1 ? `<div class="atlas-pager"><button type="button" id="atlas-prev" ${atlasPage === 0 ? 'disabled' : ''}>← Назад</button><span>Страница ${atlasPage + 1} / ${pages}</span><button type="button" id="atlas-next" ${atlasPage === pages - 1 ? 'disabled' : ''}>Вперёд →</button></div>` : '');
  $('atlas-prev')?.addEventListener('click', () => { atlasPage--; showAtlas(); });
  $('atlas-next')?.addEventListener('click', () => { atlasPage++; showAtlas(); });
}
function showTree(direction) {
  atlasMode = direction;
  const root = direction === 'forward' ? vals.from : vals.to;
  const era = phase(), maxD = Number($('depth').value), requireStage = $('atlas-stage').checked;
  const ev = $('evidence').checked;
  const eligible = EDGES.filter(e => e.era === era && (!ev || e.tested));
  const adjacency = new Map();
  for (const e of eligible) {
    const from = direction === 'forward' ? e.a : e.b;
    if (!adjacency.has(from)) adjacency.set(from, []);
    adjacency.get(from).push(e);
  }
  const queue = [{ current: root, nodes: [root], edges: [], bound: direction === 'forward' ? -1 : 99, position: 'any' }];
  const found = [];
  let examined = 0, truncated = false;
  const maxStates = 50000, maxPaths = 1500;
  for (let head = 0; head < queue.length; head++) {
    const p = queue[head];
    if (++examined > maxStates) { truncated = true; break; }
    if (p.edges.length >= maxD) continue;
    for (const e of adjacency.get(p.current) || []) {
      if (requireStage && (direction === 'forward' ? e.stage < p.bound : e.stage > p.bound)) continue;
      const next = direction === 'forward' ? e.b : e.a;
      if (p.nodes.includes(next)) continue;
      if (p.position !== 'any' && e.position && e.position !== 'any' && e.position !== p.position) continue;
      const nodes = p.nodes.concat(next);
      const edges = p.edges.concat(e);
      const np = { current: next, nodes, edges, bound: e.stage, position: p.position === 'any' ? (e.position || 'any') : p.position };
      found.push(np);
      if (found.length >= maxPaths) { truncated = true; break; }
      queue.push(np);
    }
    if (truncated) break;
  }
  // Each result is one distinct sequence. Do not assign atlas grades based on endpoints.
  const groups = new Map();
  for (const path of found) {
    const depth = path.edges.length;
    if (!groups.has(depth)) groups.set(depth, []);
    groups.get(depth).push(path);
  }
  const shown = [...found].sort((a,b) => a.edges.length - b.edges.length || a.nodes.join().localeCompare(b.nodes.join())).slice(0, 250);
  const byStep = new Map();
  for (const p of shown) { const n = p.edges.length; if (!byStep.has(n)) byStep.set(n, []); byStep.get(n).push(p); }
  atlasCount.textContent = `${direction === 'forward' ? 'Развитие от' : 'Происхождение'} [${root}] · ${found.length} цепочек до ${maxD} шагов${truncated ? ' · поиск ограничен' : ''}. Отображаются первые ${shown.length}.`;
  atlasOutput.innerHTML = `<p class="atlas-note">Дерево структурных путей, не каталог доказанных этимологий. На каждом шаге учитывается период, ${requireStage ? 'порядок ступеней' : 'без ограничения ступеней'} и выбранный фильтр примеров. Результаты не получают автоматически категорий A–X/U.</p>` + ([...byStep].map(([n, paths]) => `<section class="atlas-tree-group"><h3>${n} ${n === 1 ? 'переход' : 'перехода'} · ${groups.get(n)?.length || 0} вариантов</h3>${paths.map(p => {
    const nodes = direction === 'forward' ? p.nodes : [...p.nodes].reverse();
    const edges = direction === 'forward' ? p.edges : [...p.edges].reverse();
    return `<details class="atlas-card"><summary>${nodes.map(safe).join(' → ')} <span class="atlas-grade">не оценена</span></summary><ol>${edges.map(e => `<li>${safe(e.a)} → ${safe(e.b)} · ${safe(e.marker)} · ${e.url ? `<a href="${safe(e.url)}" target="_blank" rel="noopener">${safe(e.rule)}</a>` : safe(e.rule)} ${e.exact ? '· пример шага' : '· нет точного примера'}</li>`).join('')}</ol></details>`;
  }).join('')}</section>`).join('') || '<div class="empty-info">В этом периоде и с выбранными ограничениями переходов не обнаружено.</div>');
}
$('all-chains').addEventListener('click', () => { atlasPage = 0; showAtlas(); });
$('develop-from').addEventListener('click', () => showTree('forward'));
$('origins-to').addEventListener('click', () => showTree('backward'));
for (const id of ['atlas-grade','atlas-period']) $(id).addEventListener('change', () => { atlasPage = 0; if (atlasMode === 'all') showAtlas(); });
$('atlas-query').addEventListener('input', () => { atlasPage = 0; if (atlasMode === 'all') showAtlas(); });
showAtlas();
