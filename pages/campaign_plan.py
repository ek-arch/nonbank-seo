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

    tab_overview, tab_audience, tab_messages, tab_channels, tab_calendar, \
        tab_assets, tab_metrics, tab_budget, tab_risks, tab_next = st.tabs([
            "Overview", "Audience", "Messages", "Channels",
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
