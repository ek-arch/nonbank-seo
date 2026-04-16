"""
pages/pseo.py — Content Brief Factory
======================================
Generates high-intent content briefs at scale across multiple formats:

  1. Competitor comparisons  — Nonbank vs X, X alternative, category roundups
  2. Differentiator deep-dives — one article per pillar × angle
  3. Use-case articles        — how users solve problems with Nonbank
  4. How-to guides            — step-by-step content for high-intent queries
  5. User-persona articles    — who should use Nonbank, in what scenario

Every brief is auto-generated from:
  - CONTENT_PILLARS (config.py)         — validated pillar research
  - COMPETITORS feature matrix          — grounded comparisons
  - PRODUCT_PROFILE differentiators     — real advantages, no hallucinations

Output feeds directly into the Content Plan's publication calendar.
"""
from __future__ import annotations

import json
from datetime import date
import streamlit as st
import pandas as pd

from config import COMPETITORS, FEATURE_DIMENSIONS, CONTENT_PILLARS, PRODUCT_PROFILE


# ══════════════════════════════════════════════════════════════════════════
# BRIEF TEMPLATES — each template = one way to package a content angle
# ══════════════════════════════════════════════════════════════════════════

COMPARISON_TEMPLATES = {
    "versus": {
        "label": "Head-to-head (Nonbank vs X)",
        "title_tmpl": "Nonbank vs {competitor}: {year} Comparison",
        "kw_tmpl":    "nonbank vs {comp_slug}",
        "slug_tmpl":  "/compare/nonbank-vs-{comp_slug}",
        "intent":     "Comparison / transactional",
        "words":      1500,
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
        "slug_tmpl":  "/{comp_slug}-alternative",
        "intent":     "Transactional / high-intent",
        "words":      1400,
        "outline": [
            "Why people look for {competitor} alternatives",
            "Key problems with {competitor}: {losses_list}",
            "How Nonbank solves them: {wins_list}",
            "Feature comparison snapshot",
            "When to stick with {competitor} (honest trade-offs)",
            "How to migrate from {competitor} to Nonbank",
            "FAQ",
        ],
    },
    "roundup": {
        "label": "Category roundup (Nonbank included)",
        "title_tmpl": "Best {category} in {year}: Top Options Compared",
        "kw_tmpl":    "best {category} {year}",
        "slug_tmpl":  "/best-{category_slug}",
        "intent":     "Informational / comparison",
        "words":      1800,
        "outline": [
            "What to look for in a {category}",
            "Our top picks — Nonbank + 4 competitors",
            "Side-by-side feature table",
            "Recommendation by user type",
            "FAQ",
        ],
    },
}

DIFFERENTIATOR_TEMPLATES = {
    "deep_dive": {
        "label": "Deep-dive explainer",
        "title_tmpl": "{diff_label}: How Nonbank {diff_action}",
        "kw_tmpl":    "{diff_seed_kw}",
        "slug_tmpl":  "/{diff_id}-explained",
        "intent":     "Informational / educational",
        "words":      1300,
        "outline": [
            "What is {diff_label}?",
            "Why it matters (problem this solves)",
            "How Nonbank implements it — technical explainer",
            "Comparison to competitors (who else has this?)",
            "Real-world user scenarios",
            "FAQ",
        ],
    },
    "why_matters": {
        "label": "Why it matters (advocacy angle)",
        "title_tmpl": "Why {diff_label} Is the Future of {category}",
        "kw_tmpl":    "why {diff_seed_kw}",
        "slug_tmpl":  "/why-{diff_id}",
        "intent":     "Thought-leadership / GEO citation",
        "words":      1200,
        "outline": [
            "The problem with current solutions (without {diff_label})",
            "Industry shift toward {diff_label}",
            "Quotable stats + data (AI citation bait)",
            "Nonbank's approach",
            "What this means for users",
            "FAQ",
        ],
    },
}

USE_CASE_TEMPLATES = {
    "persona": {
        "label": "User persona",
        "title_tmpl": "Best Crypto Wallet for {persona} in {year}",
        "kw_tmpl":    "crypto wallet for {persona_slug}",
        "slug_tmpl":  "/for-{persona_slug}",
        "intent":     "Transactional",
        "words":      1200,
        "outline": [
            "What {persona} need from a crypto wallet + card",
            "Common pain points",
            "How Nonbank fits — differentiators that matter for this persona",
            "Feature walkthrough",
            "FAQ",
        ],
    },
    "problem_solution": {
        "label": "Problem → solution",
        "title_tmpl": "How to {problem_action}: {year} Guide",
        "kw_tmpl":    "how to {problem_slug}",
        "slug_tmpl":  "/how-to-{problem_slug}",
        "intent":     "Informational / problem-aware",
        "words":      1100,
        "outline": [
            "The problem explained",
            "Traditional solutions (and why they fall short)",
            "Step-by-step solution with Nonbank",
            "Alternatives worth considering",
            "FAQ",
        ],
    },
}

