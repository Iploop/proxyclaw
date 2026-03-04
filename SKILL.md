---
name: proxyclaw
description: |
  ProxyClaw by IPLoop — Residential proxy access for AI agents. Route requests through 2M+ residential IPs across 195+ countries from real Android, Windows, Mac & Smart TV devices. Bypass geo-restrictions, rotate IPs automatically. Free tier with 0.5GB included. Earn unlimited proxy credits by contributing bandwidth via Docker.
compatibility: Requires network access
metadata:
  author: iploop
  version: "2.1"
  website: https://proxyclaw.ai
  platform: https://iploop.io
  docker: ultronloop2026/iploop-node
---

# 🌐 ProxyClaw by IPLoop

**Premium residential proxies for AI agents — powered by 2M+ real device IPs across 195+ countries.**

Unlike datacenter proxies that get blocked instantly, ProxyClaw routes through real Android phones, Windows PCs, Macs, and Smart TVs. Sites see a normal residential user, not a bot.

## ⚡ Why ProxyClaw

| Feature | ProxyClaw | Datacenter Proxy | Bright Data |
|---------|-----------|------------------|-------------|
| IP Pool | **2M+ residential** | ~10K shared | 72M ($$$$) |
| Detection Rate | **< 5%** | 40-60% | < 5% |
| Price (per GB) | **$2.50 - $4.50** | $0.10 | $8-15 |
| Free Tier | **0.5 GB included** | ❌ | ❌ |
| Earn Credits | **✅ Docker node** | ❌ | ❌ |
| Device Types | Android, Windows, Mac, Smart TV | Servers | Mixed |
| Setup Time | **30 seconds** | Minutes | Hours |
| Countries | **195+** | Limited | 195+ |
| Success Rate | **99%+** | 60-80% | 99%+ |

## 🚀 Quick Start (30 seconds)

### 1. Get Your Free API Key

