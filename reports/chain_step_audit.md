# Проверка индивидуальных шагов цепочек (v4)

Аудит строго сопоставляет период, входной и выходной звук и URL конкретного правила с атомарным графом.
Это проверка происхождения данных, **не** доказательство применения всей истории к одной словоформе.

## quenya

### critical

- `chain:graph_steps_verified`: 66
- `chain:unresolved_steps`: 73
- `exact_step_match`: 197
- `missing_chain_rule_url`: 8
- `not_in_atomic_graph`: 88
- `rule_url_mismatch`: 3

### structural

- `chain:ambiguous_rule_identity`: 2
- `chain:graph_steps_verified`: 208
- `chain:unresolved_steps`: 6
- `exact_step_match`: 473
- `missing_chain_rule_url`: 6
- `multiple_matching_rules`: 2

## sindarin

### critical

- `chain:graph_steps_verified`: 102
- `chain:incompatible_position`: 5
- `chain:unresolved_steps`: 11
- `exact_step_match`: 259
- `missing_chain_rule_url`: 11

### structural

- `chain:graph_steps_verified`: 106
- `chain:unresolved_steps`: 8
- `exact_step_match`: 251
- `missing_chain_rule_url`: 8

Отсутствие шага в атомарном графе означает несоответствие **моделей представления**, не опровержение звукового закона.
Подробности по каждому шагу: `branches/<branch>/data/chain_step_provenance.json`; проблемные случаи: `reports/chain_step_audit.json`.
