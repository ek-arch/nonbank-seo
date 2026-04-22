"""
serpzilla_client.py — Serpzilla REST API client
================================================
Pure-Python client for Serpzilla's guest-post / link-insertion marketplace.
Used by Outlet Matching + Publication ROI pages to pull a live catalog
of crypto-native donor sites (DR, traffic, price, placement quality)
and normalize the rows to the same shape as `collaborator_outlets.py`.

Auth flow (per https://serpzilla.com/api/authentication):
  1. POST /login   {login, apiToken}        -> AUTH_TICKET cookie
  2. GET  /auth    Cookie: AUTH_TICKET=...   -> JWT
  3. All /rest/* calls need BOTH
       Authorization: Bearer <JWT>
       Cookie: AUTH_TICKET=<ticket>

Link-type semantics (from /api/buy-permanent):
  news    = Advertiser's Article (Guest Post) — we write it
  review  = Publisher's Article  (Guest Post) — they write it
  link    = In The News          (Link Insertion)
  archive = In The Archive       (Link Insertion)

For Nonbank's SEO/GEO sprint we almost exclusively want `news` (guest
posts we control). Link insertions score far lower in the ROI model
(`publication_roi.calculate_publication_roi(content_type=...)`).
"""
from __future__ import annotations

import os
from typing import Any, Optional

import requests

BASE_URL = "https://app.serpzilla.com"

# Serpzilla-side link-type codes -> our internal content_type strings.
LINK_TYPE_TO_CONTENT = {
    "news":    "guest_post",
    "review":  "guest_post",
    "link":    "link_insertion",
    "archive": "link_insertion",
}


class SerpzillaError(Exception):
    """Wraps any Serpzilla-side auth / transport / API-response failure."""


