# Usage Guide

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[ai,ui,dev]"
```

## Analyze a Watchlist

```bash
trade-sentinel analyze --watchlist examples/watchlist.yaml --cash 10000
```

This command pulls recent market data from Yahoo Finance through `yfinance`.

Free market-data APIs may be delayed, rate limited, or occasionally unavailable. Treat the report as research input, not a live trading signal.

## Plan Trades

After analyzing the watchlist, Trade Sentinel can convert bullish signals into risk-checked order tickets:

```bash
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000
```

The order planner only creates buy tickets when:

- The signal is `bullish`.
- The score is at or above `--min-trade-score`.
- The allocation passes max-position and max-order-value rules.
- The account cash value can support the planned ticket.

Useful options:

```bash
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000 --min-trade-score 80
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000 --max-order-value 500
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000 --whole-shares
```

## Dry-Run Execution

Dry-run execution prints what would be submitted, but sends no orders to a broker:

```bash
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000 --execute --mode dry-run
```

This is the safest way to verify the full trading workflow.

## HTML Dashboard

Generate a standalone dashboard that opens in any browser:

```bash
trade-sentinel dashboard --watchlist examples/watchlist.yaml --cash 10000
```

By default, the file is written to:

```text
reports/trade_sentinel_dashboard.html
```

You can choose a custom path:

```bash
trade-sentinel dashboard --watchlist examples/watchlist.yaml --cash 10000 --output reports/my_report.html
```

The dashboard includes summary metrics, research signals, and the current order plan. Generated reports are ignored by Git through the `reports/` folder.

## Paper Broker Execution

The project includes an Alpaca-compatible broker adapter for paper trading.

Set credentials:

```bash
$env:ALPACA_API_KEY="your-paper-key"
$env:ALPACA_SECRET_KEY="your-paper-secret"
$env:ALPACA_BASE_URL="https://paper-api.alpaca.markets"
```

Then run:

```bash
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000 --execute --mode paper
```

Live execution is intentionally blocked from the CLI. That guard is there because real-money execution should only be enabled after paper trading, backtesting, account-position checks, and manual review are added.

## Why Use a Watchlist?

The current version analyzes a watchlist because it keeps the research universe explicit. You decide which stocks or ETFs are worth studying, then Trade Sentinel scores them with the same trend, momentum, volatility, and allocation rules.

That makes the first version easier to understand:

- The input is visible in `examples/watchlist.yaml`.
- Every ticker in the report has a reason for being there.
- The agent does not silently scan thousands of low-quality or illiquid tickers.
- Results are easier to compare across multiple runs.

The next natural feature is a discovery command that builds a watchlist automatically from a larger universe. For example, it could scan S&P 500 names, remove low-volume stocks, filter for positive momentum, and then send the survivors into the same analysis engine.

## Optional AI Commentary

Set an API key, then pass `--ai`:

```bash
$env:OPENAI_API_KEY="your-key"
trade-sentinel analyze --watchlist examples/watchlist.yaml --cash 10000 --ai
```

## Watchlist Format

```yaml
watchlist:
  - symbol: MSFT
    thesis: High-quality cloud and AI infrastructure compounder.
    max_allocation_pct: 0.12
```

`max_allocation_pct` is optional. If it is missing, the global risk rule is used.

## Interpreting Signals

- `bullish`: The setup passes trend, momentum, and risk checks.
- `neutral`: The setup has mixed evidence.
- `avoid`: The setup has weak trend, negative momentum, or excessive risk.

The agent is a research assistant, not a trading system. It should be used as one input in a larger decision process.
