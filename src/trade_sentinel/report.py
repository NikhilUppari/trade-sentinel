from __future__ import annotations

from trade_sentinel.models import ExecutionResult, OrderTicket, PortfolioRules, SignalResult


def render_report(results: list[SignalResult], rules: PortfolioRules, ai_commentary: str | None = None) -> None:
    try:
        _render_rich_report(results, rules, ai_commentary)
    except ImportError:
        _render_plain_report(results, rules, ai_commentary)


def _render_plain_report(
    results: list[SignalResult], rules: PortfolioRules, ai_commentary: str | None = None
) -> None:
    print("Trade Sentinel Research Report")
    print(f"Cash: ${rules.cash:,.2f}")
    print()
    for result in results:
        print(
            f"{result.symbol:6} {result.label:8} score={result.score:3} "
            f"last=${result.latest_close:,.2f} volatility={result.volatility_pct:.2f}% "
            f"max_allocation=${result.suggested_allocation:,.2f}"
        )
        print(f"  Reasons: {'; '.join(result.reasons)}")
    if ai_commentary:
        print()
        print("AI Commentary")
        print(ai_commentary)


def _render_rich_report(
    results: list[SignalResult], rules: PortfolioRules, ai_commentary: str | None = None
) -> None:
    from rich.console import Console
    from rich.table import Table

    console = Console()
    console.print("[bold]Trade Sentinel Research Report[/bold]")
    console.print(f"Cash: ${rules.cash:,.2f}")
    console.print()

    table = Table(show_header=True, header_style="bold")
    table.add_column("Symbol")
    table.add_column("Signal")
    table.add_column("Score", justify="right")
    table.add_column("Last", justify="right")
    table.add_column("Volatility", justify="right")
    table.add_column("Max Allocation", justify="right")
    table.add_column("Reasons")

    for result in results:
        table.add_row(
            result.symbol,
            result.label,
            str(result.score),
            f"${result.latest_close:,.2f}",
            f"{result.volatility_pct:.2f}%",
            f"${result.suggested_allocation:,.2f}",
            "; ".join(result.reasons),
        )

    console.print(table)
    if ai_commentary:
        console.print()
        console.print("[bold]AI Commentary[/bold]")
        console.print(ai_commentary)


def render_order_plan(tickets: list[OrderTicket]) -> None:
    if not tickets:
        print("No order tickets passed the current signal and risk rules.")
        return

    print("Trade Sentinel Order Plan")
    print()
    for ticket in tickets:
        print(
            f"{ticket.side.upper():4} {ticket.symbol:6} qty={ticket.quantity} "
            f"type={ticket.order_type} tif={ticket.time_in_force} "
            f"est_price=${ticket.estimated_price:,.2f} est_value=${ticket.estimated_value:,.2f}"
        )
        print(f"  Reason: {ticket.reason}")


def render_execution_results(results: list[ExecutionResult]) -> None:
    if not results:
        return

    print()
    print("Execution Results")
    for result in results:
        ticket = result.ticket
        print(
            f"{result.mode:7} {result.status:9} {ticket.side.upper()} {ticket.symbol} "
            f"qty={ticket.quantity}: {result.message}"
        )
