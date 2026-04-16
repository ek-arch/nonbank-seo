# Nonbank SEO & GEO Intelligence Agent

A Streamlit app for running **research-first SEO and GEO** (Generative Engine Optimization) for [Nonbank](https://nonbank.io) — a DeFi wallet with an integrated custodial Visa card (hybrid model, Kolo issuer under the hood, 100+ countries).

**Live app:** https://nonbank-seo.streamlit.app
**Repo:** https://github.com/ek-arch/nonbank-seo

---

## What this does

The app supports a **research → strategy → execution → measure** workflow:

1. **Research** — audit competitors, find keyword gaps, check AI visibility
2. **Strategy** — pick content pillars, shortlist outlets, sanity-check ROI
3. **Execution** — generate articles, draft social comments, build content briefs at scale
4. **Measure** — monitor AI mentions, track rankings, evaluate monthly ROI

Nonbank's 3 key differentiators drive every pillar:

1. **Gasless fees** — send crypto without native gas tokens
2. **Built-in AML Watchtower** — blocks transfers from sanctioned wallets
3. **Hybrid DeFi wallet + card** — self-custody keys, card in the same app, 100+ countries

---

## Quick start

### 1. Clone

```bash
git clone https://github.com/ek-arch/nonbank-seo.git
cd nonbank-seo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Requires Python 3.11+. Uses Streamlit 1.32+.

### 3. Configure secrets

Copy the example and fill in your keys:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and add:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
PERPLEXITY_KEY    = "pplx-..."
SERPAPI_KEY       = "..."

[gsheets]
# Google service account JSON for Google Sheets persistence (optional)
type = "service_account"
project_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
# ...etc
```

See [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) for the full schema.

### 4. Run locally

```bash
streamlit run app.py
```

Opens at http://localhost:8501.

---

## App tabs

The app is organized into 4 phases:

### 🔍 Research
| Tab | Purpose |
|---|---|
| **Dashboard** | Product profile, competitor snapshot, technical SEO audit, phased actions |
| **Competitor Intel** | Feature comparison matrix (Nonbank vs Gnosis Pay, MetaMask, COCA, Bleap, etc.), SerpAPI competitor keyword spy, Perplexity AI visibility audit, gap analysis |
| **Keyword Intel** | Generate Nonbank-focused keyword matrix (237 keywords), Google Autocomplete validation, Perplexity AI visibility check |

### 📋 Strategy
| Tab | Purpose |
|---|---|
| **Content Strategy** | Content pillars (gasless, AML, hybrid card, watch wallets, NON ID), editable briefs, publication calendar (Google Sheets sync) |
| **Outlet Matching** | Search 70+ Collaborator.pro outlets by DR/price/score, shortlist to pillars |
| **Publication ROI** | 4-layer ROI model (referral + SEO compound + GEO citation + revenue) |

### ✍️ Execution
| Tab | Purpose |
|---|---|
| **PR Generator** | Generate GEO-optimized article drafts via Claude, revise, translate |
| **Distribution** | Find Reddit/Quora threads via SerpAPI, draft natural comments via Claude |
| **Content Brief Factory** | Generate 35+ briefs across 5 types: competitor comparisons, category roundups, differentiator deep-dives, persona articles, problem-solution how-tos |

### 📊 Measure
| Tab | Purpose |
|---|---|
| **GEO Tracker** | Claude-powered prompt discovery, Perplexity AI monitoring, opportunity finder |
| **Monthly Eval** | Log actual performance, compare vs. projected ROI |
| **Monthly Planner** | Claude generates next month's plan based on last month's results |

---

## Architecture

### Top-level files

```
app.py                   # Streamlit entry point, st.navigation()
config.py                # Product profile, competitor matrix, content pillars, keyword seeds
data_sources.py          # Card allowance (Kolo issuer list), legacy data shell
collaborator_outlets.py  # Outlet catalog (70+ domains, DR, price, score)
requirements.txt         # Python dependencies
```

### Helper modules (pure Python, no Streamlit)

```
keyword_research.py      # Keyword matrix generator, scoring, Google Autocomplete
perplexity_geo.py        # Perplexity AI visibility audit
geo_visibility.py        # SerpAPI Google visibility tracking
geo_prompt_research.py   # Claude-powered prompt discovery for GEO
llm_client.py            # Anthropic Claude wrapper (all Claude calls)
sheets_client.py         # Google Sheets persistence
publication_roi.py       # 4-layer ROI model
monthly_cycle.py         # Monthly eval + planner logic
programmatic_seo.py      # Legacy keyword matrix (pattern-based)
seo_builder.py           # Legacy HTML page builder
seo_deploy.py            # Legacy deploy scaffolding
ahrefs_hook.py           # Ahrefs API stub
```

### Pages

```
pages/
  __init__.py
  dashboard.py           # Product profile + SEO audit
  competitor_intel.py    # Feature matrix + AI audit
  keyword_intel.py       # Taxonomy + discovery pipeline
  content_plan.py        # Pillars + briefs + calendar
  outlet_matching.py     # Outlet search + shortlist
  pub_roi.py             # ROI calculator
  pr_generator.py        # Article generation
  distribution.py        # Reddit/Quora shilling
  pseo.py                # Content Brief Factory
  geo_tracker.py         # AI visibility monitoring
  monthly_eval.py        # Monthly actuals
  monthly_planner.py     # Next-month planning
```

### Shared utilities

```
utils/
  __init__.py
  api_keys.py            # Sidebar API key management, auto-load from secrets
```

---

## External APIs

| API | Used by | Required? | Approx. cost |
|-----|---------|-----------|--------------|
| **Anthropic Claude** | PR Generator, Distribution, Content Plan (brief generator), Monthly Planner, GEO Tracker (prompt discovery), Content Brief Factory | **Critical** | ~$0.005/call (Sonnet 4-6), ~$0.002/call (Haiku 4-5) |
| **Perplexity AI** | Competitor Intel, Keyword Intel (AI audit), GEO Tracker (monitoring) | Optional — needed for GEO features | ~$0.005/query (sonar model) |
| **SerpAPI** | Competitor Intel (keyword spy), Keyword Intel (expansion), Distribution (thread discovery) | Optional — needed for SERP features | Free: 100/month, then paid |
| **Google Sheets** | Content Plan (save/load), Distribution (push tracker) | Optional — app works without it | Free |
| **Collaborator.pro** | Outlet Matching (live catalog) | Optional — uses scraped static catalog | Manual API activation required |
| **Ahrefs** | Keyword Intel (optional enhancement) | Optional | Paid subscription |

### Model names (Anthropic)

The org account uses these exact model strings — if you fork, confirm they're available to your key:

- `claude-sonnet-4-6` — main model (used in `llm_client.py`, most Claude calls)
- `claude-haiku-4-5-20251001` — fast model (`seo_builder.py`, `geo_prompt_research.py` prompt discovery)

If you get `404 model not found`, check available models:

```bash
curl https://api.anthropic.com/v1/models -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01"
```

---

## Deployment to Streamlit Cloud

The app auto-deploys to https://nonbank-seo.streamlit.app on every push to `main`.

### First-time setup

1. Fork/clone this repo to your GitHub account.
2. Go to https://share.streamlit.io → **Create app**.
3. Select:
   - **Repository:** `your-org/nonbank-seo`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** e.g. `nonbank-seo`
4. Click **Advanced settings → Secrets** and paste the contents of your `.streamlit/secrets.toml`.
5. Click **Deploy**. First build takes ~2 minutes.

### Updating secrets

In Streamlit Cloud: **Manage app → Settings → Secrets** → edit → save. Changes propagate in ~1 minute.

### Manual reboot

If a deploy gets stuck or cached state is weird: **Manage app → ⋮ → Reboot**.

---

## Development

### Local run with hot reload

```bash
streamlit run app.py
```

Streamlit auto-reloads on file save.

### Smoke-testing imports

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from pages.dashboard import page_dashboard
from pages.competitor_intel import page_competitor_intel
from pages.keyword_intel import page_keyword_intel
from pages.content_plan import page_content_plan
from pages.outlet_matching import page_outlet_matching
from pages.pub_roi import page_publication_roi
from pages.pr_generator import page_pr_generator
from pages.distribution import page_content_distribution
from pages.pseo import page_programmatic_seo
from pages.geo_tracker import page_geo_tracker
from pages.monthly_eval import page_monthly_eval
from pages.monthly_planner import page_monthly_planner
print('all pages OK')
"
```

### Compile-check all .py files

```bash
python3 -c "
import py_compile, pathlib
for p in pathlib.Path('.').rglob('*.py'):
    if '.git' in str(p): continue
    py_compile.compile(str(p), doraise=True)
print('all compile OK')
"
```

### Pushing to GitHub

```bash
git add -A
git commit -m "your message"
git push origin main
```

Streamlit Cloud picks up the push and redeploys automatically.

---

## Key design decisions

- **Research-first flow** — the app is explicitly designed to run competitor/keyword/AI research *before* picking content topics or outlets. Pages are ordered accordingly in the sidebar nav (Research → Strategy → Execution → Measure).
- **No legacy metrics** — unlike the Kolo ancestor, this app starts with **no internal Hex data**. Populate `DATA["countries"]`, `DATA["languages"]`, etc. in `data_sources.py` as real cohorts emerge.
- **Centralized brand constants** — `config.py` holds `NONBANK_DOMAINS`, `NONBANK_BRAND_TERMS`, `COMPETITOR_BRANDS` so all engine modules (`perplexity_geo.py`, `geo_visibility.py`, `geo_prompt_research.py`) share one source of truth.
- **EN-global only** — Nonbank is a borderless DeFi wallet, so all content is English. No country matrix, no localization pillars.
- **Card geography = Kolo** — the NON×CARD is Kolo's card under the hood, so `data_sources.py["card_allowance"]` mirrors Kolo's exact issuer list (EU, APAC, LATAM, Central Asia, Middle East; TUR/ISR/CHN/IND/US excluded).
- **All Claude calls isolated** — every Claude API call goes through `llm_client.py`. Model names are constants at the top. One place to swap models.
- **Session state hygiene** — `Keyword Intel` and `GEO Tracker` pages auto-clear stale Kolo-era session state (non-'global' markets, old category keys) on load.

---

## Common issues

| Issue | Fix |
|-------|-----|
| `404 model not found` | Model names changed. Check `llm_client.py` and update to a model your org account has access to. |
| App shows 980 keywords with GBR/ARE/ITA markets | Stale session state from old Kolo matrix. Click "Generate Matrix" again — page auto-clears and regenerates with ~237 Nonbank-focused keywords. |
| `StreamlitAPIException` on multiselect default | Don't hardcode `default=` with keys that might be renamed. Use `default=list(X.keys())`. |
| App not picking up code changes | Manual reboot in Streamlit Cloud: Manage app → ⋮ → Reboot. |
| Auth failed on git push | Use a Personal Access Token in remote URL: `https://TOKEN@github.com/ek-arch/nonbank-seo.git`. |
| SerpAPI / Perplexity warnings on pages | Add the missing key to `.streamlit/secrets.toml` (or to Streamlit Cloud → Settings → Secrets). |

---

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — page flow, data model, how engine modules connect
- [DEPLOYMENT.md](DEPLOYMENT.md) — Streamlit Cloud setup, secrets management, reboots
- [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) — secrets schema

---

## License

Private / internal use.
