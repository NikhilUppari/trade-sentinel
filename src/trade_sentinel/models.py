from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SignalLabel = Literal["bullish", "neutral", "avoid"]
OrderSide = Literal["buy", "sell"]
OrderType = Literal["market", "limit"]
TimeInForce = Literal["day", "gtc"]
ExecutionMode = Literal["dry-run", "paper", "live"]


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
    min_trade_score: int = 70
    max_order_value: float = 2_000.0
    allow_fractional: bool = True


@dataclass(frozen=True)
class OrderTicket:
    symbol: str
    side: OrderSide
    quantity: float
    order_type: OrderType
    time_in_force: TimeInForce
    estimated_price: float
    estimated_value: float
    reason: str


@dataclass(frozen=True)
class ExecutionResult:
    ticket: OrderTicket
    mode: ExecutionMode
    status: str
    message: str
