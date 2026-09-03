#!/usr/bin/env bash
# Reproduce main-text tables and Figure 3 (CPU; ~5–15 min depending on hardware).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "[1/9] assemble primary nested table (from archived JSON if present)"
python3 scripts/assemble_primary_nested_table.py
echo "[2/8] build systematic 8-task audit table"
python3 scripts/build_systematic_audit_table.py
echo "[3/8] C1 reference protocol-conformance benchmark"
python3 scripts/build_protocol_conformance_splits.py
python3 scripts/run_protocol_conformance_audit.py
echo "[4/10] C2 Hu + GenomicBenchmarks retrieval + audit"
python3 scripts/retrieve_c2_hu_artifacts.py
python3 scripts/build_c2_hu_phylo_manifest.py
python3 scripts/retrieve_c2_genomicbenchmarks.py
python3 scripts/run_c2_realworld_audit.py
python3 scripts/build_c2_case_level_table.py
python3 scripts/sync_c2_registry_artifacts.py
echo "[5/10] literature structured field audit (n=80)"
python3 scripts/build_literature_structured_field_audit.py
echo "[6/10] Figures (GeneLab E2E + legacy multi-task matrix)"
python3 scripts/make_figure3_genelab_e2e.py
python3 scripts/make_figure3_multi_task_matrix.py
echo "[7/9] verify hashes (optional)"
python3 scripts/write_reproducibility_hashes.py 2>/dev/null || true
echo "DONE: Table_reference_protocol_conformance_benchmark.csv, Table_realworld_supplied_split_audit.csv, Table_literature_structured_field_audit.csv, Figure3"
