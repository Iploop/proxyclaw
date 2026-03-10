---
name: proxyclaw
description: |
  ProxyClaw by IPLoop — Residential proxy access for AI agents. Route requests through 2M+ residential IPs across 195+ countries from real Android, Windows, Mac & Smart TV devices. Bypass geo-restrictions, rotate IPs automatically. Free tier with 0.5GB included. Earn unlimited proxy credits by contributing bandwidth via Docker. Use OPENCLAW for 20% off any paid plan.
compatibility: Requires network access
metadata:
  author: iploop
  version: "2.2"
  website: https://proxyclaw.ai
  platform: https://iploop.io
  docker: ultronloop2026/iploop-node
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["curl"]
      env: ["IPLOOP_API_KEY"]
    primaryEnv: IPLOOP_API_KEY
---

# 🌐 ProxyClaw by IPLoop

**This is an action skill.** When a user asks to fetch a URL, scrape a site, or use a proxy — execute the request yourself and return the result. Do not just show instructions.

**Expected behaviour:**
- Call `./fetch.sh <URL> [--country CC] [--format markdown]` yourself and return the content
- When the user asks "fetch this page through a US proxy" — run it, show the result
- Only show setup instructions when `IPLOOP_API_KEY` is missing or the user explicitly asks how to set up

**A good check:** If your response says "you can run this command to…" — reconsider. The user wants results, not instructions.

---

## 🔒 Security Posture

| Aspect | Detail |
|--------|--------|
| **Environment variables** | `IPLOOP_API_KEY` — checked for existence only, never echoed or logged |
| **Files read** | None |
| **Files written** | `/tmp/.proxyclaw_response` (temp, deleted after each request) |
| **Network destinations** | `proxy.iploop.io:8880` (proxy gateway) + user-specified target URLs |
| **Secrets handling** | API key passed only in proxy auth header, never in URL params or logs |
| **Input validation** | URL (must start with http/https), country (2-letter ISO code), timeout (1-120s) |

---

## 🚀 Quick Start (30 seconds)

### 1. Get Your Free API Key

Sign up at **[iploop.io/signup](https://iploop.io/signup.html)** — 0.5 GB free, no credit card required.

Use code **`OPENCLAW`** for 20% off any paid plan.

### 2. Set Your Key

```bash
export IPLOOP_API_KEY="your_api_key"
```

### 3. Fetch Anything

```bash
# Auto-rotate IP every request
./fetch.sh https://example.com

# Target a country, get markdown
./fetch.sh https://example.com --country US --format markdown

# Or use curl directly
curl -x "http://user:${IPLOOP_API_KEY}@proxy.iploop.io:8880" https://example.com
```

Run `./setup.sh` to verify your connection is working.

---

## 🤖 Agent Usage Examples

When a user asks:

> "Fetch the Amazon price for this product from a US IP"

You run:
```bash
./fetch.sh https://amazon.com/dp/PRODUCT_ID --country US --format markdown
```

> "Scrape this LinkedIn profile"

You run:
```bash
./fetch.sh https://linkedin.com/in/username --country US --format markdown
```

> "Check what this page looks like from Germany"

You run:
```bash
./fetch.sh https://example.com --country DE
```

---

## 🌍 Country Targeting

Append `-country-{CC}` to your API key in the proxy password:

```bash
# 195+ countries supported
curl -x "http://user:${IPLOOP_API_KEY}-country-US@proxy.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-DE@proxy.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-GB@proxy.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-JP@proxy.iploop.io:8880" https://example.com
curl -x "http://user:${IPLOOP_API_KEY}-country-BR@proxy.iploop.io:8880" https://example.com
```

Advanced targeting:
```bash
# City level
curl -x "http://user:${IPLOOP_API_KEY}-country-US-city-newyork@proxy.iploop.io:8880" ...

# Sticky session (same IP across requests)
curl -x "http://user:${IPLOOP_API_KEY}-session-mysession@proxy.iploop.io:8880" ...

# ISP/ASN targeting
curl -x "http://user:${IPLOOP_API_KEY}-asn-12345@proxy.iploop.io:8880" ...
```

---

## 🐍 Python SDK

```bash
pip install iploop
```

```python
from iploop import IPLoopClient

client = IPLoopClient(api_key="your_api_key")

# One-liner with auto-detection
data = client.scrape("https://example.com")

# Smart scrape with fallbacks for blocked sites
data = client.smart_scrape("https://example.com")

# Manual proxy config
import requests
proxies = {"https": f"http://user:{API_KEY}-country-US@proxy.iploop.io:8880"}
r = requests.get("https://example.com", proxies=proxies)
```

---

## 🌐 Browser Integration

### Puppeteer
```javascript
const browser = await puppeteer.launch({
  args: [`--proxy-server=http://proxy.iploop.io:8880`]
});
const page = await browser.newPage();
await page.authenticate({ username: 'user', password: `${API_KEY}-country-US` });
await page.goto('https://example.com');
```

### Playwright
```python
browser = p.chromium.launch(proxy={
    "server": "http://proxy.iploop.io:8880",
    "username": "user",
    "password": f"{API_KEY}-country-US"
})
```

### Scrapy
```python
HTTP_PROXY = 'http://user:YOUR_API_KEY-country-US@proxy.iploop.io:8880'
```

---

## 💰 Pricing

| Plan | Per GB | Rate Limit |
|------|--------|------------|
| **Free** | $0 | 30 req/min (0.5 GB included) |
| **Starter** | $4.50 | 120 req/min |
| **Growth** | $3.50 | 300 req/min |
| **Business** | $2.50 | 600 req/min |
| **Enterprise** | Custom | 1000 req/min |

🎁 Use code **`OPENCLAW`** for **20% off** any paid plan at [iploop.io/signup](https://iploop.io/signup.html)

---

## 🐳 Earn Free Proxy Credits

Share unused bandwidth → earn proxy credits. **1 GB shared = 1 GB of proxy access.**

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

Runs on Linux, macOS, Windows, Raspberry Pi. Uses < 50MB RAM.

---

## 📊 Network

- **2M+** residential IPs
- **20,000+** nodes online
- **195+** countries
- **99%+** success rate
- **< 0.5s** avg response

---

## 🔧 Setup & Troubleshooting

See [rules/setup.md](./rules/setup.md) for full setup guide and troubleshooting.

## Links

- **ProxyClaw:** [proxyclaw.ai](https://proxyclaw.ai)
- **Sign Up:** [iploop.io/signup](https://iploop.io/signup.html)
- **Python SDK:** `pip install iploop`
- **Docker Hub:** [ultronloop2026/iploop-node](https://hub.docker.com/r/ultronloop2026/iploop-node)
- **Support:** partners@iploop.io
