from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

from trade_sentinel.models import OrderTicket, PortfolioRules, SignalResult


def write_dashboard(
    results: list[SignalResult],
    rules: PortfolioRules,
    output_path: str | Path,
    tickets: list[OrderTicket] | None = None,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_render_dashboard(results, rules, tickets or []), encoding="utf-8")
    return path


def _render_dashboard(
    results: list[SignalResult], rules: PortfolioRules, tickets: list[OrderTicket]
) -> str:
    bullish = sum(1 for result in results if result.label == "bullish")
    neutral = sum(1 for result in results if result.label == "neutral")
    avoid = sum(1 for result in results if result.label == "avoid")
    total_alloc = sum(result.suggested_allocation for result in results)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    rows = "\n".join(_signal_row(result) for result in results)
    ticket_rows = "\n".join(_ticket_row(ticket) for ticket in tickets)
    if not ticket_rows:
        ticket_rows = """
          <tr>
            <td colspan="6" class="empty">No order tickets passed the current signal and risk rules.</td>
          </tr>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Trade Sentinel Dashboard</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4f7fb;
      --panel: #ffffff;
      --ink: #18212f;
      --muted: #687386;
      --line: #d9e1ec;
      --green: #0b8f5a;
      --amber: #af6b00;
      --red: #b42318;
      --blue: #255cc7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    header {{
      background: #101828;
      color: white;
      padding: 28px 32px;
    }}
    header h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      font-weight: 750;
      letter-spacing: 0;
    }}
    header p {{
      margin: 0;
      color: #cbd5e1;
      max-width: 850px;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 28px 20px 48px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(5, minmax(140px, 1fr));
      gap: 12px;
      margin-bottom: 22px;
    }}
    .metric {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 6px;
    }}
    .metric strong {{
      font-size: 22px;
    }}
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      margin-top: 18px;
      overflow: hidden;
    }}
    section h2 {{
      margin: 0;
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
      font-size: 18px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      padding: 12px 14px;
      text-align: left;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0;
      background: #f8fafc;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    .number {{ text-align: right; white-space: nowrap; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 12px;
      font-weight: 700;
      text-transform: capitalize;
    }}
    .bullish {{ color: var(--green); background: #e7f7ef; }}
    .neutral {{ color: var(--amber); background: #fff3df; }}
    .avoid {{ color: var(--red); background: #fde8e7; }}
    .reason {{ color: var(--muted); max-width: 340px; }}
    .empty {{ color: var(--muted); text-align: center; padding: 26px; }}
    .note {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
      padding: 14px 18px 18px;
      border-top: 1px solid var(--line);
      background: #fbfdff;
    }}
    @media (max-width: 900px) {{
      .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      table {{ min-width: 760px; }}
      .scroll {{ overflow-x: auto; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Trade Sentinel Dashboard</h1>
    <p>Research signals and risk-checked trade planning generated from recent market data. Generated {generated_at}.</p>
  </header>
  <main>
    <div class="metrics">
      <div class="metric"><span>Cash</span><strong>${rules.cash:,.0f}</strong></div>
      <div class="metric"><span>Bullish</span><strong>{bullish}</strong></div>
      <div class="metric"><span>Neutral</span><strong>{neutral}</strong></div>
      <div class="metric"><span>Avoid</span><strong>{avoid}</strong></div>
      <div class="metric"><span>Max Allocations</span><strong>${total_alloc:,.0f}</strong></div>
    </div>

    <section>
      <h2>Research Signals</h2>
      <div class="scroll">
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Signal</th>
              <th class="number">Score</th>
              <th class="number">Last</th>
              <th class="number">Volatility</th>
              <th class="number">Max Allocation</th>
              <th>Reasons</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <div class="note">Signals are rule-based research outputs, not guarantees or personalized financial advice.</div>
    </section>

    <section>
      <h2>Order Plan</h2>
      <div class="scroll">
        <table>
          <thead>
            <tr>
              <th>Side</th>
              <th>Symbol</th>
              <th class="number">Quantity</th>
              <th>Type</th>
              <th class="number">Est. Price</th>
              <th class="number">Est. Value</th>
            </tr>
          </thead>
          <tbody>{ticket_rows}</tbody>
        </table>
      </div>
      <div class="note">Order tickets are planned trades. Use dry-run or paper mode before considering any live workflow.</div>
    </section>
  </main>
</body>
</html>
"""


def _signal_row(result: SignalResult) -> str:
    reasons = escape("; ".join(result.reasons))
    return f"""
            <tr>
              <td><strong>{escape(result.symbol)}</strong></td>
              <td><span class="badge {result.label}">{escape(result.label)}</span></td>
              <td class="number">{result.score}</td>
              <td class="number">${result.latest_close:,.2f}</td>
              <td class="number">{result.volatility_pct:.2f}%</td>
              <td class="number">${result.suggested_allocation:,.2f}</td>
              <td class="reason">{reasons}</td>
            </tr>
    """


def _ticket_row(ticket: OrderTicket) -> str:
    return f"""
            <tr>
              <td>{escape(ticket.side.upper())}</td>
              <td><strong>{escape(ticket.symbol)}</strong></td>
              <td class="number">{ticket.quantity:g}</td>
              <td>{escape(ticket.order_type)} / {escape(ticket.time_in_force)}</td>
              <td class="number">${ticket.estimated_price:,.2f}</td>
              <td class="number">${ticket.estimated_value:,.2f}</td>
            </tr>
    """
