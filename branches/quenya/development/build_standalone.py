from pathlib import Path
import re
root=Path(__file__).resolve().parent
p=(root/'app') if (root/'app').exists() else (root.parent/'app')
html=(p/'index.html').read_text()
css=(p/'styles.css').read_text()
data=(p/'data.js').read_text()
app=(p/'app.js').read_text()
chains=(p/'chains.js').read_text()
html=re.sub(r'<link\s+href="styles.css"\s+rel="stylesheet"\s*/?>',lambda m:'<style>\n'+css+'</style>',html)
html=re.sub(r'<script\s+defer=""\s+src="data.js"\s*>\s*</script>|<script\s+src="data.js"\s+defer=""\s*>\s*</script>',lambda m:'<script>\n'+data+'</script>',html)
html=re.sub(r'<script\s+defer=""\s+src="chains.js"\s*></script>',lambda m:'<script>\n'+chains+'</script>',html)
html=re.sub(r'<script\s+defer=""\s+src="app.js"\s*>\s*</script>|<script\s+src="app.js"\s+defer=""\s*>\s*</script>',lambda m:'<script>\n'+app+'</script>',html)
assert 'src="app.js"' not in html and 'src="data.js"' not in html and 'src="chains.js"' not in html
(p/'built.html').write_text(html)
print('Generated',p/'built.html')
