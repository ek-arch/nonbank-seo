# Webflow Designer SEO Fixes — HISTORICAL

**Status:** This was a Kolo-era punch list for Webflow Designer tasks on
nonbank.io (hreflang fixes across en/ru/uk locales, JSON-LD with `areaServed`
values like "Europe, United Kingdom, UAE, CIS", and a deployment plan for ~41
country-matrixed landing pages). Those tasks either completed, were superseded
by Nonbank's EN-global strategy, or no longer apply.

Any future Webflow-side SEO work should align with the current product positioning:

- EN-global content (no hreflang locales needed beyond `en`/`x-default`)
- Structured data describing Nonbank as a hybrid DeFi wallet + custodial Visa
  card, not a country-matrixed CeFi card
- `areaServed`: global wallet; card supported in 100+ countries (exclusions listed
  in `data_sources.py::card_allowance`)

Source of truth: [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md),
[llms.txt](llms.txt).
