"""
Crypto.com Exchange API Wrapper for PowerTrader_AI
Replaces KuCoin and Robinhood APIs with Crypto.com Exchange API

Documentation: https://exchange-docs.crypto.com/exchange/v1/rest-ws/index.html
"""

import os
import time
import hmac
import hashlib
import requests
import json
from typing import List, Dict, Optional, Tuple


class CryptocomExchangeAPI:
    """
    Crypto.com Exchange API client for market data and trading.

    Public endpoints (no auth required):
    - Market data, tickers, candles, order book

    Private endpoints (auth required):
    - Trading, account balance, order history
    """

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 base_url: str = "https://api.crypto.com/exchange/v1", timeout: int = 10):
        """
        Initialize Crypto.com API client.

        Args:
            api_key: API key from Crypto.com Exchange (optional for public endpoints)
            api_secret: API secret key (optional for public endpoints)
            base_url: API base URL
            timeout: Request timeout in seconds
        """
        self.api_key = (api_key or "").strip() if api_key else None
        self.api_secret = (api_secret or "").strip() if api_secret else None
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    @staticmethod
    def load_credentials(key_file: str = "crypto_key.txt", secret_file: str = "crypto_secret.txt") -> Tuple[Optional[str], Optional[str]]:
        """
        Load API credentials from files.

        Returns:
            (api_key, api_secret) or (None, None) if files don't exist
        """
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

    def _get_timestamp(self) -> int:
        """Get current timestamp in milliseconds."""
        return int(time.time() * 1000)

    def _generate_signature(self, params: dict) -> str:
        """
        Generate HMAC SHA-256 signature for authenticated requests.

        Args:
            params: Request parameters including nonce

        Returns:
            Hexadecimal signature string
        """
        if not self.api_secret:
            raise ValueError("API secret required for signature generation")

        # Create parameter string (sorted alphabetically)
        param_string = ""
        for key in sorted(params.keys()):
            param_string += str(key) + str(params[key])

        # Generate HMAC signature
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            param_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature

    def _make_request(self, method: str, endpoint: str, params: dict = None, auth_required: bool = False) -> dict:
        """
        Make HTTP request to Crypto.com Exchange API.

        Args:
            method: HTTP method (GET or POST)
            endpoint: API endpoint (e.g., "public/get-ticker")
            params: Request parameters
            auth_required: Whether authentication is required

        Returns:
            API response as dictionary

        Raises:
            RuntimeError: If request fails or API returns error
        """
        url = f"{self.base_url}/{endpoint}"

        if params is None:
            params = {}

        # Add request metadata for authenticated requests
        if auth_required:
            if not self.api_key or not self.api_secret:
                raise ValueError("API credentials required for authenticated endpoints")

            nonce = self._get_timestamp()
            params["nonce"] = nonce
            params["api_key"] = self.api_key
            params["sig"] = self._generate_signature(params)

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=self.timeout)
            else:
                response = self.session.post(url, json=params, timeout=self.timeout)

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

    # ====== PUBLIC MARKET DATA ENDPOINTS (NO AUTH REQUIRED) ======

    def get_ticker(self, instrument_name: str) -> dict:
        """
        Get current ticker for an instrument.

        Args:
            instrument_name: Trading pair (e.g., "BTC_USDT")

        Returns:
            Ticker data with bid, ask, last price, volume, etc.
        """
        instrument_name = self._format_symbol(instrument_name)

        response = self._make_request("GET", "public/get-ticker", {
            "instrument_name": instrument_name
        })

        result = response.get("result", {}).get("data", [])
        if not result:
            raise RuntimeError(f"No ticker data for {instrument_name}")

        return result[0]

    def get_candlestick(self, instrument_name: str, timeframe: str, count: int = 300) -> List[dict]:
        """
        Get candlestick/kline data.

        Args:
            instrument_name: Trading pair (e.g., "BTC_USDT")
            timeframe: Candlestick period (1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1D, 7D, 14D, 1M)
            count: Number of candlesticks (max 300)

        Returns:
            List of candlestick data: [{"t": timestamp, "o": open, "h": high, "l": low, "c": close, "v": volume}, ...]
        """
        instrument_name = self._format_symbol(instrument_name)
        timeframe = self._map_timeframe(timeframe)

        response = self._make_request("GET", "public/get-candlestick", {
            "instrument_name": instrument_name,
            "timeframe": timeframe,
            "count": min(count, 300)  # API limit is 300
        })

        data = response.get("result", {}).get("data", [])
        return data

    def get_book(self, instrument_name: str, depth: int = 10) -> dict:
        """
        Get order book (bids and asks).

        Args:
            instrument_name: Trading pair (e.g., "BTC_USDT")
            depth: Number of price levels (max 50)

        Returns:
            Order book with bids and asks
        """
        instrument_name = self._format_symbol(instrument_name)

        response = self._make_request("GET", "public/get-book", {
            "instrument_name": instrument_name,
            "depth": min(depth, 50)
        })

        result = response.get("result", {}).get("data", [])
        if not result:
            return {"bids": [], "asks": []}

        return result[0]

    def get_current_ask(self, instrument_name: str) -> float:
        """
        Get current ASK price (buy price).

        Args:
            instrument_name: Trading pair (e.g., "BTC_USDT")

        Returns:
            Current ask price as float
        """
        ticker = self.get_ticker(instrument_name)
        ask_price = float(ticker.get("a", 0.0))

        if ask_price <= 0:
            # Fallback to order book if ticker ask is invalid
            book = self.get_book(instrument_name, depth=1)
            asks = book.get("asks", [])
            if asks:
                ask_price = float(asks[0][0])

        if ask_price <= 0:
            raise RuntimeError(f"Invalid ask price for {instrument_name}")

        return ask_price

    def get_current_bid(self, instrument_name: str) -> float:
        """
        Get current BID price (sell price).

        Args:
            instrument_name: Trading pair (e.g., "BTC_USDT")

        Returns:
            Current bid price as float
        """
        ticker = self.get_ticker(instrument_name)
        bid_price = float(ticker.get("b", 0.0))

        if bid_price <= 0:
            # Fallback to order book if ticker bid is invalid
            book = self.get_book(instrument_name, depth=1)
            bids = book.get("bids", [])
            if bids:
                bid_price = float(bids[0][0])

        if bid_price <= 0:
            raise RuntimeError(f"Invalid bid price for {instrument_name}")

        return bid_price

    # ====== PRIVATE TRADING ENDPOINTS (AUTH REQUIRED) ======

    def get_account_summary(self) -> dict:
        """
        Get account balance and positions.

        Returns:
            Account summary with balances
        """
        response = self._make_request("POST", "private/get-account-summary", auth_required=True)
        return response.get("result", {})

    def create_order(self, instrument_name: str, side: str, type: str,
                     quantity: Optional[float] = None, notional: Optional[float] = None,
                     price: Optional[float] = None, time_in_force: str = "GOOD_TILL_CANCEL") -> dict:
        """
        Create a new order.

        Args:
            instrument_name: Trading pair (e.g., "BTC_USDT")
            side: "BUY" or "SELL"
            type: "LIMIT", "MARKET", "STOP_LOSS", "STOP_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT"
            quantity: Order quantity in base currency (for LIMIT/STOP orders)
            notional: Order amount in quote currency (for MARKET orders in quote currency)
            price: Limit price (for LIMIT/STOP_LIMIT/TAKE_PROFIT_LIMIT orders)
            time_in_force: "GOOD_TILL_CANCEL", "FILL_OR_KILL", "IMMEDIATE_OR_CANCEL"

        Returns:
            Order confirmation with order_id
        """
        instrument_name = self._format_symbol(instrument_name)

        params = {
            "instrument_name": instrument_name,
            "side": side.upper(),
            "type": type.upper(),
            "time_in_force": time_in_force
        }

        if quantity is not None:
            params["quantity"] = str(quantity)

        if notional is not None:
            params["notional"] = str(notional)

        if price is not None:
            params["price"] = str(price)

        response = self._make_request("POST", "private/create-order", params, auth_required=True)
        return response.get("result", {})

    def cancel_order(self, order_id: str, instrument_name: str) -> dict:
        """
        Cancel an open order.

        Args:
            order_id: Order ID to cancel
            instrument_name: Trading pair (e.g., "BTC_USDT")

        Returns:
            Cancellation confirmation
        """
        instrument_name = self._format_symbol(instrument_name)

        params = {
            "instrument_name": instrument_name,
            "order_id": order_id
        }

        response = self._make_request("POST", "private/cancel-order", params, auth_required=True)
        return response.get("result", {})

    def get_order_detail(self, order_id: str) -> dict:
        """
        Get details of a specific order.

        Args:
            order_id: Order ID

        Returns:
            Order details
        """
        params = {"order_id": order_id}
        response = self._make_request("POST", "private/get-order-detail", params, auth_required=True)
        return response.get("result", {})

    def get_order_history(self, instrument_name: Optional[str] = None,
                          page_size: int = 20, page: int = 0) -> dict:
        """
        Get order history.

        Args:
            instrument_name: Trading pair (optional filter)
            page_size: Results per page (max 200)
            page: Page number (0-indexed)

        Returns:
            Order history
        """
        params = {
            "page_size": min(page_size, 200),
            "page": page
        }

        if instrument_name:
            params["instrument_name"] = self._format_symbol(instrument_name)

        response = self._make_request("POST", "private/get-order-history", params, auth_required=True)
        return response.get("result", {})

    def get_trades(self, instrument_name: Optional[str] = None,
                   page_size: int = 20, page: int = 0) -> dict:
        """
        Get trade history.

        Args:
            instrument_name: Trading pair (optional filter)
            page_size: Results per page (max 200)
            page: Page number (0-indexed)

        Returns:
            Trade history
        """
        params = {
            "page_size": min(page_size, 200),
            "page": page
        }

        if instrument_name:
            params["instrument_name"] = self._format_symbol(instrument_name)

        response = self._make_request("POST", "private/get-trades", params, auth_required=True)
        return response.get("result", {})

    # ====== HELPER METHODS ======

    @staticmethod
    def _format_symbol(symbol: str) -> str:
        """
        Convert symbol to Crypto.com format.

        Args:
            symbol: Symbol in various formats (BTC-USDT, BTC-USD, BTC_USDT)

        Returns:
            Symbol in Crypto.com format (BTC_USDT)
        """
        symbol = symbol.upper().strip()

        # Replace hyphens with underscores
        symbol = symbol.replace("-", "_")

        # Replace USD with USDT if needed (Crypto.com uses USDT pairs)
        if symbol.endswith("_USD") and not symbol.endswith("_USDT"):
            symbol = symbol.replace("_USD", "_USDT")

        return symbol

    @staticmethod
    def _map_timeframe(timeframe: str) -> str:
        """
        Map PowerTrader timeframes to Crypto.com format.

        Args:
            timeframe: PowerTrader timeframe (1hour, 1day, etc.)

        Returns:
            Crypto.com timeframe (1h, 1D, etc.)
        """
        timeframe_map = {
            "1min": "1m",
            "5min": "5m",
            "15min": "15m",
            "30min": "30m",
            "1hour": "1h",
            "2hour": "2h",
            "4hour": "4h",
            "6hour": "6h",
            "8hour": "8h",
            "12hour": "12h",
            "1day": "1D",
            "1week": "7D",
            "1month": "1M",
        }

        return timeframe_map.get(timeframe, timeframe)


