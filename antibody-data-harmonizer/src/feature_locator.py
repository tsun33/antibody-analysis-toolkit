"""Utilities for locating and marking sequence features."""

from __future__ import annotations

import re

import pandas as pd


def clean_protein_sequence(value: object) -> str:
    """Remove whitespace/non-letters and convert a protein sequence to uppercase."""
    if pd.isna(value):
        return ""
    return re.sub(r"[^A-Za-z]", "", str(value)).upper()


def locate_sequence_feature(
    df: pd.DataFrame,
    id_column: str,
    sequence_column: str,
    feature: str,
    *,
    feature_name: str = "feature",
    regex: bool = False,
) -> pd.DataFrame:
    """
    Locate a literal motif or regular-expression feature in every sequence.

    Output includes:
    - feature_present
    - feature_count
    - start_positions_1based
    - matched_features
    - marked_sequence

    Matches are non-overlapping. The source dataframe is not modified.
    """
    required = {id_column, sequence_column}
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    if not feature:
        raise ValueError("feature must not be empty.")

    pattern = re.compile(feature if regex else re.escape(feature), flags=re.IGNORECASE)
    rows: list[dict[str, object]] = []

    for _, row in df.iterrows():
        sequence = clean_protein_sequence(row[sequence_column])
        matches = list(pattern.finditer(sequence))

        positions = [match.start() + 1 for match in matches]
        matched_text = [match.group(0) for match in matches]
        marked_sequence = pattern.sub(lambda match: f"[{match.group(0)}]", sequence)

        rows.append(
            {
                id_column: row[id_column],
                "feature_name": feature_name,
                "query_pattern": feature,
                "feature_present": bool(matches),
                "feature_count": len(matches),
                "start_positions_1based": ";".join(map(str, positions)),
                "matched_features": ";".join(matched_text),
                "marked_sequence": marked_sequence,
            }
        )

    return pd.DataFrame(rows)
