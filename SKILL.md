---
name: proxyclaw
description: |
  ProxyClaw by IPLoop — Residential proxy access for AI agents. Route requests through 2M+ residential IPs across 50+ countries from real Android, Windows, Mac & Smart TV devices. Bypass geo-restrictions, rotate IPs automatically. Free tier with 0.5GB included. Earn unlimited proxy credits by contributing bandwidth via Docker.
compatibility: Requires network access
metadata:
  author: iploop
  version: "2.0"
  website: https://iploop.io
  github: https://github.com/iploop/iploop-node
  docker: ultronloop2026/iploop-node
---

# 🌐 ProxyClaw by IPLoop

**Premium residential proxies for AI agents — powered by 2M+ real device IPs.**

Unlike datacenter proxies that get blocked instantly, ProxyClaw routes through real Android phones, Windows PCs, Macs, and Smart TVs in 192+ countries. Sites see a normal residential user, not a bot.

**Two sides:**
- 🖥️ **Demand:** `pip install iploop` / `npm install iploop` — proxy SDK for web scraping & unblocking
- 📱 **Supply:** Android SDK / Docker node — earn rewards by sharing bandwidth

## ⚡ Why ProxyClaw

| Feature | ProxyClaw | Datacenter Proxy | Bright Data |
|---------|-----------|------------------|-------------|
| IP Pool | **2M+ residential** | ~10K shared | 72M ($$$$) |
| Detection Rate | **< 5%** | 40-60% | < 5% |
| Price (per GB) | **$0.60 - $1.00** | $0.10 | $8-15 |
| Free Tier | **0.5 GB included** | ❌ | ❌ |
| Earn Credits | **✅ Docker node** | ❌ | ❌ |
| Device Types | Android, Windows, Mac, Smart TV | Servers | Mixed |
| Setup Time | **30 seconds** | Minutes | Hours |

## 🚀 Quick Start (30 seconds)

### 1. Get Your Free API Key

```bash
curl -s -X POST https://gateway.iploop.io:9443/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'
```

Returns your `api_key` — that's all you need. **0.5 GB free, no credit card required.**

Or sign up at [iploop.io](https://iploop.io)

### 2. Start Fetching

```bash
export IPLOOP_API_KEY="your_api_key"

# Basic — auto-rotates IP every request
curl -x "http://user:${IPLOOP_API_KEY}@gateway.iploop.io:8880" https://example.com

# Target a country
curl -x "http://user:${IPLOOP_API_KEY}-country-US@gateway.iploop.io:8880" https://example.com

# Use the helper script
./fetch.sh https://example.com --country US --format markdown
```

## 🌍 Country Targeting

Append `-country-{CC}` to your API key in the proxy password:

```bash
# United States (largest pool — 1M+ IPs)
curl -x "http://user:${IPLOOP_API_KEY}-country-US@gateway.iploop.io:8880" https://example.com

# Germany, UK, Brazil, Japan...
curl -x "http://user:${IPLOOP_API_KEY}-country-DE@gateway.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-GB@gateway.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-BR@gateway.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-JP@gateway.iploop.io:8880" https://example.com
```

**50+ countries:** US, GB, DE, FR, CA, AU, JP, KR, BR, IN, IT, ES, NL, SE, NO, DK, FI, PL, CZ, AT, CH, BE, PT, IE, RU, UA, TR, IL, ZA, MX, AR, CL, CO, PE, TH, VN, PH, ID, MY, SG, HK, TW, NZ, RO, BG, HU, GR, EG, NG, KE, and more.

## 🐍 Python

```python
import requests

API_KEY = "your_api_key"

# Auto-rotating residential IP
proxies = {"https": f"http://user:{API_KEY}@gateway.iploop.io:8880"}
r = requests.get("https://httpbin.org/ip", proxies=proxies)
print(r.json())  # Different IP every request

# Country-targeted
proxies = {"https": f"http://user:{API_KEY}-country-US@gateway.iploop.io:8880"}
r = requests.get("https://example.com", proxies=proxies)
```

## 🌐 Browser Integration

### Puppeteer (Headless Chrome)
```javascript
const puppeteer = require('puppeteer');

const browser = await puppeteer.launch({
  args: [`--proxy-server=http://gateway.iploop.io:8880`]
});
const page = await browser.newPage();
await page.authenticate({ username: 'user', password: `${API_KEY}-country-US` });
await page.goto('https://example.com');
console.log(await page.content());
await browser.close();
```

### Playwright (Multi-Browser)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(proxy={
        "server": "http://gateway.iploop.io:8880",
        "username": "user",
        "password": f"{API_KEY}-country-US"
    })
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.content())
    browser.close()
```

