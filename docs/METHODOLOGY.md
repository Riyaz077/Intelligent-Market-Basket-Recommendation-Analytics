# Methodology

1. Load line-item transactions with transaction identifiers and product names.
2. Pivot the data into a transaction-by-product Boolean matrix.
3. Apply Apriori to find frequent itemsets above the configured minimum support.
4. Generate association rules above the minimum confidence threshold.
5. Rank recommendations for a supplied basket using lift, confidence, and support.
6. Visualize product popularity, frequent itemsets, association rules, and recommendations.

## Metrics
- Support measures the fraction of transactions containing an itemset.
- Confidence estimates the conditional frequency of the consequent given the antecedent.
- Lift compares rule confidence with the consequent's baseline support.

These metrics describe association in the observed dataset and do not establish causation.
