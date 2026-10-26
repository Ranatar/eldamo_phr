# Проверка секвенсора

Источник: Eldamo 0.8.13. Файл создаётся `scripts/build.py`; не править вручную.

Секвенсор (`shared/sequencer.py`) прогоняет начальную форму деривации через все правила ветви в хронологическом порядке — так, как будет порождаться форма нового слова, — и сравнивает результат с конечной формой деривации Eldamo. В отличие от `audit.md`, где каждый шаг проверяется отдельно, здесь правила не подсказываются: секвенсор сам решает, какие из них применимы. Прогон останавливается на правиле последнего засвидетельствованного шага (деривация может кончаться промежуточной формой).

«Основное» — первое чтение (необязательные правила применены, из альтернатив выбрана первая подформула); «любое» — конечная форма среди всех вариантов (необязательные правила, альтернативные исходы, правила на границе морфем `+` в формах без отмеченной границы).

## Quenya / Qenya

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1212 | 921 (76.0%) | 1006 (83.0%) |
| средняя | 907 | 725 (79.9%) | 781 (86.1%) |
| ранняя | 1594 | 1063 (66.7%) | 1074 (67.4%) |
| всего | 3713 | 2709 (73.0%) | 2861 (77.1%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [voiced spirants becames stops after liquids, nasals and [z]](https://eldamo.org/content/words/word-1497556499.html) | eq | 65 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-2794740763.html) | p | 59 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html) | mp | 50 |
| [[j], [w] became [i], [u] after a vowel](https://eldamo.org/content/words/word-2868696637.html) | eq | 46 |
| [final consonant clusters simplified](https://eldamo.org/content/words/word-4175300709.html) | eq | 38 |
| [final [ss], [st], [ps], [ts], [ks] became [s]](https://eldamo.org/content/words/word-2485190991.html) | eq | 36 |
| [short syllabic [ṇ] became [a] + homorganic nasal, [i] before palatals or [u] before labials](https://eldamo.org/content/words/word-2670096403.html) | eq | 29 |
| [[β] became [v]](https://eldamo.org/content/words/word-1245311459.html) | eq | 27 |
| [short syllabic [ḷ] became [il], or [ul] before labials](https://eldamo.org/content/words/word-1720939405.html) | eq | 17 |
| [[ð] became [z]](https://eldamo.org/content/words/word-1053361623.html) | eq | 15 |
| [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-4062489737.html) | ep | 15 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | p | 14 |
| [initial [x-] became [h-]](https://eldamo.org/content/words/word-777007581.html) | eq | 14 |
| [long syllabic [ṇ̄] became [a] + homorganic nasal](https://eldamo.org/content/words/word-406180735.html) | eq | 12 |
| [initial [gʷ] became [w]](https://eldamo.org/content/words/word-1196923337.html) | eq | 12 |

### Условие «elsewhere»

Общая подформула не применяется там, где более позднее правило того же языка задаёт тот же вход для определённой позиции:

- eq: [ndj] became [nj] in Inwelin ← initial nasalized stops became nasals
- eq: medial [sj] became [j̊] ← initial [sw] and [sβ] became [f], [sj] became [j̊]
- eq: [sp] became [ps], [sk] sometimes [ks] ← final [sk] became [ss]
- eq: voiceless and voiced [w] became [f], [v] in Inwelin ← [w] became [v] in Cortirion, later [j], [w] became [i], [u] finally or between a vowel and a consonant
- eq: [kt] became [xt] ← final consonant clusters simplified
- aq: stops frequently underwent metathesis with nasals and liquids ← initial [dr-], [dl-] became [r-], [l-]
- aq: [sr] became [ss] ← initial [s] unvoiced following continuant
- q: [pt], [kt] became [ɸt], [xt] ← final consonant clusters reduced
- maq: stops frequently underwent metathesis with nasals and liquids ← initial [dr-], [dl-] became [r-], [l-]
- maq: [sr] became [ss] ← initial [s] unvoiced following continuant

Подформул вне документированной нотации, пропускаемых секвенсором: 4 (в 3 правилах).

### Сложения с праформами

Сложения Eldamo из двух элементов, у которых есть деривация от праформы и праформы обоих элементов. Праформы элементов соединяются через `+` (полный первый элемент или без конечного гласного), затем соединение проходит все правила ветви (`shared/compound.py`).

| показатель | случаев |
|---|---|
| случаев (сложение × деривация) | 64 |
| соединение праформ совпало с начальной формой деривации | 13 (20%) |
| основное чтение = засвидетельствованная форма | 8 (12%) |
| форма среди вариантов | 27 (42%) |

### Сложения на последней стадии

Сложения квенья из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/quenya/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс правила §6.1 учебника (`shared/morphophonology.py`).

| показатель | случаев |
|---|---|
| сложений | 423 |
| первый вариант = засвидетельствованная форма | 196 (46%) |
| форма среди первых 8 вариантов | 281 (66%) |

### Суффиксы и приставки

Производные слова Eldamo из основы и одного аффикса (часть речи `suf` или `pref`). Модель (`shared/affixes.py`, `branches/quenya/data/affixes.json`) строится без проверяемого слова: какая форма аффикса берётся после гласного и после согласного, что происходит на стыке и в конце — сначала по словам с этим же аффиксом, иначе по всем словам с аффиксом того же вида.

| | слов | первый вариант = форма Eldamo | среди первых 8 |
|---|---|---|---|
| суффиксы | 327 | 213 (65%) | 259 (79%) |
| приставки | 118 | 63 (53%) | 76 (64%) |
| всего | 445 | 276 (62%) | 335 (75%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 100) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 100 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 98 (98%) |
| первая из них = праформа Eldamo | 30 (30%) |
| праформа Eldamo среди найденных (до 8) | 49 (49%) |

Расходящиеся деривации (1004) — `reports/sequencer.json`.

## Sindarin / Noldorin

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1027 | 743 (72.3%) | 791 (77.0%) |
| средняя | 1356 | 923 (68.1%) | 1006 (74.2%) |
| ранняя | 377 | 227 (60.2%) | 233 (61.8%) |
| всего | 2760 | 1893 (68.6%) | 2030 (73.6%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [long final vowels were shortened](https://eldamo.org/content/words/word-1410098833.html) | on | 69 |
| [[ai] became [oe] or [ae]](https://eldamo.org/content/words/word-3173115217.html) | n | 41 |
| [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html) | n | 27 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html) | n | 23 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html) | mp | 21 |
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html) | s | 17 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html) | os | 16 |
| [final [i], [u] generally vanished](https://eldamo.org/content/words/word-1815401039.html) | s | 14 |
| [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2240258959.html) | s | 13 |
| [short final vowels vanished](https://eldamo.org/content/words/word-634661439.html) | g | 13 |
| [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html) | s | 12 |
| [final [i] intruded into preceding syllable](https://eldamo.org/content/words/word-2399289739.html) | s | 12 |
| [non-initial [m] usually became [v]](https://eldamo.org/content/words/word-3030431535.html) | n | 11 |
| [[ŋ] became [ŋg]](https://eldamo.org/content/words/word-2869972293.html) | g | 10 |
| [long voiceless spirants shortened](https://eldamo.org/content/words/word-4228274355.html) | g | 9 |

### Условие «elsewhere»

Общая подформула не применяется там, где более позднее правило того же языка задаёт тот же вход для определённой позиции:

- g: [nd] generally became [nn], while [mb] became [m] finally ← initial nasals vanished before stops
- s: short [u] often became [o] ← final [i], [u] generally vanished
- n: short [u] often became [o] ← final [i], [u] generally vanished
- n: short [a], [o], [u] became [e], [œ], [y] preceding [i] ← final [i] intruded into preceding syllable

Подформул вне документированной нотации, пропускаемых секвенсором: 2 (в 2 правилах).

### Сложения с праформами

Сложения Eldamo из двух элементов, у которых есть деривация от праформы и праформы обоих элементов. Праформы элементов соединяются через `+` (полный первый элемент или без конечного гласного), затем соединение проходит все правила ветви (`shared/compound.py`).

| показатель | случаев |
|---|---|
| случаев (сложение × деривация) | 63 |
| соединение праформ совпало с начальной формой деривации | 10 (16%) |
| основное чтение = засвидетельствованная форма | 11 (17%) |
| форма среди вариантов | 19 (30%) |

### Сложения на последней стадии

Сложения синдарина из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/sindarin/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс мягкая мутация второго элемента и правила синдарина для многосложных слов.

| показатель | случаев |
|---|---|
| сложений | 388 |
| первый вариант = засвидетельствованная форма | 150 (39%) |
| форма среди первых 8 вариантов | 242 (62%) |

### Суффиксы и приставки

Производные слова Eldamo из основы и одного аффикса (часть речи `suf` или `pref`). Модель (`shared/affixes.py`, `branches/sindarin/data/affixes.json`) строится без проверяемого слова: какая форма аффикса берётся после гласного и после согласного, что происходит на стыке и в конце — сначала по словам с этим же аффиксом, иначе по всем словам с аффиксом того же вида.

| | слов | первый вариант = форма Eldamo | среди первых 8 |
|---|---|---|---|
| суффиксы | 154 | 75 (49%) | 86 (56%) |
| приставки | 42 | 17 (40%) | 29 (69%) |
| всего | 196 | 92 (47%) | 115 (59%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 64) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 64 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 36 (56%) |
| первая из них = праформа Eldamo | 2 (3%) |
| праформа Eldamo среди найденных (до 8) | 10 (16%) |

Расходящиеся деривации (867) — `reports/sequencer.json`.
