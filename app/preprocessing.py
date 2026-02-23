import joblib
import pandas as pd
import scorecardpy as sc

bins = joblib.load("artifacts/woe_bins.pkl")
feature_columns = joblib.load("artifacts/feature_columns.pkl")


def transform_data(input_data):

    df = pd.DataFrame([input_data])

    # Apply WOE transformation
    df_woe = sc.woebin_ply(df, bins)

    # STRICT feature alignment
    missing = set(feature_columns) - set(df_woe.columns)
    if missing:
        raise ValueError(f"Missing required WOE features: {missing}")

    # Keep only trained features
    df_woe = df_woe[feature_columns]

    return df_woe
