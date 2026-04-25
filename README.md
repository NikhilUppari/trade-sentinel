# Trade Sentinel

Trade Sentinel is an AI-assisted stock research and trade-planning agent for watchlist analysis, risk-aware order planning, and broker-ready paper-trading workflows. It is designed as a portfolio project: practical enough to run, documented enough to extend, and conservative enough to avoid pretending that trading is magic.

> This project is for education and research. It is not financial advice and it does not place real trades.

## What It Does

- Loads a stock watchlist from YAML.
- Pulls recent stock data from Yahoo Finance through `yfinance`.
- Computes trend, momentum, volatility, and risk signals.
- Scores each ticker as `bullish`, `neutral`, or `avoid`.
- Produces a research report with position sizing guidance.
- Creates risk-checked buy order tickets with a `plan-trades` command.
- Supports dry-run execution by default and broker-ready paper execution through Alpaca.
- Optionally adds LLM commentary when an OpenAI API key is configured.

Free finance APIs are usually delayed and can have usage limits. Trade Sentinel is built for research and paper trading, not high-frequency execution.

## Why It Starts With a Watchlist

Trade Sentinel analyzes a watchlist because v1 is designed to be a reliable research assistant, not a noisy market scanner. A watchlist gives the agent a controlled universe of companies or ETFs that the user already cares about, which makes the output easier to inspect, test, and trust.

This also avoids a common trading-agent mistake: scanning thousands of tickers with shallow data and returning random-looking "top picks." The better workflow is:

1. Build or import a universe of candidate stocks.
2. Filter that universe with simple rules such as liquidity, volatility, trend, sector, and market cap.
3. Send the smaller candidate list into the research agent.
4. Produce a risk-aware report for human review.

In other words, the watchlist is the current input layer. A future discovery mode can generate that watchlist automatically.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[ai,ui,dev]"
trade-sentinel analyze --watchlist examples/watchlist.yaml --cash 10000
```

Create a risk-checked order plan:

```bash
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000
```

Dry-run the planned orders without sending anything to a broker:

```bash
trade-sentinel plan-trades --watchlist examples/watchlist.yaml --cash 10000 --execute --mode dry-run
```

Run tests:

```bash
pytest
```

## Example Output

```text
Trade Sentinel Research Report
Cash: $10,000

MSFT | bullish | score 74
Suggested max allocation: $1,200
Reason: Uptrend confirmed, momentum improving, volatility acceptable.
```

## Project Structure

```text
src/trade_sentinel/   Core package
tests/                Unit tests
docs/                 Architecture, usage, and safety notes
examples/             Example watchlists
```

Helpful docs:

- [Usage Guide](docs/usage.md)
- [Architecture](docs/architecture.md)
- [Universe Selection](docs/universe_selection.md)
- [Trading Workflow](docs/trading_workflow.md)
- [Safety Notes](docs/safety.md)

## AI Agent Design

The agent separates analysis into four stages:

1. Data collection
2. Signal generation
3. Risk control
4. Order planning
5. Research narration or dry-run execution

The LLM layer is intentionally optional. The scoring engine works from market data without it, so the project remains testable and explainable.

## Trading Modes

- `analyze`: produces research signals only.
- `plan-trades`: creates order tickets from bullish signals that pass risk rules.
- `--execute --mode dry-run`: simulates execution locally and sends no broker orders.
- `--execute --mode paper`: submits to a paper broker when broker credentials are configured.

The CLI intentionally blocks `--mode live`. This project should prove itself in research and paper trading before live order execution is enabled by a developer who understands the risks.

## Roadmap

- Add market discovery mode for scanning a larger stock universe.
- Add filters for volume, price, volatility, trend, and sector.
- Add portfolio tracking and paper-trade history.
- Add earnings calendar awareness.
- Add a second free data provider fallback.
- Expand broker sandbox integrations.
- Add a Streamlit dashboard.
- Add backtesting with transaction costs.

## Publish to GitHub

See [docs/github_publish.md](docs/github_publish.md) for the recommended repository setup.

## Safety

Trade Sentinel never sends live orders from the default CLI. Any suggested allocation is capped by configurable risk rules. Always do your own research before making investment decisions.
