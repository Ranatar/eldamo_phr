// The start of the page, shown before the data of the page are read (the page is large):
// the intro with the examples and the recent words, or, for an address that opens a word, a
// line saying it is coming. word_ui.js takes it over (window.QINTRO).
(function () {
'use strict';
const T = window.I18N.t;
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const RECENT_KEY = 'quettamin-recent';
function recent() {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]').filter(r => r && r.id); } catch (_e) { return []; }
}
function remember(item) {
  const list = [item, ...recent().filter(r => r.id !== item.id)].slice(0, 8);
  try { localStorage.setItem(RECENT_KEY, JSON.stringify(list)); } catch (_e) { /* storage unavailable */ }
}
const chip = r => `<button type="button" class="chip" data-word="${esc(r.id)}" data-branch="${esc(r.b || '')}"><span class="marker">${esc(r.marker)}</span> <span class="form">${esc(r.form)}</span> <span class="muted">${esc(r.gloss)}</span></button>`;
const EXAMPLES = [
  { id: '403686503', b: 'quenya', marker: 'Q.', form: 'lindë', gloss: 'song, air, tune' },
  { id: '4273482913', b: 'quenya', marker: 'Q.', form: 'Ambar', gloss: 'world' },
  { id: '3005081253', b: 'sindarin', marker: 'S.', form: 'galadh', gloss: 'tree' },
  { id: '3880471189', b: 'quenya', marker: 'Q.', form: 'lelya', gloss: 'delicate, beautiful and fine' },
];
function render() {
  const rec = recent();
  $('intro').innerHTML = `<h1>${T('intro.title')}</h1>
    <p class="lead">${T('intro.lead')}</p>
    <p>${T('intro.examples')} ${EXAMPLES.map(chip).join(' ')}</p>
    ${rec.length ? `<p>${T('intro.recent')} ${rec.map(chip).join(' ')}</p>` : ''}
    <p class="small muted">${T('intro.note')}</p>`;
}
// before the data: the intro, or the word being opened
let raw = location.hash.slice(1);
try { raw = decodeURIComponent(raw); } catch (_e) { /* as is */ }
const p = new URLSearchParams(raw.includes('=') ? raw : '');
if (p.get('w') || p.get('f') || p.get('r')) {
  $('intro').hidden = true;
  const card = $('word-card');
  card.hidden = false;
  card.innerHTML = `<p class="muted">${T('page.loading')}</p>`;
} else render();
window.QINTRO = { render, recent, remember, chip };
})();
