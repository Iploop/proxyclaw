#!/usr/bin/env bash
set -euo pipefail

echo "=== ProxyClaw Setup ==="

# Check API key
if [ -z "${IPLOOP_API_KEY:-}" ]; then
  echo "❌ IPLOOP_API_KEY is not set."
  echo ""
  echo "Get your API key:"
  echo "  1. Sign up at https://iploop.io"
  echo "  2. Or via API:"
  echo '     curl -X POST https://gateway.iploop.io:9443/api/auth/signup \'
  echo '       -H "Content-Type: application/json" \'
  echo '       -d '"'"'{"email":"you@example.com","password":"your_password"}'"'"
  echo ""
  echo "Then: export IPLOOP_API_KEY=\"your_key\""
  exit 1
fi

echo "✅ IPLOOP_API_KEY is set"

# Test connectivity
echo "Testing proxy connectivity..."
RESULT=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 \
  -x "http://user:${IPLOOP_API_KEY}@gateway.iploop.io:8880" \
  https://httpbin.org/ip 2>/dev/null || echo "000")

if [ "$RESULT" = "200" ]; then
  echo "✅ Proxy connection successful"
else
  echo "⚠️  Proxy returned HTTP $RESULT (may need valid API key)"
fi

# Check for HTML→MD converter
if command -v nhm &>/dev/null; then
  echo "✅ node-html-markdown (nhm) available"
else
  echo "ℹ️  node-html-markdown not installed (optional)"
  echo "   Install: npm install -g node-html-markdown"
fi

echo ""
echo "Setup complete! Try: ./fetch.sh https://example.com"
