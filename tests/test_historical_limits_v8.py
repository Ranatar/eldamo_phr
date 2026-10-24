import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from scripts.audit_historical_limits_v8 import run
s=run()
for branch in ('quenya','sindarin'):
 d=R/'branches'/branch/'data';chains=json.loads((d/'unified_assessed_chains.json').read_text());ledger=json.loads((d/'historical_limit_ledger_v8.json').read_text())
 assert len(chains)==len(ledger)==s[branch]['canonical']['total']
 assert {c['id'] for c in chains}=={c['id'] for c in ledger}
 assert all(x['relative_chronology_unverified'] and x['authorial_revision_compatibility_unverified'] for x in ledger)
 assert all(len(x['stage_sequence'])==len(x['states'])-1 for x in ledger)
 assert len(json.loads((d/'archival_gap_register_v8.json').read_text()))==2
print('v8 historical limits: PASS')
