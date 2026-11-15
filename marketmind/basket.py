from pathlib import Path
import pandas as pd

REQUIRED = {"transaction_id", "product"}

def load_transactions(path="data/transactions.csv"):
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df = df.dropna(subset=["transaction_id", "product"]).copy()
    df["transaction_id"] = df["transaction_id"].astype(str)
    df["product"] = df["product"].astype(str).str.strip()
    df = df[df["product"] != ""]
    return df

def to_basket_matrix(df):
    if df.empty:
        raise ValueError("Transaction data is empty")
    return (df.assign(present=1)
              .pivot_table(index="transaction_id", columns="product",
                           values="present", aggfunc="max", fill_value=0)
              .astype(bool))
