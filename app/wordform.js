// Word formation engine: a JavaScript port of shared/interpreter.py,
// shared/stress.py, shared/sequencer.py (run), shared/junctions.py (predict),
// shared/morphophonology.py, shared/orthography.py, shared/backform.py and
// shared/compound.py. tests/test_browser.py checks parity with the Python
// build on vectors exported by shared/app.py.
(function () {
'use strict';

// ---------------------------------------------------------------- phonemes
const SUBSCRIPTS = { '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9' };
const MODIFIERS = new Set(['ʰ', 'ʷ', 'ʲ']);
const MACRON = '̄', BREVE = '̆', ACUTE = '́';
const VOWEL_BASES = new Set('aeiouyæœøəɛɔɨɯǫęɑɒʊɪ');
const CLASSES = new Set(['V', 'C', 'X', 'S']);
const EQUIVALENT = { 'þ': 'θ', 'ñ': 'ŋ', 'ʒ': 'ɣ' };
const BOUNDARY_CHARS = new Set(['+', '’', "'", 'ʼ', '·']);
const LABIALIZABLE = new Set(['k', 'g']);
const DIPHTHONGS = new Set(['ai', 'au', 'oi', 'ui', 'eu', 'iu', 'ei', 'ou', 'ae', 'oe', 'œi', 'yi', 'yu']);
const MARK = /\p{M}/u;

class Unsupported extends Error {}

const nfc = s => s.normalize('NFC');
const nfd = s => s.normalize('NFD');
const isMark = ch => MARK.test(ch);
const chars = s => Array.from(s);

function phonemes(s) {
  const out = [];
  for (const ch of chars(nfd(s))) {
    if (out.length && (isMark(ch) || MODIFIERS.has(ch))) out[out.length - 1] += ch;
    else out.push(ch);
  }
  return out.map(nfc);
}

function canonical(p) {
  p = nfc(p);
  if (!p) return p;
  const cs = chars(p);
  p = (EQUIVALENT[cs[0]] || cs[0]) + cs.slice(1).join('');
  const d = chars(nfd(p));
  return nfc(d[0] + d.slice(1).filter(c => c !== BREVE && c !== ACUTE).join(''));
}
const base = p => { const d = chars(nfd(p)); return d.length ? d[0] : ''; };
const isVowel = p => VOWEL_BASES.has(base(p));
const isLong = p => nfd(p).includes(MACRON);
const shorten = p => nfc(chars(nfd(p)).filter(c => c !== MACRON && c !== BREVE).join(''));
function lengthen(p) { const d = chars(nfd(shorten(p))); return nfc(d[0] + MACRON + d.slice(1).join('')); }
const join = ph => nfc(ph.join(''));
const r3 = x => Number(x.toFixed(3));   // Python round(x, 3)

// ---------------------------------------------------------------- patterns
function token(kind, o = {}) {
  return { kind, options: o.options || [], cls: o.cls || '', length: o.length || '', index: o.index || '',
           star: !!o.star, stress: o.stress || '' };
}
const tokenKey = t => JSON.stringify([t.kind, t.options, t.cls, t.length, t.index, t.star, t.stress]);
const family = t => t.kind === 'class' ? t.cls : t.kind;

function splitTop(s, sep = '|') {
  let depth = 0, start = 0; const parts = [];
  const cs = chars(s);
  for (let i = 0; i < cs.length; i++) {
    const ch = cs[i];
    if (ch === '{') depth++;
    else if (ch === '}') { depth--; if (depth < 0) throw new Unsupported('unbalanced braces'); }
    else if (ch === sep && depth === 0) { parts.push(cs.slice(start, i).join('')); start = i + 1; }
  }
  if (depth) throw new Unsupported('unbalanced braces');
  parts.push(cs.slice(start).join(''));
  return parts;
}

function positionOf(s) {
  s = s.trim();
  if (s.startsWith('[') && s.endsWith(']')) s = s.slice(1, -1);
  const lead = s.startsWith('-'), trail = s.endsWith('-') && chars(s).length > 1;
  const cs = chars(s);
  const core = cs.slice(lead ? 1 : 0, trail ? cs.length - 1 : cs.length).join('');
  if (lead && trail) return [core, 'medial'];
  if (trail) return [core, 'initial'];
  if (lead) return [core, 'final'];
  return [core, 'any'];
}

function readTail(s, i) {
  let mods = '';
  while (i < s.length && (isMark(s[i]) || MODIFIERS.has(s[i]))) { mods += s[i]; i++; }
  let idx = '';
  while (i < s.length && SUBSCRIPTS[s[i]]) { idx += SUBSCRIPTS[s[i]]; i++; }
  return [mods, idx, i];
}

function parsePattern(text) {
  const [core, position] = positionOf(text);
  for (const ch of '?()/=<>') if (core.includes(ch)) throw new Unsupported('notation not defined by Eldamo documentation');
  const s = chars(nfd(core));
  const tokens = [];
  let i = 0, pending = '', mark = 0;
  while (i < s.length) {
    if (pending && tokens.length > mark) { tokens[mark].stress = pending; pending = ''; }
    const ch = s[i];
    if (ch === 'ˌ' || ch === 'ˈ') { pending = ch === 'ˌ' ? 'unstressed' : 'stressed'; mark = tokens.length; i++; continue; }
    if (ch === ' ' || ch === '\t') throw new Unsupported('space inside pattern');
    if (ch === '{') {
      const j = s.indexOf('}', i);
      if (j < 0) throw new Unsupported('unclosed group');
      const raw = s.slice(i + 1, j).join('');
      const [mods, idx, ni] = readTail(s, j + 1); i = ni;
      let opts;
      if (raw.includes('|')) opts = raw.split('|').filter(o => o).map(o => phonemes(o + mods));
      else {
        opts = phonemes(nfc(raw)).map(p => [p]);
        if (mods) opts = opts.map(o => [nfc(o[0] + mods)]);
      }
      if (!opts.length) throw new Unsupported('empty group');
      if (opts.some(o => o.some(p => chars(p).some(c => CLASSES.has(c))))) throw new Unsupported('class inside group');
      tokens.push(token('set', { options: opts, index: idx, stress: mods.includes(ACUTE) ? 'stressed' : '' }));
      continue;
    }
    if (ch === '+') { tokens.push(token('boundary')); i++; continue; }
    if (ch === '*') {
      if (!tokens.length || tokens[tokens.length - 1].kind === 'null' || tokens[tokens.length - 1].kind === 'boundary')
        throw new Unsupported('star without token');
      tokens[tokens.length - 1].star = true; i++; continue;
    }
    if (SUBSCRIPTS[ch]) throw new Unsupported('subscript without token');
    if (ch === '}') throw new Unsupported('unbalanced braces');
    const [mods, idx, nxt] = readTail(s, i + 1);
    if (CLASSES.has(ch)) {
      const length = mods.includes(MACRON) ? 'long' : mods.includes(BREVE) ? 'short' : '';
      if (ch !== 'V' && mods.split(ACUTE).join('')) throw new Unsupported('diacritic on non-vowel class');
      tokens.push(token('class', { cls: ch, length, index: idx }));
    } else if (ch === 'ø') tokens.push(token('null', { index: idx }));
    else tokens.push(token('lit', { options: [[nfc(ch + mods)]], index: idx }));
    if (mods.includes(ACUTE)) tokens[tokens.length - 1].stress = 'stressed';
    i = nxt;
  }
  if (pending && tokens.length > mark) tokens[mark].stress = pending;
  return { tokens, position, text };
}

// ---------------------------------------------------------------- matching
function litEq(pattern, sound) {
  if (nfd(pattern).includes(BREVE) && isLong(sound)) return false;
  return canonical(pattern) === canonical(sound);
}

function stressOk(tok, word, i, end, stress) {
  if (!tok.stress || stress == null) return true;
  const vowels = [];
  for (let k = i; k < end; k++) if (isVowel(word[k])) vowels.push(k);
  if (!vowels.length) return true;
  const hit = vowels.some(k => stress.has(k));
  return tok.stress === 'stressed' ? hit : !hit;
}

function* matchToken(tok, word, i, openStart, stress, bounds) {
  if (tok.kind === 'boundary') { if (bounds == null || bounds.has(i)) yield [i, [], null]; return; }
  for (const r of matchPlain(tok, word, i, openStart)) if (stressOk(tok, word, i, r[0], stress)) yield r;
}

function* matchPlain(tok, word, i, openStart) {
  if (tok.kind === 'null') { yield [i, [], null]; return; }
  if (tok.kind === 'lit' || tok.kind === 'set') {
    for (let k = 0; k < tok.options.length; k++) {
      const opt = tok.options[k], n = opt.length;
      if (i + n <= word.length && opt.every((x, t) => litEq(x, word[i + t]))) yield [i + n, word.slice(i, i + n), k];
    }
    return;
  }
  if (tok.cls === 'S') { yield* matchSyllable(word, i, openStart); return; }
  if (i >= word.length) return;
  const p = word[i];
  if (tok.cls === 'C' && i + 1 < word.length && LABIALIZABLE.has(base(p)) && word[i + 1] === 'w') yield [i + 2, [p, 'w'], null];
  let ok;
  if (tok.cls === 'X') ok = true;
  else if (tok.cls === 'C') ok = !isVowel(p);
  else ok = isVowel(p) && (tok.length === '' || (tok.length === 'long') === isLong(p));
  if (ok) yield [i + 1, [p], null];
}

function* matchSyllable(word, i, openStart) {
  const n = word.length;
  if (openStart) {
    let k = i;
    while (k < n && !isVowel(word[k])) { k++; yield [k, word.slice(i, k), null]; }
  }
  let j = i;
  while (j < n && !isVowel(word[j])) j++;
  if (j >= n) return;
  const nuclei = [j + 1];
  if (j + 1 < n && isVowel(word[j + 1]) && 'iue'.includes(base(word[j + 1])) && !isLong(word[j + 1])) nuclei.push(j + 2);
  for (const k of nuclei) {
    let end = k; const ends = [end];
    while (end < n && !isVowel(word[end])) { end++; ends.push(end); }
    for (const e of ends) yield [e, word.slice(i, e), null];
  }
}

function* matchAt(pattern, word, start, fragment, stress, bounds) {
  const [leadFragment, trailFragment] = fragment;
  const pos = pattern.position;
  function* rec(t, i, caps) {
    if (t === pattern.tokens.length) {
      if (pos === 'initial' && (start !== 0 || leadFragment)) return;
      if (pos === 'final' && i !== word.length) return;
      if (pos === 'medial' && ((start === 0 && !leadFragment) || (i === word.length && !trailFragment))) return;
      yield [i, caps.slice()];
      return;
    }
    const tok = pattern.tokens[t];
    if (tok.star) {
      let spans = [[i, []]], frontier = [[i, []]];
      while (frontier.length) {
        const nxt = [];
        for (const [at, cap] of frontier)
          for (const [end, c] of matchToken(tok, word, at, leadFragment && at === 0, stress, bounds))
            if (end > at) nxt.push([end, cap.concat(c)]);
        spans = spans.concat(nxt); frontier = nxt;
      }
      const sorted = spans.map((s, k) => [s, k]).sort((a, b) => (b[0][0] - a[0][0]) || (a[1] - b[1])).map(x => x[0]);
      for (const [end, cap] of sorted) yield* rec(t + 1, end, caps.concat([[cap, null]]));
      return;
    }
    for (const [end, cap, opt] of matchToken(tok, word, i, leadFragment && i === 0, stress, bounds))
      yield* rec(t + 1, end, caps.concat([[cap, opt]]));
  }
  yield* rec(0, start, []);
}

function offglide(word, i) {
  const a = word[i - 1], b = word[i];
  return isVowel(a) && isVowel(b) && !isLong(a) && !isLong(b)
    && DIPHTHONGS.has(chars(canonical(a))[0] + chars(canonical(b))[0])
    && !(i >= 2 && offglide(word, i - 1));
}

// ---------------------------------------------------------------- alignment and output
function compatible(a, b) {
  if (a.kind === 'boundary' || b.kind === 'boundary') return a.kind === b.kind ? 0 : 2;
  if (a.kind === 'null' || b.kind === 'null') return 0;
  if (a.index && b.index && a.index === b.index) return 0;
  if (a.kind === 'class' && b.kind === 'class' && family(a) === family(b)) return 0;
  if (a.kind === 'set' && b.kind === 'set' && a.options.length === b.options.length) return 0;
  if (a.kind === 'lit' && b.kind === 'lit') {
    const x = a.options[0], y = b.options[0];
    if (x.length === 1 && y.length === 1) {
      if (litEq(x[0], y[0])) return 0;
      return isVowel(x[0]) === isVowel(y[0]) ? 1 : 2;
    }
    return 2;
  }
  return 2;
}

function align(src, dst) {
  if (src.length === dst.length) return src.map((s, k) => [s, dst[k]]);
  const n = src.length, m = dst.length, INF = 1e9;
  const cost = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(INF));
  const back = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(null));
  cost[0][0] = 0;
  for (let i = 0; i <= n; i++) for (let j = 0; j <= m; j++) {
    if (cost[i][j] === INF) continue;
    if (i < n && j < m) { const c = cost[i][j] + compatible(src[i], dst[j]); if (c < cost[i + 1][j + 1]) { cost[i + 1][j + 1] = c; back[i + 1][j + 1] = [i, j, 'pair']; } }
    if (i < n) { const c = cost[i][j] + 2; if (c < cost[i + 1][j]) { cost[i + 1][j] = c; back[i + 1][j] = [i, j, 'del']; } }
    if (j < m) { const c = cost[i][j] + 2; if (c < cost[i][j + 1]) { cost[i][j + 1] = c; back[i][j + 1] = [i, j, 'ins']; } }
  }
  const out = []; let i = n, j = m;
  while (i !== 0 || j !== 0) {
    const [pi, pj, op] = back[i][j];
    out.push([op !== 'ins' ? src[pi] : null, op !== 'del' ? dst[pj] : null]);
    i = pi; j = pj;
  }
  return out.reverse();
}