class SerpzillaClient:
    """
    Minimal read-oriented client. Create, authenticate, and search.
    Safe to reuse across calls within a single session; re-authenticate
    by constructing a new client if the JWT is rejected.

    Example
    -------
    >>> c = SerpzillaClient("you@example.com", "sz_xxx").authenticate()
    >>> proj = c.ensure_project("https://nonbank.io/")
    >>> items = c.search_catalog(proj["projectId"], link_type="news",
    ...                          price_min=50, price_max=400)
    >>> outlets = c.normalize(items["items"], link_type="news")
    """

    def __init__(
        self,
        login: str,
        api_token: str,
        *,
        timeout: int = 30,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not login or not api_token:
            raise SerpzillaError("login and api_token are required")
        self.login = login
        self.api_token = api_token
        self.timeout = timeout
        self.session = session or requests.Session()
        self._jwt: Optional[str] = None
        self._auth_ticket: Optional[str] = None

    # ── Auth ────────────────────────────────────────────────────────────────

    def authenticate(self) -> "SerpzillaClient":
        """Run the two-step handshake. Idempotent — calling twice re-auths."""
        # Step 1: login -> AUTH_TICKET (cookie or body).
        r = self.session.post(
            f"{BASE_URL}/login",
            json={"login": self.login, "apiToken": self.api_token},
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )
        _raise_for_status(r, "login")

        # The docs show AUTH_TICKET "in response" — try cookie jar, then body.
        ticket = self.session.cookies.get("AUTH_TICKET")
        if not ticket:
            body = _safe_json(r)
            ticket = (
                body.get("AUTH_TICKET")
                or body.get("authTicket")
                or body.get("ticket")
                or body.get("auth_ticket")
            )
        if not ticket:
            raise SerpzillaError(
                f"AUTH_TICKET missing in /login response (status={r.status_code}, "
                f"body preview={_preview(r.text)})"
            )
        self._auth_ticket = ticket

        # Step 2: /auth with the ticket -> JWT (body).
        r = self.session.get(
            f"{BASE_URL}/auth",
            headers={
                "Accept": "application/json",
                "Cookie": f"AUTH_TICKET={self._auth_ticket}",
            },
            timeout=self.timeout,
        )
        _raise_for_status(r, "auth")
        body = _safe_json(r)
        jwt = (
            body.get("jwt")
            or body.get("token")
            or body.get("access_token")
            or (r.text.strip().strip('"') if r.text else "")
        )
        if not jwt or len(jwt) < 20:
            raise SerpzillaError(
                f"JWT missing in /auth response (status={r.status_code}, "
                f"body preview={_preview(r.text)})"
            )
        self._jwt = jwt
        return self

    def _headers(self, *, json_body: bool = True) -> dict[str, str]:
        if not self._jwt or not self._auth_ticket:
            self.authenticate()
        h = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._jwt}",
            "Cookie": f"AUTH_TICKET={self._auth_ticket}",
        }
        if json_body:
            h["Content-Type"] = "application/json"
        return h

    # ── Projects ────────────────────────────────────────────────────────────

    def ensure_project(self, domain: str) -> dict[str, Any]:
        """
        Create (or hit the idempotent endpoint for) a promotion project.
        Every search requires a projectId + urlId bound to a target domain.

        Returns {"projectId": int, "urlId": int, "textId": int}.
        """
        r = self.session.post(
            f"{BASE_URL}/rest/Project/addSimpleProjectAndContent",
            headers=self._headers(),
            json={"domain": domain},
            timeout=self.timeout,
        )
        _raise_for_status(r, "Project.addSimpleProjectAndContent")
        data = _safe_json(r)
        if data.get("isError"):
            raise SerpzillaError(f"project create error: {data}")
        return {
            "projectId": data.get("id") or data.get("projectId"),
            "urlId": data.get("urlId"),
            "textId": data.get("textId"),
            "raw": data,
        }

    def add_promotion_url(
        self, project_id: int, url: str, anchor_html: str
    ) -> dict[str, Any]:
        """
        Add a custom promotion URL + anchor text to an existing project.
        `anchor_html` uses Serpzilla's #a#...#/a# anchor syntax, e.g.
        "Learn about #a#gasless crypto wallets#/a#".
        """
        r = self.session.post(
            f"{BASE_URL}/rest/Content/add/texts/projectId/{project_id}",
            headers=self._headers(),
            json={
                "urlsTexts": [
                    {"url": url, "texts": [{"text": anchor_html}]},
                ]
            },
            timeout=self.timeout,
        )
        _raise_for_status(r, "Content.addTexts")
        return _safe_json(r)

    # ── Catalog search ──────────────────────────────────────────────────────

    def search_catalog(
        self,
        project_id: int,
        *,
        link_type: str = "news",
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        dr_min: Optional[int] = None,
        traffic_min: Optional[int] = None,
        extra_filters: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Hit SearchPermanent with price / DR / traffic filters.

        Parameters
        ----------
        link_type : one of "news" | "review" | "link" | "archive".
        price_min, price_max : USD bounds mapped to priceArticleFrom/To.
        dr_min : minimum domain rating (Ahrefs DR). Sent as
                 `domainRatingFrom` (best-guess — pass in
                 `extra_filters` if Serpzilla rejects it).
        traffic_min : minimum monthly traffic. Sent as `trafficFrom`.
        extra_filters : any extra Serpzilla filter params (spec:
                        SearchPermanent.searchPermanent).

        Returns the raw Serpzilla response:
            { "nofItemsTotal": int, "searchHistoryId": str,
              "message": str, "items": [...] }
        """
        if link_type not in LINK_TYPE_TO_CONTENT:
            raise SerpzillaError(
                f"link_type must be one of {sorted(LINK_TYPE_TO_CONTENT)}, "
                f"got {link_type!r}"
            )

        # Build the fullest filter payload; if Serpzilla rejects unknown
        # filter names (e.g. domainRatingFrom / trafficFrom are best-guesses
        # not in the public /api/buy-permanent example), we fall back to
        # price-only + client-side filtering for DR and traffic.
        full: dict[str, Any] = {}
        if price_min is not None:
            full["priceArticleFrom"] = price_min
        if price_max is not None:
            full["priceArticleTo"] = price_max
        if dr_min is not None:
            full["domainRatingFrom"] = dr_min
        if traffic_min is not None:
            full["trafficFrom"] = traffic_min
        if extra_filters:
            full.update(extra_filters)

        url = f"{BASE_URL}/rest/SearchPermanent/projectId/{project_id}"
        params = {"permanentLinkType": link_type, "projectId": project_id}

        r = self.session.post(
            url, params=params, headers=self._headers(),
            json=full, timeout=self.timeout,
        )

        # Graceful fallback: if server rejects the filter payload, retry
        # with confirmed-safe price filters only and post-filter locally.
        if r.status_code in (400, 422):
            safe = {k: full[k] for k in ("priceArticleFrom", "priceArticleTo") if k in full}
            r = self.session.post(
                url, params=params, headers=self._headers(),
                json=safe, timeout=self.timeout,
            )
            _raise_for_status(r, "SearchPermanent.searchPermanent (fallback)")
            data = _safe_json(r)
            items = data.get("items", []) or []
            if dr_min is not None:
                items = [it for it in items if (it.get("domainRating") or 0) >= dr_min]
            if traffic_min is not None:
                items = [it for it in items if (it.get("traffic") or 0) >= traffic_min]
            data["items"] = items
            data["nofItemsTotal"] = len(items)
            data["_fallback_applied"] = True
            return data

        _raise_for_status(r, "SearchPermanent.searchPermanent")
        return _safe_json(r)

    # ── Normalization to the shape used elsewhere in the app ───────────────

    @staticmethod
    def normalize(items: list[dict], *, link_type: str = "news") -> list[dict]:
        """
        Map Serpzilla items -> dicts compatible with
        `collaborator_outlets.get_outlets()` plus a few GEO-friendly
        extras. The `content_type` field plugs straight into
        `publication_roi.calculate_publication_roi(content_type=...)`.
        """
        content_type = LINK_TYPE_TO_CONTENT.get(link_type, "guest_post")
        out: list[dict] = []
        for it in items or []:
            price_article = it.get("priceArticle") or it.get("priceReview")
            price = it.get("price")
            effective_price = float(
                price_article if content_type == "guest_post" else price or 0
            )
            dr = int(it.get("domainRating") or 0)
            traffic = int(it.get("traffic") or 0)
            out.append({
                "domain": it.get("shortUrlFormatted") or it.get("fullUrl") or "",
                "dr": dr,
                "price": effective_price,
                "search_pct": None,
                "traffic": traffic,
                # Score is computed upstream; Serpzilla gives us richer inputs.
                "score": None,
                "has_crypto": True,  # Serpzilla's catalog is crypto-focused.
                "lang": "en",
                "price_per_dr": round(effective_price / max(dr, 1), 2),
                # Serpzilla-specific extras useful for ranking / GEO:
                "serpzilla_id": it.get("id"),
                "serpzilla_domain_id": it.get("domainId"),
                "content_type": content_type,
                "link_type": link_type,
                "placement_percent": it.get("placementPercent"),
                "placement_uniqueness": it.get("placementUniqueness"),
                "avg_days_to_index": it.get("avgDaysToIndex"),
                "avg_placement_time": it.get("avgPlacementTime"),
                "trust": it.get("trust"),
                "cleanliness": it.get("cleanliness"),
                "rating_combined": it.get("ratingCombined"),
                "sqi": it.get("sqi"),
                "moz_da": it.get("mozDomainAuthority"),
                "moz_spam_score": it.get("mozSpamScore"),
                "ahrefs_domains": it.get("ahrefsDomains"),
                "mj_cf": it.get("mjCf"),
                "mj_tf": it.get("mjTf"),
                "is_nofollow": it.get("isPlacingNoFollow"),
                "is_profitable": it.get("isProfitable"),
                "traffic_checked_at": it.get("trafficCheckedAt"),
                "advert_indexed_percent": it.get("advertIndexedPercent"),
                "source": "serpzilla",
            })
        return out


# ── Convenience factory ────────────────────────────────────────────────────

def client_from_env(
    login: Optional[str] = None,
    api_token: Optional[str] = None,
) -> SerpzillaClient:
    """
    Build a client from explicit args or from env vars
    SERPZILLA_LOGIN + SERPZILLA_API_TOKEN.

    Streamlit callers should prefer pulling from `st.secrets` /
    `st.session_state` directly — this is a framework-free fallback.
    """
    login = login or os.getenv("SERPZILLA_LOGIN", "")
    api_token = api_token or os.getenv("SERPZILLA_API_TOKEN", "")
    if not login or not api_token:
        raise SerpzillaError(
            "Missing credentials: pass login/api_token or set "
            "SERPZILLA_LOGIN + SERPZILLA_API_TOKEN env vars"
        )
    return SerpzillaClient(login, api_token)


# ── Helpers ────────────────────────────────────────────────────────────────

def _safe_json(r: requests.Response) -> dict:
    if not r.content:
        return {}
    try:
        body = r.json()
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {"_list": body}


def _preview(text: str, n: int = 300) -> str:
    if not text:
        return ""
    return text[:n].replace("\n", " ") + ("..." if len(text) > n else "")


def _raise_for_status(r: requests.Response, where: str) -> None:
    if r.status_code >= 400:
        raise SerpzillaError(
            f"{where} failed: HTTP {r.status_code} — {_preview(r.text)}"
        )
