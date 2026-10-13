import pandas as pd


def load_and_save(df):
    raw = pd.read_csv("data/01_raw/x.csv")  # bad
    df.to_parquet("data/02_intermediate/x.parquet")
    return raw
