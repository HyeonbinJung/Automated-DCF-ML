import numpy as np
import pandas as pd

TARGETS = [
    "revenue_growth",
    "ebit_margin",
    "tax_rate",
    "da_ratio",
    "capex_ratio",
    "nwc_ratio",
]

BASE_FEATURES = [
    "revenue_growth", "gross_margin", "ebit_margin", "tax_rate",
    "da_ratio", "capex_ratio", "nwc_ratio", "roic",
    "debt_ebitda", "volatility", "beta",
    "log_revenue", "log_market_cap",
    "gdp_growth", "fed_rate", "cpi", "credit_spread",
]

LAG_COLS = [
    "revenue_growth", "ebit_margin", "capex_ratio",
    "da_ratio", "nwc_ratio", "roic"
]

def engineer_features(df: pd.DataFrame):
    df = df.sort_values(["ticker", "year"]).copy()

    for c in LAG_COLS:
        if c in df.columns:
            df[f"{c}_lag1"] = df.groupby("ticker")[c].shift(1)
            df[f"{c}_lag2"] = df.groupby("ticker")[c].shift(2)
            df[f"{c}_3y_mean"] = df.groupby("ticker")[c].transform(
                lambda s: s.shift(1).rolling(3).mean()
            )

    for t in TARGETS:
        if t in df.columns:
            df[f"target_{t}"] = df.groupby("ticker")[t].shift(-1)

    if "sector" in df.columns:
        df = pd.get_dummies(df, columns=["sector"], drop_first=True)

    features = [
        c for c in BASE_FEATURES if c in df.columns
    ]
    features += [
        c for c in df.columns
        if ("_lag" in c or "_3y_mean" in c or c.startswith("sector_"))
    ]
    features = sorted(set(features))
    return df, features
