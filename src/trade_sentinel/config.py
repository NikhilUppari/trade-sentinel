from __future__ import annotations

from pathlib import Path

from trade_sentinel.models import WatchlistItem


def load_watchlist(path: str | Path) -> list[WatchlistItem]:
    text = Path(path).read_text(encoding="utf-8")
    items = _parse_watchlist_yaml(text)
    if not items:
        raise ValueError("Watchlist is empty or invalid.")
    return items


def _parse_watchlist_yaml(text: str) -> list[WatchlistItem]:
    """Parse the small watchlist YAML shape without requiring PyYAML."""
    watchlist: list[WatchlistItem] = []
    current: dict[str, str] | None = None

    def flush() -> None:
        nonlocal current
        if current and current.get("symbol"):
            cap = current.get("max_allocation_pct")
            watchlist.append(
                WatchlistItem(
                    symbol=current["symbol"].upper(),
                    thesis=current.get("thesis", ""),
                    max_allocation_pct=float(cap) if cap else None,
                )
            )
        current = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "watchlist:":
            continue
        if line.startswith("- "):
            flush()
            current = {}
            line = line[2:].strip()
            if ":" not in line:
                current["symbol"] = _clean_value(line)
                continue
        if ":" in line:
            if current is None:
                current = {}
            key, value = line.split(":", 1)
            current[key.strip()] = _clean_value(value)
    flush()
    return watchlist


def _clean_value(value: str) -> str:
    return value.strip().strip("\"'")
