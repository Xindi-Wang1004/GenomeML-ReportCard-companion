#!/usr/bin/env python3
"""Write SHA-256 lock table for GB submission."""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_GIT = ROOT.parents[2] / "Spillover_public_git"
FILES = [
    "docs/PREREGISTRY_MULTI_TASK_BENCHMARK.md",
    "docs/PREREGISTRY_MULTI_TASK_BENCHMARK_GBv2.md",
    "docs/LOCKED_ANALYSIS_PROTOCOL_GBv2.md",
    "docs/REPRODUCIBILITY_LOCK.md",
    "tables/Table_multi_task_matrix_summary.csv",
    "tables/Table_simulation_label_geometry.csv",
    "tables/Table_robustness_split_design.csv",
    "tables/Table_published_benchmark_reanalysis.csv",
    "tables/Table_multimodel_split_contrast.csv",
    "tables/Table_external_holdout_validation.csv",
    "tables/Table_published_panel_reportcard_audit.csv",
    "tables/Table_dual_declaration_demo.csv",
    "tables/Table_contract_status_rules.md",
    "tables/Table_guideline_reportcard_mapping.csv",
    "tables/Table_literature_scan_methods.csv",
    "tables/Table_T06_block_sensitivity.csv",
    "tables/Table_T06_cluster_construction.csv",
    "multi_task_audit/results/published_audits/Hu_pa_ceftaz_country_reportcard.json",
    "multi_task_audit/results/published_audits/Hu_pa_ceftaz_strain_as_block.json",
    "multi_task_audit/manifests/T03_mollentze.tsv",
    "multi_task_audit/manifests/T03_REP_mollentze_n2.tsv",
    "multi_task_audit/T04/manifests/T04_ALT_pa_ceftaz.tsv",
    "multi_task_audit/T04/manifests/T06_pa_ceftaz_cluster.tsv",
    "multi_task_audit/T05/manifests/T05_babayan.tsv",
    "multi_task_audit/T05/manifests/T08_babayan_viral_group.tsv",
    "second_domain_bacteria/data/manifest.tsv",
    "third_domain_ogt_large/data/manifest.tsv",
    "GB_estimand_v1.md",
]


def _git(cwd: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def main():
    rows = []
    for rel in FILES:
        p = ROOT / rel
        if not p.is_file():
            rows.append({"path": rel, "status": "MISSING"})
            continue
        data = p.read_bytes()
        rows.append(
            {
                "path": rel,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "mtime_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(p.stat().st_mtime)),
            }
        )
    head = _git(PUBLIC_GIT, "rev-parse", "HEAD") if PUBLIC_GIT.is_dir() else ""
    tag_commit = _git(PUBLIC_GIT, "rev-parse", "reportcard-v0.1.1^{commit}") if PUBLIC_GIT.is_dir() else ""
    out = {
        "generated_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "spillover_public_git_head": head,
        "reportcard_v0_1_1_commit": tag_commit,
        "reportcard_v0_1_1_tag": "reportcard-v0.1.1",
        "pypi": "https://pypi.org/project/genome-ml-reportcard/0.1.1/",
        "zenodo_software_doi": "10.5281/zenodo.22226465",
        "files": rows,
        "regen": "python3 scripts/write_reproducibility_hashes.py",
    }
    path = ROOT / "tables" / "Table_reproducibility_hashes.json"
    path.write_text(json.dumps(out, indent=2))
    print("wrote", path, "n=", len(rows), "head=", head[:12], "tag=", tag_commit[:12])


if __name__ == "__main__":
    main()
