# Independent SPEAR wet-lab false-positive audit

Date: 2026-09-13

Scope: `data/df_wetlab_validated.tsv` plus the companion TSVs in this repository. I ran the repository structural checks and targeted the suspicious cases requested in `README.md` and `AUDIT_PROMPT.md`: blank MICs, sequence/name joins, censored heatmap values, stereochemistry, terminal modifications, and paper-level count mismatches. I did not edit any input TSV.

## Short verdict

I did not find evidence that the large positive table is broadly contaminated by inactive peptides, prediction-only hits, mouse-only outcomes, or censored no-growth values transcribed as exact MICs.

I did find one high-confidence class of contamination for sequence-only model training: several rows describe assayed compounds whose chemistry is not represented by the primary `sequence` field. The strongest examples are all-D peptides and C-terminally amidated peptides. These are real antimicrobial molecules, so the source evidence is not false; the false-positive risk is that the unmodified one-letter amino-acid string is labeled active when the assayed molecule is a different stereoisomer and/or terminally modified chemical entity.

Recommended go/no-go: no-go for training a model that consumes only the `sequence` column until chemistry-bearing rows are either removed from the sequence-only training set or given structured chirality/terminal-modification fields. Go with caution for evidence review or training pipelines that retain a full peptide-chemistry representation and source identifiers.

## Counts by category

| Category | Count | Interpretation |
| --- | ---: | --- |
| Confirmed false positives / chemistry-encoding bugs for `sequence`-only training | 26 rows, 19 unique bare sequence strings | Source evidence shows the active assay belongs to all-D and/or C-terminally amidated peptide chemistry not encoded in `sequence`. |
| Likely issues | 5 rows, 5 unique bare sequence strings | Rows are already annotated as C-terminal amides and have figure-level antimicrobial support, but I did not re-open enough source detail to promote them to confirmed before source discovery was stopped. |
| Needs manual verification | 36 rows, 36 unique sequences | Wasp-CRPS blank-MIC rows are supported by source sequence tables and figure/round1 locators but require visual panel-level verification for exact activity/threshold. |
| Not-an-issue patterns checked | 107 blank-MIC rows across 5 DOI clusters; several count and duplicate-ID patterns | Most suspicious blanks and count mismatches had defensible explanations or indicate incompleteness rather than false positives. |

The 26 confirmed chemistry-encoding rows are rows 2-11, row 39, and rows 1862-1874 plus 1881-1882 of `data/df_wetlab_validated.tsv`. Row 38 (`L-GK17`) is not a chemistry false positive; it is the L-enantiomer record for the same bare sequence string.

## Confirmed false positives / chemistry-encoding bugs

These findings should be treated as false positives only under the current five-column, sequence-only schema. The assayed compounds themselves appear to be antimicrobial according to the cited source.

