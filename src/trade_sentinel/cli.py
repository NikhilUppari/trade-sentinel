from __future__ import annotations

import argparse

from trade_sentinel.agent import TradingResearchAgent, optional_ai_commentary
from trade_sentinel.config import load_watchlist
from trade_sentinel.models import PortfolioRules
from trade_sentinel.report import render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI-assisted stock research agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze a stock watchlist")
    analyze.add_argument("--watchlist", required=True, help="Path to YAML watchlist")
    analyze.add_argument("--cash", type=float, default=10_000, help="Available paper-trading cash")
    analyze.add_argument("--max-position-pct", type=float, default=0.12)
    analyze.add_argument("--max-volatility-pct", type=float, default=6.0)
    analyze.add_argument("--offline", action="store_true", help="Use deterministic sample data")
    analyze.add_argument("--ai", action="store_true", help="Add optional LLM commentary")
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
        agent = TradingResearchAgent(rules=rules, offline=args.offline)
        results = agent.analyze(watchlist)
        commentary = optional_ai_commentary(results) if args.ai else None
        render_report(results, rules, commentary)


if __name__ == "__main__":
    main()
