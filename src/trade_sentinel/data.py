from __future__ import annotations

from trade_sentinel.models import MarketSnapshot, PriceBar


def fetch_snapshot(symbol: str, days: int = 180) -> MarketSnapshot:
    """Fetch recent market data from Yahoo Finance through yfinance.

    Free public market-data sources can be delayed and are not a replacement for
    paid exchange feeds. This is suitable for research and paper-trading workflows.
    """
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError(
            "Market data requires yfinance. Install the project with: pip install -e ."
        ) from exc

    ticker = yf.Ticker(symbol)
    frame = ticker.history(period="6mo", interval="1d", auto_adjust=True)
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
