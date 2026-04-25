from __future__ import annotations

from trade_sentinel.models import OrderTicket, PortfolioRules, SignalResult


def build_buy_ticket(result: SignalResult, rules: PortfolioRules) -> OrderTicket | None:
    if result.label != "bullish":
        return None
    if result.score < rules.min_trade_score:
        return None
    if result.suggested_allocation <= 0:
        return None

    order_value = min(result.suggested_allocation, rules.max_order_value)
    if order_value < result.latest_close and not rules.allow_fractional:
        return None

    quantity = order_value / result.latest_close
    if not rules.allow_fractional:
        quantity = float(int(quantity))
        order_value = quantity * result.latest_close
    if quantity <= 0:
        return None

    return OrderTicket(
        symbol=result.symbol,
        side="buy",
        quantity=round(quantity, 6),
        order_type="market",
        time_in_force="day",
        estimated_price=result.latest_close,
        estimated_value=round(order_value, 2),
        reason=f"{result.label} signal with score {result.score}: {'; '.join(result.reasons)}",
    )


def plan_buy_orders(results: list[SignalResult], rules: PortfolioRules) -> list[OrderTicket]:
    tickets: list[OrderTicket] = []
    remaining_cash = rules.cash
    for result in results:
        ticket = build_buy_ticket(result, rules)
        if ticket is None:
            continue
        if ticket.estimated_value > remaining_cash:
            continue
        tickets.append(ticket)
        remaining_cash -= ticket.estimated_value
    return tickets
