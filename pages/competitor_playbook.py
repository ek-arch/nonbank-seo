"""Page — Competitor Playbook: how Gnosis Pay, MetaMask Card, COCA,
Bleap, Crypto.com, Bybit, RedotPay, Holyheld, and Nexo actually reach
their audiences. Source: structured research, April 2026.

This is the "what competitors do" research brief — lives under
Research, separate from Competitor Intel (feature/SERP data) and
Campaign Plan (our sprint brief that cites this page).
"""
from __future__ import annotations

import pandas as pd
import streamlit as st


def page_competitor_playbook():
    st.title("🎯 Competitor Playbook")
    st.caption(
        "How the 9 reference competitors actually reach users — channels, "
        "KOLs, referral economics, gimmicks. Source: structured research, "
        "April 2026. Read first, then apply to Campaign Plan."
    )

    st.info(
        "**Opinionated summary (jump to 'Roll-up' tab):** copy RedotPay's "
        "TikTok + multi-tier affiliate playbook. Copy Bybit's lifetime-"
        "revshare affiliate model. Copy MetaMask's token-rewards narrative "
        "even pre-token. Copy Gnosis Pay's help-center-as-SEO. Steal "
        "Crypto.com's programmatic country pages. **Ignore** Crypto.com's "
        "F1/UFC tier (budget-prohibitive), COCA's Telegram-only bet (too "
        "regional), Gnosis Pay's NFT-gated referrals (too tribal)."
    )

    tabs = st.tabs([
        "🏆 Roll-up / What to Copy",
        "Gnosis Pay", "MetaMask Card", "COCA Wallet", "Bleap",
        "Crypto.com", "Bybit Card", "RedotPay", "Holyheld", "Nexo",
    ])

    # ── Roll-up ────────────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("What to copy · one play, not a strategy · ignore")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("### ✅ Copy aggressively")
            st.markdown("""
- **RedotPay — TikTok + multi-tier affiliate.**
  Direct fit for 100+ country, EN-global scope. Highest
  ROI/$ in the set. Filipino / LATAM / MENA creators showing "pay
  for Shopee with USDT" drive thousands of installs per video.
- **Bybit — lifetime revshare (not CPA).**
  Up to 50% + sub-affiliate +10%. Lifetime payouts let
  affiliates dominate "Nonbank referral code" SERPs — free
  evergreen content.
- **MetaMask — token-rewards narrative, pre-token OK.**
  $30M Linea rewards program tied to future token. Pre-announcing
  a points/rewards program creates FOMO and referral pull.
- **Gnosis Pay — help-center-as-SEO.**
  Every support article becomes a long-tail landing page. Nonbank's
  existing docs should be SEO-optimized, not just functional.
- **Crypto.com — programmatic country pages.**
  Baseline for 100+ country coverage. "Crypto card in
  [country]" pages — Nonbank needs them.
- **Bleap — Mastercard partnership PR beat.**
  One co-branded announcement = 10+ pickups. Frame
  our Kolo/Visa relationship as a press beat, not footnote.
""")
        with c2:
            st.markdown("### 🟡 One play, not a strategy")
            st.markdown("""
- **Bleap — founder pedigree PR.**
  Ex-Revolut duo drove every headline. Use if Nonbank
  founders have similar pedigree.
- **Nexo — dual-mode "credit card" framing.**
  "Crypto credit card" SERP is less contested than "crypto
  debit card". Consider microsite/page variant.
- **Holyheld — niche-down positioning.**
  "For AI builders" cuts through "another crypto card"
  noise. Test vertical variants (nomads, USDT spenders,
  self-custody purists).
- **MetaMask — $199 metal-card tier.**
  Premium SKU as identity signal. Revisit post-sprint
  if base card has traction.
""")
        with c3:
            st.markdown("### ❌ Ignore")
            st.markdown("""
- **Crypto.com — F1 / UFC / Eminem / Matt Damon.**
  Budget-prohibitive and off-positioning for a
  self-custody narrative.
- **COCA — Telegram-only bet.**
  Too regional (CIS/SEA) unless Nonbank ships a TG
  bot. Not sprint scope.
- **Gnosis Pay — NFT-gated referrals.**
  Adds friction, niche-tribal. Nonbank's addressable
  market is wider.
- **Google/Meta/LinkedIn paid.**
  Confirmed by research: **none of the 9 competitors
  use Google/Meta ads** either. License blockers are
  universal — everyone relies on earned PR, affiliates,
  KOLs, organic SEO.
""")

        st.divider()
        st.markdown("### 🎯 The unclaimed land")
        st.success(
            "**None of the 9 rank for honest multi-product comparison "
            "content.** Every `[competitor] vs [competitor]` SERP is owned "
            "by affiliate farms (cryptocardhub, coinsoncards, fintechdeepak). "
            "Nonbank should build a first-party comparison hub early — "
            "uncontested brand-adjacent real estate. This is the "
            "single highest-leverage SEO move in the category."
        )

        st.divider()
        st.markdown("### Ad-policy validation")
        st.markdown(
            "Research confirmed: **none of Gnosis Pay, MetaMask, COCA, "
            "Bleap, Bybit, RedotPay, Holyheld, or Nexo rely on Google "
            "Ads / Meta Ads / LinkedIn Ads / TikTok Ads** for paid "
            "acquisition. Crypto.com is the only exception — they pay "
            "for sports sponsorships (F1, UFC) and celebrity ads but "
            "*not* platform search/display ads. This confirms the "
            "structural policy block on DeFi wallet advertising and "
            "validates the sprint plan's exclusion of those channels."
        )

    # ── 1. Gnosis Pay ──────────────────────────────────────────────────────
    with tabs[1]:
        _profile(
            name="Gnosis Pay",
            url="https://gnosispay.com",
            positioning='"Fully self-custodial Visa — your keys, your spend." GNO-staking cashback tiers (1–5%).',
            geo="EU/UK only. No push outside.",
            channels="Blog on gnosispay.com + Gnosis parent blog (gnosis.io/blog); heavy X (@gnosispay); dedicated help center with SEO-targeted articles. No podcast / YouTube cadence.",
            paid_pr=(
                "Earned: Decrypt feature (**Why Gnosis Pay Isn't Just Another Crypto Card**), "
                "CoinGape review, Altcoin Buzz. No visible Bankless / Milk Road sponsorships — "
                "punch through **editorial, not paid newsletters**."
            ),
            kol="Mid-tier Eth/DeFi creators organic (e.g. 'mattbullish' tutorial). Not bought. Zeal and Picnic wallets now run referral — Gnosis offloaded KOL recruiting to integrating wallet partners.",
            community="Active Discord + X. Farcaster via Gnosis ecosystem. OG NFT holders = de facto ambassador tier.",
            seo='Ranks for "self-custodial crypto card," "Gnosis Pay review." Help-center articles drive long-tail ("Gnosis card SAFE best practices").',
            referral=(
                "**Season-based NFT-gated.** Season 4: OG NFT holders earn 40 EURe per referral; "
                "non-OG unlock NFT by referring 2; referees get 100% card discount. "
                "[Source](https://x.com/gnosispay/status/1886396982908060108). Now ended at Gnosis level — "
                "partner wallets run their own."
            ),
            gimmick="OG NFT as status/earning asset; 2025–26 strategic pivot to 'Gnosis Pay for Fintechs' (white-label).",
            steal=[
                "**Seasonal, time-boxed** referral drops with status-NFT gate drive urgency > evergreen programs.",
                "**Offload referral to integrating wallet partners** — viable if Nonbank opens infra to partners.",
                "**Help-center-as-SEO**: every support article is a long-tail landing page.",
            ],
        )

    # ── 2. MetaMask Card ───────────────────────────────────────────────────
    with tabs[2]:
        _profile(
            name="MetaMask Card",
            url="https://metamask.io/card",
            positioning='"True self-custody at point of sale" — funds stay in wallet until swipe, JIT conversion via Linea spender contract.',
            geo="EEA, UK, Argentina, Brazil, Canada, Colombia, Mexico, Switzerland, US (GA Feb 2026). **LATAM priority.**",
            channels="metamask.io/news blog; Consensys press wire; Linea blog cross-posting. Big event plays (ETHDenver 2025 unveil, ETHCC).",
            paid_pr=(
                "Heavy Tier-1 coverage — CoinDesk, The Defiant, Cointelegraph, TradingView. "
                "**Consensys PR machine is the moat**; minimal reliance on paid crypto ad networks."
            ),
            kol="Leans on Consensys/Linea ecosystem builders rather than paid KOLs. Founder-led (Dan Finlay, Joe Lubin) on podcasts.",
            community="Captive — 30M+ MetaMask MAU. Linea Discord, r/Metamask. **Distribution is the product.**",
            seo='Dominates branded "MetaMask card." Competes for "self-custody debit card," "Linea card."',
            referral=(
                "**$30M Linea rewards program tied to future token** ([CoinDesk Oct 2025](https://www.coindesk.com/markets/2025/10/07/metamask-confirms-usd30m-rewards-program-links-to-future-token)). "
                "1% USDC cashback virtual, 3% metal, +8% Coinmunity Cashback via Linea/DapDap = "
                "**up to 9% — industry-leading**."
            ),
            gimmick="**$199/yr Metal Card** (premium SKU). Token-incentivized rewards ('stakeholders, not spenders'). ETHDenver stage launch.",
            steal=[
                "**Premium metal tier** as an identity-signal SKU — fintech-adjacent audiences pay.",
                "**Token-gated rewards narrative** ('become a stakeholder') even pre-token is a strong funnel hook. Nonbank could pre-announce a points program convertible later.",
                "**Event-stage launches** (ETHDenver, ETHCC, Token2049) beat press releases.",
            ],
        )

    # ── 3. COCA Wallet ─────────────────────────────────────────────────────
    with tabs[3]:
        _profile(
            name="COCA Wallet",
            url="https://coca.xyz",
            positioning='"Crypto card on Telegram — no app download."',
            geo="Global, Telegram-heavy regions (CIS, SEA, MENA).",
            channels="coca.xyz/post blog (tutorials), PRNewswire wire releases, Telegram-native distribution.",
            paid_pr='PRNewswire-driven ("[COCA Wallet Launches on Telegram](https://www.prnewswire.com/news-releases/coca-wallet-launches-on-telegram-simplifying-crypto-access-for-millions-of-users-302313304.html)"). Wire-service heavy, not tier-1 earned.',
            kol="Minimal visible paid KOLs; distribution via Telegram discovery (@COCAWallet_Bot) and TON/Telegram creator ecosystem.",
            community="Telegram-first. Bot = acquisition surface. **800M TG MAU is the entire thesis.**",
            seo='Thin. "COCA wallet Telegram," "MPC wallet card." Not ranking for category terms.',
            referral="Exists but not prominently marketed.",
            gimmick="Telegram bot as primary onboarding; 13+ chain cross-chain swaps inside the bot.",
            steal=[
                "Limited. Telegram bot onboarding is interesting **only** if Nonbank targets TG-heavy geos.",
                'Worth copying: **"no app download"** messaging hook.',
            ],
        )

    # ── 4. Bleap ───────────────────────────────────────────────────────────
    with tabs[4]:
        _profile(
            name="Bleap",
            url="https://bleap.finance",
            positioning='"Stablecoin payments mainstream — gasless, no seed phrase, Portal MPC." **Directly adjacent to Nonbank.**',
            geo='EU first, LATAM next ("where demand for alternative financial solutions is accelerating").',
            channels="bleap.finance/blog; founder-led press (ex-Revolut duo João Alves & Guilherme Gomes). The Block, Financial IT, FFNews coverage.",
            paid_pr=(
                "Strong PR on **Mastercard partnership** (April 2025) — "
                "[The Block](https://www.theblock.co/post/350832/ex-revolut-bleap-mastercard-stablecoins), "
                "Altcoin Buzz, Cryptoenews. **Leveraged Revolut founder pedigree hard.**"
            ),
            kol="Early-stage, minimal paid KOL. Founder interviews carrying the narrative.",
            community="Small but growing X, Discord. Arbitrum ecosystem affinity.",
            seo='Thin. Ranks for "Bleap card," building toward "stablecoin card."',
            referral="Cashback-driven (2% USDC, up to 20% promotional).",
            gimmick="**Founder credibility (Revolut alumni)** used as social proof in every headline.",
            steal=[
                '**Lead with founder pedigree** if any exists — "ex-Revolut/ex-Wise/ex-Monzo built X" is a press-magnet hook.',
                '**Beta-period transaction/savings stats** in PR ("$5M processed, $100K saved in fees") — easy earned-media line.',
                "**Mastercard/Visa partnership press beat** is replicable: one co-branded announcement generates 10+ pickups. Frame Nonbank's Kolo/Visa relationship as a launch beat, not a footnote.",
            ],
        )

    # ── 5. Crypto.com ──────────────────────────────────────────────────────
    with tabs[5]:
        _profile(
            name="Crypto.com Card",
            url="https://crypto.com/cards",
            positioning='"Fortune Favors the Brave" — aspirational, lifestyle.',
            geo="30+ countries.",
            channels="Massive — Crypto.com University blog, YouTube (1M+ subs), podcast, newsletter.",
            paid_pr=(
                "**Category-defining spend.** F1 sponsor through 2030 "
                "([Decrypt](https://decrypt.co/298021/formula-1-secures-multi-year-renewal-with-crypto-com-in-sports-sponsorship-push)), "
                "Miami GP title partner, UFC Official Fight Kit Partner since 2021, UFC Freedom 250 co-presenter "
                "with $1M CRO bonus pool. Celebrity: Matt Damon 'Fortune Favors the Brave,' replaced by Eminem in 2024 "
                "([The Block](https://www.theblock.co/post/291168/eminem-replaces-matt-damon-stepping-up-to-the-mic-in-crypto-com-ad))."
            ),
            kol="Tier-1 ambassadors (LeBron, Lewis Hamilton-adjacent via F1). Long-term, not one-off.",
            community="r/Crypto_com 900K+, Discord, huge Telegram.",
            seo='Dominates "crypto visa card," "crypto debit card." **Programmatic country pages, comparison pages, coin-price pages.**',
            referral="$25 CRO referral; tiered based on card level (Ruby → Obsidian).",
            gimmick="**CRO staking tiers (Ruby/Jade/Icy/Obsidian)** with perks (Spotify, Netflix, Amazon Prime rebates) — industry-defining.",
            steal=[
                "Mostly **ignore** — budget category.",
                "**Staking-tier rebate for streaming subs** is a proven retention lever; a self-custody version (hold X stables → free Netflix reimbursement) would differentiate.",
                "**Programmatic country landing pages** is a must-copy for Nonbank's 100+ country scope.",
            ],
        )

    # ── 6. Bybit Card ──────────────────────────────────────────────────────
    with tabs[6]:
        _profile(
            name="Bybit Card",
            url="https://bybit.com/card",
            positioning='"Free, no fees, up to 10% cashback" — promo-led.',
            geo="Global ex-US.",
            channels="Bybit Learn, YouTube, Bybit blog. Exchange-integrated.",
            paid_pr="Exchange brand carries it; less standalone card PR.",
            kol=(
                "**Massive paid affiliate army — up to 50% lifetime commission** "
                "([Whaleportal](https://whaleportal.com/blog/bybit-affiliate-program-2025-complete-guide-to-earning-up-to-50-commission/)) "
                "+ sub-affiliate +10%. Card-specific: 20 USDT per referral who spends 100 USDT in 30 days "
                "([Bybit Promo](https://www.bybit.com/en/promo/global/bybit-card-referral))."
            ),
            community="Captive exchange userbase.",
            seo='Ranks for "Bybit card review," "crypto card cashback." **Referral-code pages dominate SERPs (NFTPlazas, Chainplay) — SEO leakage to affiliates is intentional.**',
            referral="**Lifetime revshare = best-in-class for affiliate volume.**",
            gimmick="Sign-up bonus stacking (up to $30K welcome package) monopolizes referral-code SEO.",
            steal=[
                "**Lifetime revshare (not CPA) for affiliates** is how you get evergreen YouTube + blog content.",
                '**Let affiliates dominate "Nonbank referral code" SERPs intentionally** — cheap acquisition, evergreen content created by others for free.',
            ],
        )

    # ── 7. RedotPay ────────────────────────────────────────────────────────
    with tabs[7]:
        _profile(
            name="RedotPay",
            url="https://redotpay.com",
            positioning='"Crypto card for the global south" (implicitly). Stablecoin payments + Apple Pay/Google Pay add.',
            geo="**6M users, 100+ countries. HK/SEA/LATAM/MENA/Nigeria strongest.**",
            channels="Website news blog, **TikTok (massive — Filipino, Spanish, Arabic content)**, Telegram, YouTube tutorials by affiliates.",
            paid_pr="$107M Series B (total $194M) drove coverage; otherwise organic/UGC-led.",
            kol=(
                "**Affiliate-driven micro-KOLs.** Up to 40% commission + 10% sub-affiliate + "
                "secondary transaction revshare paid every 30 days "
                "([RedotPay Affiliates](https://www.redotpay.com/affiliates))."
            ),
            community="TikTok is the main surface in PH/LATAM/MENA. Telegram for SEA.",
            seo='Medium tutorials, "RedotPay referral code" SERPs dominated by affiliates.',
            referral="Fee cut on card order (instant) + transaction % (monthly) + 10% L2 override. **Tiered levels.**",
            gimmick='**TikTok virality.** Filipino creators showing "how I pay for Shopee with USDT" drive thousands of sign-ups per video.',
            steal=[
                "🥇 **TikTok-first for emerging markets** — Nonbank's 100+ country scope maps perfectly. Seed 50 micro-creators in PH, NG, MX, BR, ID with a 40% revshare deal.",
                "🥇 **Multi-tier commission** (order fee + txn % + sub-affiliate) creates **self-recruiting affiliate networks**.",
                "🥇 **Apple Pay / Google Pay demo videos** are the single highest-converting TikTok format — copy exactly.",
            ],
        )

    # ── 8. Holyheld ────────────────────────────────────────────────────────
    with tabs[8]:
        _profile(
            name="Holyheld",
            url="https://holyheld.com",
            positioning='2025 reposition: **"Crypto Debit Card for AI Builders & Web3 Natives"** — niche-down play.',
            geo="EEA only (30 countries).",
            channels="holyheld.com blog, X, Toyota Ventures-backed (credibility hook).",
            paid_pr="Thin. Toyota Ventures investment = one PR beat. Otherwise quiet.",
            kol="Minimal. Organic Web3/DeFi niche following.",
            community="Small Discord, crypto-native X audience.",
            seo='Ranks for "crypto debit card EU," "Mastercard crypto card no KYC income."',
            referral="15 USDC ($13 EUR) on card order via referral code. Simple, not aggressive.",
            gimmick="**1,200+ tokens supported** (widest conversion breadth); SEPA IBAN included.",
            steal=[
                '**Niche-down positioning** ("for X type of user") cuts through "another crypto card" noise. Test vertical variants (nomads, USDT spenders, self-custody purists).',
                '**Broadest-token-support** as a differentiator — easy SEO hook ("spend [any token] IRL").',
            ],
        )

    # ── 9. Nexo ────────────────────────────────────────────────────────────
    with tabs[9]:
        _profile(
            name="Nexo Card",
            url="https://nexo.com/card",
            positioning='"Spend without selling — credit card backed by crypto collateral." **Unique framing in this set.**',
            geo="EU/UK/global; 2025 expansion to LATAM/SEA.",
            channels="Nexo blog, Nexo YouTube (product explainers), **The Nexperience podcast**, newsletter.",
            paid_pr="Tier-1 PR on roadmap announcements; InsideBitcoins + press-release syndication heavy. Sponsors European crypto conferences.",
            kol="Mid-tier DeFi/lending YouTubers with dedicated review videos; affiliate-driven.",
            community="r/Nexo ~60K, Discord, Telegram.",
            seo='**Ranks strongly for "crypto credit card," "crypto-backed loan card." Comparison content-heavy.**',
            referral=(
                "**Up to $5,000 total per referral** ($2,500 each) — 0.5% of referee's 30-day avg portfolio, "
                "gated at $5K deposit + 30-day hold. **Highest-ceiling referral in category** "
                "([nexo.com/referral](https://nexo.com/referral))."
            ),
            gimmick=(
                "**Dual-mode (Credit vs Debit) on one card.** Loyalty tiers (Bronze → Platinum) based on NEXO holdings. "
                "Affiliate: 10% of referral interest earnings, 0.2% exchange volume, 1% loans, "
                "**$20/card txn for 12 months**."
            ),
            steal=[
                "**High-ceiling whale-referral** ($2,500 payouts) — a few of these dominate influencer content because the payoff justifies a dedicated video.",
                "**Per-transaction affiliate kicker** ($20/txn × 12 months) aligns affiliates with retention, not just acquisition.",
                '**Dual-mode framing** opens new SEO surface ("crypto credit card" is less contested than "crypto debit card").',
            ],
        )


def _profile(
    *, name: str, url: str, positioning: str, geo: str,
    channels: str, paid_pr: str, kol: str, community: str,
    seo: str, referral: str, gimmick: str, steal: list[str],
) -> None:
    st.subheader(f"{name} · [{url.replace('https://', '')}]({url})")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Positioning.** {positioning}")
        st.markdown(f"**Geo.** {geo}")
        st.markdown(f"**Channels.** {channels}")
        st.markdown(f"**Paid / PR.** {paid_pr}")
        st.markdown(f"**KOL strategy.** {kol}")
    with c2:
        st.markdown(f"**Community.** {community}")
        st.markdown(f"**SEO footprint.** {seo}")
        st.markdown(f"**Referral / affiliate.** {referral}")
        st.markdown(f"**Gimmick.** {gimmick}")

    st.divider()
    st.markdown("### 🎁 What Nonbank can steal")
    for item in steal:
        st.markdown(f"- {item}")
