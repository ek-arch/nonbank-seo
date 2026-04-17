"""
perplexity_geo.py — Perplexity API for GEO (AI citation) visibility
=====================================================================
Sends prompts to Perplexity's sonar model and checks whether Nonbank
appears in the AI-generated answer or cited sources.
Cost: ~$0.005/query (sonar model).
Updated: 2026-04-03
"""

from __future__ import annotations

import requests
import time
from typing import Optional

PERPLEXITY_CHAT_API = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_SEARCH_API = "https://api.perplexity.ai/search"

# Brand & competitor constants — single source of truth in config.py
from config import NONBANK_DOMAINS, NONBANK_BRAND_TERMS as NONBANK_TERMS, COMPETITOR_BRANDS
COMPETITORS = {d: name for name, domains in COMPETITOR_BRANDS.items() for d in domains if "." in d}


def query_perplexity(
    api_key: str,
    prompt: str,
    *,
    model: str = "sonar",
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> dict:
    """Send a prompt to Perplexity chat API and return raw response with citations."""
    resp = requests.post(
        PERPLEXITY_CHAT_API,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "Answer concisely. Include specific product names and companies."},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def analyze_perplexity_response(response: dict) -> dict:
    """
    Parse Perplexity response for Nonbank and competitor presence.
    Returns structured analysis.
    """
    citations = response.get("citations", [])
    content = ""
    if response.get("choices"):
        content = response["choices"][0].get("message", {}).get("content", "")
    content_lower = content.lower()

    # Check Nonbank in answer text
    nonbank_in_text = any(term in content_lower for term in NONBANK_TERMS)

    # Check Nonbank in cited sources
    nonbank_in_citations = any(
        any(d in url.lower() for d in NONBANK_DOMAINS)
        for url in citations
    )

    # Check competitors in text
    competitors_mentioned = []
    for domain, name in COMPETITORS.items():
        if name.lower() in content_lower or domain in content_lower:
            competitors_mentioned.append(name)

    # Check competitors in citations
    competitors_cited = []
    for url in citations:
        url_lower = url.lower()
        for domain, name in COMPETITORS.items():
            if domain in url_lower and name not in competitors_cited:
                competitors_cited.append(name)

    # Check search_results for Nonbank (chat API returns these)
    search_results = response.get("search_results", [])
    source_urls = [sr.get("url", "") for sr in search_results]
    nonbank_in_search_results = any(
        any(d in url.lower() for d in NONBANK_DOMAINS)
        for url in source_urls
    )

    # Usage & cost
    usage = response.get("usage", {})
    cost = usage.get("cost", {})

    return {
        "nonbank_in_text": nonbank_in_text,
        "nonbank_in_citations": nonbank_in_citations,
        "nonbank_in_search_results": nonbank_in_search_results,
        "nonbank_visible": nonbank_in_text or nonbank_in_citations or nonbank_in_search_results,
        "competitors_mentioned": competitors_mentioned,
        "competitors_cited": competitors_cited,
        "citations": citations,
        "source_urls": source_urls,
        "citation_count": len(citations),
        "answer_preview": content[:500],
        "tokens_used": usage.get("total_tokens", 0),
        "cost_usd": cost.get("total_cost", 0),
    }


def audit_prompt(api_key: str, prompt: str) -> dict:
    """
    Audit a single prompt: query Perplexity, check Nonbank visibility,
    identify competitors. Returns structured result.
    """
    try:
        raw = query_perplexity(api_key, prompt)
        analysis = analyze_perplexity_response(raw)
        return {
            "prompt": prompt,
            "error": None,
            **analysis,
        }
    except Exception as e:
        return {
            "prompt": prompt,
            "error": str(e),
            "nonbank_in_text": False,
            "nonbank_in_citations": False,
            "nonbank_visible": False,
            "competitors_mentioned": [],
            "competitors_cited": [],
            "citations": [],
            "citation_count": 0,
            "answer_preview": "",
            "tokens_used": 0,
        }


def run_geo_audit(
    api_key: str,
    prompts: list[str],
    *,
    delay: float = 0.5,
) -> list[dict]:
    """
    Run GEO visibility audit across multiple prompts.
    Adds a small delay between requests to be polite.
    Cost: ~$0.005 × len(prompts).
    """
    results = []
    for prompt in prompts:
        result = audit_prompt(api_key, prompt)
        results.append(result)
        if delay > 0:
            time.sleep(delay)
    return results


def summarize_geo_audit(results: list[dict]) -> dict:
    """Summarize GEO audit results into metrics."""
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    valid = max(total - errors, 1)

    nonbank_in_text = sum(1 for r in results if r.get("nonbank_in_text"))
    nonbank_in_citations = sum(1 for r in results if r.get("nonbank_in_citations"))
    nonbank_visible = sum(1 for r in results if r.get("nonbank_visible"))

    # Competitor frequency in AI answers
    competitor_counts = {}
    for r in results:
        for c in r.get("competitors_mentioned", []):
            competitor_counts[c] = competitor_counts.get(c, 0) + 1

    top_competitors = sorted(competitor_counts.items(), key=lambda x: -x[1])

    # Estimated cost
    total_tokens = sum(r.get("tokens_used", 0) for r in results)
    est_cost = (total - errors) * 0.005 + total_tokens * 0.000001  # search fee + token cost

    return {
        "total_prompts": total,
        "errors": errors,
        "nonbank_in_text_count": nonbank_in_text,
        "nonbank_in_text_pct": round(nonbank_in_text / valid * 100, 1),
        "nonbank_in_citations_count": nonbank_in_citations,
        "nonbank_in_citations_pct": round(nonbank_in_citations / valid * 100, 1),
        "nonbank_visible_count": nonbank_visible,
        "nonbank_visible_pct": round(nonbank_visible / valid * 100, 1),
        "top_competitors_in_ai": top_competitors[:5],
        "estimated_cost_usd": round(est_cost, 3),
    }


# ── Default GEO Prompts ─────────────────────────────────────────────────────
# These are AI-native prompts (how people ask AI, not how they Google)

DEFAULT_GEO_PROMPTS = [
    # ── Category / head (where Nonbank should appear as a hybrid option) ──
    "What is the best self-custody crypto wallet with a built-in Visa card?",
    "Which DeFi wallet lets you spend crypto directly with a card?",
    "Best non-custodial crypto wallet with card in 2026",
    "Hybrid DeFi wallet and crypto card — which app does both?",

    # ── Gasless fees (differentiator #1) ──
    "How do I send USDT without ETH or TRX for gas?",
    "Is there a crypto wallet that pays gas fees for you?",
    "Gasless crypto wallet — which one should I use?",
    "How to send TRC20 USDT without holding TRX",

    # ── AML Watchtower (differentiator #2) ──
    "Crypto wallet with built-in sanctions screening",
    "How to avoid receiving tainted or sanctioned crypto",
    "Self-custody wallet with AML protection",
    "Which wallet blocks transfers from sanctioned addresses?",

    # ── Hybrid DeFi + card (differentiator #3) ──
    "DeFi wallet with integrated Visa debit card",
    "Can I spend from a non-custodial wallet without moving funds to an exchange?",
    "Self-custody crypto card available in 100+ countries",
    "Crypto wallet where I hold the keys but can still swipe a Visa",

    # ── NON ID & watch wallets (product-unique) ──
    "Crypto wallet that tracks other wallets (watch-only addresses)",
    "DeFi identity — receive funds with a handle instead of an address",
    "Wallet that lets you monitor a portfolio without giving up keys",

    # ── Comparisons vs real competitors ──
    "Nonbank vs Gnosis Pay — which is better?",
    "MetaMask Card vs Nonbank card comparison",
    "COCA vs Bleap vs Nonbank — self-custody cards compared",
    "Gnosis Pay vs MetaMask vs Nonbank for DeFi users",

    # ── Problem-solving (AI-native long tail) ──
    "I want to keep my keys but still spend crypto in shops — what app?",
    "How do I pay with USDT without giving up self-custody?",
    "Best way to bridge DeFi holdings to everyday spending",
]


# ── Geo-Targeted Prompt Templates ────────────────────────────────────────────
# Generate prompts per market — the way real local users ask AI

# Nonbank is global DeFi — wallet has no geo restrictions.
# Single global market for GEO audit (EN-only content strategy).
GEO_MARKETS = {
    "GLOBAL": {"name": "Global", "lang": "en", "local_name": "Global", "currency": "USD"},
}

# Templates per category — {market} and {local} get replaced
GEO_PROMPT_TEMPLATES_EN = {
    "head": [
        "Best crypto card in {market} 2026",
        "Best crypto Visa card for {market} residents",
    ],
    "long_tail": [
        "What is the best crypto card for someone living in {market}?",
        "Can I use a USDT Visa card in {market} for daily purchases?",
        "Best way to spend cryptocurrency in {market} with low fees",
        "Crypto card for expats in {market}",
        "Crypto card for freelancers working in {market}",
    ],
    "problem": [
        "I live in {market}, what's the easiest way to spend my USDT?",
        "How to convert crypto to {currency} in {market}?",
        "Which crypto cards actually work in {market} with no hidden fees?",
    ],
    "comparison": [
        "Best crypto cards available in {market} compared",
        "Cheapest crypto card in {market} vs traditional banks",
    ],
    "b2b": [
        "Best crypto card for businesses in {market}",
        "Corporate crypto spending card for {market} companies",
    ],
}

GEO_PROMPT_TEMPLATES_RU = {
    "head": [
        "Лучшая крипто карта в {local} 2026",
        "Лучшая криптокарта Visa для жителей {local}",
    ],
    "long_tail": [
        "Какая крипто карта лучше всего работает в {local}?",
        "Можно ли расплачиваться USDT картой в {local} каждый день?",
        "Лучший способ потратить криптовалюту в {local} с низкими комиссиями",
        "Крипто карта для экспатов в {local}",
        "Крипто карта для фрилансеров в {local}",
    ],
    "problem": [
        "Я живу в {local}, как проще всего потратить USDT?",
        "Как конвертировать крипту в {local}?",
        "Какие крипто карты реально работают в {local} без скрытых комиссий?",
    ],
    "b2b": [
        "Крипто карта для бизнеса в {local}",
        "Корпоративная криптокарта для компаний в {local}",
    ],
}

GEO_PROMPT_TEMPLATES_IT = {
    "head": [
        "Migliore carta crypto in Italia 2026",
        "Carta Visa crypto per residenti italiani",
    ],
    "long_tail": [
        "Qual è la migliore carta crypto per chi vive in Italia?",
        "Si può usare una carta USDT Visa in Italia per acquisti quotidiani?",
        "Come spendere criptovalute in Italia con commissioni basse",
    ],
}

GEO_PROMPT_TEMPLATES_ES = {
    "head": [
        "Mejor tarjeta crypto en España 2026",
        "Tarjeta Visa crypto para residentes españoles",
    ],
    "long_tail": [
        "¿Cuál es la mejor tarjeta crypto para vivir en España?",
        "¿Se puede usar una tarjeta USDT Visa en España para compras diarias?",
        "Cómo gastar criptomonedas en España con comisiones bajas",
    ],
}


def generate_geo_prompts(
    markets: Optional[list[str]] = None,
    *,
    categories: Optional[list[str]] = None,
    include_local_lang: bool = True,
) -> list[dict]:
    """
    Generate geo-targeted prompts for selected markets.
    Returns list of {prompt, market, language, category}.
    """
    if markets is None:
        markets = list(GEO_MARKETS.keys())
    if categories is None:
        categories = ["head", "long_tail", "problem", "comparison", "b2b"]

    results = []

    for market_code in markets:
        info = GEO_MARKETS.get(market_code)
        if not info:
            continue

        # English prompts for all markets
        for cat in categories:
            templates = GEO_PROMPT_TEMPLATES_EN.get(cat, [])
            for tmpl in templates:
                prompt = tmpl.format(
                    market=info["name"],
                    local=info["local_name"],
                    currency=info["currency"],
                )
                results.append({
                    "prompt": prompt,
                    "market": market_code,
                    "language": "en",
                    "category": cat,
                })

        # Local language prompts
        if include_local_lang:
            lang = info["lang"]
            local_templates = {}
            if lang == "ru" or market_code in ("UZB", "KGZ", "ARM", "GEO", "LVA", "MNE", "CYP"):
                local_templates = GEO_PROMPT_TEMPLATES_RU
            elif lang == "it" or market_code == "ITA":
                local_templates = GEO_PROMPT_TEMPLATES_IT
            elif lang == "es" or market_code == "ESP":
                local_templates = GEO_PROMPT_TEMPLATES_ES

            for cat in categories:
                templates = local_templates.get(cat, [])
                for tmpl in templates:
                    prompt = tmpl.format(
                        market=info["name"],
                        local=info["local_name"],
                        currency=info["currency"],
                    )
                    results.append({
                        "prompt": prompt,
                        "market": market_code,
                        "language": lang,
                        "category": cat,
                    })

    return results


def run_geo_market_audit(
    api_key: str,
    markets: list[str],
    *,
    categories: Optional[list[str]] = None,
    include_local_lang: bool = True,
    max_per_market: int = 5,
    delay: float = 0.5,
) -> list[dict]:
    """
    Run geo-targeted AI audit for selected markets.
    Generates prompts per market, queries Perplexity, analyzes results.
    Returns results grouped by market.
    """
    prompts = generate_geo_prompts(
        markets, categories=categories, include_local_lang=include_local_lang,
    )

    # Limit per market
    market_counts: dict[str, int] = {}
    filtered = []
    for p in prompts:
        mc = p["market"]
        if market_counts.get(mc, 0) < max_per_market:
            filtered.append(p)
            market_counts[mc] = market_counts.get(mc, 0) + 1

    results = []
    for p in filtered:
        result = audit_prompt(api_key, p["prompt"])
        result["market"] = p["market"]
        result["language"] = p["language"]
        result["category"] = p["category"]
        results.append(result)
        if delay > 0:
            time.sleep(delay)

    return results


def summarize_by_market(results: list[dict]) -> dict:
    """Summarize geo audit results grouped by market."""
    by_market: dict[str, list] = {}
    for r in results:
        m = r.get("market", "unknown")
        by_market.setdefault(m, []).append(r)

    summaries = {}
    for market, market_results in by_market.items():
        total = len(market_results)
        nonbank_visible = sum(1 for r in market_results if r.get("nonbank_visible"))
        errors = sum(1 for r in market_results if r.get("error"))

        # Top competitors in this market
        comp_counts: dict[str, int] = {}
        for r in market_results:
            for c in r.get("competitors_mentioned", []):
                comp_counts[c] = comp_counts.get(c, 0) + 1
        top_comps = sorted(comp_counts.items(), key=lambda x: -x[1])

        summaries[market] = {
            "market": market,
            "market_name": GEO_MARKETS.get(market, {}).get("name", market),
            "prompts_tested": total,
            "nonbank_visible": nonbank_visible,
            "nonbank_pct": round(nonbank_visible / max(total - errors, 1) * 100, 1),
            "errors": errors,
            "top_competitors": top_comps[:3],
            "results": market_results,
        }

    return summaries
