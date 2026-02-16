import pandas as pd
from app.config import woe

def transform_data(df: pd.DataFrame):
    return woe.transform(df)
