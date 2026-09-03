# GenomeML Report Card audit status rules (fail / warn / info)

| Audit condition | Status | Meaning for interpretation |
|---|---|---|
| Required manifest fields absent / feature–table length mismatch | **Fail** | Contract cannot be evaluated; correction required |
| Exact sequence-ID overlap across compared partitions (`--table-b`) | **Fail** | Partition contamination risk |
| User-provided split: declared block in both train and test within a fold | **Fail** | Inconsistency with a **strict block-exclusion contract**; does not invalidate all alternative evaluation goals |
| Near-neighbor candidate overlap (MinHash screen) | **Warn** | Candidate pairs for sequence-level review; not proof of homology |
| All singleton blocks / few unique blocks (`n_blocks<10`) | **Warn** | Declaration is executable, but the cohort has limited diagnostic value for block-level stress testing |
| High random-CV shared-block fraction (≥0.5) | **Info** | Random estimand likely differs from block-held-out estimand |
| Low within-block label homogeneity (<0.5) | **Info** | \(\Delta_B\) may be weak or non-monotone; does not invalidate the block |
| Large \(\|\Delta_B\|\) under declared probe (≥0.2) | **Info** | Cohort-conditional sensitivity; not an external forecast |

Overall `contract_status`: **fail** if any fail finding; else **warn** if any warn; else **pass** (info findings allowed).

Implemented in `genome_ml_reportcard.contract.evaluate_contract`.
