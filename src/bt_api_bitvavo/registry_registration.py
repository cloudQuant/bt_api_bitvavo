from bt_api_base.balance_utils import simple_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_bitvavo.exchange_data import BitvavoExchangeDataSpot
from bt_api_bitvavo.feeds.live_bitvavo.spot import BitvavoRequestDataSpot


def register_bitvavo():
    ExchangeRegistry.register_feed("BITVAVO___SPOT", BitvavoRequestDataSpot)
    ExchangeRegistry.register_exchange_data("BITVAVO___SPOT", BitvavoExchangeDataSpot)
    ExchangeRegistry.register_balance_handler("BITVAVO___SPOT", simple_balance_handler)


register_bitvavo()
