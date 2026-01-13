from typing import List, Dict
import pandas as pd


def row_to_text(row: pd.Series) -> str:
    h_lines = []
    t_lines = []
    other_lines = []
    
    for col, val in row.items():
        if pd.isna(val):
            continue
        
        line = f"{col}: {val}"
        if col.endswith("_h") or col in ["PortfolioName", "SecurityId", "ShortName", "AsOfDate", "OpenDate", "SecName"]:
            h_lines.append(line)
        elif col.endswith("_t") or col in ["TradeDate", "SettleDate", "Quantity", "Price_t", "Principal", "TotalCash", "AllocationQTY"]:
            t_lines.append(line)
        else:
            other_lines.append(line)
            
    text = "--- HOLDING DATA ---\n" + "\n".join(h_lines)
    if t_lines:
        text += "\n\n--- TRADE DATA ---\n" + "\n".join(t_lines)
    if other_lines:
        text += "\n\n--- OTHER INFO ---\n" + "\n".join(other_lines)
        
    return text


def build_documents(df: pd.DataFrame) -> List[Dict]:
    """
    Returns:
    [
        {
            "text": "...",
            "metadata": {
                "source": "holdings",
                "row_id": 12
            }
        }
    ]
    """
    documents = []

    for idx, row in df.iterrows():
        text = row_to_text(row)
        documents.append(
            {
                "text": text,
                "metadata": {
                    "source": row.get("source"),
                    "row_id": idx
                }
            }
        )

    return documents
