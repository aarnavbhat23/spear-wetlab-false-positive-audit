# SPEAR wet-lab false-positive audit

This temporary repository exists for an independent, adversarial review of the
wet-lab antimicrobial-peptide dataset prepared for SPEAR. The audit question is
simple: **does every sequence in the positive-only table have defensible,
sequence-specific experimental evidence of antimicrobial activity?**

This is a bug-finding exercise. The reviewer should try to disprove rows, not
summarize the papers or praise the extraction.

## Primary dataset

`data/df_wetlab_validated.tsv` has exactly five columns:

```text
sequence  wetlab_experiment  mic  paper_title  paper_doi
```

It contains 2,449 peptide–assay rows representing 596 unique sequences from 22
primary journal papers. It is long-form: one sequence may have several rows
because each organism or strain measurement is stored separately.

- 2,342 rows contain a reported numerical MIC.
- 107 rows have a blank MIC. These were included because the cited source
  identifies the sequence as experimentally active, but a safe numerical value
  was not recoverable from the public machine-readable material.
- Reviews, preprints, predictions and censored/no-inhibition results are meant
  to be absent from this positive-only table.

## Companion evidence

- `data/df_wetlab_heatmap_results.tsv` contains the broader extracted assay
  matrix, including censored/no-inhibition cells.
- `data/df_cesar_wetlab_round1.tsv` records paper-level tested, active and mouse
  cohort counts for all 32 final journal papers in the César catalogue.
- `data/df_cesar_murine_validated.tsv` contains source-linked murine-efficacy
  records.
- `data/df_cesar.tsv` is the authoritative 32-paper catalogue.

## What counts as a false positive

A row or sequence should be flagged when one or more of these statements is
supported by evidence:

1. The peptide was tested but had no antimicrobial activity, yet appears in the
   positive-only table.
2. The result belongs to a different sequence, analog, stereoisomer or terminal
   modification.
3. A prediction, structural assay, toxicity assay, immune-only result or mouse
   outcome was mistaken for direct antimicrobial validation.
4. A heatmap ceiling, missing value or censored result was transcribed as an
   exact positive MIC.
5. A sequence-to-name, table-column or DOI/title join is shifted or incorrect.
6. The paper-level active count contradicts the number or identity of sequences
   represented without a documented explanation.

Multiple rows for one peptide are not inherently duplicates or false positives.
They usually represent different strains. A high MIC is not automatically a
false positive unless the source defines it as no inhibition or above the assay
ceiling.

## Required evidence standard

Every proposed issue must identify the sequence, DOI, affected row(s), source
location and the exact nature of the contradiction. Separate findings into:

- **Confirmed false positive** — the source directly contradicts inclusion.
- **Likely false positive** — strong evidence, but one source element is still
  unavailable.
- **Needs manual verification** — insufficient evidence to classify.
- **Not an issue** — suspicious pattern explained by the long-form schema or
  assay design.

Do not invent MICs, sequence mappings or paper conclusions. If the source is
unavailable, mark the item for manual verification.

## Deliverable

Write `findings/INDEPENDENT_AUDIT.md` with:

1. a short verdict;
2. counts by finding category;
3. a row-level evidence table;
4. checks that passed;
5. unresolved source-access limitations;
6. precise recommended corrections, without editing the input TSVs.

The ready-to-use reviewer instruction is in `AUDIT_PROMPT.md`.

