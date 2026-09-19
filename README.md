# 📈 ML DCF Forecasting MVP

### Machine Learning for Fundamental Valuation

> 🤖 **Can machine learning automate parts of a DCF?**

**ML DCF Forecasting** is an experimental valuation pipeline that uses historical **financial, market, and macroeconomic data** to forecast key operating variables required for a Discounted Cash Flow model.

Instead of predicting a stock price directly, the system forecasts the company's future financial fundamentals first.

Those forecasts are then passed through a traditional **FCFF → DCF → Fair Value** framework.

---

# 🎯 Project Goal

Traditional DCF models depend heavily on manually selected assumptions such as:

* Revenue growth
* Operating margins
* Capital expenditure
* Working capital
* Depreciation
* Tax rates

This project explores whether historical data and regularized machine-learning models can help estimate those assumptions systematically.

The core idea is:

```text
Historical Data
      ↓
Machine Learning
      ↓
Financial Forecast
      ↓
FCFF
      ↓
DCF
      ↓
Estimated Fair Value
```

> ⚠️ The model does **not** predict the target price directly.

It predicts future financial variables first and then calculates valuation using standard corporate finance relationships.

---

# 🏗️ Architecture

```text
        ┌─────────────────────┐
        │   Data Collection   │
        │ Financial / Market  │
        │       / Macro       │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │    Data Cleaning    │
        │ Missing / Outliers  │
        │  PIT Alignment      │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Feature Engineering │
        │ Ratios / Growth /   │
        │ Market Variables    │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  Ridge / ElasticNet │
        │ Financial Forecast  │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Forecasted Financial│
        │      Variables      │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │        FCFF         │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │         DCF         │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │     Fair Value      │
        └─────────────────────┘
```

---

# 🔮 Forecast Targets

The MVP currently focuses on six core DCF variables.

| Variable                  | Description                           | Role in DCF                   |
| ------------------------- | ------------------------------------- | ----------------------------- |
| 📈 **Revenue Growth**     | YoY revenue growth                    | Top-line forecast             |
| 💰 **EBIT Margin**        | EBIT / Revenue                        | Operating profitability       |
| 🧾 **Effective Tax Rate** | Taxes / Pretax Income                 | After-tax operating profit    |
| 🏭 **D&A / Revenue**      | Depreciation & Amortization intensity | Non-cash operating adjustment |
| 🏗️ **CapEx / Revenue**   | Capital expenditure intensity         | Reinvestment requirement      |
| 💼 **NWC / Revenue**      | Net working capital intensity         | Working-capital investment    |

These variables can be transformed into projected free cash flow through standard accounting relationships.

---

# 💵 From ML Forecasts to FCFF

The ML layer is deliberately separated from the valuation layer.

```text
ML Predictions
      │
      ├── Revenue Growth
      ├── EBIT Margin
      ├── Effective Tax Rate
      ├── D&A / Revenue
      ├── CapEx / Revenue
      └── NWC / Revenue
               │
               ▼
      Financial Statements
               │
               ▼
              FCFF
               │
               ▼
              DCF
               │
               ▼
          Fair Value
```

Conceptually:

```text
FCFF
=
NOPAT
+ D&A
- CapEx
- ΔNWC
```

The model therefore remains interpretable from a traditional corporate-finance perspective.

---

# 🧠 Why Ridge & Elastic Net?

Financial datasets often contain:

* Highly correlated accounting variables
* Relatively small historical samples
* Noisy macroeconomic features
* Structural differences between companies
* Large numbers of potentially redundant predictors

Regularized linear models provide a useful starting point because they are:

✅ Relatively interpretable
✅ Resistant to multicollinearity
✅ Less prone to overfitting than unrestricted linear models
✅ Easy to inspect and backtest
✅ Suitable as a baseline before introducing more complex models

The MVP currently uses:

```text
Ridge Regression
Elastic Net
```

More sophisticated models can later be compared against these baselines.

---

# ⏳ Backtest Methodology

Financial forecasting is a **time-series prediction problem**.

For that reason, this project avoids random train/test shuffling.

## Strict Time Split

```text
Timeline
────────────────────────────────────────────────────────▶

       TRAIN                GAP / VALIDATION        TEST
   ≤ 2018                     2019–2021             ≥ 2022

██████████████████       ░░░░░░░░░░░░░░       ███████████
```

Current MVP configuration:

| Period        | Purpose                 |
| ------------- | ----------------------- |
| **≤ 2018**    | Training                |
| **2019–2021** | Gap / validation period |
| **≥ 2022**    | Out-of-sample testing   |

Each observation follows:

