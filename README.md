# MarketMind AI
### Intelligent Market Basket Analysis and Product Recommendation Engine

MarketMind AI is an end-to-end retail analytics demo that discovers product associations in transaction data and turns those patterns into explainable cross-sell recommendations. It uses frequent itemset mining and association rules to help explore which products are commonly purchased together.

> **Data notice:** The included transactions are synthetic and generated for demonstration. They do not represent real customers, retailers, or purchasing behaviour. Recommendations are association-based signals, not causal claims or guaranteed sales uplift.

## Features
- Synthetic retail transaction generator
- Transaction preprocessing and basket construction
- Apriori frequent-itemset mining
- Association rule generation with support, confidence, and lift
- Basket-based product recommendations
- Streamlit dashboard with KPI cards, charts, filters, and CSV downloads
- FastAPI endpoints for rule discovery and recommendations
- Unit tests, methodology documentation, and exploratory notebook

## Quick Start

- Ensure Python 3.10 or later is installed.
- Create and activate a Python virtual environment.
- Install the required dependencies from `requirements.txt`.
- Generate the sample transaction dataset.
- Launch the interactive Streamlit dashboard.
- Explore customer purchasing patterns and market basket analytics.

## API Usage

- Start the FastAPI backend in a separate terminal.
- Access interactive API documentation at `http://127.0.0.1:8000/docs`.
- Submit product combinations to the `/recommend` POST endpoint.
- Analyze frequently purchased product combinations.
- Generate association-based product recommendations in JSON format.

**Example input parameters:**

- Customer basket containing purchased products.
- Product combinations for association analysis.
- Transaction patterns for identifying cross-selling opportunities.

## Project structure

```text
MarketMindAI/
├── api/                 # FastAPI service
├── app/                 # Streamlit dashboard
├── data/                # Synthetic transaction dataset
├── docs/                # Methodology, API, responsible-use notes
├── marketmind/          # Basket mining and recommendation modules
├── notebooks/           # Exploratory analysis notebook
├── scripts/             # Data generation
├── tests/               # Unit tests
├── requirements.txt
└── README.md
```

## How it works
1. Convert line-item transactions into one-hot encoded baskets.
2. Use Apriori to identify frequent product combinations.
3. Generate association rules using support, confidence, and lift.
4. Match a customer's current basket against rule antecedents.
5. Rank unseen consequent products by confidence and lift.

### Metric definitions
- **Support:** Fraction of transactions containing the itemset.
- **Confidence:** Fraction of transactions containing the antecedent that also contain the consequent.
- **Lift:** Confidence divided by the consequent's overall support. Lift above 1 indicates a positive association in the observed data.

## Limitations
- Synthetic data is provided; replace it only with properly authorized and privacy-protected transaction data.
- Association does not imply causation.
- Rules can be affected by seasonality, promotions, stock availability, and product popularity.
- Recommendation quality should be evaluated with offline ranking metrics and controlled experiments before business use.

## Author

**Mohamed Riyaz S.**  
Integrated M.Tech, Computer Science and Engineering (Business Analytics)  
VIT Chennai