# Pre-defined user personas (EN-global, no country-specific)
PERSONAS = [
    {"label": "Digital Nomads",      "slug": "digital-nomads"},
    {"label": "DeFi Power Users",    "slug": "defi-users"},
    {"label": "Crypto Freelancers",  "slug": "crypto-freelancers"},
    {"label": "Hardware Wallet Users","slug": "hardware-wallet-users"},
    {"label": "Stablecoin Savers",   "slug": "stablecoin-savers"},
    {"label": "Self-Custody Beginners","slug": "self-custody-beginners"},
]

# Pre-defined problem-action pairs (derived from Nonbank's actual features)
PROBLEMS = [
    {"action": "Spend Crypto Without Giving Up Your Keys",              "slug": "spend-crypto-self-custody"},
    {"action": "Send USDT Without Paying Gas Fees",                     "slug": "send-usdt-without-gas"},
    {"action": "Get a Crypto Visa Card in 100+ Countries",              "slug": "crypto-card-global"},
    {"action": "Track Multiple Wallets in One App",                     "slug": "track-multiple-wallets"},
    {"action": "Protect Yourself from Sanctioned Wallet Transfers",     "slug": "avoid-sanctioned-wallets"},
    {"action": "Spend Crypto from a Hardware Wallet",                   "slug": "spend-from-hardware-wallet"},
]

# Categories for roundups
ROUNDUP_CATEGORIES = [
    {"label": "non-custodial crypto card",       "slug": "non-custodial-crypto-card"},
    {"label": "DeFi wallet with Visa card",      "slug": "defi-wallet-with-card"},
    {"label": "hybrid DeFi+card crypto app",     "slug": "hybrid-defi-card-app"},
    {"label": "gasless crypto wallet",           "slug": "gasless-crypto-wallet"},
    {"label": "AML-safe self-custody wallet",    "slug": "aml-safe-wallet"},
]


# ══════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════

def _slug(s: str) -> str:
    return s.lower().replace(" ", "-").replace(".", "").replace(",", "").replace("'", "").replace("×", "x")


def _competitor_gaps_vs_nonbank(comp: dict, nonbank: dict) -> tuple[list[str], list[str]]:
    """Return (nonbank_wins, competitor_wins) — dimensions where each has advantage."""
    nonbank_wins, comp_wins = [], []
    for dim in FEATURE_DIMENSIONS:
        nb_val = str(nonbank.get(dim, "")).lower()
        cp_val = str(comp.get(dim, "")).lower()
        nb_positive = any(x in nb_val for x in ["yes", "live", "100+", "multi", "global"])
        nb_negative = any(x in nb_val for x in ["no ", "no\"", "pilot", "limited", "planned"])
        cp_positive = any(x in cp_val for x in ["yes", "live", "100+", "multi", "global"])
        cp_negative = any(x in cp_val for x in ["no ", "no\"", "pilot", "limited", "planned"])
        if nb_positive and cp_negative:
            nonbank_wins.append(f"**{dim}**: {nonbank.get(dim)}")
        elif cp_positive and nb_negative:
            comp_wins.append(f"**{dim}**: {comp.get(dim)}")
    return nonbank_wins, comp_wins


def _fmt(tmpl: str, **kwargs) -> str:
    """Format template safely — missing keys become blank."""
    class _D(dict):
        def __missing__(self, k): return ""
    return tmpl.format_map(_D(**kwargs))


