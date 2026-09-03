#!/usr/bin/env python3
"""Regenerate C2-HU-MSMA-LOSO-OUTER fold membership from frozen evidence.

No network. No randomness for outer LOSO. Reads only:
  protocol_conformance_benchmark/c2_data/C2-HU-MSMA-LOSO-OUTER/evidence/
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = "C2-HU-MSMA-LOSO-OUTER"
DATA = ROOT / "protocol_conformance_benchmark" / "c2_data" / CASE
EV = DATA / "evidence"
PROC = DATA / "processed"
COMMIT = "2850078b912483b352f9a355a86a618c3553ca94"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_iso(gid: str) -> str:
    return gid[4:] if gid.lower().startswith("iso_") else gid


def main() -> None:
    PROC.mkdir(parents=True, exist_ok=True)
    loo_dir = EV / "loo_folds"
    unit2block: dict[str, str] = {}
    for p in sorted(loo_dir.glob("*_KMA_cv.json")):
        sp = p.name.replace("_KMA_cv.json", "")
        for fold in json.loads(p.read_text()):
            for gid in fold:
                if gid in unit2block and unit2block[gid] != sp:
                    raise SystemExit(f"species conflict for {gid}")
                unit2block[gid] = sp
    blocks = sorted(set(unit2block.values()))
    assert len(blocks) == 9

    rows = []
    fold_stats = []
    coverage_test: set[str] = set()
    for fold_id, held in enumerate(blocks):
        test_ids = sorted(u for u, b in unit2block.items() if b == held)
        train_ids = sorted(u for u, b in unit2block.items() if b != held)
        train_blocks = sorted({unit2block[u] for u in train_ids})
        test_blocks = sorted({unit2block[u] for u in test_ids})
        inter = set(train_blocks) & set(test_blocks)
        coverage_test.update(test_ids)
        for gid in train_ids:
            rows.append((gid, strip_iso(gid), held, fold_id, "train", unit2block[gid]))
        for gid in test_ids:
            rows.append((gid, strip_iso(gid), held, fold_id, "test", unit2block[gid]))
        fold_stats.append(
            {
                "fold_id": fold_id,
                "held_out_species": held,
                "n_train": len(train_ids),
                "n_test": len(test_ids),
                "accession_overlap": len(set(train_ids) & set(test_ids)),
                "block_recurrence": len(inter),
                "held_out_in_train": held in train_blocks,
            }
        )

    test_counts = Counter(r[0] for r in rows if r[4] == "test")
    multi = {k: v for k, v in test_counts.items() if v != 1}
    assert not multi
    assert coverage_test == set(unit2block)
    assert all(s["accession_overlap"] == 0 and s["block_recurrence"] == 0 for s in fold_stats)

    cols = [
        "genome_id_fold",
        "genome_id_patric",
        "held_out_species",
        "fold_id",
        "partition",
        "species_block",
        "source_generator",
        "source_commit",
        "generator_parameters",
    ]
    tsv = PROC / "fold_assignment_regenerated.tsv"
    with tsv.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for gid, pat, held, fid, part, sp in rows:
            f.write(
                "\t".join(
                    [
                        gid,
                        pat,
                        held,
                        str(fid),
                        part,
                        sp,
                        "AMR_benchmarking.main_MSMA_concat.MSMA_concatLOO",
                        COMMIT,
                        "outer=leave_one_species_out;level=loose;f_kma=True",
                    ]
                )
                + "\n"
            )

    with (PROC / "fold_counts.tsv").open("w") as f:
        f.write(
            "fold_id\theld_out_species\tn_train\tn_test\taccession_overlap\tblock_recurrence\theld_out_in_train\n"
        )
        for s in fold_stats:
            f.write(
                f"{s['fold_id']}\t{s['held_out_species']}\t{s['n_train']}\t{s['n_test']}\t"
                f"{s['accession_overlap']}\t{s['block_recurrence']}\t{s['held_out_in_train']}\n"
            )

    with (PROC / "unit_to_block.tsv").open("w") as f:
        f.write("genome_id_fold\tgenome_id_patric\tspecies_block\tspecies_source_file\n")
        for gid, sp in sorted(unit2block.items()):
            f.write(f"{gid}\t{strip_iso(gid)}\t{sp}\t{sp}_KMA_cv.json\n")

    env = {
        "regeneration_date": str(date.today()),
        "python": sys.version,
        "platform": platform.platform(),
        "script": "scripts/regenerate_hu_msma_loso_outer.py",
        "commit_pinned": COMMIT,
        "n_genomes": len(unit2block),
        "n_outer_folds": 9,
        "input_sha256": {
            str(p.relative_to(EV)): sha256(p)
            for p in sorted(EV.rglob("*"))
            if p.is_file() and p.name != "SHA256SUMS.txt"
        },
        "output_sha256": {},
    }
    for name in [
        "fold_assignment_regenerated.tsv",
        "fold_counts.tsv",
        "unit_to_block.tsv",
    ]:
        env["output_sha256"][name] = sha256(PROC / name)
    (PROC / "regeneration_environment.json").write_text(json.dumps(env, indent=2) + "\n")
    print(
        f"OK {CASE}: genomes={len(unit2block)} folds=9 "
        f"recurrence0=True coverage=True unique_test=True"
    )


if __name__ == "__main__":
    main()
