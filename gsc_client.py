"""
gsc_client.py — Google Search Console integration for Nonbank SEO Agent
=======================================================================
Wraps the GSC API for:
- Search Analytics (queries, pages, dates, devices, countries)
- URL Inspection (index status + request indexing)
- Sitemaps (list / submit / delete)
- Sites (verify access)

Auth: service account JSON (same pattern as sheets_client.py). The service
account email must be added as a user on the GSC property (Settings → Users
and permissions → Add user → Full or Restricted).

Property identifier for nonbank.io: use either
  - "sc-domain:nonbank.io"           (domain property, recommended)
  - "https://nonbank.io/"            (URL-prefix property)
The app tries both and uses whichever the service account can access.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any

import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Read-only for analytics + inspection; webmasters scope also covers sitemap submit.
SCOPES = ["https://www.googleapis.com/auth/webmasters"]

DEFAULT_SITE_CANDIDATES = [
    "sc-domain:nonbank.io",
    "https://nonbank.io/",
    "https://www.nonbank.io/",
]


# ── Auth ──────────────────────────────────────────────────────────────────────

def _get_service(creds_json: str | dict, api: str = "searchconsole", version: str = "v1"):
    """Build a GSC API client. `creds_json` can be a JSON string or a dict."""
    if isinstance(creds_json, str):
        creds_info = json.loads(creds_json)
    else:
        creds_info = creds_json
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return build(api, version, credentials=creds, cache_discovery=False)


def list_sites(creds_json: str | dict) -> list[dict]:
    """Return all GSC properties this service account has access to."""
    svc = _get_service(creds_json)
    resp = svc.sites().list().execute()
    return resp.get("siteEntry", [])


def pick_site(creds_json: str | dict, preferred: str | None = None) -> str | None:
    """
    Return the best matching GSC property URL for nonbank.io.
    If `preferred` is given and the account has access, return it.
    Otherwise try DEFAULT_SITE_CANDIDATES in order.
    """
    try:
        sites = list_sites(creds_json)
    except HttpError:
        return None
    urls = {s["siteUrl"] for s in sites}
    if preferred and preferred in urls:
        return preferred
    for cand in DEFAULT_SITE_CANDIDATES:
        if cand in urls:
            return cand
    # Fallback — any nonbank.io match
    for u in urls:
        if "nonbank.io" in u:
            return u
    return None


# ── Search Analytics ──────────────────────────────────────────────────────────

def query_search_analytics(
    creds_json: str | dict,
    site_url: str,
    *,
    start: date | str | None = None,
    end: date | str | None = None,
    dimensions: list[str] | None = None,
    row_limit: int = 1000,
    search_type: str = "web",
    filters: list[dict] | None = None,
) -> pd.DataFrame:
    """
    Query Search Analytics.

    dimensions: any combination of "query", "page", "country", "device", "date",
                "searchAppearance"
    search_type: "web", "image", "video", "news", "discover", "googleNews"
    filters: list of {"dimension": "query", "operator": "contains", "expression": "gasless"}

    Returns a DataFrame with columns = dimensions + ["clicks", "impressions", "ctr", "position"].
    """
    if end is None:
        end = date.today() - timedelta(days=2)  # GSC lags 2-3 days
    if start is None:
        start = end - timedelta(days=28) if isinstance(end, date) else None
    if isinstance(start, date):
        start = start.isoformat()
    if isinstance(end, date):
        end = end.isoformat()
    if dimensions is None:
        dimensions = ["query"]

    body: dict[str, Any] = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": row_limit,
        "type": search_type,
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]

    svc = _get_service(creds_json)
    resp = svc.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = resp.get("rows", [])
    if not rows:
        return pd.DataFrame(columns=dimensions + ["clicks", "impressions", "ctr", "position"])

    records = []
    for r in rows:
        rec = {}
        for i, d in enumerate(dimensions):
            rec[d] = r["keys"][i]
        rec["clicks"] = r.get("clicks", 0)
        rec["impressions"] = r.get("impressions", 0)
        rec["ctr"] = r.get("ctr", 0.0)
        rec["position"] = r.get("position", 0.0)
        records.append(rec)

    df = pd.DataFrame(records)
    return df.sort_values("impressions", ascending=False).reset_index(drop=True)


# ── URL Inspection ────────────────────────────────────────────────────────────

def inspect_url(creds_json: str | dict, site_url: str, url: str, language: str = "en-US") -> dict:
    """
    Check index status of a URL. Returns the inspectionResult dict (or error).
    Includes: indexStatusResult, mobileUsabilityResult, richResultsResult, etc.
    """
    svc = _get_service(creds_json)
    body = {
        "inspectionUrl": url,
        "siteUrl": site_url,
        "languageCode": language,
    }
    try:
        resp = svc.urlInspection().index().inspect(body=body).execute()
        return resp.get("inspectionResult", {})
    except HttpError as e:
        return {"error": str(e)}


def inspect_urls_bulk(
    creds_json: str | dict, site_url: str, urls: list[str]
) -> pd.DataFrame:
    """Inspect many URLs; returns a DataFrame of key index status fields."""
    rows = []
    for u in urls:
        r = inspect_url(creds_json, site_url, u)
        idx = r.get("indexStatusResult", {}) if isinstance(r, dict) else {}
        rows.append({
            "url": u,
            "coverage_state": idx.get("coverageState", ""),
            "verdict": idx.get("verdict", ""),
            "last_crawl_time": idx.get("lastCrawlTime", ""),
            "google_canonical": idx.get("googleCanonical", ""),
            "user_canonical": idx.get("userCanonical", ""),
            "indexing_state": idx.get("indexingState", ""),
            "page_fetch_state": idx.get("pageFetchState", ""),
            "robots_txt_state": idx.get("robotsTxtState", ""),
            "error": r.get("error", "") if isinstance(r, dict) else "",
        })
    return pd.DataFrame(rows)


# ── Sitemaps ──────────────────────────────────────────────────────────────────

def list_sitemaps(creds_json: str | dict, site_url: str) -> list[dict]:
    """List submitted sitemaps for a GSC property."""
    svc = _get_service(creds_json)
    resp = svc.sitemaps().list(siteUrl=site_url).execute()
    return resp.get("sitemap", [])


def submit_sitemap(creds_json: str | dict, site_url: str, sitemap_url: str) -> bool:
    """Submit (or re-submit) a sitemap. Returns True on success."""
    svc = _get_service(creds_json)
    try:
        svc.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
        return True
    except HttpError:
        return False


def delete_sitemap(creds_json: str | dict, site_url: str, sitemap_url: str) -> bool:
    """Delete a sitemap submission."""
    svc = _get_service(creds_json)
    try:
        svc.sitemaps().delete(siteUrl=site_url, feedpath=sitemap_url).execute()
        return True
    except HttpError:
        return False


# ── High-level convenience ────────────────────────────────────────────────────

def performance_summary(
    creds_json: str | dict, site_url: str, days: int = 28
) -> dict[str, Any]:
    """
    Return a one-shot dashboard summary: totals, top queries, top pages,
    by country, by device.
    """
    end = date.today() - timedelta(days=2)
    start = end - timedelta(days=days)

    q_total = query_search_analytics(creds_json, site_url, start=start, end=end,
                                     dimensions=[], row_limit=1)
    q_by_query = query_search_analytics(creds_json, site_url, start=start, end=end,
                                        dimensions=["query"], row_limit=100)
    q_by_page = query_search_analytics(creds_json, site_url, start=start, end=end,
                                       dimensions=["page"], row_limit=100)
    q_by_country = query_search_analytics(creds_json, site_url, start=start, end=end,
                                          dimensions=["country"], row_limit=20)
    q_by_device = query_search_analytics(creds_json, site_url, start=start, end=end,
                                         dimensions=["device"], row_limit=10)
    q_by_date = query_search_analytics(creds_json, site_url, start=start, end=end,
                                       dimensions=["date"], row_limit=days + 1)

    totals = {
        "clicks": int(q_total["clicks"].sum()) if not q_total.empty else 0,
        "impressions": int(q_total["impressions"].sum()) if not q_total.empty else 0,
        "ctr": float(q_total["ctr"].mean()) if not q_total.empty else 0.0,
        "position": float(q_total["position"].mean()) if not q_total.empty else 0.0,
    }
    return {
        "range": {"start": start.isoformat(), "end": end.isoformat(), "days": days},
        "totals": totals,
        "by_query": q_by_query,
        "by_page": q_by_page,
        "by_country": q_by_country,
        "by_device": q_by_device,
        "by_date": q_by_date,
    }
