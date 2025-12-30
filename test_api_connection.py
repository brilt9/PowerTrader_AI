#!/usr/bin/env python3
"""
Test script for Crypto.com API connection
"""
from cryptocom_api import CryptocomExchangeAPI

print("=" * 60)
print("Crypto.com API Connection Test")
print("=" * 60)

api_key, api_secret = CryptocomExchangeAPI.load_credentials()

if not api_key or not api_secret:
    print("\nAPI credentials not found!")
    print("\nCreate these files:")
    print("  1. crypto_key.txt    (paste your API key)")
    print("  2. crypto_secret.txt (paste your secret key)")
    exit(1)

print(f"\nAPI Key: {api_key[:8]}...{api_key[-4:]}")
print("Secret Key: (hidden)")

client = CryptocomExchangeAPI(api_key=api_key, api_secret=api_secret)

print("\n" + "-" * 60)
print("TEST 1: Public API (Get BTC price)")
print("-" * 60)
try:
    ticker = client.get_ticker("BTC_USDT")
    price = float(ticker.get('a', 0))
    print(f"BTC/USDT price: ${price:,.2f}")
except Exception as e:
    print(f"Failed: {e}")

print("\n" + "-" * 60)
print("TEST 2: Private API (Get Account)")
print("-" * 60)
try:
    account = client.get_account_summary()
    print("Connected to account successfully")
    print(f"Response: {account}")
except Exception as e:
    print(f"Failed: {e}")
    print("\nCommon issues:")
    print("  1. IP not whitelisted in Crypto.com Exchange")
    print("  2. API key missing 'Read' permission")
    print("  3. Incorrect credentials")

print("\n" + "=" * 60)
