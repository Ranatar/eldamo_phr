# Аудит сборки

Источник: Eldamo 0.8.13 (`eldamo-data.xml`, sha256 `4e561d4dfc15919d…`). Файл создаётся `scripts/build.py`; не править вручную.

Каждый засвидетельствованный шаг деривации Eldamo (`<rule-example>`) проигрывается интерпретатором `shared/interpreter.py`: формула шага применяется к предыдущей форме и результат сравнивается со следующей. Расхождение не обязательно ошибка интерпретатора: в данных Eldamo встречаются шаги, где в одной записи совмещено несколько изменений, повторы формы без изменения и позиционные правила внутри сложных слов.

## Quenya / Qenya

| показатель | значение |
|---|---|
| правил (страниц `phonetic-rule`) | 387 |
| из них с порядком Eldamo (`order`) | 261 |
| исключено как удалённые Толкином | 2 |
| подформул `<rule>` | 1186 (contextual: 241, identity: 12, literal: 925, loss: 8) |
| подформул с засвидетельствованными примерами | 723 |
| дериваций (из них отвергнутых Толкином) | 4183 (226) |
| шагов дериваций в языках ветви | 7532 |
| доля воспроизведённых среди шагов с известной формулой | 94.0% |
| рёбер графа (условных; с примерами) | 931 (226; 550) |
| контекстных подформул вне графа | 253 |
| цепочек | 511 (A: 109, B: 68, C: 51, D: 283) |
| путей, отброшенных как противоречащие хронологии Eldamo | 84 |

### Проверка шагов

| результат | шагов |
|---|---|
| правило удалено Толкином (`deleted_rule`) | 11 |
| исключение правила: звук сохраняется (`identity`) | 28 |
| формула применима, но даёт другую форму (`mismatch`) | 110 |
| формула не находит, к чему примениться (`no_match`) | 284 |
| формула воспроизводит шаг (`reproduced`) | 6903 |
| воспроизводит при применении в одной позиции (`reproduced_partial`) | 24 |
| правило в Eldamo не указано («?») (`unknown_rule`) | 115 |
| формулы шага нет среди правил (`unmatched_formula`) | 8 |
| нотация вне документированной (`unsupported`) | 49 |

### Правила с наибольшим числом невоспроизведённых шагов

