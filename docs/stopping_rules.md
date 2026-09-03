# Declared-block E2E search — stopping rules (frozen)

**Frozen date:** 2026-09-03  
**Criteria:** `docs/e2e_candidate_acceptance_criteria.md`  
**Search log:** `docs/e2e_candidate_search_log.md`  
**Disposition table:** `docs/candidate_disposition_table.csv`

## Triggered stop

Open-ended search for a **second genome-ML declared-block E2E** is **stopped**.

Rationale: youngfran and VirHost/RNAVirHost were triaged under A1–A8 and rejected for membership/generator reasons that are informative negative findings, not incomplete screening. Further hunting has diminishing returns for  submission and risks A8 violations (inventing seeds/LOGO).

## Rules

1. Do **not** invent GroupKFold, seeded subsamples, or LOGO reconstructions to manufacture a second E2E.
2. Do **not** delay submission waiting on BIG-TB unless maintainers already delivered membership/phenotype artifacts.
3. Re-open a candidate **only** if upstream newly releases either:
   - direct unit→block→partition membership, or
   - a fully specified deterministic generator (code + frozen inputs + seed/parameters) that regenerates membership without ambiguity.
4. Negative dispositions mean **cannot audit the reported evaluation membership**, not that the authors’ scientific evaluation is invalid.
5. Manuscript claims must not imply “two independent genome-ML declared-block E2Es”; GeneLab is a direct-membership **route** (transcriptomic); under the frozen registry/screen, Hu is the only packaged **genome-ML** generator-derived E2E in this release (do not use absolute “sole in the literature” wording in main-text tables).

## Allowed residual work (non-search)

- Optional BIG-TB maintainer issue (non-blocking)
- v0.2.0 / Zenodo / Hu frozen-input archive
- Nested-CV smoke already hardened (`docs/PRIMARY_NESTED_SMOKE.md`)
- Manuscript claim-intensity edits consistent with this freeze
