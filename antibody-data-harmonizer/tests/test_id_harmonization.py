import pandas as pd

from src.id_harmonization import (
    add_normalized_id,
    normalize_antibody_id,
    safe_merge,
)


def test_normalize_antibody_id():
    assert normalize_antibody_id(" ab-001 ") == "AB001"
    assert normalize_antibody_id("AB003-HC", removable_suffixes=("HC",)) == "AB003"


def test_safe_merge_audit():
    left = pd.DataFrame({"antibody_id": ["AB001", "AB002"], "value": [1, 2]})
    right = pd.DataFrame({"antibody_id": ["AB001", "AB003"], "note": ["x", "y"]})

    merged, audit = safe_merge(left, right)

    assert len(audit["matched"]) == 1
    assert len(audit["left_only"]) == 1
    assert len(audit["right_only"]) == 1
    assert set(merged["_merge"].astype(str)) == {"both", "left_only", "right_only"}


def test_add_normalized_id():
    df = pd.DataFrame({"raw": ["AB-001", "AB 002"]})
    result = add_normalized_id(df, "raw")
    assert result["antibody_id"].tolist() == ["AB001", "AB002"]
