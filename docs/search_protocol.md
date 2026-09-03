# Declared-block E2E candidate search protocol

**Start:** 2026-09-02  
**Freeze / stop triggered:** 2026-09-03 (`docs/stopping_rules.md`)  
**Acceptance criteria:** `docs/e2e_candidate_acceptance_criteria.md` (A1–A8; distinct from C1 fixtures / C2 registry)  
**Live log:** `docs/e2e_candidate_search_log.md`  
**Machine-readable dispositions:** `docs/candidate_disposition_table.csv`

## Objective

Identify whether a **second** official/traceable **genome-ML** declared-block E2E (beyond Hu MSMA LOSO outer) exists in public artifacts—**without** post-hoc protocol invention.

## Scope

- Prefer pathogen / viral / microbial genome-ML tasks with biological holdouts (species, lineage, genus, family, geography, time).
- Allow deterministic generators only when author-specified and fully frozen.
- GeneLab-style transcriptomic holdouts may illustrate a **direct-membership route** but do **not** fill the genome-ML E2E slot.
- Chromosome-only human sequence splits deprioritized unless the declared deployment claim is chromosome-level.

## Screening procedure

1. Locate claim (paper/README) of biologically structured generalization / holdout.
2. Pin version (commit, DOI, archive hash).
3. Search for unit→partition membership **or** complete deterministic generator.
4. Score A1–A8; record disposition even on reject.
5. Stop per `docs/stopping_rules.md` (triggered 2026-09-03).

## What we do not count as success

- Metrics-only or label-only releases
- Unseeded random holdout sampling
- Our GroupKFold / LOGO constructed from taxonomy tables
- Remediations created in the analysis companion

## Outcome at freeze

Within this prespecified scope, packaged auditable declared-block evidence comprises:

- one direct-membership biological holdout route (GeneLab; transcriptomic), and
- one microbial genome-ML generator-derived E2E (Hu MSMA LOSO outer),

plus multiple negative dispositions (youngfran, VirHost, VirusTaxo boundary, BIG-TB blocked) documenting that claim + code + metrics/labels often lack recoverable membership.
