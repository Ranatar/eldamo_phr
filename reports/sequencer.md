# Проверка секвенсора

Источник: Eldamo 0.8.13. Файл создаётся `scripts/build.py`; не править вручную.

Секвенсор (`shared/sequencer.py`) прогоняет начальную форму деривации через все правила ветви в хронологическом порядке — так, как будет порождаться форма нового слова, — и сравнивает результат с конечной формой деривации Eldamo. В отличие от `audit.md`, где каждый шаг проверяется отдельно, здесь правила не подсказываются: секвенсор сам решает, какие из них применимы. Прогон останавливается на правиле последнего засвидетельствованного шага (деривация может кончаться промежуточной формой).

«Основное» — первое чтение (необязательные правила применены, из альтернатив выбрана первая подформула); «любое» — конечная форма среди всех вариантов (необязательные правила, альтернативные исходы, правила на границе морфем `+` в формах без отмеченной границы).

## Quenya / Qenya

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1212 | 908 (74.9%) | 953 (78.6%) |
| средняя | 907 | 730 (80.5%) | 765 (84.3%) |
| всего | 2119 | 1638 (77.3%) | 1718 (81.1%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [long final vowels were shortened](https://eldamo.org/content/words/word-2821506177.html) | q | 18 |
| [second short vowel of same quality lost](https://eldamo.org/content/words/word-3116715705.html) | aq | 17 |
| [[ɸ], [β] became [f], [v]](https://eldamo.org/content/words/word-14484545.html) | q | 15 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | p | 14 |
| [[r], [l] often became syllabic in clusters](https://eldamo.org/content/words/word-720793221.html) | maq | 11 |
| [initial nasals plus stops reduced to nasals](https://eldamo.org/content/words/word-2830500177.html) | maq | 11 |
| [medial [s] often became [z]](https://eldamo.org/content/words/word-127393503.html) | aq | 11 |
| [aspirates became voiceless spirants](https://eldamo.org/content/words/word-3262991621.html) | aq | 11 |
| [voiced stops became spirants except after nasals and liquids](https://eldamo.org/content/words/word-2772726195.html) | maq | 11 |
| [voiced stops became spirants except after nasals](https://eldamo.org/content/words/word-1141570065.html) | aq | 10 |
| [[nm], [ŋm] became [nw], [ŋgw]](https://eldamo.org/content/words/word-1197128543.html) | q | 10 |
| [[θ] became [s]](https://eldamo.org/content/words/word-3491983963.html) | q | 10 |
| [[ɣ] from [g] vanished](https://eldamo.org/content/words/word-1833409085.html) | q | 9 |
| [[pt], [kt] became [ps], [xt]](https://eldamo.org/content/words/word-2701010297.html) | mq | 9 |
| [[j], [w] often reduced between vowels](https://eldamo.org/content/words/word-3978101829.html) | aq | 8 |

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
| случаев (сложение × деривация) | 47 |
| соединение праформ совпало с начальной формой деривации | 16 (34%) |
| основное чтение = засвидетельствованная форма | 6 (13%) |
| форма среди вариантов | 19 (40%) |

### Сложения на последней стадии

Сложения квенья из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/quenya/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс правила §6.1 учебника (`shared/morphophonology.py`).

| показатель | случаев |
|---|---|
| сложений | 811 |
| первый вариант = засвидетельствованная форма | 392 (48%) |
| форма среди первых 8 вариантов | 551 (68%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 150) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 150 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 135 (90%) |
| первая из них = праформа Eldamo | 19 (13%) |
| праформа Eldamo среди найденных (до 8) | 39 (26%) |

Расходящиеся деривации (481) — `reports/sequencer.json`.

## Sindarin / Noldorin

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1027 | 719 (70.0%) | 765 (74.5%) |
| средняя | 1356 | 879 (64.8%) | 938 (69.2%) |
| всего | 2383 | 1598 (67.1%) | 1703 (71.5%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [long final vowels were shortened](https://eldamo.org/content/words/word-1410098833.html) | on | 70 |
| [[ai] became [oe] or [ae]](https://eldamo.org/content/words/word-3173115217.html) | n | 43 |
| [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html) | s | 24 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html) | n | 21 |
| [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2240258959.html) | s | 20 |
| [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html) | n | 18 |
| [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2951504533.html) | n | 17 |
| [[ai], [oi] became [ae], [oe]](https://eldamo.org/content/words/word-941153689.html) | s | 16 |
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html) | s | 15 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html) | os | 15 |
| [[mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-1317326183.html) | n | 12 |
| [non-initial [m] usually became [v]](https://eldamo.org/content/words/word-3030431535.html) | n | 11 |
| [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-2399289739.html) | s | 11 |
| [aspirates became voiceless spirants](https://eldamo.org/content/words/word-883570327.html) | os | 11 |
| [initial [x-] became [h-]](https://eldamo.org/content/words/word-1195324115.html) | n | 10 |

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
| случаев (сложение × деривация) | 57 |
| соединение праформ совпало с начальной формой деривации | 11 (19%) |
| основное чтение = засвидетельствованная форма | 10 (18%) |
| форма среди вариантов | 16 (28%) |

### Сложения на последней стадии

Сложения синдарина из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/sindarin/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс мягкая мутация второго элемента и правила синдарина для многосложных слов.

| показатель | случаев |
|---|---|
| сложений | 553 |
| первый вариант = засвидетельствованная форма | 203 (37%) |
| форма среди первых 8 вариантов | 322 (58%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 64) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 64 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 34 (53%) |
| первая из них = праформа Eldamo | 2 (3%) |
| праформа Eldamo среди найденных (до 8) | 8 (12%) |

Расходящиеся деривации (785) — `reports/sequencer.json`.