# ====== CONVENIENCE FUNCTIONS ======

_global_client = None


def get_client(api_key: Optional[str] = None, api_secret: Optional[str] = None) -> CryptocomExchangeAPI:
    """
    Get global Crypto.com API client (singleton pattern).

    Args:
        api_key: API key (optional, will auto-load from files)
        api_secret: API secret (optional, will auto-load from files)

    Returns:
        CryptocomExchangeAPI client instance
    """
    global _global_client

    if _global_client is None:
        # Try to load credentials from files if not provided
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
        **kwargs: Additional parameters

    Returns:
        List of candles: [[timestamp, open, close, high, low, volume], ...]
    """
    client = get_client()
    data = client.get_candlestick(symbol, timeframe)

    # Convert to KuCoin format: [time, open, close, high, low, volume, turnover]
    result = []
    for candle in data:
        result.append([
            candle.get("t", 0),           # timestamp
            str(candle.get("o", 0)),      # open
            str(candle.get("c", 0)),      # close
            str(candle.get("h", 0)),      # high
            str(candle.get("l", 0)),      # low
            str(candle.get("v", 0)),      # volume
            "0"                           # turnover (not provided by Crypto.com)
        ])

    return result


if __name__ == "__main__":
    # Example usage
    print("Crypto.com Exchange API Wrapper")
    print("=" * 50)

    # Initialize client (will auto-load credentials from files if available)
    client = get_client()

    try:
        # Test public endpoint (no auth required)
        print("\n1. Getting BTC_USDT ticker...")
        ticker = client.get_ticker("BTC_USDT")
        print(f"   Last price: ${float(ticker.get('a', 0)):,.2f}")
        print(f"   24h volume: {float(ticker.get('v', 0)):,.2f}")

        # Test candlestick data
        print("\n2. Getting BTC_USDT hourly candles...")
        candles = client.get_candlestick("BTC_USDT", "1h", count=5)
        print(f"   Retrieved {len(candles)} candles")
        if candles:
            latest = candles[-1]
            print(f"   Latest candle: O=${latest['o']} H=${latest['h']} L=${latest['l']} C=${latest['c']}")

        print("\n✅ API connection successful!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: For trading endpoints, you need to create crypto_key.txt and crypto_secret.txt files")
