import pandas as pd

from src.feature_locator import locate_sequence_feature


def test_locate_literal_feature():
    df = pd.DataFrame(
        {"antibody_id": ["AB001"], "sequence": ["AAAWGQGTTTWGQG"]}
    )
    result = locate_sequence_feature(
        df,
        id_column="antibody_id",
        sequence_column="sequence",
        feature="WGQG",
        feature_name="FR4 motif",
    )

    assert result.loc[0, "feature_present"]
    assert result.loc[0, "feature_count"] == 2
    assert result.loc[0, "start_positions_1based"] == "4;11"
    assert result.loc[0, "marked_sequence"] == "AAA[WGQG]TTT[WGQG]"
