# Final acceptance checklist — C2-HU-MSMA-LOSO-OUTER

**Date:** 2026-09-02  
**Decision:** ACCEPT as generator-derived declared-block E2E

| Check | Result |
|---|---|
| A. Claim evidence (code L219–220 verbatim + commit + SHA256 snapshots) | PASS — `evidence/upstream_code/` |
| B. Deterministic outer generator (no outer random subsample; 9 fixed species) | PASS — inner homology seed 42 irrelevant to outer membership |
| C. ID mapping (`iso_` strip; no external PATRIC API) | PASS — deterministic adapter |
| D. Membership form (secondary-strong: frozen species files + LOSO spec) | PASS — `processed/fold_assignment_regenerated.tsv` |
| E. Beyond recurrence: coverage, uniqueness, provenance, label join report | PASS — see `processed/audit_report.json` |
| A1–A8 | ALL PASS |

**Manuscript phrasing (required):**

> A version-pinned outer leave-one-species-out protocol in the Hu et al. MSMA-concat implementation enabled deterministic regeneration of nine species-held-out evaluation folds…

**Forbidden phrasing:** “Hu provide an official species-disjoint fold release.”


## Offline regeneration

```bash
python3 scripts/regenerate_hu_msma_loso_outer.py
```
Writes `fold_assignment_regenerated.tsv`, `fold_counts.tsv`, `unit_to_block.tsv`, and `regeneration_environment.json` from frozen `evidence/` only.