### Selenium
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--proxy-server=http://gateway.iploop.io:8880')
driver = webdriver.Chrome(options=options)
driver.get("https://example.com")
print(driver.page_source)
driver.quit()
```

### Scrapy
```python
# settings.py
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}
HTTP_PROXY = 'http://user:YOUR_API_KEY-country-US@gateway.iploop.io:8880'
```

### Anti-Detect Browsers (GoLogin, Multilogin, AdsPower)
Use these proxy settings in any anti-detect browser profile:
- **Type:** HTTP
- **Host:** `gateway.iploop.io`
- **Port:** `8880`
- **Username:** `user`
- **Password:** `YOUR_API_KEY-country-US` (change country code as needed)

Each browser profile gets a unique residential IP — perfect for multi-account management.

## 🛡️ Anti-Bot Bypass Tips

ProxyClaw residential IPs naturally bypass most anti-bot systems because they come from **real devices with real ISP fingerprints**. For best results:

1. **Rotate IPs per request** — default behavior, every request gets a fresh IP
2. **Use country targeting** — match the proxy country to the site's target audience
3. **Add realistic headers** — set User-Agent, Accept-Language matching the proxy country
4. **Rate limit requests** — 1-2 req/sec per IP avoids rate limiting
5. **Use browser automation** — Puppeteer/Playwright with our proxy passes JavaScript challenges
6. **Handle CAPTCHAs** — combine with 2Captcha or Anti-Captcha for CAPTCHA-heavy sites

### Sites That Work Out of the Box
- Google Search, Google Maps, Google Shopping
- Amazon, eBay, Walmart, Target
- LinkedIn, Facebook, Instagram, Twitter/X
- Zillow, Realtor, Redfin
- Yelp, TripAdvisor
- Any site that allows residential traffic

### Common Use Cases
| Use Case | Recommended Setup |
|----------|-------------------|
| **Web Scraping** | Puppeteer + country targeting + IP rotation |
| **Price Monitoring** | Scrapy + rotating US/EU proxies |
| **Ad Verification** | Playwright + geo-targeted IPs |
| **SEO Monitoring** | Python requests + country targeting |
| **Social Media** | Anti-detect browser + sticky sessions |
| **Market Research** | Browser automation + multi-country |
| **Brand Protection** | Rotating proxies + global coverage |
| **AI Training Data** | High-volume scraping + all countries |

## 📄 HTML → Markdown

```bash
# With node-html-markdown installed
./fetch.sh https://example.com --format markdown

# Or pipe manually
curl -x "http://user:${IPLOOP_API_KEY}@gateway.iploop.io:8880" https://example.com | nhm
```

Install converter: `npm install -g node-html-markdown`

---

## 💰 Pricing

| Plan | Data | Price | Per GB |
|------|------|-------|--------|
| **Free** | 0.5 GB | $0 | Free |
| **Starter** | 10 GB | $10/mo | $1.00 |
| **Growth** | 50 GB | $40/mo | $0.80 |
| **Business** | 200 GB | $120/mo | $0.60 |
| **Enterprise** | 1 TB+ | Custom | $0.40+ |

**Or earn unlimited free proxy data** by running a Docker node ↓

---

## 🐳 Earn Free Proxy Credits (Docker)

Share your unused bandwidth and earn proxy credits. **1 GB shared = 1 GB of proxy access.**

### One Command Setup

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

That's it. The container:
- Auto-registers with the IPLoop network
- Shares idle bandwidth (configurable limits)
- Earns credits in real-time
- Uses < 50MB RAM, near-zero CPU
- Auto-reconnects on network issues

### Check Your Credits

```bash
# Get your node token from container logs
docker logs iploop-node | head -5

