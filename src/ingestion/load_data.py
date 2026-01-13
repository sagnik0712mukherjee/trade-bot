# src/ingestion/load_data.py

import pandas as pd
from pathlib import Path


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"CSV file is empty: {path}")

    df = pd.read_csv(path)

    if df.empty or len(df.columns) == 0:
        raise ValueError(f"CSV has no columns or rows: {path}")

    return df


def load_all_data(holdings_path: Path, trades_path: Path) -> pd.DataFrame:
    holdings_df = load_csv(holdings_path)
    trades_df = load_csv(trades_path)

    # Perform outer merge to combine information where possible
    # We merge on SecurityId and PortfolioName as they are likely the common links
    merged_df = pd.merge(
        holdings_df, 
        trades_df, 
        on=["SecurityId", "PortfolioName"], 
        how="outer", 
        suffixes=("_h", "_t")
    )

    # Fill source column to identify where the data came from
    merged_df["source"] = "merged"
    
    return merged_df
