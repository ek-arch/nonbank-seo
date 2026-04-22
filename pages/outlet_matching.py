"""Page — Outlet Matching: search Collaborator.pro catalog, score, shortlist, assign to pillars."""
from __future__ import annotations

import streamlit as st
import pandas as pd

from collaborator_outlets import (
    get_outlets, get_top_outlets_all_langs,
    LANG_LABELS, score_label, RAW_OUTLETS,
)
from config import CONTENT_PILLARS
from serpzilla_client import SerpzillaClient, SerpzillaError


def page_outlet_matching():
    st.title("🗞️ Outlet Matching")
    st.caption("Search → Score → Shortlist → Assign to content pillars")

    st.info(
        "**Research-first flow:** Run Keyword Intel and Competitor Intel first to identify "
        "which pillars to target. Then use this page to find outlets that match those pillars."
    )

    with st.expander("ℹ️ How outlet scoring works", expanded=False):
        st.markdown("""
**5-dimension scoring model (0–15 points, from Collaborator.pro catalog):**

| Dimension | 3 pts | 2 pts | 1 pt | 0 pts |
|---|---|---|---|---|
| **Search %** | >50% | 40–50% | 35–40% | <35% |
| **DR** | >65 | 50–65 | 40–50 | <40 |
| **$/DR point** | <$2 | $2–4 | $4–6 | >$6 |
| **Category fit** | Crypto+Finance | Crypto+Other | Finance only | Irrelevant |
| **Monthly traffic** | >100K | 30–100K | 5–30K | <5K |

**Verdict:** ≥14 = must-buy, ≥11 = strong, ≥8 = viable, <8 = skip
""")

    catalog_total = sum(len(v) for v in RAW_OUTLETS.values())
    st.caption(f"Catalog: {catalog_total} outlets across {len(RAW_OUTLETS)} languages · Collaborator.pro · DR ≥ 30, price ≤ $250")

    # ══════════════════════════════════════════════════════════════
    tab_search, tab_serpzilla, tab_shortlist = st.tabs([
        "🔍 Search Catalog (Collaborator)",
        "🪙 Serpzilla (live, crypto-native)",
        "📋 My Shortlist",
    ])

    # ── Tab 1: Search Catalog ────────────────────────────────────
    with tab_search:
        st.subheader("Search & Filter")

        fc1, fc2, fc3, fc4, fc5 = st.columns([2, 1, 1, 1, 1])
        with fc1:
            # Default to English only (EN-global strategy)
            selected_langs = st.multiselect(
                "Languages", options=list(LANG_LABELS.keys()),
                default=["en"],
                format_func=lambda k: LANG_LABELS[k],
            )
        with fc2:
            min_dr = st.slider("Min DR", min_value=30, max_value=80, value=50, step=5)
        with fc3:
            max_price = st.slider("Max price ($)", min_value=20, max_value=250, value=200, step=10)
        with fc4:
            min_score = st.slider("Min score", min_value=0, max_value=15, value=11, step=1)
        with fc5:
            crypto_only = st.toggle("Crypto category only", value=True)

        catalog_rows = []
        for lang in selected_langs:
            for o in get_outlets(lang, min_dr=min_dr, max_price=max_price,
                                 min_score=min_score, crypto_only=crypto_only):
                catalog_rows.append({
                    "Lang":      LANG_LABELS[lang],
                    "Domain":    o["domain"],
                    "DR":        o["dr"],
                    "Price ($)": o["price"],
                    "$/DR":      o["price_per_dr"],
                    "Search %":  o["search_pct"],
                    "Traffic":   o["traffic"],
                    "Score":     o["score"],
                    "Rating":    score_label(o["score"]),
                    "Crypto":    "✅" if o["has_crypto"] else "—",
                })

        if catalog_rows:
            cat_df = pd.DataFrame(catalog_rows)

            def color_catalog(row):
                s = row["Score"]
                if s >= 14: return ["background-color: #c3e6cb"] * len(row)
                if s >= 12: return ["background-color: #d4edda"] * len(row)
                if s >= 11: return ["background-color: #e8f4fd"] * len(row)
                return [""] * len(row)

            st.dataframe(
                cat_df.style.apply(color_catalog, axis=1),
                use_container_width=True, hide_index=True,
                column_config={
                    "Price ($)": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
                    "$/DR":      st.column_config.NumberColumn("$/DR",      format="$%.2f"),
                    "Search %":  st.column_config.NumberColumn("Search %",  format="%d%%"),
                    "Traffic":   st.column_config.NumberColumn("Traffic",   format="%d"),
                    "DR":        st.column_config.NumberColumn("DR"),
                    "Score":     st.column_config.NumberColumn("Score /15"),
                },
            )

            c1, c2, c3 = st.columns(3)
            c1.metric("Outlets shown", len(catalog_rows))
            c2.metric("Avg score", f"{cat_df['Score'].mean():.1f} / 15")
            c3.metric("Avg price", f"${cat_df['Price ($)'].mean():.0f}")

            # ── Add to shortlist ──────────────────────────────────
            st.subheader("Add to Shortlist")
            st.caption("Select outlets from the catalog above and assign them to a content pillar.")

            pillar_options = {p["id"]: p["label"] for p in CONTENT_PILLARS}
            ac1, ac2, ac3 = st.columns([3, 2, 1])
            with ac1:
                selected_domain = st.selectbox(
                    "Outlet", options=[r["Domain"] for r in catalog_rows],
                    key="shortlist_domain",
                )
            with ac2:
                selected_pillar = st.selectbox(
                    "Assign to pillar",
                    options=list(pillar_options.keys()),
                    format_func=lambda k: pillar_options[k],
                    key="shortlist_pillar",
                )
            with ac3:
                st.markdown("&nbsp;")  # spacer
                if st.button("➕ Add", type="primary"):
                    if "outlet_shortlist" not in st.session_state:
                        st.session_state["outlet_shortlist"] = []
                    # Find the full row data
                    row_data = next((r for r in catalog_rows if r["Domain"] == selected_domain), None)
                    if row_data:
                        entry = {**row_data, "Pillar": selected_pillar, "Pillar Name": pillar_options[selected_pillar]}
                        # Avoid duplicates
                        existing = {(e["Domain"], e["Pillar"]) for e in st.session_state["outlet_shortlist"]}
                        if (selected_domain, selected_pillar) not in existing:
                            st.session_state["outlet_shortlist"].append(entry)
                            st.success(f"Added {selected_domain} → {pillar_options[selected_pillar]}")
                        else:
                            st.warning(f"{selected_domain} already in shortlist for this pillar.")
        else:
            st.info("No outlets match current filters — try relaxing DR, price, or score constraints.")

        # ── Top Picks ─────────────────────────────────────────────
        st.subheader("🏆 Top 5 per Language")
        st.caption("Auto-ranked by score · DR ≥ 50 · Price ≤ $200 · Crypto category preferred")
        top = get_top_outlets_all_langs(min_dr=50, max_price=200, top_n=5)
        visible_langs = [lang for lang in selected_langs if top.get(lang)]
        if visible_langs:
            cols = st.columns(len(visible_langs))
            for idx, lang in enumerate(visible_langs):
                picks = top[lang]
                with cols[idx]:
                    st.markdown(f"**{LANG_LABELS[lang]}**")
                    for p in picks:
                        badge = score_label(p["score"])
                        crypto_tag = " 🪙" if p["has_crypto"] else ""
                        st.markdown(
                            f"**{p['domain']}**{crypto_tag}  \n"
                            f"{badge} · DR {p['dr']} · ${p['price']:.0f}  \n"
                            f"Search {p['search_pct']}% · {p['traffic']:,} visits"
                        )
                        st.divider()

    # ── Tab 1b: Serpzilla live catalog ───────────────────────────
    with tab_serpzilla:
        st.subheader("Serpzilla — Live Crypto-Native Catalog")
        st.caption(
            "Live pull from https://app.serpzilla.com via its REST API. "
            "Crypto-focused catalog; every result is topically relevant. "
            "Guest posts score 1.0× in Publication ROI, link insertions 0.10× GEO — "
            "pick `news` / `review` for guest posts, `link` / `archive` for insertions."
        )

        sz_login = st.session_state.get("serpzilla_login", "")
        sz_token = st.session_state.get("serpzilla_token", "")
        if not (sz_login and sz_token):
            st.warning(
                "Add **SERPZILLA_LOGIN** + **SERPZILLA_API_TOKEN** to "
                "`.streamlit/secrets.toml` (or the sidebar inputs) to enable "
                "live catalog. Get your API token from app.serpzilla.com → "
                "Passport → API Token."
            )
            st.stop()

        sc1, sc2, sc3, sc4 = st.columns([2, 1, 1, 1])
        with sc1:
            sz_target = st.text_input(
                "Target domain (creates/reuses a Serpzilla project)",
                value="https://nonbank.io/",
                key="sz_target_domain",
            )
        with sc2:
            sz_link_type = st.selectbox(
                "Link type", options=["news", "review", "link", "archive"],
                format_func=lambda v: {
                    "news":    "news (Guest Post, advertiser-written)",
                    "review":  "review (Guest Post, publisher-written)",
                    "link":    "link (Link Insertion — existing article)",
                    "archive": "archive (Link Insertion — archive)",
                }[v],
                index=0,
                help="Guest posts (news/review) get 1.0× SEO+GEO in the ROI model. Link insertions get 0.45× SEO / 0.10× GEO.",
            )
        with sc3:
            sz_price_min = st.number_input("Min price ($)", 0, 5000, 30, 10, key="sz_pmin")
            sz_price_max = st.number_input("Max price ($)", 0, 5000, 400, 10, key="sz_pmax")
        with sc4:
            sz_dr_min = st.number_input("Min DR", 0, 100, 40, 5, key="sz_drmin")
            sz_traffic_min = st.number_input("Min traffic", 0, 10_000_000, 1_000, 500, key="sz_tmin")

        if st.button("🔍 Search Serpzilla", type="primary", key="sz_search_btn"):
            try:
                with st.spinner("Authenticating + searching Serpzilla catalog..."):
                    client = SerpzillaClient(sz_login, sz_token).authenticate()
                    proj = client.ensure_project(sz_target)
                    resp = client.search_catalog(
                        project_id=proj["projectId"],
                        link_type=sz_link_type,
                        price_min=sz_price_min or None,
                        price_max=sz_price_max or None,
                        dr_min=sz_dr_min or None,
                        traffic_min=sz_traffic_min or None,
                    )
                    items = resp.get("items", []) or []
                    outlets = SerpzillaClient.normalize(items, link_type=sz_link_type)
                    st.session_state["sz_last_outlets"] = outlets
                    if resp.get("_fallback_applied"):
                        st.info(
                            "Server-side DR/traffic filters rejected — applied "
                            "client-side after fetching by price only."
                        )
                    st.success(f"Found {len(outlets)} Serpzilla outlets (projectId={proj['projectId']}).")
            except SerpzillaError as e:
                st.error(f"Serpzilla error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

        outlets = st.session_state.get("sz_last_outlets", [])
        if outlets:
            sz_rows = [{
                "Domain":       o["domain"],
                "DR":           o["dr"],
                "Price ($)":    o["price"],
                "$/DR":         o["price_per_dr"],
                "Traffic":      o["traffic"],
                "Type":         "📝 Guest post" if o["content_type"] == "guest_post" else "🔗 Link insertion",
                "Placement %":  o.get("placement_percent"),
                "Uniqueness %": o.get("placement_uniqueness"),
                "Days→Index":   o.get("avg_days_to_index"),
                "Trust":        o.get("trust"),
                "Rating":       o.get("rating_combined"),
                "Moz DA":       o.get("moz_da"),
                "Ahrefs dom.":  o.get("ahrefs_domains"),
                "Nofollow":     "⚠️" if o.get("is_nofollow") else "—",
                "Content type": o["content_type"],
            } for o in outlets]

            sz_df = pd.DataFrame(sz_rows)

            # Sort by a Serpzilla-tuned composite: DR × trust × placement% / price
            if not sz_df.empty:
                sz_df["_rank"] = (
                    sz_df["DR"].fillna(0)
                    * sz_df["Trust"].fillna(0).clip(lower=0.1)
                    * (sz_df["Placement %"].fillna(50) / 100)
                    / sz_df["Price ($)"].clip(lower=1)
                )
                sz_df = sz_df.sort_values("_rank", ascending=False)

            st.dataframe(
                sz_df.drop(columns=[c for c in ["_rank", "Content type"] if c in sz_df.columns]),
                use_container_width=True, hide_index=True,
                column_config={
                    "Price ($)":    st.column_config.NumberColumn("Price ($)",    format="$%.0f"),
                    "$/DR":         st.column_config.NumberColumn("$/DR",         format="$%.2f"),
                    "Traffic":      st.column_config.NumberColumn("Traffic",      format="%d"),
                    "Placement %":  st.column_config.NumberColumn("Placement %",  format="%d%%"),
                    "Uniqueness %": st.column_config.NumberColumn("Uniqueness %", format="%d%%"),
                    "Days→Index":   st.column_config.NumberColumn("Days→Index"),
                    "Trust":        st.column_config.NumberColumn("Trust",        format="%.1f"),
                    "Rating":       st.column_config.NumberColumn("Rating",       format="%.1f"),
                    "Moz DA":       st.column_config.NumberColumn("Moz DA"),
                    "Ahrefs dom.":  st.column_config.NumberColumn("Ahrefs dom."),
                },
            )

            c1, c2, c3 = st.columns(3)
            c1.metric("Outlets", len(sz_df))
            c2.metric("Avg DR", f"{sz_df['DR'].mean():.0f}")
            c3.metric("Avg price", f"${sz_df['Price ($)'].mean():.0f}")

            st.subheader("Add to Shortlist")
            pillar_options = {p["id"]: p["label"] for p in CONTENT_PILLARS}
            zc1, zc2, zc3 = st.columns([3, 2, 1])
            with zc1:
                sz_pick = st.selectbox(
                    "Outlet", options=[r["Domain"] for r in sz_rows],
                    key="sz_shortlist_domain",
                )
            with zc2:
                sz_pillar = st.selectbox(
                    "Assign to pillar",
                    options=list(pillar_options.keys()),
                    format_func=lambda k: pillar_options[k],
                    key="sz_shortlist_pillar",
                )
            with zc3:
                st.markdown("&nbsp;")
                if st.button("➕ Add", key="sz_add_btn", type="primary"):
                    row_data = next((r for r in sz_rows if r["Domain"] == sz_pick), None)
                    if row_data:
                        entry = {
                            **row_data,
                            "Lang": "🇬🇧 English",  # Serpzilla rows treated as EN-global
                            "Score": None,
                            "Crypto": "✅",
                            "Source": "serpzilla",
                            "Pillar": sz_pillar,
                            "Pillar Name": pillar_options[sz_pillar],
                        }
                        if "outlet_shortlist" not in st.session_state:
                            st.session_state["outlet_shortlist"] = []
                        existing = {(e["Domain"], e.get("Pillar")) for e in st.session_state["outlet_shortlist"]}
                        if (sz_pick, sz_pillar) not in existing:
                            st.session_state["outlet_shortlist"].append(entry)
                            st.success(f"Added {sz_pick} → {pillar_options[sz_pillar]} (Serpzilla)")
                        else:
                            st.warning(f"{sz_pick} already in shortlist for this pillar.")
        else:
            st.info("No Serpzilla results yet — hit **🔍 Search Serpzilla** above.")

    # ── Tab 2: My Shortlist ──────────────────────────────────────
    with tab_shortlist:
        shortlist = st.session_state.get("outlet_shortlist", [])

        if not shortlist:
            st.info(
                "No outlets shortlisted yet. Go to **Search Catalog** tab, find outlets, "
                "and click **➕ Add** to build your shortlist."
            )
            st.markdown("""
**Recommended workflow:**
1. Run **Competitor Intel** → understand which pillars to target
2. Run **Keyword Intel** → validate search demand
3. Come here → search outlets by DR, price, crypto category
4. Add best outlets to shortlist, assign to pillars
5. Go to **Publication ROI** → sanity-check expected ROI
6. Go to **Content Strategy** → build the publication calendar
""")
        else:
            st.subheader(f"Shortlisted Outlets ({len(shortlist)})")

            sl_df = pd.DataFrame(shortlist)
            display_cols = ["Pillar Name", "Domain", "DR", "Price ($)", "Score", "Rating", "Lang"]
            available_cols = [c for c in display_cols if c in sl_df.columns]

            st.dataframe(sl_df[available_cols], use_container_width=True, hide_index=True)

            # Summary by pillar
            st.subheader("Budget by Pillar")
            if "Price ($)" in sl_df.columns:
                pillar_spend = sl_df.groupby("Pillar Name")["Price ($)"].agg(["sum", "count"]).reset_index()
                pillar_spend.columns = ["Pillar", "Total ($)", "Outlets"]
                st.dataframe(pillar_spend, use_container_width=True, hide_index=True,
                             column_config={"Total ($)": st.column_config.NumberColumn("Total ($)", format="$%.0f")})

                total = pillar_spend["Total ($)"].sum()
                st.metric("Total Shortlist Spend", f"${total:,.0f}")

            # Clear shortlist
            if st.button("🗑️ Clear Shortlist"):
                st.session_state["outlet_shortlist"] = []
                st.rerun()

            # Export
            csv = sl_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Export shortlist as CSV", csv,
                               file_name="nonbank_outlet_shortlist.csv", mime="text/csv")