def _build_comparison_brief(competitor: dict, angle: str, nonbank: dict, year: int = 2026) -> dict:
    t = COMPARISON_TEMPLATES[angle]
    comp_name = competitor["name"]
    comp_slug = _slug(comp_name)
    wins, losses = _competitor_gaps_vs_nonbank(competitor, nonbank)
    wins_list = ", ".join(w.split(":")[0].replace("*", "").strip() for w in wins[:5]) or "(see matrix)"
    losses_list = ", ".join(l.split(":")[0].replace("*", "").strip() for l in losses[:5]) or "(none significant)"

    ctx = {
        "competitor": comp_name, "comp_slug": comp_slug, "year": year,
        "wins_list": wins_list, "losses_list": losses_list,
        "category": "non-custodial crypto card", "category_slug": "non-custodial-crypto-card",
    }
    return {
        "Type": "Comparison",
        "Angle": t["label"],
        "Title": _fmt(t["title_tmpl"], **ctx),
        "Primary Keyword": _fmt(t["kw_tmpl"], **ctx),
        "Slug": _fmt(t["slug_tmpl"], **ctx),
        "Intent": t["intent"],
        "Words": t["words"],
        "Outline Full": [_fmt(o, **ctx) for o in t["outline"]],
        "Wins Detail": wins,
        "Losses Detail": losses,
        "Source": f"vs {comp_name}",
    }


def _build_differentiator_brief(pillar: dict, angle: str, year: int = 2026) -> dict:
    t = DIFFERENTIATOR_TEMPLATES[angle]
    diff_id = pillar["id"]
    diff_label = pillar["label"]
    diff_seed_kw = pillar["seed_keywords"][0] if pillar.get("seed_keywords") else diff_label.lower()

    # Action phrase from pillar description
    diff_action = pillar["description"].split(".")[0].split(" — ")[0][:60]

    ctx = {
        "diff_id": diff_id, "diff_label": diff_label, "diff_seed_kw": diff_seed_kw,
        "diff_action": diff_action, "year": year,
        "category": "crypto wallets", "category_slug": "crypto-wallets",
    }
    return {
        "Type": "Differentiator",
        "Angle": t["label"],
        "Title": _fmt(t["title_tmpl"], **ctx),
        "Primary Keyword": _fmt(t["kw_tmpl"], **ctx),
        "Slug": _fmt(t["slug_tmpl"], **ctx),
        "Intent": t["intent"],
        "Words": t["words"],
        "Outline Full": [_fmt(o, **ctx) for o in t["outline"]],
        "Wins Detail": [f"**Pillar priority:** {pillar.get('priority', 'Medium')}"],
        "Losses Detail": [],
        "Source": f"pillar: {diff_label}",
    }


def _build_persona_brief(persona: dict, year: int = 2026) -> dict:
    t = USE_CASE_TEMPLATES["persona"]
    ctx = {
        "persona": persona["label"], "persona_slug": persona["slug"],
        "year": year, "category": "crypto wallet",
    }
    return {
        "Type": "Use Case",
        "Angle": t["label"],
        "Title": _fmt(t["title_tmpl"], **ctx),
        "Primary Keyword": _fmt(t["kw_tmpl"], **ctx),
        "Slug": _fmt(t["slug_tmpl"], **ctx),
        "Intent": t["intent"],
        "Words": t["words"],
        "Outline Full": [_fmt(o, **ctx) for o in t["outline"]],
        "Wins Detail": [],
        "Losses Detail": [],
        "Source": f"persona: {persona['label']}",
    }


def _build_problem_brief(problem: dict, year: int = 2026) -> dict:
    t = USE_CASE_TEMPLATES["problem_solution"]
    ctx = {
        "problem_action": problem["action"], "problem_slug": problem["slug"],
        "year": year,
    }
    return {
        "Type": "How-To",
        "Angle": t["label"],
        "Title": _fmt(t["title_tmpl"], **ctx),
        "Primary Keyword": _fmt(t["kw_tmpl"], **ctx),
        "Slug": _fmt(t["slug_tmpl"], **ctx),
        "Intent": t["intent"],
        "Words": t["words"],
        "Outline Full": [_fmt(o, **ctx) for o in t["outline"]],
        "Wins Detail": [],
        "Losses Detail": [],
        "Source": f"problem: {problem['action']}",
    }


def _build_roundup_brief(category: dict, competitors_list: list[dict], year: int = 2026) -> dict:
    t = COMPARISON_TEMPLATES["roundup"]
    ctx = {
        "category": category["label"], "category_slug": category["slug"],
        "year": year,
    }
    return {
        "Type": "Roundup",
        "Angle": t["label"],
        "Title": _fmt(t["title_tmpl"], **ctx),
        "Primary Keyword": _fmt(t["kw_tmpl"], **ctx),
        "Slug": _fmt(t["slug_tmpl"], **ctx),
        "Intent": t["intent"],
        "Words": t["words"],
        "Outline Full": [_fmt(o, **ctx) for o in t["outline"]],
        "Wins Detail": [f"**Competitors included:** " + ", ".join(c["name"] for c in competitors_list[:5])],
        "Losses Detail": [],
        "Source": f"category: {category['label']}",
    }


