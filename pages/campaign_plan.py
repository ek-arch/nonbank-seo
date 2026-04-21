"""Page — Campaign Plan: 4-week competitor-conquest sprint brief.

Static brief generated from /marketing:campaign-plan conversation.
Goal: acquisition + SEO/GEO authority; hero angle "DeFi wallet with a
card built in"; targets Gnosis Pay / MetaMask Card / COCA / Bleap
comparison-shoppers. Budget $5–15K. Timeline 4 weeks.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st


def page_campaign_plan():
    st.title("🎯 Campaign Plan · The Card Is Already Inside")
    st.caption(
        "4-week competitor-conquest sprint — acquisition + SEO/GEO authority. "
        "Hero angle: DeFi wallet with a real Visa card built in (100+ countries)."
    )

    # ── Top-line KPIs ────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Duration", "4 weeks")
    c2.metric("Budget", "$5–15K")
    c3.metric("Installs target", "1,500")
    c4.metric("Card applications", "400")

    tab_overview, tab_audience, tab_messages, tab_channels, tab_outlets, \
        tab_content, tab_calendar, tab_assets, tab_metrics, tab_budget, \
        tab_risks, tab_next = st.tabs([
            "Overview", "Audience", "Messages", "Channels", "Media & Outlets",
            "Content to Publish", "Calendar", "Assets", "Metrics", "Budget",
            "Risks", "Next Steps",
        ])

    # ── 1. Overview ──────────────────────────────────────────────────────────
    with tab_overview:
        st.subheader("Campaign Overview")
        st.markdown("""
**Campaign name:** The Card Is Already Inside

**One-line summary:** A 4-week competitor-conquest sprint aimed at
Gnosis Pay / MetaMask Card / COCA / Bleap shoppers, positioning Nonbank
as the only DeFi wallet with a real Visa card built in, 100+ countries.

**Primary objective:** Drive **1,500 app installs** (iOS + Android) and
**400 card applications** from competitor-intent traffic in 4 weeks.

**Secondary objectives:**
- Rank top-10 for 6 competitor-alternative keywords within 60 days.
- Earn Nonbank citations in **≥3 LLM answers** (Perplexity, ChatGPT,
  Gemini) for "best self-custody crypto card" by end of sprint.
- Build a reusable multi-channel playbook for Month 2 scale-up.
""")

    # ── 2. Audience ─────────────────────────────────────────────────────────
    with tab_audience:
        st.subheader("Target Audience")
        st.markdown("""
**Primary — Competitor comparison-shoppers**

Crypto users already convinced they want a self-custody wallet with a
card, actively evaluating Gnosis Pay, MetaMask Card, COCA, or Bleap.
Pain: Gnosis Pay is EU-only, MetaMask Card is pilot/limited, COCA lacks
AML, Bleap is Mastercard + MPC. They read Reddit threads, comparison
blogs, KOL reviews.

- **Where they are:** r/CryptoCurrency, r/defi, r/ethfinance, r/Gnosis,
  Crypto Twitter, Perplexity/ChatGPT queries, Google searches with
  "alternative" / "vs" / "review" intent.
- **Buying stage:** Consideration → Decision. Not teaching the
  category — closing the choice.

**Secondary (warm-up only):** DeFi-native users frustrated by gas and
off-ramp friction. Picked up for free by the same SEO/GEO assets.
""")

    # ── 3. Messages ─────────────────────────────────────────────────────────
    with tab_messages:
        st.subheader("Key Messages")
        st.markdown("""
**Core message:**

