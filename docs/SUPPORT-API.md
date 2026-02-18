# IPLoop Support API

Base URL: `https://gateway.iploop.io:9443`

All endpoints return JSON. Rate limit headers included on every response.

---

## Authentication

Most endpoints require your API key via query parameter or header:
- Query: `?api_key=YOUR_KEY`
- Header: `Authorization: Bearer YOUR_KEY`

Get your API key at [iploop.io/signup.html](https://iploop.io/signup.html)

---

## Endpoints

### 1. GET /api/support/status

System health check. **No auth required.**

**Response:**
```json
{
  "status": "operational",
  "network": "High volume residential IP pool worldwide",
  "countries_available": 195,
  "coverage": "High availability across all regions",
  "protocols": ["HTTP CONNECT", "SOCKS5"],
  "proxy_endpoint": "gateway.iploop.io:8880",
  "supported_targeting": ["country", "city", "session", "sticky"],
  "docs": "https://docs.iploop.io"
}
```

**Status values:** `operational`, `degraded`, `down`

**Example:**
```bash
curl -s https://gateway.iploop.io:9443/api/support/status
```

---

### 2. GET /api/support/diagnose

Diagnose your API key — check validity, plan, quota, usage. **Auth required.**

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| api_key | string | Yes | Your API key |

**Response (valid key):**
```json
{
  "key_valid": true,
  "plan": "starter",
  "quota_gb": 10.0,
  "used_gb": 3.2,
  "remaining_gb": 6.8,
  "usage_percent": 32,
  "network": "High volume residential IP pool available",
  "countries_available": 195,
  "best_countries": ["US", "GB", "CA", "DE", "IN", "FR", "BR", "AU", "JP", "KR"],
  "suggestion": "Your key is healthy. 68% quota remaining."
}
```

**Response (invalid key):**
```json
{
  "key_valid": false,
  "error": "API key not found",
  "fix": "Sign up at https://iploop.io/signup.html"
}
```

**Example:**
```bash
curl -s "https://gateway.iploop.io:9443/api/support/diagnose?api_key=YOUR_KEY"
```

---

### 3. GET /api/support/errors/{code}

Look up error codes and fixes. **No auth required.**

**Supported codes:** 407, 403, 502, 503, 504, 429

**Response:**
```json
{
  "code": 407,
  "meaning": "Proxy Authentication Required — invalid or missing API key",
  "causes": ["Typo in proxy password", "Key not activated", "Quota exceeded"],
  "fix": "Check api_key in proxy password field. Format: user:YOUR_API_KEY-country-US",
  "docs": "https://docs.iploop.io/errors/407"
}
```

**Example:**
```bash
curl -s https://gateway.iploop.io:9443/api/support/errors/407
```

---

### 4. POST /api/support/ask

Ask a question about the service. **Auth required.**

**Body:**
```json
{
  "question": "why am I getting timeouts?"
}
```

**Topics handled:** countries, quota, pricing, errors, timeouts, speed, availability

**Response:**
```json
{
  "answer": "For best performance, use country-US which has the highest availability...",
  "related": {}
}
```

**Example:**
```bash
curl -s -X POST "https://gateway.iploop.io:9443/api/support/ask?api_key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "what countries do you support?"}'
```

---

## Rate Limits

Every API response includes rate limit headers:

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | Max requests per minute for your plan |
| X-RateLimit-Remaining | Requests remaining in current window |
| X-RateLimit-Reset | Unix timestamp when limit resets |

**Limits by plan:**

| Plan | Requests/min |
|------|-------------|
| Free | 30 |
| Rewarded | 120 |
| Starter | 120 |
| Growth | 300 |
| Business | 600 |
| Enterprise | 1000+ |

---

## Proxy Usage

**HTTP CONNECT:**
```bash
curl -x http://user:YOUR_API_KEY-country-US@gateway.iploop.io:8880 https://httpbin.org/ip
```

**Python:**
```python
proxies = {
    "http": "http://user:YOUR_API_KEY-country-US@gateway.iploop.io:8880",
    "https": "http://user:YOUR_API_KEY-country-US@gateway.iploop.io:8880"
}
requests.get("https://httpbin.org/ip", proxies=proxies)
```

**Targeting options:**
- `country-US` — target country
- `city-miami` — target city
- `session-abc123` — sticky session
- Combine: `YOUR_KEY-country-US-city-miami-session-abc`

---

## Quick Start for Bots

1. Sign up: `POST /api/auth/signup` with `{"email": "...", "password": "..."}`
2. Check status: `GET /api/support/status`
3. Test your key: `GET /api/support/diagnose?api_key=YOUR_KEY`
4. Use proxy: `curl -x http://user:KEY-country-US@gateway.iploop.io:8880 https://target.com`
5. Monitor quota: `GET /api/support/diagnose?api_key=YOUR_KEY`
6. Handle errors: `GET /api/support/errors/{code}`

---

© 2026 IPLoop.io
