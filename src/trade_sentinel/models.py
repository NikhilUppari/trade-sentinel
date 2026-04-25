from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SignalLabel = Literal["bullish", "neutral", "avoid"]


@dataclass(frozen=True)
class WatchlistItem:
    symbol: str
    thesis: str = ""
    max_allocation_pct: float | None = None


@dataclass(frozen=True)
class PriceBar:
    close: float
    high: float
    low: float
    volume: int


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    bars: list[PriceBar]

    @property
    def latest_close(self) -> float:
        return self.bars[-1].close


@dataclass(frozen=True)
class SignalResult:
    symbol: str
    label: SignalLabel
    score: int
    reasons: list[str]
    latest_close: float
    volatility_pct: float
    suggested_allocation: float


@dataclass(frozen=True)
class PortfolioRules:
    cash: float
    max_position_pct: float = 0.12
    max_volatility_pct: float = 6.0
