"""Page 0 — Dashboard: product profile, competitor snapshot, SEO status, and weekly actions."""
from __future__ import annotations

import streamlit as st
import pandas as pd

from config import PRODUCT_PROFILE, COMPETITORS


def page_dashboard():
    # ── Section 1: Product Profile Card ────────────────────────────
    st.title("🤖 Nonbank SEO & GEO Intelligence Agent")
    st.markdown(f"**{PRODUCT_PROFILE['domain']}** — {PRODUCT_PROFILE['tagline']}")
    st.caption(PRODUCT_PROFILE["description"])

    c1, c2, c3 = st.columns(3)
    diffs = {d["id"]: d for d in PRODUCT_PROFILE["differentiators"]}
    with c1:
        st.metric("Gasless Fees", "Yes")
        st.caption(diffs["gasless"]["description"])
    with c2:
        st.metric("Built-in AML", "Yes")
        st.caption(diffs["aml"]["description"])
    with c3:
        st.metric("DeFi + Card Hybrid", PRODUCT_PROFILE["card_name"])
        st.caption(diffs["hybrid_defi_card"]["description"])

    plat = PRODUCT_PROFILE["platforms"]
    st.markdown(
        f"**Platforms:** [iOS]({plat['ios']}) · [Android]({plat['android']}) "
        f"&nbsp;|&nbsp; **Card Status:** {PRODUCT_PROFILE['card_status']}"
    )

    st.divider()

    # ── Section 2: Competitor Snapshot ─────────────────────────────
    st.subheader("Competitor Snapshot")

    cols = [
        "Custody Model", "Card Network", "Gasless Fees",
        "Built-in AML", "Multi-Account (banks+exchanges+wallets)", "Key Regions",
    ]
    rows = []
    for comp in COMPETITORS:
        rows.append({"Name": comp["name"], **{c: comp.get(c, "—") for c in cols}})

    df = pd.DataFrame(rows).set_index("Name")
    df.columns = ["Custody", "Card", "Gasless", "AML", "Multi-Account", "Regions"]

    def highlight_nonbank(row):
        if row.name == "Nonbank":
            return ["background-color: #e8f5e9"] * len(row)
        return [""] * len(row)

    st.dataframe(df.style.apply(highlight_nonbank, axis=1), use_container_width=True)

    st.divider()

    # ── Section 3: SEO Status ─────────────────────────────────────
    st.subheader("SEO Status")

    seo = PRODUCT_PROFILE["seo_baseline"]
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Domain Rating", seo["domain_rating"] or "TBD")
    s2.metric("Organic Traffic", seo["organic_traffic"] or "TBD")
    s3.metric("Blog Posts", seo["blog_posts"])
    s4.metric("Backlinks", seo["backlinks"] or "TBD")

    st.info("Connect Ahrefs or Google Search Console to populate real data.")

    st.divider()

    # ── Section 4: Phased Weekly Actions ──────────────────────────
    st.subheader("Phased Weekly Actions")

    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.markdown("**Phase 1 — Research**")
            st.markdown(
                "- Competitor analysis (features, pricing, positioning)\n"
                "- Keyword gap analysis vs top 5 competitors\n"
                "- AI visibility audit (ChatGPT, Perplexity, Google AI)"
            )
        with st.container(border=True):
            st.markdown("**Phase 2 — Content**")
            st.markdown(
                "- Write comparison articles (Nonbank vs each competitor)\n"
                "- Publish via vetted outlets (DR 50+)\n"
                "- Translate pillar articles to ES, PT, TR"
            )

    with col_right:
        with st.container(border=True):
            st.markdown("**Phase 3 — Distribution**")
            st.markdown(
                "- Reddit threads: r/cryptocurrency, r/CryptoCards, r/defi\n"
                "- Quora answers on self-custody and gasless topics\n"
                "- Social comments on competitor posts"
            )
        with st.container(border=True):
            st.markdown("**Phase 4 — Measure**")
            st.markdown(
                "- Track AI mentions across ChatGPT, Perplexity, Gemini\n"
                "- Check keyword rankings weekly\n"
                "- Monthly ROI evaluation by channel (SEO vs GEO vs Social)"
            )

    st.divider()

    # ── Section 5: Quick Start ────────────────────────────────────
    st.subheader("Quick Start")
    st.markdown(
        "| Step | Tab | What to do |\n"
        "|---|---|---|\n"
        "| 1 | **Content Plan** | Draft briefs and pick target markets |\n"
        "| 2 | **Outlet Matching** | Select outlets by DR and price efficiency |\n"
        "| 3 | **Publication ROI** | Sanity-check expected ROI before buying |\n"
        "| 4 | **PR Generator** | Generate GEO-optimized article drafts |\n"
        "| 5 | **Distribution** | Find Reddit/Quora threads and draft replies |\n"
        "| 6 | **GEO Tracker** | Monitor Nonbank mentions in AI answers |\n"
        "| 7 | **Monthly Eval** | Log actuals and feed into next month's plan |"
    )