Sign up at [iploop.io/signup](https://iploop.io/signup.html) — **0.5 GB free, no credit card required.**

### 2. Start Fetching

```bash
export IPLOOP_API_KEY="your_api_key"

# Basic — auto-rotates IP every request
curl -x "http://user:${IPLOOP_API_KEY}@proxy.iploop.io:8880" https://example.com

# Target a country
curl -x "http://user:${IPLOOP_API_KEY}-country-US@proxy.iploop.io:8880" https://example.com

# Use the helper script
./fetch.sh https://example.com --country US --format markdown
```

## 🌍 Country Targeting

Append `-country-{CC}` to your API key in the proxy password:

```bash
# United States (largest pool)
curl -x "http://user:${IPLOOP_API_KEY}-country-US@proxy.iploop.io:8880" https://example.com

# Germany, UK, Brazil, Japan...
curl -x "http://user:${IPLOOP_API_KEY}-country-DE@proxy.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-GB@proxy.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-BR@proxy.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-JP@proxy.iploop.io:8880" https://example.com
```

**195+ countries** with city-level, ZIP code, ISP, and ASN-level targeting.

## 🐍 Python

```python
import requests

API_KEY = "your_api_key"

# Auto-rotating residential IP
proxies = {"https": f"http://user:{API_KEY}@proxy.iploop.io:8880"}
r = requests.get("https://httpbin.org/ip", proxies=proxies)
print(r.json())  # Different IP every request

# Country-targeted
proxies = {"https": f"http://user:{API_KEY}-country-US@proxy.iploop.io:8880"}
r = requests.get("https://example.com", proxies=proxies)
```

### Python SDK

```bash
pip install iploop
```

```python
from iploop import IPLoopClient

client = IPLoopClient(api_key="your_api_key")

# One-liner scraping with site presets
data = client.scrape("https://example.com")

# Smart scrape with fallbacks for blocked sites
data = client.smart_scrape("https://example.com")
```

## 🌐 Browser Integration

### Puppeteer (Headless Chrome)
```javascript
const puppeteer = require('puppeteer');

const browser = await puppeteer.launch({
  args: [`--proxy-server=http://proxy.iploop.io:8880`]
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
        "server": "http://proxy.iploop.io:8880",
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
options.add_argument('--proxy-server=http://proxy.iploop.io:8880')
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
HTTP_PROXY = 'http://user:YOUR_API_KEY-country-US@proxy.iploop.io:8880'
```

### Anti-Detect Browsers (GoLogin, Multilogin, AdsPower)
- **Type:** HTTP
- **Host:** `proxy.iploop.io`
- **Port:** `8880`
- **Username:** `user`
- **Password:** `YOUR_API_KEY-country-US`

## 🛡️ Anti-Bot Bypass

ProxyClaw residential IPs naturally bypass most anti-bot systems — real devices with real ISP fingerprints.

**Tips for best results:**
1. **Rotate IPs per request** — default behavior
2. **Use country targeting** — match proxy country to site's audience
3. **Add realistic headers** — User-Agent, Accept-Language
4. **Rate limit** — 1-2 req/sec per IP
5. **Use browser automation** — Puppeteer/Playwright passes JS challenges

### Sites That Work Out of the Box
Google Search, Maps, Shopping · Amazon, eBay, Walmart · LinkedIn, Facebook, Instagram, X · Zillow, Realtor · Yelp, TripAdvisor · and virtually any site that accepts residential traffic.

### Common Use Cases
| Use Case | Recommended Setup |
|----------|-------------------|
| **Web Scraping** | Puppeteer + country targeting + IP rotation |
| **Price Monitoring** | Scrapy + rotating US/EU proxies |
| **Ad Verification** | Playwright + geo-targeted IPs |
| **SEO Monitoring** | Python requests + country targeting |
| **Social Media** | Anti-detect browser + sticky sessions |
| **AI Training Data** | High-volume scraping + all countries |

## 📄 HTML → Markdown

```bash
# With node-html-markdown installed
./fetch.sh https://example.com --format markdown

# Or pipe manually
curl -x "http://user:${IPLOOP_API_KEY}@proxy.iploop.io:8880" https://example.com | nhm
```

Install converter: `npm install -g node-html-markdown`

---

## 💰 Pricing

| Plan | Per GB | Rate Limit | Details |
|------|--------|------------|---------|
| **Free** | $0 | 30 req/min | 0.5 GB included |
| **Starter** | $4.50 | 120 req/min | Pay per GB |
| **Growth** | $3.50 | 300 req/min | Pay per GB |
| **Business** | $2.50 | 600 req/min | Pay per GB |
| **Enterprise** | Custom | 1000 req/min | SLA + dedicated support |

Sign up: [iploop.io/signup](https://iploop.io/signup.html)

**Or earn unlimited free proxy data** by running a Docker node ↓

---

## 🐳 Earn Free Proxy Credits (Docker)

Share your unused bandwidth and earn proxy credits. **1 GB shared = 1 GB of proxy access.**

### One Command Setup

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

The container:
- Auto-registers with the IPLoop network
- Shares idle bandwidth (configurable limits)
- Earns credits in real-time
- Uses < 50MB RAM, near-zero CPU
- Auto-reconnects on network issues

### Docker Compose

```yaml
version: '3'
services:
  iploop-node:
    image: ultronloop2026/iploop-node:latest
    container_name: iploop-node
    restart: always
```

### Supported Platforms

| Platform | Architecture |
|----------|-------------|
| Linux | amd64, arm64 |
| macOS | Intel, Apple Silicon |
| Windows | x64 |
| Raspberry Pi | armv7 |

---

## 📊 Live Network Stats

- **2,000,000+** residential IPs
- **20,000+** nodes online
- **195+** countries covered
- **Device types:** Android, Windows, Mac, Smart TV
- **Uptime:** 99.9%
- **Avg response:** < 0.5s
- **Success rate:** 99%+

---

## 🔒 How It Works

1. **You send a request** through ProxyClaw (HTTP/HTTPS CONNECT proxy)
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

- **ProxyClaw:** [proxyclaw.ai](https://proxyclaw.ai)
- **Platform:** [iploop.io](https://iploop.io)
- **Sign Up:** [iploop.io/signup](https://iploop.io/signup.html)
- **Docker Hub:** [ultronloop2026/iploop-node](https://hub.docker.com/r/ultronloop2026/iploop-node)
- **Python SDK:** `pip install iploop`
- **Support:** partners@iploop.io
