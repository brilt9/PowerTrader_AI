# Changelog - PowerTrader_AI

All notable changes to this project will be documented in this file.

## [2.1.0] - 2025-12-29

### 🔧 **PRODUCTION READY RELEASE**

**Changes**:
- ✅ Complete Crypto.com Exchange API integration
- ✅ Updated all Python files to use Crypto.com API
- ✅ Simplified API setup wizard in GUI
- ✅ Removed legacy API code
- ✅ Production-ready codebase

**Files Updated**:
- `pt_hub.py` - New Crypto.com API setup wizard
- `pt_trader.py` - Crypto.com trading integration
- `pt_thinker.py` - Crypto.com market data
- `cryptocom_api.py` - Complete API wrapper
- `README.md` - Updated documentation
- `CHANGELOG.md` - This file

---

## [2.0.1] - 2025-12-29

### 🔧 **API FIXES**

**Fixed**:
- ✅ Request format corrected (proper JSON-RPC structure)
- ✅ Signature generation fixed (HMAC-SHA256)
- ✅ Request ID counter for tracking
- ✅ Endpoint URLs unified
- ✅ Number formatting for API calls

---

## [2.0.0] - 2025-12-28

### 🔄 **CRYPTO.COM EXCHANGE API**

Major update: Full Crypto.com Exchange API integration.

### Added

- ✅ **cryptocom_api.py**: API wrapper for Crypto.com Exchange
  - Public endpoints (market data, tickers, candles)
  - Private endpoints (trading, account balance, orders)
  - HMAC-SHA256 authentication
  - Rate limit handling
  - Error handling

- ✅ **Documentation**:
  - `CRYPTO_COM_MIGRATION_GUIDE.md` - API setup guide
  - `.gitignore` - Protects sensitive files
  - Example configuration files

### Changed

- ✅ **requirements.txt**: Updated dependencies
  - Added: `cryptocom-exchange>=0.15.0`
  - Added: `aiohttp`, `websockets`

- ✅ **README.md**: Updated setup instructions

### Symbol Format

- Format: `BTC_USDT`, `ETH_USDT` (underscore separator)

### Timeframe Mapping

| PowerTrader | Crypto.com |
|-------------|------------|
| `1min` | `1m` |
| `5min` | `5m` |
| `15min` | `15m` |
| `30min` | `30m` |
| `1hour` | `1h` |
| `4hour` | `4h` |
| `1day` | `1D` |
| `1week` | `1W` |

---

## [1.0.0] - Original Version

### Features

- AI-powered price prediction
- Structured/tiered DCA system
- Real-time GUI monitoring
- Neural network training
- Multi-coin support
- Account value tracking
- Trade history logging

---

## Future Plans

### Planned

- [ ] WebSocket support for real-time data
- [ ] Advanced order types (stop-loss, take-profit)
- [ ] Backtesting framework
- [ ] Performance analytics dashboard
- [ ] Mobile notifications

---

**Version Format**: [Major].[Minor].[Patch]
- **Major**: Breaking changes
- **Minor**: New features
- **Patch**: Bug fixes

**Last Updated**: 2025-12-29
