# Аудит сборки

Источник: Eldamo 0.8.13 (`eldamo-data.xml`, sha256 `4e561d4dfc15919d…`). Файл создаётся `scripts/build.py`; не править вручную.

Каждый засвидетельствованный шаг деривации Eldamo (`<rule-example>`) проигрывается интерпретатором `shared/interpreter.py`: формула шага применяется к предыдущей форме и результат сравнивается со следующей. Расхождение не обязательно ошибка интерпретатора: в данных Eldamo встречаются шаги, где в одной записи совмещено несколько изменений, повторы формы без изменения и позиционные правила внутри сложных слов.

## Quenya / Qenya

| показатель | значение |
|---|---|
| правил (страниц `phonetic-rule`) | 251 |
| из них с порядком Eldamo (`order`) | 211 |
| исключено как удалённые Толкином | 1 |
| подформул `<rule>` | 782 (contextual: 163, identity: 11, literal: 603, loss: 5) |
| подформул с засвидетельствованными примерами | 464 |
| дериваций (из них отвергнутых Толкином) | 2556 (194) |
| шагов дериваций в языках ветви | 4485 |
| доля воспроизведённых среди шагов с известной формулой | 94.3% |
| рёбер графа (условных; с примерами) | 606 (112; 340) |
| контекстных подформул вне графа | 174 |
| цепочек | 344 (A: 83, B: 63, C: 2, D: 196) |
| путей, отброшенных как противоречащие хронологии Eldamo | 64 |

### Проверка шагов

| результат | шагов |
|---|---|
| правило удалено Толкином (`deleted_rule`) | 11 |
| исключение правила: звук сохраняется (`identity`) | 2 |
| формула применима, но даёт другую форму (`mismatch`) | 80 |
| формула не находит, к чему примениться (`no_match`) | 145 |
| формула воспроизводит шаг (`reproduced`) | 4106 |
| воспроизводит при применении в одной позиции (`reproduced_partial`) | 23 |
| правило в Eldamo не указано («?») (`unknown_rule`) | 87 |
| формулы шага нет среди правил (`unmatched_formula`) | 5 |
| нотация вне документированной (`unsupported`) | 26 |

### Правила с наибольшим числом невоспроизведённых шагов

| правило | mismatch | no_match | unsupported |
|---|---|---|---|
| [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-3978101829.html) | 0 | 26 | 0 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | 0 | 0 | 15 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2821506177.html) | 8 | 7 | 0 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2630259491.html) | 0 | 0 | 11 |
| [second short vowel of same quality lost](https://eldamo.org/content/words/word-3116715705.html) | 7 | 3 | 0 |
| [medial [ɣ]/[h] vanished except before [t]](https://eldamo.org/content/words/word-2690267141.html) | 3 | 5 | 0 |
| [voiced stops became spirants except after nasals and liquids](https://eldamo.org/content/words/word-2772726195.html) | 2 | 6 | 0 |
| [initial [s] plus voiceless stops became voiceless spirants](https://eldamo.org/content/words/word-3333849997.html) | 0 | 8 | 0 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-1072764601.html) | 2 | 5 | 0 |
| [aspirates became voiceless spirants](https://eldamo.org/content/words/word-3262991621.html) | 1 | 6 | 0 |
| [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-1833409085.html) | 5 | 1 | 0 |
| [unstressed medial long vowels shortened](https://eldamo.org/content/words/word-3034061375.html) | 3 | 3 | 0 |
| [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-1324632797.html) | 0 | 6 | 0 |
| [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-720793221.html) | 1 | 4 | 0 |
| [voiced stops became spirants except after nasals](https://eldamo.org/content/words/word-1141570065.html) | 1 | 4 | 0 |

### Исключённые правила

- p: [ɣ] became [h] before voiceless consonants — deleted by Tolkien (mark "-")

### Формулы шагов, которых нет среди правил

- `aq: -Sā > -Să`
- `maq: -CC > -C`
- `maq: rx > rk`
- `maq: ɸ > f`
- `mp: None > !`
- `q: None > ???`
- `s: None > !`

Полный список невоспроизведённых шагов (251) — `reports/audit.json`.

## Sindarin / Noldorin

| показатель | значение |
|---|---|
| правил (страниц `phonetic-rule`) | 303 |
| из них с порядком Eldamo (`order`) | 263 |
| исключено как удалённые Толкином | 3 |
| подформул `<rule>` | 868 (contextual: 268, identity: 17, literal: 574, loss: 9) |
| подформул с засвидетельствованными примерами | 664 |
| дериваций (из них отвергнутых Толкином) | 2847 (186) |
| шагов дериваций в языках ветви | 8379 |
| доля воспроизведённых среди шагов с известной формулой | 94.7% |
| рёбер графа (условных; с примерами) | 575 (98; 419) |
| контекстных подформул вне графа | 293 |
| цепочек | 332 (A: 123, B: 81, C: 1, D: 127) |
| путей, отброшенных как противоречащие хронологии Eldamo | 101 |

### Проверка шагов

| результат | шагов |
|---|---|
| правило удалено Толкином (`deleted_rule`) | 11 |
| исключение правила: звук сохраняется (`identity`) | 114 |
| формула применима, но даёт другую форму (`mismatch`) | 134 |
| формула не находит, к чему примениться (`no_match`) | 202 |
| формула воспроизводит шаг (`reproduced`) | 7696 |
| воспроизводит при применении в одной позиции (`reproduced_partial`) | 18 |
| правило в Eldamo не указано («?») (`unknown_rule`) | 98 |
| формулы шага нет среди правил (`unmatched_formula`) | 10 |
| нотация вне документированной (`unsupported`) | 96 |

### Правила с наибольшим числом невоспроизведённых шагов

| правило | mismatch | no_match | unsupported |
|---|---|---|---|
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html) | 0 | 0 | 40 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html) | 2 | 22 | 0 |
| [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html) | 3 | 20 | 0 |
| [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html) | 7 | 12 | 0 |
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-3230272819.html) | 0 | 0 | 18 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | 0 | 0 | 15 |
| [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-2399289739.html) | 1 | 13 | 0 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2630259491.html) | 0 | 0 | 11 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html) | 6 | 5 | 0 |
| [medial [j] became [i]](https://eldamo.org/content/words/word-1679623085.html) | 6 | 5 | 0 |
| [short vowels generally lengthened in monosyllables](https://eldamo.org/content/words/word-1053424933.html) | 0 | 11 | 0 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-3958031275.html) | 1 | 9 | 0 |
| [medial [ɣ]/[h] vanished except before [t]](https://eldamo.org/content/words/word-2690267141.html) | 3 | 5 | 0 |
| [unstressed initial syllables reduced to favored clusters](https://eldamo.org/content/words/word-341640763.html) | 4 | 3 | 1 |
| [[n] assimilated to following labial](https://eldamo.org/content/words/word-1126284559.html) | 0 | 0 | 8 |

### Исключённые правила

- p: [ɣ] became [h] before voiceless consonants — deleted by Tolkien (mark "-")
- on: [ei], [ou] became [oi], [ū] — deleted by Tolkien (mark "-")
- on: initial [s] unvoiced following [l], [r] — deleted by Tolkien (mark "-")

### Формулы шагов, которых нет среди правил

- `maq: -CC > -C`
- `mp: None > !`
- `n: None > !`
- `os: -j- > -i-`
- `os: None > !`
- `os: ŋ- > ŋg-`
- `s: -Sā > -Să`
- `s: None > !`

Полный список невоспроизведённых шагов (432) — `reports/audit.json`.
