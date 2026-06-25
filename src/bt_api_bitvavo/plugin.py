from __future__ import annotations

from typing import Any

from bt_api_base.balance_utils import simple_balance_handler
from bt_api_base.plugins.protocol import PluginInfo

from bt_api_bitvavo.exchange_data import BitvavoExchangeDataSpot
from bt_api_bitvavo.feeds.live_bitvavo.spot import BitvavoRequestDataSpot

PLUGIN_INFO = PluginInfo(
    name="bt_api_bitvavo",
    version="0.1.0",
    core_requires=">=0.15,<1.0",
    supported_exchanges=("BITVAVO___SPOT",),
    supported_asset_types=("SPOT",),
)


def register_plugin(registry: Any, runtime_factory: Any | None = None) -> PluginInfo:
    registry.register_feed("BITVAVO___SPOT", BitvavoRequestDataSpot)
    registry.register_exchange_data("BITVAVO___SPOT", BitvavoExchangeDataSpot)
    registry.register_balance_handler("BITVAVO___SPOT", simple_balance_handler)
    return PLUGIN_INFO
