<div align="center">

<a href="https://ashareapi.com/en/"><img src="https://ashareapi.com/icon-512.png" width="88" height="88" alt="ashareapi"></a>

# ashareapi — Official MCP Server for the A-Share Data API

Let Claude Code / Codex / Cursor / any **AI agent (MCP)** query China A-share data directly: quotes / K-lines / **5-level order book** / financials / money flow / Dragon-Tiger list / sectors / convertible bonds / factor screening / macro / **quant backtests** — **31 tools, and the free tools need no key**.

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![MCP SDK](https://img.shields.io/badge/mcp%20SDK-1.x%20%7C%202.x-6E56CF)
[![CI](https://github.com/ashareapi/ashareapi-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ashareapi/ashareapi-mcp/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green)

**Works with 19 mainstream AI agent clients** — out of the box:

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

An **A-share data MCP**: it packages China A-share data as **tools** an AI agent can call directly. Configure it once and then just ask "how is the money flow on stock X today" — the agent calls the right tool itself and gets **real data**. No code to write, and no need to paste the usage docs into every conversation.

---

## Why use it

- **31 tools, configured once**: quotes / K-lines / 5-level order book / full-field profile / financials / money flow / Dragon-Tiger list / sectors / macro / convertible bonds / ETFs / factor screening / **quant backtests** — covering the mainstream surface of the A-share market
- **Free tools are genuinely key-free**: `ashare_quote` / `ashare_kline` / `ashare_hot` / `ashare_market_overview` / `ashare_changedist` work right after installation, no key purchase needed
- **Hosted endpoint, zero install**: just fill in a URL; you can also self-host locally over stdio (for intranets or if you want to read the source)
- **Automatic source failover**: 70 data sources back each other up on the backend; if one has a problem it switches to the next, and **your quota is not charged**
- **Tool descriptions written for AI**: every tool states *when to use it / how to fill the parameters / what it returns*, so the agent does not call it wrong
- **No data ≠ failure**: "the market genuinely has no data" (e.g. a suspended stock) is returned separately from "the fetch failed" — the agent will not mistake a suspension for an outage
- **Fixed conventions, no post-processing**: K-line adjustment is fixed server-side (there is no `adjust` parameter) — forward-adjusted (qfq) for daily bars and above, raw for minute bars — so there is no double-adjustment
- **Nothing for you to maintain**: source failover / caching / health checks all live server-side; the client just calls

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

**Or hand it to your AI agent** — copy this line and send it:

> Please add this ashareapi MCP server for me: name `ashareapi`, type HTTP, URL `https://api.ashareapi.com/mcp`. Free tools need no key; to use paid tools add the request header `Authorization: Bearer ct-YOUR-KEY`. When done, confirm it connects and that 31 tools are visible.

**Restart your client after adding it** (or reopen the session) for the config to take effect — then just ask in the conversation, e.g. "check today's money flow for stock X".

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

→ The AI will call the tools below to get **real data** (not invented numbers).

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `ASHARE_API` | `https://api.ashareapi.com` | Server address (usually no need to change) |
| `ASHARE_KEY` | empty | API key. **Leaving it empty still gives you** the 5 free tools; paid tools require it ([get one](https://ashareapi.com/en/pricing/) from ¥9.9) |

### Self-test

```bash
python mcp_ashare.py --selftest     # calls the REST API directly to verify the tools work (does not start MCP)
```

---

## The 31 tools

| Tool | Description | Key-free |
|---|---|---|
| `ashare_quote` | Real-time quote snapshot (last / open / high / low / volume / amount / turnover) | ✅ |
| `ashare_kline` | K-line (daily / weekly / monthly / quarterly / yearly + minute bars `m1`–`m120`) · adjustment fixed server-side | ✅ daily and above / paid for minute bars |
| `ashare_minute` | **Intraday tick chart** (today / last 5 sessions) | — |
| `ashare_kline_full` | **Full-history K-line** (10 years of daily bars, from 2016-08-08) · adjustable `qfq` / `hfq` / `nofq` | — |
| `ashare_backtest` | **Quant backtest** (single stock live / portfolio precomputed) · return / drawdown / trades / equity curve | — |
| `ashare_backtest_batch` | **Batch backtest** (many stocks × many strategies comparison matrix, ≤20×≤10) | — |
| `ashare_strategies` | Quant **strategy list** (20 single-stock + 9 portfolio, with parameter ranges) | — |
| `ashare_factors` | Quant **factor library** (88 factors + 50 screening shortcuts + 22 presets) | — |
| `ashare_playbooks` | Quant **playbook library** (13 "how to judge the market" workflows) | — |
| `ashare_hot` | Hot-search ranking | ✅ |
| `ashare_market_overview` | Market overview (profile / valuation / style rotation) | ✅ |
| `ashare_changedist` | Advance-decline distribution (market breadth) | ✅ |
| `ashare_orderbook` | 5-level order book (5 bid + 5 ask levels with sizes) | — |
| `ashare_snapshot` | Full-field quote profile (valuation / market cap / share capital / limit-up price) | — |
| `ashare_finance` | Financial statements (income statement / balance sheet / cash flow) | — |
| `ashare_fund` | Per-stock money flow + Dragon-Tiger list + block trades + margin trading (all from one call) | — |
| `ashare_lhb` | Dragon-Tiger sub-rankings (institutions / hot money / active seats) | — |
| `ashare_technical` | Technical indicators: MA / MACD / KDJ / RSI / BOLL | — |
| `ashare_shareholder` | Shareholder research (top-10 holders / holder count / institutional holdings) | — |
| `ashare_events` | Per-stock event tags (42 categories) | — |
| `ashare_screen` | Factor screening (multi-factor intersection / 22 presets) | — |
| `ashare_sector` | Sector performance board (industry / concept / region) | — |
| `ashare_sector_valuation` | Sector valuation (with historical percentile) | — |
| `ashare_macro` | Macro data (GDP / CPI / PMI / LPR / government bond yields) | — |
| `ashare_bond` | Convertible bond terms (premium rate / double-low / forced-redemption trigger) | — |
| `ashare_etf` | ETF quotes / size / premium-discount / money flow | — |
| `ashare_ipo` | IPO calendar (issue / subscription / allotment / listing) | — |
| `ashare_dividend` | Dividend and bonus-share history | — |
| `ashare_dehydrated` | Dehydrated research notes (broker report summaries) | — |
| `ashare_search` | Stock / fund / sector search (fuzzy term disambiguation) | — |
| `ashare_usage` | Check your own usage and quota | — |

> ⚠️ **K-line adjustment is fixed server-side** (there is **no** `adjust` parameter): forward-adjusted (qfq) for daily bars and above — no gaps on ex-dividend dates — and **raw** for minute bars. **Do not adjust them yourself** (that would double-adjust).
>
> ⚠️ **`ashare_minute` (tick chart) ≠ `ashare_kline` minute bars**: the former gives one price per minute plus cumulative volume; the latter gives OHLC candles.
>
> 💡 **Billing is per call**: `ashare_snapshot` gets valuation + market cap + share capital + limit-up price in one call, which is **cheaper in calls** than calling quote / valuation / orderbook separately.

---

## Development / testing

```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

The tests start the server once over the **real MCP protocol (stdio)** and read the tool list (**no network requests are made**).

---

## Related

**Official SDKs**: Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`

**Agent Skill** (an endpoint manual for AI agents): <https://ashareapi.com/en/skill/>

---

## License

MIT · Data is for research reference only and is not investment advice