> "Your DeFi wallet already has a card. Spend from self-custody in 100+
> countries — no second app, no EU-only, no pilot."
""")
        msgs = pd.DataFrame([
            {
                "#": 1,
                "Message": "The card is inside the wallet, not a separate app.",
                "Proof point": "NON×CARD lives inside the Nonbank DeFi wallet; one KYC, one balance.",
                "Against": "Gnosis Pay (Safe web app), MetaMask Card (separate delegation flow).",
            },
            {
                "#": 2,
                "Message": "Live in 100+ countries today — not EU-only, not a pilot.",
                "Proof point": "Kolo issuer network: EU, APAC, LATAM, Central Asia, Middle East.",
                "Against": "Gnosis Pay (EU/UK), MetaMask Card (pilot, limited regions).",
            },
            {
                "#": 3,
                "Message": "Gasless — no ETH/xDAI/TRX needed to move funds to your card balance.",
                "Proof point": "Fees deducted from purchase amount.",
                "Against": "Gnosis Pay needs xDAI, MetaMask needs ETH.",
            },
            {
                "#": 4,
                "Message": "Built-in AML Watchtower — your self-custody isn't tainted by sanctioned counterparties.",
                "Proof point": "Automatic screening on inbound transfers.",
                "Against": "MetaMask, COCA, Bleap have none.",
            },
        ])
        st.dataframe(msgs, use_container_width=True, hide_index=True)
        st.info("Messages 3 and 4 are **supporting** — they close doubts, they don't lead.")

    # ── 4. Channels ─────────────────────────────────────────────────────────
    with tab_channels:
        st.subheader("Channel Strategy")
        st.markdown(
            "Multi-channel mix calibrated for $5–15K / 4 weeks. "
            "**KOL is a seed test, not the hero.** SEO/GEO + founder X + "
            "Reddit/Quora + PR do the heavy lifting."
        )

        st.error(
            "⚠️ **Crypto ad-policy constraint:** Google Ads, Meta (Facebook/"
            "Instagram), LinkedIn, and YouTube (Google-owned) **reject "
            "DeFi wallet advertising** without a financial-services license "
            "in each target market. Nonbank doesn't hold those licenses, "
            "so these channels are **out of scope** for paid media. "
            "X/Twitter and Reddit require crypto-category certification and "
            "approve case-by-case — usable, but with policy risk. "
            "**Primary paid surfaces: crypto-native ad networks only.**"
        )

        channels = pd.DataFrame([
            {"Channel": "Comparison SEO pages (Content Brief Factory)",
             "Why it fits": "Competitor-intent searchers self-qualify; compounds past sprint.",
             "Format": "6 comparison pages + 1 category hub",
             "Effort": "High (Wk 1–2)", "Budget": "~$1.5K (production)"},
            {"Channel": "Founder/CEO X (organic)",
             "Why it fits": "Free, fastest trust signal, best for competitor call-outs.",
             "Format": "3×/week threads + daily replies in competitor mentions",
             "Effort": "Medium, daily", "Budget": "$0"},
            {"Channel": "Reddit/Quora distribution",
             "Why it fits": "Where comparison-shoppers actually ask. Fuels LLM citations.",
             "Format": "15–25 natural comments via Distribution tab",
             "Effort": "Medium", "Budget": "$0"},
            {"Channel": "PR on tier-2 crypto outlets + Collaborator network",
             "Why it fits": "Backlinks + GEO citations; mid-tier DR outlets rank fast. No ad-policy risk.",
             "Format": "2 placements on hybrid wallet+card angle + 1 PR wire",
             "Effort": "Medium", "Budget": "~$3–5K"},
            {"Channel": "Crypto-native ad networks (Coinzilla / Bitmedia / Cointraffic)",
             "Why it fits": "**Only compliant paid surface for DeFi wallets.** Crypto-specific, no license required.",
             "Format": "Native + display on tier-2/3 crypto sites; retarget comparison-page visitors",
             "Effort": "Low-medium", "Budget": "~$1.5–3K"},
            {"Channel": "Crypto newsletter sponsorships (direct-buy)",
             "Why it fits": "Direct-buy = no ad-policy gate. The Defiant / DeFi Prime / smaller lists.",
             "Format": "1 slot in The Defiant or 2 in smaller newsletters",
             "Effort": "Low", "Budget": "~$2–3K"},
            {"Channel": "Micro-KOL seeds (direct-deal)",
             "Why it fits": "Direct-to-creator = no ad-platform policy gate. Message testing.",
             "Format": "2–3 Twitter micro-KOLs + 1 small YouTuber review",
             "Effort": "Low", "Budget": "~$1.5–3K"},
            {"Channel": "Telegram channel sponsorships (direct)",
             "Why it fits": "Direct-buy; huge crypto audiences by geo; no platform-ad policy.",
             "Format": "2–3 sponsored posts in niche DeFi / card-focused TG channels",
             "Effort": "Low", "Budget": "~$500–1.5K"},
            {"Channel": "GEO optimization pass",
             "Why it fits": "Ensure Perplexity/ChatGPT cite the new comparison pages.",
             "Format": "llms.txt + schema + FAQ blocks on each page",
             "Effort": "Low (Wk 2)", "Budget": "$0 (in-house)"},
            {"Channel": "X/Twitter Ads (conditional — crypto-category certified)",
             "Why it fits": "Works if Nonbank account is cert'd. If rejected, reallocate to Coinzilla.",
             "Format": "Promoted founder threads, conquest on competitor handles",
             "Effort": "Low", "Budget": "~$500–1K (test only)"},
            {"Channel": "Reddit Ads (conditional — sub-targeted)",
             "Why it fits": "Approved case-by-case for crypto wallets; sub-targeting works well.",
             "Format": "Promoted posts in r/CryptoCurrency, r/defi (if approved)",
             "Effort": "Low", "Budget": "~$300–700 (test only)"},
        ])
        st.dataframe(channels, use_container_width=True, hide_index=True)

        st.info(
            "**Blocked/excluded channels:** Google Search Ads, Google Display "
            "Network, YouTube Ads, Meta (Facebook/Instagram) Ads, LinkedIn "
            "Ads, TikTok Ads (crypto-restricted in most regions). Any paid "
            "budget that would have gone here is **reallocated to crypto-"
            "native networks, newsletters, KOLs, and PR** (see Budget tab)."
        )

    # ── 4b. Media & Outlets ─────────────────────────────────────────────────
    with tab_outlets:
        st.subheader("Media & Outlets — Full Traffic Stack")
        st.markdown(
            "Concrete platforms ranked by **fit × cost × speed** for this "
            "sprint. Priority: **P0 = book now**, **P1 = secondary**, "
            "**P2 = Month 2+ / awareness-only**. Costs are 2026 ballpark "
            "ranges — confirm with outlet reps before booking."
        )

        sub_mkt, sub_pr, sub_adnet, sub_listing, sub_review, sub_news, sub_pod, sub_community = st.tabs([
            "Aggregators & Marketplaces", "PR / Guest Posts", "Ad Networks",
            "Listings & Aggregators", "Review / Comparison", "Newsletters",
            "Podcasts", "Community",
        ])

        # ── Sub-tab: Aggregators & Marketplaces ────────────────────────────
        with sub_mkt:
            st.markdown(
                "**Volume guest-post marketplaces — the backbone of SEO/GEO "
                "surface area.** For Nonbank we deliberately pick "
                "**catalog-access marketplaces** (one login → hundreds of "
                "outlets, pay-per-placement, no agency retainers) because "
                "SEO/GEO needs **breadth of placements** — many different "
                "domains, many different articles — not a handful of premium "
                "tier-1 hits. Tier-1 direct outlets (Cointelegraph, Decrypt, "
                "etc.) are covered separately in the **PR / Guest Posts** "
                "sub-tab; PR wires in the section below."
            )

            st.markdown("#### Volume guest-post marketplaces (catalog access, pay-per-placement)")
            marketplaces = pd.DataFrame([
                {"Platform": "Collaborator.pro",
                 "Origin": "Ukraine/CIS",
                 "Catalog": "40,000+ sites; ~300–500 crypto-relevant (DR 30–80)",
                 "Model": "Pay per publication; fixed price per site",
                 "Price range (crypto)": "$40–1,500 / article (avg ~$200–400)",
                 "Language": "EN + RU + many others",
                 "Quality control": "Editor review, sample articles visible",
                 "Crypto-friendly": "✅ Huge crypto vertical",
                 "Fit for Nonbank": "**P0** — already in the app (collaborator_outlets.py)",
                 "Priority": "P0"},
                {"Platform": "PRPosting.com",
                 "Origin": "Ukraine/CIS",
                 "Catalog": "35,000+ sites; strong crypto + fintech catalog",
                 "Model": "Pay per publication; often cheaper than Collaborator for same DR",
                 "Price range (crypto)": "$30–1,200 / article",
                 "Language": "EN + RU + EU languages",
                 "Quality control": "Manual moderation; dispute system",
                 "Crypto-friendly": "✅ Large crypto/DeFi catalog",
                 "Fit for Nonbank": "**P0** — complements Collaborator, often has unique outlets",
                 "Priority": "P0"},
                {"Platform": "WhitePress.com",
                 "Origin": "Poland / EU",
                 "Catalog": "100,000+ sites; 40+ countries; strong EU + LATAM coverage",
                 "Model": "Pay per publication OR content-production bundle",
                 "Price range (crypto)": "€50–2,000 / article",
                 "Language": "30+ languages",
                 "Quality control": "Editor approval; content quality scoring",
                 "Crypto-friendly": "✅ Crypto section active in EU markets",
                 "Fit for Nonbank": "**P0** for multi-geo push (Nonbank's 100+ country card)",
                 "Priority": "P0"},
                {"Platform": "Adsy.com",
                 "Origin": "US",
                 "Catalog": "15,000+ sites; curated guest-post inventory",
                 "Model": "Pay per publication; managed service option",
                 "Price range (crypto)": "$50–1,000 / article",
                 "Language": "EN primary",
                 "Quality control": "Editor pre-approval",
                 "Crypto-friendly": "⚠️ Mixed — check outlet-level policy",
                 "Fit for Nonbank": "P1 — US/EN-only angle, volume play",
                 "Priority": "P1"},
                {"Platform": "LinksManagement",
                 "Origin": "US (SEO-focused)",
                 "Catalog": "2,000+ verified outlets",
                 "Model": "Subscription + per-link pricing",
                 "Price range (crypto)": "$50–800 / link",
                 "Language": "EN primary",
                 "Quality control": "Metrics-vetted (DR/DA)",
                 "Crypto-friendly": "⚠️ SEO-first — some crypto outlets",
                 "Fit for Nonbank": "P2 — too SEO-farmy; risk of low-quality backlinks",
                 "Priority": "P2"},
                {"Platform": "Getfluence.com",
                 "Origin": "France / EU",
                 "Catalog": "10,000+ premium media outlets across EU",
                 "Model": "Sponsored-content marketplace (premium tier)",
                 "Price range (crypto)": "€200–5,000 / article",
                 "Language": "FR, EN, ES, DE, IT + others",
                 "Quality control": "Premium-only outlets",
                 "Crypto-friendly": "✅ — but premium pricing",
                 "Fit for Nonbank": "P1 stretch — premium EU reach",
                 "Priority": "P1"},
                {"Platform": "Miralinks",
                 "Origin": "Russia/CIS",
                 "Catalog": "10,000+ RU/EN sites; strong CIS crypto catalog",
                 "Model": "Pay per publication",
                 "Price range (crypto)": "$20–600 / article",
                 "Language": "RU primary, some EN",
                 "Quality control": "Manual editor check",
                 "Crypto-friendly": "✅ Large CIS crypto catalog",
                 "Fit for Nonbank": "P2 — CIS-skewed, Nonbank is EN-global",
                 "Priority": "P2"},
                {"Platform": "GoGetLinks",
                 "Origin": "Russia/CIS",
                 "Catalog": "Webmaster network, RU-heavy",
                 "Model": "Monthly link rental OR guest post",
                 "Price range (crypto)": "$10–300",
                 "Language": "RU primary",
                 "Quality control": "Auto + manual",
                 "Crypto-friendly": "✅ Crypto category present",
                 "Fit for Nonbank": "P3 — RU-only, skip for EN-global sprint",
                 "Priority": "Skip"},
                {"Platform": "Sape.ru",
                 "Origin": "Russia/CIS",
                 "Catalog": "Link-rental network",
                 "Model": "Monthly link rental (NOT clean guest-post)",
                 "Price range (crypto)": "Varies",
                 "Language": "RU",
                 "Quality control": "Weak; Google-penalty risk",
                 "Crypto-friendly": "—",
                 "Fit for Nonbank": "**SKIP** — rented-link risk, bad for SEO",
                 "Priority": "Skip"},
                {"Platform": "Rocketlink",
                 "Origin": "Global",
                 "Catalog": "Niche guest-post service",
                 "Model": "Managed placements",
                 "Price range (crypto)": "$100–800",
                 "Language": "EN",
                 "Quality control": "Depends on account manager",
                 "Crypto-friendly": "⚠️ Case-by-case",
                 "Fit for Nonbank": "P2 backup",
                 "Priority": "P2"},
                {"Platform": "PostWith.com",
                 "Origin": "EU",
                 "Catalog": "5,000+ content sites",
                 "Model": "Sponsored content marketplace",
                 "Price range (crypto)": "€80–1,500",
                 "Language": "Multiple EU",
                 "Quality control": "Editor review",
                 "Crypto-friendly": "⚠️ Mixed",
                 "Fit for Nonbank": "P2",
                 "Priority": "P2"},
                {"Platform": "Presspad",
                 "Origin": "EU",
                 "Catalog": "Niche publisher network",
                 "Model": "Content placement marketplace",
                 "Price range (crypto)": "€100–1,200",
                 "Language": "EU langs",
                 "Quality control": "Curated",
                 "Crypto-friendly": "⚠️",
                 "Fit for Nonbank": "P2",
                 "Priority": "P2"},
                {"Platform": "PublicFast",
                 "Origin": "Ukraine/CIS",
                 "Catalog": "Mid-tier outlets + influencer crossover",
                 "Model": "Content placement + influencer",
                 "Price range (crypto)": "$30–500",
                 "Language": "RU/UA/EN",
                 "Quality control": "Manual",
                 "Crypto-friendly": "✅",
                 "Fit for Nonbank": "P2 — redundant with Collaborator/PRPosting",
                 "Priority": "P2"},
                {"Platform": "Linkhouse.co",
                 "Origin": "Poland / EU",
                 "Catalog": "20,000+ sites across 30+ countries; active crypto vertical",
                 "Model": "Pay per publication; self-serve catalog",
                 "Price range (crypto)": "€40–1,500 / article",
                 "Language": "Multi-EU + EN",
                 "Quality control": "Verified metrics; editor pre-approval",
                 "Crypto-friendly": "✅ Dedicated crypto category",
                 "Fit for Nonbank": "**P0** — closest WhitePress alternative; often cheaper for same DR",
                 "Priority": "P0"},
                {"Platform": "Serpzilla.com",
                 "Origin": "Global (crypto-focused)",
                 "Catalog": "Smaller (~5K sites) but **crypto-weighted** selection",
                 "Model": "Pay per placement; crypto-payment accepted (USDT/BTC)",
                 "Price range (crypto)": "$40–900 / article",
                 "Language": "EN + major EU",
                 "Quality control": "Metrics + manual review",
                 "Crypto-friendly": "✅ **Crypto-specialized** — most catalog is on-topic",
                 "Fit for Nonbank": "**P0** — every outlet is topically relevant; less filtering needed",
                 "Priority": "P0"},
                {"Platform": "Authority Builders (ABC)",
                 "Origin": "US",
                 "Catalog": "Curated link marketplace; premium outlets only",
                 "Model": "Pay per link; subscription tiers",
                 "Price range (crypto)": "$200–1,200 / link",
                 "Language": "EN",
                 "Quality control": "High — vetted outlets, metrics-filtered",
                 "Crypto-friendly": "⚠️ Mixed — subset supports crypto",
                 "Fit for Nonbank": "P1 — smaller catalog but higher-quality US outlets",
                 "Priority": "P1"},
                {"Platform": "Fat Joe",
                 "Origin": "UK",
                 "Catalog": "Managed + self-serve blogger outreach",
                 "Model": "Self-serve order → managed placement; DR-tiered pricing",
                 "Price range (crypto)": "£60–500 / placement (DR 10–50+)",
                 "Language": "EN",
                 "Quality control": "Metrics-based tier selection",
                 "Crypto-friendly": "⚠️ Ask for crypto-verified sites; available but not default",
                 "Fit for Nonbank": "P1 — good for EN-UK/US DR30–50 volume",
                 "Priority": "P1"},
                {"Platform": "The HOTH",
                 "Origin": "US",
                 "Catalog": "Managed guest-post service (HOTH Blitz, HOTH Guest Post)",
                 "Model": "Fixed-price packages; DR 20 / 30 / 40 / 50+ tiers",
                 "Price range (crypto)": "$100–500 / placement",
                 "Language": "EN primary",
                 "Quality control": "DR-tiered; standardized",
                 "Crypto-friendly": "⚠️ Request crypto-accepting sites explicitly",
                 "Fit for Nonbank": "P1 — volume buy for DR30–50 US tier",
                 "Priority": "P1"},
                {"Platform": "OutreachZ",
                 "Origin": "UK / Global",
                 "Catalog": "Curated marketplace of niche sites",
                 "Model": "Pay per placement; niche-matched",
                 "Price range (crypto)": "$80–600 / article",
                 "Language": "EN primary",
                 "Quality control": "Manual match + editor review",
                 "Crypto-friendly": "⚠️ Has crypto category on request",
                 "Fit for Nonbank": "P2 — backup / test",
                 "Priority": "P2"},
                {"Platform": "SE Ranking Marketplace",
                 "Origin": "Global (SE Ranking SEO tool)",
                 "Catalog": "Integrated backlink/guest-post marketplace inside the SE Ranking platform",
                 "Model": "Pay per placement; DR/traffic-filtered catalog",
                 "Price range (crypto)": "$50–800 / article",
                 "Language": "Multi-language",
                 "Quality control": "Metrics-gated; needs SE Ranking subscription",
                 "Crypto-friendly": "⚠️ Some crypto outlets",
                 "Fit for Nonbank": "P2 — only if already using SE Ranking",
                 "Priority": "P2"},
                {"Platform": "Linkifier",
                 "Origin": "US / Global",
                 "Catalog": "Backlink marketplace",
                 "Model": "Pay per link; DR-based pricing",
                 "Price range (crypto)": "$50–500 / link",
                 "Language": "EN",
                 "Quality control": "Basic metrics filtering",
                 "Crypto-friendly": "⚠️ Mixed",
                 "Fit for Nonbank": "P2 — generic SEO link farm risk",
                 "Priority": "P2"},
                {"Platform": "Crypto-PR.io / Crypto-Guestposting.com",
                 "Origin": "Global (crypto-niche resellers)",
                 "Catalog": "Resold inventory across multiple wires + outlets",
                 "Model": "Flat packages ($X for Y placements)",
                 "Price range (crypto)": "$300–3,000 / package",
                 "Language": "EN",
                 "Quality control": "**Variable — verify each package**",
                 "Crypto-friendly": "✅ Crypto-only by design",
                 "Fit for Nonbank": "P2 — only if price-per-placement beats Collaborator/PRPosting on same DR",
                 "Priority": "P2"},
                {"Platform": "Prowly / BuzzStream / Muck Rack",
                 "Origin": "US / EU",
                 "Catalog": "NOT marketplaces — journalist & media CRM tools",
                 "Model": "Subscription; you do the outreach yourself",
                 "Price range (crypto)": "$100–500 / mo tool cost",
                 "Language": "EN",
                 "Quality control": "DIY outreach",
                 "Crypto-friendly": "N/A",
                 "Fit for Nonbank": "P2 — useful for earned PR, not volume guest posts",
                 "Priority": "P2 (different use case)"},
            ])
            st.dataframe(marketplaces, use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("#### Press-release distribution wires")
            wires = pd.DataFrame([
                {"Wire": "Chainwire",
                 "Type": "Crypto-native PR wire",
                 "Distribution": "100+ crypto outlets incl. Cointelegraph, Decrypt, CryptoSlate, Bitcoinist, NewsBTC, CryptoPotato, U.Today",
                 "Cost / release": "$450–900 (tiered packages)",
                 "Speed": "24–48 hrs",
                 "Best for": "Multi-outlet coverage from one filing",
                 "Priority": "**P0**"},
                {"Wire": "Cryptonews.com PR (PR wire)",
                 "Type": "Crypto-native",
                 "Distribution": "Cryptonews network + partner tier-2/3 sites",
                 "Cost / release": "$300–800",
                 "Speed": "24–72 hrs",
                 "Best for": "Additional tier-2 coverage",
                 "Priority": "P1"},
                {"Wire": "CoinCodex PR",
                 "Type": "Crypto-native",
                 "Distribution": "CoinCodex + partnered aggregators",
                 "Cost / release": "$200–600",
                 "Speed": "24–48 hrs",
                 "Best for": "Cheap tier-2 distribution",
                 "Priority": "P1"},
                {"Wire": "Blockchain PR Buzz",
                 "Type": "Crypto PR aggregator",
                 "Distribution": "50+ crypto outlets",
                 "Cost / release": "$300–1,000",
                 "Speed": "48–72 hrs",
                 "Best for": "Budget multi-outlet distribution",
                 "Priority": "P1"},
                {"Wire": "CryptoPR.io",
                 "Type": "Crypto PR marketplace",
                 "Distribution": "Curated tier-1/2 placement",
                 "Cost / release": "$500–3,000 (premium packages)",
                 "Speed": "3–7 days",
                 "Best for": "Higher-tier single placements",
                 "Priority": "P1"},
                {"Wire": "AccessWire (crypto tier)",
                 "Type": "General + crypto wire",
                 "Distribution": "Syndicates to Yahoo Finance, MarketWatch + crypto outlets",
                 "Cost / release": "$500–1,200",
                 "Speed": "24 hrs",
                 "Best for": "SEO backlinks from high-DR mainstream finance sites",
                 "Priority": "**P0** (one release for the Yahoo/MW backlink)"},
                {"Wire": "GlobeNewswire",
                 "Type": "Mainstream PR wire",
                 "Distribution": "Reuters + mainstream finance + aggregators",
                 "Cost / release": "$350–2,000",
                 "Speed": "24 hrs",
                 "Best for": "Mainstream finance media backlinks",
                 "Priority": "P1"},
                {"Wire": "PR Newswire",
                 "Type": "Mainstream premier wire",
                 "Distribution": "Premium syndication (Cision network)",
                 "Cost / release": "$800–5,000",
                 "Speed": "24 hrs",
                 "Best for": "Corporate-grade announcements (product launches)",
                 "Priority": "P2 (expensive for sprint)"},
                {"Wire": "Business Wire",
                 "Type": "Mainstream premier wire",
                 "Distribution": "Berkshire Hathaway co; premium",
                 "Cost / release": "$700–4,000",
                 "Speed": "24 hrs",
                 "Best for": "Enterprise-looking announcements",
                 "Priority": "P2"},
                {"Wire": "PRWeb (Cision)",
                 "Type": "Mainstream wire",
                 "Distribution": "Broad syndication, moderate reach",
                 "Cost / release": "$99–389",
                 "Speed": "24–72 hrs",
                 "Best for": "Cheap mainstream wire coverage",
                 "Priority": "P1"},
                {"Wire": "EIN Presswire",
                 "Type": "Mainstream wire (self-serve)",
                 "Distribution": "Broad auto-syndication",
                 "Cost / release": "$99–400",
                 "Speed": "2–24 hrs",
                 "Best for": "Cheapest wire option — SEO backlinks",
                 "Priority": "P1"},
            ])
            st.dataframe(wires, use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("#### Crypto PR agencies (for-reference, not sprint scope)")
            agencies = pd.DataFrame([
                {"Agency": "NinjaPromo", "Service": "Crypto PR + marketing retainer",
                 "Retainer": "$8K–25K/mo", "Why consider": "Full-stack crypto campaigns, but retainer-scale not sprint.",
                 "Sprint fit": "❌ Skip — Month 2+ option"},
                {"Agency": "Guerrilla Buzz", "Service": "Crypto PR + Reddit + community",
                 "Retainer": "$5K–15K/mo", "Why consider": "Community-first; aligned with our Reddit/Quora play.",
                 "Sprint fit": "❌ Skip — Month 2+ option"},
                {"Agency": "Lunar Strategy", "Service": "Web3 growth agency",
                 "Retainer": "$5K–20K/mo", "Why consider": "Campaign strategy + execution",
                 "Sprint fit": "❌ Skip"},
                {"Agency": "Coinbound", "Service": "Crypto marketing + PR",
                 "Retainer": "$5K–15K/mo", "Why consider": "Media relationships",
                 "Sprint fit": "❌ Skip"},
                {"Agency": "MarketAcross", "Service": "Crypto PR + content",
                 "Retainer": "$10K+/mo", "Why consider": "Tier-1 placements",
                 "Sprint fit": "❌ Skip — retainer scale"},
            ])
            st.dataframe(agencies, use_container_width=True, hide_index=True)
            st.caption(
                "**Why agencies are out of sprint scope:** they bill on "
                "monthly retainer and need 4–6 weeks to warm up. The whole "
                "sprint is 4 weeks. Re-evaluate for Month 2+ if the in-house "
                "+ marketplaces path underperforms."
            )

            st.divider()
            st.success(
                "**Recommended sprint stack — volume marketplaces + wires (~$4–5K total, 12–18 placements):**\n\n"
                "**Core P0 marketplaces (run in parallel — don't pick one, use all five):**\n"
                "1. **Collaborator.pro** — 3–4× DR50+ crypto outlets (~$700–1,400). Already wired into the app.\n"
                "2. **PRPosting** — 3–4× outlets Collaborator doesn't stock, often cheaper at same DR (~$500–1,000).\n"
                "3. **WhitePress** — 2× European outlets for geo-diversity / different language footprint (~$400–1,000).\n"
                "4. **Linkhouse.co** — 2× Polish/EU crypto-category outlets, closest WhitePress alternative, often cheaper (~$300–700).\n"
                "5. **Serpzilla** — 2× crypto-specialized outlets (every site is on-topic → less filtering, faster approval) (~$300–700).\n\n"
                "**Wires (add to above for syndication):**\n"
                "6. **Chainwire** — 1 release (~$450–900) → 20+ outlets from one filing.\n"
                "7. **AccessWire** — 1 release (~$500–1,200) → Yahoo Finance / MarketWatch backlinks.\n\n"
                "**Result:** 12–18 unique outlets **plus** 20+ syndicated "
                "mentions from Chainwire, spread across UA/CIS + EU + crypto-"
                "native networks. Mixes geos, languages, and outlet types — "
                "strongest possible breadth signal for GEO/SEO in 2–3 weeks."
            )
            st.warning(
                "**Quality gate:** before booking any outlet on a marketplace, "
                "check: (1) DR ≥ 40, (2) crypto/fintech articles published in "
                "the last 30 days, (3) sample article is editorial (not PBN-"
                "style thin content), (4) do-follow link permitted, (5) "
                "article stays indexed ≥ 12 months. Use the app's **Outlet "
                "Matching** tab to cross-reference Collaborator DR/price/score."
            )

        # ── Sub-tab: PR / Guest Posts ──────────────────────────────────────
        with sub_pr:
            st.markdown("**Paid editorial + guest posts. Primary GEO-citation fuel.**")
            pr_outlets = pd.DataFrame([
                {"Outlet": "Cointelegraph (sponsored)", "Type": "Tier-1 crypto media", "DR": "91",
                 "Est. cost": "$4–8K", "Fit": "High (card audience)", "Priority": "P1 (stretch)"},
                {"Outlet": "Decrypt (sponsored)", "Type": "Tier-1 crypto media", "DR": "88",
                 "Est. cost": "$3–6K", "Fit": "High", "Priority": "P1"},
                {"Outlet": "CoinDesk (sponsored)", "Type": "Tier-1 crypto media", "DR": "92",
                 "Est. cost": "$5–10K", "Fit": "Medium (institutional lean)", "Priority": "P2"},
                {"Outlet": "CryptoSlate (sponsored)", "Type": "Tier-2 crypto media", "DR": "82",
                 "Est. cost": "$1.5–3K", "Fit": "High", "Priority": "P0"},
                {"Outlet": "BeInCrypto", "Type": "Tier-2 crypto media", "DR": "81",
                 "Est. cost": "$1–2.5K", "Fit": "High (retail DeFi audience)", "Priority": "P0"},
                {"Outlet": "NewsBTC", "Type": "Tier-2 crypto media", "DR": "79",
                 "Est. cost": "$800–2K", "Fit": "Medium-High", "Priority": "P0"},
                {"Outlet": "Bitcoinist", "Type": "Tier-2 crypto media", "DR": "78",
                 "Est. cost": "$600–1.5K", "Fit": "Medium", "Priority": "P1"},
                {"Outlet": "CryptoPotato", "Type": "Tier-2 crypto media", "DR": "78",
                 "Est. cost": "$700–1.5K", "Fit": "High (retail)", "Priority": "P0"},
                {"Outlet": "Cryptonews.com", "Type": "Tier-2 aggregator+media", "DR": "80",
                 "Est. cost": "$700–1.5K", "Fit": "High", "Priority": "P0"},
                {"Outlet": "Collaborator.pro network (70+ outlets)", "Type": "DR40–70 guest-post marketplace", "DR": "40–70",
                 "Est. cost": "$150–800", "Fit": "Mid (volume + backlinks)", "Priority": "P0"},
                {"Outlet": "Chainwire (PR wire)", "Type": "Crypto press-release distribution", "DR": "—",
                 "Est. cost": "$450–900 / release", "Fit": "Broad syndication (100+ sites)", "Priority": "P0"},
                {"Outlet": "AccessWire / GlobeNewswire (crypto tier)", "Type": "General PR wire", "DR": "—",
                 "Est. cost": "$500–1,200 / release", "Fit": "SEO backlinks + trad-finance reach", "Priority": "P1"},
                {"Outlet": "Blockonomi", "Type": "Long-form crypto blog", "DR": "72",
                 "Est. cost": "$400–900", "Fit": "High (comparison-style reviews)", "Priority": "P0"},
                {"Outlet": "CoinJournal", "Type": "Crypto news", "DR": "73",
                 "Est. cost": "$400–800", "Fit": "Medium", "Priority": "P1"},
                {"Outlet": "CoinGape", "Type": "Tier-2 crypto news", "DR": "75",
                 "Est. cost": "$500–1,000", "Fit": "Medium", "Priority": "P1"},
                {"Outlet": "AMBCrypto", "Type": "Tier-2 crypto news", "DR": "76",
                 "Est. cost": "$500–1,200", "Fit": "Medium-High", "Priority": "P1"},
                {"Outlet": "U.Today", "Type": "Tier-2 crypto news", "DR": "74",
                 "Est. cost": "$400–900", "Fit": "Medium", "Priority": "P1"},
                {"Outlet": "CryptoBriefing", "Type": "Tier-2 analysis", "DR": "74",
                 "Est. cost": "$1–2K", "Fit": "High (DeFi-literate readers)", "Priority": "P0"},
            ])
            st.dataframe(pr_outlets, use_container_width=True, hide_index=True)
            st.success(
                "**Sprint pick (within $5–15K):** CryptoSlate **+** BeInCrypto **or** "
                "CryptoPotato **+** 1× Chainwire release **+** 2–3× "
                "Collaborator.pro DR50+ mid-tier **+** 2–3× PRPosting DR40–60 "
                "**+** 1× WhitePress EU outlet. Total ≈ $4–6K, 8–10 placements "
                "across 30+ outlets (including Chainwire syndication), strong "
                "backlink + GEO footprint. See **Aggregators & Marketplaces** "
                "sub-tab for the full marketplace stack."
            )

        # ── Sub-tab: Ad Networks ───────────────────────────────────────────
        with sub_adnet:
            st.markdown(
                "**Crypto-native display / native-ad networks.** These are "
                "the **only compliant paid surfaces** for a DeFi wallet — "
                "they don't require a financial-services license. Mainstream "
                "ad platforms (Google, Meta, LinkedIn, TikTok, YouTube) "
                "**reject DeFi wallet ads** without a license and are "
                "excluded from this plan."
            )
            ad_nets = pd.DataFrame([
                {"Platform": "Coinzilla", "Format": "Display, native, push",
                 "Reach": "1B+ crypto impressions/mo", "Min. budget": "$500",
                 "Typical CPM": "$1.50–4", "Fit": "Retargeting + awareness", "Status": "✅ Compliant", "Priority": "P0"},
                {"Platform": "Bitmedia", "Format": "Display, native",
                 "Reach": "600M+ crypto impressions/mo", "Min. budget": "$100",
                 "Typical CPM": "$1–3", "Fit": "Retargeting", "Status": "✅ Compliant", "Priority": "P0"},
                {"Platform": "Cointraffic", "Format": "Display, native, pop",
                 "Reach": "Premium crypto pubs", "Min. budget": "$500",
                 "Typical CPM": "$2–5", "Fit": "Premium awareness", "Status": "✅ Compliant", "Priority": "P0"},
                {"Platform": "A-ADS", "Format": "Display (anonymous, BTC-paid)",
                 "Reach": "Niche crypto forums", "Min. budget": "$10",
                 "Typical CPM": "$0.50–2", "Fit": "Cheap long-tail testing", "Status": "✅ Compliant", "Priority": "P1"},
                {"Platform": "Adshares", "Format": "Programmatic (web3)",
                 "Reach": "Web3 dapp ad slots", "Min. budget": "$100",
                 "Typical CPM": "$1–3", "Fit": "DeFi-native placements", "Status": "✅ Compliant", "Priority": "P1"},
                {"Platform": "Dao.Ad", "Format": "Native crypto ads",
                 "Reach": "Mid-tier crypto sites", "Min. budget": "$200",
                 "Typical CPM": "$1–3", "Fit": "Backup / scale-up", "Status": "✅ Compliant", "Priority": "P2"},
                {"Platform": "Brave Ads (Basic Attention Token)", "Format": "Browser-native, privacy-first",
                 "Reach": "Brave browser users (crypto-skewed)", "Min. budget": "$2.5K typical min",
                 "Typical CPM": "$3–8", "Fit": "Privacy-audience match", "Status": "✅ Crypto-friendly", "Priority": "P2"},
                {"Platform": "X/Twitter Ads", "Format": "Promoted posts",
                 "Reach": "Crypto Twitter", "Min. budget": "$50/day",
                 "Typical CPM": "$6–12", "Fit": "Amplify founder threads",
                 "Status": "⚠️ Requires crypto-cat cert; case-by-case approval", "Priority": "P1 (conditional)"},
                {"Platform": "Reddit Ads", "Format": "Promoted post, sub-targeted",
                 "Reach": "r/CryptoCurrency, r/defi, r/ethfinance", "Min. budget": "$5/day",
                 "Typical CPM": "$3–8", "Fit": "Sub-targeted conquest",
                 "Status": "⚠️ Approved case-by-case for crypto wallets", "Priority": "P1 (conditional)"},
                {"Platform": "Google Ads (search + display)", "Format": "Search, display, YouTube",
                 "Reach": "Mainstream", "Min. budget": "—",
                 "Typical CPM": "—", "Fit": "Would be primary if allowed",
                 "Status": "🚫 **BLOCKED** — DeFi wallet ads rejected without FinCEN/MSB license", "Priority": "Excluded"},
                {"Platform": "Meta (Facebook/Instagram) Ads", "Format": "Social feed, reels",
                 "Reach": "Mainstream", "Min. budget": "—",
                 "Typical CPM": "—", "Fit": "—",
                 "Status": "🚫 **BLOCKED** — crypto wallet = prohibited financial product", "Priority": "Excluded"},
                {"Platform": "LinkedIn Ads", "Format": "B2B social",
                 "Reach": "Professional", "Min. budget": "—",
                 "Typical CPM": "—", "Fit": "—",
                 "Status": "🚫 **BLOCKED** — crypto wallet prohibited", "Priority": "Excluded"},
                {"Platform": "TikTok Ads", "Format": "Short video",
                 "Reach": "Mainstream retail", "Min. budget": "—",
                 "Typical CPM": "—", "Fit": "—",
                 "Status": "🚫 **BLOCKED** — crypto-restricted in most regions", "Priority": "Excluded"},
                {"Platform": "YouTube Ads (pre-roll)", "Format": "Video",
                 "Reach": "Crypto review channels", "Min. budget": "—",
                 "Typical CPM": "—", "Fit": "—",
                 "Status": "🚫 **BLOCKED** — Google-owned, same wallet-ad policy", "Priority": "Excluded"},
            ])
            st.dataframe(ad_nets, use_container_width=True, hide_index=True)
            st.success(
                "**Sprint pick (crypto-native only, ≈$2.5K total):** "
                "Coinzilla ($1K, native + retargeting) **+** Bitmedia ($700, "
                "retargeting comparison-page visitors) **+** Cointraffic "
                "($500, premium pub placements) **+** A-ADS ($300, cheap "
                "long-tail test). Optional: X Ads + Reddit Ads ($500–1K total) "
                "**only after Nonbank confirms crypto-category certification**."
            )
            st.warning(
                "**Workaround for mainstream reach:** to appear in Google / "
                "YouTube results for DeFi wallet queries, rely on **SEO + GEO** "
                "(comparison pages) and **YouTuber sponsorships** (direct-buy, "
                "not via YouTube Ads). Direct creator deals aren't subject to "
                "the ad-platform policy."
            )

        # ── Sub-tab: Listings & Aggregators ─────────────────────────────────
        with sub_listing:
            st.markdown(
                "**Free or low-cost listings where comparison-shoppers discover "
                "wallets & cards.** Claim listings, verify data, request feature updates."
            )
            listings = pd.DataFrame([
                {"Platform": "CoinGecko (wallet + card listing)", "Type": "Data aggregator", "DR": "92",
                 "Cost": "Free listing; $2–5K for promoted slots", "Fit": "Very high — huge traffic", "Priority": "P0"},
                {"Platform": "CoinMarketCap (wallet directory)", "Type": "Data aggregator", "DR": "93",
                 "Cost": "Free listing; paid promo available", "Fit": "Very high", "Priority": "P0"},
                {"Platform": "DappRadar (wallet category)", "Type": "Web3 dapp directory", "DR": "82",
                 "Cost": "Free", "Fit": "High (DeFi audience)", "Priority": "P0"},
                {"Platform": "DeFiLlama (wallet/protocols)", "Type": "DeFi data", "DR": "81",
                 "Cost": "Free (submit PR)", "Fit": "High (DeFi-literate)", "Priority": "P0"},
                {"Platform": "CoinPaprika (wallet directory)", "Type": "Data aggregator", "DR": "77",
                 "Cost": "Free", "Fit": "Medium", "Priority": "P1"},
                {"Platform": "CoinCarp (wallets & cards)", "Type": "Aggregator", "DR": "70",
                 "Cost": "Free listing; paid promo", "Fit": "High (explicitly lists crypto cards)", "Priority": "P0"},
                {"Platform": "Coinstats (wallet tracker integration)", "Type": "Portfolio tracker", "DR": "74",
                 "Cost": "Free listing; integration partner", "Fit": "High (wallet audience)", "Priority": "P1"},
                {"Platform": "CryptoCompare (wallet reviews)", "Type": "Review aggregator", "DR": "82",
                 "Cost": "Free; paid featured reviews", "Fit": "High", "Priority": "P0"},
                {"Platform": "Alternativeto.net (MetaMask alt)", "Type": "Software alternatives directory", "DR": "87",
                 "Cost": "Free submission", "Fit": "**High — literally captures 'alternative to' queries**", "Priority": "P0"},
                {"Platform": "Product Hunt (launch)", "Type": "Tech launch platform", "DR": "92",
                 "Cost": "Free (requires hunter + launch prep)", "Fit": "Medium (tech crowd, not pure crypto)", "Priority": "P1"},
                {"Platform": "Wallet Scrutiny", "Type": "Wallet security review", "DR": "45",
                 "Cost": "Free", "Fit": "Trust signal for self-custody angle", "Priority": "P1"},
            ])
            st.dataframe(listings, use_container_width=True, hide_index=True)
            st.warning(
                "**Do in Week 1:** claim/verify all P0 listings. These are "
                "free, compound forever, and seed LLM training data "
                "(Perplexity/ChatGPT pull from CoinGecko, CMC, DappRadar)."
            )

        # ── Sub-tab: Review / Comparison ───────────────────────────────────
        with sub_review:
            st.markdown(
                "**Review and comparison sites ranking for 'best crypto "
                "card' / 'gnosis pay vs' queries.** Pitch to get Nonbank "
                "added; sponsor featured placements where it pays back."
            )
            reviews = pd.DataFrame([
                {"Site": "CryptoWallet-Comparison.com", "Traffic driver": "'Best crypto wallet' + card queries",
                 "Add method": "Pitch review / paid placement",
                 "Est. cost": "Free pitch; $500–2K for featured", "Priority": "P0"},
                {"Site": "Finder.com (crypto card section)", "Traffic driver": "Mainstream + crypto crossover",
                 "Add method": "Affiliate + editorial pitch",
                 "Est. cost": "CPA/revshare", "Priority": "P0"},
                {"Site": "CryptoNews Wallet Reviews", "Traffic driver": "Review-intent search",
                 "Add method": "Paid review",
                 "Est. cost": "$800–2K", "Priority": "P1"},
                {"Site": "Cryptotesters.com", "Traffic driver": "Card comparison rankings",
                 "Add method": "Pitch inclusion",
                 "Est. cost": "Free / sponsorship tier", "Priority": "P0"},
                {"Site": "BestWallet / TopCryptoWallets listicles", "Traffic driver": "'Best X for Y' SEO farms",
                 "Add method": "Paid placement or affiliate",
                 "Est. cost": "$500–3K depending on rank position", "Priority": "P1"},
                {"Site": "BanklessTimes (reviews)", "Traffic driver": "Card/wallet review SEO",
                 "Add method": "Editorial pitch + paid",
                 "Est. cost": "$1–2K", "Priority": "P1"},
                {"Site": "DeFiPrime", "Traffic driver": "DeFi project directory",
                 "Add method": "Free submission",
                 "Est. cost": "Free", "Priority": "P0"},
                {"Site": "Cryptorank.io", "Traffic driver": "Project ranking",
                 "Add method": "Free + paid promo",
                 "Est. cost": "Free / $500+ promo", "Priority": "P1"},
            ])
            st.dataframe(reviews, use_container_width=True, hide_index=True)

        # ── Sub-tab: Newsletters ───────────────────────────────────────────
        with sub_news:
            st.markdown(
                "**Paid sponsorships in crypto newsletters** — high-intent, "
                "deeply engaged audiences. CPM is high but conversion quality "
                "beats most display."
            )
            news = pd.DataFrame([
                {"Newsletter": "Milk Road", "Audience": "330K+ retail crypto",
                 "Sponsorship cost": "$8–15K / primary sponsor",
                 "Fit": "Very high (card-buying demo)", "Priority": "P2 (stretch budget)"},
                {"Newsletter": "Bankless", "Audience": "200K+ DeFi-native",
                 "Sponsorship cost": "$5–12K / slot",
                 "Fit": "Perfect audience match", "Priority": "P2"},
                {"Newsletter": "Blockworks Daily", "Audience": "Institutional + retail",
                 "Sponsorship cost": "$4–8K / slot",
                 "Fit": "Medium (more institutional)", "Priority": "P2"},
                {"Newsletter": "The Defiant", "Audience": "80K+ DeFi power users",
                 "Sponsorship cost": "$2–5K / slot",
                 "Fit": "**High for sprint budget**", "Priority": "P1"},
                {"Newsletter": "DeFi Pulse / DeFi Prime", "Audience": "DeFi-focused",
                 "Sponsorship cost": "$1–3K", "Fit": "High", "Priority": "P1"},
                {"Newsletter": "The Tie Insights", "Audience": "Institutional data-driven",
                 "Sponsorship cost": "$3–6K", "Fit": "Low for retail card", "Priority": "P2"},
                {"Newsletter": "CryptoPragmatist", "Audience": "Trader-leaning",
                 "Sponsorship cost": "$500–1.5K", "Fit": "Medium", "Priority": "P2"},
            ])
            st.dataframe(news, use_container_width=True, hide_index=True)
            st.caption(
                "Newsletter sponsorships generally blow the sprint budget. "
                "Realistic pick: **The Defiant** (1 slot ≈ $3K) **or** skip to Month 2."
            )

        # ── Sub-tab: Podcasts ──────────────────────────────────────────────
        with sub_pod:
            st.markdown(
                "**Crypto podcast ad reads / sponsorships.** High cost, slow "
                "production, strong brand build. Month 2+ territory unless "
                "you have a tight pitch ready."
            )
            pods = pd.DataFrame([
                {"Show": "Bankless", "Host": "David Hoffman / Ryan Sean Adams",
                 "Audience": "DeFi-native", "Cost": "$8–15K / host-read", "Priority": "P2"},
                {"Show": "The Breakdown (NLW)", "Host": "NLW",
                 "Audience": "Macro + crypto", "Cost": "$5–10K", "Priority": "P2"},
                {"Show": "Unchained (Laura Shin)", "Host": "Laura Shin",
                 "Audience": "Institutional + retail", "Cost": "$6–12K", "Priority": "P2"},
                {"Show": "The Defiant Podcast", "Host": "Camila Russo",
                 "Audience": "DeFi deep-dive", "Cost": "$2–5K", "Priority": "P1"},
                {"Show": "Zero Knowledge", "Host": "Anna Rose",
                 "Audience": "Technical crypto", "Cost": "$2–4K", "Priority": "P2 (wrong audience)"},
                {"Show": "Smaller DeFi YouTubers (CoinBureau-tier micro)", "Host": "Various",
                 "Audience": "Retail crypto reviewers", "Cost": "$500–3K / sponsored review", "Priority": "P1 (micro-KOL)"},
            ])
            st.dataframe(pods, use_container_width=True, hide_index=True)

        # ── Sub-tab: Community ─────────────────────────────────────────────
        with sub_community:
            st.markdown(
                "**Organic community surfaces.** Zero cost, high time-investment, "
                "best long-run compounding. These also **feed LLM citations**."
            )
            comms = pd.DataFrame([
                {"Surface": "r/CryptoCurrency", "Members": "9M+",
                 "Strategy": "Value-first comments on card/wallet threads", "Priority": "P0"},
                {"Surface": "r/defi", "Members": "280K+",
                 "Strategy": "DeFi-native discussions; card + gasless angle", "Priority": "P0"},
                {"Surface": "r/ethfinance", "Members": "180K+",
                 "Strategy": "ETH-adjacent; MetaMask Card comparison", "Priority": "P0"},
                {"Surface": "r/Gnosis + r/GnosisPay", "Members": "25K+",
                 "Strategy": "Direct conquest — frustrated EU-limited users", "Priority": "P0"},
                {"Surface": "r/CryptoCards (niche)", "Members": "Small but targeted",
                 "Strategy": "Every thread is buying-intent", "Priority": "P0"},
                {"Surface": "Quora (crypto card + wallet topics)", "Members": "Long-tail SEO",
                 "Strategy": "Answer once, ranks for years", "Priority": "P0"},
                {"Surface": "Crypto Twitter (quote-RT / replies)", "Members": "Founder + brand handle",
                 "Strategy": "Reply in Gnosis Pay / MetaMask Card mentions", "Priority": "P0"},
                {"Surface": "Discord (Gnosis, MetaMask, DeFi communities)", "Members": "Tens of thousands",
                 "Strategy": "Presence only; no direct shilling (rules)", "Priority": "P1"},
                {"Surface": "Telegram crypto channels", "Members": "Varies",
                 "Strategy": "AMAs + partnered channels", "Priority": "P1"},
                {"Surface": "Farcaster / Warpcast", "Members": "Growing web3-native",
                 "Strategy": "Founder presence + $NON-native posts", "Priority": "P1"},
                {"Surface": "Lens Protocol", "Members": "Smaller but DeFi-native",
                 "Strategy": "Founder posting", "Priority": "P2"},
                {"Surface": "Hacker News (when relevant)", "Members": "Tech-first",
                 "Strategy": "Only for product launches / technical posts", "Priority": "P2"},
            ])
            st.dataframe(comms, use_container_width=True, hide_index=True)
            st.success(
                "**Sprint community rule:** 15–25 Reddit/Quora comments + "
                "daily founder X + 1 AMA in a partnered TG channel. Zero "
                "paid spend here — all compounds into GEO and organic trust."
            )

        # ── Summary allocation ─────────────────────────────────────────────
        st.divider()
        st.subheader("Recommended sprint allocation across outlets ($10K midpoint)")
        alloc = pd.DataFrame([
            {"Bucket": "PR placements (direct + marketplaces + wires)",
             "Picks": "1× CryptoSlate or BeInCrypto direct + 2–3× Collaborator + 2–3× PRPosting + 1× WhitePress (EU) + 1× Chainwire + 1× AccessWire",
             "Amount": "$4,000", "Why": "8–10 placements across 30+ outlets. Backlinks + GEO citations + no ad-policy risk."},
            {"Bucket": "Crypto-native paid ads", "Picks": "Coinzilla + Bitmedia + Cointraffic + A-ADS",
             "Amount": "$2,500", "Why": "Only compliant paid surface for DeFi wallet. Retargeting comparison-page visitors."},
            {"Bucket": "Newsletter sponsorship (direct-buy)", "Picks": "The Defiant slot or 2× smaller DeFi newsletters",
             "Amount": "$1,500", "Why": "Direct-buy = bypasses ad-platform policy. High-engagement audience."},
            {"Bucket": "Micro-KOL seeds (direct-deal)", "Picks": "2× Twitter micro + 1× small YouTuber review",
             "Amount": "$1,500", "Why": "Direct-to-creator = no ad policy gate. Message testing."},
            {"Bucket": "Telegram channel sponsorships", "Picks": "2–3 sponsored posts in niche DeFi TG channels",
             "Amount": "$500", "Why": "Direct-buy; strong crypto-native reach by geo."},
            {"Bucket": "Listings + community", "Picks": "Claim all P0 listings; Reddit/Quora/X effort",
             "Amount": "$0 (time only)", "Why": "Highest long-run ROI. Labor-heavy."},
            {"Bucket": "Production overflow", "Picks": "Design, comparison-table infographic, landing-page polish",
             "Amount": "—", "Why": "Absorbed into PR / KOL line items"},
        ])
        st.dataframe(alloc, use_container_width=True, hide_index=True)
        st.caption(
            "Total: $10,000 ± contingency. If budget stretches to $15K: add "
            "The Defiant primary slot ($3K), CryptoPotato as a second PR ($1K), "
            "and 1 tier-1 TG channel sponsorship ($1K). If compressed to $5K: "
            "2 PR placements only (BeInCrypto + 1 Collaborator) + $1K "
            "Coinzilla + 1 micro-KOL. **Google/Meta/LinkedIn Ads are excluded "
            "at every budget tier — DeFi wallets require a license those "
            "platforms don't grant.**"
        )

    # ── 4c. Content to Publish ──────────────────────────────────────────────
    with tab_content:
        st.subheader("Content to Publish — Sprint Deliverables")
        st.caption(
            "Two content streams: **(A)** on-site comparison pages on "
            "nonbank.io/blog (SEO/GEO anchor assets); **(B)** guest-post "
            "articles pushed through marketplaces (Serpzilla + Collaborator "
            "+ PRPosting + WhitePress + Linkhouse). Every guest-post brief "
            "is **spun into 3–4 angle variants** so the same argument hits "
            "different outlets without duplicate-content risk."
        )

        st.info(
            "**Scoring model update:** `publication_roi.py` now takes a "
            "`content_type` parameter — guest posts get 1.0× SEO/GEO weight, "
            "link insertions get 0.45× SEO and **0.10× GEO** (no new article "
            "to cite), PR wires get 0.55×/0.35×. Marketplaces that only sell "
            "link insertions are now deprioritized automatically in the "
            "Publication ROI tab."
        )

        st.markdown("### A · On-site comparison pages (nonbank.io/blog)")
        st.markdown(
            "Built in Content Brief Factory → PR Generator. These are the "
            "**anchor pages** — everything else links back here."
        )
        onsite = pd.DataFrame([
            {"#": 1, "URL slug": "/blog/gnosis-pay-alternative",
             "Target keyword": "gnosis pay alternative", "Est. volume": "1.6K/mo",
             "Angle": "Why EU-only isn't enough; 100+ country alternative with gasless + AML", "Length": "1,800w"},
            {"#": 2, "URL slug": "/blog/metamask-card-alternative",
             "Target keyword": "metamask card alternative", "Est. volume": "880/mo",
             "Angle": "Pilot vs. live; full-release self-custody card", "Length": "1,800w"},
            {"#": 3, "URL slug": "/blog/coca-wallet-alternative",
             "Target keyword": "coca wallet alternative / vs nonbank", "Est. volume": "320/mo",
             "Angle": "MPC vs. hybrid DeFi wallet; AML presence/absence", "Length": "1,500w"},
            {"#": 4, "URL slug": "/blog/bleap-vs-nonbank",
             "Target keyword": "bleap card vs nonbank / alternative", "Est. volume": "210/mo",
             "Angle": "Mastercard+MPC vs. Visa+hybrid; KYC + AML comparison", "Length": "1,500w"},
            {"#": 5, "URL slug": "/blog/crypto-com-card-self-custody-alternative",
             "Target keyword": "crypto.com card alternative self custody", "Est. volume": "590/mo",
             "Angle": "Fully custodial vs. hybrid; own your keys + still spend", "Length": "1,800w"},
            {"#": 6, "URL slug": "/blog/best-self-custody-crypto-cards-2026",
             "Target keyword": "best self custody crypto card 2026", "Est. volume": "720/mo",
             "Angle": "Category listicle — Gnosis Pay / MetaMask Card / COCA / Bleap / Nonbank / Crypto.com", "Length": "2,400w"},
            {"#": 7, "URL slug": "/blog/self-custody-crypto-cards-hub",
             "Target keyword": "self custody crypto card (hub)", "Est. volume": "1.1K/mo",
             "Angle": "**Category hub** — links to all 6 above; canonical pillar page", "Length": "2,800w"},
        ])
        st.dataframe(onsite, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### B · Guest-post articles (marketplace placements)")
        st.markdown(
            "**6 master briefs × 3–4 angle variants each = ~18–24 "
            "unique articles** to distribute across marketplaces. Anchor "
            "text rotates per variant. Internal link always points back to "
            "the relevant on-site comparison page."
        )

        briefs = pd.DataFrame([
            {
                "Brief #": "GP-1",
                "Master title": "Why Gnosis Pay Isn't Enough Outside the EU",
                "Primary message": "#1 Card inside wallet + #2 100+ countries",
                "Outline": "1) Gnosis Pay's EU/UK limitation; 2) Card+wallet category explained; 3) What to look for in a 100+ country alternative; 4) Nonbank (NON×CARD) as a live example",
                "Word count": "1,200–1,500",
                "Anchor text variants": "gnosis pay alternative · best gnosis pay alternative · non-EU gnosis pay · self-custody card in 100+ countries",
                "Internal link target": "/blog/gnosis-pay-alternative",
                "Best marketplace": "Serpzilla (crypto-native) + WhitePress (EU geo)",
                "Variants": "4 (EU-resident angle, APAC angle, LATAM angle, general global)",
            },
            {
                "Brief #": "GP-2",
                "Master title": "MetaMask Card Is Still a Pilot — Here's What's Already Live",
                "Primary message": "#1 Card inside wallet + #2 live in 100+ countries (not pilot)",
                "Outline": "1) MetaMask Card pilot state; 2) What 'live' means for a self-custody card; 3) Category explainer: DeFi wallet + card; 4) Live alternatives comparison",
                "Word count": "1,200–1,500",
                "Anchor text variants": "metamask card alternative · live metamask card alternative · self-custody visa card · defi wallet card",
                "Internal link target": "/blog/metamask-card-alternative",
                "Best marketplace": "Serpzilla + Collaborator + PRPosting",
                "Variants": "3 (retail-user angle, ETH-native angle, card-first angle)",
            },
            {
                "Brief #": "GP-3",
                "Master title": "The Hybrid Model: Non-Custodial Wallet + Custodial Card",
                "Primary message": "Core category education — hero angle #1",
                "Outline": "1) Why fully on-chain cards (Gnosis Pay) are slow; 2) Why fully custodial cards (Crypto.com) give up self-custody; 3) The hybrid model; 4) What good hybrid looks like",
                "Word count": "1,500–1,800",
                "Anchor text variants": "hybrid defi wallet card · self-custody crypto card · defi wallet with card built in · crypto wallet with visa card",
                "Internal link target": "/blog/self-custody-crypto-cards-hub",
                "Best marketplace": "All 5 marketplaces — evergreen explainer",
                "Variants": "4 (explainer, comparison, buyer's-guide, technical-deep-dive)",
            },
            {
                "Brief #": "GP-4",
                "Master title": "Gasless Crypto Transactions: Sending Without ETH for Gas",
                "Primary message": "Differentiator #3 — supporting proof for hero",
                "Outline": "1) Gas as friction; 2) Meta-tx / gas-sponsored models; 3) What gasless actually means for users; 4) Wallets shipping it today",
                "Word count": "1,200–1,500",
                "Anchor text variants": "gasless crypto wallet · no gas fee wallet · send crypto without gas · gasless usdt transfer",
                "Internal link target": "nonbank.io/blog (existing gasless post) + link to hub",
                "Best marketplace": "Serpzilla + Collaborator",
                "Variants": "3 (technical, consumer, stablecoin-user)",
            },
            {
                "Brief #": "GP-5",
                "Master title": "AML in Self-Custody: Can You Have Both?",
                "Primary message": "Differentiator #4 — trust / compliance angle",
                "Outline": "1) Self-custody ≠ freedom from tainted funds; 2) Sanctioned-address exposure cases; 3) AML Watchtower pattern; 4) Wallets that screen inbound transfers",
                "Word count": "1,200–1,500",
                "Anchor text variants": "aml crypto wallet · compliant self-custody wallet · sanction-screening wallet · aml watchtower",
                "Internal link target": "nonbank.io/blog (AML pillar) + link to hub",
                "Best marketplace": "Collaborator + Linkhouse (EU compliance angle resonates)",
                "Variants": "3 (compliance officer, retail trust, trader)",
            },
            {
                "Brief #": "GP-6",
                "Master title": "The 2026 Self-Custody Crypto Card Landscape",
                "Primary message": "Category listicle — hero + proof for all 4 messages",
                "Outline": "1) Category state in 2026; 2) Matrix: Gnosis Pay / MetaMask Card / COCA / Bleap / Crypto.com / Nonbank; 3) Pick-by-use-case (EU resident, global nomad, USDT spender, self-custody purist); 4) What to look for",
                "Word count": "1,800–2,200",
                "Anchor text variants": "best self-custody crypto card · crypto card comparison · defi card 2026 · crypto wallet with card list",
                "Internal link target": "/blog/best-self-custody-crypto-cards-2026 + hub",
                "Best marketplace": "Serpzilla (priority) + PRPosting + WhitePress",
                "Variants": "4 (use-case, ranking, deep-comparison, beginner's-guide)",
            },
        ])
        st.dataframe(briefs, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### C · Distribution matrix — which brief goes to which marketplace")
        dist = pd.DataFrame([
            {"Marketplace": "Serpzilla",      "Placements": 4, "Briefs": "GP-2, GP-3, GP-4, GP-6",
             "Why": "Crypto-native catalog → on-topic sites for every brief; accepts USDT/BTC."},
            {"Marketplace": "Collaborator.pro", "Placements": 3, "Briefs": "GP-1, GP-3, GP-5",
             "Why": "DR50+ curated; already wired in the app (collaborator_outlets.py)."},
            {"Marketplace": "PRPosting",      "Placements": 3, "Briefs": "GP-2, GP-5, GP-6",
             "Why": "Unique outlets Collaborator doesn't stock; often cheaper same-DR."},
            {"Marketplace": "WhitePress",     "Placements": 2, "Briefs": "GP-1 (EU variant), GP-6 (EU variant)",
             "Why": "EU + 40-country multi-language footprint."},
            {"Marketplace": "Linkhouse",      "Placements": 2, "Briefs": "GP-3, GP-5",
             "Why": "PL/EU crypto category; AML/compliance angle resonates in EU."},
            {"Marketplace": "Chainwire (PR wire)", "Placements": "1 release → 20+ sites",
             "Briefs": "Short-form syndication of GP-6 (category listicle)",
             "Why": "One filing = multi-outlet mention blast."},
            {"Marketplace": "AccessWire (PR wire)", "Placements": "1 release",
             "Briefs": "Corporate-framed version of GP-3 (category explainer)",
             "Why": "Yahoo Finance / MarketWatch backlink for DR."},
        ])
        st.dataframe(dist, use_container_width=True, hide_index=True)
        st.caption(
            "**Total: 15 unique guest-post placements + 20+ wire-syndicated "
            "mentions**, covering 6 master briefs across 5 marketplaces and "
            "2 wires. Every placement links to a nonbank.io comparison page — "
            "so SEO/GEO juice concentrates on the anchor assets."
        )

        st.divider()
        st.markdown("### D · Production workflow (Wk 1 sprint)")
        workflow = pd.DataFrame([
            {"Day": "Mon", "Step": "Draft all 6 master briefs in PR Generator (Claude)", "Output": "6 × 1,500w drafts"},
            {"Day": "Tue", "Step": "Spin each master into 3–4 angle variants (PR Generator 'revise' mode)", "Output": "~20 unique variants"},
            {"Day": "Wed", "Step": "Human edit pass + fact-check + anchor-text assignment", "Output": "Ready-to-submit articles"},
            {"Day": "Thu", "Step": "Parallel submission: Serpzilla (4) + Collaborator (3) + PRPosting (3)", "Output": "10 placements queued"},
            {"Day": "Fri", "Step": "WhitePress (2) + Linkhouse (2) + Chainwire release + AccessWire release", "Output": "5 more + wire syndication"},
            {"Day": "Wk 2", "Step": "On-site: publish 6 comparison pages + hub", "Output": "nonbank.io anchor assets live"},
            {"Day": "Wk 2–3", "Step": "Monitor indexation (GSC + Ahrefs) + GEO Tracker for Perplexity/ChatGPT citations", "Output": "Mid-sprint read"},
        ])
        st.dataframe(workflow, use_container_width=True, hide_index=True)

        st.success(
            "**Handoff:** click over to the **PR Generator** tab → paste "
            "each master brief into Claude → generate → paste variants into "
            "the **Distribution** queue. Every article you produce goes to "
            "**one nonbank.io comparison page** as its internal link target — "
            "that's the SEO/GEO concentration mechanism."
        )

    # ── 5. Calendar ─────────────────────────────────────────────────────────
    with tab_calendar:
        st.subheader("Week-by-Week Content Calendar")
        cal = pd.DataFrame([
            {"Week": "Wk 1", "Content": "Keyword + AI audit refresh on competitor terms",
             "Channel": "Keyword Intel + GEO Tracker", "Notes": "Baseline before we publish"},
            {"Week": "Wk 1", "Content": "Draft 6 comparison pages (Gnosis Pay / MetaMask Card / COCA / Bleap / Crypto.com / best-alternatives)",
             "Channel": "Content Brief Factory → PR Generator", "Notes": "Must ship by end of Wk 1"},
            {"Week": "Wk 1", "Content": "Category hub page: Self-custody crypto cards in 2026",
             "Channel": "PR Generator", "Notes": "Links to all 6"},
            {"Week": "Wk 1", "Content": "Founder X: pinned thread 'Why we built the card inside the wallet'",
             "Channel": "Founder X", "Notes": "Anchor for sprint"},
            {"Week": "Wk 2", "Content": "Publish all 6 comparison pages + hub, GEO-optimize",
             "Channel": "Blog + GEO Tracker", "Notes": "Live before paid goes on"},
            {"Week": "Wk 2", "Content": "Launch crypto-native paid ads (Coinzilla + Bitmedia) to comparison pages",
             "Channel": "Crypto ad networks", "Notes": "Google Ads blocked (no license); retargeting + native only"},
            {"Week": "Wk 2", "Content": "2 PR placements commissioned (DR50+)",
             "Channel": "Outlet Matching", "Notes": "7–10 day lead time — start Wk 1"},
            {"Week": "Wk 2", "Content": "Reddit/Quora: 8–10 natural comments on competitor threads",
             "Channel": "Distribution tab", "Notes": "Claude-drafted, manual post"},
            {"Week": "Wk 2", "Content": "Micro-KOL #1 brief + contract (sponsored thread)",
             "Channel": "X", "Notes": "Post lands Wk 3"},
            {"Week": "Wk 3", "Content": "PR placement #1 goes live",
             "Channel": "Collaborator outlet", "Notes": "Backlink to hub page"},
            {"Week": "Wk 3", "Content": "Micro-KOL #1 post lives; founder quote-RTs",
             "Channel": "X", "Notes": "Amplify"},
            {"Week": "Wk 3", "Content": "Founder X: comparison-table thread + poll",
             "Channel": "X", "Notes": "Engagement bait"},
            {"Week": "Wk 3", "Content": "Reddit/Quora: 8–10 more comments",
             "Channel": "Distribution tab", "Notes": "Refresh based on new threads"},
            {"Week": "Wk 4", "Content": "PR placement #2 + Micro-KOL #2 (YouTube review)",
             "Channel": "Collaborator + YouTube", "Notes": ""},
            {"Week": "Wk 4", "Content": "GEO Tracker check: are pages being cited by Perplexity/ChatGPT?",
             "Channel": "GEO Tracker", "Notes": "Mid-sprint read"},
            {"Week": "Wk 4", "Content": "Retargeting burst on comparison-page visitors",
             "Channel": "Coinzilla / Bitmedia retargeting", "Notes": "Only if budget left; crypto-native only"},
            {"Week": "Wk 4", "Content": "Monthly Eval: measure vs. targets, decide what scales",
             "Channel": "Monthly Eval tab", "Notes": "Sprint retro"},
        ])
        st.dataframe(cal, use_container_width=True, hide_index=True)

    # ── 6. Assets ───────────────────────────────────────────────────────────
    with tab_assets:
        st.subheader("Content Assets Needed")
        col_must, col_nice = st.columns(2)
        with col_must:
            st.markdown("**Must-have**")
            st.markdown("""
