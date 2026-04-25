from __future__ import annotations

import os

from trade_sentinel.data import fetch_snapshot
from trade_sentinel.models import PortfolioRules, SignalResult, WatchlistItem
from trade_sentinel.strategy import analyze_stock


class TradingResearchAgent:
    def __init__(self, rules: PortfolioRules, offline: bool = False):
        self.rules = rules
        self.offline = offline

    def analyze(self, watchlist: list[WatchlistItem]) -> list[SignalResult]:
        results: list[SignalResult] = []
        for item in watchlist:
            snapshot = fetch_snapshot(item.symbol, offline=self.offline)
            results.append(analyze_stock(item, snapshot, self.rules))
        return sorted(results, key=lambda result: result.score, reverse=True)


def optional_ai_commentary(results: list[SignalResult]) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=api_key)
    compact = [
        {
            "symbol": result.symbol,
            "label": result.label,
            "score": result.score,
            "volatility_pct": result.volatility_pct,
            "suggested_allocation": result.suggested_allocation,
            "reasons": result.reasons,
        }
        for result in results
    ]
    response = client.responses.create(
        model=os.getenv("TRADE_SENTINEL_MODEL", "gpt-4.1-mini"),
        input=[
            {
                "role": "system",
                "content": (
                    "You are a cautious trading research assistant. Summarize the watchlist, "
                    "emphasize risk, and never claim certainty or give personalized financial advice."
                ),
            },
            {"role": "user", "content": f"Summarize these scored stock setups: {compact}"},
        ],
    )
    return response.output_text