# Check credits
curl "https://gateway.iploop.io:9443/api/credits?token=YOUR_TOKEN"
```

### Docker Compose

```yaml
version: '3'
services:
  iploop-node:
    image: ultronloop2026/iploop-node:latest
    container_name: iploop-node
    restart: always
    environment:
      - IPLOOP_GATEWAY=gateway.iploop.io:9443
```

### Supported Platforms

| Platform | Architecture | Image |
|----------|-------------|-------|
| Linux | amd64 | `ultronloop2026/iploop-node:latest` |
| Linux | arm64 | `ultronloop2026/iploop-node:latest` |
| macOS | Intel/M1+ | `ultronloop2026/iploop-node:latest` |
| Windows | x64 | `ultronloop2026/iploop-node:latest` |
| Raspberry Pi | armv7 | `ultronloop2026/iploop-node:latest` |

### Standalone Binaries

Don't want Docker? Download the binary directly:
- [Linux amd64](https://github.com/iploop/iploop-node/releases)
- [Linux arm64](https://github.com/iploop/iploop-node/releases)
- [macOS Intel](https://github.com/iploop/iploop-node/releases)
- [macOS ARM](https://github.com/iploop/iploop-node/releases)
- [Windows x64](https://github.com/iploop/iploop-node/releases)
- [Linux armv7 (RPi)](https://github.com/iploop/iploop-node/releases)

---

## 📊 Network Stats

- **2,000,000+** residential IPs
- **19,000+** nodes online at any time
- **50+** countries covered
- **Device types:** Android, Windows, Mac, Smart TV
- **Uptime:** 99.9%
- **Avg response:** < 2s

Check live stats: `curl https://gateway.iploop.io:9443/dashboard`

---

## 🔒 How It Works

1. **You send a request** through ProxyClaw (HTTPS CONNECT proxy)
2. **Gateway selects a residential node** matching your country/targeting
3. **Request routes through a real device** (phone, PC, TV)
4. **Response returns** through the same path
5. **Target site sees a normal residential IP** — not a datacenter

All traffic is encrypted end-to-end. We don't inspect, log, or cache your requests.

---

## 🔧 Setup

Run `setup.sh` to verify everything works:
```bash
./setup.sh
```

## Links

- **Dashboard:** [iploop.io](https://iploop.io)
- **GitHub:** [github.com/iploop/iploop-node](https://github.com/iploop/iploop-node)
- **Docker Hub:** [hub.docker.com/r/ultronloop2026/iploop-node](https://hub.docker.com/r/ultronloop2026/iploop-node)
- **Support:** partners@iploop.io

---

## 🛠 Support API

Self-service support endpoints at `gateway.iploop.io:9443`:

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/support/status` | GET | No | System health check |
| `/api/support/diagnose?api_key=KEY` | GET | Yes | Diagnose your key — plan, quota, usage |
| `/api/support/errors/{code}` | GET | No | Error code lookup (407, 403, 502, etc.) |
| `/api/support/ask` | POST | Yes | Ask questions (body: `{"question": "..."}`) |

### Rate Limits

All responses include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.

| Plan | Requests/min |
|------|-------------|
| Free | 30 |
| Rewarded | 120 |
| Starter | 120 |
| Growth | 300 |
| Business | 600 |
| Enterprise | 1000+ |
