#!/usr/bin/env python3
"""
IPLoop Support AI — HTTP endpoint for customer/bot queries
POST /chat  {"question": "..."}  →  {"answer": "..."}

Uses knowledge base + pattern matching + fallback to helpful links.
"""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

KNOWLEDGE_BASE = {'about': {'keywords': ['what is iploop', 'about iploop', 'what do you do', 'tell me about'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'pricing': {'keywords': ['cost', 'price', 'pricing', 'how much', 'free plan', 'free tier', 'plans', 'payment', 'pay'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'countries': {'keywords': ['countr', 'geo', 'location', 'target', 'region', 'city'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'python_sdk': {'keywords': ['python', 'pip install', 'pip'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'node_sdk': {'keywords': ['node', 'npm', 'javascript', 'js sdk'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'endpoint': {'keywords': ['endpoint', 'proxy url', 'proxy address', 'curl', 'connect'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'sessions': {'keywords': ['sticky', 'session', 'same ip', 'rotate', 'rotation'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'antibot': {'keywords': ['cloudflare', 'anti-bot', 'antibot', 'bypass', 'block', 'stealth', 'captcha', 'protect'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'serp': {'keywords': ['serp', 'google search', 'search results', 'startpage', 'verification', 'unusual traffic', 'raw google'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'sites': {'keywords': ['site', 'preset', 'supported site', 'which site', 'what site', 'scrape'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'ethical': {'keywords': ['gdpr', 'ccpa', 'ethical', 'legal', 'comply', 'compliance', 'sourced', 'source', 'legit'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'protocols': {'keywords': ['protocol', 'socks', 'http', 'https'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'signup': {'keywords': ['api key', 'sign up', 'register', 'account', 'get started', 'start'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'proxyclaw': {'keywords': ['proxyclaw', 'difference', 'api.proxyclaw'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'fleet': {'keywords': ['how many', 'fleet', 'nodes', 'ips', 'pool size'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'success': {'keywords': ['success rate', 'reliable', 'uptime', 'stable'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'speed': {'keywords': ['fast', 'speed', 'latency', 'slow', 'performance'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'datacenter': {'keywords': ['datacenter', 'data center', 'dc proxy'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'troubleshoot': {'keywords': ['not working', 'error', 'fail', 'timeout', '403', 'blocked', 'issue', 'problem', 'help'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'china': {'keywords': ['china', 'russia', 'iran', 'restricted'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'api': {'keywords': ['api', 'rest api', 'http api'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}, 'earnclaw': {'keywords': ['earn', 'earnclaw', 'bandwidth', 'share', 'money', 'credit'], 'answer': 'For new V2 accounts: https://platform.iploop.io/ . Use separate proxy username/password; the API key is for account access. Current setup: https://proxyclaw.ai/docs.html . Country routing and sticky sessions are available subject to live pool availability. State/city targeting is V2 pending server deployment. Check dashboard pricing/balance; no universal anti-bot, free quota or rewards guarantee. Support: support@iploop.io'}}

# Greeting patterns
GREETINGS = ["hi", "hello", "hey", "sup", "yo", "greetings", "good morning", "good afternoon"]

def find_answer(question: str) -> dict:
    q = question.lower().strip()
    
    # Greetings
    if q in GREETINGS or any(q.startswith(g + " ") or q == g for g in GREETINGS):
        return {
            "answer": "Hey! 👋 I'm IPLoop Support AI. I can help with:\n• Pricing & plans\n• SDK setup (Python/Node.js)\n• Proxy configuration\n• Anti-bot bypass\n• Troubleshooting\n\nWhat do you need?",
            "category": "greeting",
            "confidence": 1.0
        }
    
    # Score each category
    best_score = 0
    best_key = None
    
    for key, data in KNOWLEDGE_BASE.items():
        score = 0
        for kw in data["keywords"]:
            if kw in q:
                # Longer keyword matches = higher confidence
                score += len(kw.split())
        if score > best_score:
            best_score = score
            best_key = key
    
    if best_key and best_score > 0:
        return {
            "answer": KNOWLEDGE_BASE[best_key]["answer"],
            "category": best_key,
            "confidence": min(best_score / 3, 1.0)
        }
    
    # Fallback
    return {
        "answer": "I can help with IPLoop pricing, setup, features, and troubleshooting.\n\n• Docs: https://proxyclaw.ai/docs.html\n• Sign up: https://platform.iploop.io/\n• Contact: partners@iploop.io\n\nCould you rephrase your question?",
        "category": "fallback",
        "confidence": 0.0
    }


class SupportHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            question = body.get("question", body.get("q", ""))
            
            result = find_answer(question)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "categories": len(KNOWLEDGE_BASE)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Quiet


if __name__ == "__main__":
    # Test mode
    print("=" * 60)
    print("  IPLoop Support AI — Full Test Suite")
    print("=" * 60)
    
    all_questions = [
        # Core questions (should all match)
        "What is IPLoop?",
        "How much does it cost?",
        "Is there a free plan?",
        "What countries do you support?",
        "How do I install the Python SDK?",
        "How do I use the proxy with curl?",
        "What's the proxy endpoint?",
        "How do I target a specific country?",
        "How do sticky sessions work?",
        "Can I scrape Amazon?",
        "Does it bypass Cloudflare?",
        "What sites are supported?",
        "How does stealth mode work?",
        "Can I scrape Zillow?",
        "What about anti-bot protection?",
        "How are the IPs sourced?",
        "Is it GDPR compliant?",
        "What protocols are supported?",
        "How do I get an API key?",
        "Can I use this for web scraping?",
        "Do you have a Node.js SDK?",
        "What's the difference between IPLoop and ProxyClaw?",
        "How many IPs do you have?",
        "What's the success rate?",
        # Edge cases
        "hi",
        "hello",
        "help me",
        "I need to scrape 1 million pages",
        "do you have datacenter proxies?",
        "what payment methods do you accept?",
        "my proxy is not working",
        "can I use this in China?",
        "what is your uptime?",
        "do you have an API?",
        "how fast is it?",
        "what about EarnClaw?",
        "how do I earn credits?",
    ]
    
    categories = {}
    for q in all_questions:
        result = find_answer(q)
        cat = result["category"]
        conf = result["confidence"]
        icon = "✅" if cat != "fallback" else "⚠️"
        categories[cat] = categories.get(cat, 0) + 1
        print(f"{icon} [{cat:12s}] {conf:.1f} | {q}")
        if cat == "fallback":
            print(f"   → FALLBACK")
    
    matched = sum(1 for q in all_questions if find_answer(q)["category"] != "fallback")
    print(f"\n{'=' * 60}")
    print(f"  {matched}/{len(all_questions)} matched ({matched/len(all_questions)*100:.0f}%)")
    print(f"  Categories hit: {dict(sorted(categories.items()))}")
    print(f"{'=' * 60}")
