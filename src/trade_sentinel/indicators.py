from __future__ import annotations

from statistics import mean, pstdev

from trade_sentinel.models import MarketSnapshot


def moving_average(values: list[float], window: int) -> float:
    if len(values) < window:
        return mean(values)
    return mean(values[-window:])


def daily_returns(values: list[float]) -> list[float]:
    return [(values[index] / values[index - 1]) - 1 for index in range(1, len(values))]


def volatility_pct(snapshot: MarketSnapshot, window: int = 20) -> float:
    closes = [bar.close for bar in snapshot.bars]
    returns = daily_returns(closes)[-window:]
    if not returns:
        return 0.0
    return round(pstdev(returns) * 100, 2)


def momentum_pct(snapshot: MarketSnapshot, window: int = 20) -> float:
    closes = [bar.close for bar in snapshot.bars]
    if len(closes) <= window:
        return 0.0
    return round(((closes[-1] / closes[-window]) - 1) * 100, 2)


def trend_score(snapshot: MarketSnapshot) -> int:
    closes = [bar.close for bar in snapshot.bars]
    ma20 = moving_average(closes, 20)
    ma50 = moving_average(closes, 50)
    latest = closes[-1]

    score = 0
    if latest > ma20:
        score += 20
    if ma20 > ma50:
        score += 20
    if latest > ma50:
        score += 10
    return score
