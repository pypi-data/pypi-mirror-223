import numpy as np
import pandas as pd

def rescale(df):
    """Assumes that data contains integer values in ascending order of latent trait.
    Transforms data such that each item response contains all values from 0 to max."""
    rescaled_df = pd.DataFrame()
    for column in df.columns:
        ranks = df[column].rank(method="dense").astype(int) - 1
        rescaled_df[column] = ranks
    return rescaled_df

def remove_single_value_columns(df):
    columns_to_drop = []
    for column in df.columns:
        if df[column].nunique() == 1:
            columns_to_drop.append(column)
    df.drop(columns=columns_to_drop, inplace=True)
    return df
