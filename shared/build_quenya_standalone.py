from pathlib import Path
import re
BASE=Path(__file__).resolve().parents[1]/'branches/quenya/app'
html=(BASE/'index.html').read_text()
html=re.sub(r'<link\s+href="styles.css"\s+rel="stylesheet"\s*/?>',lambda m:'<style>\n'+(BASE/'styles.css').read_text()+'\n</style>',html)
for n in ['data.js','chains.js','app.js']:
 html=re.sub(r'<script\b[^>]*\bsrc="'+n+r'"[^>]*>\s*</script>',lambda m:'<script>\n'+(BASE/n).read_text()+'\n</script>',html)
 assert f'src="{n}"' not in html
(BASE/'built.html').write_text(html)
(BASE/'standalone.html').write_text(html)
print('Quenya standalone built from exactly the current modular sources')
