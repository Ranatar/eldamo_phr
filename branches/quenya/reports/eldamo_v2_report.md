# Eldamo 0.8.13 — интерпретатор фонетических правил v2 и повторный анализ

## Статус и границы результата

**Это реализованный и повторно запущенный расширенный интерпретатор, но ещё не всеохватывающий в историко-фонологическом смысле.** Он разбирает все 990 формул имеющегося инвентаря, однако исполнение проверено лишь для поддержанных конструкций и ограниченного набора примеров. Нельзя из синтаксической успешности выводить семантическую корректность.

## Фактически выполненные прогоны

- Различных записей инвентаря: **990**; прошли синтаксический разбор **990**.
- Ранее исключённых записей: **155**, успешно разобраны: **155**. Это НЕ означает, что все примеры этих правил проверены. 
- Исходных кандидатов: **101**, для **24** найдено полное буквальное воспроизведение хотя бы одного ранее отобранного примера.
- Новых кандидатов предыдущей версии: **27**, с точным сопоставлением всех атомарных рёбер инвентаря: **23**; остальные **4** не получают автоматического подтверждения.
- Новый атомарный поиск дал **114** разных структурных путей (две–три ступени) при последовательности Primitive → Ancient → Quenya внутри одной редакционной эпохи. Это не 114 новых, а общий набор структурных путей с текущим фильтром.

## Что добавлено к старому исполнителю

- Множества `{...}` с синхронным выбором вариантов в исходном и результирующем выражениях.
- Варианты `|` сопоставляются попарно, а не образуют декартово произведение.
- Базовые операции над долготой `V → V̄`, сохранение согласных `C` и применение границ `-`.
- Удаление `ø`, фрагменты `S` и последовательное применение к полному слову для поддерживаемых случаев.
- Тесты контролируют, что порядок замен, смешение вариантов и выходы отличны от входа.

## Что ещё не доказывает интерпретатор

- В синтаксисе Eldamo могут встречаться условные и просодические конструкции, не представленные в этом инвентаре; формальная охватность 990/990 не равна универсальной спецификации.
- `S` реализован как грубая согласная-позиция, а не как полный слоговой оператор.
- Несколько одинаковых переменных `V` при сложных согласованных изменениях требуют явной системы связывания по индексам; текущий исполнитель может недоопределять их.
- Для дифтонгов, вставок, метатезы, просодии и позиционных ограничений из ПРОЗЫ нужны отдельные структурированные семантические условия.
- Без экспертной валидации комментариев и лексических примеров нельзя произвольно присвоить исторические категории A или X.

## Повторная проверка 101 цепочки

| Результат | Количество |
|---|---:|
| no complete evidence example | 76 |
| reproduced example | 24 |
| partial example | 1 |

Отсутствие полного примера в данных не означает невозможность. Буквальное совпадение примера не гарантирует совместимость редакций и диалектов.

## Четыре новые цепочки, не сопоставленные со всеми рёбрами

- `bʰ → pʰ → ɸ` — маркеры `✶ → AQ.`; требуется проверка формулы и исходного представления.
- `bʰ → pʰ → ɸ → f` — маркеры `✶ → AQ. → Q.`; требуется проверка формулы и исходного представления.
- `dʰ → tʰ → θ` — маркеры `✶ → AQ.`; требуется проверка формулы и исходного представления.
- `dʰ → tʰ → θ → s` — маркеры `✶ → AQ. → Q.`; требуется проверка формулы и исходного представления.

## Все 101 цепочка: новая техническая проверка

