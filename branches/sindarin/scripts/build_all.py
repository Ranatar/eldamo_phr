"""Full offline Eldamo Sindarin rebuild (original eldamo-0.8.13.zip beside project)."""
from pathlib import Path
import subprocess,sys
P=Path(__file__).resolve().parent
for script in ['build_sindarin.py','build_ipa_navigation.py','assess_chains.py','finalize_evidence.py','build_standalone.py','test_project.py','test_browser_parity.py']:
 print('==>',script,flush=True)
 subprocess.run([sys.executable,str(P/script)],check=True)
print('COMPLETE')
