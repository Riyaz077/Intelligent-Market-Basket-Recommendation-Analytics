from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from marketmind.basket import load_transactions
from marketmind.mining import mine_itemsets, build_rules, recommend_products
from marketmind.analytics import transaction_summary

ROOT = Path(__file__).resolve().parents[1]
DATA = load_transactions(ROOT / "data" / "transactions.csv")
ITEMSETS = mine_itemsets(DATA, min_support=0.025, max_len=3)
RULES = build_rules(ITEMSETS, min_confidence=0.25)

app = FastAPI(title="MarketMind AI API", version="1.0.0",
              description="Synthetic retail market-basket analytics demo.")

class BasketRequest(BaseModel):
    basket: list[str] = Field(min_length=1, max_length=30)
    limit: int = Field(default=5, ge=1, le=20)

@app.get("/health")
def health():
    return {"status":"ok", "mode":"synthetic_demo"}

@app.get("/summary")
def summary():
    return transaction_summary(DATA)

@app.get("/rules")
def rules(limit: int = 20):
    view = RULES.head(max(1, min(limit, 100))).copy()
    if view.empty:
        return []
    return [{
        "antecedents": sorted(list(row.antecedents)),
        "consequents": sorted(list(row.consequents)),
        "support": float(row.support),
        "confidence": float(row.confidence),
        "lift": float(row.lift)
    } for row in view.itertuples()]

@app.post("/recommend")
def recommend(request: BasketRequest):
    try:
        return {"basket": request.basket,
                "recommendations": recommend_products(request.basket, RULES, request.limit),
                "notice": "Association-based demo recommendations from synthetic transactions."}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
