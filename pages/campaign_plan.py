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
        tab_calendar, tab_assets, tab_metrics, tab_budget, tab_risks, tab_next = st.tabs([
            "Overview", "Audience", "Messages", "Channels", "Media & Outlets",
            "Calendar", "Assets", "Metrics", "Budget", "Risks", "Next Steps",
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
        channels = pd.DataFrame([
            {"Channel": "Comparison SEO pages (Content Brief Factory)",
             "Why it fits": "Competitor-intent searchers self-qualify; compounds past sprint.",
             "Format": "6 comparison pages + 1 category hub",
             "Effort": "High (Wk 1–2)", "Budget": "~$1.5K (production)"},
            {"Channel": "Founder/CEO X",
             "Why it fits": "Free, fastest trust signal, best for competitor call-outs.",
             "Format": "3×/week threads + daily replies in competitor mentions",
             "Effort": "Medium, daily", "Budget": "$0"},
            {"Channel": "Reddit/Quora distribution",
             "Why it fits": "Where comparison-shoppers actually ask. Fuels LLM citations.",
             "Format": "15–25 natural comments via Distribution tab",
             "Effort": "Medium", "Budget": "$0"},
            {"Channel": "PR on Collaborator outlets",
             "Why it fits": "Backlinks + GEO citations; mid-tier DR outlets rank fast.",
             "Format": "2 placements on hybrid wallet+card angle",
             "Effort": "Medium", "Budget": "~$3–5K"},
            {"Channel": "Competitor-intent Google Ads",
             "Why it fits": "High intent, clean attribution, kills where SEO hasn't landed.",
             "Format": "Bid on 'gnosis pay alternative', 'metamask card review', etc.",
             "Effort": "Low-medium", "Budget": "~$2.5–4K"},
            {"Channel": "Micro-KOL seeds",
             "Why it fits": "2–3 micro voices (5–20K followers) testing messaging — NOT hero.",
             "Format": "Sponsored thread + 1 YouTube review",
             "Effort": "Low", "Budget": "~$1.5–3K"},
            {"Channel": "GEO optimization pass",
             "Why it fits": "Ensure Perplexity/ChatGPT cite the new comparison pages.",
             "Format": "llms.txt + schema + FAQ blocks on each page",
             "Effort": "Low (Wk 2)", "Budget": "$0 (in-house)"},
        ])
        st.dataframe(channels, use_container_width=True, hide_index=True)

    # ── 4b. Media & Outlets ─────────────────────────────────────────────────
    with tab_outlets:
        st.subheader("Media & Outlets — Full Traffic Stack")
        st.markdown(
            "Concrete platforms ranked by **fit × cost × speed** for this "
            "sprint. Priority: **P0 = book now**, **P1 = secondary**, "
            "**P2 = Month 2+ / awareness-only**. Costs are 2026 ballpark "
            "ranges — confirm with outlet reps before booking."
        )

        sub_pr, sub_adnet, sub_listing, sub_review, sub_news, sub_pod, sub_community = st.tabs([
            "PR / Guest Posts", "Ad Networks", "Listings & Aggregators",
            "Review / Comparison", "Newsletters", "Podcasts", "Community",
        ])

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
                "Collaborator.pro DR50+ mid-tier. Total ≈ $4–6K, 5–6 placements, "
                "strong backlink + GEO footprint."
            )

        # ── Sub-tab: Ad Networks ───────────────────────────────────────────
        with sub_adnet:
            st.markdown(
                "**Crypto-native display / native-ad networks.** Cheap CPMs, "
                "reach crypto audiences that mainstream networks block. Use "
                "for retargeting comparison-page visitors."
            )
            ad_nets = pd.DataFrame([
                {"Platform": "Coinzilla", "Format": "Display, native, push",
                 "Reach": "1B+ crypto impressions/mo", "Min. budget": "$500",
                 "Typical CPM": "$1.50–4", "Fit": "Retargeting + awareness", "Priority": "P0"},
                {"Platform": "Bitmedia", "Format": "Display, native",
                 "Reach": "600M+ crypto impressions/mo", "Min. budget": "$100",
                 "Typical CPM": "$1–3", "Fit": "Retargeting", "Priority": "P0"},
                {"Platform": "Cointraffic", "Format": "Display, native, pop",
                 "Reach": "Premium crypto pubs", "Min. budget": "$500",
                 "Typical CPM": "$2–5", "Fit": "Premium awareness", "Priority": "P1"},
                {"Platform": "A-ADS", "Format": "Display (anonymous, BTC-paid)",
                 "Reach": "Niche crypto forums", "Min. budget": "$10",
                 "Typical CPM": "$0.50–2", "Fit": "Cheap long-tail testing", "Priority": "P1"},
                {"Platform": "Adshares", "Format": "Programmatic (web3)",
                 "Reach": "Web3 dapp ad slots", "Min. budget": "$100",
                 "Typical CPM": "$1–3", "Fit": "DeFi-native placements", "Priority": "P1"},
                {"Platform": "Dao.Ad", "Format": "Native crypto ads",
                 "Reach": "Mid-tier crypto sites", "Min. budget": "$200",
                 "Typical CPM": "$1–3", "Fit": "Backup / scale-up", "Priority": "P2"},
                {"Platform": "Google Ads (competitor-intent)", "Format": "Search",
                 "Reach": "High-intent searchers", "Min. budget": "Open",
                 "Typical CPM": "CPC $1.50–4", "Fit": "**Primary paid channel** — conquest keywords", "Priority": "P0"},
                {"Platform": "X/Twitter Ads", "Format": "Promoted posts",
                 "Reach": "Crypto Twitter", "Min. budget": "$50/day",
                 "Typical CPM": "$6–12", "Fit": "Amplify founder threads", "Priority": "P1"},
                {"Platform": "Reddit Ads", "Format": "Promoted post, sub-targeted",
                 "Reach": "r/CryptoCurrency, r/defi, r/ethfinance", "Min. budget": "$5/day",
                 "Typical CPM": "$3–8", "Fit": "Sub-targeted conquest", "Priority": "P1"},
                {"Platform": "YouTube Ads (pre-roll)", "Format": "Video",
                 "Reach": "Crypto review channels", "Min. budget": "Open",
                 "Typical CPM": "$10–25", "Fit": "Awareness (Month 2+)", "Priority": "P2"},
            ])
            st.dataframe(ad_nets, use_container_width=True, hide_index=True)
            st.info(
                "**Sprint pick:** Google Ads competitor-intent ($2.5–3K) **+** "
                "Coinzilla retargeting ($500–800) **+** Reddit Ads sub-targeted "
                "test ($300–500). Skip YouTube / X Ads for the 4-week sprint."
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
            {"Bucket": "PR placements", "Picks": "CryptoSlate + BeInCrypto + 1 Chainwire + 2× Collaborator DR50+",
             "Amount": "$4,000", "Why": "Backlinks, GEO citations, mid-tier DR coverage"},
            {"Bucket": "Paid search + crypto display", "Picks": "Google Ads (conquest) + Coinzilla retarget + Reddit Ads test",
             "Amount": "$3,500", "Why": "High-intent capture + retargeting of comparison-page visitors"},
            {"Bucket": "Micro-KOL seeds", "Picks": "2× Twitter micro + 1× small YouTuber review",
             "Amount": "$2,000", "Why": "Message testing, not brand-build"},
            {"Bucket": "Listings + community", "Picks": "Claim all P0 listings; Reddit/Quora/X effort",
             "Amount": "$0 (time only)", "Why": "Highest long-run ROI, but labor-heavy"},
            {"Bucket": "Production overflow", "Picks": "Design, comparison-table infographic, landing-page polish",
             "Amount": "$500", "Why": "Ensure shippable quality"},
        ])
        st.dataframe(alloc, use_container_width=True, hide_index=True)
        st.caption(
            "Total: $10,000 ± contingency. If budget stretches to $15K: add "
            "The Defiant newsletter slot (~$3K) **and** CryptoPotato or "
            "CryptoBriefing as a second PR. If compressed to $5K: drop KOL "
            "to 1× micro, cut to Coinzilla-only on display, keep PR + "
            "Google Ads as-is."
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
            {"Week": "Wk 2", "Content": "Launch competitor-intent Google Ads pointing to comparison pages",
             "Channel": "Paid search", "Notes": "Depends on pages being live"},
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
            {"Week": "Wk 4", "Content": "Retargeting ads on comparison-page visitors",
             "Channel": "Paid social / display", "Notes": "Only if budget left"},
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
            {"Metric": "Paid search CPA", "Target": "<$15 per install", "Tracked via": "Google Ads"},
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
            {"Bucket": "Competitor-intent Google Ads", "Amount": "$3,000", "%": "30%"},
            {"Bucket": "PR placements (2× DR50+)", "Amount": "$4,000", "%": "40%"},
            {"Bucket": "Micro-KOL seeds (2–3)", "Amount": "$2,000", "%": "20%"},
            {"Bucket": "Production overflow (design, video cuts)", "Amount": "$1,000", "%": "10%"},
            {"Bucket": "Contingency (reserved)", "Amount": "+$1,000", "%": "—"},
        ])
        st.dataframe(budget, use_container_width=True, hide_index=True)
        st.warning(
            "**Flex rule:** if a channel isn't hitting targets by Wk 2, "
            "reallocate to the top performer — don't dilute."
        )

    # ── 9. Risks ────────────────────────────────────────────────────────────
    with tab_risks:
        st.subheader("Risks and Mitigations")
        risks = pd.DataFrame([
            {"Risk": "Comparison pages don't rank in 4 weeks (SEO lag)",
             "Mitigation": "Paid search + Reddit carry traffic until organic kicks in; value compounds past sprint."},
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
