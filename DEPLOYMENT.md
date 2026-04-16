# Deployment Guide

How to deploy the Nonbank SEO & GEO Intelligence Agent.

---

## Streamlit Cloud (recommended)

### First-time setup

1. **Fork or import this repo** to your GitHub account
2. Go to https://share.streamlit.io and sign in with GitHub
3. Click **Create app** → **Deploy a public app from GitHub**
4. Fill in:

   | Field | Value |
   |---|---|
   | Repository | `your-org/nonbank-seo` |
   | Branch | `main` |
   | Main file path | `app.py` |
   | App URL (optional) | `nonbank-seo` → yields `nonbank-seo.streamlit.app` |

5. Click **Advanced settings → Secrets**
6. Paste contents from your local `.streamlit/secrets.toml` (see [`secrets.toml.example`](.streamlit/secrets.toml.example) for schema)
7. Click **Deploy**. First build takes ~2 minutes.

### Secrets required

See [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example). Minimum for core features:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."   # Claude — required for generation
PERPLEXITY_KEY    = "pplx-..."           # AI visibility audits — recommended
SERPAPI_KEY       = "..."                # SERP + competitor spy — recommended

[gsheets]
# Google service account JSON — optional, for Content Plan persistence
```

### Updating secrets

**Manage app → Settings → Secrets** → edit → save. Changes propagate in ~1 minute. No redeploy needed.

### Auto-deploy on push

Streamlit Cloud picks up every push to `main` and redeploys automatically (~30-60 seconds).

### Manual reboot

If a deploy gets stuck or cached state is wrong:

**Manage app → ⋮ → Reboot**

---

## Local development

### Requirements

- Python 3.11+
- `pip`

### Install

```bash
git clone https://github.com/ek-arch/nonbank-seo.git
cd nonbank-seo
pip install -r requirements.txt
```

### Configure

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml with your real keys
```

### Run

```bash
streamlit run app.py
```

Opens at http://localhost:8501 with hot reload.

---

## Docker (optional)

No official Dockerfile, but a minimal one:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:

```bash
docker build -t nonbank-seo .
docker run -p 8501:8501 \
  -v $(pwd)/.streamlit/secrets.toml:/app/.streamlit/secrets.toml \
  nonbank-seo
```

---

## API key sources

| Key | Where to get | Approx. cost |
|-----|--------------|--------------|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com → API keys | ~$0.005/call (Sonnet 4-6) |
| `PERPLEXITY_KEY` | https://www.perplexity.ai/settings/api | ~$0.005/query (sonar) |
| `SERPAPI_KEY` | https://serpapi.com → dashboard | Free: 100/month, then paid |
| `[gsheets]` | https://console.cloud.google.com → Service Accounts → create key → JSON | Free |

### Google Sheets service account setup

1. Go to https://console.cloud.google.com → pick or create a project
2. **APIs & Services → Library** → enable **Google Sheets API** and **Google Drive API**
3. **APIs & Services → Credentials → Create credentials → Service account**
4. Grant role: `Editor` (or narrower `Sheets` scope)
5. After creation, click the service account → **Keys → Add key → JSON** → download
6. Paste the JSON contents into `.streamlit/secrets.toml` under `[gsheets]`
7. **Share your target Google Sheet** with the service account email (found in the JSON as `client_email`)

---

## CI / testing

No formal CI. Validate locally before pushing:

```bash
# Compile-check all .py files
python3 -c "
import py_compile, pathlib
errs = []
for p in pathlib.Path('.').rglob('*.py'):
    if '.git' in str(p): continue
    try: py_compile.compile(str(p), doraise=True)
    except py_compile.PyCompileError as e: errs.append((p, e))
if errs:
    for p, e in errs: print('ERR', p, e)
else: print('all compile OK')
"

# Import-check all pages
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

---

## Common deploy issues

| Symptom | Cause | Fix |
|---|---|---|
| `ImportError: cannot import name 'X' from 'config'` | Streamlit Cloud has stale cache | Manage app → ⋮ → **Reboot** |
| `404 model not found` (Anthropic) | Model name not available to your account | Check `llm_client.py` model constants, update to available model |
| `Set your SerpAPI key in the sidebar` but it's in secrets | Key name mismatch | Must be exactly `SERPAPI_KEY` (not `SERP_API_KEY`) in secrets |
| Secrets file committed by accident | `.streamlit/secrets.toml` not gitignored | Confirm `.gitignore` contains `.streamlit/secrets.toml`. Rotate all leaked keys. |
| App runs locally, crashes on Cloud | Python version mismatch | Streamlit Cloud uses Python 3.14. Test locally with 3.11+ and avoid `from __future__ import annotations` issues with runtime type subscripts. |
| Page 404s with "This branch does not exist" on deploy form | Stale Streamlit form cache | Refresh the form page, retype the branch name |

---

## Rolling back

Streamlit Cloud deploys whatever is at `HEAD` of the configured branch. To roll back:

```bash
git log --oneline                    # find the good commit
git revert <bad-commit>              # safer than reset
git push origin main
```

Or force to a specific commit (destructive):

```bash
git reset --hard <good-commit>
git push --force-with-lease origin main
```

Streamlit will redeploy within ~30-60 seconds of the push.

---

## Monitoring

### Streamlit Cloud logs

**Manage app** → logs panel on the right. Shows Python tracebacks, request latencies, crashes.

### API usage

- **Anthropic**: https://console.anthropic.com → Usage
- **Perplexity**: https://www.perplexity.ai/settings/api → Usage
- **SerpAPI**: https://serpapi.com/account → Usage

### Google Analytics (nonbank.io)

Unrelated to this app — nonbank.io itself runs GA4 (`G-9HN610W2LE`). Use Search Console for SEO monitoring.
