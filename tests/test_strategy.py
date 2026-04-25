from trade_sentinel.models import MarketSnapshot, PortfolioRules, PriceBar, WatchlistItem
from trade_sentinel.strategy import analyze_stock


def test_analyze_stock_returns_bounded_score_and_allocation():
    item = WatchlistItem(symbol="MSFT")
    snapshot = MarketSnapshot(
        symbol="MSFT",
        bars=[
            PriceBar(close=100 + index, high=101 + index, low=99 + index, volume=1_000_000)
            for index in range(90)
        ],
    )
    result = analyze_stock(item, snapshot, PortfolioRules(cash=10_000))

    assert 0 <= result.score <= 100
    assert result.suggested_allocation <= 1_200
    assert result.label in {"bullish", "neutral", "avoid"}
    assert result.reasons
