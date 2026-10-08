<div align="center">

<a href="https://ashareapi.com"><img src="https://ashareapi.com/icon-512.png" width="88" height="88" alt="ashareapi"></a>

# ashareapi — A股数据 API 官方 MCP 服务器

让 Claude Code / Codex / Cursor / 任意 **AI Agent（MCP）**直接调用 A 股数据：行情 / K线 / **五档盘口** / 财务 / 资金 / 龙虎榜 / 板块 / 可转债 / 因子选股 / 宏观 / **量化回测** —— **31 个工具，免费工具无需 Key**。

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![MCP SDK](https://img.shields.io/badge/mcp%20SDK-1.x%20%7C%202.x-6E56CF)
[![CI](https://github.com/ashareapi/ashareapi-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ashareapi/ashareapi-mcp/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green)

**中文** · [English](README.en.md)

**支持 19 家主流 AI Agent 客户端** —— 开箱即用：

![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-D97757?logo=claude&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-supported-000000?logo=cursor&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-supported-007ACC)
![Codex](https://img.shields.io/badge/Codex-supported-000000)
![OpenCode](https://img.shields.io/badge/OpenCode-supported-000000?logo=opencode&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-supported-8E75B2?logo=googlegemini&logoColor=white)
![Cline](https://img.shields.io/badge/Cline-supported-18181B?logo=cline&logoColor=white)
![Windsurf](https://img.shields.io/badge/Windsurf-supported-0B100F?logo=windsurf&logoColor=white)

[官网](https://ashareapi.com) · [文档](https://ashareapi.com/docs/) · [端点清单](https://ashareapi.com/endpoints/) · [MCP 接入](https://ashareapi.com/mcp) · [Agent Skill](https://ashareapi.com/skill)

[GitHub 源码](https://github.com/ashareapi/ashareapi-mcp) · [问题反馈 Issues](https://github.com/ashareapi/ashareapi-mcp/issues) · [更新日志](https://ashareapi.com/changelog)

</div>

---

## 这是什么

一个 **A股数据 MCP**：把 A 股数据封装成 AI Agent 能直接调用的**工具**。配一次，之后你问「某某股票今天资金怎么样」，Agent 自己会去调对应工具拿**真实数据** —— 不用你写代码，也不用每次把用法贴给它。

---

## 为什么用它

- **31 个工具，一次配好**：行情 / K线 / 五档盘口 / 全字段画像 / 财务 / 资金 / 龙虎榜 / 板块 / 宏观 / 可转债 / ETF / 因子选股 / **量化回测** —— 覆盖 A 股主流面
- **免费工具真的免 Key**：`ashare_quote` / `ashare_kline` / `ashare_hot` / `ashare_market_overview` / `ashare_changedist` 装上就能调，不用先买 Key
- **托管端点零安装**：填一个 URL 就能用；也可以本地 stdio 自托管（内网 / 想读源码）
- **多源自动切换**：后端 70 个数据源互为备份，某个源出问题会自动换下一个，且**不扣调用次数**
- **工具描述写给 AI 看**：每个工具都写清「什么时候用 / 参数怎么填 / 返回什么」，Agent 不会调错
- **无数据 ≠ 失败**：停牌这类「市场真没数据」和「取数失败」分开返回 —— Agent 不会把停牌误判成故障
- **口径固定，不用二次处理**：K 线固定**前复权**（没有 `adjust` 参数），不会二次复权
- **不用你维护**：多源切换 / 缓存 / 巡检都在服务端，客户端只负责调用

---

## 两种用法

| 方式 | 适合 | 说明 |
|---|---|---|
| **① 托管端点**（推荐） | 大多数用户 | 服务器地址 **`https://api.ashareapi.com/mcp`**，**不用装任何东西** |
| **② 本地运行**（本仓） | 想自己托管 / 内网部署 / 想读源码 | 跑本仓的 `mcp_ashare.py`，走 stdio |

> ⚠️ 托管端点填 **`https://api.ashareapi.com/mcp`** —— 站点上的 `ashareapi.com/mcp` 是**配置说明页**，不是接口地址。

**托管端点最快的接法** —— Claude Code 一行命令（其他客户端见下节）：

```bash
# 免费工具（无需 Key）
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp

# 要用付费工具（财务 / 资金 / 龙虎榜…）再加请求头
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp \
  --header "Authorization: Bearer ct-你的KEY"

claude mcp list   # 验证：应显示 √ Connected（不显示工具数，工具在会话里让它列）
```

**或者交给你的 AI Agent** —— 复制这句话发给它：

> 帮我把这个 ashareapi MCP 服务器加上：名字 `ashareapi`，类型 HTTP，URL `https://api.ashareapi.com/mcp`。免费工具不用 Key；要用付费工具再加请求头 `Authorization: Bearer ct-你的KEY`。加完确认能连上、能看到 31 个工具。

**加完重启客户端**（或重开会话）配置才生效 —— 重启后直接在对话里问，例如「查一下某某股票今天的资金」。

---

## 支持的客户端

配置文件位置（键名与文件名都逐家核对过官方文档）：

| 客户端 | 配置文件 |
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
| Trae | 设置 → MCP → 手动配置 |
| Kimi Code | `~/.kimi/mcp.json` |
| ZCode | `~/.zcode/cli/config.json` |
| MiMo Code | `mimocode.json` |
| Kilo Code | `kilo.jsonc` |
| Manus | 设置 → 集成 → 自定义 MCP |
| Devin | `~/.config/devin/mcp_config.json` |
| OpenClaw | `~/.openclaw/openclaw.json` |
| Hermes | `~/.hermes/config.yaml` |

**国内平台**（同样填 URL + 请求头，无需安装任何东西）：阿里云百炼 · 扣子 Coze · 腾讯元器 · 腾讯云智能体开发平台 · 火山方舟

> 各家**完整配置写法**（键名不一样，别照抄）：<https://ashareapi.com/mcp>

---

## 本地运行

### 环境要求

- **Python ≥ 3.9**
- 依赖：[`mcp`](https://pypi.org/project/mcp/)（**1.x 与 2.x 都支持**）+ [`requests`](https://pypi.org/project/requests/)（≥ 2.28）

```bash
pip install -r requirements.txt
```

### 配置（以 Claude Desktop 为例）

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

配置好之后可以直接说：

```
查一下 600667 现在多少钱
帮我筛一下 PE<20 且 ROE>15 的股票
今天市场什么情况
```

→ AI 会自动调用下面的工具拿**真实数据**（不是编造）。

### 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `ASHARE_API` | `https://api.ashareapi.com` | 服务端地址（一般不用改） |
| `ASHARE_KEY` | 空 | API Key。**留空也能用** 5 个免费工具；付费工具必填（[获取](https://ashareapi.com/pricing)，¥9.9 起）|

### 自测

```bash
python mcp_ashare.py --selftest     # 直连 REST 验证工具可用性（不启 MCP）
```

---

## 31 个工具

| 工具 | 说明 | 免 Key |
|---|---|---|
| `ashare_quote` | 实时行情快照（现价/开高低/量额/换手率）| ✅ |
| `ashare_kline` | K 线（日/周/月/季/年 + 分钟线 `m1`~`m120`）· 复权口径由服务端固定 | ✅ 日线及以上 / 分钟线付费 |
| `ashare_minute` | **分时**（当日 / 近 5 日盘中走势）| — |
| `ashare_kline_full` | **全历史 K 线**（10 年日线，2016-08-08 起）· 复权可选 `qfq`/`hfq`/`nofq` | — |
| `ashare_backtest` | **量化回测**（单标的实时 / 组合预计算）· 收益 / 回撤 / 交易次数 / 净值曲线 | — |
| `ashare_backtest_batch` | **批量回测**（多标的 × 多策略对比矩阵，≤20×≤10）| — |
| `ashare_strategies` | 量化**策略清单**（20 条单标的 + 9 条组合，含参数范围）| — |
| `ashare_factors` | 量化**因子库**（88 因子 + 50 筛选入口 + 22 预设）| — |
| `ashare_playbooks` | 量化**方法论库**（13 条「怎么判断市场」流程）| — |
| `ashare_hot` | 热搜榜 | ✅ |
| `ashare_market_overview` | 市场总览（画像/估值/风格轮动）| ✅ |
| `ashare_changedist` | 涨跌分布（市场广度）| ✅ |
| `ashare_orderbook` | 五档盘口（买五卖五 + 挂单量）| — |
| `ashare_snapshot` | 全字段行情画像（估值/市值/股本/涨停价）| — |
| `ashare_finance` | 财务报表（利润表 / 资产负债表 / 现金流量表）| — |
| `ashare_fund` | 个股资金 + 龙虎榜 + 大宗 + 两融（一接口拿全）| — |
| `ashare_lhb` | 龙虎榜分榜（机构 / 游资 / 活跃席位）| — |
| `ashare_technical` | 技术指标 MA / MACD / KDJ / RSI / BOLL | — |
| `ashare_shareholder` | 股东研究（十大股东 / 股东户数 / 机构持仓）| — |
| `ashare_events` | 个股事件标签（42 类）| — |
| `ashare_screen` | 因子选股（多因子交集 / 22 个预设）| — |
| `ashare_sector` | 板块行情榜（行业 / 概念 / 地域）| — |
| `ashare_sector_valuation` | 板块估值（含历史百分位）| — |
| `ashare_macro` | 宏观数据（GDP / CPI / PMI / LPR / 国债收益率）| — |
| `ashare_bond` | 可转债条款（溢价率 / 双低 / 强赎触发价）| — |
| `ashare_etf` | ETF 行情 / 规模 / 溢折率 / 资金流 | — |
| `ashare_ipo` | 新股日历（发行 / 申购 / 中签 / 上市）| — |
| `ashare_dividend` | 分红送转历史 | — |
| `ashare_dehydrated` | 脱水研报（券商研报摘要）| — |
| `ashare_search` | 股票 / 基金 / 板块搜索（模糊词消歧）| — |
| `ashare_usage` | 查询自己的用量与额度 | — |

> ⚠️ **K 线复权口径由服务端固定**（**没有** `adjust` 参数）：日线及以上为**前复权**（除权除息日不跳空），分钟线为**不复权** —— **不要再自己复权**（会二次复权）。
>
> ⚠️ **`ashare_minute`（分时）≠ `ashare_kline` 的分钟线**：前者是每分钟一个价+累计量，后者是 OHLC 蜡烛。
>
> 💡 **计费 = 次数**：`ashare_snapshot` 一次拿全估值+市值+股本+涨停价，比分别调 quote / valuation / orderbook **更省次数**。

---

## 开发 / 测试

```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

测试会以**真实 MCP 协议（stdio）**起一次服务端并取工具清单（**不发起任何网络请求**）。

---

## 相关

**官方 SDK**：Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`

**Agent Skill**（给 AI 读的接口说明书）：<https://ashareapi.com/skill>

---

## License

MIT · 数据仅供研究参考，不构成投资建议
