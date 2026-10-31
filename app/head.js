// In <head> of the atlas and the corpus (template.html, corpus_template.html), before anything is
// drawn: the theme and the language chosen last time (i18n.js, runtime.js), so that the page does
// not show first in the light theme and in Russian; until its static text is translated, the page
// stays hidden (I18N.ready)
(function () {
  var root = document.documentElement;
  try { var t = localStorage.getItem('quettamin-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) { /* no storage */ }
  var lang = null;
  try { var raw = location.hash.slice(1); try { raw = decodeURIComponent(raw); } catch (e) { /* as is */ }
    var m = /(?:^|&)lang=(ru|en)(?:&|$)/.exec(raw); lang = m ? m[1] : localStorage.getItem('quettamin-lang'); } catch (e) { /* no storage */ }
  if (lang !== 'ru' && lang !== 'en') {
    var nav = (navigator.languages && navigator.languages[0]) || navigator.language || 'ru';
    lang = /^(ru|uk|be|kk)\b/i.test(nav) ? 'ru' : 'en';
  }
  root.lang = lang;
  if (lang !== 'ru') root.classList.add('i18n-wait');
  // the theme chosen in another tab of Quettamin (the atlas, the corpus, the graph) follows here
  window.addEventListener('storage', function (e) {
    if (e.key === 'quettamin-theme' && e.newValue) root.setAttribute('data-theme', e.newValue);
  });
})();
