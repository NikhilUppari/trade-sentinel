from __future__ import annotations

from trade_sentinel.models import PortfolioRules, WatchlistItem


def allocation_cap(item: WatchlistItem, rules: PortfolioRules, score: int, volatility_pct: float) -> float:
    score_multiplier = max(0.0, min(score / 100, 1.0))
    volatility_multiplier = 0.5 if volatility_pct > rules.max_volatility_pct else 1.0
    item_cap = item.max_allocation_pct if item.max_allocation_pct is not None else rules.max_position_pct
    capped_pct = min(item_cap, rules.max_position_pct) * score_multiplier * volatility_multiplier
    return round(rules.cash * capped_pct, 2)