function render(outTok, inTok, cap, opt, bound) {
  if (outTok == null) return [[]];
  if (outTok.kind === 'null' || outTok.kind === 'boundary') return [[]];
  if (outTok.kind === 'lit') return [outTok.options[0].slice()];
  if (outTok.kind === 'set') {
    let k = null;
    if (inTok && inTok.kind === 'set' && inTok.options.length === outTok.options.length) k = opt;
    if (outTok.index && bound[outTok.index] && bound[outTok.index][1] != null
        && bound[outTok.index][2].options.length === outTok.options.length) k = bound[outTok.index][1];
    if (k == null) throw new Unsupported('output set without a paired input set');
    return [outTok.options[k].slice()];
  }
  let source = null;
  if (outTok.index && bound[outTok.index]) source = bound[outTok.index][0];
  else if (inTok && (inTok.kind === 'class' || inTok.kind === 'set' || inTok.kind === 'lit')) source = cap;
  if (source == null) throw new Unsupported('output class without a source');
  source = source.slice();
  if (outTok.star || (inTok && inTok.star)) return [source];
  if (outTok.cls === 'V' && source.length) {
    const v = source[source.length - 1], head = source.slice(0, -1);
    if (outTok.length === 'long') return [head.concat([lengthen(v)])];
    if (outTok.length === 'short') return [head.concat([shorten(v)])];
    if (inTok && inTok.kind === 'class' && inTok.length && inTok.length !== outTok.length) return [source, head.concat([shorten(v)])];
  }
  return [source];
}

