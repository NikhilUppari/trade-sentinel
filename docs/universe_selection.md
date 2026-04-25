# Universe Selection

Trade Sentinel currently starts from a watchlist.

That means the user provides a list of stocks or ETFs, and the agent analyzes only those symbols. This is a deliberate v1 design choice.

## Why Not Scan Every Stock Immediately?

Scanning the whole market sounds more powerful, but it can produce noisy and misleading results if the filters are weak. A broad scan can include illiquid stocks, penny stocks, temporary news spikes, broken data, or companies that do not fit the user's strategy.

A watchlist-based workflow is simpler and more transparent:

- The user knows exactly what the agent is analyzing.
- The same symbols can be compared across multiple days.
- The output is easier to manually verify.
- The risk engine can size positions against a known set of candidates.
- The project stays understandable for a first release.

## Recommended Workflow

1. Choose a starting universe, such as AI stocks, mega-cap tech, ETFs, dividend stocks, or S&P 500 names.
2. Save those symbols in `examples/watchlist.yaml`.
3. Run Trade Sentinel against that watchlist.
4. Review the report manually.
5. Update the watchlist as your investing thesis changes.

## Future Discovery Mode

The next version can add a `discover` command that creates a candidate watchlist automatically.

Example future command:

```bash
trade-sentinel discover --universe sp500 --min-volume 1000000 --min-price 10 --top 25
```

Possible filters:

- Minimum average volume
- Minimum stock price
- Positive 20-day momentum
- Price above 50-day moving average
- Maximum volatility
- Sector or industry
- Market-cap range

The important design principle is that discovery should create candidates, not final decisions. The normal analysis and risk engines should still score the discovered symbols before the user acts.
