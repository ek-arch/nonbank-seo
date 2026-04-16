"""
data_sources.py — Nonbank SEO Intelligence Agent
All data, API clients, and scoring logic in one place.

Nonbank starts with no legacy: historical platform metrics are empty by
design. Populate the dicts below as real data comes in (GA4 exports, card
issuer reports, etc.). The structure is kept so downstream pages render
without errors against an empty dataset.
"""

import requests
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# STATIC DATA — starter scaffolding, no historical backfill.
# Fill in as real data becomes available.
# ─────────────────────────────────────────────────────────────────────────────

DATA = {
    # Platform-level aggregate stats. Zeroed until we have real data.
    "platform": {
        "period": "—",
        "pre_cashback":  {"label": "—", "active_users": 0, "transactions": 0, "card_spend": 0, "avg_daily_spend": 0, "avg_daily_tx": 0},
        "post_cashback": {"label": "—", "active_users": 0, "transactions": 0, "card_spend": 0, "avg_daily_spend": 0, "avg_daily_tx": 0},
    },
    # Monthly P&L — empty arrays until we have real months.
    "pnl": {
        "months":          [],
        "card_spend_fee":  [],
        "swap_fees":       [],
        "topup_fees":      [],
        "issuance_fees":   [],
        "withdrawal_fees": [],
        "total_revenue":   [],
        "cashback_cost":   [],
        "net_pnl":         [],
    },
    # Country performance. Schema:
    # {"country", "flag", "tier" (1/2/3), "card_users", "card_spend",
    #  "revenue", "spend_per_user", "conversion"}
    "countries": [],
    # Language cluster performance. Schema:
    # {"lang", "code", "card_users", "total_spend", "spend_per_user"}
    "languages": [],
    # Funnel: registered → onboarded → card_requested → card_active → has_spent.
    "acquisition_funnel": [],
    # Content locale map: native-language vs English user distribution per country.
    "content_locale_map": [],
    # Product feature popularity (active_cards, deposit_volume) per country+lang.
    "product_features": [],
    # Cashback unit economics. Zeroed.
    "cashback_unit_economics": {
        "roi_pct": 0.0, "cac_cashback": 0, "cac_cpa": 0,
        "cac_seo_low": 0, "cac_seo_high": 0,
        "revenue_per_user": 0, "net_per_user": 0,
        "spend_multiplier": 0, "total_cashback_users": 0,
    },
    # SEO revenue/cost forecast. Placeholder scenarios for the Monthly Eval page.
    "seo_forecast": {
        "conservative": {"revenue": 0, "cost": 2000, "roi": 0.0},
        "mid":          {"revenue": 0, "cost": 2000, "roi": 0.0},
        "optimistic":   {"revenue": 0, "cost": 2000, "roi": 0.0},
    },
    # Card issuance allowance — same issuer as Kolo (card is Kolo under the hood).
    # Wallet itself is global DeFi (no geo restrictions). Card has issuer restrictions.
    # Source: Kolo Hex "Card Issuance & Spend Restrictions" — updated 2026-03-12.
    "card_allowance": {
        "can_issue": {
            "europe": [
                "FRA", "DEU", "GBR", "NLD", "POL", "FIN", "SWE", "ESP", "ITA", "CHE",
                "CZE", "AUT", "ROU", "BGR", "NOR", "PRT", "LTU", "CYP", "LUX", "EST",
                "GRC", "HUN", "SRB", "SVK", "HRV", "SVN", "MLT", "ISL", "AND", "LIE",
                "MCO", "MDA",
            ],
            "asia_pacific": [
                "IDN", "SGP", "JPN", "KOR", "MYS", "THA", "HKG", "AUS", "NZL",
            ],
            "latam_caribbean": [
                "BRA", "ARG", "COL", "MEX", "PER", "CRI", "URY", "CHL",
            ],
            "central_asia_caucasus": [
                "GEO", "AZE", "UZB", "KGZ", "ARM",
            ],
            "middle_east": [
                "BHR", "ARE",
            ],
            "french_overseas": [
                "REU", "GLP", "MTQ", "GUF",
            ],
        },
        "cannot_issue": [
            "RUS", "BLR", "VEN", "CUB", "IRN", "SYR", "PRK", "UKR",
            "TUR", "ISR", "CHN", "IND", "VNM", "NPL", "IRQ", "KAZ",
        ],
        "cannot_spend": [
            "SYR", "IRN", "CUB", "PRK", "RUS", "UKR", "VEN",
        ],
        "note": "Wallet is global DeFi (no geo restrictions). Card uses Kolo issuer — "
                "same geography. The US is NOT a supported market for card issuance.",
        "updated": "2026-03-12",
    },
    # Outlet shortlist — empty for Nonbank (build via Outlet Matching research).
    # Legacy key "march_outlets" kept so other pages referencing it don't crash.
    "march_outlets": {},
}


