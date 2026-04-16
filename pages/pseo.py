"""
pages/pseo.py — Comparison Page Factory
========================================
Replaces Kolo's country × crypto × use-case programmatic SEO with a
tool that actually fits Nonbank's research-first strategy:

Generate "Nonbank vs [competitor]" and "[competitor] alternative"
comparison page briefs at scale. Uses the COMPETITOR_BRANDS feature
matrix from config.py so every page is grounded in real differences.

Why this, not the old pseo:
- Research showed "gnosis pay alternative" and similar comparison queries
  have moderate competition with a real entry point for Nonbank
- Comparison pages are high-intent (transactional SEO)
- Leverages existing competitor matrix data — no new content invention needed
- Scales to 10-20 pages from one click
"""
from __future__ import annotations

import json
import os
from datetime import date
import streamlit as st
import pandas as pd

from config import COMPETITORS, FEATURE_DIMENSIONS, CONTENT_PILLARS, PRODUCT_PROFILE


# ── Brief templates ────────────────────────────────────────────────────────

ANGLE_TEMPLATES = {
    "versus": {
        "label": "Head-to-head (Nonbank vs X)",
        "title_tmpl": "Nonbank vs {competitor}: {year} Comparison",
        "kw_tmpl":    "nonbank vs {comp_slug}",
        "intent":     "Comparison / transactional",
        "outline": [
            "Quick verdict (who wins for whom)",
            "Feature comparison table (custody, card, fees, chains, AML, regions)",
            "Where Nonbank wins: {wins_list}",
            "Where {competitor} wins: {losses_list}",
            "Pricing breakdown",
            "Which one to choose — user scenarios",
            "FAQ (5–7 Qs)",
        ],
    },
    "alternative": {
        "label": "Alternative to X",
        "title_tmpl": "{competitor} Alternative: Why Nonbank Fits Better",
        "kw_tmpl":    "{comp_slug} alternative",
        "intent":     "Transactional / high-intent",
        "outline": [
            "Why people look for {competitor} alternatives",
            "Key problems with {competitor}: {competitor_gaps}",
            "How Nonbank solves them: {nonbank_advantages}",
            "Feature comparison snapshot",
            "When to stick with {competitor} (honest trade-offs)",
            "How to migrate from {competitor} to Nonbank",
            "FAQ",
        ],
    },
    "roundup": {
        "label": "Category roundup (Nonbank included)",
        "title_tmpl": "Best {category} in {year}: {competitor_list}",
        "kw_tmpl":    "best {category} {year}",
        "intent":     "Informational / comparison",
        "outline": [
            "What to look for in a {category}",
            "Top picks with pros/cons (Nonbank + 4-5 competitors)",
            "Side-by-side feature table",
            "Recommendation by use case",
            "FAQ",
        ],
    },
}

CATEGORY_LABELS = [
    "non-custodial crypto card",
    "DeFi wallet with Visa card",
    "hybrid DeFi+card crypto app",
    "crypto wallet with integrated card",
    "self-custody crypto card",
]


# ── Helpers ────────────────────────────────────────────────────────────────

def _slug(s: str) -> str:
    return s.lower().replace(" ", "-").replace(".", "").replace(",", "")


def _competitor_gaps_vs_nonbank(comp: dict, nonbank: dict) -> tuple[list[str], list[str]]:
    """Return (nonbank_wins, competitor_wins) — dimensions where each has advantage."""
    nonbank_wins = []
    comp_wins = []
    for dim in FEATURE_DIMENSIONS:
        nb_val = str(nonbank.get(dim, "")).lower()
        cp_val = str(comp.get(dim, "")).lower()
        # Simple heuristic: "yes" / "live" / "100+" vs "no" / "pilot" / "limited"
        nb_positive = any(x in nb_val for x in ["yes", "live", "100+", "multi", "global"])
        nb_negative = any(x in nb_val for x in ["no ", "no\"", "pilot", "limited", "planned"])
        cp_positive = any(x in cp_val for x in ["yes", "live", "100+", "multi", "global"])
        cp_negative = any(x in cp_val for x in ["no ", "no\"", "pilot", "limited", "planned"])
        if nb_positive and cp_negative:
            nonbank_wins.append(f"**{dim}**: {nonbank.get(dim)}")
        elif cp_positive and nb_negative:
            comp_wins.append(f"**{dim}**: {comp.get(dim)}")
    return nonbank_wins, comp_wins


