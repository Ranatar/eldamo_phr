# Проверка сквозных фонетических цепочек Eldamo 0.8.13: строгий этап

## Метод и границы доказательства

Исследованы 101 формальный кандидат и примеры в HTML-карточках фонетических правил из локального архива. Для полной последовательности требуется: (1) соответствие формулы в каждой строке примера ребру графа; (2) буквальное равенство промежуточных **словоформ**; (3) общий идентификатор словарной статьи **на всех шагах**; (4) одинаковая библиографическая ссылка **на всех шагах**; (5) отсутствие метки `deleted-section` для приоритетного класса; (6) принадлежность страниц правила к одному из шести рассматриваемых языковых каталогов.

**Статус «подтверждена история слова» не присваивается автоматически**: одинаковая библиографическая ссылка не удостоверяет порядок реализации законов, условия и редакционную совместимость. Встречающиеся в заметках оговорки требуют отдельной филологической интерпретации.

## Статистика

| Машинный статус | Цепочек |
|---|---:|
| `LANGUAGE_CONFLICT_REVIEW` | 45 |
| `NO_CONTINUOUS_WORD_FORMS` | 33 |
| `COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW` | 19 |
| `ANNOTATION_OR_UNCHANGED_FORM_REVIEW` | 2 |
| `ONLY_OBSOLETE_OR_DELETED_EXAMPLES` | 1 |
| `FORM_CHAIN_WITHOUT_COMMON_SOURCE_AND_ARTICLE` | 1 |

Полных склеек с одинаковой статьёй и источником, без явной пометы удалённого примера, на страницах шести целевых языков: **19 цепочек**. Это **кандидаты на углублённую филологическую проверку**, а не окончательные реконструкции.

## Приоритетные линии со сквозными примерами

| ID | Звуковая линия | Полные формы | Первичный источник | Статус |
|---:|---|---|---|---|
| 15 | `b → β → v` | `aubie → auβie → auvie` | ✧ PE22/151 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 20 | `g → ɣ → ø` | `agwalda → aɣwalda → awalda` | ✧ PE17/189 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 21 | `gd → kt → xt` | `negdē → nektē → nextē` | ✧ PE19/91 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 25 | `gt → kt → xt` | `magta- → makta- → maxta-` | ✧ PE17/161 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 27 | `kn → kt → xt` | `paknā → paktā → paxtā` | ✧ PE17/171 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 28 | `ktʰ → kt → xt` | `naktʰa- → nakta- → naxta-` | ✧ PE17/166 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 29 | `kʰ → x → h` | `nākʰa → naxa → naha` | ✧ PE17/166 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 32 | `pm → pw → pp` | `napma → napwa → nappa` | ✧ VT47/20 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 35 | `pʰ → ɸ → f` | `rapʰe → raɸe → rafe` | ✧ PE19/89 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 44 | `tʰ → θ → s` | `atʰa- → aθa- → asa-` | ✧ PE17/148 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 67 | `bd → pt → ps` | `labdā → laptā → lapsā` | ✧ PE19/45 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 69 | `bt → pt → ps` | `abta- → apta- → apsa-` | ✧ PE19/45 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 71 | `dm → nm → nw` | `jadmē → janmē → janwē` | ✧ Ety/YAT | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 72 | `g → ɣ → ø` | `ga → ɣa → a` | ✧ PE22/94 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 74 | `gm → ŋm → ŋgw` | `nagma → naŋma → naŋgwa` | ✧ Ety/NAK | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 79 | `kʰn → kt → xt` | `lakʰne → lakte → laxte` | ✧ PE22/103 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 85 | `pʰ → ɸ → f` | `rapʰe → raɸe → rafe` | ✧ PE22/102 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 91 | `sg → zg → sk` | `lisge → lizge → liske` | ✧ PE19/51 | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |
| 93 | `tʰ → θ → s` | `itʰil → iθil → isil` | ✧ Ety/I² | COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW |

## Случаи, требующие отдельной проверки

