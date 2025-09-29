import pandas as pd
import numpy as np

def print_df(df: pd.DataFrame, max_rows: int = 10):
    with pd.option_context("display.max_rows", max_rows, "display.max_columns", None):
        print(df)


def season_of(dt) -> str:
    m = getattr(dt, "month", pd.Timestamp(dt).month)
    if m in (12, 1, 2):
        return "winter"
    if m in (3, 4, 5):
        return "spring"
    if m in (6, 7, 8):
        return "summer"
    return "autumn"

def convert_numpy(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    return obj

def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean(v) for v in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    return obj
