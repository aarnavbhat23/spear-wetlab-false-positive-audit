#!/usr/bin/env python3
"""Run deterministic structural checks; this does not replace source review."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
AA = set("ACDEFGHIKLMNPQRSTVWY")
EXPECTED = ["sequence", "wetlab_experiment", "mic", "paper_title", "paper_doi"]


def read_tsv(name):
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return reader.fieldnames, list(reader)


header, rows = read_tsv("df_wetlab_validated.tsv")
round1_header, round1 = read_tsv("df_cesar_wetlab_round1.tsv")
_, murine = read_tsv("df_cesar_murine_validated.tsv")

assert header == EXPECTED, (header, EXPECTED)
assert not any(set(row["sequence"]) - AA for row in rows)
assert not any(not 8 <= len(row["sequence"]) <= 50 for row in rows)
assert len({tuple(row[column] for column in EXPECTED) for row in rows}) == len(rows)

primary_dois = {
    row["paper_doi"].lower()
    for row in round1
    if row["article_category"] == "primary_research"
}
observed_dois = {row["paper_doi"].lower() for row in rows}
assert observed_dois == primary_dois
assert not any(row["sequence_status"] == "unresolved" for row in murine)

sequences = {row["sequence"] for row in rows}
per_sequence = Counter(row["sequence"] for row in rows)
print(f"rows={len(rows)}")
print(f"unique_sequences={len(sequences)}")
print(f"primary_papers={len(observed_dois)}")
print(f"rows_with_mic={sum(bool(row['mic']) for row in rows)}")
print(f"rows_without_mic={sum(not row['mic'] for row in rows)}")
print(f"maximum_rows_for_one_sequence={max(per_sequence.values())}")
print("structural_checks=PASS")

