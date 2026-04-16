"""
config.py — Constants and static data for Nonbank SEO & GEO Intelligence Agent
==============================================================================
Product profile, competitor matrix, content pillars, keyword seeds,
article briefs, outlet queries, and subreddit lists.

Nonbank (nonbank.io) — DeFi wallet with seamlessly integrated custodial Visa card
(NON×CARD, Kolo issuer under the hood, 100+ countries).
HYBRID model: non-custodial wallet + custodial card in one app.
Key differentiators: gasless fees, built-in AML, seamless DeFi-to-card bridge.
Note: portfolio integrations (exchanges, banks) are NOT live yet — current
features are: DeFi wallet, proxy addresses, watch wallets, card (Kolo).
All content is EN-global (wallet is borderless DeFi).
"""
from __future__ import annotations


# ═══════════════════════════════════════════════════════════════════════════════
# BRAND CONSTANTS — single source of truth for all engine modules
# Import these in perplexity_geo.py, geo_visibility.py, geo_prompt_research.py
# ═══════════════════════════════════════════════════════════════════════════════

NONBANK_DOMAINS: set[str] = {"nonbank.io", "www.nonbank.io", "t.me/nonbankers"}

NONBANK_BRAND_TERMS: set[str] = {
    "nonbank", "nonbank.io", "nonbank wallet", "nonbank visa",
    "nonbank card", "nonbank crypto", "non×card", "nonxcard", "nons",
}

# Full competitor dict — used by all GEO/visibility modules
COMPETITOR_BRANDS: dict[str, set[str]] = {
    "Gnosis Pay":  {"gnosispay.com", "gnosis pay", "gnosispay"},
    "MetaMask":    {"metamask.io", "metamask", "metamask card"},
    "COCA":        {"coca.xyz", "coca wallet", "coca card"},
    "Bleap":       {"bleap.finance", "bleap", "bleap card"},
    "Crypto.com":  {"crypto.com", "crypto.com card", "cryptocom"},
    "Bitget":      {"bitget.com", "bitget wallet"},
    "Cypher":      {"cypher.com", "cypher card"},
    "Bybit":       {"bybit.com", "bybit card"},
    "Nexo":        {"nexo.com", "nexo card"},
    "RedotPay":    {"redotpay.com", "redotpay"},
    "Holyheld":    {"holyheld.com", "holyheld"},
    "Moon":        {"paywithmoon.com", "moon card"},
}

# Flat domain list for Ahrefs/SerpAPI competitor keyword pulls
COMPETITOR_DOMAINS_FLAT: list[str] = [
    "gnosispay.com", "metamask.io", "coca.xyz", "bleap.finance",
    "crypto.com", "bitget.com", "cypher.com", "bybit.com", "nexo.com",
    "redotpay.com", "holyheld.com", "paywithmoon.com",
]


# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCT PROFILE
# ═══════════════════════════════════════════════════════════════════════════════

