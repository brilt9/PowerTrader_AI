#!/usr/bin/env python3
"""
Test public API endpoint (no credentials required)
"""
from cryptocom_api import CryptocomExchangeAPI

print("=" * 60)
print("Testing Crypto.com Public API")
print("=" * 60)

client = CryptocomExchangeAPI()

print("\nGetting BTC/USDT price...")
print("-" * 60)

try:
    ticker = client.get_ticker("BTC_USDT")
    price = float(ticker.get('a', 0))
    print(f"BTC/USDT Ask Price: ${price:,.2f}")
    print(f"Ticker data: {ticker}")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