function familyKey(t) {
  if (t.kind === 'class') return 'class:' + family(t);
  if (t.kind === 'set') return 'set:' + t.options.length;
  return '';
}

function product(lists) {
  let out = [[]];
  for (const l of lists) { const nxt = []; for (const p of out) for (const x of l) nxt.push(p.concat([x])); out = nxt; }
  return out;
}

function correspondences(src, dst) {
  const families = new Map();
  src.forEach((t, i) => { const k = familyKey(t); if (k && !t.index) { if (!families.has(k)) families.set(k, [[], []]); families.get(k)[0].push(i); } });
  dst.forEach((t, j) => { const k = familyKey(t); if (k && !t.index) { if (!families.has(k)) families.set(k, [[], []]); families.get(k)[1].push(j); } });
  const options = [];
  for (const [k, [ins, outs]] of families) {
    if (!outs.length) continue;
    if (outs.length > ins.length) {
      if (!ins.length) { options.push([{}]); continue; }
      throw new Unsupported('more output than input members of ' + k);
    }
    const keep = outs.length > 1 ? ins.slice(0, outs.length - 1).concat([ins[ins.length - 1]]) : ins.slice(0, 1);
    const map = {}; outs.forEach((o, n) => { map[o] = keep[n]; });
    options.push([map]);
  }
  const maps = [];
  for (const combo of (options.length ? product(options) : [[]])) maps.push(Object.assign({}, ...combo));
  return maps;
}

function transform(src, dst, captures) {
  const caps = captures, bound = {};
  src.tokens.forEach((tok, i) => { if (tok.index) bound[tok.index] = [caps[i][0], caps[i][1], tok]; });
  const keys = src.tokens.map(tokenKey);
  const positional = new Map();
  for (const [a, b] of align(src.tokens, dst.tokens)) if (a && b) positional.set(b, keys.indexOf(tokenKey(a)));
  const results = [];
  for (const mapping of correspondences(src.tokens, dst.tokens)) {
    const pieces = dst.tokens.map((b, j) => {
      const i = j in mapping ? mapping[j] : (positional.has(b) ? positional.get(b) : null);
      const a = i != null ? src.tokens[i] : null;
      const [cap, opt] = i != null ? caps[i] : [[], null];
      return render(b, a, cap, opt, bound);
    });
    for (const combo of product(pieces)) results.push([].concat(...combo));
  }
  return results;
}

// ---------------------------------------------------------------- rules
function parseRule(src, dst) {
  const a = splitTop(src.trim()), b = splitTop(dst.trim());
  if (a.length !== b.length) throw new Unsupported('unpaired top-level alternatives');
  const alts = [];
  for (let k = 0; k < a.length; k++) {
    const px = parsePattern(a[k]), py = parsePattern(b[k]);
    if (px.position !== py.position) throw new Unsupported('different position constraints');
    if (!px.tokens.length) throw new Unsupported('empty input pattern');
    alts.push([px, py]);
  }
  return alts;
}
const ruleCache = new Map();
function compileRule(src, dst) {
  const key = src + '\u0000' + dst;
  if (!ruleCache.has(key)) {
    try { ruleCache.set(key, { alts: parseRule(src, dst) }); } catch (e) { ruleCache.set(key, { error: e }); }
  }
  const r = ruleCache.get(key);
  if (r.error) throw r.error;
  return r.alts;
}