# ══════════════════════════════════════════════════════════════════════════
# MAIN PAGE
# ══════════════════════════════════════════════════════════════════════════

def page_programmatic_seo():
    st.title("🚀 Content Brief Factory")
    st.caption("Generate high-intent content briefs across comparisons, differentiators, use cases, and how-tos")

    st.info(
        "**Research-first flow:** Every brief is grounded in validated data — "
        "CONTENT_PILLARS (from keyword/AI research), COMPETITORS feature matrix, "
        "and PRODUCT_PROFILE differentiators. No hallucinated topics. "
        "Output pushes directly into your Content Plan calendar."
    )

    nonbank = next((c for c in COMPETITORS if c.get("is_self")), None)
    competitors = [c for c in COMPETITORS if not c.get("is_self")]
    if not nonbank:
        st.error("No self-marked competitor row in config.py COMPETITORS")
        return

    tab_generate, tab_preview, tab_export = st.tabs([
        "1️⃣ Generate Briefs", "2️⃣ Preview & Refine", "3️⃣ Export"
    ])

    # ── TAB 1: GENERATE ───────────────────────────────────────────────
    with tab_generate:
        st.subheader("What to generate")
        st.caption("Mix and match — each section below produces briefs from a different angle.")

        # ── Comparisons ──────────────────────────────────────────
        with st.expander("🥊 Competitor Comparisons", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                cmp_selected_comps = st.multiselect(
                    "Competitors", options=[c["name"] for c in competitors],
                    default=[c["name"] for c in competitors[:4]],
                    key="cmp_comps",
                )
            with col2:
                cmp_angles = st.multiselect(
                    "Comparison angles",
                    options=["versus", "alternative"],
                    default=["versus", "alternative"],
                    format_func=lambda a: COMPARISON_TEMPLATES[a]["label"],
                    key="cmp_angles",
                )
            st.caption(f"→ **{len(cmp_selected_comps) * len(cmp_angles)}** comparison briefs")

        # ── Roundups ─────────────────────────────────────────────
        with st.expander("🏆 Category Roundups", expanded=True):
            rnd_categories = st.multiselect(
                "Categories",
                options=[c["slug"] for c in ROUNDUP_CATEGORIES],
                default=[ROUNDUP_CATEGORIES[0]["slug"], ROUNDUP_CATEGORIES[1]["slug"]],
                format_func=lambda s: next(c["label"] for c in ROUNDUP_CATEGORIES if c["slug"] == s),
                key="rnd_cats",
            )
            st.caption(f"→ **{len(rnd_categories)}** roundup briefs (each includes Nonbank + top 4 competitors)")

        # ── Differentiators ──────────────────────────────────────
        with st.expander("💎 Differentiator Deep-Dives", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                diff_pillars = st.multiselect(
                    "Pillars (from Content Pillars)",
                    options=[p["id"] for p in CONTENT_PILLARS],
                    default=[p["id"] for p in CONTENT_PILLARS if p.get("priority", "").startswith(("P0", "P1", "P2"))],
                    format_func=lambda pid: next(p["label"] for p in CONTENT_PILLARS if p["id"] == pid),
                    key="diff_pillars",
                )
            with col2:
                diff_angles = st.multiselect(
                    "Angles",
                    options=["deep_dive", "why_matters"],
                    default=["deep_dive"],
                    format_func=lambda a: DIFFERENTIATOR_TEMPLATES[a]["label"],
                    key="diff_angles",
                )
            st.caption(f"→ **{len(diff_pillars) * len(diff_angles)}** differentiator briefs")

        # ── Personas ─────────────────────────────────────────────
        with st.expander("👥 User Persona Articles", expanded=False):
            persona_selected = st.multiselect(
                "Personas",
                options=[p["slug"] for p in PERSONAS],
                default=[PERSONAS[0]["slug"], PERSONAS[1]["slug"], PERSONAS[2]["slug"]],
                format_func=lambda s: next(p["label"] for p in PERSONAS if p["slug"] == s),
                key="persona_sel",
            )
            st.caption(f"→ **{len(persona_selected)}** persona briefs")

        # ── Problems / How-To ────────────────────────────────────
        with st.expander("🔧 How-To / Problem-Solution", expanded=False):
            problem_selected = st.multiselect(
                "Problems to address",
                options=[p["slug"] for p in PROBLEMS],
                default=[p["slug"] for p in PROBLEMS[:3]],
                format_func=lambda s: next(p["action"] for p in PROBLEMS if p["slug"] == s),
                key="problem_sel",
            )
            st.caption(f"→ **{len(problem_selected)}** how-to briefs")

        # ── Totals ───────────────────────────────────────────────
        st.divider()
        total = (
            len(cmp_selected_comps) * len(cmp_angles)
            + len(rnd_categories)
            + len(diff_pillars) * len(diff_angles)
            + len(persona_selected)
            + len(problem_selected)
        )
        st.metric("Total briefs to generate", total)

        if st.button("🔧 Generate All Briefs", type="primary", disabled=total == 0):
            briefs = []
            # Comparisons
            for comp_name in cmp_selected_comps:
                comp = next((c for c in competitors if c["name"] == comp_name), None)
                if not comp: continue
                for angle in cmp_angles:
                    briefs.append(_build_comparison_brief(comp, angle, nonbank))
            # Roundups
            for cat_slug in rnd_categories:
                cat = next((c for c in ROUNDUP_CATEGORIES if c["slug"] == cat_slug), None)
                if cat:
                    briefs.append(_build_roundup_brief(cat, competitors))
            # Differentiators
            for pid in diff_pillars:
                pillar = next((p for p in CONTENT_PILLARS if p["id"] == pid), None)
                if not pillar: continue
                for angle in diff_angles:
                    briefs.append(_build_differentiator_brief(pillar, angle))
            # Personas
            for pslug in persona_selected:
                persona = next((p for p in PERSONAS if p["slug"] == pslug), None)
                if persona:
                    briefs.append(_build_persona_brief(persona))
            # Problems
            for pslug in problem_selected:
                problem = next((p for p in PROBLEMS if p["slug"] == pslug), None)
                if problem:
                    briefs.append(_build_problem_brief(problem))

            st.session_state["content_briefs"] = briefs
            st.success(f"Generated {len(briefs)} briefs across {len(set(b['Type'] for b in briefs))} content types")

    # ── TAB 2: PREVIEW ────────────────────────────────────────────────
    with tab_preview:
        briefs = st.session_state.get("content_briefs", [])
        if not briefs:
            st.info("Generate briefs first in Tab 1.")
        else:
            # Type summary
            types_count = {}
            for b in briefs:
                types_count[b["Type"]] = types_count.get(b["Type"], 0) + 1

            mcols = st.columns(len(types_count))
            for i, (typ, cnt) in enumerate(sorted(types_count.items())):
                mcols[i].metric(typ, cnt)

            # Filter
            type_filter = st.multiselect(
                "Filter by type", options=sorted(types_count.keys()),
                default=sorted(types_count.keys()),
            )
            filtered = [b for b in briefs if b["Type"] in type_filter]

            # Summary table
            summary_rows = [
                {
                    "Type": b["Type"],
                    "Angle": b["Angle"],
                    "Title": b["Title"],
                    "Keyword": b["Primary Keyword"],
                    "Intent": b["Intent"],
                    "Words": b["Words"],
                    "Source": b["Source"],
                }
                for b in filtered
            ]
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True, height=400)

            # Detail view
            st.subheader("Brief Detail")
            idx = st.selectbox(
                "Select brief",
                range(len(filtered)),
                format_func=lambda i: f"[{filtered[i]['Type']}] {filtered[i]['Title']}",
            )
            sel = filtered[idx]

            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"### {sel['Title']}")
                st.markdown(
                    f"**Type:** {sel['Type']} — {sel['Angle']}  \n"
                    f"**Slug:** `{sel['Slug']}`  \n"
                    f"**Keyword:** `{sel['Primary Keyword']}`  \n"
                    f"**Intent:** {sel['Intent']}  \n"
                    f"**Target words:** {sel['Words']}"
                )
                st.markdown("**Outline:**")
                for i, item in enumerate(sel["Outline Full"], 1):
                    st.markdown(f"{i}. {item}")
            with c2:
                if sel["Wins Detail"]:
                    st.markdown("**✅ Nonbank advantages:**")
                    for w in sel["Wins Detail"]:
                        st.markdown(f"- {w}")
                if sel["Losses Detail"]:
                    st.markdown("**⚠️ Trade-offs:**")
                    for l in sel["Losses Detail"]:
                        st.markdown(f"- {l}")

            # Full article generation
            st.divider()
            st.subheader("Expand to Full Article (optional)")
            api_key = st.session_state.get("anthropic_token")

            if not api_key:
                st.caption("Add Anthropic key in sidebar to enable full-article generation.")
            else:
                if st.button(f"✍️ Generate full article"):
                    from llm_client import _call_with_retry, _client
                    system = (
                        f"You are a senior SEO/GEO content writer for Nonbank (nonbank.io) — "
                        f"{PRODUCT_PROFILE['description']}\n\n"
                        "Write a detailed article that follows the outline exactly. Include a "
                        "comparison table (markdown) where relevant, FAQ section (5-7 Qs), "
                        "3-5 data-dense stat paragraphs AI engines can cite, and clear "
                        "recommendations. Target the word count specified. Return clean markdown."
                    )
                    wins_block = ""
                    if sel["Wins Detail"]:
                        wins_block = "Nonbank advantages:\n" + "\n".join(f"- {w}" for w in sel["Wins Detail"]) + "\n\n"
                    losses_block = ""
                    if sel["Losses Detail"]:
                        losses_block = "Trade-offs (be honest):\n" + "\n".join(f"- {l}" for l in sel["Losses Detail"]) + "\n\n"

                    user_msg = (
                        f"Article brief:\n"
                        f"Title: {sel['Title']}\n"
                        f"Type: {sel['Type']} — {sel['Angle']}\n"
                        f"Primary keyword: {sel['Primary Keyword']}\n"
                        f"Intent: {sel['Intent']}\n"
                        f"Target words: {sel['Words']}\n\n"
                        f"Outline:\n" + "\n".join(f"- {o}" for o in sel["Outline Full"]) + "\n\n"
                        + wins_block + losses_block +
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
                            st.session_state[f"_article_{sel['Slug']}"] = resp.content[0].text
                    except Exception as e:
                        st.error(f"Generation failed: {e}")

                article = st.session_state.get(f"_article_{sel['Slug']}")
                if article:
                    st.markdown("### Generated Article")
                    st.markdown(article)
                    st.download_button(
                        "⬇️ Download as Markdown",
                        article.encode("utf-8"),
                        file_name=f"{_slug(sel['Title'])}.md",
                        mime="text/markdown",
                    )

    # ── TAB 3: EXPORT ─────────────────────────────────────────────────
    with tab_export:
        briefs = st.session_state.get("content_briefs", [])
        if not briefs:
            st.info("Generate briefs first in Tab 1.")
        else:
            st.subheader(f"Export {len(briefs)} Briefs")

            export_rows = [
                {
                    "Type": b["Type"],
                    "Angle": b["Angle"],
                    "Title": b["Title"],
                    "Slug": b["Slug"],
                    "Primary Keyword": b["Primary Keyword"],
                    "Intent": b["Intent"],
                    "Words": b["Words"],
                    "Source": b["Source"],
                    "Outline": " · ".join(b["Outline Full"]),
                    "Nonbank Advantages": " | ".join(b["Wins Detail"]),
                    "Trade-offs": " | ".join(b["Losses Detail"]),
                }
                for b in briefs
            ]
            df_export = pd.DataFrame(export_rows)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "⬇️ CSV",
                    df_export.to_csv(index=False).encode("utf-8"),
                    file_name=f"nonbank_briefs_{date.today().isoformat()}.csv",
                    mime="text/csv",
                )
            with col2:
                st.download_button(
                    "⬇️ JSON",
                    json.dumps(export_rows, indent=2).encode("utf-8"),
                    file_name=f"nonbank_briefs_{date.today().isoformat()}.json",
                    mime="application/json",
                )

            st.divider()
            st.markdown("### Push to Content Plan")
            st.caption(
                "Add these briefs as tasks in the **Content Strategy → Publication Calendar**. "
                "Each brief becomes a row you can assign to an outlet and week."
            )
            if st.button("➕ Add all briefs to Content Plan", type="primary"):
                current_plan = st.session_state.get("content_plan", [])
                for b in briefs:
                    current_plan.append({
                        "Task": b["Title"],
                        "Type": f"SEO+GEO ({b['Type']})",
                        "Market": "🌍 Global",
                        "Outlet Options": "",
                        "Price": "",
                        "GEO": f"{b['Angle']} · {b['Words']} words · {b['Intent']}",
                        "Week": "",
                        "Status": "To Do",
                        "Publication URL": "",
                        "Reddit/Quora URL": "",
                    })
                st.session_state["content_plan"] = current_plan
                st.success(
                    f"Added {len(briefs)} briefs to Content Plan. "
                    f"Go to **Content Strategy → Publication Calendar** to review."
                )