| Finding | Affected rows | Bare sequence(s) in `sequence` | DOI | Source locator and evidence | Severity | Recommended correction |
| --- | --- | --- | --- | --- | --- | --- |
| MRGPRB2/DJK5 analogues are all-D and C-terminally amidated, but stored as ordinary uppercase one-letter sequences. | 2-11 | `VQWDAIRVRVIR`; `VQWEAIRVRVIR`; `VQWRAIRDRVIR`; `VQWRAIRVRDIR`; `VQWRAIRVRKIR`; `VQWRAIRVRRIR`; `VQWRAIRVRVIR`; `VQWRAIRVRVIT`; `VQWRAIRVRVKR`; `VQWRAWRVRVIR` | 10.1016/j.celbio.2025.100088 | Article Table 1 lists DJK5 and variants in lowercase one-letter notation and states that all sequences are C-terminally amidated. The article text says DJK5 is formed exclusively by D-amino acids. Figure 1B is the antimicrobial activity heatmap. The extraction correctly omits `[Pro]7-DJK5`, which the article says lacks direct activity under the tested conditions. | High for sequence-only training; low for source truth if chemistry metadata is preserved. | Add structured fields such as `stereochemistry=all-D` and `c_terminal_modification=amide`; otherwise exclude rows 2-11 from any unmodified-L-sequence positive training set. Do not replace them with unmodified L-peptide positives unless a source tests those exact L/unamidated chemicals. |
| D-GK17 row collapses an all-D enantiomer onto the same bare sequence as L-GK17. | 39 only for the all-D row; row 38 is the separate L-GK17 row. | `GKEFKRIVQRIKDFLRN` | 10.1016/j.celbio.2026.100452 | Supplementary Table S1 lists `GK-17` as `GKEFKRIVQRIKDFLRN` and `D-GK17` as lowercase `gkefkrivqrikdflrn`. The same paper reports broth microdilution MICs of 1.56 uM for GK17 and 3.12 uM for D-GK17 against A. baumannii ATCC 19606. | High, because the table has two chemically different peptides under one `sequence` key. | Split chirality in a structured field. For sequence-only training, keep row 38 as the L-sequence positive and remove or segregate row 39 unless D-chirality can be encoded. |
| Designed nanopore peptides with `+9-NH2` names are C-terminally amidated, but the `sequence` field omits `-NH2`. | 1862-1874 and 1881-1882 | `KKKKLDDILDDLFQFIKQLKNKLQKIKKKK`; `KKKKLKKFFKKLIQLINQLFDDLDDFKKKK`; `KKKKLKKILKKLFQFIDQLDNDLQDIKKKK`; `KKKKLKKILKKLFQFINQLDNQLQDIKQNK`; `KKKKLKKILKKLFQFINQLIDDLDDIKKKK`; `KKKKLKKILKKLIQLIDQLDNDLQDIKKKK`; `KKKKVKKVVKKVFSFVDSVDSDVSDVKKKK`; `RRRRLRRILRRLFQFINQLDNQLQDIRQNR` | 10.1038/s41589-026-02269-z | The article supplement describes the `+9-NH2` variants as having an amidated C-terminus and notes that atomistic simulations made peptide C-termini amidated to match experimentally tested peptides. The validated rows cite Table 1 MIC assays against E. coli K-12 and/or S. carnosus TM300. | Medium-high for sequence-only training; not a source false positive for the amidated compounds. | Add `c_terminal_modification=amide` and preserve the peptide names (`DKFC16+9-NH2`, `KDFD24+9-NH2`, `KDFC16+9-NH2`, `KDFA2i+9-NH2`, `KDFC21+9-NH2`, `KD16+9-NH2`, `KDFC16+9SV-NH2`, `RDFA2i+9-NH2`). Exclude these rows from unmodified-sequence training if the model cannot represent terminal amidation. |

## Likely issues

| Finding | Affected rows | Bare sequence(s) | DOI | Evidence already collected | Severity | Recommended correction |
| --- | --- | --- | --- | --- | --- | --- |
| Frog-derived dF-AndD1 rows are recorded as C-terminal amides with blank MICs. This is probably the same terminal-modification issue as the confirmed nanopore rows, but I am leaving it as likely because I did not complete a fresh source-panel verification before source discovery was stopped. | 421-425 | `IFLKKNIINSLFGR`; `IFPKKNIINSLFGR`; `IFPKKNIINSLFKR`; `IFPLLNIINSLFGR`; `IKPKKNIINSLFGR` | 10.1016/j.tibtech.2025.02.007 | The rows cite broth microdilution antimicrobial heatmaps and explicitly say `C-terminal amide` for L3-dF-AndD1, dF-AndD1, K13-dF-AndD1, L4,L5-dF-AndD1, and K2-dF-AndD1. The article supplement contains figure captions for antimicrobial heatmaps and second-generation libraries; `df_cesar_wetlab_round1.tsv` records 18 active of 19 tested, with A8-dF-AndD1 as the inactive control. | Medium for sequence-only training; unresolved for exact source panel values. | Verify the source figure panels visually, then either add `c_terminal_modification=amide` or exclude rows 421-425 from unmodified sequence-only training. Keep MIC blank unless an exact value is recoverable from the source. |
| Venomics duplicate source peptide IDs collapse to the same `sequence` and sometimes give different MIC/censored results for the same organism label. | Six duplicated `sequence`+DOI+experiment keys have multiple exact MICs; three also have exact-vs-`>64 uM` conflicts in `df_wetlab_heatmap_results.tsv`. Examples: `KLLKIGLKSFARVLKKVL`; `KNKRFIRNLRSNLYQKIIKSTKSLL`; `KRRRASPLWKRRRFLSMLKARAK`. | See previous cell | 10.1038/s41467-025-60051-6 | The source mapping assigns the same amino-acid string to multiple peptide IDs, e.g. `KLLKIGLKSFARVLKKVL` as UniprotKB-1 and Arachnoserver-1, `KNKRFIRNLRSNLYQKIIKSTKSLL` as UniprotKB-14 and Arachnoserver-9, and `KRRRASPLWKRRRFLSMLKARAK` as UniprotKB-10 and Conoserver-2. Supplementary source workbook `41467_2025_60051_MOESM7_ESM.xlsx`, sheet `Figure 2a`, has different row-level values for those IDs. | Low for binary positive labels, medium for exact MIC modeling. | Add a `peptide_id` or `source_row_id` field before collapsing. If sequence-only output is required, define a clear replicate policy, e.g. keep minimum exact positive, keep all source-ID replicates with IDs, or aggregate to a single sequence-strain result with provenance. |

