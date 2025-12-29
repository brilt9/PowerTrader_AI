# Crypto.com API Guide

## Overview

PowerTrader_AI uses the **Crypto.com Exchange API** for market data and trading.

---

## Installation

```bash
pip install -r requirements.txt
```

Dependencies:
```
cryptocom-exchange>=0.15.0
aiohttp
websockets
```

---

## API Endpoints

### Market Data (Public)

| Function | Endpoint |
|----------|----------|
| Get Ticker | `public/get-ticker` |
| Get Candles | `public/get-candlestick` |
| Get Order Book | `public/get-book` |

### Trading (Private)

| Function | Endpoint |
|----------|----------|
| Place Order | `private/create-order` |
| Cancel Order | `private/cancel-order` |
| Get Account | `private/get-account-summary` |
| Order History | `private/get-order-history` |
| Trade History | `private/get-trades` |

---

## Symbol Format

**Format**: `BTC_USDT`, `ETH_USDT` (underscore separator)

Examples:
- Bitcoin: `BTC_USDT`
- Ethereum: `ETH_USDT`
- Ripple: `XRP_USDT`
- Dogecoin: `DOGE_USDT`

---

## Authentication

Crypto.com uses **HMAC-SHA256** for API authentication:

```python
import hmac
import hashlib

def generate_signature(params, api_secret, timestamp):
    param_string = ''.join(f"{k}{v}" for k, v in sorted(params.items()))
    sig_payload = param_string + str(timestamp)

    signature = hmac.new(
        api_secret.encode('utf-8'),
        sig_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return signature
```

---

## API Setup

### 1. Create Crypto.com Exchange Account

1. Go to https://crypto.com/exchange
2. Complete KYC verification
3. Enable 2FA for security

### 2. Generate API Keys

1. Navigate to **Settings** → **API Keys**
2. Click **+ Create API Key**
3. Set permissions:
   - ✅ Read
   - ✅ Trade
4. Save the **API Key** and **Secret Key**

### 3. Configure PowerTrader_AI

Create two files in the PowerTrader_AI directory:

**crypto_key.txt**:
```
your_api_key_here
```

**crypto_secret.txt**:
```
your_secret_key_here
```

**Set file permissions**:
```bash
chmod 600 crypto_key.txt crypto_secret.txt
```

---

## Timeframe Mapping

| PowerTrader | Crypto.com |
|-------------|------------|
| `1min` | `1m` |
| `5min` | `5m` |
| `15min` | `15m` |
| `30min` | `30m` |
| `1hour` | `1h` |
| `2hour` | `2h` |
| `4hour` | `4h` |
| `8hour` | `8h` |
| `12hour` | `12h` |
| `1day` | `1D` |
| `1week` | `1W` |

---

## Testing Checklist

Before going live:

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `crypto_key.txt` and `crypto_secret.txt`
- [ ] Test connection in Settings → Setup Wizard
- [ ] Run trainer: `python pt_trainer.py BTC`
- [ ] Test with small trade amounts
- [ ] Monitor logs for errors

---

## API Rate Limits

**Crypto.com Exchange Limits**:
- Public endpoints: 100 requests/second
- Private endpoints: 100 requests/second

**Best Practices**:
- Add delays between requests if needed
- Use caching for market data
- Don't exceed rate limits

---

## Troubleshooting

### Common Issues

1. **"Invalid signature" error**
   - Check API key and secret are correct
   - Ensure no extra whitespace in key files
   - Verify system clock is accurate

2. **"Symbol not found" error**
   - Use `BTC_USDT` format (underscore, not hyphen)
   - Ensure trading pair exists on Crypto.com

3. **"Insufficient balance" error**
   - Check USDT balance in account
   - Verify minimum order size requirements

4. **Connection timeouts**
   - Check internet connection
   - Verify Crypto.com API is accessible

---

## Resources

- **Crypto.com API Docs**: https://exchange-docs.crypto.com/exchange/v1/rest-ws/index.html
- **API Management**: https://crypto.com/exchange/user/settings/api-management

---

**Last Updated**: 2025-12-29
