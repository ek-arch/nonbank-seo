"""
geo_visibility.py — SerpAPI-powered GEO visibility tracking
============================================================
Queries Google via SerpAPI and checks whether Nonbank appears in results.
Also detects competitors and featured snippets.
Free tier: 100 searches/month at serpapi.com.
"""

import requests
from typing import Optional

# Brand & competitor constants — single source of truth in config.py
from config import NONBANK_DOMAINS, NONBANK_BRAND_TERMS, COMPETITOR_BRANDS
COMPETITORS = {d: name for name, domains in COMPETITOR_BRANDS.items() for d in domains if "." in d}

# Default queries to audit — mix of branded, generic, and geo-targeted
DEFAULT_QUERIES = [
    # Generic high-volume
    {"q": "best crypto card 2026", "intent": "transactional", "geo": "global"},
    {"q": "crypto debit card", "intent": "transactional", "geo": "global"},
    {"q": "USDT Visa card", "intent": "transactional", "geo": "global"},
    {"q": "spend crypto with Visa card", "intent": "informational", "geo": "global"},
    {"q": "best way to spend USDT", "intent": "informational", "geo": "global"},
    # Geo-targeted
    {"q": "crypto card Europe", "intent": "transactional", "geo": "EU"},
    {"q": "crypto card UK", "intent": "transactional", "geo": "GBR"},
    {"q": "crypto card Italy", "intent": "transactional", "geo": "ITA"},
    {"q": "carta crypto Italia 2026", "intent": "transactional", "geo": "ITA"},
    {"q": "crypto card UAE", "intent": "transactional", "geo": "ARE"},
    {"q": "crypto card digital nomad", "intent": "informational", "geo": "global"},
    # Product-specific
    {"q": "Telegram crypto wallet card", "intent": "transactional", "geo": "global"},
    {"q": "TRC20 USDT card", "intent": "transactional", "geo": "global"},
    {"q": "crypto card low fees", "intent": "transactional", "geo": "global"},
    {"q": "crypto card comparison 2026", "intent": "informational", "geo": "global"},
]


def search_serpapi(api_key: str, query: str, *, num: int = 10) -> dict:
    """Run a Google search via SerpAPI. Returns raw API response."""
    url = "https://serpapi.com/search.json"
    params = {
        "api_key": api_key,
        "engine": "google",
        "q": query,
        "num": min(num, 10),
    }
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def analyze_result(result: dict) -> dict:
    """Analyze a single search result for Nonbank/competitor presence."""
    link = result.get("link", "").lower()
    title = result.get("title", "").lower()
    snippet = result.get("snippet", "").lower()
    displayed_link = result.get("displayed_link", "").lower()

    # Check Nonbank presence
    nonbank_in_title = any(t in title for t in NONBANK_BRAND_TERMS)
    nonbank_in_snippet = any(t in snippet for t in NONBANK_BRAND_TERMS)
    nonbank_domain = any(d in link for d in NONBANK_DOMAINS)

    # Check competitor presence
    competitor = None
    for domain, name in COMPETITORS.items():
        if domain in displayed_link or domain in link:
            competitor = name
            break

    return {
        "title": result.get("title", ""),
        "link": result.get("link", ""),
        "snippet": result.get("snippet", "")[:200],
        "position": result.get("position", 0),
        "nonbank_domain": nonbank_domain,
        "nonbank_mentioned": nonbank_in_title or nonbank_in_snippet,
        "competitor": competitor,
    }


def audit_query(api_key: str, query: str) -> dict:
    """
    Audit a single query: search Google via SerpAPI, check Nonbank visibility,
    identify competitors. Returns a structured result.
    """
    try:
        data = search_serpapi(api_key, query)
    except Exception as e:
        return {
            "query": query,
            "error": str(e),
            "nonbank_visible": False,
            "nonbank_position": None,
            "competitors_found": [],
            "results": [],
            "total_results": 0,
        }

    organic = data.get("organic_results", [])
    total = int(data.get("search_information", {}).get("total_results", 0))

    analyzed = []
    nonbank_position = None
    competitors_found = []

    for item in organic:
        a = analyze_result(item)
        analyzed.append(a)

        if (a["nonbank_domain"] or a["nonbank_mentioned"]) and nonbank_position is None:
            nonbank_position = a["position"]

        if a["competitor"] and a["competitor"] not in competitors_found:
            competitors_found.append(a["competitor"])

    # Check AI overview / featured snippet
    ai_overview = None
    if data.get("ai_overview"):
        ai_text = str(data["ai_overview"]).lower()
        ai_overview = {
            "present": True,
            "nonbank_mentioned": any(t in ai_text for t in NONBANK_BRAND_TERMS),
        }

    featured_snippet = None
    if data.get("answer_box"):
        featured_snippet = data["answer_box"].get("title", "") or data["answer_box"].get("answer", "")

    return {
        "query": query,
        "error": None,
        "nonbank_visible": nonbank_position is not None,
        "nonbank_position": nonbank_position,
        "competitors_found": competitors_found,
        "top_result": organic[0].get("title", "") if organic else "",
        "top_result_domain": organic[0].get("displayed_link", "") if organic else "",
        "featured_snippet": featured_snippet,
        "ai_overview": ai_overview,
        "results": analyzed,
        "total_results": total,
    }


def run_full_audit(api_key: str, queries: Optional[list] = None) -> list[dict]:
    """
    Run visibility audit across all queries.
    Returns list of audit results.
    Free tier: 100 searches/month at serpapi.com.
    """
    if queries is None:
        queries = [q["q"] for q in DEFAULT_QUERIES]

    results = []
    for q in queries:
        result = audit_query(api_key, q)
        results.append(result)

    return results


def summarize_audit(results: list[dict]) -> dict:
    """Summarize audit results into metrics."""
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    nonbank_visible = sum(1 for r in results if r.get("nonbank_visible"))
    avg_position = None
    positions = [r["nonbank_position"] for r in results if r.get("nonbank_position")]
    if positions:
        avg_position = round(sum(positions) / len(positions), 1)

    # AI overview mentions
    ai_mentions = sum(
        1 for r in results
        if r.get("ai_overview") and r["ai_overview"].get("nonbank_mentioned")
    )

    # Competitor frequency
    competitor_counts = {}
    for r in results:
        for c in r.get("competitors_found", []):
            competitor_counts[c] = competitor_counts.get(c, 0) + 1

    # Sort by frequency
    top_competitors = sorted(competitor_counts.items(), key=lambda x: -x[1])

    return {
        "total_queries": total,
        "errors": errors,
        "nonbank_visible_count": nonbank_visible,
        "nonbank_visible_pct": round(nonbank_visible / max(total - errors, 1) * 100, 1),
        "avg_nonbank_position": avg_position,
        "ai_overview_mentions": ai_mentions,
        "top_competitors": top_competitors[:5],
        "visibility_score": f"{nonbank_visible}/{total - errors}",
    }
