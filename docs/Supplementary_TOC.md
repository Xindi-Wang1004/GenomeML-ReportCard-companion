# Supplementary Table of Contents (estimand-era pointers)

One-page guide to items cited from the main text (paths relative to `./` unless noted). Full cautionary-era numbered tables (S0–S15) remain in `02_Supplementary_Material.docx`.

| Item | Role (one line) | Primary path |
|---|---|---|
| S_integrity (figure) | Seq-level SpillOver-score eval + our-pool contamination rebuild | `figures/Figure4_viral_flagship.*` |
| S1b (table) | 111 MD5-identical accessions (dev ∩ eval) | `tables/Table_S_MD5_identical_accessions.csv` |
| S_external (figure/table) | T01/T07 external holdout panels | `figures/FigureS_external_holdout_t01.*`; tables under `tables/` |
| S_primary_nested | **Primary** nested Ridge-α repeated-CV (main-text Tables 2–3) | `tables/Table_primary_nested_cv.csv` |
| S_locked_alpha | Locked-α sensitivity (formerly primary; 15–40 repeats) | `tables/Table_locked_alpha_sensitivity.csv` |
| S_nested | Locked vs nested Δ contrast summary | `tables/Table_nested_tuning_sensitivity.csv` |
| S_systematic_audit | Eight-task executable audit matrix | `tables/Table_systematic_audit_8tasks.csv` |
| S_protocol_conformance | C1 protocol-conformance reference suite (n=12 fixtures) | `tables/Table_reference_protocol_conformance_benchmark.csv` |
| S_realworld_audit | C2 public evaluation-artifact audit (four-axis) | `tables/Table_realworld_supplied_split_audit.csv`; `protocol_conformance_benchmark/c2_case_registry.json` |
| S_case_contract_matrix | Distinct analyses vs declared contracts (Hu Table3 ≠ Hu Table5) | `tables/Table_case_to_contract_matrix.csv`; `docs/case_to_contract_matrix.md` |
| S_c2_heatmap | C2 four-axis verification-depth matrix | `tables/Table_c2_verification_depth_matrix.tsv`; `figures/Figure_c2_verification_depth_heatmap.*` |
| S_c2_case_level | Full C2 case-level registry (n=16; membership provenance) — main text Table 3 shows 8 representative rows | `tables/Table_c2_case_level_registry.csv` |
| S_assertion_provenance | Who declared each contract field (claim / block / mapping / membership / curation) for key cases | `tables/Table_S_assertion_provenance.csv`; `docs/assertion_provenance.md` |
| S_c2_depth_summary | C2 verification-depth tier rollup (n=16; direct vs generator-derived E2E split) | `tables/Table_c2_verification_depth_summary.tsv` |
| S_hu_msma_loso | Hu MSMA LOSO outer regenerator env + fold counts + SHA-256 | `c2_data/C2-HU-MSMA-LOSO-OUTER/processed/` |
| S_c2_external_trials | Source-preserving interoperability trials (GB + GeneLab) | `protocol_conformance_benchmark/external_trials/` |
| S_ecosystem | Positioning vs splitters / checklists / leaderboards | `tables/Table_ecosystem_positioning.csv` |
| S_deltaB_panels | Optional claim-specific Δ_B contrasts (former main Fig 3) | `figures/Figure3_multi_task_matrix.*` |
| S_c2_protocol | C2 inclusion/exclusion protocol | `docs/c2_public_artifact_interoperability_protocol.md` |
| S_semantic_boundary | Records vs verifies vs does not infer | `tables/Table_semantic_boundary.csv` |
| S_audit_taxonomy | Shared A/C1/C2 outcome definitions | `docs/evaluation_audit_outcome_taxonomy.md` |
| S_robustness (figure) | Locked-α contrast figure (companion to S_locked_alpha) | `figures/FigureS_robustness_delta_ci.*` |
| S_T08_logo (figure) | T08 leave-one-group-out AUROC | `figures/FigureS_T08_logo_per_group.*` |
| S_provenance | Protocol-specified vs dated amendments | `tables/Table_analysis_provenance.csv` |
| S_simulation | Label-geometry grid + sign-reversal / negative Δ_B | `tables/Table_simulation_label_geometry.csv` (+ summary JSON) |
| S_published_panel_audit | Babayan/Mollentze/Hu single-seed Report Cards | `tables/Table_published_panel_reportcard_audit.csv` |
| S_dual_declaration | Same panel, two claims | `tables/Table_dual_declaration_demo.csv` |
| S_contract_status | Fail/warn/info audit rules | `tables/Table_contract_status_rules.md` |
| S_T06_external | AMR BioSample temporal/geo holdouts | `tables/` (T06 external grid) |
| S_T07_threshold / S_T07_loo | T07 external sensitivity | `tables/` |
| S_literature | Illustrative structured audit (n=80; L1/L2/L3; not prevalence) | `tables/Table_literature_structured_field_audit.csv` |
| S_lit_summary | Field-audit prevalence summary | `tables/Table_literature_field_audit_summary.csv` |
| S_lit_kappa | Dual-coding Cohen's κ (n=16 subsample) | `tables/Table_literature_dual_coding_kappa.csv` |
| S_lit_methods | Seed-and-snowball scan transparency | `tables/Table_literature_scan_methods.csv` |
| S_guideline_map | Bernett/Whalen ↔ Report Card mapping | `tables/Table_guideline_reportcard_mapping.csv` |
| S_multimodel | Model-class split-design contrasts | `tables/Table_multimodel_split_contrast.csv` |
| S_audit | Public-dataset audit demos | `tables/Table_published_benchmark_reanalysis.csv` |
| Box S_reportcard_json | Toy report-card JSON | `tables/BoxS_reportcard_toy_audit.json`; GenomeML-ReportCard `tests/toy_data/` |
