"""
pages/competitor_intel.py -- Competitor Intel page
===================================================
Feature comparison matrix, competitor keyword spy, AI visibility audit,
and gap analysis for Nonbank vs competitors.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st
import requests

from config import COMPETITORS, FEATURE_DIMENSIONS, PRODUCT_PROFILE
from perplexity_geo import query_perplexity


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_matrix_df() -> pd.DataFrame:
    """Build a DataFrame: rows = competitors, columns = feature dimensions."""
    rows = []
    for c in COMPETITORS:
        row = {"Competitor": c["name"]}
        for dim in FEATURE_DIMENSIONS:
            row[dim] = c.get(dim, "")
        rows.append(row)
    return pd.DataFrame(rows)


def _is_positive(val: str) -> bool:
    """Heuristic: does this cell value indicate the feature is present?"""
    v = str(val).strip().lower()
    if not v or v in ("no", "n/a", "none", "—", "-"):
        return False
    if v.startswith("no ") or v.startswith("no—") or v.startswith("no —"):
        return False
    return True


def _nonbank_row(df: pd.DataFrame) -> pd.Series:
    return df[df["Competitor"] == "Nonbank"].iloc[0]


# ---------------------------------------------------------------------------
# Tab 1: Feature Comparison Matrix
# ---------------------------------------------------------------------------

def _tab_feature_matrix():
    st.subheader("Feature Comparison Matrix")
    st.caption(
        "Edit cells directly. Green-highlighted values indicate Nonbank "
        "advantages (feature present when most competitors lack it)."
    )

    key = "comp_matrix_df"
    if key not in st.session_state:
        st.session_state[key] = _build_matrix_df()

    edited = st.data_editor(
        st.session_state[key],
        use_container_width=True,
        num_rows="fixed",
        key="matrix_editor",
    )
    st.session_state[key] = edited

    # --- Gap summary ---
    st.markdown("---")
    st.subheader("Gap Summary")

    nb = edited[edited["Competitor"] == "Nonbank"].iloc[0]
    others = edited[edited["Competitor"] != "Nonbank"]

    bullets: list[str] = []
    for dim in FEATURE_DIMENSIONS:
        nb_has = _is_positive(nb[dim])
        others_have = [_is_positive(row[dim]) for _, row in others.iterrows()]
        count_others = sum(others_have)

        if nb_has and count_others == 0:
            bullets.append(
                f"Nonbank is the ONLY competitor with **{dim}**"
            )
        elif nb_has and count_others <= 1:
            who = [
                row["Competitor"]
                for _, row in others.iterrows()
                if _is_positive(row[dim])
            ]
            bullets.append(
                f"Nonbank + {who[0]} lead on **{dim}** (others lack it)"
                if who
                else f"Nonbank leads on **{dim}**"
            )

    if bullets:
        for b in bullets:
            st.markdown(f"- {b}")
    else:
        st.info("No clear Nonbank-only advantages detected in current data.")


# ---------------------------------------------------------------------------
# Tab 2: Competitor Keyword Spy
# ---------------------------------------------------------------------------

def _tab_keyword_spy():
    st.subheader("Competitor Keyword Spy")
    st.caption(
        "Search SerpAPI for competitor domain visibility. "
        "Results are for research only and are not saved."
    )

    serpapi_key = st.session_state.get("serpapi_key", "")
    if not serpapi_key:
        st.warning("Set your SerpAPI key in the sidebar (Settings) to enable this tool.")

    domains = [c["domain"] for c in COMPETITORS if not c.get("is_self")]
    queries = [
        "crypto card",
        "non-custodial crypto card",
        "gasless crypto wallet",
        "self-custody visa card",
    ]

    with st.expander("Customize queries", expanded=False):
        custom_q = st.text_area(
            "Queries (one per line)",
            value="\n".join(queries),
            height=120,
        )
        queries = [q.strip() for q in custom_q.strip().splitlines() if q.strip()]

    if st.button("Run keyword spy", disabled=not serpapi_key):
        results = []
        progress = st.progress(0)
        total = len(domains) * len(queries)
        step = 0

        for domain in domains:
            for q in queries:
                step += 1
                progress.progress(step / total)
                search_q = f"site:{domain} {q}"
                try:
                    resp = requests.get(
                        "https://serpapi.com/search.json",
                        params={
                            "q": search_q,
                            "api_key": serpapi_key,
                            "num": 5,
                        },
                        timeout=15,
                    )
                    data = resp.json()
                    organic = data.get("organic_results", [])
                    for r in organic[:3]:
                        results.append({
                            "Domain": domain,
                            "Query": q,
                            "Title": r.get("title", ""),
                            "Link": r.get("link", ""),
                            "Position": r.get("position", ""),
                        })
                    if not organic:
                        results.append({
                            "Domain": domain,
                            "Query": q,
                            "Title": "(no results)",
                            "Link": "",
                            "Position": "",
                        })
                except Exception as exc:
                    results.append({
                        "Domain": domain,
                        "Query": q,
                        "Title": f"Error: {exc}",
                        "Link": "",
                        "Position": "",
                    })

        progress.empty()
        if results:
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.info("No results returned.")


# ---------------------------------------------------------------------------
# Tab 3: AI Visibility Audit
# ---------------------------------------------------------------------------

_DEFAULT_PROMPTS = [
    "best non-custodial crypto card 2026",
    "gnosis pay vs alternatives",
    "gasless crypto wallet",
    "self-custody visa card comparison",
    "crypto card without gas fees",
]


def _tab_ai_audit():
    st.subheader("AI Visibility Audit")
    st.caption(
        "Query Perplexity AI with crypto-card prompts and check which "
        "competitors get mentioned in the responses."
    )

    pplx_key = st.session_state.get("perplexity_key", "")
    if not pplx_key:
        st.warning("Set your Perplexity API key in the sidebar (Settings) to enable this tool.")

    with st.expander("Customize prompts", expanded=False):
        custom_p = st.text_area(
            "Prompts (one per line)",
            value="\n".join(_DEFAULT_PROMPTS),
            height=120,
        )
        prompts = [p.strip() for p in custom_p.strip().splitlines() if p.strip()]

    competitor_names = [c["name"] for c in COMPETITORS]

    if st.button("Run AI audit", disabled=not pplx_key):
        matrix_rows: list[dict] = []
        progress = st.progress(0)

        for i, prompt in enumerate(prompts):
            progress.progress((i + 1) / len(prompts))
            try:
                answer = query_perplexity(api_key=pplx_key, prompt=prompt)
            except Exception as exc:
                st.error(f"Error querying '{prompt}': {exc}")
                continue

            answer_lower = answer.lower()
            row: dict = {"Prompt": prompt}
            for name in competitor_names:
                mentioned = name.lower() in answer_lower
                row[name] = "Mentioned" if mentioned else "--"
            matrix_rows.append(row)

        progress.empty()

        if matrix_rows:
            result_df = pd.DataFrame(matrix_rows)
            st.dataframe(
                result_df.style.applymap(
                    lambda v: "background-color: #d4edda" if v == "Mentioned" else "",
                    subset=competitor_names,
                ),
                use_container_width=True,
            )

            # Quick stats
            mentioned_counts = {
                name: sum(1 for r in matrix_rows if r[name] == "Mentioned")
                for name in competitor_names
            }
            cols = st.columns(len(competitor_names))
            for col, name in zip(cols, competitor_names):
                col.metric(name, f"{mentioned_counts[name]}/{len(prompts)}")
        else:
            st.info("No results returned.")


# ---------------------------------------------------------------------------
# Tab 4: Gap Analysis
# ---------------------------------------------------------------------------

def _tab_gap_analysis():
    st.subheader("Gap Analysis")
    st.caption(
        "Auto-generated from the Feature Comparison Matrix. "
        "Export as markdown for content briefs."
    )

    key = "comp_matrix_df"
    if key not in st.session_state:
        st.session_state[key] = _build_matrix_df()

    df = st.session_state[key]
    nb = df[df["Competitor"] == "Nonbank"].iloc[0]
    others = df[df["Competitor"] != "Nonbank"]

    wins: list[str] = []
    parity: list[str] = []
    losses: list[str] = []

    for dim in FEATURE_DIMENSIONS:
        nb_has = _is_positive(nb[dim])
        others_status = {
            row["Competitor"]: _is_positive(row[dim])
            for _, row in others.iterrows()
        }
        count_others = sum(others_status.values())

        if nb_has and count_others == 0:
            wins.append(f"**{dim}**: {nb[dim]}")
        elif not nb_has and count_others > 0:
            who = [k for k, v in others_status.items() if v]
            losses.append(f"**{dim}**: offered by {', '.join(who)}")
        else:
            parity.append(f"**{dim}**: Nonbank = {nb[dim]}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Wins", len(wins))
    col2.metric("Parity", len(parity))
    col3.metric("Gaps", len(losses))

    st.markdown("### Nonbank Wins")
    if wins:
        for w in wins:
            st.markdown(f"- {w}")
    else:
        st.info("No exclusive wins detected.")

    st.markdown("### Parity")
    if parity:
        for p in parity:
            st.markdown(f"- {p}")
    else:
        st.info("No parity features.")

    st.markdown("### Gaps (Competitors Lead)")
    if losses:
        for lo in losses:
            st.markdown(f"- {lo}")
    else:
        st.success("No gaps -- Nonbank covers all features.")

    # --- Markdown export ---
    st.markdown("---")
    md_lines = ["# Nonbank Competitor Gap Analysis\n"]
    md_lines.append("## Wins (Nonbank Only)")
    for w in wins:
        md_lines.append(f"- {w}")
    md_lines.append("\n## Parity")
    for p in parity:
        md_lines.append(f"- {p}")
    md_lines.append("\n## Gaps")
    for lo in losses:
        md_lines.append(f"- {lo}")

    md_text = "\n".join(md_lines)
    st.download_button(
        "Export as Markdown",
        data=md_text,
        file_name="nonbank_gap_analysis.md",
        mime="text/markdown",
    )


# ---------------------------------------------------------------------------
# Main page entry point
# ---------------------------------------------------------------------------

def page_competitor_intel():
    st.title("Competitor Intel")
    st.markdown(
        f"Competitive intelligence for **{PRODUCT_PROFILE['name']}** "
        f"({PRODUCT_PROFILE['domain']}) vs key rivals."
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Feature Matrix",
        "Keyword Spy",
        "AI Visibility Audit",
        "Gap Analysis",
    ])

    with tab1:
        _tab_feature_matrix()
    with tab2:
        _tab_keyword_spy()
    with tab3:
        _tab_ai_audit()
    with tab4:
        _tab_gap_analysis()
