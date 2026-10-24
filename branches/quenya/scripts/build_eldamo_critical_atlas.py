import pandas as pd,re,collections,os
from urllib.parse import urlparse
P='/mnt/data/'
a=pd.read_csv(P+'eldamo_strict_chain_audit.csv').fillna('')
t=pd.read_csv(P+'eldamo_textual_chain_assessment.csv').fillna('')
c=pd.read_csv(P+'eldamo_rule_commentary_audit.csv').fillna('')
notes={r.rule_url:r for r in c.itertuples(index=False)}
prior={int(r.id):r for r in t.itertuples(index=False)}
rows=[]
for r in a.itertuples(index=False):
 id=int(r.id); urls=[u.strip() for u in str(r.rule_urls).split(' || ') if u.strip()]
 if len(urls)==1: urls=re.findall(r'https?://[^\s;,]+',str(r.rule_urls))
 # URL separator appears ';' or ' | ' inspect below
 if len(urls)<2: urls=re.findall(r'https?://eldamo\.org/content/words/word-\d+\.html',str(r.rule_urls))
 found=[notes[u] for u in urls if u in notes]
 ncnt=sum(bool(str(n.notes).strip()) for n in found)
 lang=[str(n.rule_language).strip() for n in found]
 unseen=len(urls)-len(found)
 st=r.status
 if id in prior:
  p=prior[id]
  grade='B' if p.assessment=='условно совместима' else 'C'
  if p.assessment=='диалектное ограничение': grade='B'
  if p.assessment=='требует первичного текста': grade='C'
  reason='Полный ряд словоформ с общими ссылками на словарную статью и источник; '+str(p.limitation).strip()
  nextstep=str(p.next_check).strip()
 elif st=='NO_CONTINUOUS_WORD_FORMS':
  grade='D'
  reason='Формулы состыкуются, но непрерывный этимологический ряд не найден. Это отсутствие прямого свидетельства, не опровержение.'
  nextstep='Проверить применимость условий к одному слову, порядок законов и наличие промежуточных форм.'
 elif st=='LANGUAGE_CONFLICT_REVIEW':
  grade='U'
  reason='Одна или несколько индивидуальных страниц правил относятся к языку вне заданной линии Quenya; необходимо установить, допустимо ли правило в рассматриваемой ветви.'
  nextstep='Прочесть языковую атрибуцию и пояснение каждого правила; не переносить закон из Sindarin/Telerin автоматически.'
 elif st=='ONLY_OBSOLETE_OR_DELETED_EXAMPLES':
  grade='U';reason='Найденное свидетельство помечено как устаревшее/удалённое; не установлено, устарела ли лишь словоформа или само правило.'
  nextstep='Разделить статус исторического закона и статус конкретного примера.'
 elif st=='ANNOTATION_OR_UNCHANGED_FORM_REVIEW':
  grade='U';reason='В примерах наблюдается неизменённый или двусмысленно аннотированный переход, который нельзя принимать за подтверждение.'
  nextstep='Сверить отдельные поля исходной/результирующей формы и условия в заметке.'
 else:
  grade='C';reason='Формы стыкуются, но нет единого свидетельства с одной статьёй и библиографической ссылкой на всю линию.'
  nextstep='Проверить историческую совместимость независимых свидетельств.'
 # notes used as *context signals*, not evidence of proof
 terms=sorted(set(x.strip() for n in found for x in str(n.caution_terms).split(',') if x.strip()))
 caution=[k for k in ('before','after','medial','initial','final','only','sometimes','dialect','alternative','later','earlier','possibly','probably','obsolete') if k in terms]
 rows.append(dict(id=id,states=r.states,era=r.era,grade=grade,previous_status=st,rules=r.rules,languages=r.languages,reason=reason,action=nextstep,example=r.example,source=r.matched_primary_source,article=r.matched_lexical_article,rule_urls=r.rule_urls,rule_page_count=len(urls),commentary_pages=ncnt,language_on_rule_page='; '.join(lang),caution_terms=', '.join(caution)))
