# GenomeML Report Card — analysis companion

Frozen tables, protocols, and regenerators that support the manuscript:

**GenomeML Report Card: a machine-readable audit framework for biological generalization claims in genome machine learning**

## Software (installable package)

Canonical software repository: https://github.com/Xindi-Wang1004/GenomeML-ReportCard

```bash
pip install genome-ml-reportcard
genome-ml-reportcard --help
```

Zenodo software archive (concept DOI): https://doi.org/10.5281/zenodo.22275801

## What this companion contains

| Path | Contents |
|------|----------|
| `tables/` | Frozen main/supplementary result tables (C2 registry, nested CV, audits, S1b MD5-identical accessions, …) |
| `protocol_conformance_benchmark/` | `c2_case_registry.json` and Hu MSMA LOSO outer **processed** freeze |
| `scripts/` | `reproduce_main_tables.sh` and regenerators used for archived tables |
| `docs/` | C2 protocol, search/stopping rules, assertion provenance notes |
| `figures/` | Key manuscript / supplementary figure PNGs |

This is a **reproduction freeze**, not a full compute dump: embeddings, raw genomes, and large model checkpoints are not included. Upstream public datasets remain regenerable from their original sources (see manuscript Data availability).

## Quick start

```bash
git clone https://github.com/Xindi-Wang1004/GenomeML-ReportCard-companion.git
cd GenomeML-ReportCard-companion
# Inspect frozen tables
ls tables/
# Optional: regenerate Hu MSMA LOSO outer membership from frozen processed inputs
python3 scripts/regenerate_hu_msma_loso_outer.py --help || true
```

## Citation

Please cite the GenomeML Report Card manuscript and the software archive DOI above.
