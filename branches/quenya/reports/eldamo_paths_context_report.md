# Аудит сквозных линий Eldamo: контексты, примеры и развёрнутые заметки

**Источник:** локальный архив Eldamo 0.8.13. Сопоставлены 101 кандидат из предыдущей модели с индивидуальными страницами всех участвующих фонетических правил.

## Ключевой результат

Предыдущие линии **не подтверждены как полные истории звуков**. Наличие формул на страницах правил доказывает отдельные переходы, но не доказывает допустимость их последовательного соединения для одного слова. В частности, примеры на разных страницах могут относиться к разным корням, позициям и редакциям.

## Результат машинного аудита

| Показатель | Значение |
|---|---:|
| Кандидатных цепочек | 101 |
| Различных страниц правил | 81 |
| Цепочек со страницами правил других языков | 43 |
| Цепочек, где хотя бы у одного правила извлечён пояснительный текст | 60 |
| Цепочек, где на страницах правил есть примеры преобразований | 97 |
| Цепочек с общей ссылкой на слово в примерах двух соседних правил | 60 |
| Цепочек, подтверждённых последовательностью форм **одного и того же слова** | **0 (ещё не установлено)** |

Значение «0» в последней строке означает **отсутствие выполненной доказательной проверки**, а не доказанное отсутствие таких цепочек в Eldamo.

## Как использованы развёрнутые заметки

Для каждой страницы правила сохранены видимые пояснительные абзацы, примеры из *Phonetic Rule Examples*, язык самой страницы, а также индикаторы формулировок вроде `only`, `sometimes`, `before`, `after`, `initial`, `final`, `uncertain`. Эти слова **не являются автоматическими логическими условиями**: они служат указателями для ручной проверки, поскольку могут описывать не ограничения, а исторические замечания.

**Методологическое предупреждение:** если пояснение содержит исключение или альтернативную датировку, оно может опровергать соединение даже при формальном совпадении соседних звуков.

## Цепочки с дополнительным риском

Кандидаты ниже используют хотя бы одну ссылку на фонетическое правило со страницей другого языка (по заголовку соответствующей страницы); требуется выяснить, относится ли такой переход к квенийской линии, или это некорректное присоединение.

| ID | Цепочка | Язык внешнего правила |
|---|---|---|
| 3 | `ŋ- → ŋg- → ŋ- → ø-` | Telerin |
| 9 | `ŋ → g → ɣ → ø` | Danian/Ossiriandic |
| 10 | `ŋ → g → ɣ → ø` | Danian/Ossiriandic, Old Noldorin |
| 11 | `ɣ → g → ɣ → ø` | Danian/Ossiriandic |
| 12 | `ɣ → g → ɣ → ø` | Danian/Ossiriandic, Old Noldorin |
| 13 | `ae → ā → ō` | Gnomish |
| 14 | `ao → ā → ō` | Gnomish |
| 17 | `bm → mm → m` | Sindarin |
| 18 | `bm → mb → mm` | Sindarin |
| 19 | `d → ð → z` | Vanyarin |
| 22 | `gj → dj → dʒ` | Vanyarin |
| 23 | `gj → dj → dʒ` | Vanyarin |
| 26 | `kj → tj → tʃ` | Vanyarin |
| 30 | `mm → mb → mm` | Vanyarin, Sindarin |
| 31 | `nn → nd → nn` | Vanyarin, Sindarin |
| 40 | `sg → zg → ðɣ` | Sindarin |
| 41 | `sj → zj → ʒ` | Vanyarin |
| 46 | `tʰt → ttʰ → θθ` | Old Sindarin |
| 48 | `tʰtʰ → ttʰ → θθ` | Old Sindarin |
| 49 | `zm → mm → m` | Sindarin |
| 50 | `ā → ǭ → ā` | Old Sindarin, Telerin |
| 51 | `ā → ǭ → ō` | Old Sindarin |
| 52 | `ā → ǭ → ō` | Old Sindarin, Ilkorin/Doriathrin |
| 53 | `ŋ- → ŋg- → g-` | Ilkorin/Doriathrin |
| 54 | `ŋ- → ŋg- → g-` | Sindarin |
| 55 | `ŋ- → ŋg- → g-` | Telerin |
| 57 | `ŋg- → ŋ- → g-` | Ilkorin/Doriathrin |
| 58 | `ŋg- → ŋ- → ø-` | Telerin |
| 59 | `ŋg- → ŋ- → ø-` | Old Noldorin |
| 60 | `ŋg- → ŋ- → ø-` | Telerin |
| 62 | `ŋgw → mb → mm` | Ancient Telerin, Sindarin |
| 64 | `Vp → Vb → Vv` | Ilkorin/Doriathrin, Danian/Ossiriandic |
| 65 | `Vp → Vb → Vv` | Ilkorin/Doriathrin, Ilkorin/Doriathrin |
| 66 | `Vt → Vd → Vð` | Ilkorin/Doriathrin, Ilkorin/Doriathrin |
| 73 | `g → ɣ → ø` | Old Noldorin |
| 81 | `nd- → d- → l-` | Danian/Ossiriandic |
| 82 | `nd- → d- → l-` | Ilkorin/Doriathrin |
| 86 | `pʰ → ɸ → f` | Old Noldorin |
| 94 | `tʰ → θ → s` | Danian/Ossiriandic |
| 95 | `tʰ → θ → s` | Ilkorin/Doriathrin |

