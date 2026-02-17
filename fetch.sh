#!/usr/bin/env bash
set -euo pipefail

# ProxyClaw fetch — fetch a URL through IPLoop residential proxy
# Usage: ./fetch.sh <URL> [--country CC] [--format raw|markdown] [--timeout N]

URL=""
COUNTRY=""
FORMAT="raw"
TIMEOUT=30

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
  echo "Examples:" >&2
  echo "  ./fetch.sh https://example.com" >&2
  echo "  ./fetch.sh https://example.com --country US --format markdown" >&2
  exit 1
fi

if [ -z "${IPLOOP_API_KEY:-}" ]; then
  echo "Error: IPLOOP_API_KEY not set. Run ./setup.sh first." >&2
  exit 1
fi

# Build auth string
AUTH="user:${IPLOOP_API_KEY}"
[ -n "$COUNTRY" ] && AUTH="user:${IPLOOP_API_KEY}-country-${COUNTRY}"

PROXY="http://${AUTH}@gateway.iploop.io:8880"

# Fetch
CONTENT=$(curl -s --max-time "$TIMEOUT" -x "$PROXY" "$URL")

# Convert to markdown if requested
if [ "$FORMAT" = "markdown" ]; then
  if command -v nhm &>/dev/null; then
    echo "$CONTENT" | nhm
  else
    # Fallback: strip HTML tags with sed
    echo "$CONTENT" | sed -e 's/<[^>]*>//g' -e '/^[[:space:]]*$/d'
  fi
else
  echo "$CONTENT"
fi