# ─────────────────────────────────────────────────────────────────────────────
# COLLABORATOR.PRO API CLIENT
# Status: /api/public/creator/list requires manual support activation.
# ─────────────────────────────────────────────────────────────────────────────

COLLAB_BASE = "https://collaborator.pro/api/public"


def fetch_collaborator_sites(token: str, category: str = "crypto", max_price: int = 500) -> list:
    """Fetch outlet catalog. Returns [] until API is activated by support."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"category": category, "_price_max": max_price, "sort": "price"}
    resp = requests.get(f"{COLLAB_BASE}/creator/list", headers=headers, params=params)
    if resp.status_code != 200:
        return []
    return resp.json().get("data", [])


def score_outlet_notion(
    search_pct: Optional[float],
    dr: Optional[float],
    price: float,
    category_fit: int,
    monthly_traffic: Optional[int],
    ai_citability: int = 0,
) -> int:
    """Score outlet 0–18 using 6-dimension system (SEO + GEO).

    Dimension 1 – Search traffic %:  >50%=3, 40-50%=2, 35-40%=1, <35%=0
    Dimension 2 – DR:                >65=3,  50-65=2,  40-50=1,  <40=0
    Dimension 3 – Price / DR point:  <$2=3,  $2-4=2,   $4-6=1,   >$6=0
    Dimension 4 – Category fit:      Crypto+Finance=3, Crypto+Other=2, Finance=1, Irrelevant=0
    Dimension 5 – Monthly traffic:   >100K=3, 30-100K=2, 5-30K=1, <5K=0
    Dimension 6 – AI Citability (GEO): Frequently cited=3, Occasionally=2, Rarely=1, Never=0

    Score thresholds: 15-18=Buy immediately, 11-14=Buy if budget, 7-10=Consider, <7=Skip
    Must-Have filters: search>35%, DR>40, Crypto/Finance/Business category, price<$5/DR
    """
    sp  = search_pct or 0
    d   = dr or 0
    p   = price or 0
    t   = monthly_traffic or 0
    pdr = (p / d) if d else 999

    s1 = 3 if sp > 50  else (2 if sp > 40 else (1 if sp >= 35 else 0))
    s2 = 3 if d > 65   else (2 if d >= 50 else (1 if d >= 40 else 0))
    s3 = 3 if pdr < 2  else (2 if pdr <= 4 else (1 if pdr <= 6 else 0))
    s4 = min(max(category_fit, 0), 3)
    s5 = 3 if t > 100000 else (2 if t >= 30000 else (1 if t >= 5000 else 0))
    s6 = min(max(ai_citability, 0), 3)

    return s1 + s2 + s3 + s4 + s5 + s6


def outlet_verdict(score: Optional[int]) -> str:
    """Map score (0-18) to buy/skip verdict."""
    if score is None: return "— Unscored"
    if score >= 15:   return "✅ Must buy"
    if score >= 11:   return "🟡 Buy if budget"
    if score >= 7:    return "🟠 Consider only"
    return "🔴 Skip"


def passes_must_haves(site: dict) -> bool:
    """Check Notion guide Must-Have criteria: search>35%, DR>40, price<$5/DR."""
    sp  = site.get("traffic_share") or 0
    d   = site.get("dr") or 0
    p   = site.get("price") or 0
    pdr = (p / d) if d else 999
    return sp >= 35 and d >= 40 and pdr < 5


def can_issue_card(country_code: str) -> bool:
    """Check if Nonbank can issue cards to residents of a country (ISO 3166-1 alpha-3)."""
    allowance = DATA.get("card_allowance", {})
    cannot = set(allowance.get("cannot_issue", []))
    if country_code.upper() in cannot:
        return False
    can = allowance.get("can_issue", {})
    all_allowed = set()
    for region_codes in can.values():
        all_allowed.update(region_codes)
    return country_code.upper() in all_allowed


def get_card_allowance_flat() -> list[str]:
    """Return flat list of all country codes where card issuance is allowed."""
    can = DATA.get("card_allowance", {}).get("can_issue", {})
    codes = []
    for region_codes in can.values():
        codes.extend(region_codes)
    return codes
