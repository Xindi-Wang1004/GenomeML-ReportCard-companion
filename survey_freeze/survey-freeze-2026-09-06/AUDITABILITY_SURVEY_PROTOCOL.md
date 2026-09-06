# Auditability survey protocol — Option B+ (microbial genome ML / AMR core)

**Status:** EXECUTING — search frozen 2026-09-05; Europe PMC harvest complete; title prefilter done; human T/A screen pending.  
**Decision date:** 2026-09-05  
**Companion plan:** `OPTION_BPLUS_PLAN.md`

---

## 0. Design choice (locked)

**Universe = Option B (narrow):**  
Public microbial genome machine-learning studies and benchmark resources (2020–2026) that claim biological / deployment block-excluded evaluation, with **AMR / microbial phenotype prediction as the core stratum**.

**Out of primary scope (do not expand mid-stream):** human genomics foundation-model papers; protein engineering DMS; single-cell cross-donor (may be a sensitivity appendix only); general viral host ML as primary corpus (may be a secondary stratum if time allows, coded separately).

**Why:** species / lineage / geography / time claims are common; evaluation design is contested; public repos exist; existing Hu/PATRIC/OGT assets reuse; GPB readership alignment.

---

## 1. Estimands (locked)

### Primary

Distribution of **verification depth** among eligible resources with a **declared** biological block-exclusion claim, and frequency of **audit termination reasons**.

### Secondary

- Report Card readiness (full / partial / insufficient contract).
- Fraction with direct conformance assessable from public release alone.
- *(Optional)* author-mediated upgrade rate among contacted teams.

### Explicitly NOT estimands

- Prevalence of leakage / nonconformant splits.
- Prevalence of “authors did not implement block exclusion.”
- Model accuracy or biological validity of chosen blocks.

---

## 2. Inclusion / exclusion

### Include if all hold

1. Microbial genome / assembly / contig / k-mer / gene-content inputs for phenotype, AMR, host-range-from-genome, or related microbial prediction **or** a named public microbial genome-ML benchmark release.
2. Paper, README, methods, or benchmark protocol states evaluation that holds out a biological/deployment unit: species, strain, lineage, clade, ST, country/hospital, time window, or analogous microbial block (**verbatim preferred**; `normalized` allowed if operational field is explicit).
3. Publication or dataset release year in **2020–2026** (or living benchmark with a freeze date in that window).
4. At least one inspectable public artifact: PDF + (GitHub | Zenodo | HF | institutional archive).

### Exclude

- Splitter libraries with no pinned evaluation release.
- Non-genome modalities (MALDI, imaging) unless clearly labeled appendix.
- Claims that are only random / sequence holdout with **no** biological block language → not in primary denominator (`claim_declared = no`).
- Duplicate task rows under the same upstream release → collapse to one **evidence_source_id**.

---

## 3. Search strategy (freeze before running)

### Query seeds (Europe PMC / PubMed)

```text
(microbial OR bacterium OR bacterial OR "antimicrobial resistance" OR AMR OR pathogen)
AND
(genome OR genomic OR WGS OR "whole genome")
AND
("machine learning" OR "deep learning" OR "neural network" OR "random forest" OR "gradient boosting")
AND
("leave-one" OR LOSO OR LOLO OR "cross-validation" OR "held out" OR hold-out OR "group" OR lineage OR species OR clade OR phylogenetic OR "domain generalization")
```

### Supplementary sources

- GitHub / Zenodo / Hugging Face keyword pass for microbial AMR benchmarks.
- Backward citation of known seeds (Hu AMR benchmarking, BIG-TB, Engqvist OGT-related ML, etc.) — mark as **seed-augmented** and report separately from database hits.

### Recording

| Field | Example |
|-------|---------|
| search_date | YYYY-MM-DD |
| database | Europe PMC |
| query_id | Q1 |
| raw_hits | N |
| after_dedup | N |

---

## 4. Screening

1. Title/abstract: two reviewers on ≥20% sample; record Cohen’s κ or % agreement; discordances resolved by third or discussion.
2. Full-text / repo: single primary coder + 10–20% dual audit of deep fields.
3. Stop rule: complete the frozen hit list; do not keep snowballing without amending protocol.

---

## 5. Coding sheet (one row per evidence_source_id)

See `survey_registry_template.csv`.

Critical fields:

| Field | Values |
|-------|--------|
| claim_declared | yes / no / ambiguous |
| claim_source | paper / repo / benchmark_protocol / author_doc |
| assertion_status | verbatim / normalized *(auditor_interpreted excluded from primary)* |
| membership_released | yes / no / partial |
| membership_reconstructable | yes_deterministic / stochastic_unseeded / no |
| block_mapping_available | yes / no / partial |
| mapping_version_pinned | yes / no |
| identifier_namespace_ok | yes / no |
| direct_conformance_assessable | yes / no |
| verification_depth | direct-membership / author-mediated / upstream-regenerated / protocol-reconstructed / membership-only / format-compatibility / not-assessable / claim-not-declared |
| main_barrier | missing_membership / missing_mapping / claim_ambiguity / identifier_mismatch / inaccessible_data / non_deterministic_generator / none |
| reportcard_readiness | full / partial / insufficient |
| evidence_source_grouping | shared release key |

---

## 6. Author-mediated validation (Layer 3)

### Eligibility for outreach

Eligible if: claim_declared=yes AND (membership_released=no OR mapping missing) AND contactable corresponding / maintainer email AND not hostile license.

### Request (low burden)

See `outreach/AUTHOR_MEDIATED_REQUEST.md`.

### Coding if successful

- `verification_depth = author-mediated`
- Archive membership (+ optional mapping) on Zenodo or companion with SHA-256
- `asserted_by = original_authors` when they confirm claim text
- **Never** pool into public direct-membership counts

### Target

2–5 completed author-mediated contracts within the 4–8 week window. Zero responses still allow survey-only GPB attempt; ≥2 strongly preferred for Option B+.

---

## 7. Planned outputs

1. PRISMA-style flow figure  
2. Stacked verification-depth bars (denominator = claim_declared=yes; one row per evidence source)  
3. Barrier frequency table / heatmap  
4. Open registry CSV + codebook  
5. GeneLab remains optional adjacent exemplar (not forced into microbial denominator)  
6. Hu MSMA = protocol-reconstructed exemplar (if in corpus)  

### Allowed headline

> Publicly available microbial genome-ML artifacts frequently support a stated evaluation protocol but do not contain the minimum linked evidence needed for independent verification of the corresponding biological block-exclusion claim.

### Forbidden headlines

> Biological block exclusion is rarely implemented. / Widespread leakage was identified.

---

## 8. Effort

4–8 weeks calendar for Option B core + parallel outreach. Do not start GPB high-impact rewrite until registry freeze + figures exist.
