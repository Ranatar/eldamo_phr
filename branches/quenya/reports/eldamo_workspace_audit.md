# Аудит рабочей папки Eldamo

Дата: 2026-10-23. Изучено 86 файлов верхнего уровня `/mnt/data`; служебная папка `__pycache__` не включена. Итоговый архив: `eldamo_integrated_research_package_ipa.zip` (16 записей).

## Метод проверки

Сопоставлены реальные имена и **байты файлов** с содержимым ZIP. Статусы характеризуют пригодность для текущего проекта, а не историческую истинность всех полученных результатов. Часть промежуточных материалов полезна для истории исследования, но не должна подменять текущий результат.

## Количество файлов по группам

| Группа | Число |
|---|---:|
| Актуальные скрипты воспроизведения | 17 |
| Историческая промежуточная версия | 35 |
| Исходник (сохранить отдельно) | 1 |
| Актуальный финальный продукт | 6 |
| Актуальное ядро и данные | 27 |

## Актуальные материалы, отсутствующие в последнем ZIP

### Актуальные скрипты воспроизведения

- `audit_eldamo_paths.py`
- `build_eldamo_critical_atlas.py`
- `build_eldamo_paths.py`
- `eldamo_extended_audit.py`
- `eldamo_new_path_candidates.py`
- `eldamo_textual_review.py`
- `eldamo_v3_final_report.py`
- `eldamo_v3_graph_audit.py`
- `eldamo_v3_report_builder.py`
- `eldamo_v3_rule_level_chain_audit.py`
- `run_eldamo_v3_validation.py`
- `verify_eldamo_strict.py`
- `verify_eldamo_word_paths.py`

### Актуальное ядро и данные

- `eldamo_critical_101_atlas.csv`
- `eldamo_critical_101_atlas.md`
- `eldamo_etymological_chain_verification.md`
- `eldamo_exact_word_joins.csv`
- `eldamo_new_atomic_candidates.csv`
- `eldamo_paths_context_audit.csv`
- `eldamo_paths_context_report.md`
- `eldamo_rule_commentary_audit.csv`
- `eldamo_sound_candidate_paths.csv`
- `eldamo_sound_edges.csv`
- `eldamo_sound_graph.graphml`
- `eldamo_strict_chain_audit.csv`
- `eldamo_strict_chain_evidence.csv`
- `eldamo_strict_chain_report.md`
- `eldamo_textual_chain_assessment.csv`
- `eldamo_textual_chain_report.md`
- `eldamo_v2_recovered_exclusions.csv`
- `eldamo_v3_101_reassessment.csv`
- `eldamo_v3_27_reassessment.csv`
- `eldamo_word_chain_validation.csv`

## Особенности последнего архива

- В ZIP встроен **новый** HTML под универсальным именем `eldamo_sound_path_explorer.html`. Он побайтово совпадает с локальным `eldamo_sound_path_explorer_ipa.html`, но **не совпадает** с локальным файлом `eldamo_sound_path_explorer.html` (старый интерфейс).
- Исходный `eldamo-0.8.13.zip` отсутствует в интегрированном ZIP (78 МБ), так что автономно воспроизвести экстракцию правил нельзя.
- В ZIP отсутствует `run_eldamo_v3_validation.py`; одного `eldamo_interpreter_v3.py` недостаточно для воспроизведения всего аудита.
- Скрипт `update_eldamo_explorer_ipa.py` использует в рабочей папке предыдущий HTML и предыдущий ZIP; последний пакет сам по себе не предоставляет исходные входные файлы в ожидаемых местах.
- Расширенная доказательная база из отдельных отчётов по 101 цепочке не включена, хотя позволяет проверить обоснование рейтингов и проблемные свидетельства.

## Полный реестр