function sites(alts, word, fragment, stress, bounds) {
  const out = [];
  for (let start = 0; start <= word.length; start++)
    for (const [src, dst] of alts)
      for (const [end, caps] of matchAt(src, word, start, fragment, stress, bounds)) {
        if (end === start && src.tokens.every(t => t.kind === 'null' || t.kind === 'boundary')) continue;
        out.push([start, end, transform(src, dst, caps)]);
      }
  return out;
}

function boundaries(form) {
  const s = nfc(form.trim());
  if (!s.includes('+')) return null;
  const out = new Set(); let k = 0;
  const kept = chars(s).filter(ch => !(BOUNDARY_CHARS.has(ch) && ch !== '+') && ch !== '-' && !/\s/.test(ch)).join('');
  for (const part of phonemes(kept)) { if (part === '+') out.add(k); else k++; }
  return out;
}

function rebuild(word, changes, bounds) {
  bounds = bounds || new Set();
  const res = []; let cursor = 0;
  const copy = (a, b) => { for (let k = a; k < b; k++) { if (bounds.has(k)) res.push('+'); res.push(word[k]); } };
  for (const [cs, ce, repl] of changes) {
    copy(cursor, cs);
    if (bounds.has(cs)) res.push('+');
    res.push(...repl);
    for (const k of bounds) if (cs < k && k < ce) { res.push('+'); break; }
    cursor = ce;
  }
  copy(cursor, word.length);
  if (bounds.has(word.length)) res.push('+');
  return join(res);
}

function normalizeWord(form) {
  const s = nfc(form.trim());
  const lead = s.startsWith('-'), trail = s.endsWith('-');
  const kept = chars(s).filter(ch => !BOUNDARY_CHARS.has(ch) && ch !== '-' && !/\s/.test(ch)).join('');
  return [phonemes(kept), [lead, trail]];
}

function cmpChange(a, b) {
  if (a[0] !== b[0]) return a[0] - b[0];
  if (a[1] !== b[1]) return a[1] - b[1];
  const x = a[2], y = b[2];
  for (let k = 0; k < Math.min(x.length, y.length); k++) if (x[k] !== y[k]) return x[k] < y[k] ? -1 : 1;
  return x.length - y.length;
}

function applyRule(alts, form, opts = {}) {
  const limit = opts.limit || 64;
  const [word, fragment] = normalizeWord(form);
  const stress = opts.stressMode ? stressed(word, opts.stressMode) : null;
  const bounds = boundaries(form);
  let ss = sites(alts, word, fragment, stress, bounds);
  if (opts.scope) {
    const n = syllableCount(word);
    if (opts.scope === 'mono') ss = ss.filter(x => n === 1 && x[1] === word.length && !word.slice(0, x[0]).some(isVowel));
    else if (opts.scope === 'poly' && n < 2) ss = [];
  }
  if (opts.protect) {
    const guarded = sites(opts.protect, word, fragment, stress, bounds).map(([st, en]) => [st, en]);
    if (guarded.length) {
      const free = (cs, ce) => !guarded.some(([st, en]) => ce > cs ? (cs < en && ce > st) : (st < cs && cs < en));
      ss = ss.filter(([st, en]) => free(st, en));
    }
  }
  const changes = [];
  for (const [start, end, outs] of ss) {
    const variants = [], seen = new Set();
    const span = word.slice(start, end);
    for (const o of outs.slice(0, limit)) {
      let pre = 0;
      while (pre < span.length && pre < o.length && canonical(span[pre]) === canonical(o[pre])) pre++;
      let suf = 0;
      while (suf < span.length - pre && suf < o.length - pre && canonical(span[span.length - 1 - suf]) === canonical(o[o.length - 1 - suf])) suf++;
      if (pre === span.length && span.length === o.length) continue;
      if (pre === 0 && start > 0 && start < word.length && offglide(word, start)) continue;
      const v = [start + pre, end - suf, o.slice(pre, o.length - suf)];
      const key = JSON.stringify(v);
      if (!seen.has(key)) { seen.add(key); variants.push(v); }
    }
    if (variants.length) changes.push(variants);
  }
  const ordered = [], all = new Set();
  if (changes.length) {
    // itertools.product order, first `limit` combinations
    const idx = new Array(changes.length).fill(0);
    for (let count = 0; count < limit; count++) {
      const combo = changes.map((c, k) => c[idx[k]]).slice().sort(cmpChange);
      const chosen = []; let last = -1;
      for (const [cs, ce, repl] of combo) {
        if (cs >= last && !(cs === ce && ce === last)) { chosen.push([cs, ce, repl]); last = Math.max(ce, cs + (cs === ce ? 1 : 0)); }
      }
      const out = rebuild(word, chosen, bounds);
      if (!all.has(out)) { all.add(out); ordered.push(out); }
      let k = changes.length - 1;
      while (k >= 0) { idx[k]++; if (idx[k] < changes[k].length) break; idx[k] = 0; k--; }
      if (k < 0) break;
    }
  }
  return { ordered, sites: ss.length };
}

function comparable(form) {
  const [word] = normalizeWord(form);
  const out = [];
  for (const p of word.map(canonical)) {
    if (out.length && isVowel(p) && !isLong(p) && out[out.length - 1] === p) out[out.length - 1] = lengthen(p);
    else out.push(p);
  }
  return join(out);
}

