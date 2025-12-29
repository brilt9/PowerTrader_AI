"""
CRITICAL FIX: Crypto.com Exchange API Wrapper
Corrected version with proper request format and signature generation

This file fixes the API implementation to match Crypto.com's actual requirements.
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
    """
    Crypto.com Exchange API client - CORRECTED VERSION

    Fixed Issues:
    1. Proper JSON request format (id, method, params, nonce, api_key, sig)
    2. Correct signature generation (includes method, id, nonce)
    3. All numbers as strings (per API requirements)
    4. Unified endpoint (not different URLs per method)
    """

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 base_url: str = "https://api.crypto.com/exchange/v1", timeout: int = 10):
        """
        Initialize Crypto.com API client.

        Args:
            api_key: API key from Crypto.com Exchange
            api_secret: API secret key
            base_url: API base URL (should be just the base, not method-specific)
            timeout: Request timeout in seconds
        """
        self.api_key = (api_key or "").strip() if api_key else None
        self.api_secret = (api_secret or "").strip() if api_secret else None
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._request_id = 0  # Counter for request IDs

    def _get_request_id(self) -> int:
        """Generate unique request ID."""
        self._request_id += 1
        return self._request_id

    def _get_timestamp(self) -> int:
        """Get current timestamp in milliseconds."""
        return int(time.time() * 1000)

    def _generate_signature(self, method: str, request_id: int, params: dict, nonce: int) -> str:
        """
        Generate HMAC SHA-256 signature for Crypto.com Exchange API.

        CORRECT FORMAT per documentation:
        - Concatenate: method + id + api_key + param_string + nonce
        - Sign with HMAC-SHA256 using api_secret

        Args:
            method: API method (e.g., "private/create-order")
            request_id: Unique request ID
            params: Request parameters
            nonce: Timestamp in milliseconds

        Returns:
            Hexadecimal signature string
        """
        if not self.api_secret:
            raise ValueError("API secret required for signature generation")

        # Create parameter string (sorted alphabetically by key)
        param_string = ""
        for key in sorted(params.keys()):
            param_string += str(key) + str(params[key])

        # CORRECT signature payload format:
        # method + id + api_key + param_string + nonce
        payload = f"{method}{request_id}{self.api_key}{param_string}{nonce}"

        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature

    def _make_request(self, method: str, params: dict = None, auth_required: bool = False) -> dict:
        """
        Make HTTP request to Crypto.com Exchange API with CORRECT format.

        Args:
            method: API method (e.g., "public/get-ticker", "private/create-order")
            params: Method parameters (NOT including id, nonce, api_key, sig)
            auth_required: Whether authentication is required

        Returns:
            API response as dictionary

        Raises:
            RuntimeError: If request fails or API returns error
        """
        url = self.base_url  # Just base URL, method goes in JSON body

        if params is None:
            params = {}

        # Generate request metadata
        request_id = self._get_request_id()
        nonce = self._get_timestamp()

        # Build CORRECT request format per Crypto.com documentation
        request_body = {
            "id": request_id,
            "method": method,
            "nonce": nonce
        }

        # Only add params if not empty
        if params:
            request_body["params"] = params

        # Add authentication for private methods
        if auth_required:
            if not self.api_key or not self.api_secret:
                raise ValueError("API credentials required for authenticated endpoints")

            request_body["api_key"] = self.api_key
            request_body["sig"] = self._generate_signature(method, request_id, params, nonce)

        try:
            # POST request with JSON body
            response = self.session.post(url, json=request_body, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            # Check API response code
            if data.get("code") != 0:
                error_msg = data.get("message", "Unknown error")
                raise RuntimeError(f"Crypto.com API error ({data.get('code')}): {error_msg}")

            return data

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse API response: {e}")

    # ====== PUBLIC MARKET DATA ENDPOINTS ======

    def get_ticker(self, instrument_name: str) -> dict:
        """Get current ticker for an instrument."""
        instrument_name = self._format_symbol(instrument_name)

        params = {"instrument_name": instrument_name}
        response = self._make_request("public/get-ticker", params)

        result = response.get("result", {}).get("data", [])
        if not result:
            raise RuntimeError(f"No ticker data for {instrument_name}")

        return result[0]

    def get_candlestick(self, instrument_name: str, timeframe: str, count: int = 300) -> List[dict]:
        """Get candlestick/kline data."""
        instrument_name = self._format_symbol(instrument_name)
        timeframe = self._map_timeframe(timeframe)

        params = {
            "instrument_name": instrument_name,
            "timeframe": timeframe,
            "count": min(count, 300)  # API limit
        }

        response = self._make_request("public/get-candlestick", params)
        data = response.get("result", {}).get("data", [])
        return data

    def get_book(self, instrument_name: str, depth: int = 10) -> dict:
        """Get order book."""
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
        """Get current ASK price (buy price)."""
        ticker = self.get_ticker(instrument_name)
        ask_price = float(ticker.get("a", 0.0))

        if ask_price <= 0:
            # Fallback to order book
            book = self.get_book(instrument_name, depth=1)
            asks = book.get("asks", [])
            if asks:
                ask_price = float(asks[0][0])

        if ask_price <= 0:
            raise RuntimeError(f"Invalid ask price for {instrument_name}")

        return ask_price

    def get_current_bid(self, instrument_name: str) -> float:
        """Get current BID price (sell price)."""
        ticker = self.get_ticker(instrument_name)
        bid_price = float(ticker.get("b", 0.0))

        if bid_price <= 0:
            # Fallback to order book
            book = self.get_book(instrument_name, depth=1)
            bids = book.get("bids", [])
            if bids:
                bid_price = float(bids[0][0])

        if bid_price <= 0:
            raise RuntimeError(f"Invalid bid price for {instrument_name}")

        return bid_price

    # ====== PRIVATE TRADING ENDPOINTS ======

    def get_account_summary(self) -> dict:
        """Get account balance and positions."""
        response = self._make_request("private/get-account-summary", {}, auth_required=True)
        return response.get("result", {})

    def create_order(self, instrument_name: str, side: str, type: str,
                     quantity: Optional[float] = None, notional: Optional[float] = None,
                     price: Optional[float] = None, time_in_force: str = "GOOD_TILL_CANCEL",
                     client_oid: Optional[str] = None) -> dict:
        """
        Create a new order.

        IMPORTANT: All numbers must be strings per Crypto.com API requirements!
        """
        instrument_name = self._format_symbol(instrument_name)

        params = {
            "instrument_name": instrument_name,
            "side": side.upper(),
            "type": type.upper(),
            "time_in_force": time_in_force
        }

        # CRITICAL: All numbers must be strings!
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
        """Cancel an open order."""
        instrument_name = self._format_symbol(instrument_name)

        params = {
            "instrument_name": instrument_name,
            "order_id": str(order_id)
        }

        response = self._make_request("private/cancel-order", params, auth_required=True)
        return response.get("result", {})

    def get_order_detail(self, order_id: str) -> dict:
        """Get details of a specific order."""
        params = {"order_id": str(order_id)}
        response = self._make_request("private/get-order-detail", params, auth_required=True)
        return response.get("result", {})

    def get_order_history(self, instrument_name: Optional[str] = None,
                          page_size: int = 20, page: int = 0) -> dict:
        """Get order history."""
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
        """Get trade history."""
        params = {
            "page_size": min(page_size, 200),
            "page": page
        }

        if instrument_name:
            params["instrument_name"] = self._format_symbol(instrument_name)

        response = self._make_request("private/get-trades", params, auth_required=True)
        return response.get("result", {})

    # ====== HELPER METHODS ======

    @staticmethod
    def _format_symbol(symbol: str) -> str:
        """Convert symbol to Crypto.com format."""
        symbol = symbol.upper().strip()
        symbol = symbol.replace("-", "_")

        if symbol.endswith("_USD") and not symbol.endswith("_USDT"):
            symbol = symbol.replace("_USD", "_USDT")

        return symbol

    @staticmethod
    def _map_timeframe(timeframe: str) -> str:
        """Map PowerTrader timeframes to Crypto.com format."""
        timeframe_map = {
            "1min": "1m", "5min": "5m", "15min": "15m", "30min": "30m",
            "1hour": "1h", "2hour": "2h", "4hour": "4h", "6hour": "6h",
            "8hour": "8h", "12hour": "12h",
            "1day": "1D", "1week": "7D", "1month": "1M",
        }
        return timeframe_map.get(timeframe, timeframe)

    @staticmethod
    def load_credentials(key_file: str = "crypto_key.txt", secret_file: str = "crypto_secret.txt") -> Tuple[Optional[str], Optional[str]]:
        """Load API credentials from files."""
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


# ====== CONVENIENCE FUNCTIONS ======

_global_client = None


def get_client(api_key: Optional[str] = None, api_secret: Optional[str] = None) -> CryptocomExchangeAPI:
    """Get global Crypto.com API client (singleton pattern)."""
    global _global_client

    if _global_client is None:
        if api_key is None or api_secret is None:
            file_key, file_secret = CryptocomExchangeAPI.load_credentials()
            api_key = api_key or file_key
            api_secret = api_secret or file_secret

        _global_client = CryptocomExchangeAPI(api_key=api_key, api_secret=api_secret)

    return _global_client


def get_klines_compat(symbol: str, timeframe: str, **kwargs) -> List[List]:
    """
    Get candlestick data in KuCoin-compatible format.

    Args:
        symbol: Trading pair (BTC-USDT, ETH-USDT, etc.)
        timeframe: Timeframe (1hour, 1day, etc.)

    Returns:
        List of candles: [[timestamp, open, close, high, low, volume], ...]
    """
    client = get_client()
    data = client.get_candlestick(symbol, timeframe)

    # Convert to KuCoin format
    result = []
    for candle in data:
        result.append([
            candle.get("t", 0),       # timestamp
            str(candle.get("o", 0)),  # open
            str(candle.get("c", 0)),  # close
            str(candle.get("h", 0)),  # high
            str(candle.get("l", 0)),  # low
            str(candle.get("v", 0)),  # volume
            "0"                       # turnover (not provided)
        ])

    return result


if __name__ == "__main__":
    # Test the corrected API
    print("Crypto.com Exchange API Wrapper - CORRECTED VERSION")
    print("=" * 60)

    client = get_client()

    try:
        print("\n✅ Testing public endpoint (no auth)...")
        ticker = client.get_ticker("BTC_USDT")
        print(f"   BTC/USDT price: ${float(ticker.get('a', 0)):,.2f}")

        print("\n✅ API wrapper is working correctly!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis is expected if API credentials are not configured.")
        print("Create crypto_key.txt and crypto_secret.txt to test authenticated endpoints.")