| № | Звуковая линия | Технический результат | Полных примеров |
|---:|---|---|---:|
| 1 | `pʰt → ptʰ → pt → ɸt` | no complete evidence example | 0 |
| 2 | `pʰtʰ → ptʰ → pt → ɸt` | no complete evidence example | 0 |
| 3 | `ŋ- → ŋg- → ŋ- → ø-` | no complete evidence example | 0 |
| 4 | `kʰt → ktʰ → kt → xt` | no complete evidence example | 0 |
| 5 | `pʰt → ptʰ → pt → ps` | no complete evidence example | 0 |
| 6 | `pʰt → ptʰ → pt → xt` | no complete evidence example | 0 |
| 7 | `sb → zb → sp → ps` | no complete evidence example | 0 |
| 8 | `sg → zg → sk → ks` | no complete evidence example | 0 |
| 9 | `ŋ → g → ɣ → ø` | no complete evidence example | 0 |
| 10 | `ŋ → g → ɣ → ø` | no complete evidence example | 0 |
| 11 | `ɣ → g → ɣ → ø` | no complete evidence example | 0 |
| 12 | `ɣ → g → ɣ → ø` | no complete evidence example | 0 |
| 13 | `ae → ā → ō` | no complete evidence example | 0 |
| 14 | `ao → ā → ō` | no complete evidence example | 0 |
| 15 | `b → β → v` | reproduced example | 10 |
| 16 | `bd → pt → ɸt` | reproduced example | 1 |
| 17 | `bm → mm → m` | no complete evidence example | 0 |
| 18 | `bm → mb → mm` | no complete evidence example | 0 |
| 19 | `d → ð → z` | no complete evidence example | 0 |
| 20 | `g → ɣ → ø` | reproduced example | 10 |
| 21 | `gd → kt → xt` | reproduced example | 1 |
| 22 | `gj → dj → dʒ` | no complete evidence example | 0 |
| 23 | `gj → dj → dʒ` | no complete evidence example | 0 |
| 24 | `gj → dj → lj` | no complete evidence example | 0 |
| 25 | `gt → kt → xt` | reproduced example | 5 |
| 26 | `kj → tj → tʃ` | no complete evidence example | 0 |
| 27 | `kn → kt → xt` | reproduced example | 1 |
| 28 | `ktʰ → kt → xt` | reproduced example | 1 |
| 29 | `kʰ → x → h` | reproduced example | 9 |
| 30 | `mm → mb → mm` | no complete evidence example | 0 |
| 31 | `nn → nd → nn` | no complete evidence example | 0 |
| 32 | `pm → pw → pp` | reproduced example | 1 |
| 33 | `pn → pt → ɸt` | no complete evidence example | 0 |
| 34 | `ptʰ → pt → ɸt` | no complete evidence example | 0 |
| 35 | `pʰ → ɸ → f` | reproduced example | 10 |
| 36 | `pʰt → ptʰ → pt` | no complete evidence example | 0 |
| 37 | `pʰtʰ → ptʰ → pt` | no complete evidence example | 0 |
| 38 | `pʰw → ppʰ → pp` | no complete evidence example | 0 |
| 39 | `sd → zd → st` | partial example | 0 |
| 40 | `sg → zg → ðɣ` | no complete evidence example | 0 |
| 41 | `sj → zj → ʒ` | no complete evidence example | 0 |
| 42 | `tk → sk → ks` | no complete evidence example | 0 |
| 43 | `tk → kt → xt` | no complete evidence example | 0 |
| 44 | `tʰ → θ → s` | reproduced example | 10 |
| 45 | `tʰt → ttʰ → tt` | no complete evidence example | 0 |
| 46 | `tʰt → ttʰ → θθ` | no complete evidence example | 0 |
| 47 | `tʰtʰ → ttʰ → tt` | no complete evidence example | 0 |
| 48 | `tʰtʰ → ttʰ → θθ` | no complete evidence example | 0 |
| 49 | `zm → mm → m` | no complete evidence example | 0 |
| 50 | `ā → ǭ → ā` | no complete evidence example | 0 |
| 51 | `ā → ǭ → ō` | no complete evidence example | 0 |
| 52 | `ā → ǭ → ō` | no complete evidence example | 0 |
| 53 | `ŋ- → ŋg- → g-` | no complete evidence example | 0 |
| 54 | `ŋ- → ŋg- → g-` | no complete evidence example | 0 |
| 55 | `ŋ- → ŋg- → g-` | no complete evidence example | 0 |
| 56 | `ŋ- → ŋg- → ŋ-` | no complete evidence example | 0 |
| 57 | `ŋg- → ŋ- → g-` | no complete evidence example | 0 |
| 58 | `ŋg- → ŋ- → ø-` | no complete evidence example | 0 |
| 59 | `ŋg- → ŋ- → ø-` | no complete evidence example | 0 |
| 60 | `ŋg- → ŋ- → ø-` | no complete evidence example | 0 |
| 61 | `ŋgj → ndj → nj` | no complete evidence example | 0 |
| 62 | `ŋgw → mb → mm` | no complete evidence example | 0 |
| 63 | `ŋs → ns → ss` | no complete evidence example | 0 |
| 64 | `Vp → Vb → Vv` | no complete evidence example | 0 |
| 65 | `Vp → Vb → Vv` | no complete evidence example | 0 |
| 66 | `Vt → Vd → Vð` | no complete evidence example | 0 |
| 67 | `bd → pt → ps` | reproduced example | 2 |
| 68 | `bd → pt → xt` | no complete evidence example | 0 |
| 69 | `bt → pt → ps` | reproduced example | 2 |
| 70 | `bt → pt → xt` | no complete evidence example | 0 |
| 71 | `dm → nm → nw` | reproduced example | 1 |
| 72 | `g → ɣ → ø` | reproduced example | 10 |
| 73 | `g → ɣ → ø` | no complete evidence example | 0 |
| 74 | `gm → ŋm → ŋgw` | reproduced example | 10 |
| 75 | `gt → kt → xt` | no complete evidence example | 0 |
| 76 | `kd → kt → xt` | no complete evidence example | 0 |
| 77 | `ktʰ → kt → xt` | no complete evidence example | 0 |
| 78 | `kʰ → x → h` | reproduced example | 8 |
| 79 | `kʰn → kt → xt` | reproduced example | 1 |
| 80 | `kʰt → ktʰ → kt` | no complete evidence example | 0 |
| 81 | `nd- → d- → l-` | no complete evidence example | 0 |
| 82 | `nd- → d- → l-` | no complete evidence example | 0 |
| 83 | `ptʰ → pt → ps` | no complete evidence example | 0 |
| 84 | `ptʰ → pt → xt` | no complete evidence example | 0 |
| 85 | `pʰ → ɸ → f` | reproduced example | 10 |
| 86 | `pʰ → ɸ → f` | reproduced example | 9 |
| 87 | `pʰm → mpʰ → ppʰ` | no complete evidence example | 0 |
| 88 | `pʰt → ptʰ → pt` | no complete evidence example | 0 |
| 89 | `sb → zb → sp` | no complete evidence example | 0 |
| 90 | `sd → zd → st` | no complete evidence example | 0 |
| 91 | `sg → zg → sk` | reproduced example | 7 |
| 92 | `skʰ → sk → ks` | no complete evidence example | 0 |
| 93 | `tʰ → θ → s` | reproduced example | 10 |
| 94 | `tʰ → θ → s` | no complete evidence example | 0 |
| 95 | `tʰ → θ → s` | reproduced example | 1 |
| 96 | `tʰ → θ → s` | reproduced example | 6 |
| 97 | `zb → sp → ps` | no complete evidence example | 0 |
| 98 | `zg → sk → ks` | no complete evidence example | 0 |
| 99 | `ŋ → g → ɣ` | no complete evidence example | 0 |
| 100 | `ŋgj → ndj → nj` | no complete evidence example | 0 |
| 101 | `ɣ → g → ɣ` | no complete evidence example | 0 |