- 6 comparison landing pages (Gnosis Pay / MetaMask Card / COCA / Bleap / Crypto.com / alternatives-category)
- 1 hub page (Self-custody crypto cards in 2026)
- 1 pinned founder X thread (hero)
- 2 PR article drafts (GEO-optimized via PR Generator)
- Google Ads copy: 3 ad groups, 4 headlines / 2 descriptions each
- 15–25 Reddit/Quora comment drafts (via Distribution tab)
- 1 FAQ/schema block reusable across all comparison pages
- Updated `llms.txt` and JSON-LD product schema
""")
        with col_nice:
            st.markdown("**Nice-to-have**")
            st.markdown("""
- 1 comparison-table infographic (reusable on X, Reddit, blog)
- 1 KOL YouTube review (Wk 4)
- 1 short-form video cut of the founder thread for X/TikTok
""")

    # ── 7. Metrics ──────────────────────────────────────────────────────────
    with tab_metrics:
        st.subheader("Success Metrics")
        st.markdown("**Primary KPI:** 1,500 installs / 400 card applications from campaign-attributed traffic in 4 weeks.")
        kpis = pd.DataFrame([
            {"Metric": "Comparison-page organic sessions", "Target": "3,000+ in Wk 4", "Tracked via": "GA4 / GSC"},
            {"Metric": "Keyword rankings (6 target terms)", "Target": "Top-20 by end of sprint, top-10 by Day 60", "Tracked via": "GSC + Keyword Intel"},
            {"Metric": "LLM citations (Perplexity/ChatGPT)", "Target": "≥3 brand mentions for 'best self-custody crypto card'", "Tracked via": "GEO Tracker"},
            {"Metric": "Crypto-native ad CPA (Coinzilla/Bitmedia)", "Target": "<$20 per install", "Tracked via": "Network dashboards + UTM to GA4"},
            {"Metric": "Reddit/Quora comment upvote ratio", "Target": "≥70% positive, ≥3 direct clicks per comment", "Tracked via": "Manual log"},
            {"Metric": "Founder X impressions", "Target": "500K cumulative across sprint", "Tracked via": "X analytics"},
            {"Metric": "PR referral traffic", "Target": "500+ sessions per placement", "Tracked via": "GA4"},
        ])
        st.dataframe(kpis, use_container_width=True, hide_index=True)
        st.caption("Reporting cadence: Weekly dashboard via Monthly Eval tab; end-of-sprint full retro.")

    # ── 8. Budget ───────────────────────────────────────────────────────────
    with tab_budget:
        st.subheader("Budget Allocation ($10K midpoint)")
        budget = pd.DataFrame([
            {"Bucket": "PR placements (tier-2 crypto + Collaborator + 1 wire)", "Amount": "$4,000", "%": "40%"},
            {"Bucket": "Crypto-native ad networks (Coinzilla + Bitmedia + Cointraffic + A-ADS)", "Amount": "$2,500", "%": "25%"},
            {"Bucket": "Newsletter sponsorship (The Defiant or 2× smaller)", "Amount": "$1,500", "%": "15%"},
            {"Bucket": "Micro-KOL seeds (2–3 direct-deal)", "Amount": "$1,500", "%": "15%"},
            {"Bucket": "Telegram channel sponsorships (2–3 direct posts)", "Amount": "$500", "%": "5%"},
            {"Bucket": "Contingency (reserved)", "Amount": "+$1,000", "%": "—"},
        ])
        st.dataframe(budget, use_container_width=True, hide_index=True)
        st.warning(
            "**Flex rule:** if a channel isn't hitting targets by Wk 2, "
            "reallocate to the top performer — don't dilute."
        )
        st.error(
            "**Why no Google/Meta/LinkedIn/TikTok Ads in this budget:** "
            "these platforms reject DeFi wallet advertising without a "
            "financial-services license in each target market. Nonbank "
            "doesn't hold those licenses, so these channels are "
            "**structurally excluded** — the budget that would normally "
            "go there is reallocated to crypto-native networks (Coinzilla "
            "et al.), direct-buy newsletters, KOLs, and PR."
        )

    # ── 9. Risks ────────────────────────────────────────────────────────────
    with tab_risks:
        st.subheader("Risks and Mitigations")
        risks = pd.DataFrame([
            {"Risk": "Comparison pages don't rank in 4 weeks (SEO lag)",
             "Mitigation": "Crypto-native paid networks + Reddit/X organic carry traffic until organic kicks in; value compounds past sprint."},
            {"Risk": "Mainstream ad platforms (Google/Meta/LinkedIn) block DeFi wallet ads",
             "Mitigation": "Structurally excluded from the plan. Budget reallocated to crypto-native networks (Coinzilla, Bitmedia) + direct-buy newsletters + KOLs + PR. Reach mainstream search via SEO, not ads."},
            {"Risk": "X/Reddit Ads reject Nonbank at review",
             "Mitigation": "Treat both as conditional (<$1K test). If rejected, reallocate to Coinzilla + Bitmedia on Day 1 of Wk 2."},
            {"Risk": "PR placements slip past Wk 4",
             "Mitigation": "Lock 2 outlets in Wk 1 with firm deadlines; keep backup outlet from Collaborator list."},
            {"Risk": "Reddit comments flagged as shilling",
             "Mitigation": "Distribution tab Claude prompts are tuned for value-first; rule: don't mention Nonbank until comment 2 in a thread."},
            {"Risk": "Micro-KOL post underperforms",
             "Mitigation": "Budget capped at 20% — worst case is a cheap signal, not a hole."},
            {"Risk": "Attribution is muddy (cross-channel)",
             "Mitigation": "UTM per channel + unique landing-page slugs per source; accept some ambient lift."},
        ])
        st.dataframe(risks, use_container_width=True, hide_index=True)

    # ── 10. Next Steps ──────────────────────────────────────────────────────
    with tab_next:
        st.subheader("Next Steps")
        st.markdown("""
**This week:**
1. Run Keyword Intel + GEO Tracker baseline on the 6 competitor terms (Day 1).
2. Generate 6 comparison-page briefs via Content Brief Factory (Day 1–2).
3. Draft + publish pages through PR Generator (Day 2–5).
4. Kick off 2 PR outlet outreaches via Outlet Matching (Day 2).
5. Founder writes + pins hero X thread (Day 3).

**Approvals needed:**
- Budget sign-off ($10K midpoint)
- Founder commitment to ~30 min/day on X for 4 weeks
- Legal/compliance review on competitor-name usage in comparison pages

**Decision points:**
- End of Wk 2: are pages indexed and ads converting? If no, rebalance.
- End of Wk 4: which channel had lowest CPA? That's the Month 2 anchor — then layer in real KOL.
""")
