from trade_sentinel.models import PortfolioRules, SignalResult
from trade_sentinel.trading import build_buy_ticket, plan_buy_orders


def bullish_result(symbol: str = "MSFT", score: int = 90) -> SignalResult:
    return SignalResult(
        symbol=symbol,
        label="bullish",
        score=score,
        reasons=["Uptrend confirmed", "Momentum improving", "Volatility acceptable"],
        latest_close=100,
        volatility_pct=2.0,
        suggested_allocation=1_200,
    )


def test_build_buy_ticket_for_bullish_signal():
    ticket = build_buy_ticket(bullish_result(), PortfolioRules(cash=10_000))

    assert ticket is not None
    assert ticket.symbol == "MSFT"
    assert ticket.side == "buy"
    assert ticket.quantity == 12
    assert ticket.estimated_value == 1_200


def test_build_buy_ticket_rejects_low_score():
    result = bullish_result(score=60)

    ticket = build_buy_ticket(result, PortfolioRules(cash=10_000, min_trade_score=70))

    assert ticket is None


def test_plan_buy_orders_respects_cash_limit():
    results = [bullish_result("MSFT"), bullish_result("GOOGL"), bullish_result("AMZN")]

    tickets = plan_buy_orders(results, PortfolioRules(cash=2_000))

    assert len(tickets) == 1
    assert tickets[0].estimated_value == 1_200
