"""
시장 국면 전환(Regime Shift) 시뮬레이션 및 백테스트

프롬프트 요구사항:
1. 데이터 생성 (1,000일):
   - 신호 x는 정규분포를 따르며, 절반(500일) 시점에 수익률 예측 계수(beta)의 부호가 반전됨 (+0.003 -> -0.003)
   - t일 자산 수익률은 t-1일 신호(lag_x)와 노이즈(표준편차 0.012)로 생성
2. 전략 및 백테스트 규칙:
   - t일 종료 시 x > 0이면 1, 아니면 0으로 신호 생성
   - t+1일에 해당 포지션을 보유(held)하여 거래
   - 포지션 변화량(|diff|)에 비례해 거래비용(0.0003) 차감
   - 순수익률(net)을 기반으로 누적 자산 곡선(equity, 초기값 1) 및 MDD 계산
3. 결과 집계:
   - 0~500일(전반), 500~1000일(후반) 구간별 누적수익률과 최대낙폭(MDD)을 딕셔너리로 계산해 출력
"""

import numpy as np

try:
    import pandas as pd
except ImportError:
    pd = None


def regime_example(n: int = 1000, seed: int = 42, cost: float = 0.0003):
    """
    시장 국면 전환 시뮬레이션 및 백테스트 함수.

    Parameters
    ----------
    n : int, default=1000
        시뮬레이션 일수
    seed : int, default=42
        난수 발생 시드
    cost : float, default=0.0003
        포지션 변화 단위당 거래 비용 (슬리피지/수수료)

    Returns
    -------
    market : pd.DataFrame or dict
        일별 자산 수익률, 생성 신호, 보유 포지션, 순수익률
    equity : np.ndarray
        전체 기간 누적 자산 곡선 (초기값 1.0)
    drawdown : np.ndarray
        전체 기간 낙폭 (drawdown) 시계열
    """
    rng = np.random.default_rng(seed)

    # 1. 신호 생성 및 예측 계수 부호 반전 (Regime Shift)
    x = rng.normal(size=n)
    beta = np.where(np.arange(n) < n // 2, 0.003, -0.003)

    # t일 자산 수익률은 t-1일 신호(lag_x)와 노이즈(표준편차 0.012)로 생성
    lag_x = np.r_[0.0, x[:-1]]
    asset_return = beta * lag_x + rng.normal(0, 0.012, n)

    # 2. 포지션 신호 및 거래 규칙
    # t일 종료 시 x > 0이면 1, 아니면 0
    signal = (x > 0).astype(float)
    # t+1일에 t일 생성 신호를 보유(held)
    held = np.r_[0.0, signal[:-1]]

    # 포지션 변화량(|diff|)에 비례해 거래비용 차감
    turnover = np.abs(np.diff(np.r_[0.0, held]))
    net = held * asset_return - cost * turnover

    # 순수익률 기반 누적 자산 곡선(초기값 1.0) 및 낙폭 계산
    equity = np.r_[1.0, np.cumprod(1 + net)]
    peak = np.maximum.accumulate(equity)
    drawdown = equity / peak - 1.0

    market_data = {
        'return': asset_return,
        'signal': signal,
        'held': held,
        'net': net
    }

    if pd is not None:
        market = pd.DataFrame(market_data)
    else:
        market = market_data

    return market, equity, drawdown


def evaluate_regimes(market, split_point: int = 500) -> dict:
    """
    0~500일(전반)과 500~1000일(후반) 구간별 누적수익률과 최대낙폭(MDD) 집계
    """
    regime_result = {}

    if hasattr(market, 'iloc'):
        segments = [
            ('전반', market.iloc[:split_point]),
            ('후반', market.iloc[split_point:])
        ]
        get_net = lambda s: s['net'].to_numpy()
    else:
        segments = [
            ('전반', market['net'][:split_point]),
            ('후반', market['net'][split_point:])
        ]
        get_net = lambda s: s

    for name, sample in segments:
        net_returns = get_net(sample)
        wealth = np.r_[1.0, np.cumprod(1 + net_returns)]
        peak = np.maximum.accumulate(wealth)
        dd = wealth / peak - 1.0
        mdd = float(-dd.min())

        regime_result[name] = {
            '누적수익률': float(wealth[-1] - 1.0),
            '최대낙폭': mdd
        }

    return regime_result


if __name__ == '__main__':
    market, equity, drawdown = regime_example()
    results = evaluate_regimes(market)

    print("=" * 50)
    print("시장 국면 전환(Regime Shift) 백테스트 결과")
    print("=" * 50)
    import pprint
    pprint.pprint(results)

    print("\n[상세 성과 지표]")
    for regime, metrics in results.items():
        cum_ret = metrics['누적수익률'] * 100
        mdd = metrics['최대낙폭'] * 100
        print(f"- {regime} 구간 (500일):")
        print(f"  * 누적수익률: {cum_ret:+.2f}%")
        print(f"  * 최대낙폭(MDD): {mdd:.2f}%")
    print("=" * 50)
