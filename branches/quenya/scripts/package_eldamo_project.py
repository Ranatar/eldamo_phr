"""Package the complete Eldamo research workspace with clear active and historical folders."""
from pathlib import Path
import zipfile,hashlib,csv,io,datetime
root=Path(__file__).resolve().parent
out=root/'eldamo_research_complete_package.zip'
active={
'app':['eldamo_sound_path_explorer_complete.html','build_eldamo_rules_ui.py','test_eldamo_html.py'],
'catalog':['eldamo_six_languages_ipa_catalog.md','eldamo_full_catalog.py'],
'engine':['eldamo_interpreter_v3.py','eldamo_context_interpreter.py','eldamo_interpreter_v2.py'],
'evidence':['eldamo_exact_word_joins.csv','eldamo_strict_chain_evidence.csv','eldamo_rule_commentary_audit.csv','eldamo_textual_chain_assessment.csv','eldamo_order_and_context_clues.csv','eldamo_sound_edges.csv','eldamo_sound_graph.graphml','eldamo_sound_candidate_paths.csv','eldamo_word_chain_validation.csv'],
'reports':['eldamo_critical_101_atlas.md','eldamo_etymological_chain_verification.md','eldamo_paths_context_report.md','eldamo_strict_chain_report.md','eldamo_textual_chain_report.md','eldamo_context_interpreter_report.md','eldamo_extended_analysis_report.md','eldamo_v2_report.md','eldamo_v3_comprehensive_audit.md','eldamo_explorer_and_chronology_report.md','eldamo_sound_paths_report.md','eldamo_workspace_audit.md'],
'data':['eldamo_critical_101_atlas.csv','eldamo_strict_chain_audit.csv','eldamo_paths_context_audit.csv','eldamo_context_chain_audit.csv','eldamo_context_example_tests.csv','eldamo_extended_rule_inventory.csv','eldamo_recovered_exclusions.csv','eldamo_extended_101_reassessment.csv','eldamo_new_atomic_candidates.csv','eldamo_v2_all_rules.csv','eldamo_v2_recovered_exclusions.csv','eldamo_v2_101_recheck.csv','eldamo_v2_27_recheck.csv','eldamo_v2_structural_candidates.csv','eldamo_v3_rule_example_validation.csv','eldamo_v3_101_reassessment.csv','eldamo_v3_101_rule_level_audit.csv','eldamo_v3_27_reassessment.csv','eldamo_v3_27_normalized_reassessment.csv','eldamo_v3_rebuilt_structural_graph.csv','eldamo_101_stage_reassessment.csv','eldamo_workspace_inventory.csv','eldamo_new_atomic_candidates.csv'],
'scripts':['build_eldamo_paths.py','build_eldamo_critical_atlas.py','eldamo_extended_audit.py','eldamo_new_path_candidates.py','run_eldamo_context_audit.py','run_eldamo_v2_complete.py','verify_eldamo_word_paths.py','verify_eldamo_strict.py','eldamo_textual_review.py','package_eldamo_project.py']
}
legacy=['eldamo_quenya_phonetics.md','eldamo_quenya_phonetics_revised.md','eldamo_quenya_ancient_quenya_full.md','eldamo_quenya_ancient_quenya_by_phoneme.md','eldamo_quenya_ancient_quenya_deduplicated.md','eldamo_quenya_ancient_quenya_tables.md','eldamo_quenya_ancient_quenya_complete_tables_v2.md','eldamo_quenya_ancient_quenya_ipa_navigation.md','eldamo_sound_path_explorer.html','eldamo_sound_path_explorer_ipa.html']
# Include original code sources present only in earlier archives, with explicit provenance.
old=[]
for source in ['eldamo_integrated_research_package_ipa.zip','eldamo_v3_research_bundle.zip','eldamo_integrated_research_package.zip']:
 with zipfile.ZipFile(root/source) as z:
  for n in z.namelist():
   if n.endswith('.py') and not (root/n).exists() and n not in [x[0] for x in old]:old.append((n,z.read(n),source))
readme='''# Eldamo phonetic research package

Version: Eldamo 0.8.13. Built from prior research results, not an officially endorsed Eldamo release.

## Start
Open `app/eldamo_sound_path_explorer_complete.html` in a modern browser (no server needed).
Select a phoneme in either IPA table, or a cluster beginning with the chosen segment. Click **Find paths**, **Rules for source** or **Rules for target** independently.

## Directory structure
- `app/`: working offline HTML and the source script that adds the rules UI.
- `catalog/`: complete six-language Markdown catalog, plus original extraction script (historical generation pipeline).
- `engine/`: interpreter iterations. v3 is the latest of those versions; its semantic scope is not exhaustive.
- `evidence/`: word forms, rule descriptions, edge lists, GraphML.
- `data/`: per-stage machine-readable audit outputs.
- `reports/`: current and previous research assessments.
- `scripts/`: locally available reconstruction and analysis scripts.
- `scripts/recovered/`: source scripts extracted from older ZIP packages. These are preserved for provenance, not guaranteed to be standalone.
- `legacy/`: older catalog layouts and prior HTML versions, reference only.

## Important limits
The interactive path finder uses atomic sound transitions, not a comprehensive environment-sensitive sound-change interpreter. A path is a candidate, not a historically proven derivation. 'Rules' views display the original catalog's rows: phoneme view lists its own entries; cluster view matches exact cluster formula sides only.

## Source dependency and reproducibility
The original `eldamo-0.8.13.zip` archive (~78 MB) is intentionally not embedded. Put it beside the scripts before attempting to rerun upstream extraction. To regenerate the HTML UI, run `python build_eldamo_rules_ui.py` with the prior IPA HTML in the same folder. To run a browser smoke test on Linux, run `python test_eldamo_html.py` (requires Playwright and Chromium). To rebuild the research ZIP, run `python package_eldamo_project.py` after laying out the archived files in a flat working directory. Some historic extraction scripts assume paths or intermediates generated in previous runs; inspect the scripts before executing. The included static HTML and data tables work without Eldamo source archive.

Data from Eldamo: https://eldamo.org/ ; consult Eldamo's own licensing and attribution terms before redistribution.
'''
selected=[];seen=set()
for folder,names in active.items():
 for name in names:
  if name in seen:continue
  assert (root/name).exists(),name
  selected.append((folder+'/'+name,(root/name).read_bytes()));seen.add(name)
for name in legacy:
 if (root/name).exists():selected.append(('legacy/'+name,(root/name).read_bytes()))
for name,content,source in old:selected.append(('scripts/recovered/'+name,content))
selected.append(('README.md',readme.encode()))
manifest=io.StringIO();w=csv.writer(manifest);w.writerow(['path','bytes','sha256'])
for n,data in selected:w.writerow([n,len(data),hashlib.sha256(data).hexdigest()])
selected.append(('MANIFEST.csv',manifest.getvalue().encode()))
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for n,content in selected:z.writestr(n,content)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist()))
 print('packed',out,len(z.namelist()),out.stat().st_size,'recovered scripts',len(old))
 print('folders',sorted(set(n.split('/')[0] for n in z.namelist())))