## Совпадающие слова в соседних правилах

Наличие одной и той же ссылки на словарную статью в примерах соседних правил — полезный сигнал для дальнейшего исследования, но не доказательство того, что изменения применялись к одной промежуточной форме.

| ID | Цепочка | Общих ссылок на слова |
|---|---|---:|
| 1 | `pʰt → ptʰ → pt → ɸt` | 13 |
| 2 | `pʰtʰ → ptʰ → pt → ɸt` | 13 |
| 4 | `kʰt → ktʰ → kt → xt` | 6 |
| 5 | `pʰt → ptʰ → pt → ps` | 6 |
| 6 | `pʰt → ptʰ → pt → xt` | 6 |
| 7 | `sb → zb → sp → ps` | 14 |
| 8 | `sg → zg → sk → ks` | 14 |
| 9 | `ŋ → g → ɣ → ø` | 130 |
| 11 | `ɣ → g → ɣ → ø` | 130 |
| 15 | `b → β → v` | 102 |
| 16 | `bd → pt → ɸt` | 10 |
| 18 | `bm → mb → mm` | 3 |
| 20 | `g → ɣ → ø` | 114 |
| 21 | `gd → kt → xt` | 10 |
| 25 | `gt → kt → xt` | 12 |
| 27 | `kn → kt → xt` | 2 |
| 28 | `ktʰ → kt → xt` | 6 |
| 29 | `kʰ → x → h` | 64 |
| 32 | `pm → pw → pp` | 2 |
| 33 | `pn → pt → ɸt` | 2 |
| 34 | `ptʰ → pt → ɸt` | 6 |
| 35 | `pʰ → ɸ → f` | 84 |
| 36 | `pʰt → ptʰ → pt` | 7 |
| 37 | `pʰtʰ → ptʰ → pt` | 7 |
| 39 | `sd → zd → st` | 3 |
| 40 | `sg → zg → ðɣ` | 1 |
| 44 | `tʰ → θ → s` | 89 |
| 45 | `tʰt → ttʰ → tt` | 7 |
| 46 | `tʰt → ttʰ → θθ` | 1 |
| 47 | `tʰtʰ → ttʰ → tt` | 7 |

## Примеры содержательных замечаний

### [Eldamo : Sindarin : [mb], [nd] became [mm], [nn]](https://eldamo.org/content/words/word-868023175.html)

Язык страницы: **Sindarin**. Примеров в секции: **92**. Длина извлечённых пояснений: **16843** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Sindarin and Noldorin, the combinations [mb] and [nd] became [mm] and [nn] medially and (usually) finally, whereas [ŋg] remained medially but became [ŋ] finally . Tolkien described these sound changes in some detail in The Lord of the Rings appendices: In Sindarin the combinations ng, nd, mb , wh…

### [Eldamo : Ancient Quenya : [n], [m] became [t], [w] after voiceless stops and aspirates](https://eldamo.org/content/words/word-3418086257.html)

Язык страницы: **Ancient Quenya**. Примеров в секции: **5**. Длина извлечённых пояснений: **9663** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Ancient Quenya, wherever a nasal n or m appeared after a voiceless stop or aspirate, that nasal was unvoiced with the ultimate result of t (from n ) and w (from m ). If the preceding sound was an aspirate, it simplified to an ordinary voiceless stop. One variation in this process was pm, phm , bo…

### [Eldamo : Quenya : [pt], [kt] became [ɸt], [xt]](https://eldamo.org/content/words/word-2265073101.html)

Язык страницы: **Quenya**. Примеров в секции: **46**. Длина извлечённых пояснений: **9211** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Quenya words with distinct pairs of voiceless stops, the first of the pair became spirantal. In particular, pt, kt > ꝑt, ht [ɸt, xt], and possibly even tk > þk [θk]. To fully understand these sound changes, you need to examine the contexts in which Tolkien conceived of them and how his ideas evol…

