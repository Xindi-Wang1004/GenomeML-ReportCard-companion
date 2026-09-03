#!/usr/bin/env python3
"""Build main-text Table 3 source: case-level registry with dual conformance columns."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "protocol_conformance_benchmark" / "c2_case_registry.json"

# upstream_ecosystem groups 15 contract-audit cases into independent release sources
META = {
    "C2-GB-HUMAN_PROMOTERS": {
        "task": "human non-TATA promoters",
        "ecosystem": "GenomicBenchmarks",
        "upstream": "GenomicBenchmarks@605d8539",
        "membership": "train/test CSV.gz folders",
        "block_map": "sequence_id (declared holdout)",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not applicable",
        "block_justification": "not applicable",
        "limitation": "chromosome recurrence undeclared",
    },
    "C2-GB-HUMAN-PROMOTERS-E2E": {
        "task": "human non-TATA promoters (source-preserving E2E)",
        "ecosystem": "GenomicBenchmarks",
        "upstream": "GenomicBenchmarks@605d8539 + Report Card manifest assembly",
        "membership": "manifest_sequence_split.tsv",
        "block_map": "sequence_id",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not applicable",
        "block_justification": "not applicable",
        "limitation": "interoperability packaging; not donor/cohort transfer",
    },
    "C2-GB-CODING_VS_INTERGENIC": {
        "task": "coding vs intergenic demo",
        "ecosystem": "GenomicBenchmarks",
        "upstream": "GenomicBenchmarks@605d8539",
        "membership": "train/test folders",
        "block_map": "sequence/interval id",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not applicable",
        "block_justification": "not applicable",
        "limitation": "demo task scope",
    },
    "C2-GB-HUMAN_OCR": {
        "task": "human OCR Ensembl",
        "ecosystem": "GenomicBenchmarks",
        "upstream": "GenomicBenchmarks@605d8539",
        "membership": "train/test folders",
        "block_map": "sequence/interval id",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not applicable",
        "block_justification": "not applicable",
        "limitation": "none for declared estimand",
    },
    "C2-GB-HUMAN_ENHANCERS": {
        "task": "human enhancers Ensembl",
        "ecosystem": "GenomicBenchmarks",
        "upstream": "GenomicBenchmarks@605d8539",
        "membership": "train/test folders",
        "block_map": "example id",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not applicable",
        "block_justification": "not applicable",
        "limitation": "interval recurrence supplemental",
    },
    "C2-GB-MOUSE_ENHANCERS": {
        "task": "mouse enhancers (registry slug)",
        "ecosystem": "GenomicBenchmarks",
        "upstream": "GenomicBenchmarks pinned commit",
        "membership": "slug absent at pin",
        "block_map": "unavailable",
        "membership_integrity": "not assessable",
        "declared_block_conformance": "not assessable",
        "block_justification": "not applicable",
        "limitation": "dataset slug missing",
    },
    "C2-HU-PA-CEFTAZ-PHYLO": {
        "task": "P. aeruginosa ceftazidime phylo CV",
        "ecosystem": "Hu AMR benchmarking",
        "upstream": "AMR_benchmarking@2850078b; Mendeley 10.17632/6vc2msmsxj.1",
        "membership": "ceftazidime_phylotree_cv.json",
        "block_map": "fold ids only; clade table absent",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not assessable",
        "block_justification": "not assessed",
        "limitation": "membership interoperability only; phylogenetic block not encodable",
    },
    "C2-HU-PA-CEFTAZ-RANDOM": {
        "task": "P. aeruginosa ceftazidime random CV",
        "ecosystem": "Hu AMR benchmarking",
        "upstream": "same suite; random_cv.json",
        "membership": "random_cv.json",
        "block_map": "fold ids",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not applicable",
        "block_justification": "not applicable",
        "limitation": "non-biological partition claim",
    },
    "C2-PROTEINGYM-DMS": {
        "task": "ProteinGym DMS supervised CV",
        "ecosystem": "ProteinGym",
        "upstream": "ProteinGym 144fe22b; Zenodo 10.5281/zenodo.15293562",
        "membership": "cv_folds_singles_substitutions.zip",
        "block_map": "not declared / N/A",
        "membership_integrity": "conformant",
        "declared_block_conformance": "not applicable",
        "block_justification": "not applicable",
        "limitation": "released CV only; not protein-disjoint transfer",
    },
    "C2-GENELAB-MISSION-LOMO": {
        "task": "GeneLab gastrocnemius LOMO",
        "ecosystem": "GeneLab benchmark",
        "upstream": "HF jang1563/genelab-benchmark A2",
        "membership": "train/test_meta.csv + fold_info.json",
        "block_map": "mission",
        "membership_integrity": "conformant",
        "declared_block_conformance": "conformant",
        "block_justification": "not assessed",
        "limitation": "mouse mission ≠ human donor",
    },
    "C2-HU-MSMA-LOSO-OUTER": {
        "task": "MSMA-concat outer leave-one-species-out",
        "ecosystem": "Hu AMR benchmarking",
        "upstream": "AMR_benchmarking@2850078b912483b352f9a355a86a618c3553ca94",
        "membership": "fold_assignment_regenerated.tsv (generator-derived)",
        "block_map": "species (from multi_S_LOO_folds files)",
        "membership_integrity": "conformant",
        "declared_block_conformance": "conformant",
        "block_justification": "not assessed",
        "limitation": "generator-derived E2E; not upstream fold-CSV release; ≠ Hu phylotree",
    },
    "C2-MOLLENTZE-ZOONOTIC_RANK": {
        "task": "zoonotic_rank InfectsHuman",
        "ecosystem": "Mollentze zoonotic_rank",
        "upstream": "Nardus/zoonotic_rank; Zenodo 10.5281/zenodo.5155330",
        "membership": "generator+seed; no export",
        "block_map": "unavailable",
        "membership_integrity": "not assessable",
        "declared_block_conformance": "not assessable",
        "block_justification": "not applicable",
        "limitation": "membership not independently verifiable",
    },
    "C2-BABAYAN-VIRAL_HOST": {
        "task": "viral host prediction",
        "ecosystem": "Babayan 2018 panel",
        "upstream": "Babayan 2018 public genomes/labels",
        "membership": "official folds absent",
        "block_map": "unavailable",
        "membership_integrity": "not assessable",
        "declared_block_conformance": "not assessable",
        "block_justification": "not applicable",
        "limitation": "reconstructed Δ_B ≠ C2 membership",
    },
    "C2-ENGQVIST-OGT": {
        "task": "bacterial OGT labels",
        "ecosystem": "Engqvist OGT",
        "upstream": "Engqvist 2018 Zenodo labels",
        "membership": "no official ML fold release",
        "block_map": "unavailable",
        "membership_integrity": "not assessable",
        "declared_block_conformance": "not assessable",
        "block_justification": "not applicable",
        "limitation": "labels ≠ ML fold artifact",
    },
    "C2-CAMI2-METAGENOMICS": {
        "task": "CAMI II sample-disjoint",
        "ecosystem": "CAMI II",
        "upstream": "doi:10.1038/s41592-023-01962-8",
        "membership": "pending retrieval",
        "block_map": "pending",
        "membership_integrity": "not assessable",
        "declared_block_conformance": "not assessable",
        "block_justification": "not applicable",
        "limitation": "pending",
    },
    "C2-SCRNA-DONOR-CV": {
        "task": "human blood atlas donor CV",
        "ecosystem": "scRNA cross-donor",
        "upstream": "scRNA-cross-donor-generalization@ccfd3b7e",
        "membership": "metrics/predictions only",
        "block_map": "donor_id in config; not exported",
        "membership_integrity": "not assessable",
        "declared_block_conformance": "not assessable",
        "block_justification": "not applicable",
        "limitation": "claim recorded; conformance withheld",
    },
}

BJ_MAP = {
    "not applicable": "not_applicable",
    "not assessed": "not_independently_verified",
}


def main() -> None:
    data = json.loads(REG.read_text())
    superseded = set(data.get("superseded_case_ids", []))
    rows = []
    ecosystems = set()
    for c in data["cases"]:
        cid = c["case_id"]
        if cid in superseded:
            continue
        if cid not in META:
            raise KeyError(f"META missing for {cid}")
        m = META[cid]
        ecosystems.add(m["ecosystem"])
        row = {
            "case_id": cid,
            "upstream_ecosystem": m["ecosystem"],
            "domain_task": m["task"],
            "upstream_source_version": m["upstream"],
            "membership_artifact": m["membership"],
            "membership_provenance": c.get(
                "membership_source",
                c.get("membership_provenance", "unspecified"),
            ),
            "block_mapping_available": m["block_map"],
            "claim_specification": c["claim_specification_status"],
            "artifact_sufficiency": c["artifact_sufficiency_status"],
            "membership_integrity": m["membership_integrity"],
            "declared_block_conformance": m["declared_block_conformance"],
            "block_justification": m["block_justification"],
            "key_limitation": m["limitation"],
        }
        rows.append(row)
        c["upstream_ecosystem"] = m["ecosystem"]
        c["membership_integrity_status"] = m["membership_integrity"]
        c["declared_block_conformance_status"] = m["declared_block_conformance"]
        c["block_justification_display"] = m["block_justification"]
        if m["block_justification"] in BJ_MAP:
            c["biological_block_validation_status"] = BJ_MAP[m["block_justification"]]

    data["n_upstream_ecosystems"] = len(ecosystems)
    data["upstream_ecosystems"] = sorted(ecosystems)
    REG.write_text(json.dumps(data, indent=2) + "\n")

    cols = list(rows[0].keys())
    csv_path = ROOT / "tables" / "Table_c2_case_level_registry.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    md = [
        "| Case ID | Domain / task | Upstream (version) | Membership artifact | Membership provenance | Block mapping | Claim | Artifact | Membership integrity | Declared-block conformance | Block justification | Key limitation |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        md.append(
            "| {cid} | {task} | {up} | {mem} | {prov} | {bm} | {cs} | {as_} | {mi} | {dbc} | {bj} | {lim} |".format(
                cid=r["case_id"].replace("C2-", ""),
                task=r["domain_task"],
                up=r["upstream_source_version"],
                mem=r["membership_artifact"],
                prov=r["membership_provenance"],
                bm=r["block_mapping_available"],
                cs=r["claim_specification"],
                as_=r["artifact_sufficiency"],
                mi=r["membership_integrity"],
                dbc=r["declared_block_conformance"],
                bj=r["block_justification"],
                lim=r["key_limitation"],
            )
        )
    (ROOT / "tables" / "Table_c2_case_level_registry.md").write_text("\n".join(md) + "\n")
    print(f"wrote {csv_path} ({len(rows)} cases, {len(ecosystems)} ecosystems)")


if __name__ == "__main__":
    main()
