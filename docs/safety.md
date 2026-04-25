# Safety and Financial Disclaimer

Trade Sentinel is an educational research project.

It does not:

- Place live trades by default
- Guarantee returns
- Replace human judgment
- Provide personalized financial advice

Markets are risky. A signal can be directionally sensible and still lose money. Earnings, interest rates, liquidity, valuation, news, and macro shocks can overwhelm technical signals.

The project uses a free public market-data source. That data may be delayed, incomplete, adjusted, rate limited, or temporarily unavailable.

The current version analyzes a user-provided watchlist. This is safer than automatically scanning the whole market because it keeps the investment universe visible and reviewable. Future market discovery features should use strict filters and should still require human review before any trading decision.

The trading workflow is intentionally staged:

1. `analyze` creates research signals.
2. `plan-trades` creates risk-checked order tickets.
3. `--execute --mode dry-run` simulates broker submission without sending orders.
4. `--execute --mode paper` can send orders to a paper broker when configured.

The CLI blocks live execution. Removing that guard should only happen after adding account-position checks, daily loss limits, duplicate-order prevention, audit logs, and explicit human confirmation.

Recommended safeguards:

- Use paper trading before real money.
- Keep position sizes small.
- Avoid concentrating in one sector.
- Never risk money needed for bills, rent, tuition, or emergencies.
- Review every result manually before acting.

Future broker integrations should default to sandbox mode and require explicit confirmation before any order is sent.
