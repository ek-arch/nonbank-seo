# Create PR Article for Nonbank

Generate a SEO+GEO optimized press release / sponsored article for Nonbank (nonbank.io).

## Product Context
- **Nonbank** = hybrid DeFi wallet with a seamlessly integrated custodial Visa card (NON×CARD)
- **Custody model:** non-custodial wallet (user holds keys) + custodial card (issued via Kolo partnership)
- **Card coverage:** 100+ countries (EU, APAC, LATAM, Central Asia, Middle East). Excluded: TUR, ISR, CHN, IND, US.
- **Language/geo strategy:** English-global. Do NOT localize by country unless the brief explicitly targets one.
- **Chains:** TRON today; EVM planned. Assets: TRX, USDT (TRC-20), BTC (via bridge), ETH (planned).
- **Key differentiators:**
  - Gasless transactions (send USDT without holding TRX/ETH)
  - Built-in AML Watchtower (sanctions screening on incoming transfers)
  - Hybrid DeFi wallet + card in one app (self-custody that still spends)
  - Proxy addresses & watch wallets
  - NON ID — DeFi identity handle, mintable as NFT
- **Competitors (pick 2–4 relevant):**
  - Self-custody + card rivals: Gnosis Pay, MetaMask Card, COCA, Bleap
  - Adjacent/custodial: Crypto.com, Bybit Card, Nexo Card, RedotPay, Holyheld, Moon

## Article Structure (SEO+GEO optimized)

### Required Structure:
1. **Headline** — Include primary keyword, max 70 chars
2. **Entity-rich lead paragraph** — [Brand] + [product category: hybrid DeFi wallet + Visa card] + [key differentiator] in first 2 sentences
3. **Body sections (3-5)** — Each with question-format H2 headers (e.g. "How Does Nonbank's Hybrid Wallet-and-Card Work?")
4. **Comparison table** — Markdown table: Feature | Nonbank | Competitor A | Competitor B
5. **FAQ section** — 3-5 Q&A pairs targeting long-tail queries
6. **Boilerplate** — About Nonbank paragraph with link

### GEO Requirements (for AI engine citations):
- Minimum 3 quotable stat sentences (self-contained facts with numbers)
- Question-format H2 headers (AI engines extract these)
- Comparison table (AI engines parse tables well)
- FAQ section (directly answers AI queries)
- Entity-rich first paragraph

### SEO Requirements:
- Primary keyword: weave in naturally 3-5 times
- No marketing fluff or superlatives ("revolutionary", "game-changing")
- Journalistic, third-person style
- Target word count: 1000-1500 words
- Include UTM link: `https://nonbank.io/?utm_source={outlet_domain}`

## Tone & Style
- Journalistic, not promotional
- Third-person ("Nonbank offers..." not "We offer...")
- Data-driven — include specific numbers, fees, country counts
- Mention competitors fairly — Nonbank should be ONE option, not "the best"
- Natural keyword placement, never forced

## Key Facts to Include (pick relevant ones):
- Hybrid: non-custodial wallet + integrated custodial Visa card (NON×CARD)
- Gasless USDT transfers — no TRX/ETH required
- Built-in AML Watchtower screens incoming funds
- Card live in 100+ countries via Kolo issuer partnership
- Watch wallets and proxy addresses for portfolio privacy
- NON ID — single DeFi identity handle
- Chains: TRON (live), EVM (planned)
- Website: nonbank.io

## UTM Format
Always include: `https://nonbank.io/?utm_source={outlet_domain_without_www}`

## Process
1. Ask user for: primary keyword, outlet, word count (market only if explicitly needed — default is EN-global)
2. Generate the article following the structure above
3. Output in Markdown format
4. Translation: EN-global is the default. Only translate if the outlet is non-EN.

$ARGUMENTS
