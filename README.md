# PowerTrader AI

Automated crypto trading bot with AI-powered price prediction and DCA (Dollar-Cost Averaging) system.

Uses **Crypto.com Exchange API** for trading.

---

## Quick Start Guide

### Step 1: Install Python

1. Download Python from **python.org**
2. Run installer
3. **Check "Add Python to PATH"** during installation
4. Click Install

### Step 2: Download PowerTrader AI

1. Download this repository as ZIP
2. Extract to a folder (e.g., `C:\PowerTrader_AI`)

### Step 3: Open Command Prompt

1. Press **Windows Key + R**
2. Type `cmd` and press Enter
3. Navigate to the PowerTrader folder:
   ```
   cd C:\PowerTrader_AI
   ```

### Step 4: Install Dependencies

Run this command:
```
pip install -r requirements.txt
```

### Step 5: Get Crypto.com API Keys

1. Go to **https://crypto.com/exchange**
2. Create account and complete verification
3. Go to **Settings > API Keys**
4. Click **Create API Key**
5. Enable: **Read** and **Trade** permissions
6. **Add your IP address** to whitelist (required):
   - Go to https://www.whatismyip.com to find your IP
   - Add it to the API key whitelist

### Step 6: Configure API Keys

Create two files in the PowerTrader folder:

**crypto_key.txt** - paste your API key

**crypto_secret.txt** - paste your secret key

### Step 7: Train the AI

```
python pt_trainer.py BTC
```

Wait for training to complete.

### Step 8: Start Trading

```
python pt_hub.py
```

In the GUI:
1. Click **Scripts > Start All**

---

## Files

| File | Purpose |
|------|---------|
| `pt_hub.py` | Main GUI application |
| `pt_thinker.py` | AI signal generation |
| `pt_trader.py` | Trade execution |
| `pt_trainer.py` | AI model training |
| `cryptocom_api.py` | Crypto.com API wrapper |

---

## Trading Logic

- **LONG signal 3+**: Opens new trade
- **DCA levels**: Buys more at lower prices (-2.5%, -5%, -10%, etc.)
- **Trailing profit**: Sells when price drops 0.5% from peak profit

---

## Commands

Train a coin:
```
python pt_trainer.py BTC
python pt_trainer.py ETH
```

Start the GUI:
```
python pt_hub.py
```

Test API connection:
```
python test_api_connection.py
```

---

## Troubleshooting

**API not working?**
- Check your IP is whitelisted at Crypto.com
- Verify `crypto_key.txt` and `crypto_secret.txt` have no extra spaces

**Trades not starting?**
- Neural signal must reach level 3+
- Run trainer first: `python pt_trainer.py BTC`

---

## Important

- This software trades real money - use at your own risk
- Start with small amounts to test
- Keep your API keys private
- You are responsible for all trading decisions

---

## License

Apache 2.0
