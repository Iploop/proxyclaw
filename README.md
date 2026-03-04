# 🌐 ProxyClaw by IPLoop

**Residential proxy access for AI agents — powered by 2M+ real device IPs across 195+ countries.**

ProxyClaw is an [OpenClaw](https://openclaw.ai) skill that gives your AI agent instant access to any website through real residential IPs. JS rendering, CAPTCHA solving, anti-bot bypass — all built in.

## ⚡ Install

```bash
clawhub install proxyclaw
```

Or manually: copy the `SKILL.md`, `fetch.sh`, and `setup.sh` into your OpenClaw skills directory.

## 🚀 Quick Start

### 1. Get Your Free API Key

Sign up at [iploop.io/signup](https://iploop.io/signup.html) — **0.5 GB free, no credit card required.**

### 2. Start Fetching

```bash
export IPLOOP_API_KEY="your_api_key"

# Auto-rotating residential IP
curl -x "http://user:${IPLOOP_API_KEY}@proxy.iploop.io:8880" https://example.com

# Target a country
curl -x "http://user:${IPLOOP_API_KEY}-country-US@proxy.iploop.io:8880" https://example.com

# Helper script
./fetch.sh https://example.com --country US --format markdown
```

### 3. Python SDK

```bash
pip install iploop
```

```python
from iploop import IPLoopClient

client = IPLoopClient(api_key="your_api_key")
data = client.scrape("https://example.com")
```

## 🌍 Features

- **195+ countries** with city, ZIP, ISP, and ASN-level targeting
- **2M+ residential IPs** from real Android, Windows, Mac, Smart TV devices
- **99%+ success rate** — real device fingerprints bypass anti-bot systems
- **< 0.5s avg response** time
- **Auto IP rotation** — fresh IP every request
- **HTTP, HTTPS, SOCKS5** support
- **Browser integration** — Puppeteer, Playwright, Selenium, Scrapy
- **Earn credits** — share bandwidth via Docker, get free proxy access

## 💰 Pricing

| Plan | Per GB | Rate Limit |
|------|--------|------------|
| **Free** | $0 | 30 req/min (0.5 GB included) |
| **Starter** | $4.50 | 120 req/min |
| **Growth** | $3.50 | 300 req/min |
| **Business** | $2.50 | 600 req/min |
| **Enterprise** | Custom | 1000 req/min |

## 🐳 Earn Free Proxy Credits

Share unused bandwidth and earn credits:

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

**1 GB shared = 1 GB of proxy access.** Runs on Linux, macOS, Windows, Raspberry Pi.

## 📖 Documentation

- **Full skill docs:** [SKILL.md](./SKILL.md)
- **Support API:** [docs/SUPPORT-API.md](./docs/SUPPORT-API.md)
- **ProxyClaw website:** [proxyclaw.ai](https://proxyclaw.ai)
- **IPLoop platform:** [iploop.io](https://iploop.io)
- **Docker Hub:** [ultronloop2026/iploop-node](https://hub.docker.com/r/ultronloop2026/iploop-node)

## 📧 Support

- Email: partners@iploop.io
- Website: [iploop.io](https://iploop.io)

## License

MIT — see [LICENSE](./LICENSE)
