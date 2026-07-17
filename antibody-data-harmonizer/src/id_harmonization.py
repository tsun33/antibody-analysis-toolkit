"""Utilities for standardizing columns and harmonizing antibody identifiers."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Iterable, Sequence

import pandas as pd


def to_snake_case(column_name: object) -> str:
    """Convert a column label into a simple snake_case name."""
    text = str(column_name).strip()
    text = re.sub(r"[\s/()%°-]+", "_", text)
    text = re.sub(r"[^0-9A-Za-z_]+", "", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_").lower()


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with standardized column names."""
    output = df.copy()
    output.columns = [to_snake_case(col) for col in output.columns]
    return output


def normalize_antibody_id(
    value: object,
    removable_suffixes: Sequence[str] = (),
) -> str | pd.NA:
    """
    Normalize an antibody ID for exact matching.

    Operations:
    1. Convert to uppercase.
    2. Remove spaces and punctuation.
    3. Optionally remove explicitly configured suffixes.

    Important: suffix removal is opt-in because aggressive rules can create
    false matches.
    """
    if pd.isna(value):
        return pd.NA

    normalized = re.sub(r"[^0-9A-Za-z]+", "", str(value).upper())

    suffixes = sorted(
        {re.sub(r"[^0-9A-Za-z]+", "", s.upper()) for s in removable_suffixes},
        key=len,
        reverse=True,
    )
    for suffix in suffixes:
        if suffix and normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)]
            break

    return normalized or pd.NA


def add_normalized_id(
    df: pd.DataFrame,
    source_column: str,
    output_column: str = "antibody_id",
    removable_suffixes: Sequence[str] = (),
) -> pd.DataFrame:
    """Return a copy containing a normalized antibody identifier column."""
    if source_column not in df.columns:
        raise KeyError(
            f"Column '{source_column}' was not found. "
            f"Available columns: {list(df.columns)}"
        )

    output = df.copy()
    output[output_column] = output[source_column].map(
        lambda value: normalize_antibody_id(value, removable_suffixes)
    )
    return output


def duplicate_id_report(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """Return all rows whose matching key is duplicated."""
    if key not in df.columns:
        raise KeyError(f"Column '{key}' was not found.")
    return df[df[key].notna() & df[key].duplicated(keep=False)].sort_values(key)


def safe_merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    key: str = "antibody_id",
    how: str = "outer",
    validate: str = "one_to_one",
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    """
    Merge two tables and return both the merged table and audit tables.

    The audit dictionary contains:
    - matched
    - left_only
    - right_only
    - left_duplicates
    - right_duplicates
    """
    for name, df in (("left", left), ("right", right)):
        if key not in df.columns:
            raise KeyError(f"The {name} table does not contain '{key}'.")

    left_duplicates = duplicate_id_report(left, key)
    right_duplicates = duplicate_id_report(right, key)

    if validate == "one_to_one" and (
        not left_duplicates.empty or not right_duplicates.empty
    ):
        raise ValueError(
            "A one-to-one merge is unsafe because duplicate IDs were found. "
            "Inspect duplicate_id_report() or choose the correct relationship."
        )

    merged = pd.merge(
        left,
        right,
        on=key,
        how=how,
        indicator=True,
        validate=validate,
        suffixes=("_assay", "_annotation"),
    )

    audits = {
        "matched": merged.loc[merged["_merge"] == "both"].copy(),
        "left_only": merged.loc[merged["_merge"] == "left_only"].copy(),
        "right_only": merged.loc[merged["_merge"] == "right_only"].copy(),
        "left_duplicates": left_duplicates,
        "right_duplicates": right_duplicates,
    }
    return merged, audits


def suggest_id_matches(
    unresolved_ids: Iterable[object],
    candidate_ids: Iterable[object],
    minimum_score: float = 0.75,
    max_candidates: int = 3,
) -> pd.DataFrame:
    """
    Suggest possible ID matches without changing the data.

    These are review candidates only. They should never be used to silently
    overwrite identifiers.
    """
    left_values = [str(v) for v in unresolved_ids if pd.notna(v)]
    right_values = [str(v) for v in candidate_ids if pd.notna(v)]

    rows: list[dict[str, object]] = []
    for left_id in left_values:
        scored = []
        for right_id in right_values:
            score = SequenceMatcher(None, left_id, right_id).ratio()
            if score >= minimum_score:
                scored.append((right_id, score))

        for rank, (right_id, score) in enumerate(
            sorted(scored, key=lambda item: item[1], reverse=True)[:max_candidates],
            start=1,
        ):
            rows.append(
                {
                    "unresolved_id": left_id,
                    "suggested_id": right_id,
                    "similarity_score": round(score, 3),
                    "candidate_rank": rank,
                }
            )

    return pd.DataFrame(rows)
