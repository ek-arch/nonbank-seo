"""Page 0 — Dashboard: weekly action checklist and quick start guide."""
from __future__ import annotations

import streamlit as st


def page_dashboard():
    st.title("🤖 Nonbank SEO & GEO Intelligence Agent")
    st.markdown("**nonbank.io · non-custodial wallet + Visa card + unified portfolio**")

    st.info(
        "Starter workspace — no legacy performance data. Build SEO, GEO (AI visibility), "
        "and social distribution from scratch as real results come in."
    )

    st.divider()

    # ── Weekly Actions ──────────────────────────────────────────
    st.subheader("🎯 This Week's Actions")

    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(border=True):
            st.markdown("### 📣 Social Distribution")
            st.markdown("""
- [ ] Search Reddit for "non-custodial crypto card" threads → draft 3 comments
- [ ] Answer Quora questions ("self custody crypto spend", "MetaMask Card alternative")
- [ ] Comment on r/ledgerwallet / r/TREZOR hardware-wallet+card threads
- [ ] Post in r/CryptoCards / r/ethfinance / r/defi when relevant
- [ ] Monitor r/cryptocurrency for new non-custodial card questions daily
""")
        with st.container(border=True):
            st.markdown("### 🤖 GEO Optimization")
            st.markdown("""
- [ ] Test 10 AI queries (ChatGPT, Perplexity, Google AI) — log Nonbank mentions
- [ ] Add FAQ section to every published article
- [ ] Add comparison tables (Nonbank vs MetaMask Card vs Gnosis Pay)
- [ ] Create stat-dense paragraphs AI engines can cite
- [ ] Submit articles to sources AI engines crawl (Reddit, Quora, Wikipedia refs)
""")

    with col_b:
        with st.container(border=True):
            st.markdown("### ✍️ Content & PR")
            st.markdown("""
- [ ] Draft EN pillar article: "Best Non-Custodial Crypto Card 2026"
- [ ] Translate to ES, PT, TR for LATAM / Turkey pillars
- [ ] Publish via vetted outlets (see Outlet Matching)
- [ ] Add UTM params to every publication link
- [ ] Use AI Revise to add question headers + quotable stats
""")
        with st.container(border=True):
            st.markdown("### 📊 Track & Measure")
            st.markdown("""
- [ ] Log all published article URLs in Track Publications
- [ ] Check referral traffic from published articles (GA4)
- [ ] Track Reddit comment karma / engagement
- [ ] Record which AI queries show Nonbank in answers
- [ ] Monthly eval: compare ROI by channel (SEO vs GEO vs Social)
""")

    st.divider()

    # ── Quick Links ─────────────────────────────────────────────
    st.subheader("🚀 Quick Start")
    st.markdown("""
| Step | Where | What to do |
|---|---|---|
| 1 | **Content Plan** | Draft the month's briefs + pick target markets |
| 2 | **Outlet Matching** | Pick crypto/finance outlets by DR + price efficiency |
| 3 | **Publication ROI** | Sanity-check expected ROI per outlet before buying |
| 4 | **PR Generator** | Generate GEO-optimized article drafts |
| 5 | **Distribution** | Find Reddit/Quora threads → draft helpful replies |
| 6 | **GEO Tracker** | Monitor Nonbank mentions in AI answers |
| 7 | **Monthly Eval** | Log actuals → feed into next month's plan |
""")
