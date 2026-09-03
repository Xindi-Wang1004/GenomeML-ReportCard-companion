#!/usr/bin/env python3
"""Build systematic 8-task Report Card audit table (GB §2.4 + Supplementary).

Reads nested-primary repeated-CV where available (T01/T07/T08/T03_REP),
single-seed probes for Hu country, and locked matrix rows for T02/T04_ALT/T06 cluster.

Writes:
  tables/Table_systematic_audit_8tasks.csv
  multi_task_audit/results/systematic_audit/summary.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "audit_toolkit"))

OUT_DIR = ROOT / "multi_task_audit" / "results" / "systematic_audit"
TABLE = ROOT / "tables" / "Table_systematic_audit_8tasks.csv"
NESTED = ROOT / "tables" / "Table_primary_nested_cv.csv"
MATRIX = ROOT / "tables" / "Table_multi_task_matrix_summary.csv"
ROBUST = ROOT / "tables" / "Table_robustness_split_design.csv"


def _nested_row(tid: str, panel: str, label_unit: str, block: str, category: str) -> dict:
    df = pd.read_csv(NESTED).set_index("task_id")
    r = df.loc[tid]
    macro = tid in {"T01", "T07"}
    if macro and pd.notna(r.get("random_macro_mean")):
        rnd, blk, delta = r["random_macro_mean"], r["blocked_macro_mean"], r["delta_macro_mean"]
        metric = "species-macro Spearman ρ"
    else:
        rnd, blk, delta = r["random_mean"], r["blocked_mean"], r["delta_mean"]
        metric = "AUROC" if r["primary"] == "auc" else "Spearman ρ"
    return {
        "task_id": tid,
        "panel": panel,
        "category": category,
        "n_genomes": int(r["n_genomes"]),
        "n_groups": int(r["n_groups"]),
        "label_assignment_unit": label_unit,
        "declared_deployment_block": block,
        "metric": metric,
        "random_cv": round(float(rnd), 3),
        "blocked_cv": round(float(blk), 3),
        "delta_B": round(float(delta), 3),
        "sai_lo": round(float(r["delta_macro_ci95_lo" if macro else "delta_ci95_lo"]), 3),
        "sai_hi": round(float(r["delta_macro_ci95_hi" if macro else "delta_ci95_hi"]), 3),
        "probe_protocol": "nested Ridge-α (group-aware outer-fold retuning); repeated CV",
        "verdict_pattern": _verdict(float(delta), float(blk), float(rnd)),
    }


def _matrix_row(tid: str, panel: str, label_unit: str, block: str, category: str, metric_filter: str) -> dict:
    m = pd.read_csv(MATRIX)
    sub = m[(m.task_id == tid) & (m.metric == metric_filter)]
    if sub.empty:
        raise KeyError(f"matrix row missing: {tid} {metric_filter}")
    r = sub.iloc[0]
    metric = "Spearman ρ" if "rho" in metric_filter else "AUROC"
    rnd, blk, delta = float(r.random_score), float(r.blocked_score), float(r.delta)
    return {
        "task_id": tid,
        "panel": panel,
        "category": category,
        "n_genomes": int(r.n_genomes),
        "n_groups": int(r.n_groups),
        "label_assignment_unit": label_unit,
        "declared_deployment_block": block,
        "metric": metric,
        "random_cv": round(rnd, 3),
        "blocked_cv": round(blk, 3),
        "delta_B": round(delta, 3),
        "sai_lo": "",
        "sai_hi": "",
        "probe_protocol": "single-seed k-mer Ridge OOF (locked α); matrix companion",
        "verdict_pattern": str(r.verdict_pattern),
    }


def _hu_country_row() -> dict:
    p = ROOT / "multi_task_audit/results/published_audits/Hu_pa_ceftaz_country_reportcard.json"
    rep = json.loads(p.read_text())
    probe = rep["probe"]
    prim = probe["primary_metric"]
    rnd = float(probe["random"][prim])
    blk = float(probe["blocked"][prim])
    geo = rep["geometry"]
    return {
        "task_id": "T06_country",
        "panel": "Hu 2024 P. aeruginosa ceftazidime (country subset)",
        "category": "published_panel_null",
        "n_genomes": int(rep["n_rows"]),
        "n_groups": int(rep["n_groups"]),
        "label_assignment_unit": "isolate/strain",
        "declared_deployment_block": "country (18 levels)",
        "metric": "AUROC",
        "random_cv": round(rnd, 3),
        "blocked_cv": round(blk, 3),
        "delta_B": round(float(probe["delta"]), 3),
        "sai_lo": "",
        "sai_hi": "",
        "shared_block_fraction_random": round(float(geo["random_cv_shared_block_fraction"]), 3),
        "within_block_homogeneity": round(float(geo["within_block_homogeneity"]), 3),
        "contract_status": rep.get("contract_status", ""),
        "probe_protocol": "single-seed k-mer Ridge OOF; country-annotated 187-isolate subset",
        "verdict_pattern": "near_zero_gap",
    }


def _verdict(delta: float, blocked: float, random: float) -> str:
    if abs(delta) < 0.05:
        return "near_zero_gap"
    if delta >= 0.30 and blocked < 0.15:
        return "large_gap_blocked_low"
    if delta >= 0.30:
        return "large_gap_blocked_moderate"
    if random < 0.30 and blocked < 0.25:
        return "weak_signal_small_gap"
    if blocked >= random - 0.05 and blocked > 0.3:
        return "blocked_retains_ranking"
    return "moderate_gap"


def main() -> None:
    if not NESTED.is_file():
        raise SystemExit(f"missing primary nested table: {NESTED} (run scripts/run_primary_nested_suite.py)")

    rows = [
        _nested_row("T01", "OGT Domain C (777 genomes)", "species", "species", "positive_control"),
        _nested_row("T07", "OGT Domain B (560 genomes)", "species", "species", "positive_control"),
        _nested_row("T08", "Babayan 2018 reservoir host", "species (often singleton)", "Viral group (12)", "published_panel"),
        _nested_row("T03_REP", "Mollentze 2021 InfectsHuman (n≥2 species)", "species", "species", "published_panel"),
        _hu_country_row(),
        _matrix_row(
            "T06",
            "Hu 2024 ceftazidime (composition cluster)",
            "isolate/strain",
            "KMeans k=40 (full-cohort)",
            "operational_block",
            "auroc",
        ),
        _matrix_row(
            "T04_ALT",
            "Hu 2024 ceftazidime (strain singleton control)",
            "isolate/strain",
            "PATRIC strain (302 singleton)",
            "construction_control",
            "spearman_rho",
        ),
        _matrix_row(
            "T02",
            "SpillOver public scores → seq-level ML (integrity audit)",
            "curated organism entity",
            "Organism_Name (25 groups)",
            "integrity_audit",
            "spearman_rho",
        ),
    ]

    df = pd.DataFrame(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLE, index=False)
    payload = {
        "n_tasks": len(rows),
        "categories": df["category"].value_counts().to_dict(),
        "verdict_patterns": df["verdict_pattern"].value_counts().to_dict(),
        "rows": rows,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(payload, indent=2))
    print(df[["task_id", "category", "delta_B", "verdict_pattern"]].to_string(index=False))
    print("wrote", TABLE)


if __name__ == "__main__":
    main()
