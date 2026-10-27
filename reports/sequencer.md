# Проверка секвенсора

Источник: Eldamo 0.8.13. Файл создаётся `scripts/build.py`; не править вручную.

Секвенсор (`shared/sequencer.py`) прогоняет начальную форму деривации через все правила ветви в хронологическом порядке — так, как будет порождаться форма нового слова, — и сравнивает результат с конечной формой деривации Eldamo. В отличие от `audit.md`, где каждый шаг проверяется отдельно, здесь правила не подсказываются: секвенсор сам решает, какие из них применимы. Прогон останавливается на правиле последнего засвидетельствованного шага (деривация может кончаться промежуточной формой).

«Основное» — первое чтение (необязательные правила применены, из альтернатив выбрана первая подформула); «любое» — конечная форма среди всех вариантов (необязательные правила, альтернативные исходы, правила на границе морфем `+` в формах без отмеченной границы).

## Quenya / Qenya

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1212 | 920 (75.9%) | 1006 (83.0%) |
| средняя | 907 | 725 (79.9%) | 781 (86.1%) |
| ранняя | 1594 | 1063 (66.7%) | 1074 (67.4%) |
| всего | 3713 | 2708 (72.9%) | 2861 (77.1%) |

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
| случаев (сложение × деривация) | 69 |
| соединение праформ совпало с начальной формой деривации | 13 (19%) |
| основное чтение = засвидетельствованная форма | 11 (16%) |
| форма среди вариантов | 30 (43%) |

### Сложения на последней стадии

Сложения квенья из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/quenya/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс правила §6.1 учебника (`shared/morphophonology.py`).

| показатель | случаев |
|---|---|
| сложений | 459 |
| первый вариант = засвидетельствованная форма | 204 (44%) |
| форма среди первых 8 вариантов | 305 (66%) |

### Суффиксы и приставки

Производные слова Eldamo из основы и одного аффикса (часть речи `suf` или `pref`). Модель (`shared/affixes.py`, `branches/quenya/data/affixes.json`) строится без проверяемого слова: какая форма аффикса берётся после гласного и после согласного, что происходит на стыке и в конце — сначала по словам с этим же аффиксом, иначе по всем словам с аффиксом того же вида.

| | слов | первый вариант = форма Eldamo | среди первых 8 |
|---|---|---|---|
| суффиксы | 345 | 228 (66%) | 273 (79%) |
| приставки | 137 | 77 (56%) | 93 (68%) |
| всего | 482 | 305 (63%) | 366 (76%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 100) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 100 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 98 (98%) |
| первая из них = праформа Eldamo | 30 (30%) |
| праформа Eldamo среди найденных (до 8) | 49 (49%) |

Расходящиеся деривации (1005) — `reports/sequencer.json`.

## Sindarin / Noldorin

| эпоха | дериваций | основное | любое |
|---|---|---|---|
| поздняя | 1027 | 734 (71.5%) | 814 (79.3%) |
| средняя | 1356 | 923 (68.1%) | 1006 (74.2%) |
| ранняя | 377 | 227 (60.2%) | 233 (61.8%) |
| всего | 2760 | 1884 (68.3%) | 2053 (74.4%) |

### Где основное чтение впервые расходится с деривацией

Правило засвидетельствованного шага, чью форму основное чтение не проходит.

