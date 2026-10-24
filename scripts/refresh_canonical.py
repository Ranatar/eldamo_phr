"""Canonical app research corpus from one shared output, on both branches."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for branch in ('quenya','sindarin'):
 d=ROOT/'branches'/branch/'data'
 source=json.loads((d/'unified_assessed_chains.json').read_text(encoding='utf-8'))
 result=[]
 for chain in source:
  entry=dict(chain)
  entry['provenance_corpus']='canonical_shared_pipeline'
  entry['evidence_scope']='verified_formula_examples_only_not_historical_proof'
  result.append(entry)
 (d/'research_chains_for_app.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(branch,len(result))
