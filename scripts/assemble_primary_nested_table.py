#!/usr/bin/env python3
"""Assemble Table_primary_nested_cv.csv from nested JSON artifacts (no recompute)."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_robustness_suite import TASKS, _load, _row  # noqa: E402

JSON_DIR = ROOT / "multi_task_audit" / "results" / "robustness"
OUT = ROOT / "tables" / "Table_primary_nested_cv.csv"
LOCKED = ROOT / "tables" / "Table_robustness_split_design.csv"
BACKUP = ROOT / "tables" / "Table_locked_alpha_sensitivity.csv"
TASKS_ORDER = ["T01", "T07", "T08", "T03_REP"]


def _load_contrast(tid: str) -> dict:
    for name in (f"{tid}_primary_nested.json", f"{tid}_nested_tuning.json"):
        p = JSON_DIR / name
        if p.is_file():
            return json.loads(p.read_text())
    raise FileNotFoundError(tid)


def main() -> None:
    if LOCKED.is_file() and not BACKUP.is_file():
        shutil.copy2(LOCKED, BACKUP)
        print("archived", BACKUP)

    rows = []
    for tid in TASKS_ORDER:
        d = _load_contrast(tid)
        cfg = TASKS[tid]
        X, y, g = _load(cfg)
        contrast = {
            "primary": d["primary"],
            "locked_alpha": d.get("locked_alpha"),
            "random_genome": d["random_genome"],
            "blocked_genome": d["blocked_genome"],
            "delta_genome": d["delta_genome"],
            "random_group_macro": d["random_group_macro"],
            "blocked_group_macro": d["blocked_group_macro"],
            "delta_group_macro": d["delta_group_macro"],
            "tuning": d["tuning"],
        }
        logo = {
            "pooled_genome": {d["primary"]: float("nan")},
            "pooled_group_macro": {d["primary"]: float("nan")},
            "drop_one_group_influence": [],
        }
        row = _row(tid, X, y, g, contrast, logo)
        row["note"] = (
            "primary: nested Ridge α retuned on each outer training fold (group-aware); "
            f"n_repeats={d['n_repeats']}"
        )
        rows.append(row)

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(out[["task_id", "delta_macro_mean", "delta_mean", "delta_ci95_lo", "delta_ci95_hi"]])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
