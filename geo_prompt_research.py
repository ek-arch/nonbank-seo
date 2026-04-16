"""
geo_prompt_research.py — AI Prompt Discovery & GEO Tracking (Semrush-style)
============================================================================
Discovers what prompts real users ask AI about crypto cards, then tracks
whether Nonbank appears in AI-generated answers.

Two engines:
  1. Prompt Discovery — uses Claude to generate realistic AI prompts
     that real users would type into ChatGPT/Perplexity/Google AI
  2. Prompt Monitoring — queries Perplexity with each prompt, checks
     Nonbank mention/citation, counts brands & sources

Cost: ~$0.003/prompt (Perplexity sonar) + ~$0.001/batch (Claude Haiku for discovery)
"""
from __future__ import annotations

import json
import time
import os
import re
from datetime import datetime
from typing import Optional, List, Dict
from dataclasses import dataclass, field, asdict

import requests

# ── Constants ────────────────────────────────────────────────────────────────

PERPLEXITY_CHAT_API = "https://api.perplexity.ai/chat/completions"
ANTHROPIC_API = "https://api.anthropic.com/v1/messages"

# Brand & competitor constants — single source of truth in config.py
from config import NONBANK_DOMAINS, NONBANK_BRAND_TERMS as NONBANK_TERMS, COMPETITOR_BRANDS
COMPETITORS = {d: name for name, domains in COMPETITOR_BRANDS.items() for d in domains if "." in d}

# ── Prompt Discovery Categories ─────────────────────────────────────────────

DISCOVERY_CATEGORIES = {
    "hybrid_defi_card": {
        "label": "DeFi Wallet + Card (Hybrid)",
        "description": "Users looking for a DeFi wallet that also has a Visa card",
        "example": "Is there a DeFi wallet where I can spend my crypto directly with a Visa card?",
    },
    "gasless": {
        "label": "Gasless Transactions",
        "description": "Users looking for wallets that don't require native gas tokens",
        "example": "Which crypto wallet lets me send USDT without paying gas fees?",
    },
    "aml_compliance": {
        "label": "AML / Compliance",
        "description": "Users worried about sanctioned wallet transfers, compliance",
        "example": "How can I make sure my crypto wallet doesn't accept funds from sanctioned addresses?",
    },
    "watch_proxy": {
        "label": "Watch Wallets & Proxy Addresses",
        "description": "Users wanting to track wallets or use proxy addresses for privacy",
        "example": "Is there a crypto wallet where I can track other wallets and also have a spending card?",
    },
    "gnosis_pay_alt": {
        "label": "Gnosis Pay / Non-Custodial Card Alternatives",
        "description": "Users comparing Gnosis Pay, MetaMask Card, Bleap, COCA, or looking for alternatives",
        "example": "What's a better alternative to Gnosis Pay that works outside the EU?",
    },
    "custodial_vs_defi": {
        "label": "Custodial vs DeFi Wallet Decision",
        "description": "Users deciding between custodial (Crypto.com, Binance) and DeFi wallet with card",
        "example": "Should I use Crypto.com card or a DeFi wallet with an integrated Visa card?",
    },
    "how_to": {
        "label": "How-To / Problem Solving",
        "description": "Users asking how to accomplish something with DeFi + card",
        "example": "How do I spend crypto from my hardware wallet without moving it to an exchange?",
    },
    "use_case": {
        "label": "Use Case",
        "description": "Specific use cases: travel, freelancing, self-custody spending",
        "example": "Best way to spend self-custody crypto while traveling without giving up keys",
    },
}

# Markets to generate geo-specific prompts for
# Nonbank is global DeFi — no geo-specific markets needed.
# Keep a small set for geo-targeted prompt discovery (EN only).
TARGET_MARKETS = {
    "Global": {"langs": ["en"], "local": "Global"},
}


# ── Pre-built Prompt Database (no API needed) ───────────────────────────────