```text
Features at Year t
        ↓
Predict
        ↓
Financial Result at Year t + 1
```

### 🚫 No Random Shuffle Split

Random splitting can allow information from later periods to influence models trained on earlier periods.

For financial forecasting, this can produce unrealistically strong backtest results.

The project therefore prioritizes:

* Chronological splits
* Rolling backtests
* Point-in-time data
* Out-of-sample evaluation

---

# 📊 Evaluation Metrics

Each target is evaluated using several complementary metrics.

| Metric                         | Purpose                          |
| ------------------------------ | -------------------------------- |
| **R²**                         | Explained variance               |
| **Pearson r**                  | Linear correlation               |
| **Spearman ρ**                 | Rank correlation                 |
| **Direction Accuracy**         | Correct direction of change      |
| **MAE**                        | Average absolute forecast error  |
| **RMSE**                       | Penalizes larger forecast errors |
| **Correlation Accuracy Index** | Internal composite metric        |

---

# 🧮 Correlation Accuracy Index

The project includes an experimental composite metric:

```text
Correlation Accuracy Index

= 35% × Normalized Pearson
+ 25% × Normalized Spearman
+ 25% × Direction Accuracy
+ 15% × Clipped R²
```

### ⚠️ Important

**Correlation Accuracy Index is a project-specific metric.**

It is **not** a standard statistical or academic performance measure.

Its purpose is to provide a simple combined diagnostic across:

* Linear correlation
* Rank correlation
* Directional correctness
* Explained variance

Individual statistical metrics should still be examined separately.

---

# 🧪 Demo Dataset

The repository includes:

```text
demo_panel.csv
```

This dataset is **synthetic** and exists only to test whether the forecasting pipeline works end-to-end.

It can be used to validate:

```text
Data Loading
      ↓
Feature Processing
      ↓
Model Training
      ↓
Prediction
      ↓
Metric Calculation
      ↓
Backtest Output
```

> 🚨 **Do not interpret performance on `demo_panel.csv` as real-world investment performance.**

Synthetic data can produce relationships that are substantially cleaner than real financial markets.

---

# 🚀 Getting Started

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2️⃣ Run the Demo Backtest

```bash
python run_backtest.py --data demo_panel.csv
```

The script trains the forecasting pipeline using the predefined chronological split and evaluates predictions on the test period.

---

# 🏛️ Real SEC Data Collection

A basic collector using the **SEC Company Facts API** is included.

Example:

```bash
python collect_sec.py \
    --tickers AAPL MSFT GOOGL META AMZN NVDA COST HD UNH CAT \
    --start-year 2010
```

---

# 🔐 SEC User-Agent Setup

The SEC requires requests to include an appropriate User-Agent.

Set it before running the collector.

### macOS / Linux

```bash
export SEC_USER_AGENT="Your Name your@email.com"
```

### Windows PowerShell

```powershell
$env:SEC_USER_AGENT="Your Name your@email.com"
```

Then run:

```bash
python collect_sec.py --tickers AAPL MSFT GOOGL META AMZN NVDA --start-year 2010
```

---

# 🌎 Data Sources

SEC filings provide a strong foundation for historical financial data, but **SEC data alone is not sufficient for the full model**.

Additional datasets are required for variables such as:

### 📑 Financial Data

```text
Revenue
EBIT
Taxes
D&A
CapEx
Working Capital
Balance Sheet Variables
```

### 📈 Market Data

```text
Stock Returns
Market Returns
Volatility
Beta
Valuation Multiples
```

### 🌐 Macro Data

```text
Interest Rates
Inflation
GDP Growth
Credit Conditions
Market Regime Variables
```

### 🏢 Company Metadata

```text
Sector
Industry
Company Classification
```

A production version should combine these sources into a **point-in-time panel dataset**.

---

# 🚨 Look-Ahead Bias

One of the most important problems in financial machine learning is **look-ahead bias**.

A model must only use information that would actually have been available at the time the forecast was made.

For example:

```text
Fiscal Year Ends
      ↓
Company Reports Results
      ↓
SEC Filing Becomes Public
      ↓
Information Becomes Available to Model
```

Using fiscal-year data before its actual filing date can accidentally leak future information into the training set.

### Production Requirement

Real-world datasets should therefore be aligned using:

```text
Filing Date
instead of
Fiscal Period End Date
```

whenever necessary.

---

# ⚠️ Important Modeling Notes

### 1️⃣ The model does not directly predict stock prices

The ML component forecasts operating fundamentals.

```text
ML
 ↓
Financial Variables
 ↓
FCFF
 ↓
DCF
 ↓
Fair Value
```

