from __future__ import annotations

from trade_sentinel.indicators import momentum_pct, trend_score, volatility_pct
from trade_sentinel.models import MarketSnapshot, PortfolioRules, SignalResult, WatchlistItem
from trade_sentinel.risk import allocation_cap


def analyze_stock(item: WatchlistItem, snapshot: MarketSnapshot, rules: PortfolioRules) -> SignalResult:
    trend = trend_score(snapshot)
    momentum = momentum_pct(snapshot)
    volatility = volatility_pct(snapshot)

    score = trend
    reasons: list[str] = []

    if trend >= 40:
        reasons.append("Uptrend confirmed")
    elif trend >= 20:
        reasons.append("Trend is mixed")
    else:
        reasons.append("Trend is weak")

    if momentum > 5:
        score += 25
        reasons.append("Momentum improving")
    elif momentum > 0:
        score += 10
        reasons.append("Momentum slightly positive")
    else:
        score -= 10
        reasons.append("Momentum is negative")

    if volatility <= rules.max_volatility_pct:
        score += 15
        reasons.append("Volatility acceptable")
    else:
        score -= 15
        reasons.append("Volatility above risk limit")

    score = max(0, min(100, score))
    if score >= 70:
        label = "bullish"
    elif score >= 45:
        label = "neutral"
    else:
        label = "avoid"

    return SignalResult(
        symbol=item.symbol,
        label=label,
        score=score,
        reasons=reasons,
        latest_close=snapshot.latest_close,
        volatility_pct=volatility,
        suggested_allocation=allocation_cap(item, rules, score, volatility),
    )
