from trade_sentinel.dashboard import write_dashboard
from trade_sentinel.models import OrderTicket, PortfolioRules, SignalResult


def test_write_dashboard_creates_html_file(tmp_path):
    result = SignalResult(
        symbol="MSFT",
        label="bullish",
        score=90,
        reasons=["Uptrend confirmed"],
        latest_close=100,
        volatility_pct=2,
        suggested_allocation=1_000,
    )
    ticket = OrderTicket(
        symbol="MSFT",
        side="buy",
        quantity=10,
        order_type="market",
        time_in_force="day",
        estimated_price=100,
        estimated_value=1_000,
        reason="Test order",
    )

    path = write_dashboard([result], PortfolioRules(cash=10_000), tmp_path / "dashboard.html", [ticket])

    html = path.read_text(encoding="utf-8")
    assert "Trade Sentinel Dashboard" in html
    assert "MSFT" in html
    assert "Order Plan" in html