| Файл | Статус | В итоговом ZIP |
|---|---|---|
| `audit_eldamo_paths.py` | Актуальные скрипты воспроизведения | Нет |
| `build_eldamo_corrected.py` | Актуальные скрипты воспроизведения | Да |
| `build_eldamo_critical_atlas.py` | Актуальные скрипты воспроизведения | Нет |
| `build_eldamo_explorer.py` | Актуальные скрипты воспроизведения | Да |
| `build_eldamo_paths.py` | Актуальные скрипты воспроизведения | Нет |
| `check_explorer.js` | Историческая промежуточная версия | Нет |
| `check_explorer_ipa.js` | Историческая промежуточная версия | Нет |
| `eldamo-0.8.13.zip` | Исходник (сохранить отдельно) | Нет |
| `eldamo_101_stage_reassessment.csv` | Актуальный финальный продукт | Да |
| `eldamo_context_chain_audit.csv` | Историческая промежуточная версия | Нет |
| `eldamo_context_example_tests.csv` | Историческая промежуточная версия | Нет |
| `eldamo_context_interpreter.py` | Историческая промежуточная версия | Нет |
| `eldamo_context_interpreter_report.md` | Историческая промежуточная версия | Нет |
| `eldamo_critical_101_atlas.csv` | Актуальное ядро и данные | Нет |
| `eldamo_critical_101_atlas.md` | Актуальное ядро и данные | Нет |
| `eldamo_etymological_chain_verification.md` | Актуальное ядро и данные | Нет |
| `eldamo_exact_word_joins.csv` | Актуальное ядро и данные | Нет |
| `eldamo_explorer_and_chronology_report.md` | Актуальный финальный продукт | Да |
| `eldamo_extended_101_reassessment.csv` | Историческая промежуточная версия | Нет |
| `eldamo_extended_analysis_report.md` | Историческая промежуточная версия | Нет |
| `eldamo_extended_audit.py` | Актуальные скрипты воспроизведения | Нет |
| `eldamo_extended_rule_inventory.csv` | Историческая промежуточная версия | Нет |
| `eldamo_full_catalog.py` | Историческая промежуточная версия | Нет |
| `eldamo_integrated_research_package.zip` | Историческая промежуточная версия | Нет |
| `eldamo_integrated_research_package_ipa.zip` | Актуальный финальный продукт | Это итоговый архив |
| `eldamo_interpreter_v2.py` | Историческая промежуточная версия | Нет |
| `eldamo_interpreter_v3.py` | Актуальное ядро и данные | Да |
| `eldamo_new_atomic_candidates.csv` | Актуальное ядро и данные | Нет |
| `eldamo_new_path_candidates.py` | Актуальные скрипты воспроизведения | Нет |
| `eldamo_order_and_context_clues.csv` | Актуальный финальный продукт | Да |
| `eldamo_paths_context_audit.csv` | Актуальное ядро и данные | Нет |
| `eldamo_paths_context_report.md` | Актуальное ядро и данные | Нет |
| `eldamo_quenya_ancient_quenya_by_phoneme.md` | Историческая промежуточная версия | Нет |
| `eldamo_quenya_ancient_quenya_complete_tables_v2.md` | Историческая промежуточная версия | Нет |
| `eldamo_quenya_ancient_quenya_deduplicated.md` | Историческая промежуточная версия | Нет |
| `eldamo_quenya_ancient_quenya_full.md` | Историческая промежуточная версия | Нет |
| `eldamo_quenya_ancient_quenya_ipa_navigation.md` | Историческая промежуточная версия | Нет |
| `eldamo_quenya_ancient_quenya_tables.md` | Историческая промежуточная версия | Нет |
| `eldamo_quenya_phonetics.md` | Историческая промежуточная версия | Нет |
| `eldamo_quenya_phonetics_revised.md` | Историческая промежуточная версия | Нет |
| `eldamo_recovered_exclusions.csv` | Историческая промежуточная версия | Нет |
| `eldamo_rule_commentary_audit.csv` | Актуальное ядро и данные | Нет |
| `eldamo_six_languages_ipa_catalog.md` | Актуальный финальный продукт | Да |
| `eldamo_sound_candidate_paths.csv` | Актуальное ядро и данные | Нет |
| `eldamo_sound_edges.csv` | Актуальное ядро и данные | Нет |
| `eldamo_sound_graph.graphml` | Актуальное ядро и данные | Нет |
| `eldamo_sound_path_explorer.html` | Историческая промежуточная версия | Нет: имя совпадает, содержимое отличается |
| `eldamo_sound_path_explorer_ipa.html` | Актуальный финальный продукт | Да, под именем eldamo_sound_path_explorer.html |
| `eldamo_sound_paths_report.md` | Историческая промежуточная версия | Нет |
| `eldamo_strict_chain_audit.csv` | Актуальное ядро и данные | Нет |
| `eldamo_strict_chain_evidence.csv` | Актуальное ядро и данные | Нет |
| `eldamo_strict_chain_report.md` | Актуальное ядро и данные | Нет |
| `eldamo_textual_chain_assessment.csv` | Актуальное ядро и данные | Нет |
| `eldamo_textual_chain_report.md` | Актуальное ядро и данные | Нет |
| `eldamo_textual_review.py` | Актуальные скрипты воспроизведения | Нет |
| `eldamo_v2_101_recheck.csv` | Историческая промежуточная версия | Нет |
| `eldamo_v2_27_recheck.csv` | Историческая промежуточная версия | Нет |
| `eldamo_v2_all_rules.csv` | Актуальное ядро и данные | Да |
| `eldamo_v2_recovered_exclusions.csv` | Актуальное ядро и данные | Нет |
| `eldamo_v2_report.md` | Историческая промежуточная версия | Нет |
| `eldamo_v2_structural_candidates.csv` | Историческая промежуточная версия | Нет |
| `eldamo_v3_101_reassessment.csv` | Актуальное ядро и данные | Нет |
| `eldamo_v3_101_rule_level_audit.csv` | Актуальное ядро и данные | Да |
| `eldamo_v3_27_normalized_reassessment.csv` | Актуальное ядро и данные | Да |
| `eldamo_v3_27_reassessment.csv` | Актуальное ядро и данные | Нет |
| `eldamo_v3_comprehensive_audit.md` | Актуальное ядро и данные | Да |
| `eldamo_v3_final_report.py` | Актуальные скрипты воспроизведения | Нет |
| `eldamo_v3_graph_audit.py` | Актуальные скрипты воспроизведения | Нет |
| `eldamo_v3_rebuilt_structural_graph.csv` | Актуальное ядро и данные | Да |
| `eldamo_v3_report_builder.py` | Актуальные скрипты воспроизведения | Нет |
| `eldamo_v3_research_bundle.zip` | Историческая промежуточная версия | Нет |
| `eldamo_v3_rule_example_validation.csv` | Актуальное ядро и данные | Да |
| `eldamo_v3_rule_level_chain_audit.py` | Актуальные скрипты воспроизведения | Нет |
| `eldamo_v3_summary.json` | Историческая промежуточная версия | Нет |
| `eldamo_word_chain_validation.csv` | Актуальное ядро и данные | Нет |
| `make_context_report.py` | Историческая промежуточная версия | Нет |
| `make_eldamo_six.py` | Актуальные скрипты воспроизведения | Да |
| `make_eldamo_v2_report.py` | Историческая промежуточная версия | Нет |
| `make_word_verification_report.py` | Историческая промежуточная версия | Нет |
| `reformat_ipa.py` | Историческая промежуточная версия | Нет |
| `run_eldamo_context_audit.py` | Историческая промежуточная версия | Нет |
| `run_eldamo_v2_complete.py` | Историческая промежуточная версия | Нет |
| `run_eldamo_v3_validation.py` | Актуальные скрипты воспроизведения | Нет |
| `update_eldamo_explorer_ipa.py` | Актуальные скрипты воспроизведения | Да |
| `verify_eldamo_strict.py` | Актуальные скрипты воспроизведения | Нет |
| `verify_eldamo_word_paths.py` | Актуальные скрипты воспроизведения | Нет |

## Рекомендуемая компоновка нового архива

1. `app/` — последний HTML и данные поиска, без предыдущей версии под тем же именем.
2. `catalog/` — шестиязычный каталог и генераторы каталога.
3. `engine/` — v3 и все скрипты тестирования/валидации.
4. `evidence/` — прежние 101 цепочка, 27 кандидатов, полные таблицы примеров, текстологический и строгий аудиты, граф.
5. `reports/` — основные и промежуточные аналитические отчёты, чётко помеченные версиями.
6. `legacy/` (опционально) — старые варианты каталога и интерпретаторов; можно не включать в основной релиз.
7. `README.md` с точной последовательностью запуска и обязательной внешней зависимостью `eldamo-0.8.13.zip`.

## Ограничение аудита

Эта проверка устанавливает факт присутствия, побайтового совпадения и назначение файлов. Она не эквивалентна полному повторному тестированию всей фонетической модели.
