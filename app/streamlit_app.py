from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import plotly.express as px
import streamlit as st
from marketmind.basket import load_transactions, to_basket_matrix
from marketmind.mining import mine_itemsets, build_rules, recommend_products
from marketmind.analytics import transaction_summary, product_popularity

st.set_page_config(page_title="MarketMind AI", page_icon="🛒", layout="wide")
st.title("🛒 MarketMind AI")
st.caption("Intelligent Market Basket Analysis and Product Recommendation Engine")
st.info("Demo mode: the bundled retail transactions are synthetic, not real customer purchases.")

path = Path(__file__).resolve().parents[1] / "data" / "transactions.csv"
df = load_transactions(path)
summary = transaction_summary(df)

with st.sidebar:
    st.header("Mining settings")
    min_support = st.slider("Minimum support", 0.01, 0.20, 0.025, 0.005)
    min_confidence = st.slider("Minimum confidence", 0.10, 0.90, 0.25, 0.05)
    max_len = st.slider("Maximum itemset size", 2, 5, 3)

with st.spinner("Mining frequent itemsets and association rules..."):
    itemsets = mine_itemsets(df, min_support=min_support, max_len=max_len)
    rules = build_rules(itemsets, min_confidence=min_confidence)

a,b,c,d = st.columns(4)
a.metric("Transactions", f"{summary['transactions']:,}")
b.metric("Unique products", summary["unique_products"])
c.metric("Line items", f"{summary['line_items']:,}")
d.metric("Average basket size", f"{summary['avg_basket_size']:.2f}")

left,right = st.columns(2)
with left:
    st.subheader("Most purchased products")
    popular = product_popularity(df)
    st.plotly_chart(px.bar(popular.sort_values("transactions"), x="transactions", y="product",
                           orientation="h"), use_container_width=True)
with right:
    st.subheader("Frequent itemsets")
    if not itemsets.empty:
        display = itemsets.copy()
        display["products"] = display["itemsets"].map(lambda x: ", ".join(sorted(x)))
        st.dataframe(display[["products","support","itemset_size"]].head(20),
                     use_container_width=True, hide_index=True)
    else:
        st.warning("No itemsets found. Try lowering minimum support.")

st.subheader("Association rules")
if not rules.empty:
    rule_view = rules.copy()
    rule_view["if_products"] = rule_view["antecedents"].map(lambda x: ", ".join(sorted(x)))
    rule_view["then_products"] = rule_view["consequents"].map(lambda x: ", ".join(sorted(x)))
    st.dataframe(rule_view[["if_products","then_products","support","confidence","lift"]].head(30),
                 use_container_width=True, hide_index=True)
    st.plotly_chart(px.scatter(rule_view.head(200), x="support", y="confidence", size="lift",
                               color="lift", hover_data=["if_products","then_products"],
                               title="Association rule strength"), use_container_width=True)
else:
    st.warning("No rules meet the selected thresholds. Lower minimum confidence or support.")

st.subheader("Product recommendation engine")
products = sorted(df.product.unique())
selected = st.multiselect("Choose products in a sample basket", products, default=["Coffee","Milk"])
if st.button("Generate recommendations"):
    recs = recommend_products(selected, rules, limit=10)
    if recs:
        st.dataframe(pd.DataFrame(recs), use_container_width=True, hide_index=True)
    else:
        st.info("No recommendations found for this basket under the current thresholds.")

st.subheader("Transaction data preview")
st.dataframe(df.head(30), use_container_width=True, hide_index=True)
st.download_button("Download transaction data (CSV)", df.to_csv(index=False).encode("utf-8"),
                   "marketmind_transactions.csv", "text/csv")
