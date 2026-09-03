# Public-artifact interoperability audit (C2) — selection protocol

Frozen selection rules for the GenomeML Report Card C2 registry.
This is an **interoperability study**, not a search for nonconforming publications.

## Inclusion (all required)

1. An identifiable evaluation claim or deployment statement (paper, README, or benchmark documentation).
2. A version-traceable public **evaluation-related** artifact, such as a membership release, split generator, sample-identifier manifest, label resource, metrics archive, code repository, and/or dataset release (commit, DOI, release tag, or archive stamp).
3. Task is genome/sequence ML (primary target domain, including human genomic/regulatory sequence classification) **or** an adjacent biological-ML evaluation ecosystem used as a source-preserving interoperability test (transcriptomics, single-cell, protein-variant assays).
4. Selection is **not** based on expected audit outcome or paper impact.

**Membership availability is an audit outcome, not an inclusion criterion.** C2 records whether publicly released artifacts suffice to establish membership directly, regenerate it deterministically, or support only partial assessment (`direct_release` / `deterministic_generator` / `unavailable`).

## Exclusion

- No identifiable evaluation claim **and** no version-traceable evaluation-related artifact.
- Data/code version cannot be located at all.
- Identifiers cannot be aligned to any usable manifest when membership assessment is attempted (outcome may still be `not assessable` if the case is otherwise in scope as claim+artifact).

## Outcome axes (not prevalence)

Each included case is coded on four axes (see `evaluation_audit_outcome_taxonomy.md`):
claim specification; artifact sufficiency; mechanical conformance; biological-block validation.

Deliberate nonconformance is demonstrated in **C1 constructed fixtures**. C2 may include
real-world `nonconformant` rows only when an official artifact fails its own declared rule;
hunting for such rows is **not** a selection goal.

## Case packaging

```text
c2_registry/<case_id>/
  contract.yaml
  field_mapping.yaml
  source_provenance.json
  retrieval_notes.md
  audit_output.json   # when assessed
```

Raw evidence may live under `c2_artifacts/<case_id>/`.
