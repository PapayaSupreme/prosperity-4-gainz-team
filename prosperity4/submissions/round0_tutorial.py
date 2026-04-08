import json
from typing import Any

from datamodel import Order, ProsperityEncoder, Symbol, TradingState


class Logger:
    def __init__(self) -> None:
        self.logs = ""
        self.max_log_length = 3750

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]], conversions: int, trader_data: str) -> None:
        payload = [
            [
                state.timestamp,
                state.traderData,
                [[l.symbol, l.product, l.denomination] for l in state.listings.values()],
                {s: [d.buy_orders, d.sell_orders] for s, d in state.order_depths.items()},
                [],
                [],
                state.position,
                [state.observations.plainValueObservations, {}],
            ],
            [[o.symbol, o.price, o.quantity] for arr in orders.values() for o in arr],
            conversions,
            trader_data,
            self.logs,
        ]
        print(json.dumps(payload, cls=ProsperityEncoder, separators=(",", ":")))
        self.logs = ""


logger = Logger()


class Trader:
    """
    Submission template for tutorial round.
    Keep `run` for website compatibility.
    """

    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        orders: dict[Symbol, list[Order]] = {}
        conversions = 0
        trader_data = ""

        logger.flush(state, orders, conversions, trader_data)
        return orders, conversions, trader_data
