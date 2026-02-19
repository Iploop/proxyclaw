---
name: proxyclaw
description: |
  ProxyClaw by IPLoop — Residential proxy access for AI agents. Route requests through 2M+ residential IPs across 192+ countries from real Android, Windows, Mac & Smart TV devices. Bypass geo-restrictions, rotate IPs automatically. Free tier with 0.5GB included. Earn unlimited proxy credits by contributing bandwidth via Docker.
compatibility: Requires network access
metadata:
  author: iploop
  version: "2.1"
  website: https://iploop.io
  github: https://github.com/Iploop
  docker: ultronloop2026/iploop-node
---

# 🌐 IPLoop — Two-Sided Proxy Network

## What is IPLoop?

IPLoop is a **two-sided residential proxy platform:**

| Side | What | Who | How |
|------|------|-----|-----|
| 🖥️ **Demand** | Use proxies for web scraping, unblocking & data collection | Developers, businesses, data teams | `pip install iploop` / `npm install iploop` |
| 📱 **Supply** | Earn rewards by sharing unused bandwidth | App developers, device owners | Android SDK / Docker node |

---

## 🖥️ DEMAND SIDE — Proxy & Unblocking SDK

**Access 2M+ residential IPs in 192+ countries. Unblock any website.**

### Install

```bash
pip install iploop        # Python
npm install iploop        # Node.js
```

### Quick Start

**Python:**
```python
from iploop import IPLoop

client = IPLoop("your-api-key", country="US")

# Fetch any URL through residential proxy — auto-rotates IP
resp = client.get("https://example.com")

# Geo-targeting
resp = client.get("https://amazon.de", country="DE", city="berlin")

# Sticky session — same IP across requests
session = client.session(country="US")
page1 = session.get("https://example.com/page1")
page2 = session.get("https://example.com/page2")  # same IP

# Batch scraping — concurrent
results = client.batch(max_workers=10).fetch(urls)

# Site presets — optimized for major sites
client.google.search("residential proxy")
client.amazon.product("B09V3KXJPB")
client.twitter.profile("elonmusk")
```

**Node.js:**
```typescript
import { IPLoopClient } from 'iploop';

const client = new IPLoopClient({ apiKey: 'your-api-key', country: 'US' });

// Fetch through residential proxy
const resp = await client.get('https://example.com');

// Geo-targeting
const de = await client.get('https://amazon.de', { country: 'DE', city: 'berlin' });

// Sticky session
const session = client.session(undefined, 'US');
await session.get('https://example.com/page1');
await session.get('https://example.com/page2');

// Batch
const results = await client.fetchAll(urls, {}, 10);

// SOCKS5 support
const proxyUrl = client.getProxyUrl({ country: 'US', protocol: 'socks5' });
```

**Raw curl (no SDK):**
```bash
curl -x "http://user:YOUR_API_KEY@gateway.iploop.io:8880" https://example.com
curl -x "http://user:YOUR_API_KEY-country-US@gateway.iploop.io:8880" https://example.com
```

### SDK Features

- 🌍 **192+ Countries** — Target any country, city, or ASN
- 🔄 **Auto IP Rotation** — Fresh residential IP on every request
- 📌 **Sticky Sessions** — Same IP across multiple requests
- 🕵️ **Chrome Fingerprinting** — 14-header browser fingerprint, country-matched
- 🔁 **Auto-Retry** — 3 attempts with backoff and IP rotation on failure
- ⚡ **Batch Scraping** — Concurrent requests (up to 25 workers)
- 🎯 **10 Site Presets** — Google, Amazon, Twitter, Instagram, TikTok, YouTube, Reddit, eBay, LinkedIn, Nasdaq
- 📊 **Request Stats** — Built-in tracking (success rate, avg time, errors)
- 🔒 **Error Handling** — Custom types: AuthError, ProxyError, TimeoutError, QuotaExceeded
- 🔌 **HTTP + SOCKS5** — Both protocols supported

### Browser Integration

Works with Puppeteer, Playwright, Selenium, Scrapy, and any anti-detect browser:

```python
# Playwright
browser = p.chromium.launch(proxy={
    "server": "http://gateway.iploop.io:8880",
    "username": "user",
    "password": f"{API_KEY}-country-US"
})
```

### Use Cases

