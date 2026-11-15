from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
products = [
    "Bread","Butter","Milk","Eggs","Cheese","Yogurt","Coffee","Tea",
    "Sugar","Cereal","Bananas","Apples","Chicken","Rice","Pasta",
    "Tomato Sauce","Chips","Salsa","Chocolate","Cookies","Orange Juice",
    "Mineral Water","Laundry Detergent","Dish Soap"
]
# Seed common combinations so the demo produces interpretable association rules.
patterns = [
    ["Bread","Butter","Milk"], ["Coffee","Milk","Sugar"],
    ["Chips","Salsa","Mineral Water"], ["Pasta","Tomato Sauce","Cheese"],
    ["Cereal","Milk","Bananas"], ["Tea","Cookies","Chocolate"],
    ["Chicken","Rice"], ["Eggs","Bread","Cheese"]
]
rows = []
for i in range(1, 2401):
    basket = set()
    if rng.random() < .72:
        basket.update(patterns[int(rng.integers(0, len(patterns)))])
    count = int(rng.integers(1, 5))
    basket.update(rng.choice(products, size=count, replace=False).tolist())
    # Small chance to add a popular staple
    if rng.random() < .25:
        basket.add(str(rng.choice(["Milk","Bread","Eggs","Coffee"])))
    for product in sorted(basket):
        rows.append({
            "transaction_id": f"MM{i:05d}",
            "product": product,
            "quantity": int(rng.integers(1, 4)),
            "transaction_date": (pd.Timestamp("2025-01-01") + pd.Timedelta(days=int(rng.integers(0,365)))).date().isoformat()
        })
out = Path(__file__).resolve().parents[1] / "data" / "transactions.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"Generated {len(rows)} line items across 2,400 synthetic transactions: {out}")
