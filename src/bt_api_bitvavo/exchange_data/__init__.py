from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BitvavoExchangeData(ExchangeData):
    def __init__(self):
        super().__init__()
        self.exchange_name = "BITVAVO___SPOT"
        self.rest_url = "https://api.bitvavo.com/v2"
        self.wss_url = "wss://ws.bitvavo.com/v2/"
        self.rest_paths = {}
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "2h": "2h",
            "4h": "4h",
            "6h": "6h",
            "8h": "8h",
            "12h": "12h",
            "1d": "1d",
        }
        self.legal_currency = ["EUR", "USDT", "USD"]

    def get_symbol(self, symbol):
        return symbol.upper()

    def get_period(self, period):
        return self.kline_periods.get(period, period)


class BitvavoExchangeDataSpot(BitvavoExchangeData):
    def __init__(self):
        super().__init__()
        self.asset_type = "spot"
        self.exchange_name = "BITVAVO___SPOT"
        self.rest_url = "https://api.bitvavo.com/v2"
        self.rest_paths = {}


__all__ = ["BitvavoExchangeData", "BitvavoExchangeDataSpot"]
