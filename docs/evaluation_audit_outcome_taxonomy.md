# Unified evaluation-audit outcome taxonomy (A, C1, C2)

Shared vocabulary across structured field audit (A), protocol-conformance
**reference suite** (C1), and real-world evaluation-artifact audit (C2).

## Layered vocabulary (do not conflate)

| Layer | Labels |
|-------|--------|
| Report-level severity (`contract_status`) | `pass` · `warn` · `fail` |
| Mechanical conformance (axis) | `conformant` · `nonconformant` · `not_assessable` · `not_required` |
| C1 fixture expected outcome | `conformant` · `deliberately_nonconformant` · `insufficient_split_artifact` (+ related insufficient_*) |
| C2 four axes | claim specification · artifact sufficiency · mechanical conformance · biological-block validation |

`contract_status` is report-level severity; mechanical conformance is axis-specific. C1 `deliberately_nonconformant` marks constructed fixtures only.

## Four-axis audit model (preferred)

C2 (and preferably A/C1 reporting) records **four independent axes**. A single
legacy `audit_outcome` string is retained only as a **derived display label**
for CI/regression compatibility.

| Axis | Allowed values | Meaning |
|------|----------------|---------|
| **claim_specification_status** | `specified` · `underspecified` · `not_recoverable` | Whether a deployment/generalization claim is clear enough to write a contract. |
| **artifact_sufficiency_status** | `sufficient` · `partially_sufficient` · `insufficient` · `pending` | Whether official, version-alignable split/membership (or reconstructible generator export) exists for the declared contract. |
| **contract_conformance_status** | `conformant` · `nonconformant` · `not_assessable` · `not_required` · `deliberately_nonconformant` (C1 only) | Mechanical consistency of the supplied split with the **scoped** contract under audit. |
| **biological_block_validation_status** | `verified` · `not_independently_verified` · `not_required` · `not_applicable` | Whether an independent biological block map (species/clade/country/…) was used beyond the fold file itself. |

### Scope rules (critical)

- `contract_conformance_status=conformant` for a **released fold-membership partition** does **not** imply phylogenetic/clade exclusion was independently verified.
- `artifact_sufficiency_status=insufficient` is an **auditability** state, not scientific invalidity of the study.
- `biological_block_validation_status=not_required` applies when the declared contract is sequence-level (or otherwise non-block) holdout.
- Non-overlapping test folds ≠ phylogenetically disjoint train/test partitions.

### C2 MVP mapping examples

| Case | claim_specification | artifact_sufficiency | contract_conformance | biological_block_validation | Legacy display |
|------|---------------------|----------------------|----------------------|-----------------------------|----------------|
| Hu AMR phylo folds | specified | sufficient (fold membership) | conformant (released fold partition) | not_independently_verified | `conformant` (scoped) |
| GenomicBenchmarks promoters | specified | sufficient | conformant (sequence-ID holdout) | not_required | `conformant` |
| Mollentze zoonotic_rank | specified | insufficient | not_assessable | not_applicable | `insufficient_split_artifact` |

## Legacy display labels (C1 / derived)

| Legacy `audit_outcome` | Typical derivation |
|------------------------|--------------------|
| **conformant** | `artifact_sufficiency=sufficient` and `contract_conformance=conformant` under the **scoped** contract (may still have `biological_block_validation≠verified`). |
| **deliberately_nonconformant** | C1 constructed fixture only. |
| **nonconformant** | Author/benchmark split shows recurrence under an explicit strict holdout claim. |
| **different_estimand** | Recurrence may occur but source does not claim strict block exclusion. |
| **insufficient_split_artifact** | `artifact_sufficiency=insufficient` for membership reconstruction. |
| **insufficient_version_alignment** | Candidates exist but cannot be linked to the study version. |
| **insufficient_metadata** | Split present but target block column missing/unalignable. |
| **claim_underspecified** | `claim_specification=underspecified`. |
| **not_assessed** | Retrieval/audit pending. |

**C2 retrieval_status:** `retrieved` | `retrieved_search_complete` | `insufficient_version_alignment` | `pending` / `not_assessed`.

**Manuscript rules:** Random splits are not intrinsically invalid; they are nonconformant **only relative to a declared strict block-exclusion claim**. Prefer “mechanically nonconformant relative to declared contract” over punitive “failed” for published C2. `insufficient_*` ≠ scientific invalidity.

**C1 vs C2:**
- **C1** — constructed **protocol-conformance reference suite** (conformant, deliberately_nonconformant, insufficient fixtures).
- **C2** — author/benchmark official artifacts only; report all four axes.
