# PowerTrader_AI
Fully automated crypto trading powered by a custom price prediction AI and a structured/tiered DCA system.

## 🔄 **CRYPTO.COM EXCHANGE API**

**This version uses the Crypto.com Exchange API** for both market data and trading.

📚 **See**: `CRYPTO_COM_MIGRATION_GUIDE.md` for full API details

# Setup & First-Time Use (Windows)

THESE INSTRUCTIONS WERE WRITTEN BY AI! PLEASE LET ME KNOW IF THERE ARE ANY ERRORS OR ISSUES WITH THIS SETUP PROCESS!

This page walks you through installing PowerTrader AI from start to finish, in the exact order a first-time user should do it.  
No coding knowledge needed.  
These instructions are Windows-based but PowerTrader AI can run on any OS.

**Important:** This software can place trades automatically. You are responsible for what it does.  
Keep your API keys private. We are not giving financial advice. We are not responsible for any losses incurred. You are fully responsible for doing your own due diligence to learn and understand this trading system and to use it properly. You are fully responsible for all of your money, and any gains or losses.

---

## Step 1 — Install Python

1. Go to **python.org** and download Python for Windows.
2. Run the installer.
3. **Check the box** that says: **“Add Python to PATH”**.
4. Click **Install Now**.

---

## Step 2 — Download PowerTrader AI

1. On the PowerTrader AI GitHub page, click **Code** → **Download ZIP**.
2. Extract the ZIP somewhere simple, like: `C:\PowerTraderAI\`

---

## Step 3 — Install PowerTrader AI (one command)

1. Open **Command Prompt** (Windows key → type **cmd** → Enter).
2. Go into your PowerTrader AI folder. Example:

   `cd C:\PowerTraderAI`

3. Install everything PowerTrader AI needs:

   `python -m pip install -r requirements.txt`

---

## Step 4 — Start PowerTrader AI

From the same Command Prompt window (inside your PowerTrader folder), run:

`python pt_hub.py`

The app that opens is the **PowerTrader Hub**.  
This is the only thing you need to run day-to-day.

---

## Step 5 — Set your folder, coins, and Crypto.com Exchange API keys

### Open Settings

In the Hub, open **Settings** and do this in order:

- **Main Neural Folder**: set this to the same folder that contains `pt_hub.py` (recommended easiest).
- **Choose which coins to trade**: start with **BTC**.

### Get Crypto.com Exchange API Keys

1. **Create Account**: Go to https://crypto.com/exchange and complete KYC verification
2. **Enable 2FA**: Set up two-factor authentication for security
3. **Generate API Keys**:
   - Navigate to **Settings** → **API Keys**
   - Click **+ Create API Key**
   - Set permissions: **Read** ✓ and **Trade** ✓
   - **Whitelist your IP address** (REQUIRED - see below)
   - Save the **API Key** and **Secret Key** securely

4. **Whitelist Your IP Address** (REQUIRED):
   - Go to https://www.whatismyip.com to find your IP
   - Add your IP to the API key's whitelist in Crypto.com Exchange
   - 📖 See [IP_WHITELIST_GUIDE.md](IP_WHITELIST_GUIDE.md) for detailed instructions

### Configure PowerTrader AI

Create two text files in your PowerTrader AI folder:

**crypto_key.txt**:
```
your_api_key_here
```

**crypto_secret.txt**:
```
your_secret_key_here
```

**IMPORTANT**: Keep these files private! Set proper permissions:
```bash
# On Linux/Mac
chmod 600 crypto_key.txt crypto_secret.txt
```

After creating these files, you're ready to use PowerTrader AI with Crypto.com Exchange.

PowerTrader AI uses a simple folder style:  
**BTC uses the main folder**, and other coins use their own subfolders (like `ETH\`).

---

## Step 6 — Train (inside the Hub)

Training builds the system’s coin “memory” so it can generate signals.

1. In the Hub, click **Train All**.
2. Wait until training finishes.

---

## Step 7 — Start the system (inside the Hub)

When training is done, click:

1. **Start All**

The Hub will:  
**start pt_thinker.py**, wait until it is ready, then it will **start trader.py**.  
You don’t need to manually start separate programs. The hub handles everything!

---

## Neural Levels (the LONG/SHORT numbers)

- These are signal strength levels from low to high.
- Higher number = stronger signal.
- LONG = buy-direction signal. SHORT = sell-direction signal.

A TRADE WILL START FOR A COIN IF THAT COIN REACHES A LONG LEVEL OF 3 OR HIGHER WHILE HAVING A SHORT LEVEL OF 0!

---

## Adding more coins (later)

1. Open **Settings**
2. Add one new coin
3. Save
4. Click **Train All**, wait for training to complete
5. Click **Start All**

---

## Donate

PowerTrader AI is COMPLETELY free and open source! If you want to support the project:

- Cash App: **$garagesteve**
- PayPal: **@garagesteve**
- Patreon: **patreon.com/MakingMadeEasy**

---

## License

PowerTrader AI is released under the **Apache 2.0** license.
