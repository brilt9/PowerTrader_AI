# Crypto.com Exchange IP Whitelist Guide

## Why You Need This

Crypto.com Exchange **requires** you to whitelist your IP address before you can use your API keys. Without whitelisting your IP, API calls will fail.

---

## Step-by-Step: How to Whitelist Your IP

### Step 1: Find Your Public IP Address

Your public IP is the address your computer uses to connect to the internet.

**Easy Method:**
1. Open your web browser
2. Go to: **https://www.whatismyip.com**
3. Copy the IP address shown (looks like `123.456.789.012`)

**Command Line Method (alternative):**
```bash
curl ifconfig.me
```

---

### Step 2: Add IP to Crypto.com Exchange

1. Go to https://crypto.com/exchange
2. Log in to your account
3. Navigate to **Settings** → **API Keys**
4. Find your API key (or create a new one):
   - Click **+ Create API Key** if needed
   - Set permissions:
     - ✅ **Read** (required for all operations)
     - ✅ **Trade** (optional, needed for placing orders)
5. In the **IP Whitelist** field, paste your IP address from Step 1
6. Click **Save** or **Create**

**IMPORTANT:** You cannot save an API key without at least one IP address whitelisted!

---

## Testing Your Setup

After whitelisting your IP, run the test script:

```bash
python test_api_connection.py
```

This will:
- ✅ Verify your API key files are set up correctly
- ✅ Test the public API (no auth required)
- ✅ Test the private API (requires IP whitelist)

---

## Common Issues

### Issue: "IP not whitelisted" error

**Solution:** Double-check that:
1. You whitelisted the correct IP address
2. Your IP hasn't changed (see below)
3. You saved the changes in Crypto.com Exchange settings

### Issue: API was working, now it's not

**Cause:** Your IP address changed (common with home/office internet)

**Solution:**
1. Get your current IP again: https://www.whatismyip.com
2. Update the IP whitelist in Crypto.com Exchange
3. Save the changes

### Issue: Using laptop/mobile setup

**Problem:** If you switch between WiFi networks (home, office, coffee shop), your IP changes each time

**Solutions:**
- **Option A:** Update the whitelist each time you change networks
- **Option B:** Add multiple IPs to the whitelist (if Crypto.com allows)
- **Option C:** Use a VPN with a static IP address
- **Option D:** Run PowerTrader AI on a cloud server (AWS, Azure, GCP) with a static IP

---

## Dynamic IP vs Static IP

### Dynamic IP (Most Common)
- Your ISP assigns you a different IP periodically
- Changes when you restart your modem/router
- **Problem:** Breaks API access until you update the whitelist
- **Who has this:** Most home and office internet connections

### Static IP (Recommended for Trading Bots)
- Your IP never changes
- **Benefit:** Set up once, works forever
- **How to get:**
  1. Contact your ISP (may cost extra monthly fee)
  2. Use a VPN service with static IPs
  3. Run on cloud server (AWS EC2, Azure VM, etc.)

---

## Cloud Deployment (Advanced)

For 24/7 automated trading, consider running PowerTrader AI on a cloud server:

### AWS EC2 Example:
1. Launch a small EC2 instance (t2.micro for free tier)
2. Get the instance's Elastic IP (static IP)
3. Whitelist the Elastic IP in Crypto.com
4. Install PowerTrader AI on the EC2 instance
5. Run 24/7 without worrying about IP changes

### Other Cloud Options:
- **Azure:** Virtual Machine with static public IP
- **Google Cloud:** Compute Engine with static IP
- **DigitalOcean:** Droplet with reserved IP

---

## Security Notes

⚠️ **Important Security Tips:**

1. **Never share your API keys** - Keep `crypto_key.txt` and `crypto_secret.txt` private
2. **Set restrictive permissions** on API key files:
   ```bash
   chmod 600 crypto_key.txt crypto_secret.txt
   ```
3. **Use read-only keys for testing** - Only enable Trade permission when you're ready
4. **Don't whitelist public IPs** - Avoid whitelisting IPs from public WiFi or shared networks
5. **Monitor your account** - Regularly check your trade history for unauthorized activity

---

## Quick Reference

| Task | Command/Link |
|------|--------------|
| Find your IP | https://www.whatismyip.com |
| Crypto.com API settings | https://crypto.com/exchange/user/settings/api-management |
| Test connection | `python test_api_connection.py` |
| Test public API only | `python test_public_api.py` |

---

## Still Having Issues?

If you've followed all steps and still get errors:

1. Check the exact error message in the test script output
2. Verify no extra spaces/newlines in `crypto_key.txt` and `crypto_secret.txt`
3. Confirm your system clock is accurate (API uses timestamps)
4. Try creating a fresh API key with a new IP whitelist

---

**Last Updated:** 2025-12-30
