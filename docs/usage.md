# Usage Guide

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[market,ai,ui,dev]"
```

If you only want to run the offline demo:

```bash
pip install -e .
```

## Analyze a Watchlist

```bash
trade-sentinel analyze --watchlist examples/watchlist.yaml --cash 10000
```

## Offline Demo

```bash
trade-sentinel analyze --watchlist examples/watchlist.yaml --offline
```

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
