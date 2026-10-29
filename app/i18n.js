// Interface language of Quettamin: Russian or English.
// The catalog (app/messages.json, embedded by shared/app.py) maps an English key to
// {ru, en}; a plural entry has {ru: {one, few, many}, en: {one, other}}. Placeholders are
// {name}. The data of Eldamo (forms, glosses, rule names) are not translated.
// The language comes from the address (#lang=en), else from the last choice, else from
// the browser. A change redraws the page in place: the static markup is translated again and
// the parts of the page listen to the event 'quettamin:lang' (window) to draw themselves again.
(function () {
'use strict';
const MESSAGES = JSON.parse(document.getElementById('messages-data').textContent);
const LANGS = ['ru', 'en'];
const KEY = 'quettamin-lang';

function stored() { try { return localStorage.getItem(KEY); } catch (_e) { return null; } }
function store(v) { try { localStorage.setItem(KEY, v); } catch (_e) { /* storage unavailable */ } }
function fromHash() {
  let raw = location.hash.slice(1);
  try { raw = decodeURIComponent(raw); } catch (_e) { /* as is */ }
  const m = /(?:^|&)lang=(ru|en)(?:&|$)/.exec(raw);
  return m ? m[1] : null;
}
function initial() {
  const h = fromHash();
  if (h) { store(h); return h; }
  const s = stored();
  if (LANGS.includes(s)) return s;
  const nav = (navigator.languages && navigator.languages[0]) || navigator.language || 'ru';
  return /^(ru|uk|be|kk)\b/i.test(nav) ? 'ru' : 'en';
}
let lang = initial();
document.documentElement.lang = lang;

function fill(text, params) {
  if (!params) return text;
  return text.replace(/\{(\w+)\}/g, (m, k) => (params[k] != null ? String(params[k]) : m));
}
function entry(key) {
  const e = MESSAGES[key];
  if (!e) { console.warn('i18n: no message', key); return null; }
  return e;
}
// t('recon.go'), t('card.links', {n: 3})
function t(key, params) {
  const e = entry(key);
  if (!e) return key;
  const text = e[lang] != null ? e[lang] : e.ru;
  return fill(typeof text === 'string' ? text : text.other || text.many || '', params);
}
function category(n) {
  if (lang === 'ru') {
    const a = Math.abs(n) % 100, b = a % 10;
    if (a > 10 && a < 20) return 'many';
    if (b === 1) return 'one';
    if (b >= 2 && b <= 4) return 'few';
    return 'many';
  }
  return Math.abs(n) === 1 ? 'one' : 'other';
}
// tn('n.rules', 3) -> "3 правила" / "3 rules"; the number is {n}
function tn(key, n, params) {
  const e = entry(key);
  if (!e) return `${n} ${key}`;
  const forms = e[lang] || e.ru;
  const text = typeof forms === 'string' ? forms : (forms[category(n)] || forms.other || forms.many);
  return fill(text, Object.assign({ n }, params));
}
// static markup: data-i18n (text), data-i18n-html (trusted markup of the catalog),
// data-i18n-attr="placeholder:key;aria-label:key"
function translate(root) {
  for (const el of root.querySelectorAll('[data-i18n]')) el.textContent = t(el.dataset.i18n);
  for (const el of root.querySelectorAll('[data-i18n-html]')) el.innerHTML = t(el.dataset.i18nHtml);
  for (const el of root.querySelectorAll('[data-i18n-attr]')) {
    for (const pair of el.dataset.i18nAttr.split(';')) {
      const [attr, key] = pair.split(':');
      if (attr && key) el.setAttribute(attr.trim(), t(key.trim()));
    }
  }
}
function setLang(v) {
  if (!LANGS.includes(v) || v === lang) return;
  lang = v;
  store(v);
  document.documentElement.lang = v;
  let raw = location.hash.slice(1);
  try { raw = decodeURIComponent(raw); } catch (_e) { /* as is */ }
  const params = new URLSearchParams(raw.includes('=') ? raw : '');
  if (params.has('lang')) {
    params.set('lang', v);
    try { history.replaceState(null, '', '#' + params.toString()); } catch (_e) { /* file:// in some browsers */ }
  }
  translate(document);
  window.dispatchEvent(new CustomEvent('quettamin:lang', { detail: v }));
}
// a table of labels read in the current language: {key: 'message.key'} or {key: [symbol, 'message.key']}
function labels(map) {
  return new Proxy(map, {
    get(target, k) {
      const v = target[k];
      if (typeof v === 'string') return t(v);
      if (Array.isArray(v)) return [v[0], t(v[1])];
      return v;
    },
  });
}
// the page is shown once its static text is in the chosen language (template.html hides it until then)
function ready() {
  translate(document);
  document.documentElement.classList.remove('i18n-wait');
}

window.I18N = { get lang() { return lang; }, t, tn, translate, setLang, labels, ready, LANGS };
})();