// ---------------------------------------------------------------- stress
function nuclei(word) {
  const out = []; let i = 0;
  const syllabic = p => !isVowel(p) && nfd(p).includes('̣');
  while (i < word.length) {
    const p = word[i];
    if (!(isVowel(p) || syllabic(p))) { i++; continue; }
    if (i + 1 < word.length && isVowel(p) && isVowel(word[i + 1]) && !isLong(p) && !isLong(word[i + 1])
        && DIPHTHONGS.has(base(p) + base(word[i + 1]))) { out.push([i, i + 2, true]); i += 2; continue; }
    out.push([i, i + 1, isVowel(p) && isLong(p)]); i++;
  }
  return out;
}
const LONG_CONSONANTS = { 'latin-sindarin': new Set(['f', 'ɸ']) };
function heavy(word, ns, k, mode = 'latin') {
  const [, end, long] = ns[k];
  if (long) return true;
  const nxt = k + 1 < ns.length ? ns[k + 1][0] : word.length;
  if (nxt - end === 1 && k + 1 < ns.length && (LONG_CONSONANTS[mode] || new Set()).has(base(word[end]))) return true;
  return nxt - end >= 2;
}
function stressed(word, mode) {
  if (!mode) return null;
  const marked = [];
  word.forEach((p, i) => { if (nfd(p).includes(ACUTE)) marked.push(i); });
  if (marked.length) return new Set(marked);
  const ns = nuclei(word);
  if (!ns.length) return new Set();
  let k;
  if (mode === 'initial' || ns.length <= 2) k = 0;
  else k = heavy(word, ns, ns.length - 2, mode) ? ns.length - 2 : ns.length - 3;
  const [s, e] = ns[k];
  const out = new Set(); for (let x = s; x < e; x++) out.add(x);
  return out;
}
const syllableCount = word => nuclei(word).length;

// ---------------------------------------------------------------- sequencer
function compileSequence(rules) {
  return rules.map(r => {
    const comp = list => { const alts = []; for (const [f, t] of list) { try { alts.push(...compileRule(f, t)); } catch (e) { if (!(e instanceof Unsupported)) throw e; } } return alts; };
    const plain = comp(r.alts), plus = comp(r.all);
    return Object.assign({}, r, { rule: r.alts.length ? plain : null, rulePlus: r.all.length ? plus : null,
                                  protectAlts: r.protect.length ? comp(r.protect) : null });
  });
}

function applyCompiled(c, alts, form) {
  if (!alts) return [];
  try { return applyRule(alts, form, { protect: c.protectAlts, stressMode: c.stress, scope: c.scope }).ordered; }
  catch (e) { if (e instanceof Unsupported) return []; throw e; }
}

const MAX_VARIANTS = 24;
function run(form, rules, branchOptional = true) {
  let variants = [{ form, trace: [] }];
  for (const c of rules) {
    if (!c.rule && !c.rulePlus) continue;
    const nxt = [];
    for (const v of variants) {
      const marked = v.form.includes('+');
      const mainRule = marked && c.rulePlus ? c.rulePlus : c.rule;
      const outs = applyCompiled(c, mainRule, v.form);
      let extra = [];
      if (!marked && c.rulePlus) extra = applyCompiled(c, c.rulePlus, v.form).filter(o => !outs.includes(o));
      if (!outs.length) nxt.push(v);
      const keep = outs.length && c.optional && branchOptional;
      if (keep && c.rare) nxt.push({ form: v.form, trace: v.trace.concat([[c.id, v.form, null]]) });
      for (const o of outs) nxt.push({ form: o, trace: v.trace.concat([[c.id, v.form, o]]) });
      if (keep && !c.rare) nxt.push({ form: v.form, trace: v.trace.concat([[c.id, v.form, null]]) });
      for (const o of extra) nxt.push({ form: o, trace: v.trace.concat([[c.id, v.form, o]]) });
    }
    const seen = new Set(); variants = [];
    for (const v of nxt) { const k = comparable(v.form); if (!seen.has(k)) { seen.add(k); variants.push(v); } }
    variants = variants.slice(0, MAX_VARIANTS);
  }
  return variants;
}

function sequence(rules, era, first, last) {
  return rules.filter(c => c.era === era && first <= c.stage && c.stage <= last);
}

// ---------------------------------------------------------------- orthography
const QUENYA = [['x', 'ks'], ['χ', 'x'], ['ph', 'f'], ['nqu', 'ŋkw'], ['ngw', 'ŋgw'], ['qu', 'kw'], ['q', 'kw'],
  ['nc', 'ŋk'], ['nk', 'ŋk'], ['ng', 'ŋg'], ['ñ', 'ŋ'], ['hy', 'j̊'], ['hw', 'w̥'], ['hl', 'l̥'], ['hr', 'r̥'], ['ht', 'xt'],
  ['c', 'k'], ['þ', 'θ'], ['th', 'θ'], ['y', 'j']];
const SINDARIN = [['ch', 'x'], ['th', 'θ'], ['dh', 'ð'], ['lh', 'l̥'], ['rh', 'r̥'], ['mh', 'ṽ'], ['hm', 'm̥'], ['hn', 'n̥'],
  ['wh', 'w̥'], ['nc', 'ŋk'], ['ng', 'ŋg'], ['ñ', 'ŋ'], ['c', 'k'], ['þ', 'θ'], ['k', 'k']];
function longMarks(text) {
  const out = [];
  for (const ch of chars(nfd(text))) {
    if (ch === ACUTE || ch === '̂') { if (!out.length || out[out.length - 1] !== MACRON) out.push(MACRON); }
    else if (ch === '̈' || ch === BREVE) continue;
    else out.push(ch);
  }
  return nfc(out.join(''));
}
function cleanForm(form) { return form.trim().replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰]/g, '').replace(/\([^)]*\)/g, '').trim(); }
const replaceAll = (s, a, b) => s.split(a).join(b);
function toPhonetic(form, fam) {
  let f = longMarks(cleanForm(form)).toLowerCase();
  if (fam === 'quenya') {
    if (f.startsWith('ñ')) f = 'n' + f.slice(1);
    for (const [a, b] of QUENYA) f = replaceAll(f, a, b);
    return f;
  }
  for (const [a, b] of SINDARIN) f = replaceAll(f, a, b);
  f = f.replace(/(?<=.)f/gu, 'v');
  f = f.replace(/^ph/u, 'f').replace(/ph$/u, 'f');
  f = replaceAll(f, 'ph', 'ff');
  f = f.replace(/ŋg$/u, 'ŋ');
  f = f.replace(/(?<=[aā])w$/u, 'u');
  f = f.replace(/(?<=[^aeiouyāēīōūȳ])w$/u, 'u');
  f = f.replace(/^i(?=[aeouāēōū])/u, 'j');
  return f;
}

