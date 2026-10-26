# Проверка секвенсора

Источник: Eldamo 0.8.13. Файл создаётся `scripts/build.py`; не править вручную.

Секвенсор (`shared/sequencer.py`) прогоняет начальную форму деривации через все правила ветви в хронологическом порядке — так, как будет порождаться форма нового слова, — и сравнивает результат с конечной формой деривации Eldamo. В отличие от `audit.md`, где каждый шаг проверяется отдельно, здесь правила не подсказываются: секвенсор сам решает, какие из них применимы. Прогон останавливается на правиле последнего засвидетельствованного шага (деривация может кончаться промежуточной формой).

«Основное» — первое чтение (необязательные правила применены, из альтернатив выбрана первая подформула); «любое» — конечная форма среди всех вариантов (необязательные правила, альтернативные исходы, правила на границе морфем `+` в формах без отмеченной границы).

## Quenya / Qenya

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1212 | 916 (75.6%) | 999 (82.4%) |
| средняя | 907 | 726 (80.0%) | 782 (86.2%) |
| ранняя | 1594 | 1035 (64.9%) | 1055 (66.2%) |
| всего | 3713 | 2677 (72.1%) | 2836 (76.4%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [voiced spirants becames stops after liquids, nasals and [z]](https://eldamo.org/content/words/word-1497556499.html) | eq | 65 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-2794740763.html) | p | 59 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html) | mp | 50 |
| [[j], [w] became [i], [u] after a vowel](https://eldamo.org/content/words/word-2868696637.html) | eq | 44 |
| [final consonant clusters simplified](https://eldamo.org/content/words/word-4175300709.html) | eq | 37 |
| [final [ss], [st], [ps], [ts], [ks] became [s]](https://eldamo.org/content/words/word-2485190991.html) | eq | 36 |
| [[β] became [v]](https://eldamo.org/content/words/word-1245311459.html) | eq | 32 |
| [short syllabic [ṇ] became [a] + homorganic nasal, [i] before palatals or [u] before labials](https://eldamo.org/content/words/word-2670096403.html) | eq | 30 |
| [short syllabic [ḷ] became [il], or [ul] before labials](https://eldamo.org/content/words/word-1720939405.html) | eq | 25 |
| [short final [e], [a], [o] became [ǝ]](https://eldamo.org/content/words/word-2954387961.html) | ep | 15 |
| [[ð] became [z]](https://eldamo.org/content/words/word-1053361623.html) | eq | 15 |
| [short final [i], [u] became [e], [o]](https://eldamo.org/content/words/word-4062489737.html) | ep | 15 |
| [initial [x-] became [h-]](https://eldamo.org/content/words/word-777007581.html) | eq | 15 |
| [[t+t], [d+d] from suffixion became [st], [zd]](https://eldamo.org/content/words/word-2479050823.html) | p | 14 |
| [long syllabic [ṇ̄] became [a] + homorganic nasal](https://eldamo.org/content/words/word-406180735.html) | eq | 12 |

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
| случаев (сложение × деривация) | 63 |
| соединение праформ совпало с начальной формой деривации | 17 (27%) |
| основное чтение = засвидетельствованная форма | 8 (13%) |
| форма среди вариантов | 30 (48%) |

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
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 98 (98%) |
| первая из них = праформа Eldamo | 30 (30%) |
| праформа Eldamo среди найденных (до 8) | 49 (49%) |

Расходящиеся деривации (1036) — `reports/sequencer.json`.

## Sindarin / Noldorin

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1027 | 715 (69.6%) | 791 (77.0%) |
| средняя | 1356 | 875 (64.5%) | 957 (70.6%) |
| ранняя | 377 | 214 (56.8%) | 220 (58.4%) |
| всего | 2760 | 1804 (65.4%) | 1968 (71.3%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [long final vowels were shortened](https://eldamo.org/content/words/word-1410098833.html) | on | 69 |
| [[ai] became [oe] or [ae]](https://eldamo.org/content/words/word-3173115217.html) | n | 40 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-2794740763.html) | p | 31 |
| [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html) | n | 27 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html) | n | 23 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html) | mp | 21 |
| [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2951504533.html) | n | 18 |
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html) | s | 17 |
| [voiceless stops spirantalized after many consonants](https://eldamo.org/content/words/word-473550387.html) | g | 15 |
| [short final vowels vanished](https://eldamo.org/content/words/word-813787869.html) | s | 15 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html) | os | 15 |
| [final [i], [u] generally vanished](https://eldamo.org/content/words/word-1815401039.html) | s | 14 |
| [voiceless stops voiced after vowels](https://eldamo.org/content/words/word-2240258959.html) | s | 13 |
| [short final vowels vanished](https://eldamo.org/content/words/word-634661439.html) | g | 13 |
| [non-initial [m] usually became [v]](https://eldamo.org/content/words/word-3030431535.html) | n | 13 |

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
| случаев (сложение × деривация) | 66 |
| соединение праформ совпало с начальной формой деривации | 10 (15%) |
| основное чтение = засвидетельствованная форма | 11 (17%) |
| форма среди вариантов | 19 (29%) |

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
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 51 (80%) |
| первая из них = праформа Eldamo | 4 (6%) |
| праформа Eldamo среди найденных (до 8) | 12 (19%) |

Расходящиеся деривации (956) — `reports/sequencer.json`.
