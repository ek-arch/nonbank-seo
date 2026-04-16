"""Page 2 — Nonbank Metrics: platform stats, P&L, country breakdown.

Starter state: no legacy data. Tables render gracefully empty and are
populated as real cohort data becomes available.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
import altair as alt
from data_sources import DATA


def page_nonbank_metrics():
    st.title("📈 Stage 2 · Nonbank Metrics")
    st.caption("Language & country analysis for SEO/GEO targeting")

    langs = pd.DataFrame(DATA.get("languages", []))
    countries = pd.DataFrame(DATA.get("countries", []))

    if langs.empty and countries.empty:
        st.info(
            "No cohort data yet — Nonbank starts from scratch. "
            "Populate `DATA['languages']` and `DATA['countries']` in `data_sources.py` "
            "as card spend, registrations, and LTV become measurable, then this page will "
            "chart language/country ROI for SEO targeting."
        )
        st.subheader("Expected schema")
        st.code(
            'DATA["languages"] = [\n'
            '  {"lang": "English", "code": "en", "card_users": N, "total_spend": $, "spend_per_user": $},\n'
            '  ...\n'
            ']\n\n'
            'DATA["countries"] = [\n'
            '  {"country": "USA", "flag": "🇺🇸", "tier": 1, "card_users": N,\n'
            '   "card_spend": $, "revenue": $, "spend_per_user": $, "conversion": 0.0-1.0},\n'
            '  ...\n'
            ']',
            language="python",
        )
        return

    # ── Language Clusters ──────────────────────────────────────────
    if not langs.empty:
        st.header("Language Cluster Analysis")
        lang_chart = alt.Chart(langs).mark_bar().encode(
            x=alt.X("spend_per_user:Q", title="Spend per User (USD)"),
            y=alt.Y("lang:N", sort="-x", title="Language"),
            color=alt.value("#2196F3"),
            tooltip=["lang", alt.Tooltip("spend_per_user:Q", format="$,.0f"),
                     "card_users", alt.Tooltip("total_spend:Q", format="$,.0f")],
        ).properties(height=280)
        st.altair_chart(lang_chart, use_container_width=True)

    # ── Country Table ──────────────────────────────────────────────
    if not countries.empty:
        st.header(f"Country Performance ({len(countries)} Active Markets)")
        tier_options = sorted({str(t) for t in countries["tier"].tolist() if t is not None})
        tier_filter = st.multiselect(
            "Filter by tier", options=tier_options, default=tier_options,
            format_func=lambda x: {"1": "Tier 1 (>$400K)", "2": "Tier 2 ($100K–$400K)",
                                    "3": "Tier 3 ($30K–$100K)"}.get(x, x),
        )
        filtered = countries[countries["tier"].astype(str).isin(tier_filter)].copy()
        filtered = filtered.fillna(0)
        filtered["spend_fmt"] = filtered["card_spend"].apply(lambda x: f"${x/1e3:.0f}K" if x else "$0")
        filtered["spu_fmt"]   = filtered["spend_per_user"].apply(lambda x: f"${int(x):,}" if x else "$0")
        filtered["conv_fmt"]  = filtered["conversion"].apply(lambda x: f"{x*100:.0f}%" if x else "0%")

        def highlight_row(row):
            try:
                conv = float(str(row.get("Conv.", "0")).replace("%", ""))
                if conv >= 80:
                    return ["background-color: #d4edda"] * len(row)
            except (ValueError, TypeError):
                pass
            return [""] * len(row)

        st.dataframe(
            filtered[["flag", "country", "card_users", "spend_fmt", "spu_fmt", "conv_fmt", "tier"]]
            .rename(columns={"flag": "", "country": "Country", "card_users": "Users", "spend_fmt": "Spend",
                             "spu_fmt": "$/User", "conv_fmt": "Conv.", "tier": "Tier"})
            .style.apply(highlight_row, axis=1),
            use_container_width=True, hide_index=True,
        )
        st.caption("🟢 = ≥80% conversion")
