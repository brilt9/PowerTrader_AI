"""
Crypto.com Exchange API Wrapper
"""

import os
import time
import hmac
import hashlib
import requests
import json
import uuid
from typing import List, Dict, Optional, Tuple


class CryptocomExchangeAPI:
    """Crypto.com Exchange API client."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 base_url: str = "https://api.crypto.com/exchange/v1", timeout: int = 10):
        self.api_key = (api_key or "").strip() if api_key else None
        self.api_secret = (api_secret or "").strip() if api_secret else None
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._request_id = 0

    def _get_request_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _get_timestamp(self) -> int:
        return int(time.time() * 1000)

    def _generate_signature(self, method: str, request_id: int, params: dict, nonce: int) -> str:
        if not self.api_secret:
            raise ValueError("API secret required")

        param_string = ""
        for key in sorted(params.keys()):
            param_string += str(key) + str(params[key])

        payload = f"{method}{request_id}{self.api_key}{param_string}{nonce}"

        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature

    def _make_request(self, method: str, params: dict = None, auth_required: bool = False) -> dict:
        url = f"{self.base_url}/{method}"

        if params is None:
            params = {}

        request_id = self._get_request_id()
        nonce = self._get_timestamp()

        request_body = {
            "id": request_id,
            "method": method,
            "nonce": nonce
        }

        if params:
            request_body["params"] = params

        if auth_required:
            if not self.api_key or not self.api_secret:
                raise ValueError("API credentials required for authenticated endpoints")

            request_body["api_key"] = self.api_key
            request_body["sig"] = self._generate_signature(method, request_id, params, nonce)

        try:
            response = self.session.post(url, json=request_body, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != 0:
                error_msg = data.get("message", "Unknown error")
                raise RuntimeError(f"API error ({data.get('code')}): {error_msg}")

            return data

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid response: {e}")

    def get_ticker(self, instrument_name: str) -> dict:
        instrument_name = self._format_symbol(instrument_name)
        params = {"instrument_name": instrument_name}
        response = self._make_request("public/get-ticker", params)

        result = response.get("result", {}).get("data", [])
        if not result:
            raise RuntimeError(f"No ticker data for {instrument_name}")

        return result[0]

    def get_candlestick(self, instrument_name: str, timeframe: str, count: int = 300) -> List[dict]:
        instrument_name = self._format_symbol(instrument_name)
        timeframe = self._map_timeframe(timeframe)

        params = {
            "instrument_name": instrument_name,
            "timeframe": timeframe,
            "count": min(count, 300)
        }

        response = self._make_request("public/get-candlestick", params)
        return response.get("result", {}).get("data", [])

    def get_book(self, instrument_name: str, depth: int = 10) -> dict:
        instrument_name = self._format_symbol(instrument_name)

        params = {
            "instrument_name": instrument_name,
            "depth": min(depth, 50)
        }

        response = self._make_request("public/get-book", params)
        result = response.get("result", {}).get("data", [])

        if not result:
            return {"bids": [], "asks": []}

        return result[0]

    def get_current_ask(self, instrument_name: str) -> float:
        ticker = self.get_ticker(instrument_name)
        ask_price = float(ticker.get("a", 0.0))

        if ask_price <= 0:
            book = self.get_book(instrument_name, depth=1)
            asks = book.get("asks", [])
            if asks:
                ask_price = float(asks[0][0])

        if ask_price <= 0:
            raise RuntimeError(f"Invalid ask price for {instrument_name}")

        return ask_price

    def get_current_bid(self, instrument_name: str) -> float:
        ticker = self.get_ticker(instrument_name)
        bid_price = float(ticker.get("b", 0.0))

        if bid_price <= 0:
            book = self.get_book(instrument_name, depth=1)
            bids = book.get("bids", [])
            if bids:
                bid_price = float(bids[0][0])

        if bid_price <= 0:
            raise RuntimeError(f"Invalid bid price for {instrument_name}")

        return bid_price

    def get_account_summary(self) -> dict:
        response = self._make_request("private/get-account-summary", {}, auth_required=True)
        return response.get("result", {})

    def create_order(self, instrument_name: str, side: str, type: str,
                     quantity: Optional[float] = None, notional: Optional[float] = None,
                     price: Optional[float] = None, time_in_force: str = "GOOD_TILL_CANCEL",
                     client_oid: Optional[str] = None) -> dict:
        instrument_name = self._format_symbol(instrument_name)

        params = {
            "instrument_name": instrument_name,
            "side": side.upper(),
            "type": type.upper(),
            "time_in_force": time_in_force
        }

        if quantity is not None:
            params["quantity"] = f"{quantity:.8f}".rstrip('0').rstrip('.')

        if notional is not None:
            params["notional"] = f"{notional:.2f}"

        if price is not None:
            params["price"] = f"{price:.8f}".rstrip('0').rstrip('.')

        if client_oid:
            params["client_oid"] = client_oid
        else:
            params["client_oid"] = str(uuid.uuid4())

        response = self._make_request("private/create-order", params, auth_required=True)
        return response.get("result", {})

    def cancel_order(self, order_id: str, instrument_name: str) -> dict:
        instrument_name = self._format_symbol(instrument_name)

        params = {
            "instrument_name": instrument_name,
            "order_id": str(order_id)
        }

        response = self._make_request("private/cancel-order", params, auth_required=True)
        return response.get("result", {})

    def get_order_detail(self, order_id: str) -> dict:
        params = {"order_id": str(order_id)}
        response = self._make_request("private/get-order-detail", params, auth_required=True)
        return response.get("result", {})

    def get_order_history(self, instrument_name: Optional[str] = None,
                          page_size: int = 20, page: int = 0) -> dict:
        params = {
            "page_size": min(page_size, 200),
            "page": page
        }

        if instrument_name:
            params["instrument_name"] = self._format_symbol(instrument_name)

        response = self._make_request("private/get-order-history", params, auth_required=True)
        return response.get("result", {})

    def get_trades(self, instrument_name: Optional[str] = None,
                   page_size: int = 20, page: int = 0) -> dict:
        params = {
            "page_size": min(page_size, 200),
            "page": page
        }

        if instrument_name:
            params["instrument_name"] = self._format_symbol(instrument_name)

        response = self._make_request("private/get-trades", params, auth_required=True)
        return response.get("result", {})

    @staticmethod
    def _format_symbol(symbol: str) -> str:
        symbol = symbol.upper().strip()
        symbol = symbol.replace("-", "_")

        if symbol.endswith("_USD") and not symbol.endswith("_USDT"):
            symbol = symbol.replace("_USD", "_USDT")

        return symbol

    @staticmethod
    def _map_timeframe(timeframe: str) -> str:
        timeframe_map = {
            "1min": "1m", "5min": "5m", "15min": "15m", "30min": "30m",
            "1hour": "1h", "2hour": "2h", "4hour": "4h", "6hour": "6h",
            "8hour": "8h", "12hour": "12h",
            "1day": "1D", "1week": "7D", "1month": "1M",
        }
        return timeframe_map.get(timeframe, timeframe)

    @staticmethod
    def load_credentials(key_file: str = "crypto_key.txt", secret_file: str = "crypto_secret.txt") -> Tuple[Optional[str], Optional[str]]:
        try:
            if os.path.isfile(key_file) and os.path.isfile(secret_file):
                with open(key_file, "r", encoding="utf-8") as f:
                    api_key = f.read().strip()
                with open(secret_file, "r", encoding="utf-8") as f:
                    api_secret = f.read().strip()
                return (api_key, api_secret)
        except Exception:
            pass
        return (None, None)


_global_client = None


def get_client(api_key: Optional[str] = None, api_secret: Optional[str] = None) -> CryptocomExchangeAPI:
    global _global_client

    if _global_client is None:
        if api_key is None or api_secret is None:
            file_key, file_secret = CryptocomExchangeAPI.load_credentials()
            api_key = api_key or file_key
            api_secret = api_secret or file_secret

        _global_client = CryptocomExchangeAPI(api_key=api_key, api_secret=api_secret)

    return _global_client


def get_klines_compat(symbol: str, timeframe: str, **kwargs) -> List[List]:
    client = get_client()
    data = client.get_candlestick(symbol, timeframe)

    result = []
    for candle in data:
        result.append([
            candle.get("t", 0),
            str(candle.get("o", 0)),
            str(candle.get("c", 0)),
            str(candle.get("h", 0)),
            str(candle.get("l", 0)),
            str(candle.get("v", 0)),
            "0"
        ])

    return result


if __name__ == "__main__":
    print("Testing Crypto.com API connection...")
    print("=" * 50)

    client = get_client()

    try:
        ticker = client.get_ticker("BTC_USDT")
        print(f"BTC/USDT price: ${float(ticker.get('a', 0)):,.2f}")
        print("Connection successful")
    except Exception as e:
        print(f"Error: {e}")
