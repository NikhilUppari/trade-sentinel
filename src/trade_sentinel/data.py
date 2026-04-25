from __future__ import annotations

import math
from random import Random

from trade_sentinel.models import MarketSnapshot, PriceBar


def sample_snapshot(symbol: str, days: int = 90) -> MarketSnapshot:
    """Create deterministic demo data so the project works without network access."""
    rng = Random(symbol)
    base = 80 + (sum(ord(char) for char in symbol) % 140)
    drift = 0.0015 if symbol[0] < "N" else 0.0005
    bars: list[PriceBar] = []
    price = float(base)
    for day in range(days):
        cycle = math.sin(day / 9) * 0.008
        shock = rng.uniform(-0.018, 0.018)
        price = max(5.0, price * (1 + drift + cycle + shock))
        high = price * (1 + rng.uniform(0.002, 0.018))
        low = price * (1 - rng.uniform(0.002, 0.018))
        bars.append(PriceBar(close=round(price, 2), high=round(high, 2), low=round(low, 2), volume=rng.randint(900_000, 12_000_000)))
    return MarketSnapshot(symbol=symbol, bars=bars)


def fetch_snapshot(symbol: str, offline: bool = False, days: int = 180) -> MarketSnapshot:
    if offline:
        return sample_snapshot(symbol, days=min(days, 120))

    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError(
            "Market data requires yfinance. Install with: pip install -e \".[market]\" "
            "or run with --offline."
        ) from exc

    frame = yf.Ticker(symbol).history(period="6mo", interval="1d", auto_adjust=True)
    if frame.empty:
        raise RuntimeError(f"No market data returned for {symbol}.")

    bars = [
        PriceBar(
            close=float(row.Close),
            high=float(row.High),
            low=float(row.Low),
            volume=int(row.Volume),
        )
        for row in frame.itertuples()
    ]
    return MarketSnapshot(symbol=symbol, bars=bars[-days:])
