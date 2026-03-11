#!/usr/bin/env bash
set -euo pipefail

# ProxyClaw fetch — route requests through IPLoop residential proxies
# Usage: ./fetch.sh <URL> [--country CC] [--city CITY] [--session ID] [--asn ASN] [--format raw|markdown] [--timeout N]

URL=""
COUNTRY=""
CITY=""
SESSION_ID=""
ASN=""
FORMAT="raw"
TIMEOUT=30

# ── Input parsing ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    --country)  COUNTRY="$2";    shift 2 ;;
    --city)     CITY="$2";       shift 2 ;;
    --session)  SESSION_ID="$2"; shift 2 ;;
    --asn)      ASN="$2";        shift 2 ;;
    --format)   FORMAT="$2";     shift 2 ;;
    --timeout)  TIMEOUT="$2";    shift 2 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) URL="$1"; shift ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Usage: ./fetch.sh <URL> [--country CC] [--city CITY] [--session ID] [--asn ASN] [--format raw|markdown] [--timeout N]" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  ./fetch.sh https://example.com" >&2
  echo "  ./fetch.sh https://example.com --country US --format markdown" >&2
  echo "  ./fetch.sh https://httpbin.org/ip --country DE" >&2
  echo "  ./fetch.sh https://example.com --country US --city newyork" >&2
  echo "  ./fetch.sh https://example.com --session mysession" >&2
  echo "  ./fetch.sh https://example.com --asn 12345" >&2
  exit 1
fi

# ── Input validation ──
# Validate URL (must start with http:// or https://)
if [[ ! "$URL" =~ ^https?:// ]]; then
  echo "Error: URL must start with http:// or https://" >&2
  exit 1
fi

# Normalize and validate country code (exactly 2 uppercase letters)
if [ -n "$COUNTRY" ]; then
  COUNTRY="${COUNTRY^^}"
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
# Auth is passed via --proxy-user to prevent exposure in `ps aux`
AUTH="user:${IPLOOP_API_KEY}"
[ -n "$COUNTRY" ]    && AUTH="${AUTH}-country-${COUNTRY}"
[ -n "$CITY" ]       && AUTH="${AUTH}-city-${CITY}"
[ -n "$SESSION_ID" ] && AUTH="${AUTH}-session-${SESSION_ID}"
[ -n "$ASN" ]        && AUTH="${AUTH}-asn-${ASN}"

# ── Temp file with guaranteed cleanup ──
TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

# ── Fetch ──
# %{content_type} captured in-band — no second request needed
CURL_OUT=$(curl -s -o "$TMPFILE" -w "%{http_code} %{content_type}" \
  --max-time "$TIMEOUT" \
  --proxy "http://proxy.iploop.io:8880" \
  --proxy-user "$AUTH" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.9" \
  "$URL" 2>/dev/null) || {
  echo "Error: Request failed (timeout or connection error)" >&2
  exit 1
}

HTTP_CODE=$(echo "$CURL_OUT" | awk '{print $1}')
CONTENT_TYPE=$(echo "$CURL_OUT" | awk '{print $2}')

if [ "$HTTP_CODE" -ge 400 ]; then
  echo "Error: HTTP $HTTP_CODE from $URL" >&2
  cat "$TMPFILE" >&2
  exit 1
fi

CONTENT=$(cat "$TMPFILE")

# ── Output ──
if [ "$FORMAT" = "markdown" ]; then
  # Only attempt HTML conversion for text/html responses
  IS_HTML=false
  [[ "$CONTENT_TYPE" == *"text/html"* ]] && IS_HTML=true
  # Fallback: sniff content if Content-Type header was absent
  if [ "$IS_HTML" = false ] && echo "$CONTENT" | grep -qi '<html'; then
    IS_HTML=true
  fi

  if [ "$IS_HTML" = true ]; then
    if command -v nhm &>/dev/null; then
      echo "$CONTENT" | nhm
    else
      # Fallback: remove <script>/<style> blocks, strip remaining tags
      echo "⚠️  nhm not installed — using basic HTML stripper (install: npm install -g node-html-markdown)" >&2
      echo "$CONTENT" \
        | sed -e '/<script/,/<\/script>/d' \
              -e '/<style/,/<\/style>/d' \
              -e 's/<[^>]*>//g' \
              -e '/^[[:space:]]*$/d' || true
    fi
  else
    # Not HTML (JSON, plain text, etc.) — output as-is
    echo "$CONTENT"
  fi
else
  echo "$CONTENT"
fi