BUILTIN_PROMPTS = [
    # ── Hybrid DeFi Wallet + Card ─────────────────────────────────
    {"prompt": "Is there a DeFi wallet with an integrated Visa card?", "category": "hybrid_defi_card", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "best non-custodial wallet that also has a spending card 2026", "category": "hybrid_defi_card", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "crypto wallet where I keep my keys but can still spend with a card", "category": "hybrid_defi_card", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "DeFi wallet card that works in 100+ countries", "category": "hybrid_defi_card", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "hybrid crypto wallet custodial card combination", "category": "hybrid_defi_card", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "spend crypto from self custody wallet with visa", "category": "hybrid_defi_card", "language": "en", "market": "Global", "intent": "informational"},

    # ── Gasless Transactions ──────────────────────────────────────
    {"prompt": "crypto wallet that doesn't require gas fees to send USDT", "category": "gasless", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "gasless crypto transactions how do they work", "category": "gasless", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "best gas-free wallet for transferring stablecoins", "category": "gasless", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "send crypto without paying gas which wallets support this", "category": "gasless", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "meta transactions explained for crypto users", "category": "gasless", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "I don't have ETH for gas how can I send my USDT", "category": "gasless", "language": "en", "market": "Global", "intent": "informational"},

    # ── AML / Compliance ──────────────────────────────────────────
    {"prompt": "crypto wallet with built in AML screening", "category": "aml_compliance", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "how to avoid receiving crypto from sanctioned wallets", "category": "aml_compliance", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "is my self custody wallet AML compliant", "category": "aml_compliance", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "crypto wallet that blocks dirty coins automatically", "category": "aml_compliance", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "best compliant non custodial wallet 2026", "category": "aml_compliance", "language": "en", "market": "Global", "intent": "transactional"},

    # ── Watch Wallets & Proxy Addresses ───────────────────────────
    {"prompt": "crypto wallet app with watch only addresses", "category": "watch_proxy", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "track multiple crypto wallets in one app", "category": "watch_proxy", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "portfolio tracker with a linked spending card", "category": "watch_proxy", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "what is a proxy address in crypto", "category": "watch_proxy", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "crypto privacy wallet with proxy addresses", "category": "watch_proxy", "language": "en", "market": "Global", "intent": "informational"},

    # ── Gnosis Pay / Non-Custodial Card Alternatives ──────────────
    {"prompt": "Gnosis Pay alternative that works globally not just EU", "category": "gnosis_pay_alt", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "MetaMask Card alternative 2026", "category": "gnosis_pay_alt", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "Bleap vs COCA vs Gnosis Pay which is best", "category": "gnosis_pay_alt", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "non custodial crypto card that works in 100 countries", "category": "gnosis_pay_alt", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "best self custody crypto card without gas fees", "category": "gnosis_pay_alt", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "is Gnosis Pay available outside Europe", "category": "gnosis_pay_alt", "language": "en", "market": "Global", "intent": "informational"},

    # ── Custodial vs DeFi Wallet ──────────────────────────────────
    {"prompt": "should I use Crypto.com card or a DeFi wallet card", "category": "custodial_vs_defi", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "DeFi wallet vs Crypto.com for daily spending", "category": "custodial_vs_defi", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "pros and cons of non custodial crypto cards", "category": "custodial_vs_defi", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "why would I use a DeFi wallet instead of Binance card", "category": "custodial_vs_defi", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "self custody crypto card vs exchange card comparison", "category": "custodial_vs_defi", "language": "en", "market": "Global", "intent": "informational"},

    # ── How-To ────────────────────────────────────────────────────
    {"prompt": "how to spend crypto from my hardware wallet directly", "category": "how_to", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "how to get a crypto card without moving funds to an exchange", "category": "how_to", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "how to connect my DeFi wallet to a Visa card", "category": "how_to", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "how to spend USDT without bridging or converting first", "category": "how_to", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "how do I keep my keys and still use a card for payments", "category": "how_to", "language": "en", "market": "Global", "intent": "informational"},

    # ── Use Cases ─────────────────────────────────────────────────
    {"prompt": "best self custody crypto card for digital nomads", "category": "use_case", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "DeFi wallet card for freelancers paid in stablecoins", "category": "use_case", "language": "en", "market": "Global", "intent": "transactional"},
    {"prompt": "crypto card for traveling without giving up keys", "category": "use_case", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "spend crypto at restaurants without exchange deposit", "category": "use_case", "language": "en", "market": "Global", "intent": "informational"},
    {"prompt": "non custodial wallet for power DeFi users who also want a card", "category": "use_case", "language": "en", "market": "Global", "intent": "transactional"},
]