PRODUCT_PROFILE = {
    "name": "Nonbank",
    "domain": "nonbank.io",
    "tagline": "Rule your Crypto and Banks in one App",
    "description": (
        "DeFi wallet with a seamlessly integrated custodial Visa card (NON×CARD). "
        "Hybrid model: non-custodial wallet where users hold keys + custodial card "
        "(Kolo issuer) available in 100+ countries. Gasless transactions, built-in "
        "AML screening, proxy addresses, and watch wallets."
    ),
    "card_name": "NON×CARD",
    "card_network": "Visa",
    "card_status": "Live (100+ countries)",
    "custody_model": "Hybrid — DeFi wallet (non-custodial) + card (custodial, Kolo issuer)",

    # ── Core differentiators ─────────────────────────────────────
    "differentiators": [
        {
            "id": "gasless",
            "label": "Gasless Fees",
            "description": "Send crypto without native gas tokens — fees deducted from purchase amount",
            "seo_angle": "Only non-custodial wallet where users don't need ETH/TRX for gas",
        },
        {
            "id": "aml",
            "label": "Built-in AML Watchtower",
            "description": "Automatic blocking of transfers from sanctioned wallets or suspicious entities",
            "seo_angle": "Compliance-first self-custody — unlike MetaMask or Gnosis Pay",
        },
        {
            "id": "hybrid_defi_card",
            "label": "DeFi Wallet + Seamless Card",
            "description": "Hybrid model: DeFi wallet (non-custodial) with integrated custodial Visa card — issue in 100+ countries, no separate app",
            "seo_angle": "Unlike Gnosis Pay (fully on-chain) or Crypto.com (fully custodial), Nonbank bridges DeFi and card spending seamlessly",
        },
        {
            "id": "proxy_watch",
            "label": "Proxy Addresses & Watch Wallets",
            "description": "Monitor any wallet via watch-only addresses; proxy addresses for privacy. Portfolio integrations (exchanges/banks) planned.",
            "seo_angle": "Track your whole portfolio without exposing keys — unique for a wallet with a card",
        },
        {
            "id": "non_id",
            "label": "NON ID (DeFi Identity)",
            "description": "Single DeFi identity — receive funds via one handle, mint as NFT, earn rewards",
            "seo_angle": "Web3 identity that replaces long wallet addresses",
        },
    ],

    # ── Supported assets & chains ────────────────────────────────
    "chains": ["TRON", "EVM (planned)"],
    "assets": ["TRX", "USDT (TRC-20)", "BTC (via bridge)", "ETH (planned)"],

    # ── Platforms ─────────────────────────────────────────────────
    "platforms": {
        "ios": "https://apps.apple.com/app/id6477441479",
        "android": "https://play.google.com/store/apps/details?id=io.nonbank",
    },

    # ── Social / community ───────────────────────────────────────
    "social": {
        "twitter": "https://twitter.com/nonbank_io",
        "telegram": "https://t.me/nonbankers",
        "discord": "https://discord.com/invite/AQUuEKugZh",
    },

    # ── Pricing / fees ───────────────────────────────────────────
    "fees": {
        "transfers": "0% transaction fee (free monthly allowance + earn more via tasks)",
        "card": "TBD — confirm with product team",
    },

    # ── SEO baseline ─────────────────────────────────────────────
    "seo_baseline": {
        "domain_rating": None,      # fill from Ahrefs when available
        "organic_traffic": None,    # fill from Ahrefs/GA4
        "blog_posts": 80,           # ~80 educational posts on nonbank.io/blog
        "backlinks": None,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# COMPETITOR MATRIX
# ═══════════════════════════════════════════════════════════════════════════════

FEATURE_DIMENSIONS = [
    "Custody Model",
    "Card Network",
    "Card Status",
    "Supported Chains",
    "Gasless Fees",
    "Built-in AML",
    "Multi-Account (banks+exchanges+wallets)",
    "DeFi Identity / Username",
    "Cashback / Rewards",
    "KYC Required",
    "Mobile App",
    "Hardware Wallet Support",
    "Key Regions",
    "Pricing",
    "Unique Angle",
]

COMPETITORS = [
    {
        "name": "Nonbank",
        "domain": "nonbank.io",
        "is_self": True,
        "Custody Model": "Hybrid — DeFi wallet (non-custodial) + card (custodial)",
        "Card Network": "Visa (NON×CARD)",
        "Card Status": "Live (100+ countries)",
        "Supported Chains": "TRON, EVM planned",
        "Gasless Fees": "Yes — fees from purchase",
        "Built-in AML": "Yes — AML Watchtower",
        "Multi-Account (banks+exchanges+wallets)": "Watch wallets + proxy addresses (exchange/bank integrations planned)",
        "DeFi Identity / Username": "NON ID (mint as NFT)",
        "Cashback / Rewards": "Nons (gamified rewards)",
        "KYC Required": "Yes (card)",
        "Mobile App": "iOS + Android",
        "Hardware Wallet Support": "Watch wallets (full HW integration planned)",
        "Key Regions": "Global (card: 100+ countries)",
        "Pricing": "0% transfer fees",
        "Unique Angle": "Hybrid DeFi+card: gasless fees + AML + seamless card in DeFi wallet",
    },
    {
        "name": "Gnosis Pay",
        "domain": "gnosispay.com",
        "is_self": False,
        "Custody Model": "Fully on-chain (Safe smart account — card spends from chain)",
        "Card Network": "Visa",
        "Card Status": "Live (EU/UK only)",
        "Supported Chains": "Gnosis Chain only",
        "Gasless Fees": "No — needs xDAI for gas",
        "Built-in AML": "No",
        "Multi-Account (banks+exchanges+wallets)": "No — Gnosis Chain only",
        "DeFi Identity / Username": "No",
        "Cashback / Rewards": "GNO staking bonus (up to 4%)",
        "KYC Required": "Yes",
        "Mobile App": "No (web only)",
        "Hardware Wallet Support": "No (Safe wallet)",
        "Key Regions": "EU, UK",
        "Pricing": "1-2% non-EUR FX",
        "Unique Angle": "First truly non-custodial Visa card on-chain",
    },
    {
        "name": "MetaMask",
        "domain": "metamask.io",
        "is_self": False,
        "Custody Model": "Non-custodial (browser/mobile wallet)",
        "Card Network": "Mastercard (pilot)",
        "Card Status": "Pilot — limited regions",
        "Supported Chains": "Ethereum, Linea, Base, Solana",
        "Gasless Fees": "No",
        "Built-in AML": "No",
        "Multi-Account (banks+exchanges+wallets)": "No — crypto only",
        "DeFi Identity / Username": "No (ENS optional)",
        "Cashback / Rewards": "1-3% mUSD",
        "KYC Required": "Yes (card)",
        "Mobile App": "iOS + Android + browser extension",
        "Hardware Wallet Support": "Yes (Ledger, Trezor, Lattice)",
        "Key Regions": "US, EU (limited)",
        "Pricing": "Multiple fees (delegation, conversion)",
        "Unique Angle": "Largest wallet user base (30M+), brand trust",
    },
    {
        "name": "COCA",
        "domain": "coca.xyz",
        "is_self": False,
        "Custody Model": "Non-custodial (MPC wallet)",
        "Card Network": "Visa",
        "Card Status": "Live",
        "Supported Chains": "Multi-chain",
        "Gasless Fees": "No",
        "Built-in AML": "No",
        "Multi-Account (banks+exchanges+wallets)": "No — crypto only",
        "DeFi Identity / Username": "No",
        "Cashback / Rewards": "8% cashback (stablecoins), 6% APY",
        "KYC Required": "Yes",
        "Mobile App": "iOS + Android",
        "Hardware Wallet Support": "No (MPC-based)",
        "Key Regions": "Global",
        "Pricing": "0% FX on direct pairs, 1% indirect",
        "Unique Angle": "Highest cashback + stablecoin yield",
    },
    {
        "name": "Bleap",
        "domain": "bleap.finance",
        "is_self": False,
        "Custody Model": "Non-custodial (MPC wallet)",
        "Card Network": "Mastercard",
        "Card Status": "Live",
        "Supported Chains": "Multi-chain",
        "Gasless Fees": "No",
        "Built-in AML": "No",
        "Multi-Account (banks+exchanges+wallets)": "No — crypto only",
        "DeFi Identity / Username": "No",
        "Cashback / Rewards": "2% USDC cashback",
        "KYC Required": "Minimal",
        "Mobile App": "iOS + Android",
        "Hardware Wallet Support": "No (MPC-based)",
        "Key Regions": "Global",
        "Pricing": "0% FX, 0% conversion, free ATM",
        "Unique Angle": "Zero-fee card + minimal KYC",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT PILLARS & SEED KEYWORDS
# ═══════════════════════════════════════════════════════════════════════════════

# Priorities validated by SERP/AI research (April 2026 audit).
# See research notes in each pillar's `serp_notes` field.
CONTENT_PILLARS = [
    {
        "id": "gasless",
        "label": "Gasless Crypto Transactions",
        "description": "Send crypto without gas fees — unique Nonbank feature, no competitor has this",
        "differentiator": "gasless",
        "priority": "P0 — Start here",
        "serp_notes": (
            "VALIDATED: Nonbank already appears in 'no gas fee wallet' SERP (nonbank.io/blog). "
            "'Send crypto without gas fees' has fragmented low-DR competition. "
            "Consumer-facing explainer gap — SERPs are developer/protocol-heavy. "
            "Highest-leverage first move: amplify existing blog post + DR60+ outlet placement."
        ),
        "seed_keywords": [
            "gasless crypto transactions",
            "send crypto without gas fees",
            "no gas fee wallet",
            "gasless USDT transfer",
            "meta-transactions crypto",
            "gas-free crypto wallet",
        ],
    },
    {
        "id": "watch_proxy",
        "label": "Watch Wallets & Proxy Addresses",
        "description": "Track any wallet without exposing keys (watch-only). Proxy addresses for privacy. Unique for a wallet that also has a card.",
        "differentiator": "proxy_watch",
        "priority": "P1 — Unclaimed niche",
        "serp_notes": (
            "VALIDATED: 'portfolio tracker with card' is COMPLETELY unclaimed — SERP returns stock "
            "trackers, not crypto. 'Crypto watch wallet' is fragmented (no dominant brand). "
            "Nonbank can own this query with one well-placed article on a DR65+ outlet."
        ),
        "seed_keywords": [
            "crypto watch wallet",
            "proxy address crypto",
            "portfolio tracker wallet",
            "watch-only wallet with card",
            "crypto privacy proxy address",
            "track multiple wallets one app",
        ],
    },
    {
        "id": "defi_wallet_card",
        "label": "DeFi Wallet with Integrated Card",
        "description": "Hybrid model: DeFi wallet + seamlessly integrated Visa card (100+ countries). Unlike Gnosis Pay (fully on-chain, EU/UK only) or Crypto.com (fully custodial).",
        "differentiator": "hybrid_defi_card",
        "priority": "P2 — Comparison angle",
        "serp_notes": (
            "VALIDATED: 'gnosis pay alternative' has moderate competition (Bleap owns it, thin field). "
            "Nonbank's hybrid model is genuinely different from Bleap/Gnosis. "
            "'Best crypto wallet with card' is saturated (MetaMask, Bleap, CoinGecko dominate). "
            "Entry point: niche comparison articles, not head terms."
        ),
        "seed_keywords": [
            "DeFi wallet with card",
            "crypto wallet with visa card",
            "best crypto card 2026",
            "DeFi wallet vs gnosis pay",
            "crypto card 100 countries",
            "crypto wallet card integration",
        ],
    },
    {
        "id": "aml_compliance",
        "label": "AML-Safe DeFi Wallet",
        "description": "Built-in AML Watchtower — the responsible DeFi angle. First consumer wallet with compliance screening.",
        "differentiator": "aml",
        "priority": "P3 — PR/GEO only",
        "serp_notes": (
            "CAUTION: 'AML crypto wallet' intent = B2B compliance tools (TRM Labs, Elliptic, AMLBot). "
            "Searchers want enterprise screening, not consumer wallets. "
            "Better as thought-leadership / PR for AI citations than direct SEO ranking. "
            "Target: fintech press, compliance newsletters, AI answer insertion."
        ),
        "seed_keywords": [
            "AML crypto wallet",
            "self-custody AML compliance",
            "sanctioned wallet checker",
            "crypto wallet AML screening",
            "compliant non-custodial wallet",
            "safe self-custody crypto",
        ],
    },
    {
        "id": "defi_identity",
        "label": "NON ID (DeFi Identity)",
        "description": "NON ID as a single DeFi handle — replaces long wallet addresses, mintable as NFT. Feature mention only — ENS/Unstoppable Domains own this search space.",
        "differentiator": "non_id",
        "priority": "P4 — Feature mention only",
        "serp_notes": (
            "NOT COMPETITIVE: ENS and Unstoppable Domains completely own the DeFi identity space. "
            "NON ID is proprietary, not interoperable. No realistic SEO opportunity. "
            "Mention NON ID within other pillar articles but do NOT create dedicated content."
        ),
        "seed_keywords": [
            "DeFi identity wallet",
            "crypto username wallet",
            "NFT identity crypto",
            "web3 identity single handle",
            "replace wallet address with username",
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# ARTICLE BRIEFS (seeded from pillars — editable in Content Strategy page)
# ═══════════════════════════════════════════════════════════════════════════════

BRIEFS = [
    # ── Pillar: DeFi Wallet + Card (hybrid model) ────────────────
    {"#": 1,  "Title": "Best Crypto Wallet with Card 2026: DeFi Meets Visa",                  "Lang": "EN", "Market": "Global", "KW": "crypto wallet with visa card",        "Words": 1500, "Priority": "High",   "Pillar": "defi_wallet_card"},
    {"#": 2,  "Title": "Nonbank vs Gnosis Pay: Hybrid DeFi+Card vs Fully On-Chain",           "Lang": "EN", "Market": "Global", "KW": "gnosis pay alternative",              "Words": 1500, "Priority": "High",   "Pillar": "defi_wallet_card"},
    {"#": 3,  "Title": "Nonbank vs MetaMask: DeFi Wallet Comparison 2026",                    "Lang": "EN", "Market": "Global", "KW": "metamask alternative wallet",         "Words": 1400, "Priority": "High",   "Pillar": "defi_wallet_card"},
    {"#": 4,  "Title": "Nonbank vs Bleap vs COCA: Which Crypto Card Wins in 2026?",           "Lang": "EN", "Market": "Global", "KW": "bleap vs coca crypto card",           "Words": 1400, "Priority": "High",   "Pillar": "defi_wallet_card"},
    {"#": 5,  "Title": "Why a Hybrid DeFi Wallet Beats Fully Custodial Crypto Cards",         "Lang": "EN", "Market": "Global", "KW": "custodial vs DeFi wallet card",       "Words": 1300, "Priority": "High",   "Pillar": "defi_wallet_card"},
    # ── Pillar: Gasless ──────────────────────────────────────────
    {"#": 6,  "Title": "Gasless Crypto: How to Send USDT Without Paying Gas Fees",             "Lang": "EN", "Market": "Global", "KW": "gasless crypto transactions",         "Words": 1300, "Priority": "High",   "Pillar": "gasless"},
    {"#": 7,  "Title": "Spend Crypto Without Gas: How Nonbank's Gasless Fees Work",            "Lang": "EN", "Market": "Global", "KW": "send crypto without gas fees",        "Words": 1200, "Priority": "High",   "Pillar": "gasless"},
    {"#": 8,  "Title": "Is Gasless Crypto the Future? Meta-Transactions Explained",            "Lang": "EN", "Market": "Global", "KW": "meta-transactions crypto",            "Words": 1000, "Priority": "Medium", "Pillar": "gasless"},
    # ── Pillar: AML ──────────────────────────────────────────────
    {"#": 9,  "Title": "DeFi Wallet + AML: Why Built-in Compliance Matters",                   "Lang": "EN", "Market": "Global", "KW": "AML crypto wallet",                   "Words": 1200, "Priority": "Medium", "Pillar": "aml_compliance"},
    {"#": 10, "Title": "Crypto Wallet AML Screening: How Nonbank Blocks Sanctioned Wallets",   "Lang": "EN", "Market": "Global", "KW": "sanctioned wallet checker",           "Words": 1200, "Priority": "Medium", "Pillar": "aml_compliance"},
    # ── Pillar: Watch + Proxy ────────────────────────────────────
    {"#": 11, "Title": "Watch Wallets Explained: Track Crypto Without Exposing Keys",          "Lang": "EN", "Market": "Global", "KW": "crypto watch wallet",                 "Words": 1000, "Priority": "Medium", "Pillar": "watch_proxy"},
    # ── Pillar: DeFi Identity ────────────────────────────────────
    {"#": 12, "Title": "NON ID: One DeFi Identity for All Your Wallets and Cards",             "Lang": "EN", "Market": "Global", "KW": "DeFi identity wallet",                "Words": 1000, "Priority": "Medium", "Pillar": "defi_identity"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT PLAN DEFAULT TASKS (seeded — editable in the Content Strategy page)
# ═══════════════════════════════════════════════════════════════════════════════

PLAN_DEFAULT = [
    # ── Week 1-2: Foundation comparisons ─────────────────────────
    {"Task": "Lead: Best non-custodial crypto card 2026 (Nonbank vs Gnosis Pay vs COCA)", "Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · bignewsnetwork.com ($20, DR75) · tycoonstory.com ($150, DR77)", "Price": "$20–150", "GEO": "FAQ + comparison table + 3 stats", "Week": "1", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Nonbank vs Gnosis Pay: feature-by-feature comparison",                      "Type": "GEO",     "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · newspioneer.co.uk ($65, DR54) · apsense.com ($45, DR73)", "Price": "$45–100", "GEO": "CRITICAL: comparison table + FAQ", "Week": "1", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Gasless crypto: how to send USDT without gas fees",                         "Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "technology.org ($190, DR73) · businessabc.net ($100, DR81) · greenrecord.co.uk ($40, DR73)", "Price": "$40–190", "GEO": "How-to + stats + FAQ", "Week": "2", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Nonbank vs MetaMask: wallet comparison 2026",                                "Type": "GEO",     "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · tycoonstory.com ($150, DR77) · kompass.com ($100, DR77)", "Price": "$100–150", "GEO": "CRITICAL: comparison table", "Week": "2", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    # ── Week 3-4: Differentiator deep dives ──────────────────────
    {"Task": "AML-safe self-custody: why your wallet needs compliance",                    "Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · technology.org ($190, DR73) · tycoonstory.com ($150, DR77)", "Price": "$100–190", "GEO": "FAQ + stat paragraphs", "Week": "3", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "All-in-one crypto: banks + exchanges + wallets in one app",                  "Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · greenrecord.co.uk ($40, DR73) · apsense.com ($45, DR73)", "Price": "$40–100", "GEO": "Use cases + FAQ", "Week": "3", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Nonbank vs Bleap vs COCA: which non-custodial card wins?",                    "Type": "GEO",     "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · tycoonstory.com ($150, DR77) · apsense.com ($45, DR73)", "Price": "$45–150", "GEO": "Comparison table + FAQ", "Week": "4", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Why non-custodial cards beat Crypto.com and Binance Card",                   "Type": "GEO",     "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · tycoonstory.com ($150, DR77) · apsense.com ($45, DR73)", "Price": "$45–150", "GEO": "CRITICAL: custodial vs non-custodial", "Week": "4", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "NON ID: one DeFi identity for all wallets and cards",                        "Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "technology.org ($190, DR73) · businessabc.net ($100, DR81)", "Price": "$100–190", "GEO": "FAQ + how-to", "Week": "Apr", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    # ── Social / Shill ───────────────────────────────────────────
    {"Task": "Reddit: 'best non-custodial crypto card' threads",       "Type": "Social", "Market": "🌍 Global", "Outlet Options": "r/cryptocurrency · r/ethfinance · r/defi · r/CryptoCards", "Price": "$0", "GEO": "AI indexes Reddit", "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Reddit: r/gnosispay comparison / alternative threads",   "Type": "Social", "Market": "🌍 Global", "Outlet Options": "r/gnosispay · r/ethereum · r/CryptoCards", "Price": "$0", "GEO": "Competitor comparison angle", "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Quora: 'how to spend crypto without exchange' threads",  "Type": "Social", "Market": "🌍 Global", "Outlet Options": "Quora crypto wallet + card topics", "Price": "$0", "GEO": "AI indexes Quora", "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Twitter/X: reply to gasless/non-custodial card threads",  "Type": "Social", "Market": "🌍 Global", "Outlet Options": "Crypto Twitter threads", "Price": "$0", "GEO": "AI indexes X posts", "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
]


# ═══════════════════════════════════════════════════════════════════════════════
# SOCIAL DISTRIBUTION
# ═══════════════════════════════════════════════════════════════════════════════

LISTENING_QUERIES = [
    {"q": "non-custodial crypto card",        "label": "Non-custodial card",    "geo": True},
    {"q": "gnosis pay alternative",           "label": "Gnosis Pay alt",        "geo": True},
    {"q": "gasless crypto transaction",       "label": "Gasless crypto",        "geo": True},
    {"q": "metamask card alternative",        "label": "MetaMask Card alt",     "geo": True},
    {"q": "self custody crypto spend",        "label": "Self-custody spend",    "geo": True},
    {"q": "AML crypto wallet",                "label": "AML wallet",            "geo": False},
    {"q": "connect bank and crypto wallet",   "label": "Bank + wallet",         "geo": True},
    {"q": "custodial vs non custodial card",  "label": "Custodial vs non",      "geo": True},
    {"q": "crypto card without gas fees",     "label": "No gas fees card",      "geo": True},
    {"q": "all in one crypto app",            "label": "All-in-one app",        "geo": True},
]

SUBREDDITS = [
    "cryptocurrency", "CryptoCards", "ethfinance", "defi",
    "ethereum", "gnosispay", "Bitcoin", "digitalnomad",
]

PLATFORM_QUERIES = {
    "Reddit": [
        "site:reddit.com non-custodial crypto card",
        "site:reddit.com gnosis pay alternative",
        "site:reddit.com gasless crypto transaction",
        "site:reddit.com metamask card alternative",
        "site:reddit.com self custody crypto spend",
        "site:reddit.com best crypto card 2026",
        "site:reddit.com custodial vs non-custodial card",
        "site:reddit.com crypto card without gas",
    ],
    "Quora": [
        "site:quora.com non-custodial crypto card",
        "site:quora.com gnosis pay",
        "site:quora.com gasless crypto",
        "site:quora.com best crypto wallet with card",
        "site:quora.com self custody crypto spend",
        "site:quora.com AML crypto wallet",
        "site:quora.com all in one crypto app",
    ],
    "Twitter": [
        "site:twitter.com OR site:x.com non-custodial card",
        "site:twitter.com OR site:x.com gnosis pay",
        "site:twitter.com OR site:x.com gasless crypto",
        "site:twitter.com OR site:x.com metamask card",
        "site:twitter.com OR site:x.com self custody spend",
        "site:twitter.com OR site:x.com crypto card 2026",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# BUDGET & LANGUAGE MAPPINGS
# ═══════════════════════════════════════════════════════════════════════════════

PILLAR_BUDGET_CAPS = {
    "English": 2000,  # all budget goes to EN global — wallet is borderless, no geo pillars needed
}

LANG_MAP = {
    "EN": "en",
}


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE FILE PATHS
# ═══════════════════════════════════════════════════════════════════════════════

DISTRIBUTION_CACHE = "distribution_cache.json"
GEO_AUDIT_CACHE = "geo_audit_cache.json"
