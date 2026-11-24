<div align="center">

<a href="https://ashareapi.com/en/"><img src="https://ashareapi.com/icon-512.png" width="88" height="88" alt="ashareapi"></a>

# ashareapi — Official MCP Server for the A-Share Data API

Let Claude Code / Codex / Cursor / any **AI Agent (MCP)** query China A-share data directly: **Quotes (intraday line · five-level depth) / K-lines / Financials / Money flow / Dragon-Tiger list / L2 order flow / Sectors / Factor screening / Quant backtest / short-term board plays / call auction / news & filings** — **94 tools, and the free tools need no key**.

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![MCP SDK](https://img.shields.io/badge/mcp%20SDK-1.x%20%7C%202.x-6E56CF)
[![CI](https://github.com/ashareapi/ashareapi-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ashareapi/ashareapi-mcp/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green)

**Works with 19 mainstream AI Agent clients** — out of the box:

![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-D97757?logo=claude&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-supported-000000?logo=cursor&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-supported-007ACC)
![Codex](https://img.shields.io/badge/Codex-supported-000000)
![OpenCode](https://img.shields.io/badge/OpenCode-supported-000000?logo=opencode&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-supported-8E75B2?logo=googlegemini&logoColor=white)
![Cline](https://img.shields.io/badge/Cline-supported-18181B?logo=cline&logoColor=white)
![Windsurf](https://img.shields.io/badge/Windsurf-supported-0B100F?logo=windsurf&logoColor=white)

[中文](README.md) · **English**

[Website](https://ashareapi.com/en/) · [Docs](https://ashareapi.com/en/docs/) · [Endpoint list](https://ashareapi.com/en/endpoints/) · [MCP](https://ashareapi.com/en/mcp/) · [Agent Skill](https://ashareapi.com/en/skill/)

[Source](https://github.com/ashareapi/ashareapi-mcp) · [Issues](https://github.com/ashareapi/ashareapi-mcp/issues) · [Changelog](https://ashareapi.com/en/changelog/)

</div>

---

## What this is

An **A-share data MCP**: it packages China A-share data as **tools** an AI Agent can call directly. Configure it once and then just ask "how is the money flow on stock X today" — the agent calls the right tool itself and gets **real data**. No code to write, and no need to paste the usage docs into every conversation.

---

## 30-second quickstart

```bash
# 1) add to your client (Claude Code shown; other clients below)
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp

# 2) restart the client, then just ask:
#    "money flow for sh600519 today"
#    "last 30 daily candles for 600519"
#    "the 10 biggest gainers by turnover among today's limit-ups"
```

Free tools (quotes / K-lines / hot list / market overview / breadth / docs search) need **no key**.
For paid tools (financials / money flow / dragon-tiger / sectors / screening / backtests), add one header:

```bash
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp \
  --header "Authorization: Bearer ct-your-key"
```

---

## Why use it

- **94 tools, configured once**: quotes / K-lines / five-level order book / full-field profile / financials / money flow / dragon-tiger list / sectors / convertible bonds / ETFs / factor screening / quant backtests / abnormal moves / call auction — the mainstream A-share surface
- **No caching on intraday data**: every call re-fetches · `minute` intraday line (242 points/day) · `auction` call-auction series (09:15–09:25, ~150 points)
- **10 years of K-line history**: back to 2016-08-08; `kline_full` returns the whole series in one call (~2,500 bars); daily / weekly / monthly / quarterly / yearly plus minute bars `m1`–`m120`
- **Whole market in one call**: `market_kline` returns daily bars for **every A-share (5,000+) on a given trading day** — no 5,000-iteration loop
- **7 L2 microstructure tools**: market-wide main-force net-flow ranking **in one call (5,568 stocks)** · dragon-tiger seats **drilled to branch level** (with an `is_youzi` flag) · four-way large orders / add-cancel queue / 100-day large-order history
- **9 batch tools**: quotes / K-lines / snapshots / financials / technicals / chips / shareholders / money flow / company profile — **150 symbols in one call ≈ 2s**
- **One key, five markets**: A-shares + on-exchange ETFs (1,716) + HK + US + futures & FX (65 symbols)
- **Free tools really need no key**: `ashare_quote` / `ashare_kline` / `ashare_hot` / `ashare_market_overview` / `ashare_changedist` / `ashare_wiki_search` work right after install
- **Hosted endpoint, zero install**: one URL and you are in; local stdio self-hosting is also supported (intranet / read the source)
- **Tool descriptions written for the agent**: each tool states when to use it, how to fill the parameters and what comes back
- **Quant stack in one place**: 87 factors + 29 strategies + 25 playbooks + backtests (single / portfolio / batch) + portfolio weight optimisation
- **You are not charged for what you do not get**: empty results, failed fetches and mistyped codes cost **nothing**
- **Traceable failures**: every response carries a `trace_id`; quote it in a support request
- **Automatic source failover**: 70 data sources back each other up; a failed fetch switches source and **does not consume your quota**
- **No data ≠ failure**: a suspended stock and a failed fetch are returned differently, so the agent never misreads a suspension as an outage
- **Adjustment fixed server-side**: K-lines are forward-adjusted (no `adjust` parameter) — no double adjustment
- **Nothing for you to maintain**: failover / caching / health checks all live on the server

---
## Ways to connect (one key, several ways in)

| Way in | Install | Covers |
|---|---|---|
| **MCP (this repo)** | one URL: `https://api.ashareapi.com/mcp` | **19 clients** · **94 tools** |
| **Personal agents** | add MCP inside the assistant app | Today / Grok Bot / Muse / Dots / Duet |
| **Python SDK** | `pip install ashareapi` | scripts / backtests / data pipelines |
| **Node.js / TS SDK** | `npm install ashareapi` | services / frontends / cron jobs |
| **Agent Skill** | drop into your skills directory | works with 45+ clients |
| **Pi / DSH** | `npm install ashareapi-pi` / install the plugin | Pi · DeepSeek Harness |
| **HTTP** | plain `curl` | any language |

Same key, same quota, native — not a relay layer.

---

## Two ways to use it

| Option | Best for | Notes |
|---|---|---|
| **① Hosted endpoint** (recommended) | Most users | Server URL **`https://api.ashareapi.com/mcp`**, **nothing to install** |
| **② Run locally** (this repo) | Self-hosting / intranet deployment / reading the source | Run `mcp_ashare.py` from this repo over stdio |

> ⚠️ For the hosted endpoint use **`https://api.ashareapi.com/mcp`** — `ashareapi.com/en/mcp/` on the site is the **configuration guide**, not the endpoint URL.

**The fastest hosted setup** — a one-liner for Claude Code (other clients in the next section):

```bash
# free tools (no key needed)
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp

# to use paid tools (financials / money flow / Dragon-Tiger list…), add the request header
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp \
  --header "Authorization: Bearer ct-YOUR-KEY"

claude mcp list   # verify: it should show √ Connected (the tool count is not shown here — ask in a session)
```

**Or hand it to your AI Agent** — copy this line and send it:

> Please add this ashareapi MCP server for me: name `ashareapi`, type HTTP, URL `https://api.ashareapi.com/mcp`. Free tools need no key; to use paid tools add the request header `Authorization: Bearer ct-YOUR-KEY`. When done, confirm it connects and that 94 tools are visible.

**Restart your client after adding it** (or reopen the session) for the config to take effect — then just ask in the conversation, e.g. "check today's money flow for stock X".

---

## Personal agents (assistants on your phone)

No code — add one MCP inside the assistant app and ask about quotes, financials or candles.

| Assistant | Where | Auth |
|---|---|---|
| **Today** | Settings → Connected apps → Add custom MCP | Bearer token |
| **Grok Bot** | Connect apps → custom remote MCP | Bearer header |
| **Muse** | Settings → Connectors → Custom connector | Bearer / OAuth |
| **Dots** | add the connector in ChatGPT first | inherits ChatGPT |
| **Duet** | add the connector in Claude first | inherits Claude |

Fill in:

```
URL:       https://api.ashareapi.com/mcp
Transport: Streamable HTTP
Auth:      Authorization: Bearer <your key>
```

- Must be public HTTPS — **localhost is not supported**
- In a "Bearer" field put **only the key**, don't type `Bearer` again
- Only fall back to `?key=` when the client cannot set headers

Then just ask: "quote sh600519", "last 30 daily candles for 600519", "the 10 biggest gainers by turnover among today's limit-ups".
Full walkthrough: <https://ashareapi.com/docs/guides/personal-agent/>

---

## Supported clients

Config file locations (key names and file names were checked against each vendor's official docs):

| Client | Config file |
|---|---|
| Claude Code | `.mcp.json` |
| Cursor | `.cursor/mcp.json` |
| VS Code | `.vscode/mcp.json` |
| Codex | `~/.codex/config.toml` |
| OpenCode | `opencode.json` |
| Gemini CLI | `~/.gemini/settings.json` |
| Cline | `~/.cline/mcp.json` |
| Windsurf | `mcp_config.json` |
| CodeBuddy | `~/.codebuddy/.mcp.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` |
| Trae | Settings → MCP → manual config |
| Kimi Code | `~/.kimi/mcp.json` |
| ZCode | `~/.zcode/cli/config.json` |
| MiMo Code | `mimocode.json` |
| Kilo Code | `kilo.jsonc` |
| Manus | Settings → Integrations → custom MCP |
| Devin | `~/.config/devin/mcp_config.json` |
| OpenClaw | `~/.openclaw/openclaw.json` |
| Hermes | `~/.hermes/config.yaml` |

**China-based platforms** (same idea — fill in the URL + header, nothing to install): Alibaba Cloud Bailian · Coze · Tencent Yuanqi · Tencent Cloud Agent Development Platform · Volcano Ark

> The **exact configuration syntax** differs per client (key names are not the same — do not copy blindly): <https://ashareapi.com/en/mcp/>

---

## Running locally

### Requirements

- **Python ≥ 3.9**
- Dependencies: [`mcp`](https://pypi.org/project/mcp/) (**both 1.x and 2.x supported**) + [`requests`](https://pypi.org/project/requests/) (≥ 2.28)

```bash
pip install -r requirements.txt
```

### Configuration (Claude Desktop shown as an example)

```json
{
  "mcpServers": {
    "ashareapi": {
      "command": "python",
      "args": ["/path/to/mcp_ashare.py"],
      "env": {
        "ASHARE_API": "https://api.ashareapi.com",
        "ASHARE_KEY": "ct-xxxxxxxx"
      }
    }
  }
}
```

Once configured you can just say:

```
How much is 600667 right now?
Screen for stocks with PE<20 and ROE>15
What is the market doing today?
```

→ The AI Agent will call the tools below to get **real data** (not invented numbers).

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `ASHARE_API` | `https://api.ashareapi.com` | Server address (usually no need to change) |
| `ASHARE_KEY` | empty | API key. **Leaving it empty still gives you** the 6 free tools; paid tools require it ([get one](https://ashareapi.com/en/pricing/) from ¥9.9) |

### Self-test

```bash
python mcp_ashare.py --selftest     # calls the REST API directly to verify the tools work (does not start MCP)
```

---

## Docker image

Run it with Docker — no local setup (`ashareapi/mcp`, ~170 MB):

```bash
# MCP mode (stdio)
docker run -i --rm -e ASHARE_KEY=ct-your-key ashareapi/mcp

# Gateway mode (HTTP)
docker run -p 8080:8080 -e ASHARE_KEY=ct-your-key ashareapi/mcp gateway
```

The image contains **no data source**: everything comes from `https://api.ashareapi.com`, and the key is passed only via environment variables.
See [`docker/README.md`](docker/README.md) for build steps and options.

---

## The 94 tools

| Tool | Description | Key-free |
|---|---|---|
| `ashare_quote` | Real-time quote snapshot (last / open / high / low / volume / amount / turnover) | — |
| `ashare_quote_batch` | ⭐ **Batch quotes** (many symbols in one call, per-symbol success flagged · Pro ≤200 / Institutional ≤1000 · 300 symbols in ~4s) | Pro |
| `ashare_kline` | K-line (daily / weekly / monthly / quarterly / yearly + minute bars `m1`–`m120`) · adjustment fixed server-side | — |
| `ashare_kline_batch` | ⭐ **Batch K-line** (many symbols × one date range, per-symbol success flagged · Pro ≤200 / Institutional ≤1000 · 200 symbols × 30 bars in ~3.4s) | Pro |
| `ashare_minute` | **Intraday tick chart** (today / last 5 sessions) | Standard |
| `ashare_kline_full` | **Full-history K-line** (10 years of daily bars, from 2016-08-08) · adjustable `qfq` / `hfq` / `nofq` | Standard |
| `ashare_market_kline` | **Whole-market single-day K-line** (every A-share, 5,000+ symbols, for one day in one call — for daily incremental updates) | Pro |
| `ashare_backtest` | **Quant backtest** (single stock live / portfolio precomputed) · return / drawdown / trades / equity curve | Pro |
| `ashare_backtest_batch` | **Batch backtest** (many stocks × many strategies comparison matrix, ≤20×≤10) | Pro |
| `ashare_strategies` | Quant **strategy list** (20 single-stock + 9 portfolio, with parameter ranges) | Pro |
| `ashare_factors` | Quant **factor library** (88 factors + 50 screening shortcuts + 22 presets) | Pro |
| `ashare_playbooks` | Quant **playbook library** (13 "how to judge the market" workflows) | Pro |
| `ashare_hot` | Market-wide **heat board** (`type`: `stock` trending / `wx` whole-market heat board (A/HK/US + `pv` heat value) / `news` hot articles / `sector` / `etf`) | — |
| `ashare_news` | **Latest news for a symbol** (title + source + summary + link) — covers about 11 days, **no history paging**; use `ashare_notice` for historical filings | Standard |
| `ashare_flash` | **7x24 financial news flash** (market-wide, newest first, `index` paging, 1-min cache) | Standard |
| `ashare_evidence` | **Multi-source evidence** (CNINFO filings + Eastmoney news · cross-source dedupe · per-row `cit_value_hash`) | Pro |
| `ashare_agent_search` | **One-question data fetch + evidence chain** (natural language → our endpoints · returns data + `value_hash` · explicit refusal when unsupported) | Pro |
| `ashare_watchlist_list` | **List watchlist** (key-isolated; CRUD does not consume data quota) | Trial |
| `ashare_watchlist_add` | **Add to watchlist** (code `600519` / `sh600519`; idempotent) | Trial |
| `ashare_watchlist_remove` | **Remove from watchlist** | Trial |
| `ashare_watchlist_quotes` | **Batch quotes for watchlist** (1 data call) | — |
| `ashare_scanner` | **Stock Screener (scanner Agent)** (natural-language conditions → read-only tools → picks + citations + tool trace) · **BYOK**: also requires `ASHARE_LLM_KEY` · Pro ¥99+ · 2,000 scanner calls, separate from data quota | Pro |
| `ashare_analyst` | **Analyst Agent** (scanner snapshot → T+1/5/20 return / benchmark / excess / hit rate + review) · read-only · optional BYOK | Pro |
| `ashare_ask_user` | **Ask the user on ambiguity** (returns 1-4 described options · descriptions written by the model) | — |
| `ashare_notice` | **Filings**: without `id` returns the **list** (supports `type` / `limit` / `offset`, **reaching ~20 years back**); with `id` returns one announcement (title + date + **PDF link**) | Standard |
| `ashare_market_overview` | Market overview (profile / valuation / style rotation) | — |
| `ashare_changedist` | Advance-decline distribution (market breadth) | — |
| `ashare_orderbook` | 5-level order book (5 bid + 5 ask levels with sizes) | Trial |
| `ashare_snapshot` | Full-field quote profile (valuation / market cap / share capital / limit-up price) | Standard |
| `ashare_chip` | Chip distribution / holding cost (profit ratio · average cost · 90%/70% concentration · `date` for ~1 year of history) | Standard |
| `ashare_profile` | **Company profile** (listing date / main business / industry / website / registered capital / chairman) · 24h cache · use `ashare_profile_batch` for many | Trial |
| `ashare_snapshot_batch` | ⭐ **Batch full-field profile** (35+ fields for many symbols in one call, per-symbol success flagged · Pro ≤200 / Institutional ≤250 · 300 symbols in ~0.4s) | Pro |
| `ashare_profile_batch` | ⭐ **Batch company profile** (listing date / main business / industry / website / registered capital / chairman, many symbols in one call · Pro ≤100 / Institutional ≤150 · 100 symbols in ~6.8s) | Pro |
| `ashare_chip_batch` | ⭐ **Batch chip distribution** (profit ratio / average cost / 90%·70% concentration, many symbols in one call · Pro ≤200 / Institutional ≤300 · 200 symbols in ~3.9s) | Pro |
| `ashare_shareholder_batch` | ⭐ **Batch shareholder research** (top-10 holders / top-10 float holders / holder count, many symbols in one call · Pro ≤200 / Institutional ≤300 · 200 symbols in ~4.1s) | Pro |
| `ashare_finance_batch` | ⭐ **Batch financials** (income statement / balance sheet / cash flow, many symbols in one call · Pro ≤10 / Institutional ≤20 · 10 symbols × 4 periods in ~4.2s; the data source quota is tight, so split into batches) | Pro |
| `ashare_technical_batch` | ⭐ **Batch technical indicators** (MA / MACD / KDJ / RSI / BOLL and 45 more — 55 fields, many symbols in one call · Pro ≤500 / Institutional ≤1000 · 500 symbols in ~1.2s · BSE / HK / US / indices can be mixed) | Pro |
| `ashare_finance` | Financial statements (income statement / balance sheet / cash flow) | Trial |
| `ashare_fund` | Per-stock money flow + Dragon-Tiger list + block trades + margin trading (all from one call) | Trial |
| `ashare_fund_batch` | **Batch money flow** (many stocks in one call, per-symbol success flagged · Pro ≤200 / Institutional ≤1000) | Pro |
| `ashare_fund_flow` | **Per-stock money flow** (A-shares / HK): main vs retail buy / sell / net + average price, close · amounts in **CNY** · ⚠️ the only option for HK (`ashare_fund` is A-share only) | Pro |
| `ashare_fund_short` | **Short-selling data** (HK / US): shorted shares / amount / ratio · ⚠️ **pass `date`** (without it, and before the day's data is published, only identifier fields come back) · no short data for A-shares (use `ashare_margin_trade` for securities lending) | Pro |
| `ashare_fund_south` | **Southbound (Stock Connect) holdings** (quarterly): shares / holding ratio / market value · HK only · this is **quarterly holdings**, not daily flow — for daily net inflow use `ashare_fund_flow` | Pro |
| `ashare_lhb` | Dragon-Tiger sub-rankings (institutions / hot money / active seats) | Trial |
| `ashare_bigorder` | **L2 large-order flow** (per-minute net large-order amount · positive = net buying) · **Institutional tier only** | Institutional |
| `ashare_bigorder_flow` | **L2 large-order fills** (tick-level · **active/passive x buy/sell** · 300k-10M CNY threshold) · **Institutional tier only** | Institutional |
| `ashare_bigorder_flow_full` | **L2 large-order fills, full session** (whole day in one call · net inflow & 4-way amounts · de-duplicated) · **Institutional tier only** | Institutional |
| `ashare_bigorder_queue` | **L2 large-order queue** (pending orders · **cancel / limit-price flags** · 500-10k lots or 300k-10M CNY) · **Institutional tier only** | Institutional |
| `ashare_bigorder_history` | **L2 historical big-order net flow** (per day · up to **100 trading days** back · steady accumulation vs a one-day spike) · **Institutional tier only** | Institutional |
| `ashare_bigorder_split` | **L2 main-capital four-way split** (minute-level · **active/passive buy & sell** + **weighted average price** · history supported) · **Institutional tier only** | Institutional |
| `ashare_bigorder_rank` | **L2 whole-market main-capital ranking** (~**5,568 stocks** · 8 sort modes: net in/out, main buy/sell, gain/loss, turnover, market cap) · **Institutional tier only** | Institutional |
| `ashare_lhb_seats` | **Dragon-tiger seat detail** (branch buy / sell / net · **hot-money flag** · up to 10 seats) · **Institutional tier only** | Institutional |
| `ashare_lhb_agency` | **Institution-participation board** (whole market): every stock that institutional seats traded on the Dragon-Tiger list on a given day, in one call (~51 stocks/day measured) · `net_buy` institutional **net** buying (⚠️ negative = net selling) · `join_num` seats involved / change / amplitude / turnover / float & total cap / theme plates · ⭐ ask "what did institutions buy today" with this; ask "who bought this stock" with `ashare_lhb_seats` · **Institutional tier only** | Institutional |
| `ashare_margin_trade` | **Margin trading detail** (financing balance / buy / repay · short balance / sell / repay) · `code` accepts a comma list | Standard |
| `ashare_block_trade` | **Block trade detail** (price / premium-discount rate / buyer and seller branches) · leave `code` empty for the whole market | Standard |
| `ashare_technical` | Technical indicators: MA / MACD / KDJ / RSI / BOLL | Standard |
| `ashare_shareholder` | Shareholder research (top-10 holders / holder count / institutional holdings) | Standard |
| `ashare_consensus` | **Sell-side consensus**: analyst **target price** + forward estimates (EPS / revenue / net profit / forward PE·PB·PS / analyst coverage) · `codes` comma-separated, per-symbol `ok`, **≤15 per call** (more than that and the data source **silently drops rows**) · ⚠️ **HK has no target price**, only the `*Forecast` set | Pro |
| `ashare_rating` | **Sell-side ratings**: target price (mean / high / low) + rating distribution (buy / overweight / neutral / underweight / sell + analyst count) + **monthly rating trend** · ⚠️ **HK / US only** (A-shares return 422 — use `ashare_consensus`) | Pro |
| `ashare_score` | **Stock score** (A-shares only): fundamentals / technical / overall / money flow / risk — five dimensions, each with `value` + `chg_week`/`chg_month`/`chg_quarter` (0–100, higher is better) · already **structured**, ⛔ no string parsing needed · `date` goes back to late April 2026 only | Pro |
| `ashare_events` | Per-stock event tags (42 categories) | Standard |
| `ashare_screen` | Factor screening (multi-factor intersection / 22 presets) | Pro |
| `ashare_sector` | Sector performance board (industry / concept / region) | Trial |
| `ashare_sector_valuation` | Sector valuation (with historical percentile) | Trial |
| `ashare_industry_chain` | **Industry chain** (183 themes · `mode=list` themes / `graph` chain graph / `stock` stock position) | Trial |
| `ashare_macro` | Macro data (GDP / CPI / PMI / LPR / government bond yields) | Trial |
| `ashare_bond` | Convertible bond terms (premium rate / double-low / forced-redemption trigger) | Trial |
| `ashare_etf` | ETF data (`kind`: overview / detail / holdings / nav / company / holders / financial) | Standard |
| `ashare_stocks` | **Full A-share universe** (about 5,576 symbols in one call): code / name / market / listing date / industry / board / issue price / registered capital · filter with `market` / `industry`; page with `limit` / `offset` | Trial |
| `ashare_index_list` | **Full index list** (1,223 entries): code / name · paged with `limit` (≤500) + `offset` · A-share and HK indices mixed together (sh/sz/cs/hk prefixes) · feed the code to `ashare_index_constituent` | Pro |
| `ashare_index_constituent` | **Full index constituents** (CSI 300 / SSE 50 / CSI 500 / CSI 1000 / STAR 50 / ChiNext / Hang Seng …) · ⚠️ **names only, no weights** (use `ashare_etf(kind='holdings')` for weights) · index codes only, one per call · ⚠️ HK indices return **Chinese keys** (`代码`/`名称`/`涨跌幅`/`成交额`) — ⛔ do not parse them with the A-share key names | Standard |
| `ashare_ipo` | IPO calendar (issue / subscription / allotment / listing) | Standard |
| `ashare_calendar` | **Corporate event calendar** (dividends / lock-up release / earnings dates / IPOs / meetings / placements · ~1 month window · multi-section) | Trial |
| `ashare_disclosure` | **Scheduled earnings disclosure dates**: when results are released (`disclosureDate`) + reporting period (`reportEndDate`) + description · A-shares / HK / US · ⚠️ not the same as `ashare_calendar` (dividends / lock-ups / meetings) · **HK `disclosureDate` is often empty** — the date lives in the `disclosureDesc` text | Standard |
| `ashare_dividend` | Dividend and bonus-share history | Standard |
| `ashare_buyback` | **Share buyback records** (the company buying its own stock — different from `ashare_shareholder`, which is who holds it) · ⚠️ **the shape differs by market**: A-shares = event summary `code`/`name`/`market`; HK = daily detail `date`/`BuybackMoney`/`BuybackPrice`/`BuybackShares`/`BuybackCumMoney`/`closePrice` | Standard |
| `ashare_dehydrated` | Dehydrated research notes (broker report summaries) | Pro |
| `ashare_report` | **Sell-side research reports**: no `id` ⇒ list (title + broker + rating + type); with `id` ⇒ **full text** (Markdown, with financial commentary) · covers A-shares and HK · list is **≤20 per call** (`limit`>20 returns 422), page with `offset` · complements `ashare_dehydrated` (condensed summaries) | Pro |
| `ashare_search` | Stock / fund / sector search (fuzzy term disambiguation) | Trial |
| `ashare_usage` | Check your own usage and quota | — |
| `ashare_wiki_search` | **Product doc search** (field units / conventions / common misuse) — **look here first when unsure about a field** | — |
| `ashare_abnormal` | **Abnormal moves / deviation** (short-term regulatory signals: severe move trigger / 10-day 100% deviation / watchlist, 6 `mode`s) | Standard |
| `ashare_suspension` | **Suspension / resumption list** (A-shares / HK / US): which stocks are halted, which resumed, and why · `market` accepts 沪深/港股/美股 or hs/hk/us · ⚠️ **use this to filter out halted stocks** — factor/strategy screening does **not** exclude them, so cross-check your candidates against this list | Standard |
| `ashare_review` | **Short-term review** (limit-up structure: `mode=board` sector mainlines (theme + count + turnover) / `mode=ladder` consecutive-board ladder (grouped + reverse flag)) | Standard |
| `ashare_limit_up` | **Limit-up pool** (all limit-up stocks with **reason** / seal amount / main-capital net / concepts / turnover) | Standard |
| `ashare_auction` | **Call auction** (09:15–09:25 auction series + **"touched limit-up" flag** · `mode` 3 options: intraday series / historical second-level ticks / auction volume) | Pro |
| `ashare_market_mood` | **Market mood** (break rate + 9-day money-making trend): `break_count` / `break_rate`% / daily `success_rate`% and `profit_rate`% (may be negative) · **Institutional tier only** | Institutional |
| `ashare_limit_reason` | **Limit-up reasons** (per stock, historical): the **full reason text** for each limit-up + sector + "dragon rank of the day" · vs `ashare_limit_up`: that one covers today's whole market, this one is per-stock history · **Institutional tier only** | Institutional |
| `ashare_broken_board` | **Broken-board history** (limit-ups that got smashed open): `code` / `name` / `concepts` · complements `ashare_limit_up` (sealed vs broken) · empty `date` = latest weekday · **Institutional tier only** | Institutional |
| `ashare_tail_chase` | **Tail-end capital grab** (~292 stocks market-wide): `chase_amount` (CNY) / `theme` / `change_pct`% / `masked` flag · ⚠️ **upstream paywall**: the first 4 rows are masked (amounts intact) — do not treat `masked=true` rows as tradable symbols · **Institutional tier only** | Institutional |
| `ashare_northbound` | **Northbound holdings by sector** (quarterly): `plate_code` / `plate_name` + top-level `total_net` (CNY, may be negative) / `total_hold` · 🔴 **pass a quarter-end date** (e.g. 2026-09-30); empty = latest quarter-end · not the same as `ashare_fund_south` (HK southbound) · **Institutional tier only** | Institutional |
| `ashare_new_high` | **100-day new highs** (by theme): `theme` / `counts` string (e.g. `17,13`) / `plate_code` · **Institutional tier only** | Institutional |
| `ashare_futures` | **Overseas futures, one contract**: last / bid-ask / settlement / open interest and daily change / expiry / 52-week range / VWAP · codes such as `fuGC` (COMEX gold) / `fuCL` (crude) / `fuES` (S&P futures) · **Institutional** | Institutional |
| `ashare_forex` | **10 FX spot quotes**: `fxUSDCNY` / `fxCNH` / `fxEURUSD` / `fxGBPUSD` / `fxUSDJPY` / `fxUSDHKD` / `fxEURCNY` / `fxHKDCNY` / `fxCNYJPY` / `fxDINIW` · **Institutional** | Institutional |

> ⚠️ **K-line adjustment is fixed server-side** (there is **no** `adjust` parameter): forward-adjusted (qfq) for daily bars and above — no gaps on ex-dividend dates — and **raw** for minute bars. **Do not adjust them yourself** (that would double-adjust).
>
> ⚠️ **`ashare_minute` (tick chart) ≠ `ashare_kline` minute bars**: the former gives one price per minute plus cumulative volume; the latter gives OHLC candles.
>
> 💡 **Billing is per call**: `ashare_snapshot` gets valuation + market cap + share capital + limit-up price in one call, which is **cheaper in calls** than calling quote / valuation / orderbook separately.

---

## Return shapes

Each tool returns **readable text + structured data**, so the agent can use it directly:

| Case | Result |
|---|---|
| Data available | text summary + `structuredContent` (`data`, `endpoint`, `tier`, `elapsed_ms`) |
| No such data (e.g. suspended) | `ok:false` with an explicit "no data" note — **not a failure**, not billed |
| Fetch failed | `ok:false`, source already switched, **not billed** — retry once |
| Invalid parameters | 422 with the allowed values and how to fix |

---

## Error handling

| Symptom | Meaning | What to do |
|---|---|---|
| `401` / "key required" | paid tool called without a key | add `Authorization: Bearer <your key>` |
| `403` / "requires Pro" | tier too low (batch / L2 / futures & FX) | upgrade, or use a free/lower-tier tool |
| `422` | invalid parameters | follow the returned options — **do not retry** |
| `429` | rate limited | wait as instructed; the PoW raises the limit |
| `ok:false` without an error code | the symbol has no such data | try another symbol, not a failure |

> Every response carries a `trace_id` — quote it when reporting an issue.

---

## Examples

Once connected, just ask — the agent picks the tool itself:

```
"quote Moutai"  "last 30 daily candles for sh600519"
"the 10 biggest gainers by turnover among today's limit-ups"  "which sectors saw the largest inflows"
"latest financials for 600519: revenue / net profit / gross margin"
"screen stocks with PE<20 and ROE>15"
"gold price (fuGC)"  "USD/CNY (fxUSDCNY)"
```

---

## Development / testing

```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

The tests start the server once over the **real MCP protocol (stdio)** and read the tool list (**no network requests are made**).

---

## Requirements

| Item | Requirement |
|---|---|
| Hosted endpoint | any MCP client with Streamable HTTP; public HTTPS, **localhost is not supported** |
| Local run (this repo) | Python **3.9+** · `pip install -r requirements.txt` · `mcp` SDK 1.x / 2.x |
| Network | access to `https://api.ashareapi.com` |

---

## Version history

Current version **2026.11.24** (94 tools). Full changes in [CHANGELOG.md](CHANGELOG.md);
site changelog: <https://ashareapi.com/changelog>

---

## Related

**Official SDKs**: Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`

**Agent Skill** (an endpoint manual for AI Agents): <https://ashareapi.com/en/skill/>

---

## License

MIT · Data is for research reference only and is not investment advice
