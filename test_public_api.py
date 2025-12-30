#!/usr/bin/env python3
"""
Quick test for public API endpoint (no credentials needed)
"""
from cryptocom_api import CryptocomExchangeAPI

print("=" * 60)
print("Testing Crypto.com Public API (No Credentials Required)")
print("=" * 60)

# Create client without credentials
client = CryptocomExchangeAPI()

print("\nTesting public endpoint: Get BTC/USDT price")
print("-" * 60)

try:
    ticker = client.get_ticker("BTC_USDT")
    price = float(ticker.get('a', 0))
    print(f"✅ SUCCESS!")
    print(f"   BTC/USDT Ask Price: ${price:,.2f}")
    print(f"   Full ticker data: {ticker}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
