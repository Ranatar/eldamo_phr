# Eldamo v8 — ограничения канонических и архивных цепочек

Все сведения взяты только из включённых данных Eldamo и файлов проекта v7. Неизвестное не превращено в утверждение о фонологии.

**Ни один формально корректный переход не считается доказанной историей слова только по наличию графового пути.**

## Поцепочечные проверки

### quenya

| Проверяемое обстоятельство | Количество цепочек |
|---|---:|
| `same_stage_order_unverified` | 92 |
| `different_position_requirements` | 0 |
| `contextual_rules_not_considered` | 216 |
| `relative_chronology_unverified` | 216 |
| `authorial_revision_compatibility_unverified` | 216 |
| `ambiguous_atomic_match` | 2 |
| `merged_rule_provenance` | 211 |
| `without_shared_example_witness` | 178 |
| `total` | 216 |

Контекстных/неатомарных записей: 139; они сохранены и не заявляются как исполняемые рёбра.

### Архивные цепочки — quenya

**critical**: {'graph_steps_verified': 66, 'unresolved_steps': 73}; статусы шагов: {'exact_step_match': 197, 'not_in_atomic_graph': 88, 'missing_chain_rule_url': 8, 'rule_url_mismatch': 3}

**structural**: {'graph_steps_verified': 208, 'unresolved_steps': 6, 'ambiguous_rule_identity': 2}; статусы шагов: {'exact_step_match': 473, 'missing_chain_rule_url': 6, 'multiple_matching_rules': 2}

### sindarin

| Проверяемое обстоятельство | Количество цепочек |
|---|---:|
| `same_stage_order_unverified` | 48 |
| `different_position_requirements` | 0 |
| `contextual_rules_not_considered` | 114 |
| `relative_chronology_unverified` | 114 |
| `authorial_revision_compatibility_unverified` | 114 |
| `ambiguous_atomic_match` | 0 |
| `merged_rule_provenance` | 110 |
| `without_shared_example_witness` | 103 |
| `total` | 114 |

Контекстных/неатомарных записей: 150; они сохранены и не заявляются как исполняемые рёбра.

### Архивные цепочки — sindarin

**critical**: {'graph_steps_verified': 102, 'unresolved_steps': 11, 'incompatible_position': 5}; статусы шагов: {'exact_step_match': 259, 'missing_chain_rule_url': 11}

**structural**: {'graph_steps_verified': 106, 'unresolved_steps': 8}; статусы шагов: {'exact_step_match': 251, 'missing_chain_rule_url': 8}

## Принципиальные ограничения

- Порядок правил внутри одной языковой ступени не восстановлен по рукописям; `same_stage_order_unverified` выделяет особенно явные случаи.
- Воспроизведение отдельных правил на примерах не означает, что все правила можно последовательно применить к одной исторической форме.
- Совпадающие ссылки на словарные статьи и библиографические обозначения являются машинными свидетельствами, не текстологической экспертизой.
- `archival_gap_register_v8.json` не трактует отсутствие в атомарном графе как опровержение правила; он фиксирует наблюдаемую причину технического разрыва.
- Сложные формулы не превращены в безусловные стрелки: это привело бы к ложным результатам.
- Невозможно корректно присвоить окончательные исторические A/B оценки по имеющимся автоматизированным проверкам.

## Воспроизводимые файлы

`branches/{quenya,sindarin}/data/historical_limit_ledger_v8.json`, `archival_gap_register_v8.json`, `reports/v8_canonical_chain_limits.csv`, `reports/v8_historical_limit_summary.json`.
