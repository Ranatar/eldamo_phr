from pathlib import Path
import re
p=Path(__file__).resolve().parent.parent/'app'
t=(p/'index.html').read_text()
t=t.replace('<link href="styles.css" rel="stylesheet"/>','<style>\n'+(p/'styles.css').read_text()+'\n</style>')
for file in ['data.js','chains.js','app.js']:
 t=re.sub(r'<script[^>]*src="'+file+r'"[^>]*>\s*</script>',lambda m:'<script>\n'+(p/file).read_text()+'\n</script>',t)
assert 'src="app.js"' not in t
(p/'standalone.html').write_text(t)
print('Build OK:',p/'standalone.html')
