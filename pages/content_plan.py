"""Page — Content Strategy: pillars, article briefs, and publication calendar."""
from __future__ import annotations

import json
import streamlit as st
import pandas as pd

from config import CONTENT_PILLARS, BRIEFS, PLAN_DEFAULT
from utils.api_keys import get_api_key, get_sheets_creds

try:
    from sheets_client import load_content_plan, save_content_plan
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False
    def load_content_plan(*a, **kw): return []
    def save_content_plan(*a, **kw): return 0

try:
    from llm_client import _client, _call_with_retry
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


# ── Helpers ──────────────────────────────────────────────────────────────────

PRIORITY_COLORS = {"High": "red", "Medium": "orange", "Low": "blue"}

STATUS_OPTIONS = ["Draft", "In Progress", "Published"]
PLAN_STATUS_OPTIONS = ["To Do", "In Progress", "Done", "Skipped"]
PLAN_TYPE_OPTIONS = ["SEO", "GEO", "SEO+GEO", "Social"]
WEEK_OPTIONS = ["1", "2", "3", "4", "Apr", "May", "Ongoing"]


def _load_plan():
    """Load publication calendar from Google Sheets; fall back to config."""
    creds = get_sheets_creds()
    if creds:
        try:
            rows = load_content_plan(creds)
            if rows:
                return rows
        except Exception:
            pass
    return list(PLAN_DEFAULT)


def _save_plan(plan):
    """Persist publication calendar to Google Sheets."""
    creds = get_sheets_creds()
    if creds:
        try:
            save_content_plan(creds, plan)
        except Exception:
            pass


def _pillar_lookup():
    """Return {id: label} map for pillars."""
    return {p["id"]: p["label"] for p in CONTENT_PILLARS}