---

### 2️⃣ Accounting logic remains explicit

Free cash flow is calculated using standard accounting relationships rather than being generated directly by a black-box model.

---

### 3️⃣ Chronological backtesting is preferred

Random train/test splitting is avoided.

The project uses chronological and eventually rolling out-of-sample tests.

---

### 4️⃣ Point-in-time data is critical

Production datasets should use information availability dates to prevent look-ahead bias.

---

### 5️⃣ Financial companies require a different framework

Banks, insurers, and other financial institutions operate under fundamentally different balance-sheet structures.

Traditional corporate FCFF models are therefore generally not directly comparable.

A separate modeling framework is recommended for the **Financials sector**.

---

# 🏦 Why Not Predict Fair Value Directly?

A direct model could theoretically attempt:

```text
Financial Data
      ↓
Machine Learning
      ↓
Target Price
```

But this creates several problems.

❌ Low interpretability
❌ Difficult economic reasoning
❌ Greater risk of learning market noise
❌ Harder to identify incorrect assumptions
❌ Less connection to fundamental valuation

Instead, this project uses:

```text
Financial Data
      ↓
ML Forecast
      ↓
Fundamental Drivers
      ↓
FCFF
      ↓
DCF
      ↓
Fair Value
```

This makes each step of the valuation process inspectable.

---

# 🔬 Research Questions

This project is ultimately an experiment around several questions:

### 🤖 Can ML automate DCF assumptions?

Can historical financial behavior produce useful estimates of future operating variables?

### 📈 Which DCF variables are predictable?

Are variables such as margins or capital intensity more predictable than revenue growth?

### 🧠 Does regularization improve financial forecasting?

Can Ridge or Elastic Net provide more stable forecasts than simple historical averages?

### 🏢 Does predictability vary by sector?

Do software, industrial, consumer, and healthcare companies require different models?

### 💰 Does better fundamental forecasting improve valuation?

Forecast accuracy alone does not necessarily imply better investment decisions.

The final question is whether improved fundamental forecasts translate into more useful valuation estimates.

---

# 🧭 Modeling Philosophy

The project follows several principles:

```text
No Direct Price Prediction
        ↓
Forecast Fundamentals
        ↓
Preserve Accounting Logic
        ↓
Use Chronological Testing
        ↓
Prevent Information Leakage
        ↓
Evaluate Out-of-Sample
```

The objective is not to replace fundamental analysis.

The objective is to test whether machine learning can make parts of the fundamental forecasting process more **systematic, scalable, and testable**.

---

# 🔮 Future Improvements

Planned extensions include:

* 📅 Rolling and expanding-window backtesting
* 🕒 Full point-in-time SEC filing alignment
* 🌎 Market and macroeconomic data integration
* 🏢 Sector-specific forecasting models
* 🔍 Automated feature selection
* 📊 Historical-average benchmark models
* 🌲 Tree-based model comparison
* 🤖 Gradient boosting benchmarks
* 🎯 Analyst consensus integration
* 📉 Forecast uncertainty intervals
* 🧪 Model stability analysis
* 📑 Automated financial statement reconstruction
* 💵 Full multi-year DCF generation
* ⚖️ Bull / Base / Bear valuation scenarios
* 📈 Implied upside/downside analysis
* 🔄 Automated company-level backtesting
* 🧠 Model explainability and coefficient analysis

---

# 🧩 Long-Term Pipeline

```text
                  ┌─────────────────┐
                  │  SEC Financials │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   Market Data         Macro Data       Company Data
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                 Point-in-Time Dataset
                           │
                           ▼
                 Feature Engineering
                           │
                           ▼
                  Forecasting Models
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Ridge       Elastic Net     Future Models
             └─────────────┼─────────────┘
                           ▼
                  Financial Forecast
                           │
                           ▼
                         FCFF
                           │
                           ▼
                          DCF
                           │
                           ▼
                     Fair Value
                           │
                           ▼
                  Backtest & Analysis
```

---

# ⚠️ Disclaimer

This repository is an **experimental research project**.

It is not financial advice and should not be interpreted as a production investment system.

Model outputs depend heavily on:

* Data quality
* Accounting consistency
* Feature construction
* Point-in-time availability
* Market regime
* Modeling assumptions
* DCF assumptions

Historical predictive performance does not guarantee future investment performance.

---

# 🚀 The Question

> **Can machine learning automate DCF?**

Not by directly predicting a stock price.

The more interesting possibility is using machine learning to forecast the **fundamental variables that drive valuation**, while keeping the financial logic of the DCF transparent.

That is what this project is designed to test.