d=pd.DataFrame(rows)
assert len(d)==101
assert list(d.id)==list(range(1,102))
d.to_csv(P+'eldamo_critical_101_atlas.csv',index=False)
ct=d.grade.value_counts().to_dict()
line=['# Eldamo 0.8.13 — критический атлас 101 кандидатной цепочки','','## Назначение и границы','', 'Переоценка **всех 101 механически построенных цепочек** по сведениям в каталоге Eldamo 0.8.13 и результатам предыдущего аудита. Библиографические цитаты Eldamo принимаются корректными в соответствии с условием исследования. Отдельной сверки печатных первоисточников нет.','', '**Ограничение:** оценки ниже — воспроизводимая *предварительная триаж-классификация*, не законченная ручная проверка каждой оговорки и относительной хронологии. Особенно важно: 19 линий с совпадающими примерами не превращаются автоматически в исторически доказанные.','', '## Шкала','', '| Код | Смысл |','|---|---|','| A | Полностью документированная и хронологически согласованная цепочка (не присвоено автоматически) |','| B | Согласованные словоформы и убедительная, но не окончательная интерпретация условий |','| C | Свидетельства частично согласованы; есть конкретная недостающая проверка |','| D | Формально композиционная линия без найденного целостного словарного ряда |','| U | Существенная неопределённость, препятствующая содержательной оценке |','| X | Доказанное нарушение условий или несовместимость редакций (не присвоено без прямого основания) |','','**Порядок шкалы A–D не является численной вероятностью.** U и X не помещаются на той же вероятностной оси.','', '## Распределение','', '| Категория | Количество |','|---|---:|']
for k in ['A','B','C','D','U','X']:line.append(f'| {k} | {ct.get(k,0)} |')
line += ['| **Итого** | **101** |','','## Почему предыдущие статусы не равны доказательству ошибки','', '- «Нет непрерывной словоформы» не означает, что последовательность невозможна.','- «Правило из другого языка» может означать ошибочный перенос, однако само по себе не доказывает невозможности: необходимо читать его описание.','- Слова из разных статей не подтверждают единый этимологический путь, но могут независимо демонстрировать последовательные законы.','- Маркеры Middle и позднего периода концепции нельзя соединять без специального доказательства совместимости.','- Для `ø` применяется условная запись исчезновения сегмента, требующая проверки окружения.','', '## Навигация по оценкам','']
for k in ['B','C','D','U']:
 ids=d[d.grade==k].id.tolist()
 line.append(f'**{k}**: '+', '.join(f'[№{i}](#цепочка-{i})' for i in ids)+'.')
 line.append('')
line += ['## Все 101 цепочка','']
for r in d.itertuples(index=False):
 line.extend([f'### Цепочка {r.id}', '',f'**{r.states}** · концепция: **{r.era}** · оценка: **{r.grade}**','',f'- **Языковые привязки прежнего графа:** {r.languages or "не указаны"}.',f'- **Правила:** {r.rules}.',f'- **Основание оценки:** {r.reason}',f'- **Что необходимо установить:** {r.action}',f'- **Предыдущий машинный статус:** `{r.previous_status}`.',f'- **Пояснения на индивидуальных страницах:** {r.commentary_pages} из {r.rule_page_count} доступных в индексе заметок.' ])
 if r.caution_terms:line.append(f'- **Слова-индикаторы ограничений в заметках (не доказательство применимости):** {r.caution_terms}.')
 if r.example:line.append(f'- **Пример:** `{r.example}`'+(f' — {r.source}' if r.source else '')+'.')
 for j,u in enumerate(re.findall(r'https?://eldamo\.org/content/words/word-\d+\.html',r.rule_urls),1):line.append(f'- [Страница правила {j}]({u})')
 line.append('')
line += ['## Следующая итерация','', '1. Для категории U отделить действительно чужие (Sindarin/Telerin) правила от общих праэльфийских законов, допустимых в линии Quenya.','2. Для категории D подобрать и применить контекстные условия к целым последовательностям сегментов, а не к одиночным IPA-символам.','3. Для B/C извлечь явные указания на относительный порядок (`before`, `after`) из развернутых заметок и вручную интерпретировать утверждение, а не просто частотность слов.','4. Повторно построить граф с атрибутами *историческая ступень, диалект, редакция, контекст* и не смешивать редакционные системы.', '', '## Использованные локальные материалы', '', '- Архив `eldamo-0.8.13.zip`.','- `eldamo_sound_candidate_paths.csv` — исходные 101 кандидата.','- `eldamo_strict_chain_audit.csv` — предыдущие критерии связи словоформ.','- `eldamo_textual_chain_assessment.csv` — разбор 19 приоритетных цепочек.','- `eldamo_rule_commentary_audit.csv` — извлечённые пояснения и страницы правил.','']
open(P+'eldamo_critical_101_atlas.md','w').write('\n'.join(line))
print(ct, 'files',os.path.getsize(P+'eldamo_critical_101_atlas.md'))
