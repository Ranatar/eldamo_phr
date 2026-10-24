"""Derive both primary path corpora from same shared modules and same Eldamo archive."""
from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from shared.extract import write
from shared.reconcile import reconcile
from shared.audit import audit_unified
from shared.graph import create
from shared.chains import evaluate
archive=ROOT/'source/eldamo-0.8.13.zip'
assert archive.is_file(), f'No source Eldamo archive: {archive}'
for branch in ('quenya','sindarin'):
 extracted=write(branch,archive)
 assert not extracted['errors'],(branch,extracted['errors'])
 legacy=reconcile(branch) # preserved only; canonical graph uses unified_rules.json directly
 audited=audit_unified(branch,archive)
 assert len(audited)==extracted['deduplicated'] or len(audited)==legacy['total_records']
 print('extraction',branch,extracted['deduplicated'],'legacy-only',legacy['restored_legacy_variants'],flush=True)
 g=create(branch)
 assert not g['search_truncations'],f"Truncated enumeration for {branch}: {g['search_truncations']}"
 a=evaluate(branch,archive)
 assert g['structural_chains']==a['number'],branch
 print(branch,g,a,flush=True)
import runpy
runpy.run_path(str(ROOT/'scripts/refresh_canonical.py'),run_name='__main__')
runpy.run_path(str(ROOT/'scripts/audit_chain_provenance.py'),run_name='__main__')
runpy.run_path(str(ROOT/'scripts/rebuild.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tests/test_canonical_pipeline.py'),run_name='__main__')

# V7: fail build if source encoding, guarded inventory, or projection provenance is incomplete.
runpy.run_path(str(ROOT/'scripts/audit_exclusions_v7.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tests/test_full_rule_provenance_v7.py'),run_name='__main__')

# V8: always regenerate epistemic-limits and archival-gap ledgers after the canonical data.
runpy.run_path(str(ROOT/'scripts/audit_historical_limits_v8.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tests/test_historical_limits_v8.py'),run_name='__main__')