## Новые 27 цепочек: структурный аудит

| № | Звуковая линия | Маркеры | Все рёбра сопоставлены |
|---:|---|---|---|
| 1 | `mpʰ → ppʰ → pp` | AQ. → Q. | True |
| 2 | `zb → sp → ps` | AQ. → Q. | True |
| 3 | `zg → sk → ks` | AQ. → Q. | True |
| 4 | `xw → w̥ → f` | AQ. → Q. | True |
| 5 | `bt → pt → ɸt` | ✶ → Q. | True |
| 6 | `bʰ → pʰ → ɸ` | ✶ → AQ. | False |
| 7 | `bʰ → pʰ → ɸ → f` | ✶ → AQ. → Q. | False |
| 8 | `pp → ppʰ → pp` | ✶ → Q. | True |
| 9 | `pp → ppʰ → pp` | ✶ → AQ. | True |
| 10 | `tp → tpʰ → tp` | ✶ → Q. | True |
| 11 | `kp → kpʰ → kp` | ✶ → Q. | True |
| 12 | `mp → mpʰ → ppʰ` | ✶ → AQ. | True |
| 13 | `mp → mpʰ → ppʰ → pp` | ✶ → AQ. → Q. | True |
| 14 | `pd → pt → ɸt` | AQ. → Q. | True |
| 15 | `kd → kt → xt` | AQ. → Q. | True |
| 16 | `dʰ → tʰ → θ` | ✶ → AQ. | False |
| 17 | `dʰ → tʰ → θ → s` | ✶ → AQ. → Q. | False |
| 18 | `pd → pt → ɸt` | ✶ → Q. | True |
| 19 | `kd → kt → xt` | ✶ → Q. | True |
| 20 | `ptʰ → pt → ɸt` | ✶ → Q. | True |
| 21 | `ktʰ → kt → xt` | ✶ → Q. | True |
| 22 | `pʰw → ppʰ → pp` | ✶ → Q. | True |
| 23 | `bt → pt → ɸt` | AQ. → Q. | True |
| 24 | `sb → zb → sp` | ✶ → AQ. | True |
| 25 | `sb → zb → sp → ps` | ✶ → AQ. → Q. | True |
| 26 | `sg → zg → sk` | ✶ → AQ. | True |
| 27 | `sg → zg → sk → ks` | ✶ → AQ. → Q. | True |

## Воспроизведение и данные

- `eldamo_interpreter_v2.py` — исполнитель с тестами (запуск `python eldamo_interpreter_v2.py`).
- `run_eldamo_v2_complete.py` — основной прогон, требует файлы инвентаря, 101 линий, 27 кандидатов и свидетельств из предыдущего этапа.
- `eldamo_v2_all_rules.csv` — инвентарь и синтаксические результаты.
- `eldamo_v2_recovered_exclusions.csv` — 155 ранее пропущенных записей.
- `eldamo_v2_101_recheck.csv` — оценки применимости по доступным словоформам.
- `eldamo_v2_27_recheck.csv` — контроль 27 кандидатов.
- `eldamo_v2_structural_candidates.csv` — 114 путей нового строгого атомарного графа.

## Вывод

Набор ранее отброшенных формул повторно обработан, но без выдуманных улучшений статуса цепочек. Следующий критический шаг для действительно всеохватывающей системы — формальная спецификация всей нотации Eldamo по её собственной документации и полнотекстовая проверка примеров правила, включая условия, описанные словами.
