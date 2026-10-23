#!/usr/bin/env python3
"""Extract Eldamo phonetic developments for every sound from Q and AQ.
Requires: requests, beautifulsoup4. Network connectivity to eldamo.org required.
Run: python eldamo_full_catalog.py
"""
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = 'https://eldamo.org'
INDEXES = [('Quenya', BASE + '/content/phonetic-indexes/phonetics-q.html'),
           ('Ancient Quenya', BASE + '/content/phonetic-indexes/phonetics-aq.html')]
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Eldamo-research-catalog/1.0 (noncommercial research)'})

def get(url):
    for attempt in range(3):
        try:
            r = SESSION.get(url, timeout=25)
            r.raise_for_status()
            return BeautifulSoup(r.content, 'html.parser')
        except Exception:
            if attempt == 2: raise
            time.sleep(1.5 * (attempt + 1))

def clean(node):
    return ' '.join(node.stripped_strings).strip()

def phonemes(index_soup, url):
    headings = index_soup.find_all(re.compile('^h[1-6]$'))
    h = next((h for h in headings if clean(h).lower() == 'phonemes'), None)
    if h is None: raise RuntimeError(f'No Phonemes heading: {url}')
    found = []
    for el in h.next_elements:
        if isinstance(el, Tag) and el.name in ('h1','h2','h3','h4','h5','h6') and clean(el) == 'Phonetic Groups':
            break
        if isinstance(el, Tag) and el.name == 'a' and el.get('href'):
            text = clean(el)
            if re.match(r'^\[[^\]]+\]$', text):
                target = urljoin(url, el['href'])
                if (text, target) not in found: found.append((text, target))
    if len(found) < 20: raise RuntimeError(f'Only {len(found)} phonemes found at {url}; inspect markup')
    return found

def parse_sound(soup, sound, url):
    # Eldamo entries can include Late, Middle and Early subentries on the same page.
    # Read every "Phonetic Development" table, retaining the period label of its subentry.
    rows = []
    candidates = [e for e in soup.find_all(string=True) if e.strip() == 'Phonetic Development']
    if not candidates:
        raise RuntimeError(f'No Phonetic Development section for {sound}: {url}')
    for label in candidates:
        parent = label.parent
        # Table is usually immediately after a section title; stop at the next subsection.
        table = parent.find_next('table')
        if table is None: raise RuntimeError(f'No phonetic table for {sound}: {url}')
        between = list(parent.next_elements)
        if table not in between: raise RuntimeError(f'Missing table at {url}')
        period = None
        subentry = parent.find_previous(string=re.compile(r'(?:ᴱ|ᴹ)?(?:AQ|Q)\.\s*\['))
        if subentry:
            m = re.search(r'((?:ᴱ|ᴹ)?(?:AQ|Q)\.)', str(subentry))
            if m: period = m.group(1)
        for tr in table.find_all('tr'):
            tds = tr.find_all(['td','th'], recursive=False)
            if len(tds) < 3: continue
            cells = [clean(td) for td in tds]
            if not any(cells): continue
            # Phonetic Development cells are usually [label, result, relation, source, refs].
            full = ' | '.join(cells)
            current = re.match(r'^(ᴱQ\.|ᴹQ\.|ᴱAQ\.|ᴹAQ\.|AQ\.|Q\.|ᴱ✶|ᴹ✶|✶)', cells[0])
            if current: period = current.group(1)
            # Early Qenya rows are excluded, also when their marker was carried over.
            if period == 'ᴱQ.' or cells[0].startswith('ᴱQ.'): continue
            if not any(c in ('<','>','←','→') for c in cells):
                continue
            refs = [urljoin(url, a['href']) for a in tr.find_all('a', href=True)]
            rows.append((period or '', cells, refs))
    # A raw multiple-sounds page may repeat identical data in several tables: preserve order,
    # but remove only exactly identical rows from the same page.
    dedup = []
    for r in rows:
        if r not in dedup: dedup.append(r)
    return dedup

def main():
    output = ['# Фонетические правила Quenya и Ancient Quenya (Eldamo)', '',
        'Источник: Eldamo, Paul Strack, https://eldamo.org/.',
        'Отбор: все строки **Phonetic Development** на страницах каждого звука из таблицы **Phonemes**; исключены строки с маркером `ᴱQ.` (Early Qenya).',
        'Строки без повторного маркера наследуют маркер предыдущей строки в пределах своего блока. Другие маркеры (Q., AQ., ᴹQ., ᴹAQ., ✶) сохранены.',
        'Приведены выражения в исходном порядке Eldamo, а не реконструированные преобразования.', '',
        'Обозначения: https://eldamo.org/general/terminology-and-notations.html', '',
        f'Дата выгрузки: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}', '']
    stats = []
    for language, index_url in INDEXES:
        index = get(index_url)
        sounds = phonemes(index, index_url)
        output += [f'## {language}', '', f'Индекс: {index_url}', '']
        linecount = 0
        for sound, page_url in sounds:
            soup = get(page_url)
            entries = parse_sound(soup, sound, page_url)
            linecount += len(entries)
            output += [f'### {sound}', '', f'Источник: {page_url}', '']
            if not entries:
                output += ['Нет подходящих записей после исключения `ᴱQ.`.', '']
            else:
                output += ['| Маркер | Правило / результат | Направление | Исходная форма | Источники |',
                           '|---|---|:---:|---|---|']
                for period, cells, refs in entries:
                    # Keep all field text, including forms and human-readable rule name.
                    # Escape Markdown table boundaries safely.
                    fields = cells[:4]
                    if len(fields) < 4: fields += [''] * (4-len(fields))
                    r = ', '.join(f'[источник]({link})' for link in refs) or '—'
                    vals = [period, fields[0], fields[2], f'{fields[1]} / {fields[3]}', r]
                    vals = [v.replace('|', '\\|').replace('\n',' ') for v in vals]
                    output += ['| ' + ' | '.join(vals) + ' |']
                output.append('')
            time.sleep(0.12)
        stats.append((language,len(sounds),linecount))
    output += ['## Проверка полноты', '', '| Язык | Обработано звуков | Отобрано строк |', '|---|---:|---:|']
    output += [f'| {name} | {n} | {rows} |' for name,n,rows in stats]
    output += ['', 'Примечание: одна фонетическая закономерность может быть приведена на страницах нескольких звуков; такие повторения сохранены.']
    outfile = 'eldamo_quenya_ancient_quenya_full.md'
    with open(outfile, 'w', encoding='utf-8') as f: f.write('\n'.join(output) + '\n')
    print('Created', outfile, 'stats:', stats)

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('ERROR: Catalog not generated; completeness cannot be guaranteed:', exc, file=sys.stderr)
        sys.exit(1)
