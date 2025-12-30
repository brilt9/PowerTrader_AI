#!/usr/bin/env python3
"""
Quick test script to verify Crypto.com API connection
"""
from cryptocom_api import CryptocomExchangeAPI

print("=" * 60)
print("Crypto.com API Connection Test")
print("=" * 60)

# Try to load credentials
api_key, api_secret = CryptocomExchangeAPI.load_credentials()

if not api_key or not api_secret:
    print("\n❌ ERROR: API credentials not found!")
    print("\nPlease create these files:")
    print("  1. crypto_key.txt    (paste your API key)")
    print("  2. crypto_secret.txt (paste your secret key)")
    print("\nMake sure there are no extra spaces or newlines!")
    exit(1)

print(f"\n✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
print("✅ Secret Key found: (hidden)")

# Create API client
client = CryptocomExchangeAPI(api_key=api_key, api_secret=api_secret)

# Test 1: Public endpoint (no auth required)
print("\n" + "-" * 60)
print("TEST 1: Public API (Get BTC price)")
print("-" * 60)
try:
    ticker = client.get_ticker("BTC_USDT")
    price = float(ticker.get('a', 0))
    print(f"✅ SUCCESS: BTC/USDT price: ${price:,.2f}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\nThis test doesn't require API keys - if it fails, there's a network issue")

# Test 2: Private endpoint (requires auth + IP whitelist)
print("\n" + "-" * 60)
print("TEST 2: Private API (Get Account Summary) - REQUIRES IP WHITELIST")
print("-" * 60)
try:
    account = client.get_account_summary()
    print("✅ SUCCESS: Connected to your account!")
    print(f"   Response: {account}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\n⚠️  Common reasons for failure:")
    print("   1. IP address not whitelisted in Crypto.com Exchange")
    print("   2. API key doesn't have 'Read' permission enabled")
    print("   3. API credentials are incorrect")
    print("   4. Extra spaces/newlines in crypto_key.txt or crypto_secret.txt")
    print("\n💡 To fix:")
    print("   1. Go to: https://www.whatismyip.com")
    print("   2. Copy your IP address")
    print("   3. Add it to Crypto.com Exchange → Settings → API Keys → IP Whitelist")

print("\n" + "=" * 60)
