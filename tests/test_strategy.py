from trade_sentinel.data import sample_snapshot
from trade_sentinel.models import PortfolioRules, WatchlistItem
from trade_sentinel.strategy import analyze_stock


def test_analyze_stock_returns_bounded_score_and_allocation():
    item = WatchlistItem(symbol="MSFT")
    snapshot = sample_snapshot("MSFT")
    result = analyze_stock(item, snapshot, PortfolioRules(cash=10_000))

    assert 0 <= result.score <= 100
    assert result.suggested_allocation <= 1_200
    assert result.label in {"bullish", "neutral", "avoid"}
    assert result.reasons
