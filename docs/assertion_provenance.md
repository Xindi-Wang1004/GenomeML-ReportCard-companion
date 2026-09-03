# Assertion provenance (contract field sources)

Mechanical conformance is assessed relative to the **recorded** evaluation contract.
`assertion_provenance` records **who declared** each contract field. It is not a
biological validation of the deployment block.

## Allowed values

| Field | Allowed values |
|---|---|
| `claim` | `author_declared`, `upstream_release`, `curator_mapped`, `user_supplied`, `remediation_only`, `not_available` |
| `deployment_block` | same |
| `unit_to_block_mapping` | same |
| `split_membership` | same, plus `direct_release`, `deterministic_generator` |
| `curation_status` | `source_preserving`, `adapter_only`, `remediation_only`, `user_supplied` |

## Definitions

| Value | Meaning |
|---|---|
| `author_declared` | Explicitly stated in the paper, README, or author-maintained documentation |
| `upstream_release` | Present in an official release artifact (dataset, fold file, metadata table, pinned code) |
| `curator_mapped` | Report Card curator mapped a field from released materials without inventing a new biological rule |
| `user_supplied` | Provided by the contract user at audit time |
| `remediation_only` | Introduced only in a remediation / analysis-companion demonstration |
| `not_available` | Field cannot be established from released materials |
| `direct_release` | Membership (unit→partition) exported as a version-pinned artifact |
| `deterministic_generator` | Membership regenerated from a version-pinned upstream generator + frozen inputs |
| `source_preserving` | Upstream artifacts used without rewriting their membership semantics |
| `adapter_only` | ID joins / packaging adapters applied; membership semantics remain upstream-defined |
| `remediation_only` (curation) | Membership created for a publication-fix demonstration, not as upstream E2E |

## Software interface

- JSON Schema: `schemas/reportcard_report.schema.json` → `assertion_provenance`
- CLI: `--assertion-provenance path/to/{json,yaml}`
- Module: `genome_ml_reportcard.assertion_provenance`

## Registry summary

Main-text–relevant rows: `tables/Table_S_assertion_provenance.csv`.