| правило | mismatch | no_match | unsupported |
|---|---|---|---|
| [long final vowels were shortened](https://eldamo.org/content/words/word-504909023.html) | 4 | 87 | 0 |
| [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-3978101829.html) | 0 | 26 | 0 |
| [short syllabic [ṇ] became [a] + homorganic nasal, [i] before palatals or [u] before labials](https://eldamo.org/content/words/word-2670096403.html) | 3 | 1 | 16 |
| [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-4062489737.html) | 1 | 16 | 0 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | 0 | 0 | 15 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2821506177.html) | 8 | 7 | 0 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2630259491.html) | 0 | 0 | 11 |
| [second short vowel of same quality lost](https://eldamo.org/content/words/word-3116715705.html) | 7 | 3 | 0 |
| [medial [ɣ]/[h] vanished except before [t]](https://eldamo.org/content/words/word-2690267141.html) | 3 | 5 | 0 |
| [final [ǝ] vanished](https://eldamo.org/content/words/word-1398002213.html) | 0 | 8 | 0 |
| [voiced stops became spirants except after nasals and liquids](https://eldamo.org/content/words/word-2772726195.html) | 2 | 6 | 0 |
| [initial [s] plus voiceless stops became voiceless spirants](https://eldamo.org/content/words/word-3333849997.html) | 0 | 8 | 0 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-1072764601.html) | 2 | 5 | 0 |
| [aspirates became voiceless spirants](https://eldamo.org/content/words/word-3262991621.html) | 1 | 6 | 0 |
| [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-1833409085.html) | 5 | 1 | 0 |

### Исключённые правила

- p: [ɣ] became [h] before voiceless consonants — deleted by Tolkien (mark "-")
- eq: intervocalic [ĭ] became [j] — deleted by Tolkien (mark "-")

### Формулы шагов, которых нет среди правил

- `aq: -Sā > -Să`
- `eq: -st > -t`
- `eq: -ĭ > -e`
- `eq: VVst > VVs`
- `maq: -CC > -C`
- `maq: rx > rk`
- `maq: ɸ > f`
- `mp: None > !`
- `q: None > ???`
- `s: None > !`

Полный список невоспроизведённых шагов (443) — `reports/audit.json`.

## Sindarin / Noldorin

| показатель | значение |
|---|---|
| правил (страниц `phonetic-rule`) | 384 |
| из них с порядком Eldamo (`order`) | 338 |
| исключено как удалённые Толкином | 4 |
| подформул `<rule>` | 1098 (contextual: 321, identity: 20, literal: 747, loss: 10) |
| подформул с засвидетельствованными примерами | 853 |
| дериваций (из них отвергнутых Толкином) | 3382 (207) |
| шагов дериваций в языках ветви | 9407 |
| доля воспроизведённых среди шагов с известной формулой | 94.4% |
| рёбер графа (условных; с примерами) | 749 (148; 559) |
| контекстных подформул вне графа | 349 |
| цепочек | 368 (A: 132, B: 98, C: 1, D: 137) |
| путей, отброшенных как противоречащие хронологии Eldamo | 127 |

### Проверка шагов

| результат | шагов |
|---|---|
| правило удалено Толкином (`deleted_rule`) | 11 |
| исключение правила: звук сохраняется (`identity`) | 121 |
| формула применима, но даёт другую форму (`mismatch`) | 151 |
| формула не находит, к чему примениться (`no_match`) | 262 |
| формула воспроизводит шаг (`reproduced`) | 8597 |
| воспроизводит при применении в одной позиции (`reproduced_partial`) | 24 |
| правило в Eldamo не указано («?») (`unknown_rule`) | 110 |
| формулы шага нет среди правил (`unmatched_formula`) | 32 |
| нотация вне документированной (`unsupported`) | 99 |

### Правила с наибольшим числом невоспроизведённых шагов

| правило | mismatch | no_match | unsupported |
|---|---|---|---|
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html) | 0 | 0 | 40 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html) | 2 | 22 | 0 |
| [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html) | 3 | 20 | 0 |
| [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html) | 7 | 12 | 0 |
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-3230272819.html) | 0 | 0 | 18 |
| [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-4062489737.html) | 1 | 16 | 0 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | 0 | 0 | 15 |
| [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-2399289739.html) | 1 | 13 | 0 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html) | 6 | 6 | 0 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2630259491.html) | 0 | 0 | 11 |
| [medial [j] became [i]](https://eldamo.org/content/words/word-1679623085.html) | 6 | 5 | 0 |
| [short vowels generally lengthened in monosyllables](https://eldamo.org/content/words/word-1053424933.html) | 0 | 11 | 0 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-3958031275.html) | 1 | 9 | 0 |
| [[ŋ] became [ŋg]](https://eldamo.org/content/words/word-2869972293.html) | 0 | 10 | 0 |
| [medial [ɣ]/[h] vanished except before [t]](https://eldamo.org/content/words/word-2690267141.html) | 3 | 5 | 0 |

### Исключённые правила

- p: [ɣ] became [h] before voiceless consonants — deleted by Tolkien (mark "-")
- g: [ǣ] became [ē] — deleted by Tolkien (mark "-")
- on: [ei], [ou] became [oi], [ū] — deleted by Tolkien (mark "-")
- on: initial [s] unvoiced following [l], [r] — deleted by Tolkien (mark "-")

### Формулы шагов, которых нет среди правил

- `g: None > !`
- `g: nj > n`
- `maq: -CC > -C`
- `mp: None > !`
- `n: None > !`
- `os: -j- > -i-`
- `os: None > !`
- `os: ŋ- > ŋg-`
- `s: -Sā > -Să`
- `s: None > !`

Полный список невоспроизведённых шагов (512) — `reports/audit.json`.
