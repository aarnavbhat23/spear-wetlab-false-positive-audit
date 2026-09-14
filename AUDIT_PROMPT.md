# Independent reviewer prompt

Here is a bug-finding challenge. This repository contains a proposed
positive-only dataset of wet-lab validated antimicrobial peptides. Find false
positives that could contaminate downstream model training.

Act as a skeptical independent scientific data auditor. Read `README.md` first,
then inspect every TSV and use the paper DOI links and publicly available final
articles or supplements to test suspicious rows. Focus first on blank MIC rows,
sequence/name joins, assay ceilings, stereochemistry and terminal modifications,
papers where the represented sequence count differs from the reported active
count, and any result that may reflect immune activity rather than direct
antimicrobial activity.

Do not accept a row merely because another LLM extracted it. Do not label a row
false solely because the MIC is high or because a peptide has multiple rows.
Require source-level evidence for every claim. Distinguish confirmed false
positives, likely false positives, items needing manual verification, and
patterns that are not issues.

Do not modify the input TSVs. Put the complete audit in
`findings/INDEPENDENT_AUDIT.md`. For every proposed issue, give the sequence,
DOI, affected row or assay description, source location, evidence, severity and
recommended correction. End with a concise go/no-go recommendation for using
the dataset in model training.

