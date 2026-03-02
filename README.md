#  Marketing A/B Test Analyzer

** Live Demo:** https://marketing-ab-test-analyzer.streamlit.app

## Business Problem
A marketing company ran an A/B test to measure whether showing 
real ads converts more users than Public Service Announcements.
Analyzed 588,000+ user sessions to deliver a data-backed 
ad spend recommendation.

## Key Findings
- PSA conversion rate: 1.79%
- Ad conversion rate: 2.55%
- Relative lift: **43.1% higher conversion with ads**
- P-value: ~0.000000 → statistically significant
- Statistical power: 1.000 — results are highly reliable
- Best performing day: **Monday (3.28% conversion)**
- Business impact: **$384,625 additional monthly revenue**

## Recommendation
Ads significantly outperform PSA content. Continue ad spend.
Focus campaigns on Monday–Tuesday for maximum ROI.

## Project Structure
```
ab-test-analyzer/
├── cleaning.py           # data cleaning & validation
├── eda.py                # exploratory data analysis
├── hypothesis_test.py    # statistical testing
├── charts.py             # advanced visualizations
├── app/
│   └── streamlit_app.py  # live dashboard
├── data/
│   └── marketing_clean.csv
└── reports/
    ├── eda_charts.png
    ├── ads_frequency_curve.png
    └── hour_heatmap.png
```

## Tech Stack
Python · Pandas · SciPy · Statsmodels · Streamlit · Plotly · Seaborn

## How to Run Locally
pip install -r requirements.txt
streamlit run app/streamlit_app.py
