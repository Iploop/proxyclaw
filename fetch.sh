#!/usr/bin/env bash
set -euo pipefail

# ProxyClaw fetch — route requests through IPLoop residential proxies
# Usage: ./fetch.sh <URL> [--country CC] [--format raw|markdown] [--timeout N]

URL=""
COUNTRY=""
FORMAT="raw"
TIMEOUT=30

# ── Input parsing ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    --country) COUNTRY="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) URL="$1"; shift ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Usage: ./fetch.sh <URL> [--country CC] [--format raw|markdown] [--timeout N]" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  ./fetch.sh https://example.com" >&2
  echo "  ./fetch.sh https://example.com --country US --format markdown" >&2
  echo "  ./fetch.sh https://httpbin.org/ip --country DE" >&2
  exit 1
fi

# ── Input validation ──
# Validate URL (must start with http:// or https://)
if [[ ! "$URL" =~ ^https?:// ]]; then
  echo "Error: URL must start with http:// or https://" >&2
  exit 1
fi

# Validate country code (exactly 2 uppercase letters)
if [ -n "$COUNTRY" ]; then
  if [[ ! "$COUNTRY" =~ ^[A-Z]{2}$ ]]; then
    echo "Error: Country must be exactly 2 uppercase letters (e.g., US, DE, GB)" >&2
    exit 1
  fi
fi

# Validate timeout (positive integer 1-120)
if [[ ! "$TIMEOUT" =~ ^[0-9]+$ ]] || [ "$TIMEOUT" -lt 1 ] || [ "$TIMEOUT" -gt 120 ]; then
  echo "Error: Timeout must be 1-120 seconds" >&2
  exit 1
fi

# Validate format
if [[ "$FORMAT" != "raw" && "$FORMAT" != "markdown" ]]; then
  echo "Error: Format must be 'raw' or 'markdown'" >&2
  exit 1
fi

# ── API key check ──
if [ -z "${IPLOOP_API_KEY:-}" ]; then
  echo "Error: IPLOOP_API_KEY not set." >&2
  echo "Get your free key at https://iploop.io/signup.html" >&2
  echo "Then: export IPLOOP_API_KEY=\"your_key\"" >&2
  exit 1
fi

# ── Build proxy auth ──
AUTH="user:${IPLOOP_API_KEY}"
[ -n "$COUNTRY" ] && AUTH="user:${IPLOOP_API_KEY}-country-${COUNTRY}"

PROXY="http://${AUTH}@proxy.iploop.io:8880"

# ── Fetch ──
HTTP_CODE=$(curl -s -o /tmp/.proxyclaw_response -w "%{http_code}" --max-time "$TIMEOUT" -x "$PROXY" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.9" \
  "$URL" 2>/dev/null) || {
  echo "Error: Request failed (timeout or connection error)" >&2
  exit 1
}

if [ "$HTTP_CODE" -ge 400 ]; then
  echo "Error: HTTP $HTTP_CODE from $URL" >&2
  cat /tmp/.proxyclaw_response >&2
  rm -f /tmp/.proxyclaw_response
  exit 1
fi

CONTENT=$(cat /tmp/.proxyclaw_response)
rm -f /tmp/.proxyclaw_response

# ── Output ──
if [ "$FORMAT" = "markdown" ]; then
  if command -v nhm &>/dev/null; then
    echo "$CONTENT" | nhm
  else
    # Fallback: strip HTML tags
    echo "$CONTENT" | sed -e 's/<[^>]*>//g' -e '/^[[:space:]]*$/d'
  fi
else
  echo "$CONTENT"
fi
