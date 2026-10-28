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

## Частичные когнаты

Связей `<cognate>` Eldamo между ветвями, где у обоих слов известны собственные корни, — 3273; из них 406 связывают слова, совпадающие лишь частью состава (другое число частей или часть с другим корнем; варианты и расширения корня — один корень). При реконструкции такая связь идёт после законов («⇋ частичный когнат») и не служит когнатом составляющей. Список — и в `reports/audit.json`.

| Quenya / Qenya | корни | Sindarin / Noldorin | корни |
|---|---|---|---|
| mq. [(ek)koiru-](https://eldamo.org/content/words/word-3826844773.html) | KOY | ns. [echuiru-](https://eldamo.org/content/words/word-3194870959.html) | ET + KOY |
| eq. [-mas](https://eldamo.org/content/words/word-4022295451.html) | ŊWAÐA | g. [-bar](https://eldamo.org/content/words/word-4219484843.html) | MBARA |
| q. [-ndacil](https://eldamo.org/content/words/word-2846883185.html) | NDAK | s. [dagnir](https://eldamo.org/content/words/word-3651249801.html) | NDAK + N(D)ER |
| eq. [-uran(do)](https://eldamo.org/content/words/word-2628769979.html) | ẆAÐA | g. [-vran](https://eldamo.org/content/words/word-2095208013.html) | MBARA |
| q. [ahtar-](https://eldamo.org/content/words/word-4040996631.html) | AT + KAR | s. [achar-](https://eldamo.org/content/words/word-3800356233.html) | AT/AK |
| eq. [Ainurarda](https://eldamo.org/content/words/word-264598725.html) | AYA¹ + ƷARA | g. [Gar Ainion](https://eldamo.org/content/words/word-1040747741.html) | ƷARA |
| nq. [aipio](https://eldamo.org/content/words/word-2977642327.html) | AYA(N) | ns. [aebin](https://eldamo.org/content/words/word-748013775.html) | AYA(N) + PI(N) |
| eq. [aipio](https://eldamo.org/content/words/word-3246693353.html) | AYA¹ | g. [aibin](https://eldamo.org/content/words/word-1753541311.html) | AYA¹ + PINI |
| nq. [aitalë](https://eldamo.org/content/words/word-2828588435.html) | AYA(N) + LEÑ | ns. [aedaith](https://eldamo.org/content/words/word-1396962581.html) | AYA(N) |
| eq. [Alalminóre](https://eldamo.org/content/words/word-3369572157.html) | ALA² | g. [Gar Lossion](https://eldamo.org/content/words/word-1832325783.html) | ƷARA + LASA |
| mq. [Alataire](https://eldamo.org/content/words/word-579893929.html) | ALAT + AY(AR) | n. [Belegoer](https://eldamo.org/content/words/word-3031818217.html) | BEL + AY(AR) |
| q. [Aldaron](https://eldamo.org/content/words/word-3330088929.html) | GAL²/GALAD | s. [Tauron](https://eldamo.org/content/words/word-1571307721.html) | TAW |
| mq. [Aldaron](https://eldamo.org/content/words/word-1342750465.html) | GALAD | n. [Tauros](https://eldamo.org/content/words/word-1279134665.html) | TAWAR + GOS |
| q. [Aldëa](https://eldamo.org/content/words/word-4158418399.html) | GAL²/GALAD | s. [Orgaladh](https://eldamo.org/content/words/word-3877833613.html) | UR + GALAD/GAL² |
| q. [Aldúya](https://eldamo.org/content/words/word-2566863855.html) | GAL²/GALAD | s. [Orgaladhad](https://eldamo.org/content/words/word-3711271661.html) | UR + GALAD/GAL² |
| mq. [almare](https://eldamo.org/content/words/word-3642303261.html) | GAL² | ns. [alvar](https://eldamo.org/content/words/word-1958490523.html) | AL(A) |
| mq. [Alqalonde](https://eldamo.org/content/words/word-1426618143.html) | (A)LAK + LOD | n. [Airlond](https://eldamo.org/content/words/word-209367293.html) | AY(AR) + LOD |
| mq. [Alqalonde](https://eldamo.org/content/words/word-1426618143.html) | (A)LAK + LOD | n. [Alfobas](https://eldamo.org/content/words/word-2923452283.html) | (A)LAK + KHOP |
| mq. [Ambarenya](https://eldamo.org/content/words/word-3060759673.html) | MBAR + (E)NED | n. [Emerin](https://eldamo.org/content/words/word-1624961797.html) | MBAR |
| mq. [ambaróne](https://eldamo.org/content/words/word-2279418957.html) | AM² | n. [amrûn](https://eldamo.org/content/words/word-1393854111.html) | AM² + RŌ/ORO |
| eq. [amunte](https://eldamo.org/content/words/word-75910897.html) | AM(U) | g. [am(b)ros(t)](https://eldamo.org/content/words/word-86207405.html) | AM(U) + ORO¹ |
| q. [Anarya](https://eldamo.org/content/words/word-2057863699.html) | NAR | s. [Oranor](https://eldamo.org/content/words/word-2747078041.html) | UR + NAR |
| q. [andamacil](https://eldamo.org/content/words/word-3003776961.html) | ANAD + MAK | s. [megil](https://eldamo.org/content/words/word-3519182345.html) | MAK |
| mq. [andatehta](https://eldamo.org/content/words/word-1162045267.html) | ANAD + TEK | on. [andatektha](https://eldamo.org/content/words/word-1414572133.html) | TEK |
| q. [ando](https://eldamo.org/content/words/word-3071385603.html) | NA/ANA | ns. [and](https://eldamo.org/content/words/word-1779573821.html) | AD |
| eq. [Angamandi](https://eldamo.org/content/words/word-2518754235.html) | M(B)ṆÐṆ | n. [Angband](https://eldamo.org/content/words/word-251244905.html) | ANGA + (M)BAD |
| nq. [angwenda](https://eldamo.org/content/words/word-745700083.html) | WED | n. [angwedh](https://eldamo.org/content/words/word-204930385.html) | ANGA + WED |
| q. [aquet-](https://eldamo.org/content/words/word-418923719.html) | AT | s. [aphed-](https://eldamo.org/content/words/word-1429737613.html) | AT + KWET |
| mq. [Ar Ulmon](https://eldamo.org/content/words/word-3098226659.html) | AR¹ + ULU | n. [Ar Uiar](https://eldamo.org/content/words/word-200969175.html) | AR¹ + WAY |
| q. [Aracorno](https://eldamo.org/content/words/word-1841825405.html) | RĀ/ARA | s. [Aragorn](https://eldamo.org/content/words/word-1838387211.html) | RĀ/ARA/ARAN + ÑGOR |
| q. [Arafinwë](https://eldamo.org/content/words/word-581344607.html) | RĀ/ARA + PHIN¹ + WĒ/EWE/WEG | s. [Finarfin](https://eldamo.org/content/words/word-765105705.html) | RĀ/ARA/ARAN |
| nq. [arcólima](https://eldamo.org/content/words/word-835585535.html) | ÑAR/AD(A) + KOL | ns. [asgolui](https://eldamo.org/content/words/word-3202643599.html) | AS² + KOL |
| eq. [Ardalomba](https://eldamo.org/content/words/word-171490717.html) | ƷARA + LOMO | g. [Gar Thurion](https://eldamo.org/content/words/word-3089350247.html) | ƷARA + FURU |
| mq. [Are Veruen](https://eldamo.org/content/words/word-1387031007.html) | AR¹ + BES | n. [Ar Vedhwen](https://eldamo.org/content/words/word-3411503153.html) | AR¹ + BED |
| q. [Arfanyarassë](https://eldamo.org/content/words/word-4285013399.html) | RĀ/ARA + PHAN + RAS | s. [Ras-Arphain](https://eldamo.org/content/words/word-239358129.html) | RAS + RĀ/ARA/ARAN + PHAN |
| mq. [Arkimbele](https://eldamo.org/content/words/word-350888851.html) | AK + IMBE | n. [Imladris(t)](https://eldamo.org/content/words/word-1743585985.html) | IMBE + LAT + RIS |
| q. [armaro](https://eldamo.org/content/words/word-3491333723.html) | ÑAR/AD(A) + MBAR | s. [sammar](https://eldamo.org/content/words/word-15708095.html) | MBAR |
| q. [Artafindë](https://eldamo.org/content/words/word-2366938049.html) | ARAT/RĀ/ARA/RAT² + SPIN(ID) | s. [Finrod](https://eldamo.org/content/words/word-2455993469.html) | SPIN(ID) + ARAT/RĀ/ARA/RAT² |
| q. [Artaresto](https://eldamo.org/content/words/word-2018176983.html) | ARAT/RĀ/ARA/RAT² | s. [Orodreth](https://eldamo.org/content/words/word-2927154629.html) | OROT/RŌ/ORO + RET |
| mq. [Aryante](https://eldamo.org/content/words/word-3346981929.html) | AR¹ + YAN²/NĀ¹/ANA¹ | n. [Eriant](https://eldamo.org/content/words/word-2630695093.html) | NĀ¹/ANA¹/AR¹ |
| eq. [aryúlima](https://eldamo.org/content/words/word-1051868245.html) | ƷARA + DYULU | g. [argulthion](https://eldamo.org/content/words/word-670684409.html) | ASA + DYULU |
| q. [asëa aranion](https://eldamo.org/content/words/word-973501211.html) | THĀ/ATHA + RĀ/ARA/ARAN | s. [athelas](https://eldamo.org/content/words/word-2311050181.html) | THĀ/ATHA + LAS¹ |
| q. [atto](https://eldamo.org/content/words/word-3038134979.html) | AT(AR) | s. [atheg](https://eldamo.org/content/words/word-4001305417.html) | AT(AR) + NIK |
| mq. [avanóte](https://eldamo.org/content/words/word-3886145639.html) | AWA + NOT | n. [arnediad](https://eldamo.org/content/words/word-3633835439.html) | AR² + NOT |
| q. [ca(na)sta](https://eldamo.org/content/words/word-414348905.html) | KANAT + SAT | s. [canath](https://eldamo.org/content/words/word-1995696881.html) | KANAT |
| nq. [calaina](https://eldamo.org/content/words/word-2472361915.html) | KAL | ns. [glaen](https://eldamo.org/content/words/word-2807387561.html) | GALAN |
| nq. [calainë](https://eldamo.org/content/words/word-3088746799.html) | KAL | ns. [glaenas](https://eldamo.org/content/words/word-685015863.html) | GALAN |
| q. [cilintilla](https://eldamo.org/content/words/word-1100144729.html) | TIR | s. [cenedril](https://eldamo.org/content/words/word-1385399405.html) | KEN + MBIRIL |
| nq. [ciryacarmen](https://eldamo.org/content/words/word-2954751005.html) | KIR + KAR + MEN | ns. [cirgarvas](https://eldamo.org/content/words/word-3871645685.html) | KIR + KAR |
| q. [coimas](https://eldamo.org/content/words/word-1906633975.html) | KOY + MBAS | s. [lembas](https://eldamo.org/content/words/word-3025263089.html) | LED + MBAS |
| nq. [cuita-](https://eldamo.org/content/words/word-2238228617.html) | KUY | ns. [echuida-](https://eldamo.org/content/words/word-1544162837.html) | ET + KUY |
| q. [Cuiviénen](https://eldamo.org/content/words/word-3051814975.html) | KUY + NEN | s. [Nen Echui](https://eldamo.org/content/words/word-2157324901.html) | NEN + KUY |
| q. [culumalda](https://eldamo.org/content/words/word-2090608941.html) | KUL + GAL²/GALAD | ns. [collorn](https://eldamo.org/content/words/word-3732406313.html) | KUL + RŌ/ORO |
| q. [Curufinwë](https://eldamo.org/content/words/word-1796517717.html) | KUR + PHIN¹ + WĒ/EWE/WEG | s. [Curufin](https://eldamo.org/content/words/word-958563403.html) | KUR |
| q. [Curumo](https://eldamo.org/content/words/word-697388925.html) | KUR | s. [Curunír](https://eldamo.org/content/words/word-2938968655.html) | KUR + N(D)ER |
| eq. [Eanosse](https://eldamo.org/content/words/word-1095242903.html) | NŌ | g. [Thornhoth](https://eldamo.org/content/words/word-1383799173.html) | ÞORO + HOSO |
| eq. [Easindi](https://eldamo.org/content/words/word-345094589.html) | SIÐI | g. [Thorn Sir](https://eldamo.org/content/words/word-711855987.html) | ÞORO + SIÐI |
| eq. [Eldalie](https://eldamo.org/content/words/word-1263240023.html) | LĪ | g. [Eglothrim](https://eldamo.org/content/words/word-640414111.html) | EÐE¹ |
| q. [Eldalótë](https://eldamo.org/content/words/word-3465788703.html) | EL + LOT(H) | s. [Edhellos](https://eldamo.org/content/words/word-2246643897.html) | DEL²/DEL¹ + LOT(H) |
| eq. [Eldamar](https://eldamo.org/content/words/word-2091931097.html) | MBARA | g. [Eglamar](https://eldamo.org/content/words/word-1027427819.html) | EÐE¹ |
| mq. [Elentári](https://eldamo.org/content/words/word-1620801097.html) | EL | n. [Elbereth](https://eldamo.org/content/words/word-2462581423.html) | EL + BARATH |
| q. [Elentári](https://eldamo.org/content/words/word-1674375635.html) | EL + TĀ/TAƷ | s. [Elbereth](https://eldamo.org/content/words/word-862238445.html) | EL + BER/BARATH |
| q. [Elenya](https://eldamo.org/content/words/word-2372957001.html) | EL | s. [Orgilion](https://eldamo.org/content/words/word-2411056289.html) | UR + (Ñ)GIL |
| eq. [Elmavoite](https://eldamo.org/content/words/word-4001535895.html) | MAHA | g. [Ermabwed](https://eldamo.org/content/words/word-2491978325.html) | MAPA |
| q. [emmë²](https://eldamo.org/content/words/word-3989317599.html) | AM¹ | s. [emig](https://eldamo.org/content/words/word-2157771091.html) | AM¹ + NIK |
| mq. [Ender](https://eldamo.org/content/words/word-1010607107.html) | E + (N)DER | n. [Enner](https://eldamo.org/content/words/word-4004491335.html) | (N)DER |
| q. [Endórë](https://eldamo.org/content/words/word-82428757.html) | ENED + NDOR/NŌ/ONO/DOR | s. [Ennorath](https://eldamo.org/content/words/word-322794511.html) | ENED + NDOR/DOR + SAT/ATATA |
| mq. [entas(se)](https://eldamo.org/content/words/word-599793627.html) | EN + TA | s. [ennas](https://eldamo.org/content/words/word-433074759.html) | EN |
| eq. [ere(n)](https://eldamo.org/content/words/word-645838561.html) | EÐE¹ | g. [ger](https://eldamo.org/content/words/word-1160596121.html) | YERE(NE) |
| mq. [Erlaire](https://eldamo.org/content/words/word-1763934265.html) | ER + LAY | n. [Ebloer](https://eldamo.org/content/words/word-2467242993.html) | LAY |
| nq. [etelelya-](https://eldamo.org/content/words/word-2104085107.html) | ET + LED | ns. [edledhia-](https://eldamo.org/content/words/word-1230357767.html) | ET |
| q. [Eärenya](https://eldamo.org/content/words/word-3684301635.html) | AY(AR)/GAY(AR) | s. [Oraeron](https://eldamo.org/content/words/word-1920796469.html) | UR + AY(AR)/GAY(AR) |
| q. [Falmari](https://eldamo.org/content/words/word-1741739599.html) | PHAL | s. [Falathrim](https://eldamo.org/content/words/word-3766094569.html) | PHAL + RIM |
| eq. [Falqalaure](https://eldamo.org/content/words/word-1547870747.html) | FḶKḶ + LOURI | g. [Glorfalc](https://eldamo.org/content/words/word-229546411.html) | LOURI |
| eq. [Faskala-númen](https://eldamo.org/content/words/word-2277218847.html) | FASA + NUHU | g. [Fôs’Almir](https://eldamo.org/content/words/word-1101408029.html) | FASA |
| eq. [Fatanyu](https://eldamo.org/content/words/word-3469303167.html) | FAGA + TANA | g. [Inthanfog](https://eldamo.org/content/words/word-1025243023.html) | IÐI + TANA + FAGA |
| eq. [Favilna](https://eldamo.org/content/words/word-3275870891.html) | FAGA + VILI | g. [Gwilfa](https://eldamo.org/content/words/word-1334041635.html) | GWILI¹ + FAGA |
| q. [findelë](https://eldamo.org/content/words/word-2098180505.html) | SPIN(ID) + LEÑ | s. [finnel](https://eldamo.org/content/words/word-3954224561.html) | SPIN(ID)/DEL³/DEL² |
| q. [findilë](https://eldamo.org/content/words/word-1897959611.html) | SPIN(ID) + LEÑ | s. [finnel](https://eldamo.org/content/words/word-3954224561.html) | SPIN(ID)/DEL³/DEL² |
| mq. [Finwe](https://eldamo.org/content/words/word-162072507.html) | PHIN/WEG | on. [Phinwe](https://eldamo.org/content/words/word-2340576295.html) | PHIN + WEG |
| eq. [Firilanda](https://eldamo.org/content/words/word-1902693721.html) | FIÐI + LAÐA | g. [Faiglindra](https://eldamo.org/content/words/word-2043468335.html) | FIÐI |
| eq. [Firin Nautaron](https://eldamo.org/content/words/word-706126489.html) | FIRIŊI + NAWA | g. [Nauglafring](https://eldamo.org/content/words/word-3063461747.html) | NAWA |
| q. [Follondië](https://eldamo.org/content/words/word-181917289.html) | PHOR + MEN + LON¹ | s. [Forlonnas](https://eldamo.org/content/words/word-1663864747.html) | PHOR + LON¹ |
| mq. [formaite](https://eldamo.org/content/words/word-1591423211.html) | PHOR + MAƷ | n. [forgam](https://eldamo.org/content/words/word-2973536205.html) | PHOR + KAB¹ |
| q. [formen](https://eldamo.org/content/words/word-1223050479.html) | PHOR + MEN | s. [for-](https://eldamo.org/content/words/word-470347903.html) | PHOR |
| q. [formen](https://eldamo.org/content/words/word-1223050479.html) | PHOR + MEN | s. [forn](https://eldamo.org/content/words/word-196480175.html) | PHOR |
| q. [formen](https://eldamo.org/content/words/word-1223050479.html) | PHOR + MEN | s. [forod](https://eldamo.org/content/words/word-348549421.html) | PHOR |
| mq. [formen](https://eldamo.org/content/words/word-1941703795.html) | PHOR + MEN | n. [forod](https://eldamo.org/content/words/word-2901190421.html) | PHOR |
| mq. [formenya](https://eldamo.org/content/words/word-693868109.html) | PHOR + MEN | n. [forodren](https://eldamo.org/content/words/word-1896446041.html) | PHOR |
| eq. [fuiyáru](https://eldamo.org/content/words/word-305812215.html) | ǶUẎU + YAÐA | g. [fuior](https://eldamo.org/content/words/word-2470625983.html) | ǶUẎU |
| eq. [fumella](https://eldamo.org/content/words/word-2288213181.html) | FUMU | g. [hum(i)los](https://eldamo.org/content/words/word-2738177801.html) | FUMU + LASA |
| q. [Fírima](https://eldamo.org/content/words/word-3903080649.html) | PHIR | s. [Fíreb](https://eldamo.org/content/words/word-654277655.html) | PHIR + KWA |
| q. [hanno](https://eldamo.org/content/words/word-3573771469.html) | KHAN¹ | s. [honeg](https://eldamo.org/content/words/word-3521663585.html) | KHAN¹ + NIK |
| eq. [Haranoldor](https://eldamo.org/content/words/word-579525141.html) | HAÐA + ŊOLO | g. [Hangoltha](https://eldamo.org/content/words/word-2802730461.html) | ŊOLO |
| eq. [Harwalin](https://eldamo.org/content/words/word-4004526593.html) | HAÐA | g. [Hathwalin](https://eldamo.org/content/words/word-1125488343.html) | ASA |
| q. [Hecel](https://eldamo.org/content/words/word-1061119547.html) | HEK + EL | s. [Eglan](https://eldamo.org/content/words/word-3564176873.html) | HEK |
| q. [Hecelmar](https://eldamo.org/content/words/word-4160434121.html) | HEK + EL + MBAR | s. [Eglamar](https://eldamo.org/content/words/word-416654487.html) | HEK + MBAR |
| q. [hendumaica](https://eldamo.org/content/words/word-3594741895.html) | KHEN + MIK | s. [maecheneb](https://eldamo.org/content/words/word-2615875029.html) | MIK + KHEN + KWA |
| q. [Hildor](https://eldamo.org/content/words/word-973681123.html) | KHIL | s. [Aphadon](https://eldamo.org/content/words/word-2014524399.html) | PĀ/APA + PAT |
| mq. [Hisilóme](https://eldamo.org/content/words/word-957167483.html) | KHITH + DOƷ/DOM | n. [Hithlum](https://eldamo.org/content/words/word-3195854661.html) | KHITH + LUM |
| eq. [huiva](https://eldamo.org/content/words/word-443071601.html) | ǶUẎU | g. [fuin¹](https://eldamo.org/content/words/word-3186890695.html) | FOƷO |
| eq. [huiva](https://eldamo.org/content/words/word-443071601.html) | ǶUẎU | g. [huith](https://eldamo.org/content/words/word-1825445067.html) | HUYU |
| eq. [hunda](https://eldamo.org/content/words/word-3337406073.html) | HUNU | g. [haug](https://eldamo.org/content/words/word-678502043.html) | HAWA |
| mq. [hyarmaite](https://eldamo.org/content/words/word-33971947.html) | KHYAR + MAƷ | n. [hargam](https://eldamo.org/content/words/word-38262983.html) | KHYAR + KAB¹ |
| mq. [hyarmen](https://eldamo.org/content/words/word-4037811261.html) | KHYAR + MEN | n. [harad](https://eldamo.org/content/words/word-3167605685.html) | KHYAR |
| q. [hyarmen](https://eldamo.org/content/words/word-1477365621.html) | KHYAR + MEN | s. [harad](https://eldamo.org/content/words/word-614934925.html) | KHYAR |
| q. [hyarmen](https://eldamo.org/content/words/word-1477365621.html) | KHYAR + MEN | s. [harn](https://eldamo.org/content/words/word-3643936511.html) | KHYAR |
| mq. [hyarmenya](https://eldamo.org/content/words/word-3120569907.html) | KHYAR + MEN | n. [haradren](https://eldamo.org/content/words/word-547004985.html) | KHYAR |
| mq. [hyarmenya](https://eldamo.org/content/words/word-3120569907.html) | KHYAR + MEN | n. [harn¹](https://eldamo.org/content/words/word-1604891939.html) | KHYAR |
| q. [Hísilómë](https://eldamo.org/content/words/word-722082651.html) | KHITH + DOM | norths. [Hithlum](https://eldamo.org/content/words/word-4278131439.html) | KHITH |
| mq. [Ialasse](https://eldamo.org/content/words/word-1475714559.html) | GEY + GOLOS | n. [Amon Uilos](https://eldamo.org/content/words/word-1347868551.html) | AM² + OY¹ + GOLOS |
| mq. [Ilmen](https://eldamo.org/content/words/word-813117283.html) | GIL + MEN | n. [gilith](https://eldamo.org/content/words/word-3232357743.html) | GIL |
| eq. [Ilqingi](https://eldamo.org/content/words/word-1017709795.html) | ILU + QINGI | g. [Thlim Quing Ilon](https://eldamo.org/content/words/word-3083357639.html) | QINGI + ILU |
| eq. [Ilsalunte](https://eldamo.org/content/words/word-114999551.html) | GILI + LUTU | g. [Gilthalont](https://eldamo.org/content/words/word-309647451.html) | GILI |
| eq. [ilwe](https://eldamo.org/content/words/word-2602100613.html) | ILU | g. [ilwint](https://eldamo.org/content/words/word-4050223721.html) | ILU + DYĒ¹ |
| eq. [ilweran(ta)](https://eldamo.org/content/words/word-2088169047.html) | ILU | g. [ilbrant](https://eldamo.org/content/words/word-1974422035.html) | ILU + RAÞA |
| eq. [Ilwerantelimba](https://eldamo.org/content/words/word-3569300061.html) | ILU + TELE | g. [Cris Ilbranteloth](https://eldamo.org/content/words/word-4029390255.html) | KIRISI + ILU + RAÞA + TELE |
| eq. [Ilúvatar](https://eldamo.org/content/words/word-1025766261.html) | ILU + ATA² | g. [Ilathon](https://eldamo.org/content/words/word-3895315785.html) | ILU |
| eq. [Indorildo](https://eldamo.org/content/words/word-3154842763.html) | IÐI | g. [Gon Indor](https://eldamo.org/content/words/word-1649916365.html) | YO(NO) + IÐI |
| eq. [Indorion](https://eldamo.org/content/words/word-1742284209.html) | IÐI + YO(NO) | g. [Gon Indor](https://eldamo.org/content/words/word-1649916365.html) | YO(NO) + IÐI |
| eq. [Indorion](https://eldamo.org/content/words/word-1742284209.html) | IÐI + YO(NO) | g. [Indorild](https://eldamo.org/content/words/word-4193360425.html) | IÐI |
| eq. [Inwe](https://eldamo.org/content/words/word-2665752009.html) | INI | g. [Githil](https://eldamo.org/content/words/word-1584244623.html) | IÞI |
| mq. [Iolosse](https://eldamo.org/content/words/word-2658845979.html) | GEY + GOLOS | n. [Uilos](https://eldamo.org/content/words/word-3242611079.html) | OY¹ + GOLOS |
| q. [Irildë](https://eldamo.org/content/words/word-1014879975.html) | ID + RIL | s. [Idril](https://eldamo.org/content/words/word-1971690885.html) | IT² + RIL |
| eq. [Irmaldi](https://eldamo.org/content/words/word-4147248425.html) | IÐI + MBARA | g. [Isbaroth](https://eldamo.org/content/words/word-370278861.html) | IÐI |
| eq. [Isil Inwe](https://eldamo.org/content/words/word-1971233455.html) | IÞI + INI | g. [Gim Githil](https://eldamo.org/content/words/word-2258946005.html) | IÞI |
| eq. [Isil Inwe](https://eldamo.org/content/words/word-1971233455.html) | IÞI + INI | g. [Inwithiel](https://eldamo.org/content/words/word-4070885791.html) | IÞI |
| eq. [Isilmo](https://eldamo.org/content/words/word-1800310493.html) | IÞI | g. [Gilweth](https://eldamo.org/content/words/word-93555561.html) | GILI |
| q. [Isilya](https://eldamo.org/content/words/word-2691220853.html) | THIL/SIL | s. [Orithil](https://eldamo.org/content/words/word-1293734281.html) | UR + THIL |
| eq. [Itselokte](https://eldamo.org/content/words/word-3051931427.html) | ITI¹ + LOHO | g. [Sithaloth](https://eldamo.org/content/words/word-465515769.html) | ITI¹ |
| mq. [kala](https://eldamo.org/content/words/word-2045968979.html) | KAL | n. [glaw](https://eldamo.org/content/words/word-679411941.html) | GAL¹ |
| mq. [Kalaqendi](https://eldamo.org/content/words/word-4059804511.html) | KAL + KWEN(ED) | n. [Caleledh](https://eldamo.org/content/words/word-3808421865.html) | KAL + ELED |
| eq. [Kapalindar](https://eldamo.org/content/words/word-315857363.html) | KAPA | g. [Thlim Ecthel](https://eldamo.org/content/words/word-566528661.html) | KELE |
| eq. [kektele](https://eldamo.org/content/words/word-375049023.html) | KEKE¹ + KELE | g. [caithl](https://eldamo.org/content/words/word-63755801.html) | KEKE¹ |
| eq. [Kiris Iluqingatelda](https://eldamo.org/content/words/word-2629812959.html) | KIRISI + ILU + QINGI + TELE | g. [Cris a Teld Quing Ilon](https://eldamo.org/content/words/word-2203118881.html) | KIRISI + TELE + QINGI + ILU |
| eq. [Kiris Iluqingatelda](https://eldamo.org/content/words/word-2629812959.html) | KIRISI + ILU + QINGI + TELE | g. [Cris Ilbranteloth](https://eldamo.org/content/words/word-4029390255.html) | KIRISI + ILU + RAÞA + TELE |
| eq. [koivie](https://eldamo.org/content/words/word-3072247457.html) | KOẎO | g. [cwivros](https://eldamo.org/content/words/word-1693621209.html) | QIVI |
| eq. [Koivie-néni](https://eldamo.org/content/words/word-2336248949.html) | KOẎO + NENE/NEÐE | g. [Nenin a Gwivros](https://eldamo.org/content/words/word-2227197955.html) | QIVI |
| eq. [Kor(o)mas](https://eldamo.org/content/words/word-1477624403.html) | KOÐO/KORO + ŊWAÐA | g. [Corangos](https://eldamo.org/content/words/word-22684497.html) | KORO |
| eq. [korda](https://eldamo.org/content/words/word-4097569447.html) | KOÐO | g. [gorthin](https://eldamo.org/content/words/word-901782463.html) | KOÐO + IÐI |
| eq. [Korosintl](https://eldamo.org/content/words/word-3902412591.html) | KORO + SṆTYṆ | g. [Glincrost](https://eldamo.org/content/words/word-682676019.html) | GILI |
| eq. [Korosintl](https://eldamo.org/content/words/word-3902412591.html) | KORO + SṆTYṆ | g. [Silgrost](https://eldamo.org/content/words/word-2499424803.html) | SILI |
| eq. [Kortirion](https://eldamo.org/content/words/word-2015993001.html) | KOÐO/KORO | g. [Mindon Gwar](https://eldamo.org/content/words/word-404487345.html) | MINI² + KORO |
| mq. [Kuiviénen](https://eldamo.org/content/words/word-1992454893.html) | KUY + NEN | n. [Nen Echui](https://eldamo.org/content/words/word-2492358511.html) | NEN + KUY |
| eq. [Kulullin](https://eldamo.org/content/words/word-265060195.html) | KULU | g. [Glingol](https://eldamo.org/content/words/word-535254837.html) | LIÐI |
| q. [Laicolassë](https://eldamo.org/content/words/word-606009255.html) | LAY + WO + LAS¹ | s. [Laegolas](https://eldamo.org/content/words/word-2829562391.html) | LAY + LAS¹ |
| mq. [Laiqendi](https://eldamo.org/content/words/word-3504382853.html) | LAYAK + KWEN(ED) | n. [Lhoebelidh](https://eldamo.org/content/words/word-2327265133.html) | LAYAK + ELED |
| q. [Laiquendi](https://eldamo.org/content/words/word-2278613393.html) | LAY + KWENED/KWEN | s. [Laegel](https://eldamo.org/content/words/word-4039322215.html) | LAY + EL |
| nq. [lambengolmë](https://eldamo.org/content/words/word-3717970713.html) | LAB + ÑGOL¹ | ns. [tengolu](https://eldamo.org/content/words/word-2269932581.html) | TEÑ + ÑGOL¹ |
| nq. [lantasírë](https://eldamo.org/content/words/word-631141049.html) | DAT + SIR | s. [lanthir](https://eldamo.org/content/words/word-38852241.html) | LAT² + SIR |
| eq. [lasselanta](https://eldamo.org/content/words/word-3827710257.html) | LASA | g. [dodri·lassion](https://eldamo.org/content/words/word-4292474033.html) | ÐOTO + LASA |
| eq. [lasselanta](https://eldamo.org/content/words/word-3827710257.html) | LASA | g. [lasgweloth](https://eldamo.org/content/words/word-604262837.html) | LASA + QELE |
| mq. [lasselanta](https://eldamo.org/content/words/word-1133217505.html) | LAS¹ + DAT | n. [lhasbelin](https://eldamo.org/content/words/word-2663522623.html) | LAS¹ + KWEL |
| mq. [latimbe](https://eldamo.org/content/words/word-438531623.html) | LAT + IMBE | n. [imlad](https://eldamo.org/content/words/word-2322924899.html) | IMBE + LAT |
| mq. [Latimberista](https://eldamo.org/content/words/word-3379797225.html) | LAT + IMBE + RIS | n. [Imladris(t)](https://eldamo.org/content/words/word-1743585985.html) | IMBE + LAT + RIS |
| q. [Laurefindele](https://eldamo.org/content/words/word-2695763285.html) | (G)LAWAR + SPIN(ID) + LEÑ | s. [Glorfindel](https://eldamo.org/content/words/word-955430001.html) | (G)LAWAR + SPIN(ID)/DEL³/DEL² |
| mq. [Laurelin](https://eldamo.org/content/words/word-4150253729.html) | (G)LAWAR + LIN² | n. [Glingal](https://eldamo.org/content/words/word-3426206997.html) | KAL/(G)LINGI |
| eq. [Laurelin](https://eldamo.org/content/words/word-1049482055.html) | LOURI + LIÐI | g. [Glingol](https://eldamo.org/content/words/word-535254837.html) | LIÐI |
| q. [Laurenandë](https://eldamo.org/content/words/word-3123790563.html) | (G)LAWAR + NAD | s. [Nan Laur](https://eldamo.org/content/words/word-566518141.html) | NAD + (G)LAWAR |
| eq. [Laurifindl](https://eldamo.org/content/words/word-403361769.html) | LOURI + FIÐI | g. [Glorfindel](https://eldamo.org/content/words/word-3017204161.html) | LOURI |
| q. [lenda](https://eldamo.org/content/words/word-117252621.html) | LEN | ns. [lîdh](https://eldamo.org/content/words/word-2314795499.html) | LED |
| q. [lepetta](https://eldamo.org/content/words/word-723386541.html) | LEP | s. [lebethron](https://eldamo.org/content/words/word-1323679033.html) | LEP + RŌ/ORO |
| q. [lepincë](https://eldamo.org/content/words/word-2996056243.html) | NIK | s. [lebig](https://eldamo.org/content/words/word-271980991.html) | LEP + NIK |
| eq. [lielesta](https://eldamo.org/content/words/word-3673796407.html) | LĪ + LESE | g. [lieglest](https://eldamo.org/content/words/word-564287273.html) | LĪ |
| q. [Linda](https://eldamo.org/content/words/word-828529721.html) | LIN² | s. [Glinnel](https://eldamo.org/content/words/word-3454641215.html) | LIN² + EL |
| q. [Linda](https://eldamo.org/content/words/word-828529721.html) | LIN² | s. [Lindel](https://eldamo.org/content/words/word-1347956775.html) | LIN² + EL |
| eq. [Lindelokte](https://eldamo.org/content/words/word-3675566739.html) | LIÐI + LOHO | g. [Liriluith](https://eldamo.org/content/words/word-2703967387.html) | LIÐI |
| eq. [lotella](https://eldamo.org/content/words/word-1963827653.html) | LOHO | g. [lothli](https://eldamo.org/content/words/word-649347729.html) | LASA |
| q. [luimë](https://eldamo.org/content/words/word-724828905.html) | DUY | s. [duinen](https://eldamo.org/content/words/word-3620266967.html) | DUY + NEN |
| eq. [Lumbi](https://eldamo.org/content/words/word-690952759.html) | LUVU | g. [Lumfod](https://eldamo.org/content/words/word-4286051227.html) | LUVU + FOTO |
| q. [Lungumá](https://eldamo.org/content/words/word-1545404097.html) | LUG¹ + MAH/MAG | s. [Mablung](https://eldamo.org/content/words/word-968299449.html) | MAP + LUG¹ |
| mq. [Lunoronti](https://eldamo.org/content/words/word-732386425.html) | LUG² + OROT | n. [Eredluin](https://eldamo.org/content/words/word-112116643.html) | OROT + LUG² |
| q. [Lóminórë](https://eldamo.org/content/words/word-4246080601.html) | LAM + NDOR/NŌ/ONO/DOR | norths. [Dor-lómin](https://eldamo.org/content/words/word-2639772321.html) | NDOR/DOR + LAM |
| eq. [Lóter Kuluinai](https://eldamo.org/content/words/word-521563091.html) | LOHO + KULU | g. [Thlim Losglóriol](https://eldamo.org/content/words/word-640862931.html) | LASA + LOURI |
| mq. [lúmeqentale](https://eldamo.org/content/words/word-1279360761.html) | LU + KWET | n. [gobennas](https://eldamo.org/content/words/word-2527132803.html) | WO + KWET |
| q. [lúna](https://eldamo.org/content/words/word-3513692377.html) | DU | s. [dûr](https://eldamo.org/content/words/word-3265511325.html) | NDU |
| q. [Lúnaturco](https://eldamo.org/content/words/word-381444979.html) | DU + TURUK | s. [Barad-dûr](https://eldamo.org/content/words/word-3236058797.html) | M(B)ARAT/BARAT + NDU |
| q. [Macalaurë](https://eldamo.org/content/words/word-3920818985.html) | MAK + (G)LAWAR | s. [Maglor](https://eldamo.org/content/words/word-231356007.html) | (G)LAWAR |
| mq. [Malarauko](https://eldamo.org/content/words/word-2698648895.html) | RUK¹ | n. [Balrog](https://eldamo.org/content/words/word-1815072641.html) | (Ñ)GWAL + RUK¹ |
| eq. [Malkamekte](https://eldamo.org/content/words/word-4132618141.html) | MBALA + MEKE | g. [Balcmeg](https://eldamo.org/content/words/word-1244455891.html) | MBALA |
| mq. [mallo](https://eldamo.org/content/words/word-3026611147.html) | MA | ns. [oman](https://eldamo.org/content/words/word-1842304361.html) | WĀ/AWA + MA |
| nq. [maltalos](https://eldamo.org/content/words/word-1989135729.html) | MALAT + LOT(H) | ns. [malthos](https://eldamo.org/content/words/word-1440238687.html) | MALAT |
| nq. [manan](https://eldamo.org/content/words/word-461879787.html) | MA | ns. [amman](https://eldamo.org/content/words/word-1290286793.html) | NA/ANA + MA |
| q. [manen](https://eldamo.org/content/words/word-1385064761.html) | MA | ns. [naman](https://eldamo.org/content/words/word-2533857839.html) | NA/ANA + MA |
| mq. [manna](https://eldamo.org/content/words/word-2128066727.html) | MA | ns. [navan](https://eldamo.org/content/words/word-3696525989.html) | NA/ANA + MA |
| q. [Manwë](https://eldamo.org/content/words/word-4066965383.html) | MAN + WĒ/EWE/WEG | s. [Manwe](https://eldamo.org/content/words/word-431387957.html) | WĒ/EWE/WEG |
| eq. [mapa-](https://eldamo.org/content/words/word-2750052825.html) | MAPA | g. [nab-](https://eldamo.org/content/words/word-1775993711.html) | NAPA |
| eq. [mapalin](https://eldamo.org/content/words/word-3598304457.html) | MAHA + PALA | g. [mavlantos](https://eldamo.org/content/words/word-1727798533.html) | PALA |
| q. [maquet-](https://eldamo.org/content/words/word-646169841.html) | KWET | ns. [mabed-](https://eldamo.org/content/words/word-3651362727.html) | MA + KWET |
| eq. [marikta](https://eldamo.org/content/words/word-1646845611.html) | RIKI | g. [mabrin(d)](https://eldamo.org/content/words/word-1468697225.html) | MAPA + RIKI |
| mq. [masse¹](https://eldamo.org/content/words/word-4164950807.html) | MA | ns. [mivan](https://eldamo.org/content/words/word-2082970245.html) | MI/IMI + MA |
| q. [massánië](https://eldamo.org/content/words/word-3839826717.html) | MBAS + NA/ANA/AMA | s. [besain](https://eldamo.org/content/words/word-2731883551.html) | MBAS |
| eq. [mastakorne](https://eldamo.org/content/words/word-436084681.html) | M(B)ASA + KORO | g. [basgorn](https://eldamo.org/content/words/word-2135527795.html) | M(B)ASA |
| q. [Melkor](https://eldamo.org/content/words/word-3020346411.html) | MBELEK | s. [Belegûr](https://eldamo.org/content/words/word-2545919425.html) | MBELEK + RŌ/ORO |
| q. [menel](https://eldamo.org/content/words/word-1335823119.html) | MENEL | s. [menel](https://eldamo.org/content/words/word-314754767.html) | MEN + EL |
| q. [Menelmacar](https://eldamo.org/content/words/word-2064169923.html) | MENEL + MAK | s. [Menelvagor](https://eldamo.org/content/words/word-1859337157.html) | MEN + EL + MAK |
| q. [Menelya](https://eldamo.org/content/words/word-1939890385.html) | MENEL | s. [Ormenel](https://eldamo.org/content/words/word-1266406213.html) | UR + MEN + EL |
| eq. [Meril-i-Turinqi](https://eldamo.org/content/words/word-112046301.html) | ŊWEĐE + I + TURU | g. [Gwithil i·Durinthi](https://eldamo.org/content/words/word-423768501.html) | ŊWEĐE |
| mq. [mindon](https://eldamo.org/content/words/word-491009435.html) | MIN | n. [mindon](https://eldamo.org/content/words/word-3336185929.html) | MIN + TUN |
| q. [Minyar](https://eldamo.org/content/words/word-1489677109.html) | MIN | s. [Miniel](https://eldamo.org/content/words/word-125781799.html) | EL |
| eq. [moar(do)](https://eldamo.org/content/words/word-1697039009.html) | MAWA | g. [mothweg](https://eldamo.org/content/words/word-774691747.html) | MAWA + WAIK |
| mq. [Moriqendi](https://eldamo.org/content/words/word-3291050415.html) | MOR + KWEN(ED) | n. [Dureledh](https://eldamo.org/content/words/word-866972063.html) | DOƷ + ELED |
| mq. [Moriqendi](https://eldamo.org/content/words/word-3291050415.html) | MOR + KWEN(ED) | n. [Durion](https://eldamo.org/content/words/word-1021747159.html) | DOƷ |
| eq. [Moritarnon](https://eldamo.org/content/words/word-4203456839.html) | MORO + TARA¹ | g. [Tarn Fui](https://eldamo.org/content/words/word-3886953873.html) | TARA¹ + ǶUẎU |
| eq. [Mormakil](https://eldamo.org/content/words/word-2459740785.html) | MORO + MAKA¹ | g. [Mormagli](https://eldamo.org/content/words/word-3198085201.html) | MORO |
| eq. [Mornie](https://eldamo.org/content/words/word-13397699.html) | MORO + NYEHE | g. [Mornir](https://eldamo.org/content/words/word-219623649.html) | MORO |
| eq. [Morwinyon](https://eldamo.org/content/words/word-4124697491.html) | MORO + GWINI | g. [Morwinthi](https://eldamo.org/content/words/word-3886766727.html) | MORO/GWINI |
| q. [mélamar](https://eldamo.org/content/words/word-3756694359.html) | MEL + MBAR | s. [milbar](https://eldamo.org/content/words/word-3004190963.html) | MBAR |
| eq. [naika¹](https://eldamo.org/content/words/word-1438629639.html) | ŊAHYA | g. [gaig](https://eldamo.org/content/words/word-2690070435.html) | YAYA |
| nq. [namoia-](https://eldamo.org/content/words/word-2477293621.html) | NA/ANA + MŌ | ns. [ammuia-](https://eldamo.org/content/words/word-2492227927.html) | MŌ |
| mq. [nandaro](https://eldamo.org/content/words/word-2708931445.html) | ÑGAN(AD) | n. [talagand](https://eldamo.org/content/words/word-1671960619.html) | TYAL + ÑGAN(AD) |
| q. [Nandor](https://eldamo.org/content/words/word-1531362389.html) | (N)DAN | s. [Danedhel](https://eldamo.org/content/words/word-1793507549.html) | (N)DAN + DEL²/DEL¹ |
| q. [Nandor](https://eldamo.org/content/words/word-1531362389.html) | (N)DAN | s. [Danwaith](https://eldamo.org/content/words/word-1560394967.html) | (N)DAN + WĒ/EWE/WEG |
| q. [Nand’ Ondoluncava](https://eldamo.org/content/words/word-3897365555.html) | NAD + GONOD + LUK | s. [Nan Gondresgion](https://eldamo.org/content/words/word-3707057995.html) | NAD + GONOD + YON²/YAN¹ |
| mq. [Nanisáro](https://eldamo.org/content/words/word-913710051.html) | THĀ/ATHA | n. [Dainthor](https://eldamo.org/content/words/word-486949099.html) | (N)DAN + THĀ/ATHA |
| q. [nanwen-](https://eldamo.org/content/words/word-4281976313.html) | (N)DAN + MEN | s. [dandol-](https://eldamo.org/content/words/word-601692547.html) | (N)DAN + TUL |
| q. [nanwë](https://eldamo.org/content/words/word-3559189537.html) | (N)DAN | s. [dannen](https://eldamo.org/content/words/word-979655405.html) | (N)DAN + NEN |
| mq. [Narqelion](https://eldamo.org/content/words/word-974619277.html) | NAR + KWEL | n. [lhasbelin](https://eldamo.org/content/words/word-2663522623.html) | LAS¹ + KWEL |
| q. [nauco](https://eldamo.org/content/words/word-234493503.html) | NUK | s. [Naugrim](https://eldamo.org/content/words/word-3358974201.html) | NUK + RIM |
| q. [nehtar](https://eldamo.org/content/words/word-3520315715.html) | SNAG/NDAK | s. [dagnir](https://eldamo.org/content/words/word-3651249801.html) | NDAK + N(D)ER |
| mq. [Neldion](https://eldamo.org/content/words/word-787974879.html) | NEL | n. [Ar Neleduir](https://eldamo.org/content/words/word-807855243.html) | AR¹ + NELED + TĀ/TAƷ |
| mq. [Nessa](https://eldamo.org/content/words/word-7408399.html) | NETH | n. [Dineth](https://eldamo.org/content/words/word-4114815571.html) | NDIS/NĪ¹/INI/NIS + NETH |
| mq. [Nessaron](https://eldamo.org/content/words/word-1687549543.html) | NETH | n. [Ar Nethwelein](https://eldamo.org/content/words/word-1666041177.html) | AR¹ + NETH + BAL |
| q. [neterquë](https://eldamo.org/content/words/word-2293017047.html) | NETER | ns. [paeneder](https://eldamo.org/content/words/word-3654391257.html) | KWAY + NETER |
| mq. [nieninqe](https://eldamo.org/content/words/word-1346536449.html) | NEY + NIK(W) | n. [nifredil](https://eldamo.org/content/words/word-3242429459.html) | NIK(W) + TIL |
| eq. [nieninqe](https://eldamo.org/content/words/word-3386767121.html) | NYEHE + NIQI | g. [ninconin](https://eldamo.org/content/words/word-2692066799.html) | NIQI |
| eq. [nierwes](https://eldamo.org/content/words/word-2018535101.html) | NEHE | g. [niost](https://eldamo.org/content/words/word-602232561.html) | NEHE + OSO² |
| eq. [nindon](https://eldamo.org/content/words/word-3882428547.html) | NINI + ƷONO | g. [nind](https://eldamo.org/content/words/word-46176045.html) | NINI |
| eq. [Noldo](https://eldamo.org/content/words/word-2665511273.html) | ŊOLO | g. [Goldothrim](https://eldamo.org/content/words/word-1184215219.html) | ŊOLO + HOSO |
| q. [Noldo](https://eldamo.org/content/words/word-840869727.html) | ÑGOL¹/ÑGOLOD/ÑGOL² | s. [Gódhel](https://eldamo.org/content/words/word-365331841.html) | DEL¹ |
| eq. [Noldomar](https://eldamo.org/content/words/word-1430415081.html) | ŊOLO + MBARA | g. [Goldobar](https://eldamo.org/content/words/word-427331973.html) | ŊOLO |
| q. [Norsus](https://eldamo.org/content/words/word-1830754881.html) | ÑGOR + THUS | s. [Gorthaur](https://eldamo.org/content/words/word-16626271.html) | ÑGOR |
| eq. [Nosse Tuilinda](https://eldamo.org/content/words/word-3588644341.html) | NŌ + TUẎU + LIÐI | g. [Nos Duilin](https://eldamo.org/content/words/word-123443075.html) | NŌ + DUYU + INI |
| nq. [nostarë](https://eldamo.org/content/words/word-2884003461.html) | NŌ/ONO + ER | ns. [oronnad](https://eldamo.org/content/words/word-1550919009.html) | UR + NŌ/ONO |
| eq. [nuste](https://eldamo.org/content/words/word-769224511.html) | NUSU | g. [nufri](https://eldamo.org/content/words/word-4011935511.html) | NUFU |
| q. [Návarot](https://eldamo.org/content/words/word-521037545.html) | ROT | s. [Nogrod](https://eldamo.org/content/words/word-3455220253.html) | NUK + ROT |
| q. [númen](https://eldamo.org/content/words/word-1285367433.html) | NDU + MEN | s. [annûn](https://eldamo.org/content/words/word-1864027637.html) | NDU |
| q. [númen](https://eldamo.org/content/words/word-1285367433.html) | NDU + MEN | s. [dûn](https://eldamo.org/content/words/word-4010460053.html) | NDU |
| mq. [Oiolosse](https://eldamo.org/content/words/word-3203011053.html) | OY¹ + GOLOS | n. [Amon Uilos](https://eldamo.org/content/words/word-1347868551.html) | AM² + OY¹ + GOLOS |
| mq. [Oiolosse](https://eldamo.org/content/words/word-3203011053.html) | OY¹ + GOLOS | on. [Uigolosse](https://eldamo.org/content/words/word-3663823667.html) | OY¹ |
| q. [Oiolossë](https://eldamo.org/content/words/word-2557589703.html) | OY + (G)LOS | s. [Amon Uilos](https://eldamo.org/content/words/word-1502997501.html) | AM²/MBON + OY + (G)LOS |
| q. [olass(i)ë](https://eldamo.org/content/words/word-2930904251.html) | WO + LAS¹ | s. [golas](https://eldamo.org/content/words/word-3571042603.html) | LAS¹ |
| eq. [Olóre Malle](https://eldamo.org/content/words/word-2974590301.html) | LORO + MALA¹ | g. [Malmaurien](https://eldamo.org/content/words/word-2241453669.html) | MURU |
| eq. [Olóre Malle](https://eldamo.org/content/words/word-2974590301.html) | LORO + MALA¹ | g. [Maurelant](https://eldamo.org/content/words/word-2161455337.html) | MURU |
| eq. [Ondolie](https://eldamo.org/content/words/word-3150036741.html) | ƷONO + LĪ | g. [Gondothlim](https://eldamo.org/content/words/word-375124927.html) | ƷONO + HOSO |
| eq. [Ondolinda](https://eldamo.org/content/words/word-277835423.html) | ƷONO + LIÐI | g. [Gondolin](https://eldamo.org/content/words/word-733614277.html) | ƷONO |
| q. [Ondoluncanan(do)](https://eldamo.org/content/words/word-4165414001.html) | GONOD + LUK + NAD | s. [Nan Gondresgion](https://eldamo.org/content/words/word-3707057995.html) | NAD + GONOD + YON²/YAN¹ |
| nq. [ondosercë](https://eldamo.org/content/words/word-92698913.html) | GONOD + SEREK | s. [seregon](https://eldamo.org/content/words/word-3527752535.html) | SEREK + GONOD |
| eq. [Ondosta](https://eldamo.org/content/words/word-2641039603.html) | ƷONO + OSO² | g. [Gondobar](https://eldamo.org/content/words/word-3134010949.html) | ƷONO + MBARA |
| eq. [Ondostamar](https://eldamo.org/content/words/word-589397363.html) | ƷONO + OSO² + MBARA | g. [Gondothlimbar](https://eldamo.org/content/words/word-2217055203.html) | ƷONO + HOSO + MBARA |
| mq. [onta-](https://eldamo.org/content/words/word-3360702751.html) | NŌ/ONO | n. [edonna-](https://eldamo.org/content/words/word-2088929859.html) | ET + NŌ/ONO |
| mq. [onóne](https://eldamo.org/content/words/word-399307841.html) | WO + NŌ/ONO | n. [gwanur](https://eldamo.org/content/words/word-3801320453.html) | WO |
| mq. [onóro](https://eldamo.org/content/words/word-2670948515.html) | WO + NŌ/ONO | n. [gwanur](https://eldamo.org/content/words/word-3801320453.html) | WO |
| mq. [opele](https://eldamo.org/content/words/word-2025617429.html) | PEL(ES) | n. [gobel](https://eldamo.org/content/words/word-1626246043.html) | WO + PEL(ES) |
| mq. [Osse](https://eldamo.org/content/words/word-4214190195.html) | GOS | n. [Oeros](https://eldamo.org/content/words/word-2119516329.html) | AY(AR) + GOS |
| q. [Ossë](https://eldamo.org/content/words/word-76076699.html) | OS | s. [Gaerys](https://eldamo.org/content/words/word-3414372253.html) | GAY(AR) + OS |
| q. [otoquë](https://eldamo.org/content/words/word-3840579707.html) | OTOS/OTOK | ns. [paenodog](https://eldamo.org/content/words/word-3048562099.html) | KWAY + OTOS/OTOK |
| mq. [Otselen](https://eldamo.org/content/words/word-2284045209.html) | OT/OTOS/OTOK + EL | n. [Edegil](https://eldamo.org/content/words/word-820632375.html) | OT/OTOS/OTOK + GIL |
| eq. [otsola](https://eldamo.org/content/words/word-1966499275.html) | OTO + KAL | g. [ochlad](https://eldamo.org/content/words/word-487196675.html) | OTO |
| q. [palantír](https://eldamo.org/content/words/word-255004773.html) | PAL + TIR | s. [Gwahaedir](https://eldamo.org/content/words/word-2508691339.html) | WĀ/AWA + KHAY + TIR |
| eq. [palapapte](https://eldamo.org/content/words/word-1603258505.html) | PALA + PAPA | g. [blantos](https://eldamo.org/content/words/word-2255046817.html) | PALA |
| eq. [Palyanoldor](https://eldamo.org/content/words/word-2603431431.html) | PALA + ŊOLO | g. [Gwadangoltha](https://eldamo.org/content/words/word-3242156097.html) | ŊOLO |
| eq. [Pelekkion](https://eldamo.org/content/words/word-1557687465.html) | PELEK + YO(NO) | g. [Pelegild](https://eldamo.org/content/words/word-3370455781.html) | PELEK |
| q. [Pereldar](https://eldamo.org/content/words/word-92269493.html) | PER + EL | s. [Peredhel](https://eldamo.org/content/words/word-3281079503.html) | PER + DEL²/DEL¹ |
| nq. [pirindëa](https://eldamo.org/content/words/word-4007111035.html) | PIR | ns. [piren](https://eldamo.org/content/words/word-708065487.html) | KWIR |
| mq. [qantien](https://eldamo.org/content/words/word-528254003.html) | KWAT + YEN¹ | n. [penninar](https://eldamo.org/content/words/word-674657133.html) | KWAT + YEN¹ + AR¹ |
| mq. [Qendelie](https://eldamo.org/content/words/word-717772043.html) | KWEN(ED) + LI | n. [penedh](https://eldamo.org/content/words/word-768849965.html) | KWEN(ED) |
| mq. [Qenta Noldorinwa](https://eldamo.org/content/words/word-1085510481.html) | KWET | n. [Pennas inGeleidh](https://eldamo.org/content/words/word-2336604527.html) | KWET + I¹ + ÑGOLOD |
| mq. [Qenta Noldorinwa](https://eldamo.org/content/words/word-1085510481.html) | KWET | n. [Pennas-na-Ngoelaidh](https://eldamo.org/content/words/word-2309188851.html) | KWET + NĀ¹/ANA¹ + ÑGOLOD |
| eq. [qim(en)ea](https://eldamo.org/content/words/word-2026113575.html) | QIMI | g. [gwiniol](https://eldamo.org/content/words/word-3271360947.html) | GIWI/GWENE¹ |
| eq. [qimelle](https://eldamo.org/content/words/word-2812839775.html) | QIMI | g. [gwiniel](https://eldamo.org/content/words/word-2732530755.html) | GIWI/GWENE¹ |
| eq. [qimenoite](https://eldamo.org/content/words/word-147980365.html) | QIMI | g. [gwinwed](https://eldamo.org/content/words/word-890902399.html) | GIWI/GWENE¹ |
| eq. [qinde](https://eldamo.org/content/words/word-4213330493.html) | QIMI | g. [gwinios](https://eldamo.org/content/words/word-3577663989.html) | GIWI/GWENE¹ |
| eq. [qin¹](https://eldamo.org/content/words/word-705831773.html) | QIMI | g. [gwin](https://eldamo.org/content/words/word-1982054357.html) | GIWI/GWENE¹ |
| q. [quaican](https://eldamo.org/content/words/word-1790292639.html) | KANAT | ns. [paegan](https://eldamo.org/content/words/word-4165621321.html) | KWAY + KANAT |
| q. [quailepen](https://eldamo.org/content/words/word-3838964689.html) | LEPEN | ns. [paeleben](https://eldamo.org/content/words/word-2719340173.html) | KWAY + LEPEN |
| q. [quainel](https://eldamo.org/content/words/word-2102686053.html) | NELE | ns. [paenel](https://eldamo.org/content/words/word-1186731603.html) | KWAY + NEL |
| q. [quainque](https://eldamo.org/content/words/word-4149987191.html) | ENEK | ns. [paeneg](https://eldamo.org/content/words/word-1576936201.html) | KWAY + ENEK |
| q. [quainëa](https://eldamo.org/content/words/word-1258418913.html) | KAYAN | s. [paenui](https://eldamo.org/content/words/word-2564509863.html) | KWAY |
| q. [quellë](https://eldamo.org/content/words/word-2960856767.html) | KWEL¹ + LEÑ | s. [firith](https://eldamo.org/content/words/word-2681462959.html) | PHIR |
| mq. [randa](https://eldamo.org/content/words/word-381606413.html) | RAD | n. [anrand](https://eldamo.org/content/words/word-3493977863.html) | ANAD + RAD |
| mq. [ravanda](https://eldamo.org/content/words/word-100709315.html) | RAB¹ | n. [Rhofannor](https://eldamo.org/content/words/word-1399703539.html) | RAB¹ + NDOR |
| eq. [rimp(in)a](https://eldamo.org/content/words/word-78256875.html) | RIPI | g. [rimin¹](https://eldamo.org/content/words/word-4214526601.html) | RIMI |
| eq. [rimpe](https://eldamo.org/content/words/word-86460877.html) | RIPI | g. [rim¹](https://eldamo.org/content/words/word-1073616967.html) | RIMI |
| q. [Ringarë](https://eldamo.org/content/words/word-701052069.html) | RINGI | s. [Girithron](https://eldamo.org/content/words/word-3643912947.html) | GIR |
| q. [ronda](https://eldamo.org/content/words/word-3942900161.html) | RON² | s. [grond](https://eldamo.org/content/words/word-1735688587.html) | GRON |
| q. [ruimen](https://eldamo.org/content/words/word-1826967725.html) | RUY + MEN | s. [ruist](https://eldamo.org/content/words/word-1403666717.html) | RUY |
| nq. [ruinalda](https://eldamo.org/content/words/word-2200453439.html) | RUY + GAL²/GALAD | ns. [ruindol](https://eldamo.org/content/words/word-590191255.html) | RUN¹ + NDOL |
| q. [ruinë](https://eldamo.org/content/words/word-3064831821.html) | RUY | s. [ruin](https://eldamo.org/content/words/word-2313781075.html) | RUN¹ |
| eq. [rímen](https://eldamo.org/content/words/word-833668827.html) | RIMI | g. [rib](https://eldamo.org/content/words/word-4114461233.html) | RIPI |
| q. [rómen](https://eldamo.org/content/words/word-3503146575.html) | (S)RŌ + MEN | s. [amrûn](https://eldamo.org/content/words/word-3136154397.html) | AM² + (S)RŌ |
| q. [rómen](https://eldamo.org/content/words/word-3503146575.html) | (S)RŌ + MEN | s. [rhûn](https://eldamo.org/content/words/word-2972186711.html) | (S)RŌ |
| mq. [róna](https://eldamo.org/content/words/word-2205804359.html) | RŌ/ORO | n. [amrûn](https://eldamo.org/content/words/word-1393854111.html) | AM² + RŌ/ORO |
| q. [Rúatan](https://eldamo.org/content/words/word-4235987617.html) | ATATA | s. [Drúadan](https://eldamo.org/content/words/word-854377075.html) | DROB + ATATA |
| eq. [Rúsitaurion](https://eldamo.org/content/words/word-2215403305.html) | RU’U + TAVA + YO(NO) | g. [Drauthodavros](https://eldamo.org/content/words/word-3182051761.html) | RAPA + TAVA |
| mq. [Sangahyando](https://eldamo.org/content/words/word-1617303585.html) | STAG + SYAD¹ | n. [Hadhafang](https://eldamo.org/content/words/word-2292673605.html) | SYAD¹ + STAG |
| eq. [Sangahyando](https://eldamo.org/content/words/word-1305471759.html) | SAŊA + HYAÐA | g. [Hanthang](https://eldamo.org/content/words/word-3074203611.html) | HYAÐA + SAŊA |
| eq. [Sangayando](https://eldamo.org/content/words/word-347697889.html) | SA + ŊAHYA | g. [Sangair](https://eldamo.org/content/words/word-431952629.html) | ŊAHYA |
| q. [Sauron](https://eldamo.org/content/words/word-1170395945.html) | THOW/THAW | s. [Gorthaur](https://eldamo.org/content/words/word-16626271.html) | ÑGOR |
| mq. [Sauron](https://eldamo.org/content/words/word-280755201.html) | THUS | n. [Gorthû](https://eldamo.org/content/words/word-1796801611.html) | ÑGOROTH + THUS |
| eq. [Silmarinko](https://eldamo.org/content/words/word-356688499.html) | SILI + RINI | g. [Silmadrin](https://eldamo.org/content/words/word-4261309707.html) | SILI |
| mq. [Silpion](https://eldamo.org/content/words/word-1145272971.html) | SILIP | on. [Balthil](https://eldamo.org/content/words/word-636942733.html) | BAL + THIL |
| mq. [Silpion](https://eldamo.org/content/words/word-1145272971.html) | SILIP | n. [Belthil](https://eldamo.org/content/words/word-1621519675.html) | BAL + THIL |
| q. [Sinda](https://eldamo.org/content/words/word-3270080025.html) | THIN | s. [Thindrim](https://eldamo.org/content/words/word-3948057659.html) | THIN + RIM |
| eq. [Solosimpe](https://eldamo.org/content/words/word-3928364761.html) | ÞOLO + SIPI | g. [Flosibrim](https://eldamo.org/content/words/word-3075901647.html) | ÞOLO |
| eq. [Solosimpe](https://eldamo.org/content/words/word-3928364761.html) | ÞOLO + SIPI | g. [Simfi](https://eldamo.org/content/words/word-3914351851.html) | SIPI |
| eq. [Solosimpe](https://eldamo.org/content/words/word-3928364761.html) | ÞOLO + SIPI | g. [Thlossibrim](https://eldamo.org/content/words/word-2123009873.html) | SIPI |
| eq. [Sornekiris](https://eldamo.org/content/words/word-1125234039.html) | ÞORO + KIRISI | g. [Cristhorn](https://eldamo.org/content/words/word-953997053.html) | KIRISI + ÞORO |
| eq. [Sorontur](https://eldamo.org/content/words/word-1653115741.html) | ÞORO + TURU | g. [Thorndor](https://eldamo.org/content/words/word-3069726757.html) | ÞORO |
| nq. [sérinqua](https://eldamo.org/content/words/word-3915151291.html) | SED + KWA | ns. [sídheb](https://eldamo.org/content/words/word-808729623.html) | SED |
| eq. [Súlimo](https://eldamo.org/content/words/word-2257734769.html) | SUHYU | g. [Gwanweg](https://eldamo.org/content/words/word-1949008215.html) | GWĀ |
| q. [Súlimë](https://eldamo.org/content/words/word-3339901781.html) | THŪ | s. [Gwaeron](https://eldamo.org/content/words/word-368969139.html) | WAY/WĀ |
| eq. [súyon](https://eldamo.org/content/words/word-1827787555.html) | SUẈU + YO(NO) | g. [fwion](https://eldamo.org/content/words/word-1368673629.html) | SUẈU |
| eq. [Taimavar](https://eldamo.org/content/words/word-2165104123.html) | DAHA + MAWA | g. [Daimord](https://eldamo.org/content/words/word-76152031.html) | MAWA |
| eq. [Taimordo](https://eldamo.org/content/words/word-1542632893.html) | DAHA + MAWA | g. [Daimord](https://eldamo.org/content/words/word-76152031.html) | MAWA |
| eq. [Talka Marda](https://eldamo.org/content/words/word-2890307653.html) | MBARA | g. [Martaglos](https://eldamo.org/content/words/word-806240559.html) | MARA² |
| mq. [Taltyelemna](https://eldamo.org/content/words/word-1407580121.html) | TAL¹ + KYELEP | n. [Celebrindal](https://eldamo.org/content/words/word-447305977.html) | KYELEP + TAL¹ |
| eq. [Taniqetil](https://eldamo.org/content/words/word-1398777461.html) | DAHA + NIQI | g. [Danigwethil](https://eldamo.org/content/words/word-1348110193.html) | DAHA |
| mq. [Taniqetil](https://eldamo.org/content/words/word-115053639.html) | TĀ/TAƷ + NIK(W) + TIL | n. [Nimdildor](https://eldamo.org/content/words/word-2517116965.html) | NIK(W) + TIL + TUR |
| q. [Tannacolli](https://eldamo.org/content/words/word-1037115073.html) | TAN² + KOL | s. [Tengyl](https://eldamo.org/content/words/word-4189293005.html) | TAN² |
| q. [Taras Lúna](https://eldamo.org/content/words/word-4187840705.html) | TĀ/TAƷ/TAR + DU | s. [Barad-dûr](https://eldamo.org/content/words/word-3236058797.html) | M(B)ARAT/BARAT + NDU |
| q. [tarhanwa](https://eldamo.org/content/words/word-3054433215.html) | TĀ/TAƷ + KHAD | s. [arahadhw](https://eldamo.org/content/words/word-127818517.html) | RĀ/ARA/ARAN + KHAD |
| mq. [Tarkil](https://eldamo.org/content/words/word-3490586973.html) | TĀ/TAƷ + KHIL | n. [Torfir](https://eldamo.org/content/words/word-354280113.html) | TUR + PHIR |
| mq. [Tarkilmar](https://eldamo.org/content/words/word-3135393577.html) | TĀ/TAƷ + KHIL + MBAR | n. [Torfirion](https://eldamo.org/content/words/word-534086899.html) | TUR + PHIR |
| q. [Tarmacorto](https://eldamo.org/content/words/word-3304032071.html) | TĀ/TAƷ + KOR | s. [Orchorod](https://eldamo.org/content/words/word-1935435815.html) | OROT/RŌ/ORO + KOR |
| eq. [Tasarinan](https://eldamo.org/content/words/word-1523647235.html) | TASA + NAÐA | g. [Dor-tathrin](https://eldamo.org/content/words/word-1470033543.html) | TASA |
| eq. [Tasarinan](https://eldamo.org/content/words/word-1523647235.html) | TASA + NAÐA | g. [Nan Tathrin](https://eldamo.org/content/words/word-1418380525.html) | NAÐA + TASA |
| mq. [Tasarinan](https://eldamo.org/content/words/word-1141369723.html) | TATHAR + NAD | n. [Nan-tathren](https://eldamo.org/content/words/word-2328899105.html) | NAD + TATHAR |
| q. [Tasarinan](https://eldamo.org/content/words/word-3669453133.html) | TATHAR + NAD | s. [Nan-tathren](https://eldamo.org/content/words/word-1055336505.html) | NAD + TATHAR |
| eq. [Tauler](https://eldamo.org/content/words/word-2122943601.html) | TAW̯A | g. [Thlim Taul](https://eldamo.org/content/words/word-2118504543.html) | TULU |
| eq. [taule²](https://eldamo.org/content/words/word-73343783.html) | TAW̯A | g. [taul](https://eldamo.org/content/words/word-714044475.html) | TULU |
| mq. [Taure Huinéva](https://eldamo.org/content/words/word-1930144875.html) | TAWAR + PHUY | n. [Taur-na-Fuin](https://eldamo.org/content/words/word-1783930661.html) | TAWAR + NĀ¹/ANA¹ + PHUY |
| eq. [Taurosse](https://eldamo.org/content/words/word-3710822845.html) | TAVA | g. [Tavrobel](https://eldamo.org/content/words/word-1557311155.html) | TAVA + PELE¹ |
| eq. [Taurosse](https://eldamo.org/content/words/word-3710822845.html) | TAVA | g. [Tavrost](https://eldamo.org/content/words/word-3796125207.html) | TAVA + ORO¹ |
| eq. [Telimektar](https://eldamo.org/content/words/word-1989343939.html) | TELE + EKE | g. [Telumaithor](https://eldamo.org/content/words/word-1499971231.html) | TELE |
| q. [tenna¹](https://eldamo.org/content/words/word-378761911.html) | TEN | ns. [naden](https://eldamo.org/content/words/word-2852741809.html) | NA/ANA + TEN |
| q. [tintila-](https://eldamo.org/content/words/word-2840834399.html) | TIN + THIL | ns. [tinthiltha-](https://eldamo.org/content/words/word-3160524315.html) | TIN + TIL |
| mq. [Tintánie](https://eldamo.org/content/words/word-192946697.html) | TIN + TAN¹ | n. [Gilthoniel](https://eldamo.org/content/words/word-3438237549.html) | GIL + TAN¹ + SEL(D) |
| eq. [Tinwetári](https://eldamo.org/content/words/word-2185884035.html) | TINI + DAHA | g. [Tinthurwin](https://eldamo.org/content/words/word-2023925535.html) | TINI + TURU |
| eq. [Tiri(o)stirion](https://eldamo.org/content/words/word-708028937.html) | TIRI + TIÐI | g. [Gwarestrin](https://eldamo.org/content/words/word-235955515.html) | WARA + EKE |
| eq. [tirion](https://eldamo.org/content/words/word-2622831779.html) | TIÐI | g. [tirin](https://eldamo.org/content/words/word-1965705027.html) | TIRI |
| eq. [Tirios Otsoyáma](https://eldamo.org/content/words/word-2846565013.html) | TIÐI + OTO + YAMA | g. [Ostrin An Ost](https://eldamo.org/content/words/word-871749661.html) | OSO² |
| mq. [Tiristemindon](https://eldamo.org/content/words/word-2120494839.html) | TIR + MIN | n. [Minas Tirith](https://eldamo.org/content/words/word-481582893.html) | MIN + TIR |
| q. [tolyo](https://eldamo.org/content/words/word-3613765759.html) | TOL/TOLOD | s. [toleg](https://eldamo.org/content/words/word-3594850469.html) | TOL + NIK |
| eq. [Tuilindo](https://eldamo.org/content/words/word-1677228443.html) | TUẎU + LIÐI | g. [Duilin](https://eldamo.org/content/words/word-273972655.html) | DUYU + INI |
| eq. [tuilindo](https://eldamo.org/content/words/word-3587092229.html) | TUẎU + LIÐI | g. [duilin(g)](https://eldamo.org/content/words/word-3993159897.html) | DUYU + INI |
| eq. [Tuilindor](https://eldamo.org/content/words/word-2993165449.html) | TUẎU + LIÐI | g. [Thlim Duilin](https://eldamo.org/content/words/word-756438231.html) | DUYU + INI |
| eq. [Tuivána](https://eldamo.org/content/words/word-487458641.html) | TUẎU + VANA | g. [Tuilir](https://eldamo.org/content/words/word-3449068231.html) | TUẎU |
| q. [turmen](https://eldamo.org/content/words/word-2316974801.html) | TUR + MEN | s. [arthor](https://eldamo.org/content/words/word-1055634733.html) | RĀ/ARA + TUR |
| q. [Turmen Follondiéva](https://eldamo.org/content/words/word-2787756753.html) | TUR + MEN + PHOR + MEN + LON¹ | s. [Arthor na Forlonnas](https://eldamo.org/content/words/word-3464805601.html) | RĀ/ARA + TUR + NA/ANA + PHOR + LON¹ |
| q. [Turmen Hyallondiéva](https://eldamo.org/content/words/word-3519902329.html) | TUR + MEN + KHYAR + LON¹ | s. [Arthor na Challonnas](https://eldamo.org/content/words/word-266328151.html) | RĀ/ARA + TUR + NA/ANA + KHYAR + LON¹ |
| eq. [Turondo](https://eldamo.org/content/words/word-2053047467.html) | TURU + ƷONO | g. [Turgon](https://eldamo.org/content/words/word-3050580123.html) | TURU |
| eq. [Turuhalme](https://eldamo.org/content/words/word-1680102945.html) | TUÐU + HALA | g. [Halmadhurwion](https://eldamo.org/content/words/word-1423575671.html) | HALA + TUÐU |
| nq. [tëangolmë](https://eldamo.org/content/words/word-3365021359.html) | TEÑ + ÑGOL¹ | ns. [lamengolu](https://eldamo.org/content/words/word-3671822361.html) | LAB + ÑGOL¹ |
| q. [Túrosto](https://eldamo.org/content/words/word-2103291357.html) | TUR + SOT | s. [Belegost](https://eldamo.org/content/words/word-1938932211.html) | MBELEK + SOT |
| eq. [Uin](https://eldamo.org/content/words/word-1369149549.html) | IWI | g. [Uin](https://eldamo.org/content/words/word-2755788105.html) | GWIŊI |
| q. [ulca](https://eldamo.org/content/words/word-768038407.html) | Ū + KAL | s. [ogol](https://eldamo.org/content/words/word-418534437.html) | OKO |
| mq. [Ulmo](https://eldamo.org/content/words/word-850118005.html) | ULU | n. [Uiar](https://eldamo.org/content/words/word-3413924877.html) | WAY |
| eq. [Ulmonan](https://eldamo.org/content/words/word-2264830629.html) | ULU¹ | g. [Ingulma(n)](https://eldamo.org/content/words/word-1921814589.html) | IÐI |
| q. [undómë](https://eldamo.org/content/words/word-1825769337.html) | NŪ/UNU + DOM | s. [aduial](https://eldamo.org/content/words/word-4029927507.html) | AT + YU + GAL¹ |
| q. [Ungoliantë](https://eldamo.org/content/words/word-1498581795.html) | UÑG + SLIG | s. [Ungoliant](https://eldamo.org/content/words/word-1772080551.html) | UÑG |
| eq. [Ungweliante](https://eldamo.org/content/words/word-2863856727.html) | GUŊU | g. [Gungliont](https://eldamo.org/content/words/word-3243008015.html) | LIYA |
| eq. [Ungweliante](https://eldamo.org/content/words/word-2863856727.html) | GUŊU | g. [Ungoliont](https://eldamo.org/content/words/word-4247225419.html) | LĪ |
| q. [ur(u)-](https://eldamo.org/content/words/word-1589987053.html) | GUR | s. [gor](https://eldamo.org/content/words/word-2957890527.html) | ÑGOR |
| eq. [Urdolwen](https://eldamo.org/content/words/word-3832687647.html) | GWṚÐṚ | g. [Gurtholfin](https://eldamo.org/content/words/word-926482673.html) | GWṚÐṚ + ALA² |
| eq. [Urwen(di)](https://eldamo.org/content/words/word-3163552589.html) | URU + GWENE¹ | g. [Urwedhin](https://eldamo.org/content/words/word-3132377893.html) | URU |
| eq. [Uswevanda](https://eldamo.org/content/words/word-2168895321.html) | USU + VAHA | g. [Bad Uthwen](https://eldamo.org/content/words/word-4162243047.html) | VAHA |
| nq. [uswë](https://eldamo.org/content/words/word-2745817325.html) | UTH | ns. [uthwen](https://eldamo.org/content/words/word-3649952321.html) | UTH + MEN |
| q. [Utumno](https://eldamo.org/content/words/word-1948434479.html) | TUB | s. [Udûn](https://eldamo.org/content/words/word-17406641.html) | TUP |
| q. [uxarë](https://eldamo.org/content/words/word-3050296043.html) | UTHU + KAR | s. [othgar(ed)](https://eldamo.org/content/words/word-283731099.html) | UTHU |
| mq. [vahai(y)a](https://eldamo.org/content/words/word-203974717.html) | KHAY | n. [gwahae](https://eldamo.org/content/words/word-2685516261.html) | AWA + KHAY |
| eq. [Vala](https://eldamo.org/content/words/word-3104279967.html) | WALA | g. [Ban¹](https://eldamo.org/content/words/word-1158175361.html) | VANA |
| mq. [Valakirka](https://eldamo.org/content/words/word-1383345177.html) | BAL + KIRIK | n. [Cerch iMbelain](https://eldamo.org/content/words/word-3350307483.html) | KIRIK + I¹ + BAL |
| q. [Valanya](https://eldamo.org/content/words/word-84450489.html) | BAL | s. [Orbelain](https://eldamo.org/content/words/word-3884665251.html) | UR + BAL |
| mq. [Valinor](https://eldamo.org/content/words/word-2643047643.html) | BAL + NDOR/NŌ/ONO | on. [Balandor](https://eldamo.org/content/words/word-2982359283.html) | BAL |
| mq. [Valinor](https://eldamo.org/content/words/word-2643047643.html) | BAL + NDOR/NŌ/ONO | n. [Balannor](https://eldamo.org/content/words/word-2577340481.html) | BAL |
| eq. [Valinor](https://eldamo.org/content/words/word-2425770369.html) | WALA + NŌ | g. [Gwalien](https://eldamo.org/content/words/word-3079100023.html) | WALA |
| q. [Valinórë](https://eldamo.org/content/words/word-1314183409.html) | BAL + NDOR/NŌ/ONO/DOR | s. [Dor-Rodyn](https://eldamo.org/content/words/word-1761423637.html) | NDOR/DOR + ARAT/RĀ/ARA/RAT² |
| eq. [Varastirion](https://eldamo.org/content/words/word-533915689.html) | VṚÐṚ + TIÐI | g. [Gwarestrin](https://eldamo.org/content/words/word-235955515.html) | WARA + EKE |
| eq. [Varavilindo](https://eldamo.org/content/words/word-2461259387.html) | WARA + VILI + LIÐI | g. [Gwarbilin](https://eldamo.org/content/words/word-1818160743.html) | WARA + DUYU + INI |
| mq. [Varda](https://eldamo.org/content/words/word-993031359.html) | BARAD | on. [Barathi(l)](https://eldamo.org/content/words/word-2863783273.html) | BARATH |
| mq. [Varda](https://eldamo.org/content/words/word-993031359.html) | BARAD | n. [Berethil](https://eldamo.org/content/words/word-2363615467.html) | BARATH |
| eq. [varimo](https://eldamo.org/content/words/word-2733856349.html) | VARA | g. [faronweg](https://eldamo.org/content/words/word-4031790877.html) | VARA + WAIK |
| eq. [varitsi](https://eldamo.org/content/words/word-4271146995.html) | VARA | g. [faronwin](https://eldamo.org/content/words/word-2160827551.html) | VARA + GIWI/GWENE¹ |
| eq. [varyani](https://eldamo.org/content/words/word-3170743759.html) | VARA | g. [faronwin](https://eldamo.org/content/words/word-2160827551.html) | VARA + GIWI/GWENE¹ |
| eq. [varyanu](https://eldamo.org/content/words/word-570718083.html) | VARA | g. [faronweg](https://eldamo.org/content/words/word-4031790877.html) | VARA + WAIK |
| eq. [Vefántur](https://eldamo.org/content/words/word-498686361.html) | WEHE | g. [Gwifanthor](https://eldamo.org/content/words/word-3007596095.html) | WEHE + FANA |
| eq. [Vefántur](https://eldamo.org/content/words/word-498686361.html) | WEHE | g. [Gwivannoth](https://eldamo.org/content/words/word-2627130957.html) | WEHE + M(B)ṆÐṆ |
| q. [vendelë](https://eldamo.org/content/words/word-4292639917.html) | WEN(ED) + LEÑ | s. [gweneth](https://eldamo.org/content/words/word-318316053.html) | WEN(ED) |
| mq. [veru²](https://eldamo.org/content/words/word-2386690219.html) | BES | n. [Bedhwen](https://eldamo.org/content/words/word-3319196731.html) | BED |
| eq. [vestaner](https://eldamo.org/content/words/word-1373723551.html) | VEÐE + NERE | g. [bedhren](https://eldamo.org/content/words/word-3644571699.html) | VEÐE + REÐE |
| eq. [vestani](https://eldamo.org/content/words/word-3211964265.html) | VEÐE | g. [bedhres](https://eldamo.org/content/words/word-3249749621.html) | VEÐE + REÐE |
| eq. [Vilna](https://eldamo.org/content/words/word-767120095.html) | VILI | g. [Gwilfa](https://eldamo.org/content/words/word-1334041635.html) | GWILI¹ + FAGA |
| q. [vinimo](https://eldamo.org/content/words/word-680222009.html) | WIN | s. [gwinig](https://eldamo.org/content/words/word-4039214635.html) | WIN + NIK |
| eq. [werelin](https://eldamo.org/content/words/word-3791414827.html) | GWERE + RINI | g. [gwerb(e)lin](https://eldamo.org/content/words/word-238344177.html) | GWERE + VELU |
| eq. [Wingilot](https://eldamo.org/content/words/word-2762772021.html) | GWIŊI + LOHO | g. [Gwingalos](https://eldamo.org/content/words/word-1233111227.html) | GWIŊI |
| eq. [Wingilot](https://eldamo.org/content/words/word-2762772021.html) | GWIŊI + LOHO | g. [Lothwing(a)](https://eldamo.org/content/words/word-3556366113.html) | LASA + GWIŊI |
| eq. [Wirilóme](https://eldamo.org/content/words/word-3532044749.html) | GWIÐI + LOMO | g. [Gwerlum](https://eldamo.org/content/words/word-4080102537.html) | GWERE + LOMO |
| q. [Yavannildi](https://eldamo.org/content/words/word-3467128665.html) | YAB + NA/ANA/HAN/AMA + N(D)IL | s. [Ivonwin](https://eldamo.org/content/words/word-2973818817.html) | YAB + WEN(ED) |
| q. [Yavannië](https://eldamo.org/content/words/word-655244079.html) | YAB + NA/ANA/HAN/AMA | s. [Ivanneth](https://eldamo.org/content/words/word-1013902241.html) | YAB |
| mq. [yelme¹](https://eldamo.org/content/words/word-3425665737.html) | DYEL | n. [deloth](https://eldamo.org/content/words/word-3052169735.html) | DYEL + GOS |
| mq. [Yénie Valinóren](https://eldamo.org/content/words/word-344305909.html) | YEN¹ + BAL + NDOR/NŌ/ONO | n. [Inias Valannor](https://eldamo.org/content/words/word-2015000957.html) | YEN¹ + BAL |
| eq. [Ílivarda](https://eldamo.org/content/words/word-2319788225.html) | GILI | g. [Gailbridh(n)ir](https://eldamo.org/content/words/word-262388217.html) | GILI + VṚÐṚ |
| eq. [Úrion](https://eldamo.org/content/words/word-333505487.html) | ƷUÐU | g. [Auros](https://eldamo.org/content/words/word-2877358213.html) | URU |
| q. [úsahtië](https://eldamo.org/content/words/word-897821827.html) | UG/Ū + SAK/THAG | s. [úthaes](https://eldamo.org/content/words/word-1889777045.html) | THAG |
| mq. [úvanimo](https://eldamo.org/content/words/word-1322838637.html) | GŪ/UMU + BAN | n. [úan](https://eldamo.org/content/words/word-724907889.html) | BAN |