def _generate_briefs_for_pillar(pillar: dict, api_key: str) -> list[dict]:
    """Use Claude to generate 3-5 article briefs for a given pillar."""
    if not LLM_AVAILABLE:
        return []
    client = _client(api_key)
    keywords = ", ".join(pillar["seed_keywords"])
    prompt = (
        f"Generate 3-5 SEO article briefs for the content pillar: {pillar['label']}.\n"
        f"Product: Nonbank (nonbank.io) — a non-custodial crypto wallet with Visa card, "
        f"gasless transactions, built-in AML screening, and unified portfolio management.\n"
        f"Seed keywords: {keywords}.\n"
        f"Return ONLY a JSON array with objects containing these fields:\n"
        f"  Title (string), Lang (EN/ES/PT), Market (Global/LATAM/ARE/BRA/etc), "
        f"KW (primary keyword), Words (800-1500), Priority (High/Medium)\n"
        f"No markdown, no explanation — just the JSON array."
    )
    resp = _call_with_retry(
        client,
        model="claude-sonnet-4-6",
        max_tokens=2048,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return []


# ── Main page ────────────────────────────────────────────────────────────────

def page_content_plan():
    st.title("Content Strategy")
    st.caption("Content pillars, article briefs, and publication calendar")

    tab_pillars, tab_briefs, tab_calendar = st.tabs([
        "Content Pillars", "Article Briefs", "Publication Calendar",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — Content Pillars
    # ══════════════════════════════════════════════════════════════════════════
    with tab_pillars:
        high = sum(1 for p in CONTENT_PILLARS if p["priority"] == "High")
        medium = sum(1 for p in CONTENT_PILLARS if p["priority"] == "Medium")

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Pillars", len(CONTENT_PILLARS))
        c2.metric("High Priority", high)
        c3.metric("Medium Priority", medium)

        st.divider()

        for pillar in CONTENT_PILLARS:
            color = PRIORITY_COLORS.get(pillar["priority"], "gray")
            with st.expander(f"{pillar['label']}  :{color}[{pillar['priority']}]"):
                st.markdown(f"**Description:** {pillar['description']}")
                st.markdown(f"**Differentiator:** `{pillar['differentiator']}`")
                st.markdown("**Seed keywords:**")
                cols = st.columns(3)
                for i, kw in enumerate(pillar["seed_keywords"]):
                    cols[i % 3].code(kw, language=None)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — Article Briefs
    # ══════════════════════════════════════════════════════════════════════════
    with tab_briefs:
        pillar_map = _pillar_lookup()
        pillar_ids = list(pillar_map.keys())

        # Initialize briefs in session state
        if "briefs" not in st.session_state:
            briefs_data = []
            for b in BRIEFS:
                row = dict(b)
                row.setdefault("Status", "Draft")
                briefs_data.append(row)
            st.session_state["briefs"] = briefs_data

        briefs_df = pd.DataFrame(st.session_state["briefs"])

        # Ensure Status column exists
        if "Status" not in briefs_df.columns:
            briefs_df["Status"] = "Draft"

        # ── Filters ──
        filter_cols = st.columns(2)
        with filter_cols[0]:
            sel_pillars = st.multiselect(
                "Filter by pillar",
                options=pillar_ids,
                format_func=lambda x: pillar_map.get(x, x),
                key="brief_pillar_filter",
            )
        with filter_cols[1]:
            sel_priority = st.multiselect(
                "Filter by priority",
                options=["High", "Medium", "Low"],
                key="brief_priority_filter",
            )

        view_df = briefs_df.copy()
        if sel_pillars:
            view_df = view_df[view_df["Pillar"].isin(sel_pillars)]
        if sel_priority:
            view_df = view_df[view_df["Priority"].isin(sel_priority)]

        # ── Summary metrics ──
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Briefs", len(briefs_df))
        m2.metric("Draft", len(briefs_df[briefs_df["Status"] == "Draft"]))
        m3.metric("In Progress", len(briefs_df[briefs_df["Status"] == "In Progress"]))
        m4.metric("Published", len(briefs_df[briefs_df["Status"] == "Published"]))

        st.divider()

        # ── Editable table ──
        edited_briefs = st.data_editor(
            view_df,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "#": st.column_config.NumberColumn("#", width="small"),
                "Title": st.column_config.TextColumn("Title", width="large"),
                "Lang": st.column_config.SelectboxColumn(
                    "Lang", options=["EN", "ES", "PT", "TR", "AR"], width="small",
                ),
                "Market": st.column_config.TextColumn("Market", width="small"),
                "KW": st.column_config.TextColumn("KW"),
                "Words": st.column_config.NumberColumn("Words", width="small"),
                "Priority": st.column_config.SelectboxColumn(
                    "Priority", options=["High", "Medium", "Low"], width="small",
                ),
                "Pillar": st.column_config.SelectboxColumn(
                    "Pillar", options=pillar_ids, width="medium",
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status", options=STATUS_OPTIONS, default="Draft", width="small",
                ),
            },
            key="briefs_editor",
        )

        # Persist edits back to session state
        st.session_state["briefs"] = edited_briefs.to_dict("records")

        # ── Brief Generator ──
        st.divider()
        st.subheader("Brief Generator")

        gen_cols = st.columns([3, 1])
        with gen_cols[0]:
            selected_pillar_id = st.selectbox(
                "Select pillar",
                options=pillar_ids,
                format_func=lambda x: pillar_map.get(x, x),
                key="gen_pillar_select",
            )
        anthropic_token = get_api_key("anthropic_token")
        can_generate = bool(anthropic_token) and LLM_AVAILABLE

        with gen_cols[1]:
            st.write("")  # vertical spacer
            st.write("")
            generate_clicked = st.button(
                "Generate briefs",
                type="primary",
                disabled=not can_generate,
            )

        if not anthropic_token:
            st.info("Enter your Anthropic API key in the sidebar to enable brief generation.")

        if generate_clicked and can_generate:
            pillar = next((p for p in CONTENT_PILLARS if p["id"] == selected_pillar_id), None)
            if pillar:
                with st.spinner(f"Generating briefs for {pillar['label']}..."):
                    new_briefs = _generate_briefs_for_pillar(pillar, anthropic_token)
                if new_briefs:
                    existing = st.session_state["briefs"]
                    next_num = max((b.get("#", 0) for b in existing), default=0) + 1
                    for i, nb in enumerate(new_briefs):
                        nb["#"] = next_num + i
                        nb["Pillar"] = selected_pillar_id
                        nb["Status"] = "Draft"
                        existing.append(nb)
                    st.session_state["briefs"] = existing
                    st.success(f"Added {len(new_briefs)} briefs for {pillar['label']}.")
                    st.rerun()
                else:
                    st.warning("No briefs generated. Check API key or try again.")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — Publication Calendar
    # ══════════════════════════════════════════════════════════════════════════
    with tab_calendar:
        # Load plan from Sheets or config
        if "content_plan" not in st.session_state:
            st.session_state["content_plan"] = _load_plan()

        plan = st.session_state["content_plan"]
        plan_df = pd.DataFrame(plan)

        # ── Filters ──
        filter_c1, filter_c2, filter_c3 = st.columns(3)
        with filter_c1:
            week_filter = st.multiselect("Filter by Week", options=WEEK_OPTIONS, key="cal_week")
        with filter_c2:
            status_filter = st.multiselect("Filter by Status", options=PLAN_STATUS_OPTIONS, key="cal_status")
        with filter_c3:
            type_filter = st.multiselect("Filter by Type", options=PLAN_TYPE_OPTIONS, key="cal_type")

        cal_df = plan_df.copy()
        if week_filter:
            cal_df = cal_df[cal_df["Week"].isin(week_filter)]
        if status_filter:
            cal_df = cal_df[cal_df["Status"].isin(status_filter)]
        if type_filter:
            cal_df = cal_df[cal_df["Type"].isin(type_filter)]

        # ── Summary metrics ──
        total = len(plan_df)
        done = len(plan_df[plan_df["Status"].fillna("") == "Done"]) if "Status" in plan_df.columns else 0
        in_prog = len(plan_df[plan_df["Status"].fillna("") == "In Progress"]) if "Status" in plan_df.columns else 0
        seo_count = len(plan_df[plan_df["Type"].str.contains("SEO", na=False)]) if "Type" in plan_df.columns else 0
        social_count = len(plan_df[plan_df["Type"].fillna("") == "Social"]) if "Type" in plan_df.columns else 0

        # Estimated spend
        spend_total = 0
        if "Price" in plan_df.columns:
            for val in plan_df["Price"].dropna():
                val_str = str(val).replace("$", "").replace(",", "")
                # Take the lower bound of ranges like "$20-150"
                parts = val_str.split("–") if "–" in val_str else val_str.split("-")
                try:
                    spend_total += float(parts[0])
                except (ValueError, IndexError):
                    pass

        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("Total Tasks", total)
        mc2.metric("Done", done)
        mc3.metric("In Progress", in_prog)
        mc4.metric("SEO/GEO Articles", seo_count)
        mc5.metric("Est. Min Spend", f"${spend_total:,.0f}")

        st.divider()

        # ── Editable table ──
        edited_plan = st.data_editor(
            cal_df,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    options=PLAN_STATUS_OPTIONS, default="To Do",
                ),
                "Type": st.column_config.SelectboxColumn(
                    options=PLAN_TYPE_OPTIONS, default="SEO",
                ),
                "Week": st.column_config.SelectboxColumn(
                    options=WEEK_OPTIONS, default="1",
                ),
                "Publication URL": st.column_config.LinkColumn("Publication URL"),
                "Reddit/Quora URL": st.column_config.LinkColumn("Reddit/Quora URL"),
            },
            key="plan_editor",
        )

        # Persist edits
        updated_plan = edited_plan.to_dict("records")
        st.session_state["content_plan"] = updated_plan

        # ── Save / Export ──
        st.divider()
        gsheets_creds = get_sheets_creds()
        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Save to Google Sheets", type="primary", disabled=not gsheets_creds):
                with st.spinner("Saving..."):
                    try:
                        n = save_content_plan(gsheets_creds, updated_plan)
                        st.success(f"Saved {n} tasks to Google Sheets.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
        with btn_cols[1]:
            csv = edited_plan.to_csv(index=False)
            st.download_button(
                "Download CSV", data=csv,
                file_name="publication_calendar.csv", mime="text/csv",
            )

        # Quick guide
        with st.expander("How to use this calendar"):
            st.markdown(
                "**Type:** SEO = backlinks + search traffic, GEO = AI citation optimized, "
                "SEO+GEO = both, Social = Reddit/Quora seeding.\n\n"
                "**Workflow:** Set status to In Progress, publish article, paste URL, "
                "then mark Done and save to Sheets."
            )
