
import pandas as pd
from itertools import combinations
from .basket import to_basket_matrix

def mine_itemsets(transactions: pd.DataFrame, min_support=0.02, max_len=3):
    matrix = to_basket_matrix(transactions)
    n = len(matrix)
    if n == 0:
        return pd.DataFrame(columns=["support", "itemsets", "itemset_size"])
    baskets = [set(matrix.columns[matrix.iloc[i].to_numpy()]) for i in range(n)]
    counts = {}
    current = [(frozenset([item]), sum(item in b for b in baskets)) for item in matrix.columns]
    current = [(s,c) for s,c in current if c/n >= min_support]
    for size in range(1, max_len + 1):
        if not current:
            break
        for itemset, count in current:
            counts[itemset] = count
        if size == max_len:
            break
        prev_sets = [s for s,_ in current]
        candidates = set()
        for a, b in combinations(prev_sets, 2):
            union = a | b
            if len(union) == size + 1 and all(frozenset(sub) in prev_sets for sub in combinations(union, size)):
                candidates.add(union)
        current = []
        for candidate in candidates:
            count = sum(candidate.issubset(b) for b in baskets)
            if count/n >= min_support:
                current.append((candidate, count))
    rows = [{"support": count/n, "itemsets": itemset, "itemset_size": len(itemset)}
            for itemset, count in counts.items()]
    if not rows:
        return pd.DataFrame(columns=["support", "itemsets", "itemset_size"])
    return pd.DataFrame(rows).sort_values(["support","itemset_size"], ascending=[False,True]).reset_index(drop=True)

def build_rules(itemsets: pd.DataFrame, min_confidence=0.2):
    columns = ["antecedents","consequents","support","confidence","lift"]
    if itemsets.empty:
        return pd.DataFrame(columns=columns)
    support_map = {frozenset(row.itemsets): float(row.support) for row in itemsets.itertuples()}
    rows = []
    for itemset, item_support in support_map.items():
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent_tuple in combinations(itemset, size):
                antecedent = frozenset(antecedent_tuple)
                consequent = itemset - antecedent
                ant_support = support_map.get(antecedent)
                con_support = support_map.get(consequent)
                if not ant_support or not con_support:
                    continue
                confidence = item_support / ant_support
                lift = confidence / con_support
                if confidence >= min_confidence:
                    rows.append({"antecedents":antecedent,"consequents":consequent,
                                 "support":item_support,"confidence":confidence,"lift":lift})
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows).sort_values(["lift","confidence","support"], ascending=False).reset_index(drop=True)

def recommend_products(basket, rules, limit=5):
    basket = {str(x) for x in basket}
    scores = {}
    if rules.empty:
        return []
    for _, row in rules.iterrows():
        antecedents = set(row["antecedents"])
        consequents = set(row["consequents"])
        if antecedents and antecedents.issubset(basket):
            for product in consequents - basket:
                candidate = {"confidence":float(row["confidence"]),
                             "lift":float(row["lift"]),
                             "support":float(row["support"])}
                current = scores.get(product, {"confidence":0.0,"lift":0.0,"support":0.0})
                if (candidate["lift"],candidate["confidence"]) > (current["lift"],current["confidence"]):
                    scores[product] = candidate
    ranked = sorted(scores.items(), key=lambda x:(x[1]["lift"],x[1]["confidence"]), reverse=True)
    return [{"product":p,**m} for p,m in ranked[:limit]]
