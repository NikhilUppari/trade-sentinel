# Trade Sentinel

Trade Sentinel is an AI-assisted stock research agent for watchlist analysis, paper-trading ideas, and risk-aware reporting. It is designed as a portfolio project: practical enough to run, documented enough to extend, and conservative enough to avoid pretending that trading is magic.

> This project is for education and research. It is not financial advice and it does not place real trades.

## What It Does

- Loads a stock watchlist from YAML.
- Pulls market data when `yfinance` is installed, or uses deterministic sample data for offline demos.
- Computes trend, momentum, volatility, and risk signals.
- Scores each ticker as `bullish`, `neutral`, or `avoid`.
- Produces a research report with position sizing guidance.
- Optionally adds LLM commentary when an OpenAI API key is configured.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[market,ai,ui,dev]"
trade-sentinel analyze --watchlist examples/watchlist.yaml --cash 10000
```

Offline demo without market dependencies:

```bash
pip install -e .
trade-sentinel analyze --watchlist examples/watchlist.yaml --offline
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

## AI Agent Design

The agent separates analysis into four stages:

1. Data collection
2. Signal generation
3. Risk control
4. Research narration

The LLM layer is intentionally optional. The scoring engine works without it, so the project remains testable and explainable.

## Roadmap

- Add portfolio tracking and paper-trade history.
- Add earnings calendar awareness.
- Add broker sandbox integrations.
- Add a Streamlit dashboard.
- Add backtesting with transaction costs.

## Publish to GitHub

See [docs/github_publish.md](docs/github_publish.md) for the recommended repository setup.

## Safety

Trade Sentinel never sends live orders. Any suggested allocation is capped by configurable risk rules. Always do your own research before making investment decisions.
