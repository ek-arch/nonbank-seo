"""
pages/gsc_dashboard.py — Google Search Console Dashboard
=========================================================
Live GSC data inside the app: performance, indexation, sitemaps, URL inspector.
Auth via service account JSON in Streamlit secrets under [gsc].
"""
from __future__ import annotations

import json
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from gsc_client import (
    DEFAULT_SITE_CANDIDATES,
    inspect_url,
    inspect_urls_bulk,
    list_sitemaps,
    list_sites,
    performance_summary,
    pick_site,
    query_search_analytics,
    submit_sitemap,
    delete_sitemap,
)


def _get_creds() -> str | None:
    """Pull GSC service account JSON from session or secrets."""
    # Prefer explicit [gsc] block; fall back to reusing [gsheets] (same account)
    creds = st.session_state.get("gsc_json")
    if creds:
        return creds
    try:
        return json.dumps(dict(st.secrets["gsc"]))
    except Exception:
        pass
    try:
        return json.dumps(dict(st.secrets["gsheets"]))
    except Exception:
        return None


def page_gsc_dashboard() -> None:
    st.title("📊 Google Search Console")
    st.caption("Live performance, indexation, sitemaps, URL inspection — pulled directly from GSC.")

    creds = _get_creds()
    if not creds:
        st.warning(
            "**GSC credentials not configured.** Add a service account JSON to "
            "`.streamlit/secrets.toml` under `[gsc]` (or reuse `[gsheets]` if the "
            "same service account has GSC access).\n\n"
            "**Setup:**\n"
            "1. Google Cloud Console → enable **Search Console API**\n"
            "2. Create a service account → download JSON key\n"
            "3. In GSC → Settings → Users and permissions → Add the service account "
            "email with Full (or Restricted) access\n"
            "4. Paste the JSON as a `[gsc]` block in secrets.toml"
        )
        return

    # Detect the site
    site_url = st.session_state.get("gsc_site_url")
    if not site_url:
        with st.spinner("Detecting GSC property…"):
            try:
                site_url = pick_site(creds)
            except Exception as e:
                st.error(f"GSC auth failed: {e}")
                return

    if not site_url:
        st.error(
            "The service account is authenticated but has no access to any GSC "
            "property. Add it as a user on `sc-domain:nonbank.io` (or the "
            "URL-prefix property) in GSC → Settings → Users and permissions."
        )
        try:
            sites = list_sites(creds)
            st.caption(f"Service account currently sees: {[s.get('siteUrl') for s in sites] or 'no sites'}")
        except Exception:
            pass
        return

    st.session_state["gsc_site_url"] = site_url
    cols = st.columns([3, 1])
    cols[0].success(f"Connected: `{site_url}`")
    if cols[1].button("Change property", use_container_width=True):
        st.session_state.pop("gsc_site_url", None)
        st.rerun()

    tabs = st.tabs([
        "📈 Performance",
        "🗂️ Indexation",
        "🗺️ Sitemaps",
        "🔍 URL Inspector",
    ])

    # ── Performance ────────────────────────────────────────────────────
    with tabs[0]:
        c1, c2, c3 = st.columns(3)
        days = c1.selectbox("Range", [7, 28, 90, 180, 365], index=1, key="gsc_days")
        search_type = c2.selectbox("Search type", ["web", "image", "video", "news"], index=0, key="gsc_type")
        refresh = c3.button("🔄 Refresh", use_container_width=True)

        cache_key = f"gsc_summary_{days}_{search_type}"
        if refresh or cache_key not in st.session_state:
            with st.spinner(f"Loading last {days}d from GSC…"):
                try:
                    summary = performance_summary(creds, site_url, days=days)
                    st.session_state[cache_key] = summary
                except Exception as e:
                    st.error(f"GSC query failed: {e}")
                    return

        summary = st.session_state[cache_key]
        t = summary["totals"]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Clicks", f"{t['clicks']:,}")
        m2.metric("Impressions", f"{t['impressions']:,}")
        m3.metric("CTR", f"{t['ctr']*100:.2f}%")
        m4.metric("Avg position", f"{t['position']:.1f}")

        if not summary["by_date"].empty:
            st.subheader("Clicks & impressions over time")
            chart_df = summary["by_date"].copy()
            chart_df["date"] = pd.to_datetime(chart_df["date"])
            st.line_chart(chart_df.set_index("date")[["clicks", "impressions"]])

        st.subheader("Top queries")
        if summary["by_query"].empty:
            st.info("No query data for this range. The site may be too new or have too few impressions.")
        else:
            st.dataframe(summary["by_query"], use_container_width=True, hide_index=True)
            st.download_button(
                "Download queries CSV",
                summary["by_query"].to_csv(index=False),
                f"gsc_queries_{days}d.csv",
                mime="text/csv",
            )

        st.subheader("Top pages")
        if not summary["by_page"].empty:
            st.dataframe(summary["by_page"], use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("By country")
            if not summary["by_country"].empty:
                st.dataframe(summary["by_country"], use_container_width=True, hide_index=True)
        with c2:
            st.subheader("By device")
            if not summary["by_device"].empty:
                st.dataframe(summary["by_device"], use_container_width=True, hide_index=True)

        with st.expander("🔎 Query filter — dig into a topic"):
            flt = st.text_input("Query contains", placeholder="e.g. gasless, usdt, self-custody", key="gsc_filter_q")
            if flt:
                end = date.today() - timedelta(days=2)
                start = end - timedelta(days=days)
                try:
                    df = query_search_analytics(
                        creds, site_url,
                        start=start, end=end,
                        dimensions=["query", "page"],
                        filters=[{"dimension": "query", "operator": "contains", "expression": flt}],
                        row_limit=500,
                    )
                    st.dataframe(df, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Filter query failed: {e}")

    # ── Indexation ─────────────────────────────────────────────────────
    with tabs[1]:
        st.caption("Bulk-inspect a URL list to see what's indexed, what's excluded, and why.")
        default_urls = [
            "https://nonbank.io/",
            "https://nonbank.io/blog",
            "https://nonbank.io/hackathon/marketing",
            "https://nonbank.io/cookies-policy",
            "https://nonbank.io/privacy-statement",
            "https://nonbank.io/terms-conditions",
        ]
        urls_text = st.text_area(
            "URLs (one per line)",
            value="\n".join(default_urls),
            height=200,
            key="gsc_urls",
        )
        if st.button("🔎 Inspect all", type="primary"):
            urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
            if len(urls) > 50:
                st.warning(f"{len(urls)} URLs — this will take a moment and may hit per-minute quotas.")
            with st.spinner(f"Inspecting {len(urls)} URL(s)…"):
                try:
                    df = inspect_urls_bulk(creds, site_url, urls)
                    st.session_state["gsc_indexation_df"] = df
                except Exception as e:
                    st.error(f"Inspection failed: {e}")

        if "gsc_indexation_df" in st.session_state:
            df = st.session_state["gsc_indexation_df"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            # Quick summary
            if not df.empty and "coverage_state" in df.columns:
                counts = df["coverage_state"].value_counts().to_dict()
                st.caption("**Summary:** " + " · ".join(f"{k}: {v}" for k, v in counts.items()))
            st.download_button(
                "Download indexation CSV",
                df.to_csv(index=False),
                "gsc_indexation.csv",
                mime="text/csv",
            )

    # ── Sitemaps ───────────────────────────────────────────────────────
    with tabs[2]:
        st.caption("Submit, list, or delete sitemaps. Heads-up: `/sitemap.xml` is currently 404 on nonbank.io — needs Webflow Designer to enable auto-sitemap first.")
        if st.button("📋 List submitted sitemaps"):
            try:
                sm = list_sitemaps(creds, site_url)
                if not sm:
                    st.info("No sitemaps submitted yet.")
                else:
                    rows = []
                    for s in sm:
                        rows.append({
                            "path": s.get("path", ""),
                            "last_submitted": s.get("lastSubmitted", ""),
                            "is_pending": s.get("isPending", False),
                            "is_sitemaps_index": s.get("isSitemapsIndex", False),
                            "errors": s.get("errors", 0),
                            "warnings": s.get("warnings", 0),
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"List failed: {e}")

        st.divider()
        st.markdown("**Submit / re-submit a sitemap**")
        sitemap_url = st.text_input("Sitemap URL", value="https://nonbank.io/sitemap.xml", key="gsc_sm_url")
        c1, c2 = st.columns(2)
        if c1.button("➕ Submit", use_container_width=True):
            try:
                ok = submit_sitemap(creds, site_url, sitemap_url)
                st.success(f"Submitted: {sitemap_url}") if ok else st.error("Submit failed")
            except Exception as e:
                st.error(str(e))
        if c2.button("🗑️ Delete", use_container_width=True):
            try:
                ok = delete_sitemap(creds, site_url, sitemap_url)
                st.success(f"Deleted: {sitemap_url}") if ok else st.error("Delete failed")
            except Exception as e:
                st.error(str(e))

    # ── URL Inspector ──────────────────────────────────────────────────
    with tabs[3]:
        st.caption("Single-URL deep inspection — full index status, canonicals, mobile usability, rich results.")
        single_url = st.text_input("URL to inspect", value="https://nonbank.io/", key="gsc_single_url")
        if st.button("🔎 Inspect", type="primary"):
            with st.spinner("Inspecting…"):
                try:
                    r = inspect_url(creds, site_url, single_url)
                    st.session_state["gsc_single_inspect"] = r
                except Exception as e:
                    st.error(f"Inspection failed: {e}")

        r = st.session_state.get("gsc_single_inspect")
        if r:
            if "error" in r:
                st.error(r["error"])
            else:
                idx = r.get("indexStatusResult", {})
                m = st.container()
                with m:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Verdict", idx.get("verdict", "—"))
                    c2.metric("Coverage", idx.get("coverageState", "—"))
                    c3.metric("Last crawl", (idx.get("lastCrawlTime", "") or "—")[:10])

                with st.expander("Full inspection JSON"):
                    st.json(r)