| правило | язык | дериваций |
|---|---|---|
| [long final vowels were shortened](https://eldamo.org/content/words/word-1410098833.html) | on | 69 |
| [[ai] became [oe] or [ae]](https://eldamo.org/content/words/word-3173115217.html) | n | 41 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-2794740763.html) | p | 31 |
| [short final vowels vanished](https://eldamo.org/content/words/word-1490765151.html) | n | 27 |
| [short [a], [o], [u] became [e], [œ], [y] preceding [i]](https://eldamo.org/content/words/word-1963461937.html) | n | 23 |
| [short final [e], [a], [o] vanished](https://eldamo.org/content/words/word-3998109579.html) | mp | 21 |
| [short vowels vanished before morpheme boundaries](https://eldamo.org/content/words/word-2749565259.html) | s | 17 |
| [long final vowels were shortened](https://eldamo.org/content/words/word-2753394075.html) | os | 16 |
| [final [i], [u] generally vanished](https://eldamo.org/content/words/word-1815401039.html) | s | 14 |
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
| случаев (сложение × деривация) | 68 |
| соединение праформ совпало с начальной формой деривации | 10 (15%) |
| основное чтение = засвидетельствованная форма | 15 (22%) |
| форма среди вариантов | 23 (34%) |

### Сложения на последней стадии

Сложения синдарина из двух элементов того же языка. Таблица стыков (`shared/junctions.py`, `branches/sindarin/data/junctions.json`) строится без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте в остальных сложениях; плюс мягкая мутация второго элемента и правила синдарина для многосложных слов.

| показатель | случаев |
|---|---|
| сложений | 415 |
| первый вариант = засвидетельствованная форма | 146 (35%) |
| форма среди первых 8 вариантов | 236 (57%) |

### Суффиксы и приставки

Производные слова Eldamo из основы и одного аффикса (часть речи `suf` или `pref`). Модель (`shared/affixes.py`, `branches/sindarin/data/affixes.json`) строится без проверяемого слова: какая форма аффикса берётся после гласного и после согласного, что происходит на стыке и в конце — сначала по словам с этим же аффиксом, иначе по всем словам с аффиксом того же вида.

| | слов | первый вариант = форма Eldamo | среди первых 8 |
|---|---|---|---|
| суффиксы | 167 | 83 (50%) | 93 (56%) |
| приставки | 53 | 20 (38%) | 39 (74%) |
| всего | 220 | 103 (47%) | 132 (60%) |

### Обратное восстановление праформ

Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины (первые 64) праформа восстанавливается по конечной форме: кандидаты перебираются по вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — гипотеза; так помечаются и сложения, построенные на ней.

| показатель | случаев |
|---|---|
| конечных форм | 64 |
| найдена хотя бы одна праформа, дающая форму прямым прогоном | 51 (80%) |
| первая из них = праформа Eldamo | 4 (6%) |
| праформа Eldamo среди найденных (до 8) | 12 (19%) |

Расходящиеся деривации (876) — `reports/sequencer.json`.

## Шаги без правила в деривациях Eldamo

Шаг, у которого Страк ставит «?» вместо правила: ни один известный закон его не объясняет (Q. pupso «муха» < ✶buzbō > buspō > **puspō** > pupso; законы дают βuspō, отсюда *vupso). Для каждого такого шага к форме перед ним применяются законы того же языка (`shared/unruled.py`): «правило» — шаг даёт одно правило языка, которое Eldamo не назвало; «законы» — их последовательность; «нет» — форма расходится с законами.

| язык | шагов | правило | законы | нет |
|---|---|---|---|---|
| AQ. Ancient Quenya | 14 | 0 | 0 | 14 |
| AT. Ancient Telerin | 3 | 0 | 0 | 3 |
| ᴱ✶ Early Primitive Elvish | 2 | 0 | 0 | 2 |
| ᴱQ. Early Quenya | 27 | 2 | 0 | 25 |
| G. Gnomish | 11 | 2 | 0 | 9 |
| ᴹAQ. Middle Ancient Quenya | 5 | 0 | 0 | 5 |
| ᴹ✶ Middle Primitive Elvish | 7 | 0 | 0 | 7 |
| ᴹQ. Middle Quenya | 15 | 0 | 0 | 15 |
| N. Noldorin | 36 | 4 | 0 | 32 |
| ON. Old Noldorin | 10 | 0 | 0 | 10 |
| OS. Old Sindarin | 5 | 0 | 0 | 5 |
| ✶ Primitive Elvish | 22 | 0 | 2 | 20 |
| Q. Quenya | 38 | 3 | 1 | 34 |
| S. Sindarin | 27 | 4 | 0 | 23 |
| всего | 222 | 15 | 3 | 204 |

| слово | язык | шаг Eldamo | по законам |
|---|---|---|---|
| [áye](https://eldamo.org/content/words/word-2281922935.html) | ᴱQ. Early Quenya | aije > āje | aie |
| [ambor](https://eldamo.org/content/words/word-2310858073.html) | ᴱQ. Early Quenya | ambur > ambor | ambur |
| [Angaino](https://eldamo.org/content/words/word-3060557329.html) | ᴱQ. Early Quenya | aŋgajer > aŋgear | aŋgaier |
| [anta-](https://eldamo.org/content/words/word-1837475905.html) | ᴹQ. Middle Quenya | janta > anta | janta |
| [apaitya-](https://eldamo.org/content/words/word-950362641.html) | ᴱQ. Early Quenya | apajkjne- > apaiksine- | apaitjne- |
| [ar](https://eldamo.org/content/words/word-1174557919.html) | Q. Quenya | ara > ar | ara |
| [ar](https://eldamo.org/content/words/word-1174557919.html) | Q. Quenya | ara > ar | ara |
| [árë](https://eldamo.org/content/words/word-2181143763.html) | Q. Quenya | are > ar | are |
| [asumo](https://eldamo.org/content/words/word-2210321027.html) | AQ. Ancient Quenya | atʰmō > atʰumō | atwō |
| [sehta-](https://eldamo.org/content/words/word-4251986003.html) | ᴱQ. Early Quenya | θēxjǝ > sie | sēiǝ |
| [céva](https://eldamo.org/content/words/word-4272116095.html) | AQ. Ancient Quenya | kewe > keu | kewe |
| [tyú(ta)](https://eldamo.org/content/words/word-4031567055.html) | ᴱQ. Early Quenya | teutā > tʲūta | teută |
| [ëa-](https://eldamo.org/content/words/word-227651571.html) | AQ. Ancient Quenya | ēijē > ējē | ēijē |
| [Elda](https://eldamo.org/content/words/word-3583944535.html) | AQ. Ancient Quenya | edelā > eledā | elðā |
| [Eldo](https://eldamo.org/content/words/word-2213582603.html) | ✶ Primitive Elvish | edelō > eledō | edelō |
| [austalende](https://eldamo.org/content/words/word-355382011.html) | ᴱQ. Early Quenya | austakalende > austalende | austalkende |
| [enquë](https://eldamo.org/content/words/word-2994670795.html) | Q. Quenya | eŋke > eŋkwe | eŋke |
| [enquë](https://eldamo.org/content/words/word-2994670795.html) | Q. Quenya | eŋke > eŋkwe | eŋke |
| [enquë](https://eldamo.org/content/words/word-2994670795.html) | Q. Quenya | eŋke > eŋkwe | eŋke |
| [entya](https://eldamo.org/content/words/word-1310424909.html) | AQ. Ancient Quenya | ɣenetja > enetja | henetja |
| [faire](https://eldamo.org/content/words/word-836230767.html) | ᴱQ. Early Quenya | ɸalri > faire | falri |
| [faldi](https://eldamo.org/content/words/word-4091278143.html) | ᴱQ. Early Quenya | fal̃di > faldi | fal̃di |
| [aquet-](https://eldamo.org/content/words/word-418923719.html) | Q. Quenya | atkwet > akwet | akswes |
| [yolme](https://eldamo.org/content/words/word-51673427.html) | ᴱQ. Early Quenya | ɣolwe > holwe | olve |
| [hravan](https://eldamo.org/content/words/word-3771168529.html) | Q. Quenya | r̥āvan > r̥avan | rāvan |
| [indyalme](https://eldamo.org/content/words/word-850964337.html) | ᴹQ. Middle Quenya | ŋjalme > jalme | njalme |
| [qinde](https://eldamo.org/content/words/word-4213330493.html) | ᴱQ. Early Quenya | giwindē > gwindē | kivindĕ |
| [-itë](https://eldamo.org/content/words/word-2528281223.html) | Q. Quenya | -vuite > -voite | -vuite |
| [larmo](https://eldamo.org/content/words/word-4002467419.html) | Q. Quenya | lammo > larmo | lammo |
| [lasse](https://eldamo.org/content/words/word-2211758847.html) | ᴹQ. Middle Quenya | lassēo > lasso | lassēo |
| [lat](https://eldamo.org/content/words/word-302085399.html) | ᴱQ. Early Quenya | lapt > latt | lapr |
| [neite](https://eldamo.org/content/words/word-4164290517.html) | ᴱQ. Early Quenya | neitte > neite | naitte |
| [lómelinde](https://eldamo.org/content/words/word-2793545755.html) | ᴹQ. Middle Quenya | lōmilindē > lōmelindē | lōmilindĕ |
| [talka²](https://eldamo.org/content/words/word-849353425.html) | ᴱQ. Early Quenya | talkwa > talka | talkva |
| [Máhanaxar](https://eldamo.org/content/words/word-3134454299.html) | ✶ Primitive Elvish | māxananaskad > māxanaskad | māxananaskad |
| [makar](https://eldamo.org/content/words/word-283772263.html) | ᴹAQ. Middle Ancient Quenya | mbakhar > mbakar | makhar |
| [málo](https://eldamo.org/content/words/word-294283349.html) | AQ. Ancient Quenya | mę̄lō > mālō | mēlo |
| [málo](https://eldamo.org/content/words/word-719134061.html) | ᴹAQ. Middle Ancient Quenya | mę̄lō > mālō | mę̄lo |
| [máma](https://eldamo.org/content/words/word-4142094615.html) | AQ. Ancient Quenya | māmā > mbāmā | māma |
| [maqua](https://eldamo.org/content/words/word-3458309631.html) | AQ. Ancient Quenya | mapā > makwā | mapa |
| [maqua](https://eldamo.org/content/words/word-3458309631.html) | AQ. Ancient Quenya | mapa > makwa | mapa |
| [már](https://eldamo.org/content/words/word-1556996255.html) | AQ. Ancient Quenya | mbara > mbār | mara |
| [mélamar](https://eldamo.org/content/words/word-3756694359.html) | Q. Quenya | mēlambar > mēlamar | mēlambar |
| [Morikotto](https://eldamo.org/content/words/word-1476108801.html) | Q. Quenya | morŋoθo > morŋoθ | morgoso |
| [narte](https://eldamo.org/content/words/word-2949784161.html) | ᴱQ. Early Quenya | narti > narte | nartsi |
| [nauro](https://eldamo.org/content/words/word-1339115679.html) | AQ. Ancient Quenya | ŋwaurō > ŋaurō | wauro |
| [nése](https://eldamo.org/content/words/word-2971183729.html) | ᴹQ. Middle Quenya | nettʰe > nesse | nettʰe |
| [Nessa](https://eldamo.org/content/words/word-7408399.html) | ᴹQ. Middle Quenya | nettʰa > nessa | nettʰa |
| [nier](https://eldamo.org/content/words/word-1563607161.html) | ᴱQ. Early Quenya | neōn > nion | neon |
| [nier](https://eldamo.org/content/words/word-1563607161.html) | ᴱQ. Early Quenya | negexer > nier | nēxer |
| [qin¹](https://eldamo.org/content/words/word-705831773.html) | ᴱQ. Early Quenya | giwim > gwin | kivin |
| [-nquë](https://eldamo.org/content/words/word-4127585931.html) | Q. Quenya | -iŋke > -iŋkwe | -iŋke |
| [nu](https://eldamo.org/content/words/word-2786267951.html) | Q. Quenya | nu > no | nu |
| [Oromë](https://eldamo.org/content/words/word-1616152177.html) | ✶ Primitive Elvish | arǭmēz > arǭmē | arǭmēz |
| [Oromë](https://eldamo.org/content/words/word-1616152177.html) | Q. Quenya | arome > orome | arome |
| [Oromë](https://eldamo.org/content/words/word-1616152177.html) | ✶ Primitive Elvish | arǭmēz > arǭmē | arǭmēz |
| [Oromë](https://eldamo.org/content/words/word-1616152177.html) | Q. Quenya | arome > orome | arome |
| [orta-¹](https://eldamo.org/content/words/word-617970291.html) | AQ. Ancient Quenya | orortaijē > orortajē | orortaijē |
| [otsëa](https://eldamo.org/content/words/word-29466041.html) | Q. Quenya | otsoia > otsea | ostoia |
| [pasta](https://eldamo.org/content/words/word-3475768127.html) | Q. Quenya | ? > passa | ? |
| [pasta](https://eldamo.org/content/words/word-3475768127.html) | Q. Quenya | patta > pasta | patta |
| [pasta](https://eldamo.org/content/words/word-3360090595.html) | ᴹQ. Middle Quenya | patta > pasta | patta |
| [pella](https://eldamo.org/content/words/word-966567391.html) | Q. Quenya | petʰla > pella | petʰala |
| [pella](https://eldamo.org/content/words/word-966567391.html) | Q. Quenya | pelola > pella | pelola |
| [pella](https://eldamo.org/content/words/word-966567391.html) | Q. Quenya | pelola > pella | pelola |
| [pupso](https://eldamo.org/content/words/word-3934957721.html) | AQ. Ancient Quenya | buspō > puspō | βuspō |
| [pupso](https://eldamo.org/content/words/word-2909200141.html) | ᴹAQ. Middle Ancient Quenya | buspō > puspō | βuspō |
| [qapta-²](https://eldamo.org/content/words/word-62970959.html) | ᴱ✶ Early Primitive Elvish | kʷapja- > kʷapta- | kʷapja- |
| [Qen](https://eldamo.org/content/words/word-1041894885.html) | ᴹAQ. Middle Ancient Quenya | kwendmēn > kwenmēn | kwennmēn |
| [qenso](https://eldamo.org/content/words/word-3975726839.html) | ᴹQ. Middle Quenya | kwentso > kwenso | kwensso |
| [rantala](https://eldamo.org/content/words/word-1164302847.html) | AQ. Ancient Quenya | rantʰlā > rantlā | rattalā |
| [rendo](https://eldamo.org/content/words/word-2916398763.html) | ᴱQ. Early Quenya | rerro > rēro | lerro |
| [saitya-](https://eldamo.org/content/words/word-27410679.html) | ᴱQ. Early Quenya | sajkjne > saiksine | saitjne |
| [samna¹](https://eldamo.org/content/words/word-1535675635.html) | ᴹQ. Middle Quenya | samne > samna | samne |
| [Sangahyando](https://eldamo.org/content/words/word-1617303585.html) | ᴹQ. Middle Quenya | θaŋgasjandō > θaŋgaj̊ando | saŋgasjandŏ |
| [sintamo](https://eldamo.org/content/words/word-2325395425.html) | Q. Quenya | siŋkitamo > sintamo | siŋkitamo |
| [sintl](https://eldamo.org/content/words/word-4148804871.html) | ᴱQ. Early Quenya | sintʲl > sintḷ | sintʲl |
| [histe-](https://eldamo.org/content/words/word-1521168377.html) | ᴱQ. Early Quenya | siste- > histe- | siste- |
| [tallune](https://eldamo.org/content/words/word-736410737.html) | ᴹQ. Middle Quenya | tallunja > tallune | tallunja |
| [tára²](https://eldamo.org/content/words/word-2520533029.html) | Q. Quenya | dāra > tāra | dāra |
| [telemna](https://eldamo.org/content/words/word-1502301043.html) | ᴹQ. Middle Quenya | tjelemna > telemna | tjelemna |
| [Teler](https://eldamo.org/content/words/word-933169263.html) | Q. Quenya | tjeleri > teleri | tjeleri |
| [telluma](https://eldamo.org/content/words/word-984079151.html) | ✶ Primitive Elvish | delgūmā > telgūmā | delgūmā |
| [telpë](https://eldamo.org/content/words/word-3102361379.html) | Q. Quenya | tjelpe > telpe | tjelpe |
| [Telperion](https://eldamo.org/content/words/word-1768035437.html) | Q. Quenya | tjelperion > telperion | tjelperion |
| [telpina](https://eldamo.org/content/words/word-2182815399.html) | ᴹQ. Middle Quenya | tjelpina > telpina | tjelpina |
| [teltasse](https://eldamo.org/content/words/word-502925457.html) | ᴱQ. Early Quenya | tetlasse > teltasse | tetlasse |
| [téma](https://eldamo.org/content/words/word-3450097969.html) | ᴹ✶ Middle Primitive Elvish | teŋma > teɣma | teŋma |
| [tuilindo](https://eldamo.org/content/words/word-2807327843.html) | ᴹAQ. Middle Ancient Quenya | tuilelindō > tuilindō | tuilelindō |
| [Tulkas](https://eldamo.org/content/words/word-2183349377.html) | ✶ Primitive Elvish | tulukʰastāz > tulukʰasta | tulukʰastāz |
| [turya-](https://eldamo.org/content/words/word-4171193413.html) | ᴱQ. Early Quenya | tuðjine- > tustine- | turjine- |
| [tyastava-](https://eldamo.org/content/words/word-261832195.html) | ᴱQ. Early Quenya | tʲastʲava- > tʲastava- | tʲastʲava- |
| [ú¹](https://eldamo.org/content/words/word-3345320209.html) | Q. Quenya | awa- > ū | ava- |
| [Ulmo](https://eldamo.org/content/words/word-159959277.html) | Q. Quenya | ulubōz > ulmo | ulubŏr |
| [úpa](https://eldamo.org/content/words/word-2831863345.html) | Q. Quenya | ūopa > ūpa | ūopa |
| [Valinor](https://eldamo.org/content/words/word-2643047643.html) | ᴹQ. Middle Quenya | valindor > valinor | valindor |
| [Valinor](https://eldamo.org/content/words/word-2643047643.html) | ᴹQ. Middle Quenya | valindor > valinor | valindor |
| [yunquë](https://eldamo.org/content/words/word-693947865.html) | Q. Quenya | jūneke > juŋkwe | jūneke |
| [yunquë](https://eldamo.org/content/words/word-693947865.html) | Q. Quenya | jūnekē > juŋkwe | jūnekĕ |
| [yunquë](https://eldamo.org/content/words/word-693947865.html) | Q. Quenya | jūneke > juŋkwe | jūneke |
| [yúyal](https://eldamo.org/content/words/word-2254977541.html) | Q. Quenya | jujal > jūjal | jujal |
| [Araw](https://eldamo.org/content/words/word-802454491.html) | ✶ Primitive Elvish | arǭmēz > arāmē | arǭmēz |
| [lebethron](https://eldamo.org/content/words/word-1323679033.html) | ✶ Primitive Elvish | lepettaoroni > lepettaroni | lepettārone |
| [lhevnar](https://eldamo.org/content/words/word-4215730511.html) | ᴹ✶ Middle Primitive Elvish | lepenar > lepnar | lepenar |
| [Morgoth](https://eldamo.org/content/words/word-941880637.html) | ✶ Primitive Elvish | moriŋgotto > moreŋgotto | moriŋgotto |
| [Morgoth](https://eldamo.org/content/words/word-941880637.html) | ✶ Primitive Elvish | moriŋgotʰo > moreŋgotʰo | moriŋgotʰo |
| [taer](https://eldamo.org/content/words/word-2191471427.html) | ᴹ✶ Middle Primitive Elvish | teñrā > tǣr | tērā |
| [tathor](https://eldamo.org/content/words/word-328291671.html) | ᴹ✶ Middle Primitive Elvish | tatʰarē > tatʰrē | tatʰarē |
| [natsai](https://eldamo.org/content/words/word-1834563299.html) | N. Noldorin | naθ > naiθ | nāθ |
| [Eldo](https://eldamo.org/content/words/word-2213582603.html) | ✶ Primitive Elvish | edelō > eledō | edelō |
| [Máhanaxar](https://eldamo.org/content/words/word-3134454299.html) | ✶ Primitive Elvish | māxananaskad > māxanaskad | māxananaskad |
| [Oromë](https://eldamo.org/content/words/word-1616152177.html) | ✶ Primitive Elvish | arǭmēz > arǭmē | arǭmēz |
| [Oromë](https://eldamo.org/content/words/word-1616152177.html) | ✶ Primitive Elvish | arǭmēz > arǭmē | arǭmēz |
| [qapta-²](https://eldamo.org/content/words/word-62970959.html) | ᴱ✶ Early Primitive Elvish | kʷapja- > kʷapta- | kʷapja- |
| [telluma](https://eldamo.org/content/words/word-984079151.html) | ✶ Primitive Elvish | delgūmā > telgūmā | delgūmā |
| [Tulkas](https://eldamo.org/content/words/word-2183349377.html) | ✶ Primitive Elvish | tulukʰastāz > tulukʰasta | tulukʰastāz |
| [-a](https://eldamo.org/content/words/word-1377240439.html) | S. Sindarin | -ō > -a | -ū |
| [a¹](https://eldamo.org/content/words/word-2814200763.html) | S. Sindarin | að > a | āð |
| [al-](https://eldamo.org/content/words/word-2152060361.html) | N. Noldorin | la- > al- | l̥a- |
| [anna-](https://eldamo.org/content/words/word-1272131327.html) | S. Sindarin | ǭne > ōne | aun |
| [anna-](https://eldamo.org/content/words/word-1272131327.html) | S. Sindarin | anθa- > anta- | anna- |
| [annabon](https://eldamo.org/content/words/word-2066803871.html) | N. Noldorin | andambond > andabond | annamon |
| [ar(a)-](https://eldamo.org/content/words/word-1222397067.html) | S. Sindarin | aran- > ara- | aran- |
| [Araw](https://eldamo.org/content/words/word-802454491.html) | S. Sindarin | orau > arau | oro |
| [Araw](https://eldamo.org/content/words/word-802454491.html) | S. Sindarin | orauv > arauv | orau |
| [Araw](https://eldamo.org/content/words/word-802454491.html) | ✶ Primitive Elvish | arǭmēz > arāmē | arǭmēz |
| [Balan](https://eldamo.org/content/words/word-1841526965.html) | N. Noldorin | Bala > Balan | Bāl |
| [Bedhwen](https://eldamo.org/content/words/word-3319196731.html) | ON. Old Noldorin | bedū+ina > bedwina | bedū+ina |
| [blectha](https://eldamo.org/content/words/word-2217074665.html) | G. Gnomish | belektā > blektā | belekθă |
| [brand²](https://eldamo.org/content/words/word-3034985991.html) | AT. Ancient Telerin | barántē > barándē | brántē |
| [ci](https://eldamo.org/content/words/word-2298877587.html) | S. Sindarin | kī > ki | kī |
| [Cirdan](https://eldamo.org/content/words/word-3197078363.html) | N. Noldorin | kerθan > kirdan | kerθ |
| [climli](https://eldamo.org/content/words/word-1777072535.html) | G. Gnomish | klim > klimli | klim |
| [cuen](https://eldamo.org/content/words/word-365143529.html) | N. Noldorin | kwen > kuen | kwe |
| [cûr](https://eldamo.org/content/words/word-3523932767.html) | G. Gnomish | kur > kūr | kor |
| [curu](https://eldamo.org/content/words/word-1953081923.html) | N. Noldorin | kyrwi > kyrui | kyru |
| [aphed-](https://eldamo.org/content/words/word-1429737613.html) | AT. Ancient Telerin | atpet- > appet- | atpet- |
| [dî](https://eldamo.org/content/words/word-3681659819.html) | N. Noldorin | nī > dī | nī |
| [di¹](https://eldamo.org/content/words/word-806516075.html) | S. Sindarin | dī > di | dī |
| [di²](https://eldamo.org/content/words/word-3183924893.html) | S. Sindarin | dī > di | dī |
| [ennin](https://eldamo.org/content/words/word-1979185855.html) | ON. Old Noldorin | andajīn > andjīn | andaiīn |
| [fanui](https://eldamo.org/content/words/word-4016710911.html) | S. Sindarin | fanoe > fanui | fano |
| [fanui](https://eldamo.org/content/words/word-4016710911.html) | S. Sindarin | fanoe > fanui | fano |
| [Feanor](https://eldamo.org/content/words/word-1330791695.html) | N. Noldorin | ɸaeanour > ɸeanour | faeanor |
| [feira-](https://eldamo.org/content/words/word-520680149.html) | N. Noldorin | feria- > feira- | feria- |
| [Felagund](https://eldamo.org/content/words/word-3295824739.html) | S. Sindarin | felaggund > felagund | felagun |
| [ferui](https://eldamo.org/content/words/word-1754724095.html) | S. Sindarin | fair > ferui | faer |
| [galw](https://eldamo.org/content/words/word-138930587.html) | N. Noldorin | galv > galu | galv |
| [glosui](https://eldamo.org/content/words/word-3768993343.html) | S. Sindarin | glossui > glosui | glossui |
| [gor-²](https://eldamo.org/content/words/word-2804380087.html) | S. Sindarin | or- > gor- | ōr- |
| [grond](https://eldamo.org/content/words/word-4288358417.html) | N. Noldorin | runda > grunda | r̥onn |
| [guruth](https://eldamo.org/content/words/word-1254089755.html) | N. Noldorin | gurθu > guruθ | gorθ |
| [gwae](https://eldamo.org/content/words/word-4071975747.html) | S. Sindarin | gwoe > gwae | go |
| [gwae](https://eldamo.org/content/words/word-4071975747.html) | S. Sindarin | gwoe > gwae | go |
| [gwarin(n)](https://eldamo.org/content/words/word-110681955.html) | G. Gnomish | gʷaren > gʷarin | gʷaren |
| [gwin](https://eldamo.org/content/words/word-1982054357.html) | G. Gnomish | giwini > gʷini | givin |
| [gwethli](https://eldamo.org/content/words/word-255884551.html) | G. Gnomish | gʷeðeθlī > gʷeθlī | gʷeðeθlĭ |
| [Hadhod](https://eldamo.org/content/words/word-4253031949.html) | OS. Old Sindarin | kʰazād > kʰaðād | xazǭd |
| [haltha-](https://eldamo.org/content/words/word-1801574793.html) | N. Noldorin | sxalia- > sxalθa- | helia- |
| [hath-](https://eldamo.org/content/words/word-99449753.html) | G. Gnomish | aθ- > haθ- | oθ- |
| [hath-](https://eldamo.org/content/words/word-99449753.html) | G. Gnomish | aθs- > haθs- | ass- |
| [heryn](https://eldamo.org/content/words/word-4231489635.html) | OS. Old Sindarin | kʰerūnī > kʰerunī | xerūnĭ |
| [Cílu](https://eldamo.org/content/words/word-3739342651.html) | N. Noldorin | xīlū > xīlu | hĭlŭ |
| [lhalorn](https://eldamo.org/content/words/word-2222043839.html) | N. Noldorin | l̥alvorn > l̥alorn | l̥alvorn |
| [lalven](https://eldamo.org/content/words/word-2500064443.html) | N. Noldorin | l̥alven > l̥alwen | l̥alv |
| [lalven](https://eldamo.org/content/words/word-2500064443.html) | N. Noldorin | lelvin > lelwin | l̥ilv |
| [lebethron](https://eldamo.org/content/words/word-1323679033.html) | ✶ Primitive Elvish | lepettaoroni > lepettaroni | lepettārone |
| [lhevnar](https://eldamo.org/content/words/word-4215730511.html) | ᴹ✶ Middle Primitive Elvish | lepenar > lepnar | lepenar |
| [Morgoth](https://eldamo.org/content/words/word-941880637.html) | ✶ Primitive Elvish | moriŋgotto > moreŋgotto | moriŋgotto |
| [Morgoth](https://eldamo.org/content/words/word-941880637.html) | ✶ Primitive Elvish | moriŋgotʰo > moreŋgotʰo | moriŋgotʰo |
| [nâr](https://eldamo.org/content/words/word-1105130879.html) | N. Noldorin | naðr > nâr | naðor |
| [neth](https://eldamo.org/content/words/word-2010726967.html) | N. Noldorin | neθr > neθ | neθor |
| [pethron](https://eldamo.org/content/words/word-602686523.html) | OS. Old Sindarin | penθro > penθrondo | penθro |
| [pethron](https://eldamo.org/content/words/word-2645852383.html) | ON. Old Noldorin | penθro > penθrondo | penθro |
| [Rohan](https://eldamo.org/content/words/word-2305351935.html) | N. Noldorin | roxan > rohan | r̥ōx |
| [rusc](https://eldamo.org/content/words/word-3717607423.html) | S. Sindarin | urusk > rusk | urusg |
| [rust](https://eldamo.org/content/words/word-3294494683.html) | S. Sindarin | urust > rust | urust |
| [ruthra-](https://eldamo.org/content/words/word-1303029907.html) | S. Sindarin | uruθra- > ruθra- | uroθra- |
| [rhŷn](https://eldamo.org/content/words/word-418954769.html) | N. Noldorin | rœin > ryn | r̥e |
| [ha](https://eldamo.org/content/words/word-3194961055.html) | ON. Old Noldorin | sa > ha | sa |
| [he](https://eldamo.org/content/words/word-3309481503.html) | ON. Old Noldorin | se > he | sa |
| [ho](https://eldamo.org/content/words/word-3595776083.html) | ON. Old Noldorin | so > ho | so |
| [iell](https://eldamo.org/content/words/word-2361617535.html) | N. Noldorin | sell > jell | sell |
| [silith](https://eldamo.org/content/words/word-764367253.html) | N. Noldorin | siliv > siliθ | siliw |
| [sinnai](https://eldamo.org/content/words/word-1118431655.html) | G. Gnomish | sindanai > sindai | sindanĭ |
| [tâd](https://eldamo.org/content/words/word-4250276895.html) | OS. Old Sindarin | atata > tata | atata |
| [taer](https://eldamo.org/content/words/word-2191471427.html) | ᴹ✶ Middle Primitive Elvish | teñrā > tǣr | tērā |
| [tathor](https://eldamo.org/content/words/word-328291671.html) | ᴹ✶ Middle Primitive Elvish | tatʰarē > tatʰrē | tatʰarē |
| [tavn](https://eldamo.org/content/words/word-620689743.html) | S. Sindarin | tamana > tamna | tavan |
| [taw](https://eldamo.org/content/words/word-1803235947.html) | N. Noldorin | towa > toua | tōw |
| [tew](https://eldamo.org/content/words/word-184661859.html) | N. Noldorin | teime > tīme | taiw |
| [thaun](https://eldamo.org/content/words/word-510540927.html) | N. Noldorin | θōn > θǭn | θō |
| [Thû](https://eldamo.org/content/words/word-658396623.html) | OS. Old Sindarin | tʰowō > tʰouō | θowŏ |
| [Tinúviel](https://eldamo.org/content/words/word-976503765.html) | N. Noldorin | tinnūviel > tinūviel | tinnŭiel |
| [trenarn](https://eldamo.org/content/words/word-1581608081.html) | N. Noldorin | trenārn > trenarn | trenārn |
| [Arandur](https://eldamo.org/content/words/word-1709396421.html) | ON. Old Noldorin | arandūr > arandur | arandūr |
| [Araume](https://eldamo.org/content/words/word-294533031.html) | N. Noldorin | oraume > araume | orov |
| [Araume](https://eldamo.org/content/words/word-294533031.html) | N. Noldorin | oraume > araume | orov |
| [Barathi(l)](https://eldamo.org/content/words/word-2863783273.html) | N. Noldorin | barathi > barathil | baredh |
| [inpanta](https://eldamo.org/content/words/word-1943416903.html) | ON. Old Noldorin | jenpanta > jinpanta | jenɸanθa |
| [lepni(a)](https://eldamo.org/content/words/word-995828525.html) | S. Sindarin | lepein > lepnia | lebai |
| [nī](https://eldamo.org/content/words/word-2457262775.html) | ON. Old Noldorin | nī > dī | nī |
| [-wega](https://eldamo.org/content/words/word-793654921.html) | ON. Old Noldorin | wego > wega | wego |
| [phile](https://eldamo.org/content/words/word-3969678323.html) | AT. Ancient Telerin | pʰili > pʰile | pʰili |