def get_builtin_prompts(
    categories: Optional[List[str]] = None,
    markets: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
) -> List[dict]:
    """Return filtered built-in prompts (no API call needed)."""
    results = BUILTIN_PROMPTS
    if categories:
        results = [p for p in results if p["category"] in categories]
    if markets:
        results = [p for p in results if p["market"] in markets or p["market"] == "global"]
    if languages:
        results = [p for p in results if p["language"] in languages]
    return results


# ── Prompt Discovery via Claude ─────────────────────────────────────────────

DISCOVERY_SYSTEM_PROMPT = """You are an AI prompt researcher for Nonbank (nonbank.io), a DeFi wallet with
an integrated custodial Visa card. Nonbank is a HYBRID model — non-custodial wallet (user holds keys)
with a seamlessly integrated card (Kolo issuer, 100+ countries). Key differentiators:
  1. Gasless fees — send crypto without paying gas (fees deducted from purchase)
  2. Built-in AML Watchtower — automatic blocking of sanctioned wallet transfers
  3. Hybrid DeFi+card bridge — unlike Gnosis Pay (fully on-chain EU/UK only),
     unlike Crypto.com/Binance (fully custodial), unlike MetaMask (no card live)
  4. Watch wallets & proxy addresses
  5. NON ID (DeFi identity)

Your job: generate realistic prompts that REAL users would type into ChatGPT / Perplexity / Google AI
when looking for solutions Nonbank COULD answer.

Rules:
- Write prompts exactly as a real person would type them — natural, conversational
- Include typos, informal language, incomplete sentences where realistic
- Mix question formats: "What's the best...", "How do I...", "Can I...", "I need a..."
- Focus on the DIFFERENTIATORS above — prompts where Nonbank has a genuine answer
- Include competitor-alternative prompts (Gnosis Pay alt, MetaMask Card alt, Bleap vs Nonbank, etc.)
- Avoid generic "best crypto card 2026" prompts — too competitive, dominated by Crypto.com/Binance
- DO NOT focus on USDT/TRC20 exclusively — Nonbank supports multiple chains
- DO NOT generate geo-specific prompts (UAE, Italy, etc) unless explicitly requested — wallet is global
- Each prompt should be distinct in intent — no near-duplicates
- Include some very specific long-tail prompts (these are GEO gold)

Output format: Return ONLY a JSON array of objects, each with:
{"prompt": "...", "category": "...", "language": "...", "market": "Global", "intent": "informational|transactional|navigational"}

No markdown, no explanation — just the JSON array."""


