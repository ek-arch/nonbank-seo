# Architecture

Technical reference for the Nonbank SEO & GEO Intelligence Agent.

---

## High-level data flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  config.py — single source of truth                                 │
│  ──────────────────────────────────                                 │
│  PRODUCT_PROFILE, COMPETITORS, FEATURE_DIMENSIONS, CONTENT_PILLARS  │
│  BRIEFS, PLAN_DEFAULT, NONBANK_DOMAINS, COMPETITOR_BRANDS           │
└────────────┬─────────────────────────────────────────┬──────────────┘
             │                                         │
             ▼                                         ▼
┌──────────────────────────┐          ┌────────────────────────────┐
│  Engine modules (pure)   │          │  Streamlit pages (UI)      │
│  ──────────────────────  │          │  ─────────────────────     │
│  keyword_research.py     │──────────▶ pages/keyword_intel.py     │
│  perplexity_geo.py       │──────────▶ pages/competitor_intel.py  │
│  geo_visibility.py       │──────────▶ pages/geo_tracker.py       │
│  geo_prompt_research.py  │──────────▶ pages/geo_tracker.py       │
│  llm_client.py           │──────────▶ pages/pr_generator.py      │
│  sheets_client.py        │──────────▶ pages/content_plan.py      │
│  publication_roi.py      │──────────▶ pages/pub_roi.py           │
│  monthly_cycle.py        │──────────▶ pages/monthly_*.py         │
│  collaborator_outlets.py │──────────▶ pages/outlet_matching.py   │
└──────────────────────────┘          └────────────────────────────┘
             │                                         │
             └─────────────────┬───────────────────────┘
                               ▼
                  ┌──────────────────────────┐
                  │  External APIs           │
                  │  ─────────────           │
                  │  • Anthropic Claude      │
                  │  • Perplexity (sonar)    │
                  │  • SerpAPI               │
                  │  • Google Autocomplete   │
                  │  • Google Sheets         │
                  └──────────────────────────┘
```

---

## User workflow (how pages chain together)

```
┌─── PHASE 1: RESEARCH ────────────────────────────────────────┐
│                                                              │
│  Dashboard  ──▶  see product profile + tech audit + actions │
│      │                                                       │
│      ▼                                                       │
│  Competitor Intel  ──▶  feature matrix, AI audit, gaps      │
│      │                                                       │
│      ▼                                                       │
│  Keyword Intel  ──▶  generate matrix, validate, score       │
│      │                                                       │
└──────┼───────────────────────────────────────────────────────┘
       ▼
┌─── PHASE 2: STRATEGY ────────────────────────────────────────┐
│                                                              │
│  Content Strategy  ──▶  define pillars, draft briefs        │
│      │                                                       │
│      ▼                                                       │
│  Outlet Matching  ──▶  search Collaborator, shortlist       │
│      │                                                       │
│      ▼                                                       │
│  Publication ROI  ──▶  sanity-check expected ROI            │
│      │                                                       │
└──────┼───────────────────────────────────────────────────────┘
       ▼
┌─── PHASE 3: EXECUTION ───────────────────────────────────────┐
│                                                              │
│  Content Brief Factory  ──▶  generate 35+ briefs at scale   │
│      │                                                       │
│      ▼                                                       │
│  PR Generator  ──▶  write articles via Claude               │
│      │                                                       │
│      ▼                                                       │
│  Distribution  ──▶  find Reddit/Quora threads, draft posts  │
│      │                                                       │
└──────┼───────────────────────────────────────────────────────┘
       ▼
