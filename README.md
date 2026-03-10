# ProxyClaw by IPLoop

Residential proxy skill for AI agents — 2M+ IPs, anti-bot bypass, 64 site presets.

## Install

```bash
# OpenClaw skill
clawhub install proxyclaw

# Python SDK (recommended)
pip install iploop[stealth]
```

## Quick Start

```python
from iploop import IPLoop

client = IPLoop(api_key="YOUR_KEY")  # stealth auto-on

# Anti-bot sites just work
r = client.get("https://www.zillow.com/homes/NYC_rb/")    # ✅ 1.3MB
r = client.get("https://www.walmart.com/browse/electronics") # ✅ 1MB
r = client.get("https://www.indeed.com/jobs?q=python")      # ✅ 1.6MB

# Country targeting
r = client.get("https://example.com", country="DE")

# Sticky session
s = client.session()
r1 = s.get("http://httpbin.org/ip")
r2 = s.get("http://httpbin.org/ip")  # same IP
```

## 64 Site Presets — 89% Success Rate

| Category | Sites | Method |
|----------|-------|--------|
| **E-commerce** | Amazon, eBay, Walmart, Target, BestBuy, AliExpress, Costco, Nordstrom, Newegg, Wayfair, Nike, Etsy, Shopify | Proxy + Scrapling |
| **Jobs** | Indeed, Fiverr, Upwork, RemoteOK, Glassdoor | Scrapling |
| **Real Estate** | Zillow, Realtor, Airbnb, Booking, Expedia, TripAdvisor | Scrapling |
| **Social** | Reddit, Twitter/X, Instagram, TikTok, Pinterest, LinkedIn, Quora | Scrapling |
| **News** | CNN, BBC, NYTimes, Bloomberg, Reuters, Medium, ProductHunt | Proxy + Scrapling |
| **Tech** | GitHub, StackOverflow, HackerNews, NPM, PyPI | Proxy |
| **APIs** | YouTube, Stocks, CoinGecko, Spotify, XKCD, SpaceX, Pokemon, Weather, ExchangeRate | Direct API |
| **Other** | Google, Wikipedia, IMDb, Steam, Goodreads, Trustpilot, Craigslist, Archive.org, HomeDepot, Cloudflare | Proxy + Scrapling |

### Anti-Bot Bypass

Stealth mode uses [Scrapling](https://github.com/D4Vinci/Scrapling) browser fingerprinting + IPLoop residential IPs. This combo cracks sites that block normal proxies:

| Without Stealth | With Stealth |
|----------------|-------------|
| 73% success    | 89% success |
| Blocked by Zillow, Walmart, Indeed | ✅ All pass |

## Pricing

| Plan | Price | Data |
|------|-------|------|
| Free | $0 | 0.5 GB |
| Starter | $2.50/GB | Pay as you go |
| Pro | $4.00/GB | Priority routing |
| Use code **OPENCLAW** for 20% off |

## Earn Free Credits

Share bandwidth via Docker → earn proxy credits:

```bash
docker run -d ultronloop2026/iploop-node -token YOUR_TOKEN
```

## Links

- 🌐 [proxyclaw.ai](https://proxyclaw.ai)
- 📖 [Docs](https://proxyclaw.ai/docs.html)
- 🐍 [Python SDK](https://github.com/Iploop/iploop-python)
- 📦 [Node.js SDK](https://github.com/Iploop/iploop-node-sdk)
- 🏠 [Sign up](https://iploop.io/signup.html)
