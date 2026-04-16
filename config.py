"""
config.py — Constants and static data for Nonbank SEO & GEO Intelligence Agent
==============================================================================
All hardcoded content plan defaults, article briefs, social listening queries,
and subreddit lists live here instead of scattered across page functions.

Nonbank (nonbank.io) is a non-custodial wallet + Visa card + unified portfolio
manager that connects banks, exchanges, hardware wallets, and DeFi wallets.
Target markets: Global English (US/UK/EU), LATAM (ES/PT), MENA/UAE/Turkey.
"""
from __future__ import annotations


# ── Article Briefs ─────────────────────────────────────────────────────────────
# Starter set — no historical Hex data. Edit freely in the Content Plan page
# or swap this list as real performance data comes in.

BRIEFS = [
    {"#": 1,  "Title": "Best Non-Custodial Crypto Wallet with Visa Card 2026",         "Lang": "EN", "Market": "Global", "KW": "non-custodial crypto card",      "Words": 1500, "Priority": "High"},
    {"#": 2,  "Title": "Self-Custody Crypto: How to Spend Without Giving Up Keys",     "Lang": "EN", "Market": "Global", "KW": "self custody crypto card",       "Words": 1300, "Priority": "High"},
    {"#": 3,  "Title": "Nonbank vs MetaMask Card vs Gnosis Pay: 2026 Comparison",      "Lang": "EN", "Market": "Global", "KW": "metamask card alternative",      "Words": 1500, "Priority": "High"},
    {"#": 4,  "Title": "Hardware Wallet + Visa Card Setup 2026 (Ledger / Trezor)",     "Lang": "EN", "Market": "Global", "KW": "ledger visa card",               "Words": 1200, "Priority": "Medium"},
    {"#": 5,  "Title": "Unified Portfolio App: Banks + Exchanges + Wallets in One",    "Lang": "EN", "Market": "Global", "KW": "unified crypto portfolio app",   "Words": 1200, "Priority": "Medium"},
    {"#": 6,  "Title": "Best Non-Custodial Crypto Card for Dubai Expats 2026",         "Lang": "EN", "Market": "ARE",    "KW": "non-custodial crypto card UAE",  "Words": 1200, "Priority": "High"},
    {"#": 7,  "Title": "En Iyi Kendi Cuzdanin Kripto Kart Turkiye 2026",               "Lang": "TR", "Market": "TUR",    "KW": "non-custodial kripto kart",      "Words": 1000, "Priority": "High"},
    {"#": 8,  "Title": "Mejor Billetera No Custodial con Tarjeta Visa en Mexico 2026", "Lang": "ES", "Market": "MEX",    "KW": "billetera no custodial tarjeta", "Words": 1000, "Priority": "High"},
    {"#": 9,  "Title": "Tarjeta Cripto No Custodial Argentina: Gastar USDT Sin Banco", "Lang": "ES", "Market": "ARG",    "KW": "tarjeta cripto no custodial",    "Words": 1000, "Priority": "High"},
    {"#": 10, "Title": "Melhor Carteira Nao Custodial com Cartao Visa Brasil 2026",    "Lang": "PT", "Market": "BRA",    "KW": "carteira nao custodial cartao",  "Words": 1000, "Priority": "High"},
    {"#": 11, "Title": "AML-Safe Self-Custody: Send Crypto Without Sanctioned-Wallet Risk", "Lang": "EN", "Market": "Global", "KW": "AML crypto wallet",         "Words": 1200, "Priority": "Medium"},
    {"#": 12, "Title": "Nonbank vs Crypto.com: Custodial vs Non-Custodial Compared",   "Lang": "EN", "Market": "Global", "KW": "custodial vs non-custodial card","Words": 1400, "Priority": "High"},
]


# ── Content Plan Default Tasks ─────────────────────────────────────────────────
# Starter plan — empty URLs, all To Do. Populate from the app as work begins.

