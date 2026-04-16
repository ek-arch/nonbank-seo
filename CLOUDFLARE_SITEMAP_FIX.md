# Cloudflare — Sitemap Fix Checklist for nonbank.io

**Problem:** Google Search Console reports "Couldn't fetch" for nonbank.io/sitemap.xml
**Goal:** Make sure Googlebot can fetch the sitemap with correct content-type

---

## What to check (in order)

### 1. Is the Worker route catching /sitemap.xml?

Go to **Cloudflare Dashboard → Workers & Pages → nonbank-proxy → Triggers (Routes)**

Check if there's a route like `nonbank.io/sitemap.xml` or `nonbank.io/*` assigned to the worker.

- **If `nonbank.io/*` is a route** → the worker intercepts ALL requests to nonbank.io, including /sitemap.xml. This means the worker's `handleSitemap()` function runs, which tries to fetch `https://nonbank.io/sitemap.xml` again — **this creates an infinite loop**. The worker is fetching from itself.
- **If only `nonbank-proxy.ek-3ff.workers.dev/*`** → the worker is NOT intercepting nonbank.io traffic. The sitemap is served directly by Webflow. The problem is likely Webflow's content-type.

**Action needed:**
- If the worker IS on nonbank.io routes: change the sitemap fetch URL inside the worker from `https://nonbank.io/sitemap.xml` to the **Webflow origin URL directly** (see step 4)
- If the worker is NOT on nonbank.io routes: skip to step 2

### 2. Check nonbank.io DNS / Proxy settings

Go to **Cloudflare Dashboard → DNS**

- Is nonbank.io proxied through Cloudflare (orange cloud)? Or DNS-only (gray cloud)?
- If **proxied (orange cloud)**: Cloudflare sits between Googlebot and Webflow. Check if any Page Rules, Cache Rules, or WAF rules block /sitemap.xml
- If **DNS-only (gray)**: Cloudflare doesn't touch the traffic. Problem is purely Webflow-side.

### 3. Test the sitemap URL

Run these checks:

```
# Check response code and content-type
curl -I https://nonbank.io/sitemap.xml

# Expected:
# HTTP/2 200
# content-type: application/xml  (or text/xml)

# If you see:
# content-type: application/rss+xml  → Webflow bug, needs fixing
# HTTP 301/302 redirect → follow the redirect, check final URL
# HTTP 403/404 → something is blocking it
```

```
# Check what Googlebot sees (simulate its user agent)
curl -A "Googlebot" https://nonbank.io/sitemap.xml | head -20
```

```
# Check the actual content
curl https://nonbank.io/sitemap.xml | head -50
```

### 4. Fix the content-type issue

Webflow serves sitemaps with `content-type: application/rss+xml` instead of `application/xml`. Some Google crawlers reject this.

**Option A — Cloudflare Transform Rule (recommended, no worker needed):**

Go to **Rules → Transform Rules → Modify Response Header**

- **When:** URI Path equals `/sitemap.xml`
- **Then:** Set response header `Content-Type` to `application/xml; charset=UTF-8`
- Save and deploy

**Option B — Use the Worker (if it's already on nonbank.io routes):**

The worker code already does this, but fix the origin fetch to avoid loops:

Change line 93 in the worker from:
```javascript
const webflowResp = await fetch('https://nonbank.io/sitemap.xml', {
```
To the direct Webflow origin (find your Webflow site's actual hosting URL):
```javascript
const webflowResp = await fetch('https://proxy-ssl.webflow.com/YOUR_WEBFLOW_SITE_ID/sitemap.xml', {
```
Or use the Webflow staging URL. The key is: **don't fetch from nonbank.io if the worker IS nonbank.io**.

### 5. Check Cache settings

Go to **Cloudflare Dashboard → Caching → Cache Rules**

- Is /sitemap.xml being cached? If cached with a stale version, Googlebot gets old data
- **Recommended:** Add a cache rule for `/sitemap.xml` with TTL of 1 hour (3600s) or set to "Bypass Cache" temporarily until Google confirms it can fetch

### 6. Check WAF / Bot rules

Go to **Security → WAF** and **Security → Bots**

- Is "Bot Fight Mode" enabled? This can block Googlebot
- Are there any firewall rules that might block requests to /sitemap.xml?
- Check **Security → Events** — filter by URI `/sitemap.xml` to see if any requests were blocked

### 7. Check Page Rules

Go to **Rules → Page Rules**

- Any rules matching `*nonbank.io/sitemap*` that redirect or block?

---

## After fixing

1. Visit `https://nonbank.io/sitemap.xml` in browser — should show XML with correct content-type
2. Test with curl: `curl -I https://nonbank.io/sitemap.xml` — verify `content-type: application/xml`
3. Go to **Google Search Console → Sitemaps → Resubmit** `https://nonbank.io/sitemap.xml`
4. Wait 24-48 hours for Google to re-fetch

---

## Quick summary for the Cloudflare person

> Google can't fetch our sitemap at nonbank.io/sitemap.xml. Please check:
> 1. Is there a Worker route on nonbank.io that might create a fetch loop for /sitemap.xml?
> 2. Is the content-type correct? (should be application/xml, not application/rss+xml)
> 3. Are any WAF, bot, or cache rules blocking or serving stale content to Googlebot?
> 4. Add a Transform Rule to set content-type to application/xml for /sitemap.xml if needed
