# Проверка секвенсора

Источник: Eldamo 0.8.13. Файл создаётся `scripts/build.py`; не править вручную.

Секвенсор (`shared/sequencer.py`) прогоняет начальную форму деривации через все правила ветви в хронологическом порядке — так, как будет порождаться форма нового слова, — и сравнивает результат с конечной формой деривации Eldamo. В отличие от `audit.md`, где каждый шаг проверяется отдельно, здесь правила не подсказываются: секвенсор сам решает, какие из них применимы. Прогон останавливается на правиле последнего засвидетельствованного шага (деривация может кончаться промежуточной формой).

«Основное» — первое чтение (необязательные правила применены, из альтернатив выбрана первая подформула); «любое» — конечная форма среди всех вариантов (необязательные правила, альтернативные исходы, правила на границе морфем `+` в формах без отмеченной границы).

## Quenya / Qenya

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1212 | 927 (76.5%) | 953 (78.6%) |
| средняя | 907 | 755 (83.2%) | 765 (84.3%) |
| всего | 2119 | 1682 (79.4%) | 1718 (81.1%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [second short vowel of same quality lost](https://eldamo.org/content/words/word-3116715705.html) | aq | 17 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | p | 14 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2821506177.html) | q | 14 |
| [medial [s] often became [z]](https://eldamo.org/content/words/word-127393503.html) | aq | 11 |
| [aspirates became voiceless spirants](https://eldamo.org/content/words/word-3262991621.html) | aq | 11 |
| [voiced stops became spirants except after nasals](https://eldamo.org/content/words/word-1141570065.html) | aq | 10 |
| [[nm], [ŋm] became [nw], [ŋgw]](https://eldamo.org/content/words/word-1197128543.html) | q | 10 |
| [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-1833409085.html) | q | 9 |
| [[pt], [kt] became [ps], [xt]](https://eldamo.org/content/words/word-2701010297.html) | mq | 9 |
| [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-14484545.html) | q | 9 |
| [initial nasals plus stops reduced to nasals](https://eldamo.org/content/words/word-2830500177.html) | maq | 8 |
| [[θ] became [s]](https://eldamo.org/content/words/word-3491983963.html) | q | 8 |
| [[w] became [β] initially and between vowels](https://eldamo.org/content/words/word-3625908403.html) | q | 8 |
| [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-720793221.html) | maq | 7 |
| [voiced stops unvoiced before voiceless consonants](https://eldamo.org/content/words/word-1944249607.html) | p | 7 |

### Условие «elsewhere»

Общая подформула не применяется там, где более позднее правило того же языка задаёт тот же вход для определённой позиции:

- aq: stops frequently underwent metathesis with nasals and liquids ← initial [dr-], [dl-] became [r-], [l-]
- aq: [sr] became [ss] ← initial [s] unvoiced following continuant
- q: [pt], [kt] became [ɸt], [xt] ← final consonant clusters reduced
- maq: stops frequently underwent metathesis with nasals and liquids ← initial [dr-], [dl-] became [r-], [l-]
- maq: [sr] became [ss] ← initial [s] unvoiced following continuant

### Сложения с праформами

Сложения Eldamo из двух элементов, у которых есть деривация от праформы и праформы обоих элементов. Праформы элементов соединяются через `+` (полный первый элемент или без конечного гласного), затем соединение проходит все правила ветви (`shared/compound.py`).

| показатель | случаев |
|---|---|
| случаев (сложение × деривация) | 61 |
| соединение праформ совпало с начальной формой деривации | 17 (28%) |
| основное чтение = засвидетельствованная форма | 7 (11%) |
| форма среди вариантов | 23 (38%) |

### Сложения на последней стадии

Сложения квенья из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/quenya/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс правила §6.1 учебника (`shared/morphophonology.py`).

| показатель | случаев |
|---|---|
| сложений | 384 |
| первый вариант = засвидетельствованная форма | 152 (40%) |
| форма среди первых 8 вариантов | 245 (64%) |

### Суффиксы и приставки

Производные слова Eldamo из основы и одного аффикса (часть речи `suf` или `pref`). Модель (`shared/affixes.py`, `branches/quenya/data/affixes.json`) строится без проверяемого слова: какая форма аффикса берётся после гласного и после согласного, что происходит на стыке и в конце — сначала по словам с этим же аффиксом, иначе по всем словам с аффиксом того же вида.

| | слов | первый вариант = форма Eldamo | среди первых 8 |
|---|---|---|---|
| суффиксы | 314 | 203 (65%) | 244 (78%) |
| приставки | 108 | 56 (52%) | 70 (65%) |
| всего | 422 | 259 (61%) | 314 (74%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 100) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 100 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 93 (93%) |
| первая из них = праформа Eldamo | 10 (10%) |
| праформа Eldamo среди найденных (до 8) | 25 (25%) |

Расходящиеся деривации (437) — `reports/sequencer.json`.

## Sindarin / Noldorin

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1027 | 723 (70.4%) | 765 (74.5%) |
| средняя | 1356 | 883 (65.1%) | 938 (69.2%) |
| всего | 2383 | 1606 (67.4%) | 1703 (71.5%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [long final vowels were shortened](https://eldamo.org/content/words/word-1410098833.html) | on | 69 |
| [[ai] became [oe] or [ae]](https://eldamo.org/content/words/word-3173115217.html) | n | 43 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html) | n | 21 |
| [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2240258959.html) | s | 19 |
| [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2951504533.html) | n | 18 |
| [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html) | n | 18 |
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html) | s | 17 |
| [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html) | s | 15 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html) | os | 15 |
| [final [i], [u] generally vanished](https://eldamo.org/content/words/word-1815401039.html) | s | 14 |
| [non-initial [m] usually became [v]](https://eldamo.org/content/words/word-3030431535.html) | n | 13 |
| [[mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-1317326183.html) | n | 12 |
| [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-2399289739.html) | s | 11 |
| [aspirates became voiceless spirants](https://eldamo.org/content/words/word-883570327.html) | os | 11 |
| [initial [x-] became [h-]](https://eldamo.org/content/words/word-1195324115.html) | n | 11 |

### Условие «elsewhere»

Общая подформула не применяется там, где более позднее правило того же языка задаёт тот же вход для определённой позиции:

- s: short [u] often became [o] ← final [i], [u] generally vanished
- n: short [u] often became [o] ← final [i], [u] generally vanished
- n: short [a], [o], [u] became [e], [œ], [y] preceding [i] ← final [i] intruded into preceding syllable

Подформул вне документированной нотации, пропускаемых секвенсором: 1 (в 1 правилах).

### Сложения с праформами

Сложения Eldamo из двух элементов, у которых есть деривация от праформы и праформы обоих элементов. Праформы элементов соединяются через `+` (полный первый элемент или без конечного гласного), затем соединение проходит все правила ветви (`shared/compound.py`).

| показатель | случаев |
|---|---|
| случаев (сложение × деривация) | 66 |
| соединение праформ совпало с начальной формой деривации | 14 (21%) |
| основное чтение = засвидетельствованная форма | 11 (17%) |
| форма среди вариантов | 17 (26%) |

### Сложения на последней стадии

Сложения синдарина из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/sindarin/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс мягкая мутация второго элемента и правила синдарина для многосложных слов.

| показатель | случаев |
|---|---|
| сложений | 365 |
| первый вариант = засвидетельствованная форма | 126 (35%) |
| форма среди первых 8 вариантов | 214 (59%) |

### Суффиксы и приставки

Производные слова Eldamo из основы и одного аффикса (часть речи `suf` или `pref`). Модель (`shared/affixes.py`, `branches/sindarin/data/affixes.json`) строится без проверяемого слова: какая форма аффикса берётся после гласного и после согласного, что происходит на стыке и в конце — сначала по словам с этим же аффиксом, иначе по всем словам с аффиксом того же вида.

| | слов | первый вариант = форма Eldamo | среди первых 8 |
|---|---|---|---|
| суффиксы | 141 | 71 (50%) | 81 (57%) |
| приставки | 41 | 17 (41%) | 28 (68%) |
| всего | 182 | 88 (48%) | 109 (60%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 64) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 64 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 34 (53%) |
| первая из них = праформа Eldamo | 2 (3%) |
| праформа Eldamo среди найденных (до 8) | 8 (12%) |

Расходящиеся деривации (777) — `reports/sequencer.json`.
