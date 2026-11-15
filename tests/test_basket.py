import pandas as pd
from marketmind.basket import to_basket_matrix
from marketmind.mining import mine_itemsets, build_rules, recommend_products

def sample_data():
    rows = []
    baskets = {
        "1":["Bread","Butter","Milk"],
        "2":["Bread","Butter"],
        "3":["Bread","Milk"],
        "4":["Coffee","Milk"],
        "5":["Bread","Butter","Milk"]
    }
    for tid, products in baskets.items():
        for product in products:
            rows.append({"transaction_id":tid,"product":product})
    return pd.DataFrame(rows)

def test_basket_matrix_shape():
    matrix = to_basket_matrix(sample_data())
    assert matrix.shape == (5,4)

def test_mining_returns_itemsets_and_rules():
    data = sample_data()
    itemsets = mine_itemsets(data, min_support=.2, max_len=3)
    assert not itemsets.empty
    rules = build_rules(itemsets, min_confidence=.2)
    assert isinstance(rules, pd.DataFrame)

def test_recommendation_excludes_existing_basket_items():
    data = sample_data()
    itemsets = mine_itemsets(data, min_support=.2, max_len=3)
    rules = build_rules(itemsets, min_confidence=.2)
    recs = recommend_products(["Bread"], rules)
    assert all(r["product"] != "Bread" for r in recs)