def _build_brief(competitor: dict, angle: str, nonbank: dict, year: int = 2026) -> dict:
    """Assemble a single comparison brief dict."""
    tmpl = ANGLE_TEMPLATES[angle]
    comp_name = competitor["name"]
    comp_slug = _slug(comp_name)
    wins, losses = _competitor_gaps_vs_nonbank(competitor, nonbank)
    wins_list = ", ".join(w.split(":")[0].strip("*") for w in wins[:5]) or "(run analysis)"
    losses_list = ", ".join(l.split(":")[0].strip("*") for l in losses[:5]) or "(run analysis)"

    outline_filled = [
        o.format(
            competitor=comp_name,
            comp_slug=comp_slug,
            year=year,
            wins_list=wins_list,
            losses_list=losses_list,
            competitor_gaps=losses_list,
            nonbank_advantages=wins_list,
            category="non-custodial crypto card",
            competitor_list=f"Nonbank, {comp_name}, ...",
        )
        for o in tmpl["outline"]
    ]

    title = tmpl["title_tmpl"].format(
        competitor=comp_name,
        comp_slug=comp_slug,
        year=year,
        category="non-custodial crypto card",
        competitor_list="",
    )
    kw = tmpl["kw_tmpl"].format(
        competitor=comp_name, comp_slug=comp_slug, year=year,
        category="non-custodial crypto card",
    )

    return {
        "Competitor": comp_name,
        "Angle": tmpl["label"],
        "Title": title,
        "Primary Keyword": kw,
        "Slug": f"/compare/nonbank-vs-{comp_slug}" if angle == "versus" else f"/{comp_slug}-alternative",
        "Intent": tmpl["intent"],
        "Nonbank Wins": len(wins),
        "Competitor Wins": len(losses),
        "Outline": " · ".join(outline_filled),
        "Outline Full": outline_filled,
        "Wins Detail": wins,
        "Losses Detail": losses,
    }


# ── Main page ──────────────────────────────────────────────────────────────

