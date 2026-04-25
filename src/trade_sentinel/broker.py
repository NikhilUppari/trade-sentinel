from __future__ import annotations

import os
from abc import ABC, abstractmethod

from trade_sentinel.models import ExecutionMode, ExecutionResult, OrderTicket


class BrokerClient(ABC):
    @abstractmethod
    def submit_order(self, ticket: OrderTicket) -> ExecutionResult:
        raise NotImplementedError


class DryRunBroker(BrokerClient):
    def submit_order(self, ticket: OrderTicket) -> ExecutionResult:
        return ExecutionResult(
            ticket=ticket,
            mode="dry-run",
            status="accepted",
            message="Dry run only. No order was sent to a broker.",
        )


class AlpacaBroker(BrokerClient):
    def __init__(self, mode: ExecutionMode):
        if mode not in {"paper", "live"}:
            raise ValueError("AlpacaBroker mode must be 'paper' or 'live'.")
        self.mode = mode
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.base_url = os.getenv(
            "ALPACA_BASE_URL",
            "https://paper-api.alpaca.markets" if mode == "paper" else "https://api.alpaca.markets",
        )
        if not self.api_key or not self.secret_key:
            raise RuntimeError("Set ALPACA_API_KEY and ALPACA_SECRET_KEY before using Alpaca.")

    def submit_order(self, ticket: OrderTicket) -> ExecutionResult:
        try:
            import requests
        except ImportError as exc:
            raise RuntimeError("Install requests before using Alpaca execution.") from exc

        response = requests.post(
            f"{self.base_url}/v2/orders",
            headers={
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.secret_key,
                "Content-Type": "application/json",
            },
            json={
                "symbol": ticket.symbol,
                "side": ticket.side,
                "type": ticket.order_type,
                "time_in_force": ticket.time_in_force,
                "qty": str(ticket.quantity),
            },
            timeout=20,
        )
        if response.status_code >= 400:
            return ExecutionResult(
                ticket=ticket,
                mode=self.mode,
                status="rejected",
                message=f"Broker rejected order: {response.status_code} {response.text}",
            )
        return ExecutionResult(
            ticket=ticket,
            mode=self.mode,
            status="submitted",
            message=response.text,
        )


def build_broker(mode: ExecutionMode) -> BrokerClient:
    if mode == "dry-run":
        return DryRunBroker()
    if mode in {"paper", "live"}:
        return AlpacaBroker(mode)
    raise ValueError(f"Unsupported execution mode: {mode}")
