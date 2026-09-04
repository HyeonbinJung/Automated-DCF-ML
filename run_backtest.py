import argparse
import pandas as pd
from src.backtest import run_backtest

p = argparse.ArgumentParser()
p.add_argument("--data", default="demo_panel.csv")
p.add_argument("--train-end", type=int, default=2018)
p.add_argument("--test-start", type=int, default=2022)
p.add_argument("--out-prefix", default="backtest")
args = p.parse_args()

df = pd.read_csv(args.data)
metrics, summary, predictions, features = run_backtest(
    df, train_end=args.train_end, test_start=args.test_start
)

metrics.to_csv(f"{args.out_prefix}_metrics.csv", index=False)
summary.to_csv(f"{args.out_prefix}_summary.csv", index=False)
predictions.to_csv(f"{args.out_prefix}_predictions.csv", index=False)

print(f"Features used: {len(features)}")
print(summary.round(4).to_string(index=False))