def page_programmatic_seo():
    st.title("🚀 Comparison Page Factory")
    st.caption("Generate 'Nonbank vs X' and 'X alternative' briefs at scale from the competitor matrix")

    st.info(
        "**Research finding:** queries like 'gnosis pay alternative' and 'metamask card vs' "
        "have moderate competition with a real entry point. This tool auto-generates "
        "comparison article briefs for each competitor × angle, grounded in the feature "
        "matrix from Competitor Intel."
    )

    nonbank = next((c for c in COMPETITORS if c.get("is_self")), None)
    competitors = [c for c in COMPETITORS if not c.get("is_self")]

    if not nonbank:
        st.error("No self-marked competitor row in config.py COMPETITORS")
        return

    tab_generate, tab_preview, tab_export = st.tabs([
        "1️⃣ Generate Briefs", "2️⃣ Preview & Refine", "3️⃣ Export"
    ])

    # ── TAB 1 ────────────────────────────────────────────────────────────
    with tab_generate:
        st.subheader("Select Comparisons")

        col1, col2 = st.columns(2)
        with col1:
            selected_comps = st.multiselect(
                "Competitors", options=[c["name"] for c in competitors],
                default=[c["name"] for c in competitors[:4]],
                help="Each selected competitor produces 1 brief per angle below",
            )
        with col2:
            selected_angles = st.multiselect(
                "Angles", options=list(ANGLE_TEMPLATES.keys()),
                default=["versus", "alternative"],
                format_func=lambda a: ANGLE_TEMPLATES[a]["label"],
            )

        total_briefs = len(selected_comps) * len(selected_angles)
        st.caption(f"**{total_briefs}** briefs will be generated.")

        if st.button("🔧 Generate Briefs", type="primary", disabled=not (selected_comps and selected_angles)):
            briefs = []
            for comp_name in selected_comps:
                comp = next((c for c in competitors if c["name"] == comp_name), None)
                if not comp:
                    continue
                for angle in selected_angles:
                    briefs.append(_build_brief(comp, angle, nonbank))
            st.session_state["comp_briefs"] = briefs
            st.success(f"Generated {len(briefs)} briefs")

    # ── TAB 2 ────────────────────────────────────────────────────────────
    with tab_preview:
        briefs = st.session_state.get("comp_briefs", [])
        if not briefs:
            st.info("Generate briefs first in Tab 1.")
        else:
            st.subheader(f"{len(briefs)} Briefs")

            # Summary table
            summary_rows = [
                {
                    "Competitor": b["Competitor"],
                    "Angle": b["Angle"],
                    "Title": b["Title"],
                    "Keyword": b["Primary Keyword"],
                    "Intent": b["Intent"],
                    "NB Wins": b["Nonbank Wins"],
                    "Comp Wins": b["Competitor Wins"],
                }
                for b in briefs
            ]
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

            # Deep dive on selected brief
            st.subheader("Brief Detail")
            idx = st.selectbox(
                "Select brief",
                range(len(briefs)),
                format_func=lambda i: f"{briefs[i]['Competitor']} — {briefs[i]['Angle']}",
            )
            sel = briefs[idx]

            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"### {sel['Title']}")
                st.markdown(f"**Slug:** `{sel['Slug']}`  ·  **Keyword:** `{sel['Primary Keyword']}`")
                st.markdown(f"**Intent:** {sel['Intent']}")
                st.markdown("**Outline:**")
                for i, item in enumerate(sel["Outline Full"], 1):
                    st.markdown(f"{i}. {item}")
            with c2:
                st.markdown("**✅ Nonbank wins on:**")
                for w in sel["Wins Detail"]:
                    st.markdown(f"- {w}")
                st.markdown("**⚠️ Competitor wins on:**")
                for l in sel["Losses Detail"]:
                    st.markdown(f"- {l}")

            # Optional: full article generation via Claude
            st.divider()
            st.subheader("Expand to Full Article (optional)")
            api_key = st.session_state.get("anthropic_token")

            if not api_key:
                st.caption("Add Anthropic key in sidebar to enable full-article generation.")
            else:
                if st.button(f"✍️ Generate full article for: {sel['Title']}", type="primary"):
                    from llm_client import _call_with_retry, _client
                    system = (
                        f"You are a senior SEO/GEO content writer for Nonbank (nonbank.io) — "
                        f"{PRODUCT_PROFILE['description']}\n\n"
                        "Write a detailed comparison article. Include: FAQ section, comparison "
                        "table (markdown), 3-5 data-dense stat paragraphs AI engines can cite, "
                        "clear verdict, honest trade-offs. Target 1500-2000 words. Return "
                        "clean markdown only."
                    )
                    user_msg = (
                        f"Article brief:\n"
                        f"Title: {sel['Title']}\n"
                        f"Primary keyword: {sel['Primary Keyword']}\n"
                        f"Intent: {sel['Intent']}\n\n"
                        f"Outline:\n" + "\n".join(f"- {o}" for o in sel["Outline Full"]) + "\n\n"
                        f"Nonbank advantages to highlight:\n" +
                        "\n".join(f"- {w}" for w in sel["Wins Detail"]) + "\n\n"
                        f"{sel['Competitor']} advantages (be honest):\n" +
                        "\n".join(f"- {l}" for l in sel["Losses Detail"]) + "\n\n"
                        "Write the full article now."
                    )
                    try:
                        with st.spinner("Generating article..."):
                            resp = _call_with_retry(
                                _client(api_key),
                                model="claude-sonnet-4-6",
                                max_tokens=4000,
                                temperature=0.7,
                                system=system,
                                messages=[{"role": "user", "content": user_msg}],
                            )
                            article = resp.content[0].text
                            st.session_state[f"article_{idx}"] = article
                    except Exception as e:
                        st.error(f"Generation failed: {e}")

                article = st.session_state.get(f"article_{idx}")
                if article:
                    st.markdown("### Generated Article")
                    st.markdown(article)
                    st.download_button(
                        "⬇️ Download as Markdown",
                        article.encode("utf-8"),
                        file_name=f"{_slug(sel['Title'])}.md",
                        mime="text/markdown",
                    )

    # ── TAB 3 ────────────────────────────────────────────────────────────
    with tab_export:
        briefs = st.session_state.get("comp_briefs", [])
        if not briefs:
            st.info("Generate briefs first in Tab 1.")
        else:
            st.subheader("Export All Briefs")
            st.caption(f"{len(briefs)} briefs ready for export")

            # CSV export
            export_rows = [
                {
                    "Competitor": b["Competitor"],
                    "Angle": b["Angle"],
                    "Title": b["Title"],
                    "Slug": b["Slug"],
                    "Primary Keyword": b["Primary Keyword"],
                    "Intent": b["Intent"],
                    "Outline": b["Outline"],
                    "Nonbank Advantages": " | ".join(b["Wins Detail"]),
                    "Competitor Advantages": " | ".join(b["Losses Detail"]),
                }
                for b in briefs
            ]
            csv_data = pd.DataFrame(export_rows).to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download all briefs as CSV",
                csv_data,
                file_name=f"nonbank_comparison_briefs_{date.today().isoformat()}.csv",
                mime="text/csv",
            )

            # JSON export
            json_data = json.dumps(export_rows, indent=2).encode("utf-8")
            st.download_button(
                "⬇️ Download as JSON",
                json_data,
                file_name=f"nonbank_comparison_briefs_{date.today().isoformat()}.json",
                mime="application/json",
            )

            st.markdown("### Push to Content Plan")
            st.caption(
                "Add these briefs as tasks in the **Content Strategy** page. Each brief "
                "becomes a row in the publication calendar that you can assign to an outlet "
                "and week."
            )
            if st.button("➕ Add all briefs to Content Plan", type="primary"):
                current_plan = st.session_state.get("content_plan", [])
                for b in briefs:
                    current_plan.append({
                        "Task": b["Title"],
                        "Type": "SEO+GEO",
                        "Market": "🌍 Global",
                        "Outlet Options": "",
                        "Price": "",
                        "GEO": "Comparison table + FAQ + quotable stats",
                        "Week": "",
                        "Status": "To Do",
                        "Publication URL": "",
                        "Reddit/Quora URL": "",
                    })
                st.session_state["content_plan"] = current_plan
                st.success(f"Added {len(briefs)} briefs to Content Plan. Go to **Content Strategy → Publication Calendar** to review.")
