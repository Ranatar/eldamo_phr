// Critical atlas: classifications apply only to manually/previously assessed chains.
const ATLAS = window.ELDAMO_CHAINS;
let atlasMode = 'all';
let atlasPage = 0;
const atlasPageSize = 20;
const gradeInfo = { A: 'Непосредственно подтверждена', B: 'Хорошо обоснована', C: 'Частично обоснована', D: 'Формально возможна', U: 'Недостаточно данных', X: 'Противоречива', '—': 'Не оценена' };
const atlasOutput = $('atlas-results');
const atlasCount = $('atlas-count');
const phase = () => $('era').value;
const atlasLink = url => /^https:\/\/eldamo\.org\//.test(url) ? `<a class="atlas-link" href="${safe(url)}" target="_blank" rel="noopener">Eldamo ↗</a>` : '';
function atlasCard(chain) {
  const grade = chain.grade;
  const details = chain.kind === 'assessed' ?
    `<p>${safe(chain.reason)}</p><p><strong>Что проверить:</strong> ${safe(chain.action)}</p>` :
    `<p>${safe(chain.reason)}</p><p><strong>Что проверить:</strong> ${safe(chain.action)}</p><p>Отдельные шаги с примером: ${safe(chain.supported ?? 'неизвестно')}.</p>`;
  return `<details class="atlas-card"><summary><span class="atlas-route">${chain.states.map(safe).join(' → ')}</span> <span class="atlas-grade" title="${safe(gradeInfo[grade])}">${safe(grade)} · ${safe(gradeInfo[grade])}</span></summary><div class="atlas-meta">${chain.era === 'late' ? 'Поздняя' : 'Средняя'} концепция · ${chain.kind === 'assessed' ? 'критический атлас' : 'новая структурная проекция'} · ${safe(chain.id)}</div>${details}${chain.evidence ? `<p><strong>Словоформы:</strong> ${safe(chain.evidence)}</p>` : ''}${chain.markers ? `<p><strong>Маркеры:</strong> ${safe(chain.markers)}</p>` : ''}${chain.language ? `<p><strong>Языковые ступени:</strong> ${safe(chain.language)}</p>` : ''}${chain.sources ? `<p><strong>Источники:</strong> ${safe(chain.sources)}</p>` : ''}${chain.rules?.length ? `<p><strong>Правила:</strong> ${chain.rules.map(safe).join(' → ')}</p>` : ''}<div>${chain.urls.filter(Boolean).map(atlasLink).join('')}</div></details>`;
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
  atlasCount.textContent = `${records.length} цепочек · страница ${atlasPage + 1} из ${pages}. A–X/U — исследовательские категории, «не оценена» — новая проекция.`;
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
  const queue = [{ current: root, nodes: [root], edges: [], bound: direction === 'forward' ? -1 : 99 }];
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
      const nodes = p.nodes.concat(next);
      const edges = p.edges.concat(e);
      const np = { current: next, nodes, edges, bound: e.stage };
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
