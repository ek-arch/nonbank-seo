# Webflow Programmatic SEO Brief — DEPRECATED

**Status:** This brief described a Kolo-era long-tail programmatic-SEO pipeline
(~41 landing pages for country × language combinations such as "crypto card UAE"
or "крипто карта ОАЭ"). That approach is incompatible with Nonbank's EN-global
strategy and is no longer active.

The Python modules that backed this pipeline (`programmatic_seo.py`,
`seo_builder.py`, `seo_deploy.py`) are marked legacy in the README. They remain
in the repo for reference but are not part of the current SEO/GEO workflow.

## Current equivalent

Scalable content generation for Nonbank is handled by the **Content Brief
Factory** (`pages/pseo.py`), which generates briefs across five types:

1. Competitor comparisons (vs Gnosis Pay, MetaMask Card, COCA, Bleap)
2. Category roundups (self-custody wallets with cards)
3. Differentiator deep-dives (gasless, AML Watchtower, hybrid DeFi + card)
4. User persona articles
5. Problem → solution how-tos

See [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md) for the full
current architecture.
