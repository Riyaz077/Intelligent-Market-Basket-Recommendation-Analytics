import pandas as pd

def transaction_summary(df):
    if df.empty:
        return {"transactions": 0, "unique_products": 0, "line_items": 0, "avg_basket_size": 0.0}
    sizes = df.groupby("transaction_id")["product"].nunique()
    return {
        "transactions": int(df["transaction_id"].nunique()),
        "unique_products": int(df["product"].nunique()),
        "line_items": int(len(df)),
        "avg_basket_size": float(sizes.mean())
    }

def product_popularity(df, limit=15):
    return (df.groupby("product")["transaction_id"].nunique()
              .sort_values(ascending=False).head(limit)
              .rename("transactions").reset_index())
