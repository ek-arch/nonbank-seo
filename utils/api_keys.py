"""
utils/api_keys.py — Sidebar API key management
================================================
Auto-loads keys from Streamlit Cloud secrets. Shows status badges for
connected keys. Only shows manual input for keys NOT in secrets.
"""
from __future__ import annotations

import json
import streamlit as st


def _try_secret(name: str) -> str:
    """Try to load a secret from Streamlit secrets, return empty string on failure."""
    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""


def setup_sidebar() -> None:
    """Render the shared sidebar: branding, API keys, pipeline status."""
    with st.sidebar:
        st.image("https://nonbank.io/favicon.ico", width=32)
        st.title("Nonbank SEO & GEO Agent")
        st.caption("nonbank.io · DeFi wallet + Visa card (hybrid)")
        st.divider()

        # ── API Keys: auto-load from secrets, show input only if missing ──
        st.subheader("🔑 API Keys")

        # Define all keys: (session_state_key, secret_name, label, placeholder)
        key_defs = [
            ("anthropic_token", "ANTHROPIC_API_KEY", "Anthropic (Claude)", "sk-ant-..."),
            ("perplexity_key",  "PERPLEXITY_KEY",    "Perplexity",         "pplx-..."),
            ("serpapi_key",     "SERPAPI_KEY",        "SerpAPI",            "..."),
            ("collab_token",    "COLLABORATOR_KEY",   "Collaborator.pro",   "etVxo-..."),
        ]

        for ss_key, secret_name, label, placeholder in key_defs:
            secret_val = _try_secret(secret_name)
            if secret_val:
                # Key exists in Streamlit secrets — auto-load silently
                st.session_state[ss_key] = secret_val
                st.markdown(f"✅ **{label}** — connected")
            else:
                # Key not in secrets — show manual input
                val = st.text_input(
                    label, type="password", placeholder=placeholder,
                    key=f"_input_{ss_key}",
                )
                if val:
                    st.session_state[ss_key] = val

        # Google Sheets creds from secrets (no manual input — too complex)
        try:
            gsheets_creds = json.dumps(dict(st.secrets["gsheets"]))
            st.session_state["gsheets_json"] = gsheets_creds
            st.markdown("✅ **Google Sheets** — connected")
        except Exception:
            st.markdown("⬜ **Google Sheets** — not configured")

        # ── Key summary ───────────────────────────────────────────
        connected = sum(1 for ss_key, _, _, _ in key_defs if st.session_state.get(ss_key))
        has_sheets = bool(st.session_state.get("gsheets_json"))
        total = len(key_defs) + (1 if has_sheets else 0)
        st.caption(f"{connected + (1 if has_sheets else 0)}/{len(key_defs) + 1} keys connected")

        # ── Pipeline Status ───────────────────────────────────────
        st.divider()
        st.subheader("📋 Pipeline")
        stages = [
            ("Research", [
                ("Competitor Intel", "🔍"),
                ("Keyword Intel", "🧠"),
            ]),
            ("Strategy", [
                ("Content Strategy", "✍️"),
                ("Outlet Matching", "🗞️"),
                ("Publication ROI", "💰"),
            ]),
            ("Execution", [
                ("PR Generator", "📝"),
                ("Distribution", "📣"),
                ("Content Brief Factory", "🚀"),
            ]),
            ("Measure", [
                ("GEO Tracker", "🎯"),
                ("Monthly Eval", "📉"),
                ("Monthly Planner", "🗓️"),
            ]),
        ]
        for group, items in stages:
            st.markdown(f"**{group}**")
            for name, icon in items:
                st.markdown(f"&nbsp;&nbsp;{icon} {name}")

        st.divider()
        st.caption("Nonbank SEO Agent · research-first flow")


def get_api_key(name: str) -> str:
    """Get an API key from session state. Returns empty string if not set."""
    return st.session_state.get(name, "")


def get_sheets_creds() -> str:
    """Get Google Sheets credentials from session state or Streamlit secrets."""
    creds = st.session_state.get("gsheets_json", "")
    if creds:
        return creds
    try:
        return json.dumps(dict(st.secrets["gsheets"]))
    except Exception:
        return ""