| Use Case | Setup |
|----------|-------|
| Web Scraping | SDK + country targeting + IP rotation |
| Price Monitoring | Batch scraping + rotating IPs |
| Ad Verification | Geo-targeted IPs |
| SEO Monitoring | Country targeting |
| Social Media | Sticky sessions |
| Market Research | Multi-country |
| AI Training Data | High-volume batch |

---

## 📱 SUPPLY SIDE — Earn Rewards SDK

**Monetize unused bandwidth. Integrate into any Android app or run a Docker node.**

### Android SDK (for app developers)

Add the IPLoop SDK to your Android app. Your users share idle bandwidth and you earn rewards.

```java
// Initialize
IPLoopSDK.init(context, "your-partner-id");

// Start sharing (runs in background, minimal resource usage)
IPLoopSDK.start();

// Check earnings
IPLoopSDK.getEarnings(callback);
```

**SDK specs:**
- Min SDK 22 (Android 5.1+)
- < 50MB RAM, near-zero CPU
- Auto-reconnects on network issues
- Bandwidth limits configurable
- Pure Java, no native dependencies

**Download:** [Android SDK v1.0.57](https://github.com/Iploop/iploop-node)

### Docker Node (for server/desktop)

Share bandwidth from any machine:

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

**1 GB shared = 1 GB of proxy access.** Or cash out.

Supported: Linux (amd64/arm64), macOS (Intel/M1+), Windows, Raspberry Pi.

### Docker Compose

```yaml
version: '3'
services:
  iploop-node:
    image: ultronloop2026/iploop-node:latest
    container_name: iploop-node
    restart: always
```

### Check Earnings

```bash
docker logs iploop-node | head -5  # get your token
curl "https://gateway.iploop.io:9443/api/credits?token=YOUR_TOKEN"
```

---

## 💰 Pricing (Demand Side)

| Plan | Data | Price | Per GB |
|------|------|-------|--------|
| **Free** | 0.5 GB | $0 | Free |
| **Starter** | 10 GB | $10/mo | $1.00 |
| **Growth** | 50 GB | $40/mo | $0.80 |
| **Business** | 200 GB | $120/mo | $0.60 |
| **Enterprise** | 1 TB+ | Custom | $0.40+ |

---

## 📊 Network Stats

- **2,000,000+** residential IPs
- **20,000+** nodes online at any time
- **192+** countries covered
- **97%+** tunnel success rate
- **Device types:** Android, Windows, Mac, Smart TV
- **Protocols:** HTTP, HTTPS, SOCKS5

---

## 🔒 How It Works

```
┌──────────────────────────────────────────────────────────┐
│                    IPLoop Network                          │
│                                                            │
│  🖥️ DEMAND (Customers)          📱 SUPPLY (Nodes)        │
│                                                            │
│  Python SDK ──┐                 ┌── Android SDK           │
│  Node.js SDK ─┤                 ├── Docker Node           │
│  Raw HTTP ────┤    Gateway      ├── Windows App           │
│  SOCKS5 ──────┤◄──────────────►├── Mac App               │
│  Puppeteer ───┤  (matching &    ├── Smart TV              │
│  Playwright ──┘   routing)      └── 20,000+ devices       │
│                                                            │
│  Unblock sites    ◄──────────►    Earn rewards            │
│  Scrape data                      Share bandwidth          │
│  Geo-target                       Passive income           │
└──────────────────────────────────────────────────────────┘
```

1. **Customer** sends request through SDK → Gateway
2. **Gateway** selects best residential node matching country/targeting
3. **Request routes** through a real device (phone, PC, TV)
4. **Response returns** → Customer gets data, target site sees residential IP
5. **Node earns** rewards for bandwidth shared

---

## 🔗 Links

| Resource | URL |
|----------|-----|
| **Website** | [iploop.io](https://iploop.io) |
| **Dashboard** | [gateway.iploop.io](https://gateway.iploop.io) |
| **Python SDK** | [pypi.org/project/iploop](https://pypi.org/project/iploop/) |
| **Node.js SDK** | [npmjs.com/package/iploop](https://www.npmjs.com/package/iploop) |
| **GitHub** | [github.com/Iploop](https://github.com/Iploop) |
| **Docker Hub** | [ultronloop2026/iploop-node](https://hub.docker.com/r/ultronloop2026/iploop-node) |
| **Support** | partners@iploop.io |

---

## License

MIT