### [Eldamo : Ancient Quenya : voiced stops became spirants except after nasals](https://eldamo.org/content/words/word-1141570065.html)

Язык страницы: **Ancient Quenya**. Примеров в секции: **232**. Длина извлечённых пояснений: **8164** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Ancient Quenya, any surviving medial voiced stops usually became voiced spirants, the most notable exception being those appearing after nasals. This sound change also excludes voiced stops that underwent other earlier changes, such as when voiced stops became nasals before nasals . Tolkien descr…

### [Eldamo : Ancient Quenya : [dj] became [lj]](https://eldamo.org/content/words/word-1574644731.html)

Язык страницы: **Ancient Quenya**. Примеров в секции: **1**. Длина извлечённых пояснений: **6600** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Ancient Quenya of the 1950s and 1960s, the combination dy became ly both initially and medially. Tolkien described this change in several places, included the Outline of Phonology (OP2) from the 1950s: In Q * del- seems to have become * led , by dissimilation. The past form [ lende ] clearly show…

### [Eldamo : Quenya : [sp], [sk] became [ps], [ks]](https://eldamo.org/content/words/word-2094898289.html)

Язык страницы: **Quenya**. Примеров в секции: **8**. Длина извлечённых пояснений: **6469** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Quenya the combinations sp, sk were frequently transposed to ps, ks : universally in the case of medial ps , sporadically in other cases. This sound change happened both initially and medially, and the initial transpositions introduced the new initial clusters ps-, ks- to Quenya. Although establi…

### [Eldamo : Quenya : [x] became [h] except before [t]](https://eldamo.org/content/words/word-2071843593.html)

Язык страницы: **Quenya**. Примеров в секции: **49**. Длина извлечённых пояснений: **5781** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Quenya the voiceless velar spirant χ [x] weakened to a simple “breath h ”. This weakening happened first at the beginning of words, in the Parmaquesta [PQ] period. It happened later medially, in the Tarquesta [TQ] period. The only combination where the χ was preserved is ht [xt]. Tolkien gave nea…

### [Eldamo : Ancient Quenya : medial [s] often became [z]](https://eldamo.org/content/words/word-127393503.html)

Язык страницы: **Ancient Quenya**. Примеров в секции: **44**. Длина извлечённых пояснений: **5560** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Ancient Quenya, an s was voiced to z between vowels and before voiced consonants, a change described in both the Outline of Phonetic Development (OP1) from the 1940s and the Outline of Phonology (OP2) from the 1950s. The sound changes in the 1930s were: s . Initially this remained unchanged. Medi…

### [Eldamo : Ancient Quenya : [ns] became [ss]](https://eldamo.org/content/words/word-2591378297.html)

Язык страницы: **Ancient Quenya**. Примеров в секции: **1**. Длина извлечённых пояснений: **5163** символов.

**Начальный фрагмент текста Eldamo (не пересказ):** Текст требует отдельного чтения: In Ancient Quenya [AQ], the combination ns became ss . Since primitive nasals assimilated to n before s , this was the ultimate result of all primitive nasals + s . This sound change was mentioned in both the Outline of Phonetic Development from the 1940s (OP1) and the Outline of Phonology from the …

## Что ещё требуется для настоящего подтверждения

1. Для каждого отдельного ребра зафиксировать контекст (`#`, границы слова, ударение, соседние сегменты) и исключения **по смыслу пояснений**, а не только по словарным ключам.
2. В примерах сопоставлять цепи **одного корня или слова**, сохраняя точные ссылки на исходные и промежуточные формы; наличие разрозненных примеров на обеих страницах недостаточно.
3. Проверить хронологические ограничения, изложенные в заметках, и запретить склейку альтернативных реконструкций.
4. Пересмотреть извлечение из карточек: некоторые правила могут быть связаны с несколькими языками; заголовок страницы — предупреждающий признак, но не окончательный приговор.
5. Строить цепочки с промежуточными значениями **в конкретных словах**, поскольку изменения групп согласных и слогов часто нельзя моделировать заменой отдельных вершин-фонем.

## Сопутствующие файлы

- [`eldamo_rule_commentary_audit.csv`](eldamo_rule_commentary_audit.csv) — полный извлечённый текст пояснений и примеров для каждой страницы правила.
- [`eldamo_paths_context_audit.csv`](eldamo_paths_context_audit.csv) — проверки всех 101 кандидата.
- [`audit_eldamo_paths.py`](audit_eldamo_paths.py) — воспроизводимый анализ локального архива.
