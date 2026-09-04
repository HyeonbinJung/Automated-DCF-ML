import pandas as pd
from .features import engineer_features, TARGETS
from .models import make_models
from .metrics import evaluate

def run_backtest(panel, train_end=2018, test_start=2022):
    df, features = engineer_features(panel)

    required_targets = [f"target_{t}" for t in TARGETS if f"target_{t}" in df.columns]
    usable_targets = [t for t in TARGETS if f"target_{t}" in df.columns and t in df.columns]
    df = df.dropna(subset=features + required_targets).copy()

    train = df[df["year"] <= train_end]
    test = df[df["year"] >= test_start]

    metrics = []
    predictions = []

    for target in usable_targets:
        ycol = f"target_{target}"
        Xtr, ytr = train[features], train[ycol]
        Xte, yte = test[features], test[ycol]
        current = test[target].to_numpy()

        for name, model in make_models().items():
            model.fit(Xtr, ytr)
            pred = model.predict(Xte)
            row = {"target": target, "model": name, "n_test": len(yte)}
            row.update(evaluate(yte, pred, current))
            metrics.append(row)

            p = test[["ticker", "year", target]].copy()
            p["target"] = target
            p["model"] = name
            p["actual_next"] = yte.to_numpy()
            p["pred_next"] = pred
            predictions.append(p)

    metrics = pd.DataFrame(metrics)
    predictions = pd.concat(predictions, ignore_index=True)

    summary = metrics.groupby("model", as_index=False).agg({
        "R2":"mean",
        "Pearson_r":"mean",
        "Spearman_rho":"mean",
        "Direction_Accuracy":"mean",
        "MAE":"mean",
        "RMSE":"mean",
        "Correlation_Accuracy_Index":"mean"
    })
    return metrics, summary, predictions, features