## Needs manual verification

| Item | Affected rows | DOI | Why unresolved | Recommended action |
| --- | --- | --- | --- | --- |
| Wasp-CRPS blank-MIC rows for WT1/WT2, alanine-scan variants, and second-generation derivatives. | 426-461; 36 unique sequences | 10.1016/j.xcrp.2023.101459 | The article supplements identify the 36 sequences, and `df_cesar_wetlab_round1.tsv` says antimicrobial results are in Figures 1B, 2A, S2, and S4 with 36 active of 36 tested. I did not finish visual panel-level verification of every heatmap cell before the stop request. The public machine-readable material I inspected did not provide safe per-row MICs, which explains the blank MICs. | Manually inspect the cited figures and confirm that every listed derivative meets the paper's active threshold. Keep MIC blank unless exact values can be recovered. |
| Frog-derived rows, exact activity and terminal-amide source confirmation. | 421-425; 5 unique sequences | 10.1016/j.tibtech.2025.02.007 | See likely-issue row above. The rows are plausible positives and the paper-level counts support the cohort, but source verification was incomplete. | Verify figure panels and chemistry notation before final release. |

## Not-an-issue patterns

| Pattern checked | Rows / sequences | Evidence and interpretation | Recommendation |
| --- | ---: | --- | --- |
| SEP blank-MIC cluster is supported as active. | 55 rows, DOI 10.1016/j.cell.2024.07.027 | Local supplement `1-s2.0-S009286742400802X-mmc1.pdf` / extracted text identifies Table S2 as active SEPs. Local article evidence says 78 SEPs were synthesized and 55 were active in broth microdilution assays. The 55 blank rows therefore are not inactive false positives; the blank MIC reflects unrecovered exact values. | Keep as positives with blank MIC, or add source table locators. Do not invent numeric MICs. |
| AMPSphere global ten lead rows are active despite blank MICs. | Rows 40-49, DOI 10.1016/j.cell.2024.05.013 | The final article text says 100 AMPs were synthesized/tested and 79 were active; the ten rows are the named A. baumannii lead set selected for mouse assays. The article gives exact A. baumannii MICs for the ten names/IDs: synechocucin-1 8 uM, proteobacticin-1 16 uM, actynomycin-1 64 uM, lachnospirin-1 2 uM, enterococcin-1 1 uM, alphaprotecin-1 1 uM, oscillospirin 8 uM, ampspherin-4 8 uM, methylocellin-1 2 uM, and reyranin-1 16 uM. | These are not false positives. If the dataset allows manual source values, populate row MICs with the exact source values and retain the source locator; otherwise keep blank and document that these are confirmed active leads. |
| Mast-MO blank row is supported as direct antimicrobial, not mouse-only or immune-only. | Row 2444, sequence `FLPIIINLKALAALAKKIL`, DOI 10.1073/pnas.2012379117 | Local supplement `wasp_pnas_pnas.2012379117.sapp.txt` lists Mast-MO sequence in Table S6 and includes antimicrobial activity figure captions for clinically relevant Gram-negative strains and CFU assays. The abstract says Mast-MO had increased antibacterial properties in vitro and in vivo. | Keep row with blank MIC unless exact MIC values are recovered. |
| De-extinction paper count mismatch is explainable by two source cohorts. | DOI 10.1038/s41551-024-01201-x; validated has 53 unique sequences while round1 says 41 active | Source workbooks `41551_2024_1201_MOESM4_ESM.xlsx` and `41551_2024_1201_MOESM5_ESM.xlsx` were parsed. MOESM4 has 41 active APEX/MEP sequences; MOESM5 adds 12 active scoring-function/control sequences. The validated table's 53 unique sequences equal the combined active set; no inactive validated sequence was found in this check. | Not a false positive. Update `df_cesar_wetlab_round1.tsv` count or notes if that table is meant to describe all positives represented in `df_wetlab_validated.tsv`; otherwise clarify that 41 refers only to the main APEX cohort. |
| Venomics represented count lower than paper active count. | DOI 10.1038/s41467-025-60051-6; round1 active 53, validated 50 unique sequences | This is incompleteness or filtering, not a false-positive contradiction. The checked duplicate-ID cases are supported by source workbook values. | Review for missing positives if completeness matters; do not remove the 50 on this basis. |
| AMPSphere, frog, and AMPDiffusion counts are lower than paper active counts. | DOI 10.1016/j.cell.2024.05.013: 79 active vs 10 rows; DOI 10.1016/j.tibtech.2025.02.007: 18 active vs 5 rows; DOI 10.1016/j.celbio.2025.100183: 35 active vs 26 rows | These are subset/incompleteness patterns, not evidence that included rows are inactive. | Clarify whether `df_wetlab_validated.tsv` is intended to be exhaustive per paper. If not, note that it contains selected/source-recoverable positives. |
| Multiple rows per sequence are expected in the long-form schema. | Many rows | The primary README says one sequence may have several rows because each organism/strain measurement is stored separately. | Not a duplicate issue unless the same sequence, same DOI, and same organism/experiment key conflict without source-ID provenance. |