// ---------------------------------------------------------------- junctions
const keyOf = parts => JSON.stringify(parts);
function junctionPredict(table, a, b, limit = 10) {
  const sk = shortKey(b);
  const shorts = sk && table.short[sk] ? table.short[sk] : [[false, 1]];
  const sn = shorts.reduce((x, [, n]) => x + n, 0);
  const out = new Map();
  for (const [short, sc] of shorts) {
    const bb = short ? shortAll(b) : b;
    for (const [form, p, jo, eo] of junctionPredict1(table, a, bb, limit)) {
      const q = p * sc / sn;
      if (!out.has(form) || out.get(form)[0] < q) out.set(form, [q, jo, eo, short]);
    }
  }
  return [...out.entries()].sort((x, y) => y[1][0] - x[1][0]).slice(0, limit)
    .map(([f, [p, jo, eo, s]]) => [f, r3(p), jo, eo, s]);
}
const shortAll = p => p.map(x => isVowel(x) ? shorten(x) : x);
function shortKey(b) {
  if (!b.some(isLong)) return null;
  const vs = b.map((x, i) => [x, i]).filter(([x]) => isVowel(x)).map(([, i]) => i);
  return isLong(b[vs[vs.length - 1]]) ? 'last' : 'earlier';
}
function junctionPredict1(table, a, b, limit) {
  const jops = new Map((table.junction[keyOf([a[a.length - 1], b[0]])] || []).map(([op, n]) => [keyOf(op), n]));
  const eops = new Map((table.ending[keyOf(b.slice(-2))] || []).map(([op, n]) => [keyOf(op), n]));
  const plainJ = keyOf([0, 0, '']), plainE = keyOf([0, '']);
  const hadJ = jops.size, hadE = eops.size;
  jops.set(plainJ, (jops.get(plainJ) || 0) + (hadJ ? table.smoothing : 1));
  eops.set(plainE, (eops.get(plainE) || 0) + (hadE ? table.smoothing : 1));
  const jn = [...jops.values()].reduce((x, y) => x + y, 0), en = [...eops.values()].reduce((x, y) => x + y, 0);
  const out = new Map();
  // iteration order follows Counter insertion order in Python (exported as ordered lists)
  for (const [jk, jc] of jops) {
    const [k, m, rep] = JSON.parse(jk);
    if (k > a.length || m > b.length) continue;
    const joined = a.slice(0, a.length - k).concat(phonemes(rep), b.slice(m));
    for (const [ek, ec] of eops) {
      const [ke, repe] = JSON.parse(ek);
      if (ke > b.length - m || ke > joined.length) continue;
      const form = join(joined.slice(0, joined.length - ke).concat(phonemes(repe)));
      const p = (jc / jn) * (ec / en);
      if (!out.has(form) || out.get(form)[0] < p) out.set(form, [p, JSON.parse(jk), JSON.parse(ek)]);
    }
  }
  return [...out.entries()].sort((x, y) => y[1][0] - x[1][0]).slice(0, limit * 2).map(([f, [p, jo, eo]]) => [f, p, jo, eo]);
}

// ---------------------------------------------------------------- morphophonology (Quenya §6.1, Sindarin lenition)
const FINAL_OK = new Set(['t', 's', 'n', 'r', 'l']);
const lastVowel = w => { for (let i = w.length - 1; i >= 0; i--) if (isVowel(w[i])) return i; return null; };
function reduceCompound(word) {
  if (syllableCount(word) < 3 || !isVowel(word[word.length - 1]) || isLong(word[word.length - 1])) return null;
  if (word.length > 1 && isVowel(word[word.length - 2])) return null;
  const stem = word.slice(0, -1);
  let form = stem.slice();
  const v = lastVowel(form);
  if (v != null && isLong(form[v])) form[v] = shorten(form[v]);
  const coda = v != null ? form.length - 1 - v : 0;
  if (coda > 1) form = form.slice(0, v + 2);
  if (form.length && form[form.length - 1] === 'm') form[form.length - 1] = 'n';
  if (form.length && !isVowel(form[form.length - 1]) && !FINAL_OK.has(form[form.length - 1])) return null;
  return [form, stem];
}
function shortenFinalLong(word, boundary) {
  const tail = word.slice(boundary);
  if (syllableCount(tail) !== 1) return null;
  const v = lastVowel(word);
  if (v == null || v < boundary || !isLong(word[v])) return null;
  const out = word.slice(); out[v] = shorten(out[v]); return out;
}
function prosodicLengthening(base, suffix, eNoun = false) {
  if (syllableCount(base) < 3 || !suffix.length) return null;
  const ns = nuclei(base);
  const sSyl = syllableCount(suffix);
  if (isVowel(base[base.length - 1])) {
    if (isVowel(suffix[0]) || (suffix.length > 1 && !isVowel(suffix[1]))) return null;
  } else {
    if (base.length > 1 && !isVowel(base[base.length - 2])) return null;
    if (!isVowel(suffix[0]) || (eNoun && ['i', 'in', 'ion'].includes(join(suffix)))) return null;
    if (suffix.length > 2 && !isVowel(suffix[1]) && !isVowel(suffix[2])) return null;
  }
  const [start, , long] = ns[ns.length - 1];
  if (long) return null;
  if (sSyl < 2) {
    const k = ns.length - 1, all = base.concat(suffix), nn = nuclei(all);
    if (heavy(all, nn, k - 1) || heavy(all, nn, k)) return null;
  }
  const out = base.slice(); out[start] = lengthen(out[start]);
  return out.concat(suffix);
}
function compoundVariants(first, second) {
  const out = [[first.concat(second), null, []]];
  const len = prosodicLengthening(first, second);
  if (len) out.push([len, null, ['lengthening']]);
  for (const [base, , rules] of out.slice()) {
    const red = reduceCompound(base);
    if (red) out.push([red[0], red[1], rules.concat(['reduction'])]);
    const sh = shortenFinalLong(base, first.length);
    if (sh) out.push([sh, null, rules.concat(['reduction'])]);
  }
  const seen = new Set();
  return out.filter(([w]) => { const k = join(w); if (seen.has(k)) return false; seen.add(k); return true; });
}
const SOFT_MUTATION = [['gw', 'w'], ['p', 'b'], ['t', 'd'], ['k', 'g'], ['b', 'v'], ['d', 'ð'], ['g', ''], ['m', 'v'],
  ['s', 'h'], ['h', 'x'], ['l̥', 'l'], ['r̥', 'r'], ['w̥', 'xw']];
