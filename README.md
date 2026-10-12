<div align="center">

# 📈 Automated DCF with Machine Learning

**Forecast the drivers of a DCF with regularized ML — then value the company with plain corporate finance.**

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="26">
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" height="26">
<img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" height="26">
<img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" height="26">
<img src="https://img.shields.io/badge/SEC%20XBRL-1F2937?style=for-the-badge" height="26">

[Overview](#-overview) · [Features](#-key-features) · [Architecture](#%EF%B8%8F-architecture) · [Getting Started](#-getting-started) · [Structure](#%EF%B8%8F-project-structure) · [Notes](#-notes--limitations)

</div>

---

## 📌 Overview

**Can machine learning automate parts of a DCF?**

Instead of predicting a stock price directly, this pipeline forecasts the **operating fundamentals** a DCF depends on — growth, margins, tax, D&A, CapEx and working capital — and passes them through a standard **FCFF → DCF → fair value** framework. The ML layer stays separate from the valuation layer, so every number remains explainable in corporate-finance terms.

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔮 **Six forecast targets** | Revenue growth, EBIT margin, effective tax rate, D&A / revenue, CapEx / revenue, NWC / revenue |
| 🧠 **Regularized models** | Ridge and Elastic Net — interpretable, robust to correlated accounting variables and small samples |
| ⏳ **Leak-free backtest** | Strict chronological split (train ≤ 2018 · gap 2019–2021 · test ≥ 2022), features at *t* predict results at *t + 1* |
| 📊 **Rich diagnostics** | R², Pearson r, Spearman ρ, direction accuracy, MAE, RMSE and a composite Correlation Accuracy Index |
| 🏛️ **SEC data collector** | Pulls historical fundamentals from the SEC Company Facts (XBRL) API |
| 🧪 **Synthetic demo panel** | Runs the full pipeline end-to-end without any external data |

## 🏗️ Architecture

```text
Financial / market / macro data
        │
        ▼
Cleaning  ─ missing values · outliers · point-in-time alignment
        │
        ▼
Feature engineering  ─ ratios · growth · market variables
        │
        ▼
Ridge / Elastic Net  ─ six driver forecasts
        │
        ▼
FCFF = NOPAT + D&A − CapEx − ΔNWC
        │
        ▼
DCF  →  enterprise value  →  equity value  →  fair value per share
```

| Forecast target | Role in the DCF |
|---|---|
| 📈 Revenue growth | Top-line forecast |
| 💰 EBIT margin | Operating profitability |
| 🧾 Effective tax rate | After-tax operating profit (NOPAT) |
| 🏭 D&A / revenue | Non-cash add-back |
| 🏗️ CapEx / revenue | Reinvestment requirement |
| 💼 NWC / revenue | Working-capital investment |

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Modeling | scikit-learn (Ridge, Elastic Net), SciPy |
| Data | pandas, NumPy, SEC Company Facts API (`requests`) |
| Evaluation | custom metrics module (`metrics.py`) |

## 🚀 Getting Started

```bash
pip install -r requirements.txt

# 1) run the end-to-end backtest on the synthetic demo panel
python run_backtest.py --data demo_panel.csv            # --train-end 2018 --test-start 2022

# 2) collect real fundamentals from the SEC
export SEC_USER_AGENT="Your Name your@email.com"       # PowerShell: $env:SEC_USER_AGENT="..."
python collect_sec.py --tickers AAPL MSFT GOOGL META AMZN NVDA --start-year 2010
```

The backtest writes `backtest_metrics.csv`, `backtest_predictions.csv` and `backtest_summary.csv`.

## 🗂️ Project Structure

```text
Automated-DCF-ML
├── run_backtest.py        # CLI: chronological backtest
├── backtest.py            # train / test split and evaluation loop
├── models.py              # Ridge and Elastic Net pipelines
├── features.py            # feature engineering
├── dcf.py                 # FCFF and DCF valuation
├── metrics.py             # R², correlations, direction accuracy, errors, composite index
├── collect_sec.py         # CLI: SEC Company Facts collection
├── sec_collector.py       # SEC API client
├── demo_panel.csv         # synthetic demo dataset
├── backtest_*.csv         # sample backtest outputs (demo data)
├── METRICS_GUIDE.md       # how to read each metric
└── requirements.txt
```

## 📝 Notes & Limitations

- **Demo data is synthetic.** Results on `demo_panel.csv` only show the pipeline works; they are **not** real-world investment performance.
- **Point-in-time matters.** Production data should be aligned to the **filing date**, not the fiscal period end, to avoid look-ahead bias.
- **SEC data alone is not enough** — market data (returns, beta, volatility), macro data (rates, inflation, GDP) and sector metadata are needed for the full model.
- **Correlation Accuracy Index** (35% Pearson · 25% Spearman · 25% direction · 15% clipped R²) is a project-specific diagnostic, not a standard academic metric.
- **Financial companies** (banks, insurers) need a separate framework; corporate FCFF does not apply directly.

See [`METRICS_GUIDE.md`](METRICS_GUIDE.md) for detailed metric definitions.

---

<div align="center"><sub>Built by <a href="https://github.com/HyeonbinJung">Hyeonbin Jung</a></sub></div>