## Structural and consistency checks passed

I ran `python3 scripts/structural_checks.py`; it reported:

```text
rows=2449
unique_sequences=596
primary_papers=22
rows_with_mic=2342
rows_without_mic=107
maximum_rows_for_one_sequence=23
structural_checks=PASS
```

Additional read-only checks:

- All five TSVs opened successfully with tab delimiters.
- `df_wetlab_validated.tsv` has exactly the documented columns: `sequence`, `wetlab_experiment`, `mic`, `paper_title`, `paper_doi`.
- No duplicate full rows were found in any TSV.
- Validated sequences use only the 20 canonical amino-acid letters and have lengths in the documented 8-50 range.
- The validated DOI set matches the primary-research DOI set asserted by the repository structural script.
- The 107 blank MIC rows are confined to five DOI clusters: 55 SEP rows, 36 Wasp-CRPS rows, 10 AMPSphere global rows, 5 frog rows, and 1 Mast-MO row.
- No validated `mic` string retains a leading `>` censored marker.
- For papers represented in `df_wetlab_heatmap_results.tsv`, exact validated rows were generally traceable to exact/non-censored heatmap entries. The apparent exact-vs-censored overlaps were concentrated in Venomics duplicate source peptide IDs with identical sequence strings, not direct evidence of inactive peptides.

## Unresolved limitations

- I stopped further source discovery when requested. This report is therefore intentionally defensible rather than exhaustive across all 22 primary papers.
- Some public sources were available only as PDF figure panels or extracted text; I did not visually verify every cell in the Wasp-CRPS and frog heatmaps.
- The current five-column schema cannot represent source peptide ID, chirality, terminal amidation, raw censored values, or source table cell coordinates. Several findings are therefore schema bugs, not necessarily extractor mistakes.
- I did not modify `df_wetlab_validated.tsv`; all row numbers above refer to the current file with the header on line 1.

## Recommended corrections before model training

1. Add structured peptide-chemistry fields before using this as a training table:
   - `peptide_name`
   - `source_peptide_id` or `source_row_id`
   - `stereochemistry` (`L`, `all-D`, mixed, unknown)
   - `n_terminal_modification`
   - `c_terminal_modification`
   - `raw_mic_value`
   - `mic_relation` (`=`, `>`, `<`, blank confirmed active)
   - `assay_organism_or_strain`
   - `source_locator`

2. For immediate sequence-only training, exclude or segregate:
   - rows 2-11 (`all-D`, C-terminally amidated DJK5/MRGPRB2 analogues);
   - row 39 (`all-D GK17`);
   - rows 1862-1874 and 1881-1882 (`+9-NH2` nanopore peptides);
   - rows 421-425 until frog chemistry/source panels are manually confirmed.

3. Preserve row 38 (`L-GK17`) as a valid L-sequence positive unless a later source check contradicts it.

4. Preserve the 55 SEP rows, 10 AMPSphere lead rows, and Mast-MO row as supported positives, but keep MIC blank unless exact source values are deliberately added with locators.

5. Add a Venomics peptide-ID column or deduplicate with an explicit policy. The same bare sequence can occur under multiple source peptide IDs with different reported MICs; collapsing without IDs makes exact MIC modeling ambiguous.

6. Update or annotate paper-level counts in `df_cesar_wetlab_round1.tsv` where they describe only a subset of the positives represented in `df_wetlab_validated.tsv`, especially the de-extinction paper's 41 vs 53 active-sequence explanation.