function lenite(word) {
  const s = join(word);
  for (const [a, b] of SOFT_MUTATION) if (s.startsWith(a)) return phonemes(b + s.slice(a.length));
  return null;
}

// ---------------------------------------------------------------- backform
const BEAM = 60, MAX_OPTIONS = 4, MIN_SHARE = 0.03;
const positionName = (i, n) => i === 0 ? 'initial' : i === n - 1 ? 'final' : 'medial';
function bfOptions(table, sound, pos) {
  const c = table[keyOf([sound, pos])] || table[keyOf([sound, 'medial'])] || [[sound, 1]];
  const total = c.reduce((x, [, n]) => x + n, 0);
  const out = c.filter(([, n]) => n / total >= MIN_SHARE).map(([s, n]) => [s, n / total]);
  if (!out.some(([s]) => s === sound)) out.push([sound, 0.5 / total]);
  return out.slice(0, MAX_OPTIONS);
}
function bfCandidates(table, form) {
  const y = phonemes(comparable(form));
  let states = [['', 0]];
  y.forEach((sound, j) => {
    const nxt = [];
    for (const [prefix, lp] of states) for (const [seg, p] of bfOptions(table, sound, positionName(j, y.length))) nxt.push([prefix + seg, lp + Math.log(p)]);
    nxt.sort((a, b) => b[1] - a[1]);
    states = nxt.slice(0, BEAM);
  });
  const end = table[keyOf(['#', 'end'])] || [['', 1]];
  const total = end.reduce((x, [, n]) => x + n, 0);
  const out = [];
  for (const [prefix, lp] of states) for (const [seg, n] of end.slice(0, MAX_OPTIONS)) if (n / total >= MIN_SHARE) out.push([prefix + seg, lp + Math.log(n / total)]);
  out.sort((a, b) => b[1] - a[1]);
  const seen = new Set(), uniq = [];
  for (const [f, lp] of out) if (f && !seen.has(f)) { seen.add(f); uniq.push([f, lp]); }
  return uniq.slice(0, BEAM);
}
function backform(engine, form, era, lastStage, limit = 5) {
  const target = comparable(form);
  const rules = sequence(engine.rules, era, 0, lastStage);
  const found = [];
  for (const [cand, lp] of bfCandidates(engine.backform, form)) {
    const vs = run(cand, rules);
    const hit = vs.findIndex(v => comparable(v.form) === target);
    if (hit < 0) continue;
    found.push({ primitive: cand, logp: r3(lp), main: hit === 0, trace: vs[hit].trace });
    if (found.length >= limit) break;
  }
  found.sort((a, b) => (a.main === b.main ? 0 : a.main ? -1 : 1) || (b.logp - a.logp));
  return found;
}