┌─── PHASE 4: MEASURE ─────────────────────────────────────────┐
│                                                              │
│  GEO Tracker  ──▶  monitor AI mentions weekly               │
│      │                                                       │
│      ▼                                                       │
│  Monthly Eval  ──▶  log actual results                      │
│      │                                                       │
│      ▼                                                       │
│  Monthly Planner  ──▶  Claude recommends next month         │
│      │                                                       │
│      └──▶ feeds back into Content Strategy                  │
└──────────────────────────────────────────────────────────────┘
```

---

## Core data structures (`config.py`)

### `PRODUCT_PROFILE`
Nonbank's product description, differentiators (gasless, AML, hybrid card, proxy/watch, NON ID), chains, platforms, social, fees, SEO baseline.

### `COMPETITORS`
List of dicts, one per competitor. Each dict has values for every dimension in `FEATURE_DIMENSIONS`. Exactly one row has `"is_self": True` (Nonbank).

```python
{
    "name": "Gnosis Pay",
    "is_self": False,
    "Custody Model": "Fully on-chain (Safe smart account — card spends from chain)",
    "Card Network": "Visa",
    # ... 15 dimensions total
}
```

### `FEATURE_DIMENSIONS`
Ordered list of 15 comparison dimensions (Custody Model, Card Network, Card Status, Supported Chains, Gasless Fees, Built-in AML, Multi-Account, DeFi Identity, Cashback, KYC, Mobile App, Hardware Wallet, Key Regions, Pricing, Unique Angle).

### `CONTENT_PILLARS`
5 pillars with priority tags (`P0–P4`) and SERP research notes:

1. **Gasless Crypto Transactions** — P0
2. **Watch Wallets & Proxy Addresses** — P1
3. **DeFi Wallet with Integrated Card** — P2
4. **AML-Safe DeFi Wallet** — P3 (PR only)
5. **NON ID (DeFi Identity)** — P4 (feature mention only)

### `BRIEFS`
12 starter article briefs across the 5 pillars. All EN-global.

### `PLAN_DEFAULT`
Starter publication calendar tasks (EN-only).

### Brand constants (centralized)
- `NONBANK_DOMAINS = {"nonbank.io", "www.nonbank.io", "t.me/nonbankers"}`
- `NONBANK_BRAND_TERMS` — 9 variants for text matching
- `COMPETITOR_BRANDS` — dict of 12 competitor → domain+term sets
- `COMPETITOR_DOMAINS_FLAT` — flat list for Ahrefs/SerpAPI

---

## Engine modules (pure Python, no Streamlit)

### `llm_client.py`
Single wrapper for all Anthropic Claude calls. Model constants:

```python
model="claude-sonnet-4-6"            # default for generation
model="claude-haiku-4-5-20251001"    # fast model for discovery/classification
```

Functions:
- `generate_press_release()` — GEO-optimized article drafts
- `revise_press_release()` — improvement pass
- `translate_press_release()` — multi-language (mostly unused in EN-only mode)
- `generate_comment_reply()` — Reddit/Quora/X replies
- `recommend_monthly_plan()` — Monthly Planner

### `keyword_research.py`
Nonbank-focused keyword matrix. Key constants:

- `PRODUCTS` — 8 Nonbank product terms
- `COMPETITOR_BRANDS_KW` — 7 competitor names
- `PERSONAS_KW` — 8 user personas
- `FEATURES_KW` — 7 differentiator features
- `PROBLEM_ACTIONS` — 8 user problems
- `INTENT_MODIFIERS` — 6 intent categories (transactional, comparison, persona, feature, problem_solution, long_tail)

Core function: `generate_keyword_matrix()` — product × (competitor | persona | feature | problem | intent). Returns ~237 keywords, all `lang='en'` / `market='global'`.

Supporting: `build_taxonomy()`, `score_keyword()`, `get_google_autocomplete()`, `expand_with_autocomplete()`.

### `perplexity_geo.py`
Perplexity AI visibility audit. Imports `NONBANK_DOMAINS`, `NONBANK_BRAND_TERMS`, `COMPETITOR_BRANDS` from `config.py` (single source of truth).

- `GEO_MARKETS = {"GLOBAL": ...}` — just one market (Nonbank is borderless)
- `DEFAULT_GEO_PROMPTS` — seed prompts
- `query_perplexity()`, `audit_prompt()`, `run_geo_audit()`, `summarize_geo_audit()`

### `geo_visibility.py`
SerpAPI Google SERP + AI overview detection. Imports the same shared constants. Key function: `audit_query()` — returns dict with `nonbank_visible`, `nonbank_position`, `ai_overview`, competitors found, featured snippets.

### `geo_prompt_research.py`
Claude-powered AI prompt discovery. Structure:

- `DISCOVERY_CATEGORIES` — 8 Nonbank-specific categories (hybrid_defi_card, gasless, aml_compliance, watch_proxy, gnosis_pay_alt, custodial_vs_defi, how_to, use_case)
- `TARGET_MARKETS = {"Global": ...}` — single global market
- `BUILTIN_PROMPTS` — 43 pre-built prompts, all Nonbank-focused
- `DISCOVERY_SYSTEM_PROMPT` — tells Claude about Nonbank's 5 differentiators, explicitly forbids Kolo-era generic prompts
- `discover_prompts_claude()`, `monitor_prompts_batch()`, `find_opportunities()`

### `publication_roi.py`
4-layer ROI model:

1. Direct referral traffic (UTM-trackable)
2. SEO compound traffic (backlink → ranking lift, 90-day window)
3. GEO / AI citation traffic
4. Revenue = visits × conversion × LTV

Placeholder LTVs (no Nonbank cohort data yet):

```python
LTV_BY_LANG = {"en": 3000, "es": 2500, "pt": 2000, "tr": 2000}
CONVERSION_RATE_BY_LANG = {"en": 0.0040, ...}
```

Main function: `calculate_publication_roi()` returns conservative / mid / optimistic scenarios.

### `sheets_client.py`
Google Sheets persistence. Hardcoded sheet ID: `1EoXaNgpF9Rg4Q-KksFL9d5k5ScDtAF0m7qbg4JxHW4k` (from Kolo era; should be replaced with a Nonbank-owned sheet).

Functions: `load_content_plan()`, `save_content_plan()`, `push_comments()`.

### `monthly_cycle.py`
Monthly Eval → Monthly Planner bridge. Dataclasses:

- `MonthlyEvaluation` — one month of actuals
- `MonthlyPlan` — next month recommendation

Functions: `generate_plan_inputs()`, `parse_plan_recommendation()`, `plan_to_notion_entries()` (legacy, now exports to CSV instead).

### `collaborator_outlets.py`
Scraped Collaborator.pro catalog. Key structures:

- `RAW_OUTLETS` — dict keyed by language (en/ru/it/es/pl/pt/id/ro) → list of outlet tuples
- `LANG_LABELS` — display labels
- `SCORE_LABEL` — 0-15 scoring verdict

Core functions: `get_outlets()`, `get_top_outlets_all_langs()`, `score_label()`.

### `data_sources.py`
Legacy data container (`DATA` dict). Most keys empty by design:

- `platform`, `pnl`, `countries`, `languages`, `acquisition_funnel`, `content_locale_map`, `product_features` — all empty (no Nonbank cohort data yet)
- `card_allowance` — **important**: Kolo issuer country list (EU, APAC, LATAM, Central Asia, Middle East; excludes TUR/ISR/CHN/IND/US)
- `march_outlets` — empty dict (outlet shortlist is built in Outlet Matching page session state)
- `cashback_unit_economics`, `seo_forecast` — zeroed

Also contains `score_outlet_notion()`, `outlet_verdict()`, `can_issue_card()`.

---

## Page-level architecture (`pages/`)

Every page is a single function `page_<name>()` that Streamlit's `st.navigation()` dispatches to.

### `pages/dashboard.py` (~170 lines)
Read-only product profile + competitor snapshot + technical SEO audit metrics + phased actions + quick start table. No external API calls.

### `pages/competitor_intel.py` (~250 lines)
4 tabs: Feature Matrix (editable), Keyword Spy (SerpAPI), AI Visibility Audit (Perplexity), Gap Analysis.

### `pages/keyword_intel.py` (~450 lines)
3 tabs: Taxonomy Builder (Ahrefs stub), Discovery Pipeline (5-step), AI Audit by Market. Auto-clears stale Kolo-era session state on load.

### `pages/content_plan.py` (~280 lines)
3 tabs: Content Pillars (from `CONTENT_PILLARS`), Article Briefs (editable + Claude brief generator), Publication Calendar (Google Sheets sync).

### `pages/outlet_matching.py` (~190 lines)
2 tabs: Search Catalog (Collaborator.pro, filter by DR/price/score/crypto), My Shortlist (assign to pillars, export CSV). No legacy pre-selected outlets.

### `pages/pub_roi.py` (~260 lines)
3 tabs: March 2026 Portfolio (legacy, mostly empty now), Single-Outlet Calculator, LTV Benchmark.

### `pages/pr_generator.py` (~200 lines)
Generate PR drafts via Claude, revise, translate, track published articles.

### `pages/distribution.py` (~350 lines)
Find Reddit/Quora/Twitter threads via SerpAPI, cache them, draft comments via Claude, push to Google Sheets tracker.

### `pages/pseo.py` — Content Brief Factory (~500 lines)
3 tabs: Generate Briefs (5 types × config-driven options), Preview & Refine (full article generation), Export (CSV/JSON + push to Content Plan session state).

Brief types:
1. Competitor Comparisons (versus / alternative)
2. Category Roundups
3. Differentiator Deep-Dives (pillar-driven)
4. User Persona Articles
5. Problem → Solution How-Tos

### `pages/geo_tracker.py` (~280 lines)
4 tabs: Discover Prompts (Claude or built-in), Monitor (Perplexity), Results & Opportunities, History. Auto-clears stale session state.

### `pages/monthly_eval.py` (~200 lines)
Log last month's actual revenue, registrations, costs per publication.

### `pages/monthly_planner.py` (~220 lines)
Claude generates next month's plan from last month's eval. Export as CSV.

---

## Session state keys

Keys used across pages (for debugging / manual state reset):

| Key | Set by | Shape |
|-----|--------|-------|
| `anthropic_token` | Sidebar (auto from secrets) | string |
| `perplexity_key` | Sidebar | string |
| `serpapi_key` | Sidebar | string |
| `gsheets_json` | Sidebar | JSON string |
| `content_plan` | Content Plan, pseo | list of dicts (publication calendar) |
| `briefs` | Content Plan | list of article briefs |
| `outlet_shortlist` | Outlet Matching | list of dicts |
| `pipe_candidates` | Keyword Intel | list of `Keyword` dataclass |
| `pipe_selected`, `pipe_ac_results`, `pipe_ai_results` | Keyword Intel | list |
| `geo_prompts` | GEO Tracker | list of dicts |
| `geo_results` | GEO Tracker | list of `PromptResult` |
| `content_briefs` | Content Brief Factory | list of brief dicts |
| `publications` | PR Generator | list of published URLs |
| `fetched_posts`, `comment_queue` | Distribution | list of dicts |
| `plan_parsed`, `plan_raw` | Monthly Planner | `MonthlyPlan` / string |
| `eval_report_<month>` | Monthly Eval | `MonthlyEvaluation` |

---

## Testing

No formal test suite. Smoke tests are run manually via import checks:

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from pages.dashboard import page_dashboard
from pages.competitor_intel import page_competitor_intel
# ... all 12 pages
print('OK')
"
```

Compile check:

```bash
python3 -c "
import py_compile, pathlib
for p in pathlib.Path('.').rglob('*.py'):
    if '.git' in str(p): continue
    py_compile.compile(str(p), doraise=True)
print('OK')
"
```

Integration testing happens in Streamlit Cloud — push to `main`, wait ~30s, test the deployed app.
