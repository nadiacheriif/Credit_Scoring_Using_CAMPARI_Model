import pandas as pd
import scorecardpy as sc
from app.config import bins, feature_columns


def transform_data(input_dict: dict) -> pd.DataFrame:

    df = pd.DataFrame([input_dict])

    # Apply WoE transformation
    df_woe = sc.woebin_ply(df, bins)

    # Ensure required columns exist
    missing_cols = set(feature_columns) - set(df_woe.columns)
    if missing_cols:
        raise ValueError(
            f"Missing required features after WOE transformation: {missing_cols}"
        )

    # Keep exact training order
    df_woe = df_woe[feature_columns]

    return df_woe
