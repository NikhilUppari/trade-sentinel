from __future__ import annotations

import argparse

from trade_sentinel.agent import TradingResearchAgent, optional_ai_commentary
from trade_sentinel.broker import build_broker
from trade_sentinel.config import load_watchlist
from trade_sentinel.dashboard import write_dashboard
from trade_sentinel.models import PortfolioRules
from trade_sentinel.report import render_execution_results, render_order_plan, render_report
from trade_sentinel.trading import plan_buy_orders


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI-assisted stock research agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze a stock watchlist")
    analyze.add_argument("--watchlist", required=True, help="Path to YAML watchlist")
    analyze.add_argument("--cash", type=float, default=10_000, help="Available paper-trading cash")
    analyze.add_argument("--max-position-pct", type=float, default=0.12)
    analyze.add_argument("--max-volatility-pct", type=float, default=6.0)
    analyze.add_argument("--ai", action="store_true", help="Add optional LLM commentary")

    plan = subparsers.add_parser("plan-trades", help="Create risk-checked order tickets")
    plan.add_argument("--watchlist", required=True, help="Path to YAML watchlist")
    plan.add_argument("--cash", type=float, default=10_000, help="Available paper-trading cash")
    plan.add_argument("--max-position-pct", type=float, default=0.12)
    plan.add_argument("--max-volatility-pct", type=float, default=6.0)
    plan.add_argument("--min-trade-score", type=int, default=70)
    plan.add_argument("--max-order-value", type=float, default=2_000)
    plan.add_argument("--whole-shares", action="store_true", help="Disable fractional-share sizing")
    plan.add_argument(
        "--execute",
        action="store_true",
        help="Submit planned orders to the selected execution mode",
    )
    plan.add_argument(
        "--mode",
        choices=["dry-run", "paper", "live"],
        default="dry-run",
        help="Execution mode. dry-run never sends orders.",
    )

    dashboard = subparsers.add_parser("dashboard", help="Generate a browser-viewable HTML report")
    dashboard.add_argument("--watchlist", required=True, help="Path to YAML watchlist")
    dashboard.add_argument("--cash", type=float, default=10_000, help="Available paper-trading cash")
    dashboard.add_argument("--max-position-pct", type=float, default=0.12)
    dashboard.add_argument("--max-volatility-pct", type=float, default=6.0)
    dashboard.add_argument("--min-trade-score", type=int, default=70)
    dashboard.add_argument("--max-order-value", type=float, default=2_000)
    dashboard.add_argument("--whole-shares", action="store_true", help="Disable fractional-share sizing")
    dashboard.add_argument(
        "--output",
        default="reports/trade_sentinel_dashboard.html",
        help="Path for the generated HTML file",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "analyze":
        rules = PortfolioRules(
            cash=args.cash,
            max_position_pct=args.max_position_pct,
            max_volatility_pct=args.max_volatility_pct,
        )
        watchlist = load_watchlist(args.watchlist)
        agent = TradingResearchAgent(rules=rules)
        results = agent.analyze(watchlist)
        commentary = optional_ai_commentary(results) if args.ai else None
        render_report(results, rules, commentary)
    elif args.command == "plan-trades":
        rules = PortfolioRules(
            cash=args.cash,
            max_position_pct=args.max_position_pct,
            max_volatility_pct=args.max_volatility_pct,
            min_trade_score=args.min_trade_score,
            max_order_value=args.max_order_value,
            allow_fractional=not args.whole_shares,
        )
        watchlist = load_watchlist(args.watchlist)
        agent = TradingResearchAgent(rules=rules)
        results = agent.analyze(watchlist)
        tickets = plan_buy_orders(results, rules)
        render_order_plan(tickets)

        if args.execute:
            if args.mode == "live":
                raise SystemExit(
                    "Live execution is intentionally blocked from the CLI. "
                    "Use paper mode first, review the broker integration, then remove this guard yourself."
                )
            broker = build_broker(args.mode)
            execution_results = [broker.submit_order(ticket) for ticket in tickets]
            render_execution_results(execution_results)
    elif args.command == "dashboard":
        rules = PortfolioRules(
            cash=args.cash,
            max_position_pct=args.max_position_pct,
            max_volatility_pct=args.max_volatility_pct,
            min_trade_score=args.min_trade_score,
            max_order_value=args.max_order_value,
            allow_fractional=not args.whole_shares,
        )
        watchlist = load_watchlist(args.watchlist)
        agent = TradingResearchAgent(rules=rules)
        results = agent.analyze(watchlist)
        tickets = plan_buy_orders(results, rules)
        path = write_dashboard(results, rules, args.output, tickets)
        print(f"Dashboard written to {path}")


if __name__ == "__main__":
    main()