def discover_prompts_claude(
    api_key: str,
    *,
    categories: Optional[List[str]] = None,
    markets: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    count_per_category: int = 10,
    existing_prompts: Optional[List[str]] = None,
) -> List[dict]:
    """
    Use Claude to generate realistic AI prompts that users would ask
    about crypto cards. Returns list of prompt dicts.
    """
    if categories is None:
        categories = list(DISCOVERY_CATEGORIES.keys())
    if markets is None:
        markets = list(TARGET_MARKETS.keys())
    if languages is None:
        languages = ["en"]

    cat_descriptions = "\n".join(
        f"- {k}: {v['description']} (e.g. \"{v['example']}\")"
        for k, v in DISCOVERY_CATEGORIES.items()
        if k in categories
    )

    market_list = ", ".join(markets)
    lang_list = ", ".join(languages)

    dedup_block = ""
    if existing_prompts:
        sample = existing_prompts[:30]
        dedup_block = f"\n\nAVOID duplicating these existing prompts:\n" + "\n".join(f"- {p}" for p in sample)

    user_msg = f"""Generate {count_per_category} realistic AI prompts per category for Nonbank — a DeFi wallet with integrated custodial Visa card (hybrid model, gasless fees, built-in AML, watch wallets). Target queries where Nonbank's differentiators give it a genuine answer.

Categories:
{cat_descriptions}

Target markets: {market_list}
Languages: {lang_list}
Total prompts needed: ~{count_per_category * len(categories)}

CRITICAL — prompts MUST be about Nonbank's differentiators:
- Hybrid DeFi wallet + integrated Visa card (self-custody keys + card in one app)
- Gasless transactions (no ETH/TRX needed for gas)
- Built-in AML screening (sanctioned wallet blocking)
- Watch wallets & proxy addresses
- Alternatives to Gnosis Pay, MetaMask Card, Bleap, COCA

FORBIDDEN — do NOT generate these Kolo-era prompts:
- Generic "best crypto card 2026" / "best crypto debit card"
- USDT-specific or TRC20-specific prompts (Nonbank is multi-chain)
- Geo-specific prompts (UAE, Dubai, Italy, Spain, UK, Poland, CIS, etc.)
- Comparisons of Crypto.com vs Wirex vs Bybit vs Binance card
- Cashback rates, conversion fees, hidden fees, monthly fees queries
- KYC-avoidance prompts

Make prompts natural — the way real DeFi-literate users type into ChatGPT or Perplexity.
Include a mix of:
- Short queries ("defi wallet with card")
- Full questions ("Is there a wallet where I hold my keys but can still spend with Visa?")
- Problem statements ("I want to spend crypto without giving up self-custody")
- Competitor-alternative requests ("Gnosis Pay alternative that works globally")
{dedup_block}

Return ONLY the JSON array."""

    resp = requests.post(
        ANTHROPIC_API,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 4096,
            "system": DISCOVERY_SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": user_msg}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    text = data["content"][0]["text"]

    # Parse JSON from response
    try:
        # Try direct parse first
        prompts = json.loads(text)
    except json.JSONDecodeError:
        # Extract JSON array from text
        match = re.search(r'\[[\s\S]*\]', text)
        if match:
            prompts = json.loads(match.group())
        else:
            prompts = []

    return prompts


# ── Prompt Monitoring via Perplexity ─────────────────────────────────────────

@dataclass
class PromptResult:
    prompt: str
    category: str
    language: str
    market: str
    intent: str
    # Results
    mentioned: str = "0/1"  # "1/1" if Nonbank appears
    nonbank_in_text: bool = False
    nonbank_in_citations: bool = False
    nonbank_visible: bool = False
    brands_count: int = 0
    brands_list: List[str] = field(default_factory=list)
    sources_count: int = 0
    sources_list: List[str] = field(default_factory=list)
    competitors_in_text: List[str] = field(default_factory=list)
    answer_preview: str = ""
    error: Optional[str] = None
    timestamp: str = ""

    def to_dict(self):
        return asdict(self)


def monitor_prompt(
    perplexity_key: str,
    prompt: str,
    *,
    model: str = "sonar",
) -> dict:
    """
    Query Perplexity with a prompt, analyze for Nonbank and competitor presence.
    Returns raw analysis dict.
    """
    try:
        resp = requests.post(
            PERPLEXITY_CHAT_API,
            headers={
                "Authorization": f"Bearer {perplexity_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "Answer concisely with specific product names, companies, and websites. Include pros and cons."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 1024,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": str(e)}

    # Extract answer text
    content = ""
    if data.get("choices"):
        content = data["choices"][0].get("message", {}).get("content", "")
    content_lower = content.lower()

    # Citations
    citations = data.get("citations", [])
    search_results = data.get("search_results", [])
    source_urls = [sr.get("url", "") for sr in search_results]
    all_sources = list(set(citations + source_urls))

    # Nonbank detection
    nonbank_in_text = any(term in content_lower for term in NONBANK_TERMS)
    nonbank_in_citations = any(
        any(d in url.lower() for d in NONBANK_DOMAINS)
        for url in all_sources
    )

    # Competitor detection
    competitors_in_text = []
    competitors_in_sources = []
    all_brands = []

    for domain, name in COMPETITORS.items():
        in_text = name.lower() in content_lower or domain in content_lower
        in_src = any(domain in url.lower() for url in all_sources)
        if in_text:
            competitors_in_text.append(name)
            all_brands.append(name)
        if in_src and name not in competitors_in_sources:
            competitors_in_sources.append(name)
            if name not in all_brands:
                all_brands.append(name)

    # Add Nonbank to brands if present
    if nonbank_in_text or nonbank_in_citations:
        all_brands.insert(0, "Nonbank")

    return {
        "nonbank_in_text": nonbank_in_text,
        "nonbank_in_citations": nonbank_in_citations,
        "nonbank_visible": nonbank_in_text or nonbank_in_citations,
        "brands_count": len(all_brands),
        "brands_list": all_brands,
        "sources_count": len(all_sources),
        "sources_list": all_sources,
        "competitors_in_text": competitors_in_text,
        "answer_preview": content[:600],
        "error": None,
    }


def monitor_prompts_batch(
    perplexity_key: str,
    prompts: List[dict],
    *,
    delay: float = 0.5,
    progress_callback=None,
) -> List[PromptResult]:
    """
    Monitor a batch of prompts. Each prompt dict should have:
    {prompt, category, language, market, intent}
    """
    results = []
    total = len(prompts)

    for i, p in enumerate(prompts):
        prompt_text = p.get("prompt", "")
        analysis = monitor_prompt(perplexity_key, prompt_text)

        result = PromptResult(
            prompt=prompt_text,
            category=p.get("category", "unknown"),
            language=p.get("language", "en"),
            market=p.get("market", "global"),
            intent=p.get("intent", "informational"),
            mentioned="1/1" if analysis.get("nonbank_visible") else "0/1",
            nonbank_in_text=analysis.get("nonbank_in_text", False),
            nonbank_in_citations=analysis.get("nonbank_in_citations", False),
            nonbank_visible=analysis.get("nonbank_visible", False),
            brands_count=analysis.get("brands_count", 0),
            brands_list=analysis.get("brands_list", []),
            sources_count=analysis.get("sources_count", 0),
            sources_list=analysis.get("sources_list", []),
            competitors_in_text=analysis.get("competitors_in_text", []),
            answer_preview=analysis.get("answer_preview", ""),
            error=analysis.get("error"),
            timestamp=datetime.utcnow().isoformat(),
        )
        results.append(result)

        if progress_callback:
            progress_callback(i + 1, total, result)

        if delay > 0 and i < total - 1:
            time.sleep(delay)

    return results


# ── Analysis & Reporting ─────────────────────────────────────────────────────

def summarize_results(results: List[PromptResult]) -> dict:
    """Semrush-style summary of monitoring results."""
    total = len(results)
    errors = sum(1 for r in results if r.error)
    valid = max(total - errors, 1)

    nonbank_visible = sum(1 for r in results if r.nonbank_visible)
    nonbank_in_text = sum(1 for r in results if r.nonbank_in_text)
    nonbank_in_citations = sum(1 for r in results if r.nonbank_in_citations)

    # Competitor frequency
    comp_counts = {}
    for r in results:
        for c in r.competitors_in_text:
            comp_counts[c] = comp_counts.get(c, 0) + 1

    # By category
    by_category = {}
    for r in results:
        cat = r.category
        if cat not in by_category:
            by_category[cat] = {"total": 0, "visible": 0}
        by_category[cat]["total"] += 1
        if r.nonbank_visible:
            by_category[cat]["visible"] += 1

    # By market
    by_market = {}
    for r in results:
        m = r.market
        if m not in by_market:
            by_market[m] = {"total": 0, "visible": 0}
        by_market[m]["total"] += 1
        if r.nonbank_visible:
            by_market[m]["visible"] += 1

    # By language
    by_lang = {}
    for r in results:
        lang = r.language
        if lang not in by_lang:
            by_lang[lang] = {"total": 0, "visible": 0}
        by_lang[lang]["total"] += 1
        if r.nonbank_visible:
            by_lang[lang]["visible"] += 1

    return {
        "total_prompts": total,
        "errors": errors,
        "nonbank_visible": nonbank_visible,
        "nonbank_visible_pct": round(nonbank_visible / valid * 100, 1),
        "nonbank_in_text": nonbank_in_text,
        "nonbank_in_citations": nonbank_in_citations,
        "missing": valid - nonbank_visible,
        "missing_pct": round((valid - nonbank_visible) / valid * 100, 1),
        "top_competitors": sorted(comp_counts.items(), key=lambda x: -x[1])[:10],
        "avg_brands_per_prompt": round(sum(r.brands_count for r in results if not r.error) / valid, 1),
        "avg_sources_per_prompt": round(sum(r.sources_count for r in results if not r.error) / valid, 1),
        "by_category": by_category,
        "by_market": by_market,
        "by_language": by_lang,
    }


def find_opportunities(results: List[PromptResult]) -> List[dict]:
    """
    Find prompts where Nonbank is NOT mentioned but competitors ARE.
    These are the best opportunities for GEO improvement.
    """
    opportunities = []
    for r in results:
        if not r.nonbank_visible and r.brands_count > 0 and not r.error:
            opportunities.append({
                "prompt": r.prompt,
                "category": r.category,
                "market": r.market,
                "language": r.language,
                "competitors_present": r.competitors_in_text,
                "brands_count": r.brands_count,
                "sources_count": r.sources_count,
                "priority": "high" if r.brands_count >= 3 else "medium",
            })

    # Sort: more competitors = higher priority
    opportunities.sort(key=lambda x: -x["brands_count"])
    return opportunities


# ── Persistence ──────────────────────────────────────────────────────────────

CACHE_DIR = os.path.join(os.path.dirname(__file__), "geo_cache")


def save_results(results: List[PromptResult], filename: Optional[str] = None):
    """Save monitoring results to JSON cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    if filename is None:
        filename = f"geo_monitor_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(CACHE_DIR, filename)
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "count": len(results),
        "results": [r.to_dict() for r in results],
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path


def load_results(filename: str) -> List[PromptResult]:
    """Load monitoring results from JSON cache."""
    path = os.path.join(CACHE_DIR, filename)
    with open(path) as f:
        data = json.load(f)
    results = []
    for d in data.get("results", []):
        r = PromptResult(
            prompt=d["prompt"],
            category=d.get("category", ""),
            language=d.get("language", "en"),
            market=d.get("market", "global"),
            intent=d.get("intent", "informational"),
            mentioned=d.get("mentioned", "0/1"),
            nonbank_in_text=d.get("nonbank_in_text", False),
            nonbank_in_citations=d.get("nonbank_in_citations", False),
            nonbank_visible=d.get("nonbank_visible", False),
            brands_count=d.get("brands_count", 0),
            brands_list=d.get("brands_list", []),
            sources_count=d.get("sources_count", 0),
            sources_list=d.get("sources_list", []),
            competitors_in_text=d.get("competitors_in_text", []),
            answer_preview=d.get("answer_preview", ""),
            error=d.get("error"),
            timestamp=d.get("timestamp", ""),
        )
        results.append(r)
    return results


def list_cached_results() -> List[dict]:
    """List all cached result files."""
    if not os.path.exists(CACHE_DIR):
        return []
    files = []
    for f in sorted(os.listdir(CACHE_DIR), reverse=True):
        if f.endswith(".json"):
            path = os.path.join(CACHE_DIR, f)
            try:
                with open(path) as fh:
                    data = json.load(fh)
                files.append({
                    "filename": f,
                    "timestamp": data.get("timestamp", ""),
                    "count": data.get("count", 0),
                })
            except Exception:
                pass
    return files
