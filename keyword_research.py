"""
keyword_research.py — Competitive keyword intelligence for Nonbank SEO Agent
==========================================================================
Three data sources:
  1. Ahrefs API/MCP — competitor organic keywords, volumes, difficulty
  2. SerpAPI — "People Also Ask" + related searches (free expansion)
  3. Manual seed list — curated from market data

Builds a ranked keyword taxonomy:
  Head → Mid-tail → Long-tail → Comparison → Problem-solving
Split by market, language, and competition level.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import requests


# ── Keyword Categories ───────────────────────────────────────────────────────

@dataclass
class Keyword:
    """A single keyword with all research data."""
    keyword: str
    language: str = "en"
    market: str = "global"           # ISO3 country code or "global"/"EU"
    category: str = "generic"         # head / mid_tail / long_tail / comparison / problem / b2b / branded
    intent: str = "transactional"     # transactional / informational / navigational
    # Volume & competition (from Ahrefs)
    volume: Optional[int] = None      # monthly search volume
    difficulty: Optional[int] = None  # keyword difficulty 0-100
    cpc: Optional[float] = None       # cost per click USD
    # SERP features
    has_ai_overview: bool = False
    has_featured_snippet: bool = False
    # Competitor presence
    competitor_domains: list[str] = field(default_factory=list)
    nonbank_ranking: Optional[int] = None
    # GEO visibility (from Perplexity)
    ai_nonbank_visible: Optional[bool] = None
    ai_competitors_mentioned: list[str] = field(default_factory=list)
    # Scoring
    priority_score: float = 0.0       # computed composite score


def classify_keyword(kw: str) -> str:
    """Auto-classify a keyword into category."""
    kw_lower = kw.lower()
    if any(w in kw_lower for w in ["vs", "versus", "comparison", "compare", "better"]):
        return "comparison"
    if any(w in kw_lower for w in ["how to", "how can", "what is the", "can i", "is there", "easiest way", "cheapest way"]):
        return "problem"
    if any(w in kw_lower for w in ["business", "corporate", "b2b", "company", "invoice"]):
        return "b2b"
    if any(w in kw_lower for w in ["nonbank"]):
        return "branded"
    words = kw_lower.split()
    if len(words) <= 3:
        return "head"
    if len(words) <= 5:
        return "mid_tail"
    return "long_tail"


def detect_language(kw: str) -> str:
    """Simple language detection based on character sets."""
    if any('\u0400' <= c <= '\u04ff' for c in kw):
        return "ru"
    if any(c in kw for c in "àèéìòùç"):
        return "it"
    if any(c in kw for c in "áéíóúñ¿¡"):
        return "es"
    if any(c in kw for c in "ąćęłńóśźż"):
        return "pl"
    if any(c in kw for c in "ãõâê"):
        return "pt"
    return "en"


def detect_market(kw: str) -> str:
    """Detect target market from keyword text."""
    kw_lower = kw.lower()
    market_map = {
        "uk": "GBR", "united kingdom": "GBR", "britain": "GBR", "british": "GBR",
        "uae": "ARE", "dubai": "ARE", "emirates": "ARE", "оаэ": "ARE", "дубай": "ARE",
        "italy": "ITA", "italia": "ITA", "italian": "ITA", "италия": "ITA",
        "spain": "ESP", "españa": "ESP", "spanish": "ESP", "испания": "ESP",
        "poland": "POL", "polish": "POL", "polska": "POL", "польша": "POL",
        "europe": "EU", "european": "EU", "eu ": "EU", "европ": "EU",
        "indonesia": "IDN", "indonesian": "IDN",
        "romania": "ROU", "romanian": "ROU",
        "brazil": "BRA", "brazilian": "BRA", "brasil": "BRA",
        "germany": "DEU", "german": "DEU", "deutschland": "DEU",
        "latvia": "LVA", "latvian": "LVA",
        "georgia": "GEO", "грузия": "GEO",
        "uzbekistan": "UZB", "узбекистан": "UZB",
        "kazakhstan": "KAZ", "казахстан": "KAZ",
        "cis": "CIS", "снг": "CIS",
    }
    for term, market in market_map.items():
        if term in kw_lower:
            return market
    return "global"


def score_keyword(kw: Keyword) -> float:
    """
    Score a keyword for priority. Higher = more worth targeting.
    Factors:
      - Volume (log-scaled, max 30 pts)
      - Difficulty inversed (easy = high score, max 25 pts)
      - AI overview present (bonus 10 pts — means AI answers, GEO opportunity)
      - No Nonbank ranking yet (bonus 10 pts — untapped)
      - Category bonus: comparison +10, problem +8, b2b +8, long_tail +5
      - Market LTV weight (RU markets get 2x)
    """
    import math

    score = 0.0

    # Volume (0-30)
    if kw.volume and kw.volume > 0:
        score += min(math.log10(kw.volume) * 10, 30)

    # Difficulty inverse (0-25)
    if kw.difficulty is not None:
        score += max(0, 25 - kw.difficulty * 0.25)

    # AI overview present = GEO opportunity
    if kw.has_ai_overview:
        score += 10

    # Not ranking yet = untapped
    if kw.nonbank_ranking is None:
        score += 10
    elif kw.nonbank_ranking > 10:
        score += 5  # ranking but not on page 1

    # Category bonus (branded terms valued during brand-building phase)
    cat_bonus = {"comparison": 10, "problem": 8, "b2b": 8, "long_tail": 5, "mid_tail": 3, "branded": 2}
    score += cat_bonus.get(kw.category, 0)

    # Language weight — EN-only strategy for now (no RU/other content budget)
    lang_multiplier = {"en": 1.0}  # all non-EN languages get 1.0 default
    score *= lang_multiplier.get(kw.language, 1.0)

    return round(score, 1)


# ── Seed Keywords ────────────────────────────────────────────────────────────
# Derived from Nonbank's 3 differentiators + competitive positioning.
# Categories: differentiator-led, competitor comparison, market-specific, long-tail.

SEED_KEYWORDS: list[dict] = [
    # ── PILLAR 1: DeFi WALLET + CARD (HYBRID) ───────────────────────────
    {"q": "DeFi wallet with card", "lang": "en", "market": "global"},
    {"q": "crypto wallet with visa card", "lang": "en", "market": "global"},
    {"q": "best crypto card 2026", "lang": "en", "market": "global"},
    {"q": "crypto wallet card integration", "lang": "en", "market": "global"},
    {"q": "DeFi wallet vs gnosis pay", "lang": "en", "market": "global"},
    {"q": "crypto card 100 countries", "lang": "en", "market": "global"},

    # ── DIFFERENTIATOR 2: GASLESS FEES ───────────────────────────────────
    {"q": "gasless crypto transactions", "lang": "en", "market": "global"},
    {"q": "send crypto without gas fees", "lang": "en", "market": "global"},
    {"q": "no gas fee wallet", "lang": "en", "market": "global"},
    {"q": "gasless USDT transfer", "lang": "en", "market": "global"},
    {"q": "meta-transactions crypto wallet", "lang": "en", "market": "global"},

    # ── DIFFERENTIATOR 3: AML COMPLIANCE ─────────────────────────────────
    {"q": "AML crypto wallet", "lang": "en", "market": "global"},
    {"q": "self-custody AML compliance", "lang": "en", "market": "global"},
    {"q": "sanctioned wallet checker", "lang": "en", "market": "global"},
    {"q": "compliant non-custodial wallet", "lang": "en", "market": "global"},

    # ── WATCH WALLETS & PROXY ADDRESSES ──────────────────────────────────
    {"q": "crypto watch wallet", "lang": "en", "market": "global"},
    {"q": "proxy address crypto", "lang": "en", "market": "global"},
    {"q": "portfolio tracker wallet", "lang": "en", "market": "global"},
    {"q": "track multiple wallets one app", "lang": "en", "market": "global"},

    # ── COMPETITOR COMPARISONS ───────────────────────────────────────────
    {"q": "Nonbank vs Gnosis Pay", "lang": "en", "market": "global"},
    {"q": "Gnosis Pay alternative", "lang": "en", "market": "global"},
    {"q": "Nonbank vs MetaMask wallet", "lang": "en", "market": "global"},
    {"q": "MetaMask card alternative", "lang": "en", "market": "global"},
    {"q": "Nonbank vs COCA wallet", "lang": "en", "market": "global"},
    {"q": "Nonbank vs Bleap card", "lang": "en", "market": "global"},
    {"q": "non-custodial card comparison 2026", "lang": "en", "market": "global"},
    {"q": "custodial vs non-custodial crypto card", "lang": "en", "market": "global"},
    {"q": "best crypto card 2026", "lang": "en", "market": "global"},

    # ── HEAD TERMS ───────────────────────────────────────────────────────
    {"q": "crypto debit card", "lang": "en", "market": "global"},
    {"q": "best crypto wallet 2026", "lang": "en", "market": "global"},
    {"q": "crypto card low fees", "lang": "en", "market": "global"},

    # ── LONG-TAIL / PROBLEM-SOLVING ──────────────────────────────────────
    {"q": "how to spend crypto without custodian", "lang": "en", "market": "global"},
    {"q": "spend stablecoins with Visa card", "lang": "en", "market": "global"},
    {"q": "crypto card for digital nomads", "lang": "en", "market": "global"},
    {"q": "best way to spend crypto while traveling", "lang": "en", "market": "global"},

    # ── DeFi IDENTITY / WEB3 UX ────────────────────────────────────────
    {"q": "DeFi identity wallet", "lang": "en", "market": "global"},
    {"q": "crypto username wallet", "lang": "en", "market": "global"},
    {"q": "NFT identity crypto", "lang": "en", "market": "global"},
    {"q": "replace wallet address with username", "lang": "en", "market": "global"},
]


# ── Ahrefs Integration ───────────────────────────────────────────────────────

from config import COMPETITOR_DOMAINS_FLAT as COMPETITOR_DOMAINS


def fetch_ahrefs_organic_keywords(
    api_key: str,
    domain: str,
    *,
    country: str = "us",
    limit: int = 100,
) -> list[dict]:
    """
    Fetch organic keywords for a domain via Ahrefs API v3.
    Returns list of {keyword, volume, position, difficulty, cpc}.
    """
    url = "https://api.ahrefs.com/v3/site-explorer/organic-keywords"
    params = {
        "target": domain,
        "select": "keyword,volume,best_position,keyword_difficulty,cpc",
        "country": country,
        "limit": limit,
        "order_by": "volume:desc",
    }
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("keywords", data.get("items", []))


def fetch_ahrefs_keyword_overview(
    api_key: str,
    keywords: list[str],
    *,
    country: str = "us",
) -> list[dict]:
    """
    Get volume, difficulty, CPC for a batch of keywords.
    """
    url = "https://api.ahrefs.com/v3/keywords-explorer/overview"
    params = {
        "keywords": ",".join(keywords[:10]),  # API limit per request
        "country": country,
        "select": "keyword,volume,difficulty,cpc",
    }
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("keywords", data.get("items", []))


# ── SerpAPI Expansion (free keyword ideas) ───────────────────────────────────

def expand_keywords_serpapi(
    api_key: str,
    seed_query: str,
) -> dict:
    """
    Use SerpAPI to get 'People Also Ask' and 'Related Searches' for a query.
    Free way to discover long-tail keywords.
    """
    url = "https://serpapi.com/search.json"
    params = {
        "api_key": api_key,
        "engine": "google",
        "q": seed_query,
        "num": 10,
    }
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {"people_also_ask": [], "related_searches": []}

    paa = [item.get("question", "") for item in data.get("related_questions", [])]
    related = [item.get("query", "") for item in data.get("related_searches", [])]

    return {
        "people_also_ask": paa,
        "related_searches": related,
    }


# ── Build Keyword Taxonomy ───────────────────────────────────────────────────

def build_taxonomy(
    seeds: Optional[list[dict]] = None,
    ahrefs_key: Optional[str] = None,
) -> list[Keyword]:
    """
    Build keyword taxonomy from seeds + optional Ahrefs enrichment.
    Returns list of Keyword objects sorted by priority score.
    """
    if seeds is None:
        seeds = SEED_KEYWORDS

    keywords = []
    for seed in seeds:
        q = seed["q"]
        lang = seed.get("lang") or detect_language(q)
        market = seed.get("market") or detect_market(q)

        kw = Keyword(
            keyword=q,
            language=lang,
            market=market,
            category=classify_keyword(q),
            intent="informational" if any(w in q.lower() for w in ["how", "what", "can", "is there"]) else "transactional",
        )
        keywords.append(kw)

    # Enrich with Ahrefs if available
    if ahrefs_key:
        _enrich_with_ahrefs(keywords, ahrefs_key)

    # Score all
    for kw in keywords:
        kw.priority_score = score_keyword(kw)

    # Sort by priority
    keywords.sort(key=lambda k: -k.priority_score)
    return keywords


def _enrich_with_ahrefs(keywords: list[Keyword], api_key: str) -> None:
    """Enrich keywords with Ahrefs volume/difficulty data in-place."""
    # Batch by language → country mapping
    lang_country = {
        "en": "us", "ru": "ru", "it": "it", "es": "es",
        "pl": "pl", "pt": "br", "id": "id", "ro": "ro",
    }

    by_lang: dict[str, list[Keyword]] = {}
    for kw in keywords:
        by_lang.setdefault(kw.language, []).append(kw)

    for lang, kws in by_lang.items():
        country = lang_country.get(lang, "us")
        batch = [kw.keyword for kw in kws]

        # Process in batches of 10
        for i in range(0, len(batch), 10):
            chunk = batch[i:i+10]
            try:
                results = fetch_ahrefs_keyword_overview(api_key, chunk, country=country)
                # Map results back to Keyword objects
                result_map = {r.get("keyword", "").lower(): r for r in results}
                for kw in kws[i:i+10]:
                    r = result_map.get(kw.keyword.lower())
                    if r:
                        kw.volume = r.get("volume")
                        kw.difficulty = r.get("difficulty")
                        kw.cpc = r.get("cpc")
            except Exception:
                pass  # Ahrefs unavailable, continue with manual scores


def get_competitor_keywords(
    ahrefs_key: str,
    competitors: Optional[list[str]] = None,
    *,
    country: str = "us",
    limit_per_competitor: int = 50,
) -> list[Keyword]:
    """
    Pull top organic keywords from competitor domains via Ahrefs.
    Returns Keyword objects for keywords Nonbank doesn't rank for.
    """
    if competitors is None:
        competitors = COMPETITOR_DOMAINS

    all_kws: dict[str, Keyword] = {}

    for domain in competitors:
        try:
            results = fetch_ahrefs_organic_keywords(
                ahrefs_key, domain, country=country, limit=limit_per_competitor,
            )
            for r in results:
                q = r.get("keyword", "")
                if not q or q.lower() in all_kws:
                    continue
                # Filter: only crypto/card related
                if not any(term in q.lower() for term in ["crypto", "card", "usdt", "visa", "debit", "wallet", "stablecoin", "bitcoin", "gasless", "aml", "non-custodial", "defi", "self-custody", "watch wallet", "proxy"]):
                    continue
                kw = Keyword(
                    keyword=q,
                    language=detect_language(q),
                    market=detect_market(q),
                    category=classify_keyword(q),
                    volume=r.get("volume"),
                    difficulty=r.get("keyword_difficulty") or r.get("difficulty"),
                    cpc=r.get("cpc"),
                    competitor_domains=[domain],
                )
                all_kws[q.lower()] = kw
        except Exception:
            continue

    keywords = list(all_kws.values())
    for kw in keywords:
        kw.priority_score = score_keyword(kw)
    keywords.sort(key=lambda k: -k.priority_score)
    return keywords


# ── Export helpers ────────────────────────────────────────────────────────────

def taxonomy_to_dicts(keywords: list[Keyword]) -> list[dict]:
    """Convert Keyword list to list of dicts for DataFrame."""
    return [
        {
            "keyword": kw.keyword,
            "language": kw.language,
            "market": kw.market,
            "category": kw.category,
            "intent": kw.intent,
            "volume": kw.volume,
            "difficulty": kw.difficulty,
            "cpc": kw.cpc,
            "ai_overview": kw.has_ai_overview,
            "nonbank_ranking": kw.nonbank_ranking,
            "ai_nonbank_visible": kw.ai_nonbank_visible,
            "priority_score": kw.priority_score,
        }
        for kw in keywords
    ]


def filter_keywords(
    keywords: list[Keyword],
    *,
    language: Optional[str] = None,
    market: Optional[str] = None,
    category: Optional[str] = None,
    min_score: float = 0,
) -> list[Keyword]:
    """Filter keywords by criteria."""
    result = keywords
    if language:
        result = [k for k in result if k.language == language]
    if market:
        result = [k for k in result if k.market == market]
    if category:
        result = [k for k in result if k.category == category]
    if min_score > 0:
        result = [k for k in result if k.priority_score >= min_score]
    return result


# ── Keyword Matrix Generator ─────────────────────────────────────────────────
# Systematic: [product] × [market] × [language] × [intent modifier]

# ══════════════════════════════════════════════════════════════════════════
# KEYWORD MATRIX — Nonbank-focused, EN-global, no country/RU legacy
# Matrix dimensions: product × angle × modifier (no geo)
# ══════════════════════════════════════════════════════════════════════════

# Nonbank product terms (what users might call the thing they're looking for)
PRODUCTS = [
    "DeFi wallet with card",
    "non-custodial crypto card",
    "crypto wallet with visa card",
    "self-custody crypto card",
    "gasless crypto wallet",
    "hybrid crypto wallet",
    "crypto portfolio tracker with card",
    "watch-only wallet with card",
]

# Competitor brands — for alternative/vs queries
COMPETITOR_BRANDS_KW = [
    "Gnosis Pay", "MetaMask Card", "Bleap", "COCA",
    "Ether.fi Cash", "Crypto.com card", "Bitget wallet",
]

# User personas (who searches) — EN-global, no geo
PERSONAS_KW = [
    "digital nomads", "crypto freelancers", "DeFi users",
    "hardware wallet users", "stablecoin holders", "self-custody beginners",
    "power users", "remote workers",
]

# Nonbank differentiator-driven features
FEATURES_KW = [
    "gasless", "AML screening", "proxy address",
    "watch wallet", "100+ countries", "no gas fees",
    "hardware wallet integration",
]


INTENT_MODIFIERS = {
    "transactional": [
        "best {product}",
        "best {product} 2026",
        "top {product}",
        "{product} review",
    ],
    "comparison": [
        "{product} vs {competitor}",
        "{competitor} alternative",
        "best alternative to {competitor}",
        "{competitor} vs Nonbank",
    ],
    "problem_solution": [
        "how to {action}",
        "how do I {action}",
        "can I {action}",
    ],
    "persona": [
        "{product} for {persona}",
        "best {product} for {persona} 2026",
        "{product} for {persona} comparison",
    ],
    "feature": [
        "crypto wallet with {feature}",
        "crypto card with {feature}",
        "DeFi wallet {feature}",
        "{feature} crypto wallet",
    ],
    "long_tail": [
        "spend crypto without giving up keys",
        "crypto wallet that doesn't require gas",
        "send USDT without paying gas fees",
        "spend crypto from hardware wallet",
        "non-custodial card 100 countries",
        "DeFi wallet with integrated visa card",
        "crypto card from self custody",
        "wallet with built-in AML screening",
    ],
}

PROBLEM_ACTIONS = [
    "spend crypto without giving up self-custody",
    "send USDT without paying gas fees",
    "get a crypto visa card without an exchange",
    "track multiple wallets in one app",
    "spend crypto from a hardware wallet",
    "use a DeFi wallet with a visa card",
    "avoid sanctioned wallet transfers",
    "connect my bank and crypto wallet in one app",
]


def generate_keyword_matrix(
    *,
    include_comparisons: bool = True,
    include_personas: bool = True,
    include_features: bool = True,
    include_problems: bool = True,
    include_longtail: bool = True,
    products: Optional[list[str]] = None,
    competitors: Optional[list[str]] = None,
    personas: Optional[list[str]] = None,
    features: Optional[list[str]] = None,
) -> list[dict]:
    """
    Generate Nonbank-focused keyword matrix.

    Axes: product × (competitor | persona | feature | problem | intent).
    No country or language combinations — wallet is global DeFi, EN-only.

    Returns list of dicts with fields: q, lang, market, category, intent.
    `market` is always 'global' and `lang` is always 'en'.
    """
    products = products or PRODUCTS
    competitors = competitors or COMPETITOR_BRANDS_KW
    personas = personas or PERSONAS_KW
    features = features or FEATURES_KW

    results = []
    seen = set()

    def _add(q: str, category: str, intent: str):
        q = q.strip()
        key = q.lower()
        if key in seen or len(q) < 5:
            return
        seen.add(key)
        results.append({
            "q": q, "lang": "en", "market": "global",
            "category": category, "intent": intent,
        })

    # Transactional: "best {product}", etc.
    for product in products:
        for tmpl in INTENT_MODIFIERS["transactional"]:
            _add(tmpl.format(product=product), "transactional", "transactional")

    # Comparison × competitor
    if include_comparisons:
        for product in products[:4]:  # cap explosion
            for competitor in competitors:
                for tmpl in INTENT_MODIFIERS["comparison"]:
                    _add(
                        tmpl.format(product=product, competitor=competitor),
                        "comparison", "comparison",
                    )

    # Persona
    if include_personas:
        for product in products[:4]:
            for persona in personas:
                for tmpl in INTENT_MODIFIERS["persona"]:
                    _add(
                        tmpl.format(product=product, persona=persona),
                        "persona", "transactional",
                    )

    # Feature
    if include_features:
        for feature in features:
            for tmpl in INTENT_MODIFIERS["feature"]:
                _add(tmpl.format(feature=feature), "feature", "informational")

    # Problem / solution
    if include_problems:
        for action in PROBLEM_ACTIONS:
            for tmpl in INTENT_MODIFIERS["problem_solution"]:
                _add(tmpl.format(action=action), "problem", "informational")

    # Pure long-tail
    if include_longtail:
        for q in INTENT_MODIFIERS["long_tail"]:
            _add(q, "long_tail", "informational")

    return results


# ── Perplexity-powered keyword discovery ─────────────────────────────────────

def discover_keywords_perplexity(
    api_key: str,
    market: str,
    language: str = "en",
    *,
    max_results: int = 20,
) -> list[dict]:
    """
    Ask Perplexity: 'What do people search for about crypto cards in {market}?'
    Returns discovered keyword ideas with classification.
    Cost: ~$0.005/query.
    """
    lang_prompts = {
        "en": f"List the top {max_results} specific search queries people use when looking for crypto debit cards or crypto Visa cards in {market}. Include long-tail queries, local-language queries, and questions. Return ONLY the search queries, one per line, no numbering.",
        "ru": f"Перечисли {max_results} конкретных поисковых запросов, которые люди используют при поиске крипто карт или крипто Visa карт в {market}. Включи длинные запросы и вопросы. Верни ТОЛЬКО запросы, по одному на строку, без нумерации.",
    }

    prompt = lang_prompts.get(language, lang_prompts["en"])

    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 800,
                "temperature": 0.3,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return []

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

    # Parse lines
    keywords = []
    for line in content.strip().split("\n"):
        line = line.strip().lstrip("0123456789.-) ").strip('"').strip()
        if len(line) < 5 or len(line) > 120:
            continue
        lang = detect_language(line)
        kw_market = detect_market(line) or market
        keywords.append({
            "q": line,
            "lang": lang,
            "market": kw_market,
            "category": classify_keyword(line),
            "intent": "informational" if any(w in line.lower() for w in ["how", "what", "can", "is", "как", "что", "можно"]) else "transactional",
            "source": "perplexity_discovery",
        })

    return keywords[:max_results]


# ── Google Autocomplete (free, no API key) ───────────────────────────────────

def get_google_autocomplete(
    query: str,
    *,
    language: str = "en",
    country: str = "",
) -> list[str]:
    """
    Get Google Autocomplete suggestions. 100% free, no API key.
    Returns list of suggested queries.
    """
    params = {
        "q": query,
        "client": "firefox",
        "hl": language,
    }
    if country:
        params["gl"] = country

    try:
        resp = requests.get(
            "https://suggestqueries.google.com/complete/search",
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and len(data) > 1:
            return [s for s in data[1] if isinstance(s, str)]
    except Exception:
        pass
    return []


def expand_with_autocomplete(
    seed: str,
    *,
    language: str = "en",
    country: str = "",
    suffixes: Optional[list[str]] = None,
) -> list[dict]:
    """
    Expand a seed keyword using Google Autocomplete + alphabet trick.
    seed + " a", seed + " b", ... seed + " z" to discover more.
    Returns classified keyword dicts.
    """
    if suffixes is None:
        suffixes = [""] + list("abcdefghijklmnopqrstuvwxyz")

    all_suggestions = set()
    import time

    for suffix in suffixes:
        query = f"{seed} {suffix}".strip()
        suggestions = get_google_autocomplete(query, language=language, country=country)
        for s in suggestions:
            all_suggestions.add(s)
        time.sleep(0.1)  # polite

    results = []
    for s in sorted(all_suggestions):
        if s.lower() == seed.lower():
            continue
        lang = detect_language(s)
        market = detect_market(s)
        results.append({
            "q": s,
            "lang": lang or language,
            "market": market or "global",
            "category": classify_keyword(s),
            "intent": "informational" if any(w in s.lower() for w in ["how", "what", "can", "is", "как", "что"]) else "transactional",
            "source": "google_autocomplete",
        })

    return results


# ── Chain Discovery ──────────────────────────────────────────────────────────

def chain_discover(
    seeds: list[str],
    *,
    serpapi_key: Optional[str] = None,
    perplexity_key: Optional[str] = None,
    use_autocomplete: bool = True,
    language: str = "en",
    market: str = "global",
    max_depth: int = 1,
) -> list[dict]:
    """
    Chain multiple discovery methods from seeds:
    1. Google Autocomplete (free, unlimited)
    2. SerpAPI PAA + Related (1 credit/seed)
    3. Perplexity discovery (1 query/market, ~$0.005)

    Returns deduplicated, classified keyword list.
    """
    import time
    all_kws: dict[str, dict] = {}

    def _add(kw_dict: dict):
        key = kw_dict["q"].lower().strip()
        if key not in all_kws and len(key) >= 5:
            all_kws[key] = kw_dict

    # Layer 1: Autocomplete (free)
    if use_autocomplete:
        for seed in seeds:
            results = expand_with_autocomplete(seed, language=language)
            for r in results:
                _add(r)

    # Layer 2: SerpAPI PAA + Related
    if serpapi_key:
        for seed in seeds[:5]:  # limit to save credits
            expansion = expand_keywords_serpapi(serpapi_key, seed)
            for q in expansion.get("people_also_ask", []):
                _add({
                    "q": q, "lang": detect_language(q),
                    "market": detect_market(q) or market,
                    "category": classify_keyword(q),
                    "intent": "informational",
                    "source": "serpapi_paa",
                })
            for q in expansion.get("related_searches", []):
                _add({
                    "q": q, "lang": detect_language(q),
                    "market": detect_market(q) or market,
                    "category": classify_keyword(q),
                    "intent": "transactional",
                    "source": "serpapi_related",
                })
            time.sleep(1)

    # Layer 3: Perplexity discovery
    if perplexity_key:
        discovered = discover_keywords_perplexity(
            perplexity_key, market, language=language,
        )
        for d in discovered:
            _add(d)

    return list(all_kws.values())
