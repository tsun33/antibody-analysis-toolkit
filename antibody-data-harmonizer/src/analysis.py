"""Statistical summaries for antibody developability variables."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
from scipy.stats import pearsonr, spearmanr


def add_sequence_length(
    df: pd.DataFrame,
    sequence_column: str,
    output_column: str = "sequence_length",
) -> pd.DataFrame:
    """Add a length column after removing non-letter characters."""
    if sequence_column not in df.columns:
        raise KeyError(f"Column '{sequence_column}' was not found.")

    output = df.copy()
    cleaned = (
        output[sequence_column]
        .fillna("")
        .astype(str)
        .str.replace(r"[^A-Za-z]", "", regex=True)
    )
    output[output_column] = cleaned.str.len()
    return output


def correlation_table(
    df: pd.DataFrame,
    predictor: str,
    outcomes: Iterable[str],
    methods: Iterable[str] = ("spearman", "pearson"),
    minimum_n: int = 3,
) -> pd.DataFrame:
    """Calculate pairwise correlations with sample size and p-value."""
    supported = {"spearman", "pearson"}
    rows: list[dict[str, object]] = []

    if predictor not in df.columns:
        raise KeyError(f"Predictor '{predictor}' was not found.")

    for outcome in outcomes:
        if outcome not in df.columns:
            raise KeyError(f"Outcome '{outcome}' was not found.")

        pair = df[[predictor, outcome]].apply(pd.to_numeric, errors="coerce").dropna()
        n = len(pair)

        for method in methods:
            method_lower = method.lower()
            if method_lower not in supported:
                raise ValueError(f"Unsupported method: {method}")

            result = {
                "predictor": predictor,
                "outcome": outcome,
                "method": method_lower,
                "n": n,
                "correlation": pd.NA,
                "p_value": pd.NA,
                "status": "ok",
            }

            if n < minimum_n:
                result["status"] = f"insufficient_n<{minimum_n}"
            elif pair[predictor].nunique() < 2 or pair[outcome].nunique() < 2:
                result["status"] = "constant_variable"
            else:
                if method_lower == "spearman":
                    statistic, p_value = spearmanr(pair[predictor], pair[outcome])
                else:
                    statistic, p_value = pearsonr(pair[predictor], pair[outcome])

                result["correlation"] = round(float(statistic), 4)
                result["p_value"] = round(float(p_value), 6)

            rows.append(result)

    return pd.DataFrame(rows)
