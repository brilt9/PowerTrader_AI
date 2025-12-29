# PowerTrader_AI - Summary

**Date**: December 29, 2025
**Version**: 2.1.0
**Status**: ✅ PRODUCTION READY

---

## Overview

PowerTrader_AI is a fully automated cryptocurrency trading bot using:
- **AI-powered price prediction** (neural network)
- **Structured DCA (Dollar Cost Averaging) system**
- **Crypto.com Exchange API** for market data and trading

---

## Files

### Core Python Files

| File | Purpose |
|------|---------|
| `pt_hub.py` | Main GUI application |
| `pt_thinker.py` | Market data & signal generation |
| `pt_trader.py` | Trading execution |
| `pt_trainer.py` | AI model training |
| `cryptocom_api.py` | Crypto.com API wrapper |

### Configuration

| File | Purpose |
|------|---------|
| `crypto_key.txt` | API Key (create this) |
| `crypto_secret.txt` | Secret Key (create this) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Protects sensitive files |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Quick start guide |
| `CRYPTO_COM_MIGRATION_GUIDE.md` | API setup |
| `SECURITY_AUDIT_REPORT.md` | Security best practices |
| `CHANGELOG.md` | Version history |

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `crypto_key.txt` and `crypto_secret.txt` with your Crypto.com Exchange API credentials.

### 3. Train the Model

```bash
python pt_trainer.py BTC
```

### 4. Start the GUI

```bash
python pt_hub.py
```

### 5. Begin Trading

Click **Start All** in the Scripts menu.

---

## API Integration

### Endpoints Used

**Public** (no authentication):
- `public/get-ticker` - Current prices
- `public/get-candlestick` - Historical candles

**Private** (authenticated):
- `private/create-order` - Place orders
- `private/get-account-summary` - Account balance
- `private/get-order-history` - Order history

### Symbol Format

Use underscore separator: `BTC_USDT`, `ETH_USDT`

### Authentication

HMAC-SHA256 signature with:
- API Key
- Secret Key
- Timestamp (nonce)

---

## Trading Strategy

### Signal Levels (0-7)

- **LONG signal**: Buy direction
- **SHORT signal**: Sell direction

**Trading triggers**:
- Trade starts when LONG ≥ 3 and SHORT = 0
- DCA buys happen at lower price levels
- Sells triggered by trailing profit management

### DCA System

- Multiple buy levels for averaging entry price
- Structured position sizing
- Trailing stop for profit taking

---

## Usage Notes

### Best Practices

1. **Start small** - Test with minimal funds first
2. **Monitor regularly** - Check the GUI daily
3. **Understand the strategy** - Read documentation
4. **Protect API keys** - Never share credentials

### Important

- Trading involves risk
- Only trade what you can afford to lose
- Monitor your trades
- Understand tax implications

---

## Support

- Check documentation in this repository
- Review troubleshooting in `CRYPTO_COM_MIGRATION_GUIDE.md`

---

**Version**: 2.1.0
**Last Updated**: 2025-12-29