PLAN_DEFAULT = [
    {"Task": "Lead: Best non-custodial crypto card 2026",              "Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · bignewsnetwork.com ($20, DR75) · tycoonstory.com ($150, DR77) · technology.org ($190, DR73)",                                                       "Price": "$20–190",  "GEO": "FAQ + 3 stats + question headers",                       "Week": "1", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Nonbank vs MetaMask Card vs Gnosis Pay comparison",      "Type": "GEO",     "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · newspioneer.co.uk ($65, DR54) · apsense.com ($45, DR73, Crypto) · kompass.com ($100, DR77)",                                                        "Price": "$45–100",  "GEO": "CRITICAL: comparison table + FAQ",                       "Week": "1", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Self-custody spend: spend crypto without giving up keys","Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · tycoonstory.com ($150, DR77) · greenrecord.co.uk ($40, DR73) · technology.org ($190, DR73)",                                                        "Price": "$40–190",  "GEO": "FAQ + comparison table",                                 "Week": "2", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Hardware wallet + Visa card setup (Ledger / Trezor)",    "Type": "SEO",     "Market": "🌍 Global", "Outlet Options": "technology.org ($190, DR73) · businessabc.net ($100, DR81) · tycoonstory.com ($150, DR77)",                                                                                         "Price": "$100–190", "GEO": "Step-by-step + stat paragraphs",                         "Week": "2", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Unified portfolio (banks + exchanges + wallets)",        "Type": "SEO+GEO", "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · tycoonstory.com ($150, DR77) · kompass.com ($100, DR77)",                                                                                            "Price": "$100–150", "GEO": "FAQ + use cases",                                        "Week": "3", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Non-custodial crypto card Dubai 2026",                   "Type": "SEO+GEO", "Market": "🇦🇪 ARE",  "Outlet Options": "uaehelper.com ($50, DR53, 86% search) · thetradable.com ($100, DR54) · theemiratestimes.com ($99, DR44) · khaleejtimes.com ($200, DR80, premium)",                                "Price": "$50–200",  "GEO": "FAQ + comparison table required",                        "Week": "2", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "En iyi non-custodial kripto kart Turkiye",               "Type": "SEO",     "Market": "🇹🇷 TUR",  "Outlet Options": "TBD Turkish outlet — source from Collaborator (crypto + finance, DR>50)",                                                                                                          "Price": "$50–150",  "GEO": "FAQ + question headers",                                 "Week": "3", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Mejor billetera no custodial con tarjeta (Mexico)",      "Type": "SEO",     "Market": "🇲🇽 MEX",  "Outlet Options": "crypto-economy.com ($190, DR60, Crypto) · kompass.com ($100, DR77) · technocio.com ($73, DR44, Crypto)",                                                                            "Price": "$73–190",  "GEO": "FAQ recommended",                                        "Week": "3", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Tarjeta cripto no custodial Argentina (USDT)",           "Type": "SEO",     "Market": "🇦🇷 ARG",  "Outlet Options": "crypto-economy.com ($190, DR60) · diariosigloxxi.com ($112, DR72) · nuevarioja.com.ar ($70, DR42, Crypto)",                                                                         "Price": "$70–190",  "GEO": "FAQ + comparison table",                                 "Week": "4", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Melhor carteira nao custodial com cartao (Brasil)",      "Type": "SEO",     "Market": "🇧🇷 BRA",  "Outlet Options": "adital.com.br ($100, DR53, Crypto) · uai.com.br ($58, DR73) · inmais.com.br ($50, DR62, Crypto) · meubanco.digital ($60, DR54, Crypto)",                                             "Price": "$50–100",  "GEO": "FAQ recommended",                                        "Week": "4", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Custodial vs Non-Custodial cards explained",             "Type": "GEO",     "Market": "🌍 Global", "Outlet Options": "businessabc.net ($100, DR81) · tycoonstory.com ($150, DR77) · apsense.com ($45, DR73, Crypto)",                                                                                      "Price": "$45–150",  "GEO": "CRITICAL: targets custodial-vs-non-custodial AI queries","Week": "4", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    # Social / Shill tasks
    {"Task": "Reddit: answer 'non-custodial crypto card' threads",     "Type": "Social",  "Market": "🌍 Global", "Outlet Options": "r/cryptocurrency · r/CryptoCards · r/ethfinance · r/defi", "Price": "$0", "GEO": "High GEO impact — AI indexes Reddit",  "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Quora: answer self-custody spending questions",          "Type": "Social",  "Market": "🌍 Global", "Outlet Options": "Quora crypto wallet + card topics",                        "Price": "$0", "GEO": "High GEO impact — AI indexes Quora",   "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Reddit: r/Ledger / r/Trezor card integration threads",   "Type": "Social",  "Market": "🌍 Global", "Outlet Options": "r/ledgerwallet · r/TREZOR · r/ethfinance",                 "Price": "$0", "GEO": "Supports hardware-wallet brief",       "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
    {"Task": "Reddit: r/dubai / r/UAE non-custodial card threads",     "Type": "Social",  "Market": "🇦🇪 ARE",  "Outlet Options": "r/dubai · r/UAE · r/cryptocurrency",                       "Price": "$0", "GEO": "Supports UAE SEO article",             "Week": "Ongoing", "Status": "To Do", "Publication URL": "", "Reddit/Quora URL": ""},
]


# ── Social Distribution ───────────────────────────────────────────────────────

LISTENING_QUERIES = [
    {"q": "non-custodial crypto card",        "label": "Non-custodial card",        "geo": True},
    {"q": "self custody crypto spend",        "label": "Self-custody spend",        "geo": True},
    {"q": "metamask card alternative",        "label": "MetaMask Card alt",         "geo": True},
    {"q": "gnosis pay review",                "label": "Gnosis Pay review",         "geo": False},
    {"q": "ledger visa card",                 "label": "Ledger + Visa",             "geo": True},
    {"q": "hardware wallet spend crypto",     "label": "Hardware wallet spend",     "geo": True},
    {"q": "unified crypto portfolio app",     "label": "Unified portfolio",         "geo": True},
    {"q": "custodial vs non custodial card",  "label": "Custodial vs non",          "geo": True},
    {"q": "AML crypto wallet",                "label": "AML wallet",                "geo": False},
    {"q": "connect bank and crypto wallet",   "label": "Bank + wallet",             "geo": True},
]

SUBREDDITS = [
    "cryptocurrency", "CryptoCards", "ethfinance", "defi",
    "ledgerwallet", "TREZOR", "ethereum", "Bitcoin",
]

PLATFORM_QUERIES = {
    "Reddit": [
        "site:reddit.com non-custodial crypto card",
        "site:reddit.com metamask card alternative",
        "site:reddit.com gnosis pay review",
        "site:reddit.com ledger card visa",
        "site:reddit.com hardware wallet spend",
        "site:reddit.com self custody crypto spend",
        "site:reddit.com unified crypto portfolio",
        "site:reddit.com custodial vs non-custodial card",
    ],
    "Quora": [
        "site:quora.com non-custodial crypto card",
        "site:quora.com self custody crypto spend",
        "site:quora.com metamask card vs",
        "site:quora.com best crypto wallet with card",
        "site:quora.com hardware wallet spending",
        "site:quora.com custodial vs non custodial wallet",
        "site:quora.com unified crypto portfolio app",
    ],
    "Twitter": [
        "site:twitter.com OR site:x.com non-custodial card",
        "site:twitter.com OR site:x.com metamask card alternative",
        "site:twitter.com OR site:x.com gnosis pay",
        "site:twitter.com OR site:x.com ledger card",
        "site:twitter.com OR site:x.com self custody spend",
        "site:twitter.com OR site:x.com unified crypto portfolio",
    ],
}


# ── Pillar Budget Caps ─────────────────────────────────────────────────────────
# Placeholder caps — adjust once real spend/ROI data exists.

PILLAR_BUDGET_CAPS = {
    "English":    800,
    "Spanish":    300,
    "Portuguese": 200,
    "Turkish":    150,
    "UAE":        400,
    "LATAM":      300,
}


# ── Language Code → Key Mapping ────────────────────────────────────────────────

LANG_MAP = {
    "EN": "en", "ES": "es", "PT": "pt", "TR": "tr",
}


# ── Cache File Paths ──────────────────────────────────────────────────────────

DISTRIBUTION_CACHE = "distribution_cache.json"
GEO_AUDIT_CACHE = "geo_audit_cache.json"
