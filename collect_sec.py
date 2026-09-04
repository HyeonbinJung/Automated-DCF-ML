import argparse
from src.sec_collector import collect

p = argparse.ArgumentParser()
p.add_argument("--tickers", nargs="+", required=True)
p.add_argument("--start-year", type=int, default=2009)
p.add_argument("--out", default="sec_panel_raw.csv")
args = p.parse_args()

df = collect(args.tickers, start_year=args.start_year)
df.to_csv(args.out, index=False)
print(f"saved {len(df)} rows -> {args.out}")
