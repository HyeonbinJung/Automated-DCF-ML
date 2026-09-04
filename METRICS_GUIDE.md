# Backtest Metrics Guide

## R2
실제 값의 분산을 모델이 얼마나 설명하는지.
- 1.0: 완전 예측
- 0: 평균값 예측과 비슷
- <0: 단순 평균보다도 나쁨

## Pearson r
예측값과 실제값의 선형 상관관계.
- +1: 완전 양의 선형 관계
- 0: 선형 관계 없음
- -1: 완전 음의 선형 관계

높은 Pearson은 "높게 예측한 기업이 실제로도 높은가?"를 확인하는 데 유용하지만,
절대 오차가 작다는 뜻은 아니다.

## Spearman rho
예측 순위와 실제 순위의 상관관계.
Stock selection / cross-sectional ranking 관점에서 중요하다.

## Direction Accuracy
다음 해 값이 현재 대비 상승/하락하는 방향을 맞춘 비율.

예:
실제 EBIT margin 15% -> 18%
예측 15% -> 17%
=> 방향 적중

## MAE
평균 절대 오차. 해석이 가장 직관적.

## RMSE
큰 오차에 더 큰 페널티를 주는 지표.

## Correlation Accuracy Index
이 프로젝트에서 비교 편의를 위해 만든 0~100 composite다.
업계 표준 지표가 아니므로 R2/Pearson/Spearman/MAE를 대체하면 안 된다.
