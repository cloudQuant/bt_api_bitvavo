from bt_api_base.balance_utils import simple_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_bitvavo.exchange_data import BitvavoExchangeDataSpot
from bt_api_bitvavo.feeds.live_bitvavo.spot import BitvavoRequestDataSpot


def register_bitvavo(
    registry: ExchangeRegistry | type[ExchangeRegistry] = ExchangeRegistry,
) -> None:
    registry.register_feed("BITVAVO___SPOT", BitvavoRequestDataSpot)
    registry.register_exchange_data("BITVAVO___SPOT", BitvavoExchangeDataSpot)
    registry.register_balance_handler("BITVAVO___SPOT", simple_balance_handler)
