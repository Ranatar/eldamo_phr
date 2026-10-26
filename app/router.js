// The address of the page: one set of parameters after '#', shared by the word
// tools (w, f, in, tab, dst) and the reference (ref, b, era, from, to, q, id).
// Old addresses of the phonetic atlas (#quenya?era=late&from=b&to=v) open the
// reference section "paths" with the same parameters.
(function () {
'use strict';
const BRANCHES = ['quenya', 'sindarin'];
const handlers = [];

function parse() {
  let raw = location.hash.slice(1);
  try { raw = decodeURIComponent(raw); } catch (_e) { /* malformed escape: use as is */ }
  const [head, query] = raw.split('?');
  if (BRANCHES.includes(head)) {
    // legacy address: branch name, then the parameters of the sound paths
    const p = new URLSearchParams(query || '');
    p.set('ref', 'paths');
    p.set('b', head);
    write(p, false);
    return p;
  }
  return new URLSearchParams(raw.includes('=') ? raw : '');
}

function write(params, push) {
  const s = params.toString();
  const url = s ? '#' + s : location.pathname + location.search;
  if (push) {
    if (s) location.hash = s;
    else location.hash = '';
    return;
  }
  try { history.replaceState(null, '', s ? url : url + '#'); } catch (_e) { /* file:// in some browsers */ }
}

// merge: {key: value}; null or '' removes the key
function set(changes, push) {
  const p = parse();
  for (const [k, v] of Object.entries(changes)) {
    if (v == null || v === '') p.delete(k);
    else p.set(k, String(v));
  }
  write(p, push);
  if (!push) for (const h of handlers) h(p, 'replace');
}

function on(handler) { handlers.push(handler); }
window.addEventListener('hashchange', () => { const p = parse(); for (const h of handlers) h(p, 'hash'); });

window.QR = { get: parse, set, on, BRANCHES };
})();
