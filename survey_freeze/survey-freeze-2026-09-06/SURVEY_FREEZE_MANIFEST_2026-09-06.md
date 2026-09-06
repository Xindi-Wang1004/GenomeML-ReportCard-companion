# Survey freeze package manifesto — `survey-freeze-2026-09-06`

**Freeze purpose.** Immutable auditability-screen archive for the GPB manuscript. This package supports verification of dispositions in Table 9; it is **not** a field-prevalence dataset.

**Decision lock:** `DECISION_LOCK_2026-09-06.md`  
**Search freeze date:** 2026-09-05 (Europe PMC)  
**Deep-coding / registry freeze date:** 2026-09-06

## Required contents (ship with submission)

| Path | Role |
|---|---|
| `survey_registry_frozen.csv` | Full coded registry (IDs, claims, depths, URLs, notes) |
| `screening/primary_outcome_panel.csv` | Compact primary + adjacent panel |
| `screening/screening_flow_counts.json` | Cascade counts (Q1–Q4, queue, wave3, primary n) |
| `AUDITABILITY_SURVEY_PROTOCOL.md` (parent `source_markdown/`) | Protocol + codebook |
| `DECISION_LOCK_2026-09-06.md` | Locked denominators / forbidden narratives |
| `run_europepmc_search.py` | Logged queries + retrieval caps |
| `logs/search_summary.json`, `logs/search_run_log.txt` | Hit counts / run log |
| `raw/Q1_*.csv|json`, `raw/Q2_*`, `raw/Q3_*`, `raw/Q4_*` | Retrieved ID lists / records |
| `screening/wave3_*.csv`, `Q3_ML_abstract_blocklang_hits.csv` | Enrichment triage dispositions |
| `screening/title_abstract_screen_queue.csv` | Working queue (honest: not fully human T/A’d) |

## Mirror plan (authors; before/at submission)

1. Tag companion release `survey-freeze-2026-09-06` containing the paths above (same bytes as this submission folder).
2. Deposit that tag to Zenodo; record version DOI in Data availability.
3. Do **not** back-date access statements: registry freeze and archive access should both read **2026-09-06** (or later final verify date).

## How to re-check Table 9

1. Open `survey_registry_frozen.csv`.
2. Filter `claim_declared=yes` and `stratum=AMR_core` (primary n = 6).
3. Confirm `verification_depth` and `main_barrier` against `notes` + linked `doi_or_url` / `repo_url`.
4. Confirm GeneLab (`ADJ-GENELAB-LOMO`) is adjacent / excluded from primary denominator.
5. Cross-check cascade integers in `screening/screening_flow_counts.json`.

## Explicit non-claims

- Not an exhaustive human screen of all 3471 queue records.
- Not a leakage-prevalence or “typical reporting practice” estimate.
- Author-mediated deposits (if any later) are never pooled into public direct-membership counts.
