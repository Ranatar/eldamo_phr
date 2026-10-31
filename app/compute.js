// Reconstructions in a background thread (a Web Worker), so that the page answers while a long
// word's panorama is being computed (docs/how-it-works.md, §7). The worker runs the same engine
// (wordform.js, its text taken from the page) on the same data (the wordform-data block); its
// caches live as long as it does. Jobs go one at a time, in order; a group of jobs (the cells of
// one panorama, a reconstruction of the tab) can be cancelled: what waits is dropped, and a job of
// the group being computed stops the worker (a new one starts with the next job). Where a worker
// cannot be made (an old browser, a page that forbids it), the jobs run here, one per tick, as before.
(function () {
'use strict';
const WF = window.WF;

// the worker: wordform.js, then this
const WORKER = `
let engines = null;
self.onmessage = e => {
  const m = e.data;
  if (m.type === 'init') {
    const data = JSON.parse(m.data);
    engines = {};
    for (const b of Object.keys(data)) engines[b] = self.WF.makeEngine(b, data[b]);
    return;
  }
  try { self.postMessage({ id: m.id, result: self.WF.reconstruct(engines, m.src, m.dst, m.opts) }); }
  catch (err) { self.postMessage({ id: m.id, error: String((err && err.message) || err) }); }
};
`;

const CANCELLED = { cancelled: true };
let worker = null, broken = false, running = null, seq = 0;
const queue = [];
let local = null;          // (src, dst, opts) -> variants, on this thread (word_ui.js sets it)

function start() {
  if (worker || broken) return worker;
  try {
    const code = document.getElementById('wordform-js').textContent + '\n' + WORKER;
    worker = new Worker(URL.createObjectURL(new Blob([code], { type: 'text/javascript' })));
    worker.onmessage = done;
    worker.onerror = ev => { if (ev.preventDefault) ev.preventDefault(); fallBack(); };
    worker.postMessage({ type: 'init', data: document.getElementById('wordform-data').textContent });
  } catch (_e) {
    worker = null;
    broken = true;
  }
  return worker;
}

// the worker failed: what it had and what waits goes on here
function fallBack() {
  if (worker) { try { worker.terminate(); } catch (_e) { /* gone */ } }
  worker = null;
  broken = true;
  if (running) { queue.unshift(running); running = null; }
  pump();
}

function pump() {
  if (running || !queue.length) return;
  const job = running = queue.shift();
  if (start()) {
    worker.postMessage({ id: job.id, src: job.src, dst: job.dst, opts: job.opts });
    return;
  }
  setTimeout(() => {
    if (running !== job) return;
    try { job.resolve(local(job.src, job.dst, job.opts)); } catch (err) { job.reject(err); }
    running = null;
    pump();
  }, 0);
}

function done(e) {
  const m = e.data;
  if (!running || m.id !== running.id) return;
  const job = running;
  running = null;
  if (m.error != null) job.reject(new Error(m.error));
  else job.resolve(m.result);
  pump();
}

// variants of the form at dst (WF.reconstruct), computed in the background
function reconstruct(src, dst, opts, group) {
  return new Promise((resolve, reject) => {
    queue.push({ id: ++seq, src, dst, opts, group, resolve, reject });
    pump();
  });
}

// the jobs of a group not done yet are dropped (their promises reject with WQ.CANCELLED)
function cancel(group) {
  for (let i = queue.length - 1; i >= 0; i--) {
    if (queue[i].group === group) { queue[i].reject(CANCELLED); queue.splice(i, 1); }
  }
  if (running && running.group === group) {
    // a worker is stopped; a job of this thread not begun yet is just not begun
    if (worker) { worker.terminate(); worker = null; }
    running.reject(CANCELLED);
    running = null;
    pump();
  }
}

window.WQ = {
  reconstruct, cancel, CANCELLED,
  setLocal: fn => { local = fn; },
  // for the tests: whether the jobs run in a worker
  get inWorker() { return !!worker; },
};
})();
