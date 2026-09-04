"""
SEC Company Facts collector.

This creates an annual company-level raw panel from SEC XBRL Company Facts.
Set SEC_USER_AGENT to a real name + email before running, per SEC guidance.

Example:
    export SEC_USER_AGENT="Your Name your@email.com"
    python collect_sec.py --tickers AAPL MSFT GOOGL META AMZN --start-year 2012
"""
import os
import time
import requests
import numpy as np
import pandas as pd

BASE = "https://data.sec.gov"
HEADERS = {
    "User-Agent": os.getenv("SEC_USER_AGENT", "Researcher example@example.com"),
    "Accept-Encoding": "gzip, deflate",
}

CONCEPTS = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
        "Revenues",
    ],
    "gross_profit": ["GrossProfit"],
    "operating_income": ["OperatingIncomeLoss"],
    "pretax_income": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
    "tax_expense": ["IncomeTaxExpenseBenefit"],
    "da": [
        "DepreciationDepletionAndAmortization",
        "DepreciationDepletionAndAmortizationPropertyPlantAndEquipment",
        "Depreciation",
    ],
    "capex": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsForAdditionsToPropertyPlantAndEquipment",
    ],
    "cash": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],
    "ar": ["AccountsReceivableNetCurrent"],
    "inventory": ["InventoryNet"],
    "ap": ["AccountsPayableCurrent"],
    "current_assets": ["AssetsCurrent"],
    "current_liabilities": ["LiabilitiesCurrent"],
    "ppe": ["PropertyPlantAndEquipmentNet"],
    "debt_current": ["LongTermDebtCurrent", "ShortTermBorrowings"],
    "debt_noncurrent": ["LongTermDebtNoncurrent"],
}

def _get_json(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def ticker_map():
    raw = _get_json(f"{BASE}/files/company_tickers.json")
    return {
        v["ticker"].upper(): str(v["cik_str"]).zfill(10)
        for v in raw.values()
    }

def _annual_fact(companyfacts, concept):
    facts = companyfacts.get("facts", {}).get("us-gaap", {}).get(concept, {})
    units = facts.get("units", {})
    # prefer USD, then shares / pure only if necessary
    candidates = units.get("USD", [])
    if not candidates:
        return pd.DataFrame()

    x = pd.DataFrame(candidates)
    if x.empty:
        return x
    x = x[x["form"].isin(["10-K", "10-K/A"])]
    if "fp" in x.columns:
        x = x[x["fp"].fillna("FY") == "FY"]
    if "fy" not in x.columns:
        return pd.DataFrame()

    x = x.dropna(subset=["fy", "val"])
    x = x.sort_values(["fy", "filed"]).drop_duplicates("fy", keep="last")
    return x[["fy", "val"]].rename(columns={"fy":"year", "val":concept})

def collect_ticker(ticker, cik, start_year=2009):
    facts = _get_json(f"{BASE}/api/xbrl/companyfacts/CIK{cik}.json")
    out = None

    for canonical, concepts in CONCEPTS.items():
        series = None
        for concept in concepts:
            candidate = _annual_fact(facts, concept)
            if not candidate.empty:
                candidate = candidate.rename(columns={concept:canonical})
                series = candidate
                break
        if series is None:
            continue
        out = series if out is None else out.merge(series, on="year", how="outer")

    if out is None:
        return pd.DataFrame()

    out["ticker"] = ticker
    out = out[out["year"] >= start_year].sort_values("year")

    # Derived DCF ratios
    out["revenue_growth"] = out["revenue"].pct_change()
    out["gross_margin"] = out["gross_profit"] / out["revenue"]
    out["ebit_margin"] = out["operating_income"] / out["revenue"]
    out["tax_rate"] = (out["tax_expense"] / out["pretax_income"]).clip(-0.2, 0.6)
    out["da_ratio"] = out["da"] / out["revenue"]
    out["capex_ratio"] = out["capex"].abs() / out["revenue"]

    out["nwc"] = out.get("ar", 0).fillna(0) + out.get("inventory", 0).fillna(0) - out.get("ap", 0).fillna(0)
    out["nwc_ratio"] = out["nwc"] / out["revenue"]

    debt_current = out["debt_current"] if "debt_current" in out else 0
    debt_noncurrent = out["debt_noncurrent"] if "debt_noncurrent" in out else 0
    out["debt"] = pd.Series(debt_current, index=out.index).fillna(0) + pd.Series(debt_noncurrent, index=out.index).fillna(0)

    # placeholders: enrich externally before final modeling
    for c in ["roic","debt_ebitda","volatility","beta","log_market_cap","gdp_growth","fed_rate","cpi","credit_spread","sector"]:
        if c not in out:
            out[c] = np.nan

    out["log_revenue"] = np.log(out["revenue"].clip(lower=1))
    return out

def collect(tickers, start_year=2009, pause=0.12):
    mapping = ticker_map()
    frames = []
    for ticker in tickers:
        t = ticker.upper()
        if t not in mapping:
            print(f"[skip] no CIK for {t}")
            continue
        try:
            f = collect_ticker(t, mapping[t], start_year=start_year)
            if not f.empty:
                frames.append(f)
                print(f"[ok] {t}: {len(f)} years")
        except Exception as e:
            print(f"[error] {t}: {e}")
        time.sleep(pause)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