| ID | Звуки | Причина |
|---:|---|---|
| 3 | `ŋ- → ŋg- → ŋ- → ø-` | `LANGUAGE_CONFLICT_REVIEW` |
| 9 | `ŋ → g → ɣ → ø` | `LANGUAGE_CONFLICT_REVIEW` |
| 10 | `ŋ → g → ɣ → ø` | `LANGUAGE_CONFLICT_REVIEW` |
| 11 | `ɣ → g → ɣ → ø` | `LANGUAGE_CONFLICT_REVIEW` |
| 12 | `ɣ → g → ɣ → ø` | `LANGUAGE_CONFLICT_REVIEW` |
| 13 | `ae → ā → ō` | `LANGUAGE_CONFLICT_REVIEW` |
| 14 | `ao → ā → ō` | `LANGUAGE_CONFLICT_REVIEW` |
| 16 | `bd → pt → ɸt` | `ONLY_OBSOLETE_OR_DELETED_EXAMPLES` |
| 17 | `bm → mm → m` | `LANGUAGE_CONFLICT_REVIEW` |
| 18 | `bm → mb → mm` | `LANGUAGE_CONFLICT_REVIEW` |
| 19 | `d → ð → z` | `LANGUAGE_CONFLICT_REVIEW` |
| 22 | `gj → dj → dʒ` | `LANGUAGE_CONFLICT_REVIEW` |
| 23 | `gj → dj → dʒ` | `LANGUAGE_CONFLICT_REVIEW` |
| 24 | `gj → dj → lj` | `LANGUAGE_CONFLICT_REVIEW` |
| 26 | `kj → tj → tʃ` | `LANGUAGE_CONFLICT_REVIEW` |
| 30 | `mm → mb → mm` | `LANGUAGE_CONFLICT_REVIEW` |
| 31 | `nn → nd → nn` | `LANGUAGE_CONFLICT_REVIEW` |
| 39 | `sd → zd → st` | `ANNOTATION_OR_UNCHANGED_FORM_REVIEW` |
| 40 | `sg → zg → ðɣ` | `LANGUAGE_CONFLICT_REVIEW` |
| 41 | `sj → zj → ʒ` | `LANGUAGE_CONFLICT_REVIEW` |
| 46 | `tʰt → ttʰ → θθ` | `LANGUAGE_CONFLICT_REVIEW` |
| 48 | `tʰtʰ → ttʰ → θθ` | `LANGUAGE_CONFLICT_REVIEW` |
| 49 | `zm → mm → m` | `LANGUAGE_CONFLICT_REVIEW` |
| 50 | `ā → ǭ → ā` | `LANGUAGE_CONFLICT_REVIEW` |
| 51 | `ā → ǭ → ō` | `LANGUAGE_CONFLICT_REVIEW` |
| 52 | `ā → ǭ → ō` | `LANGUAGE_CONFLICT_REVIEW` |
| 53 | `ŋ- → ŋg- → g-` | `LANGUAGE_CONFLICT_REVIEW` |
| 54 | `ŋ- → ŋg- → g-` | `LANGUAGE_CONFLICT_REVIEW` |
| 55 | `ŋ- → ŋg- → g-` | `LANGUAGE_CONFLICT_REVIEW` |
| 56 | `ŋ- → ŋg- → ŋ-` | `LANGUAGE_CONFLICT_REVIEW` |
| 57 | `ŋg- → ŋ- → g-` | `LANGUAGE_CONFLICT_REVIEW` |
| 58 | `ŋg- → ŋ- → ø-` | `LANGUAGE_CONFLICT_REVIEW` |
| 59 | `ŋg- → ŋ- → ø-` | `LANGUAGE_CONFLICT_REVIEW` |
| 60 | `ŋg- → ŋ- → ø-` | `LANGUAGE_CONFLICT_REVIEW` |
| 62 | `ŋgw → mb → mm` | `LANGUAGE_CONFLICT_REVIEW` |
| 64 | `Vp → Vb → Vv` | `LANGUAGE_CONFLICT_REVIEW` |
| 65 | `Vp → Vb → Vv` | `LANGUAGE_CONFLICT_REVIEW` |
| 66 | `Vt → Vd → Vð` | `LANGUAGE_CONFLICT_REVIEW` |
| 73 | `g → ɣ → ø` | `LANGUAGE_CONFLICT_REVIEW` |
| 78 | `kʰ → x → h` | `ANNOTATION_OR_UNCHANGED_FORM_REVIEW` |
| 81 | `nd- → d- → l-` | `LANGUAGE_CONFLICT_REVIEW` |
| 82 | `nd- → d- → l-` | `LANGUAGE_CONFLICT_REVIEW` |
| 86 | `pʰ → ɸ → f` | `LANGUAGE_CONFLICT_REVIEW` |
| 90 | `sd → zd → st` | `FORM_CHAIN_WITHOUT_COMMON_SOURCE_AND_ARTICLE` |
| 94 | `tʰ → θ → s` | `LANGUAGE_CONFLICT_REVIEW` |
| 95 | `tʰ → θ → s` | `LANGUAGE_CONFLICT_REVIEW` |
| 96 | `tʰ → θ → s` | `LANGUAGE_CONFLICT_REVIEW` |
| 99 | `ŋ → g → ɣ` | `LANGUAGE_CONFLICT_REVIEW` |
| 101 | `ɣ → g → ɣ` | `LANGUAGE_CONFLICT_REVIEW` |

## Как читать данные

- `eldamo_strict_chain_audit.csv` — отдельный статус для всех 101 цепочек.
- `eldamo_strict_chain_evidence.csv` — примеры с одинаковой ссылкой на статью и первоисточник, до 10 для каждой цепочки.
- Поля `languages` и `rule_urls` помогают перепроверить, не происходит ли смешение Telerin/Sindarin с Quenya.
- `commentary_warning_terms` — сигнальные слова из пояснений, а не автоматическая интерпретация исключений.
- Этот этап ограничен исходными 101 кандидатами, полученными упрощённым графом; он не доказывает полноту всех возможных звуковых цепочек.
