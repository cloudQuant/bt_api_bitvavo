import hashlib
import hmac
import time
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient
from bt_api_base.logging_factory import get_logger

from bt_api_bitvavo.exchange_data import BitvavoExchangeDataSpot


class BitvavoRequestData(Feed):
    @classmethod
    def _capabilities(cls):
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any):
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "BITVAVO___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = BitvavoExchangeDataSpot()
        self._params.api_key = kwargs.get("public_key") or kwargs.get("api_key")
        self._params.api_secret = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret")
        )
        self.request_logger = get_logger("bitvavo_feed")
        self.async_logger = get_logger("bitvavo_feed")
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    def _generate_signature(self, timestamp: str, method: str, url_path: str, body: str = ""):
        secret = self._params.api_secret
        if not secret:
            return ""
        sign_str = timestamp + method.upper() + url_path + body
        signature = hmac.new(
            secret.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature

    def _get_headers(self, method: str, request_path: str, params=None, body=""):
        timestamp = str(int(time.time() * 1000))
        url_path = "/v2" + request_path
        if params and method == "GET":
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url_path = url_path + "?" + query
        body_str = body if body else ""

        headers = {
            "Content-Type": "application/json",
            "Bitvavo-Access-Key": self._params.api_key if self._params.api_key else "",
            "Bitvavo-Access-Signature": self._generate_signature(
                timestamp, method, url_path, body_str
            ),
            "Bitvavo-Access-Timestamp": timestamp,
            "Bitvavo-Access-Window": "10000",
        }
        return headers

    def request(self, path, params=None, body=None, extra_data=None, timeout=10):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path
        headers = self._get_headers(method, request_path, params, body)

        try:
            response = self._http_client.request(
                method=method,
                url=self._params.rest_url + request_path,
                headers=headers,
                json_data=body if method in ["POST", "PUT"] else None,
                params=params if method == "GET" else None,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.request_logger.error(f"Request failed: {e}")
            raise

    async def async_request(self, path, params=None, body=None, extra_data=None, timeout=5):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path
        headers = self._get_headers(method, request_path, params, body)

        try:
            response = await self._http_client.async_request(
                method=method,
                url=self._params.rest_url + request_path,
                headers=headers,
                json_data=body if method in ["POST", "PUT"] else None,
                params=params if method == "GET" else None,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.async_logger.error(f"Async request failed: {e}")
            raise

    def async_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.error(f"Async callback error: {e}")

    def _process_response(self, response, extra_data=None):
        if extra_data is None:
            extra_data = {}
        return RequestData(response, extra_data)

    def _get_server_time(self, extra_data=None, **kwargs):
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_server_time",
            }
        )
        return "GET /time", {}, extra_data

    def get_server_time(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_server_time(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def push_data_to_queue(self, data):
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self):
        pass

    def disconnect(self):
        super().disconnect()

    def is_connected(self):
        return True
