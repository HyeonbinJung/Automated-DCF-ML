# ML DCF Forecasting MVP

목표: 과거 재무/시장/거시 데이터를 사용해 다음 해 DCF 핵심 변수들을 예측하고,
예측된 재무변수를 FCFF/DCF 엔진으로 전달하는 구조.

## Architecture

Data Collection
-> Cleaning
-> Feature Engineering
-> Ridge / ElasticNet
-> Financial Forecast
-> FCFF
-> DCF
-> Fair Value

Forecast targets:
- Revenue Growth
- EBIT Margin
- Effective Tax Rate
- D&A / Revenue
- CapEx / Revenue
- NWC / Revenue

## Backtest methodology

현재 MVP는 1-year-ahead forecasting을 strict time split으로 검증한다.

- Train: <= 2018
- Gap / validation period: 2019-2021
- Test: >= 2022
- Random shuffle split 사용 안 함
- 각 회사의 t 시점 feature로 t+1 실적을 예측

Metrics:
- R2
- Pearson r
- Spearman rho
- Direction Accuracy
- MAE
- RMSE
- Correlation Accuracy Index (프로젝트 내부 composite; 표준 통계량 아님)

Correlation Accuracy Index:
35% normalized Pearson +
25% normalized Spearman +
25% Direction Accuracy +
15% clipped R2

## Demo

`demo_panel.csv`는 파이프라인 검증용 합성 데이터다.
따라서 demo 성능 수치를 실전 투자 성능으로 해석하면 안 된다.

Run:

    pip install -r requirements.txt
    python run_backtest.py --data demo_panel.csv

## Real SEC data collection

SEC Company Facts API를 이용하는 기본 collector가 포함되어 있다.

SEC 요청 정책에 맞는 User-Agent를 환경변수로 지정:

macOS/Linux:
    export SEC_USER_AGENT="Your Name your@email.com"

Windows PowerShell:
    $env:SEC_USER_AGENT="Your Name your@email.com"

예:
    python collect_sec.py --tickers AAPL MSFT GOOGL META AMZN NVDA COST HD UNH CAT --start-year 2010

주의:
SEC만으로는 sector, market return/volatility/beta, macro series가 모두 채워지지 않는다.
실전 모델에서는 별도 market/macro source와 결합해야 한다.

## Important modeling notes

1. 모델이 target price를 직접 예측하지 않는다.
2. 미래 재무변수를 예측한 뒤 회계식으로 FCFF를 계산한다.
3. Random split보다 chronological / rolling backtest를 사용한다.
4. 실전에서는 filing date 기준 point-in-time 데이터로 구성해 look-ahead bias를 차단해야 한다.
5. Financial sector는 일반 corporate FCFF DCF와 구조가 달라 별도 모델이 권장된다.