// ---------------------------------------------------------------- compounds
const MAX_ORIGINS = 4, MAX_JOINS = 12, LENITION_WEIGHT = 0.2, MORPH_WEIGHT = 0.3, POLY_WEIGHT = 1.01;
function cleanOrigin(form) {
  let f = form.replace(/[-()’/]/g, '');
  f = chars(f).filter(ch => ch !== ACUTE).join('');
  return f.slice(0, 1).toUpperCase() === f.slice(0, 1) && f.slice(0, 1).toLowerCase() !== f.slice(0, 1) && f.toUpperCase() !== f ? f.toLowerCase() : f;
}
function origins(entry, era) {
  const proto = era === 'middle' ? 'mp' : 'p';
  let out = (entry.starts || []).concat((entry.stages || {})[proto] || []);
  if (!out.length) out = (entry.written_origins || []).filter(w => w.toUpperCase() !== w);
  const seen = new Set(), clean = [];
  for (const f of out) { const c = cleanOrigin(f); if (c && !seen.has(comparable(c))) { seen.add(comparable(c)); clean.push(c); } }
  return clean.slice(0, MAX_ORIGINS);
}
function formsAt(engine, entry, era, stage, final = false) {
  const langs = engine.languages.filter(l => l.era === era);
  const lang = langs.find(l => l.stage === stage);
  const code = lang ? lang.code : null;
  const attested = code && stage > 0 ? ((entry.stages || {})[code] || []) : [];
  let out = attested.map(f => [f, 'attested']);
  if (out.length) return out;
  if (code && entry.lang === code) {
    out = final ? [] : (entry.stems || []).map(x => [toPhonetic(x, engine.branch).replace(/-+$/, ''), 'stem']);
    out.push([toPhonetic(entry.form, engine.branch).replace(/-+$/, ''), 'dictionary']);
    const seen = new Set();
    return out.filter(([f]) => f && !seen.has(comparable(f)) && seen.add(comparable(f)));
  }
  let baseForms = origins(entry, era).map(f => [f, 'primitive']);
  const finalLang = langs.reduce((a, b) => (b.stage > a.stage ? b : a));
  if (!baseForms.length && entry.lang === finalLang.code) {
    const word = toPhonetic(entry.form, engine.branch).replace(/-+$/, '');
    baseForms = backform(engine, word, era, finalLang.stage, 3).map(f => [f.primitive, 'reconstructed']);
  }
  if (stage === 0) return baseForms;
  const rules = sequence(engine.rules, era, 0, stage);
  for (const [f, how] of baseForms) for (const v of run(f, rules).slice(0, 2)) out.push([v.form, how === 'primitive' ? 'computed' : 'reconstructed']);
  return out;
}
function junctionsOf(a, b) {
  const out = [[a + '+' + b, 'full']];
  const pa = phonemes(a);
  if (pa.length > 1 && isVowel(pa[pa.length - 1])) out.push([join(pa.slice(0, -1)) + '+' + b, 'elided']);
  return out;
}
function predictLatest(engine, ids, era) {
  const last = Math.max(...engine.languages.filter(l => l.era === era).map(l => l.stage));
  if (ids.length !== 2) return [];
  const e1 = engine.lexicon.get(ids[0]), e2 = engine.lexicon.get(ids[1]);
  const firsts = e1 ? formsAt(engine, e1, era, last) : [];
  const seconds = e2 ? formsAt(engine, e2, era, last, true) : [];
  if (engine.branch === 'sindarin') {
    for (const [b] of seconds.slice()) { const m = lenite(phonemes(comparable(b))); if (m) seconds.push([join(m), 'soft-mutation']); }
  }
  const poly = sequence(engine.rules, era, last, last).filter(c => /polysyllab/i.test(c.name));
  const scored = new Map();
  const add = (form, score, info) => { const k = comparable(form); if (!scored.has(k) || scored.get(k)[0] < score) scored.set(k, [score, form, info]); };
  for (const [a, ha] of firsts) for (const [b, hb] of seconds) {
    const pa = phonemes(comparable(a)), pb = phonemes(comparable(b));
    let weight = ha === 'dictionary' && firsts.some(([, h]) => h === 'stem') ? 0.5 : 1;
    if (hb === 'soft-mutation') weight *= LENITION_WEIGHT;
    for (const [form, p0, jop, eop, short] of junctionPredict(engine.junctions, pa, pb, 10)) {
      const p = p0 * weight;
      const info = { joined: a + '+' + b, elements: [a, b], sources: [ha, hb], junction: jop, ending: eop, shortened: short, adjustments: [], trace: [] };
      add(form, p, info);
      if (poly.length) for (const v of run(form, poly).slice(0, 3)) if (v.trace.length) add(v.form, p * POLY_WEIGHT, Object.assign({}, info, { trace: v.trace }));
    }
    if (engine.branch === 'quenya') {
      for (const [w, stem, rules] of compoundVariants(pa, pb).slice(1)) {
        add(join(w), MORPH_WEIGHT * Math.pow(0.5, rules.length - 1) * 0.5, { joined: a + '+' + b, elements: [a, b], sources: [ha, hb],
          junction: [0, 0, ''], ending: [0, ''], shortened: false, adjustments: rules, stem: stem ? join(stem) : null, trace: [] });
      }
    }
  }
  return [...scored.values()].sort((x, y) => y[0] - x[0]).map(([sc, f, info]) => Object.assign({ form: f, score: r3(sc) }, info));
}
function predict(engine, ids, era, stage, lastStage = null) {
  const last = lastStage != null ? lastStage : Math.max(...engine.languages.filter(l => l.era === era).map(l => l.stage));
  if (lastStage == null && stage >= last) return predictLatest(engine, ids, era);
  const parts = [];
  for (let k = 0; k < ids.length; k++) {
    const e = engine.lexicon.get(ids[k]);
    const fs = e ? formsAt(engine, e, era, stage, k === ids.length - 1) : [];
    if (!fs.length) return [];
    parts.push(fs);
  }
  const rules = sequence(engine.rules, era, stage + 1, last);
  const joins = [];
  for (const combo of product(parts)) {
    let acc = [[combo[0][0], 'full']];
    for (const [form] of combo.slice(1)) {
      const nxt = [];
      for (const [x, lab] of acc) for (const [j, l2] of junctionsOf(x, form)) nxt.push([j, lab === 'elided' || l2 === 'elided' ? 'elided' : 'full']);
      acc = nxt;
    }
    for (const [j, label] of acc) joins.push([j, label, combo.map(c => c[0]), combo.map(c => c[1])]);
  }
  const ordered = joins.filter(j => j[1] === 'full').concat(joins.filter(j => j[1] !== 'full'));
  const variants = [], seen = new Set();
  for (const [j, label, forms, how] of ordered.slice(0, MAX_JOINS)) {
    for (const v of run(j, rules)) {
      const k = comparable(v.form);
      if (seen.has(k)) continue;
      seen.add(k);
      variants.push({ form: v.form.split('+').join(''), joined: j, junctionLabel: label, elements: forms, sources: how, trace: v.trace });
    }
  }
  return variants;
}

// ---------------------------------------------------------------- engine
function makeEngine(branch, wf) {
  return {
    branch,
    languages: wf.languages,
    rules: compileSequence(wf.rules),
    ruleNames: new Map(wf.rules.map(r => [r.id, r.name])),
    lexicon: new Map(wf.lexicon.map(e => [e.id, e])),
    lexiconList: wf.lexicon,
    junctions: wf.junctions,
    backform: wf.backform,
    analogues: wf.analogues,
  };
}

// ---------------------------------------------------------------- parity with the Python build
function parity(engine, V) {
  const bad = [];
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const check = (kind, input, want, got) => { if (!same(want, got)) bad.push({ kind, input, want, got }); };
  for (const [f, t, before, want] of V.apply) {
    let got;
    try { got = applyRule(compileRule(f, t), before).ordered; } catch (e) { if (!(e instanceof Unsupported)) throw e; got = null; }
    check('apply', [f, t, before], want, got);
  }
  for (const [f, want] of V.comparable) check('comparable', f, want, comparable(f));
  for (const [f, mode, want] of V.stress) check('stress', [f, mode], want, [...stressed(phonemes(f.replace(/^-+|-+$/g, '')), mode)].sort((a, b) => a - b));
  for (const [start, era, first, last, forms, trace] of V.run) {
    const vs = run(start, sequence(engine.rules, era, first, last));
    check('run', [start, era, first, last], [forms, trace], [vs.map(v => v.form), vs[0].trace.map(t => [t[0], t[2]])]);
  }
  for (const [w, want] of V.phonetic) check('phonetic', w, want, toPhonetic(w, engine.branch));
  for (const [a, b, want] of V.junction) check('junction', [a, b], want, junctionPredict(engine.junctions, phonemes(a), phonemes(b), 10));
  for (const [ids, want] of V.latest) check('latest', ids, want, predict(engine, ids, 'late', 9).slice(0, 10).map(v => [v.form, v.score]));
  for (const [ids, era, stage, last, want] of V.early) check('early', ids, want, predict(engine, ids, era, stage, last).slice(0, 10).map(v => v.form));
  for (const [form, last, want] of V.backform) check('backform', form, want, backform(engine, form, 'late', last).map(r => r.primitive));
  return bad;
}

window.WF = {
  parity,
  Unsupported, phonemes, canonical, comparable, compileRule, applyRule, stressed, nuclei, run, sequence,
  toPhonetic, junctionPredict, reduceCompound, prosodicLengthening, compoundVariants, lenite, backform,
  formsAt, predict, makeEngine,
};
})();
