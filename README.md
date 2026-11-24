<div align="center">

<a href="https://ashareapi.com"><img src="https://ashareapi.com/icon-512.png" width="88" height="88" alt="ashareapi"></a>

# ashareapi — A股数据 API 官方 MCP 服务器

让 Claude Code / Codex / Cursor / 任意 **AI Agent（MCP）**直接调用 A 股数据：**行情（分时 · 五档盘口）/ K线 / 财务 / 资金 / 龙虎榜 / L2 大单 / 板块 / 因子选股 / 量化回测 / 短线打板 / 集合竞价 / 资讯公告** —— **94 个工具，免费工具无需 Key**。

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

一个 **A股数据 MCP**：把 A 股数据变成 AI Agent 能直接调用的**工具**。配一次，之后你问「某某股票今天资金怎么样」，AI Agent 自己会去调对应工具拿**真实数据** —— 不用你写代码，也不用每次把用法贴给它。

---

## 30 秒上手

```bash
# 1) 加进客户端（Claude Code 示例，其他客户端见下节）
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp

# 2) 重启客户端，然后直接问：
#    「查一下 sh600519 今天的资金流向」
#    「600519 最近 30 天日 K」
#    「今天涨停里成交额最大的 10 只」
```

免费工具（行情 / K线 / 热搜 / 市场总览 / 涨跌分布 / 文档检索）**不用 Key**；
财务 / 资金 / 龙虎榜 / 板块 / 因子选股 / 量化回测等付费工具，加一行请求头即可：

```bash
claude mcp add --transport http ashareapi https://api.ashareapi.com/mcp \
  --header "Authorization: Bearer ct-你的KEY"
```

---

## 为什么用它

- **94 个工具，一次配好**：行情 / K线 / 五档盘口 / 全字段画像 / 财务 / 资金 / 龙虎榜 / 板块 / 可转债 / ETF / 因子选股 / 量化回测 / 异动偏离值 / 集合竞价 —— 覆盖 A 股主流面
- **盘中数据不缓存**：每次调用都重新取 · `minute` 分时（当日 242 点）· `auction` 集合竞价分时（9:15–9:25，约 150 个点）
- **K 线 10 年历史**：2016-08-08 起，`kline_full` 一次拿全（约 2,500 根），日 / 周 / 月 / 季 / 年 + 分钟线 `m1`–`m120`
- **全市场一次拿**：`market_kline` 一次返回某交易日**全部 A 股（5,000+ 只）**的日线 —— 不用循环 5,000 次
- **L2 微观结构 7 个工具**：全市场主力净额榜**一次 5,568 只** · 龙虎榜席位穿透到**营业部级**（带 `is_youzi`）· 大单四方向 / 挂撤单队列 / 100 日历史大单
- **批量工具 9 个**：行情 / K 线 / 快照 / 财务 / 技术 / 筹码 / 股东 / 资金流 / 公司简况，**一次 150 只约 2 秒**
- **一个 Key 覆盖 5 个市场**：A 股 + 场内 ETF（1,716 只）+ 港股 + 美股 + 期货外汇（65 个品种）
- **免费工具真的免 Key**：`ashare_quote` / `ashare_kline` / `ashare_hot` / `ashare_market_overview` / `ashare_changedist` / `ashare_wiki_search` 装上就能调
- **托管端点零安装**：填一个 URL 就能用；也可以本地 stdio 自托管（内网 / 想读源码）
- **工具描述写给 AI Agent 看**：每个工具都写清「什么时候用 / 参数怎么填 / 返回什么」，AI Agent 不会调错
- **量化五位一体**：87 因子 + 29 策略 + 25 方法论 + 回测（单标的 / 组合 / 批量）+ 组合权重优化
- **不该扣的就不扣**：空结果、取数失败、代码传错 —— 都**不计费**（按实际返回只数计）
- **出问题能定位**：每次响应带 `trace_id`，报障时报这个号，直接查到那一次请求
- **多源自动切换**：70 个数据源互为备份，某个源出问题会自动换下一个，且**不扣调用次数**
- **无数据 ≠ 失败**：停牌这类「市场真没数据」和「取数失败」分开返回 —— AI Agent 不会把停牌误判成故障
- **口径固定，不用二次处理**：K 线固定**前复权**（没有 `adjust` 参数），不会二次复权
- **不用你维护**：多源切换 / 缓存 / 巡检都在服务端，客户端装上就能用

---
## 接入方式（同一个 Key，多种用法）

| 方式 | 怎么装 | 覆盖 |
|---|---|---|
| **MCP（本仓）** | 填地址 `https://api.ashareapi.com/mcp` | **19 家客户端** · **94 个工具** |
| **Personal Agent** | 在助理 App 里加 MCP | Today / Grok Bot / Muse / Dots / Duet |
| **Python SDK** | `pip install ashareapi` | 脚本 / 回测 / 数据入库 |
| **Node.js / TS SDK** | `npm install ashareapi` | 服务端 / 前端 / 定时任务 |
| **Agent Skill** | 放进 skills 目录 | 45+ 客户端通用 |
| **Pi / DSH** | `npm install ashareapi-pi` / 装插件 | Pi · DeepSeek Harness |
| **HTTP** | 直接 `curl` | 任意语言 |

同一个 Key、同一份额度、同一套端点——每个入口都是原生支持。

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

> 帮我把这个 ashareapi MCP 服务器加上：名字 `ashareapi`，类型 HTTP，URL `https://api.ashareapi.com/mcp`。免费工具不用 Key；要用付费工具再加请求头 `Authorization: Bearer ct-你的KEY`。加完确认能连上、能看到 94 个工具。

**加完重启客户端**（或重开会话）配置才生效 —— 重启后直接在对话里问，例如「查一下某某股票今天的资金」。

---

## Personal Agent（手机上的个人助理）

不写代码，在助理 App 里配一个 MCP 就能问行情、财报、K 线。

| 助理 | 客户端入口 | 认证 |
|---|---|---|
| **Today** | 设置 → 连接应用 → 添加自定义 MCP | Bearer Token |
| **Grok Bot** | Connect apps → 自定义远程 MCP | Bearer Header |
| **Muse** | Settings → Connectors → Custom Connector | Bearer / OAuth |
| **Dots** | 先在 ChatGPT 里加 connector | 继承 ChatGPT |
| **Duet** | 先在 Claude 里加 connector | 继承 Claude |

统一填：

```
URL:       https://api.ashareapi.com/mcp
Transport: Streamable HTTP
Auth:      Authorization: Bearer <你的 Key>
```

- 必须公网 HTTPS，**不支持 localhost**
- Bearer 下拉框里**只填 Key**，不要再手写 `Bearer`
- 客户端不能填 Header 时，才用 `?key=` 作为后备

接上之后可以直接问：「查一下 sh600519 最新行情」「给我 600519 最近 30 天日 K」「今天涨停里成交额最大的 10 只」。
完整步骤见 <https://ashareapi.com/docs/guides/personal-agent/>

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

→ AI Agent 会自动调用下面的工具拿**真实数据**（不是编造）。

### 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `ASHARE_API` | `https://api.ashareapi.com` | 服务端地址（一般不用改） |
| `ASHARE_KEY` | 空 | API Key。**留空也能用** 6 个免费工具；付费工具必填（[获取](https://ashareapi.com/pricing)，¥9.9 起）|

### 自测

```bash
python mcp_ashare.py --selftest     # 直连 REST 验证工具可用性（不启 MCP）
```

---

## Docker 镜像

用 Docker 跑，不用配任何环境（镜像 `ashareapi/mcp`，约 170 MB）：

```bash
# MCP 模式（stdio）
docker run -i --rm -e ASHARE_KEY=ct-你的Key ashareapi/mcp

# 网关模式（HTTP，内网统一出口）
docker run -p 8080:8080 -e ASHARE_KEY=ct-你的Key ashareapi/mcp gateway
```

镜像里**不含任何数据源**：数据全部来自 `https://api.ashareapi.com`，Key 只通过环境变量传入。
细节（构建方式、环境变量、配置示例）见 [`docker/README.md`](docker/README.md)。

---

## 94 个工具

| 工具 | 说明 | 免 Key |
|---|---|---|
| `ashare_quote` | 实时行情快照（现价/开高低/量额/换手率）| — |
| `ashare_quote_batch` | ⭐ **批量行情**（一次拿多只，逐只标明成功与否 · 专业版 ≤200 只 / 机构版 ≤1000 只 · 300 只约 4 秒）| 专业版 |
| `ashare_kline` | K 线（日/周/月/季/年 + 分钟线 `m1`~`m120`）· 复权口径由服务端固定 | — |
| `ashare_kline_batch` | ⭐ **批量 K 线**（多只 × 同一段时间，逐只标明成功与否 · 专业版 ≤200 只 / 机构版 ≤1000 只 · 200 只×30 根约 3.4 秒）| 专业版 |
| `ashare_minute` | **分时**（当日 / 近 5 日盘中走势）| 标准版 |
| `ashare_kline_full` | **全历史 K 线**（10 年日线，2016-08-08 起）· 复权可选 `qfq`/`hfq`/`nofq` | 标准版 |
| `ashare_market_kline` | **全市场单日 K 线**（一次拿全 A 股 5000+ 只某日行情，用于每日增量更新） | 专业版 |
| `ashare_backtest` | **量化回测**（单标的实时 / 组合预计算）· 收益 / 回撤 / 交易次数 / 净值曲线 | 专业版 |
| `ashare_backtest_batch` | **批量回测**（多标的 × 多策略对比矩阵，≤20×≤10）| 专业版 |
| `ashare_strategies` | 量化**策略清单**（20 条单标的 + 9 条组合，含参数范围）| 专业版 |
| `ashare_factors` | 量化**因子库**（87 因子 + 50 筛选入口 + 22 预设）| 专业版 |
| `ashare_playbooks` | 量化**方法论库**（25 条「怎么判断市场」流程）| 专业版 |
| `ashare_hot` | 全市场**热度榜**（`type`：`stock` 热搜股票 / `wx` 全市场热度榜（跨 A/港/美 + `pv` 热度值）/ `news` 热文 / `sector` 板块 / `etf`）| — |
| `ashare_news` | 个股**最新资讯**（标题 + 来源 + 摘要 + 链接）—— 覆盖约 11 天，**无历史翻页**，要历史公告用 `ashare_notice` | 标准版 |
| `ashare_flash` | **7×24 财经快讯**（全市场电报 · 时间倒序 · `index` 翻页）| 标准版 |
| `ashare_evidence` | **财经多源取证**（上市公司公告 + 财经资讯 · 跨源去重 · 每行带 `cit_value_hash` 证据指纹）| 专业版 |
| `ashare_agent_search` | **一句话取数 + 证据链**（自然语言 → 数据端点 · 返回数据 + `value_hash` 可核验 · 不支持的问法明确拒答）| 专业版 |
| `ashare_watchlist_list` | **查自选股**（按 Key 隔离；CRUD 不扣数据次数）| 体验版 |
| `ashare_watchlist_add` | **加自选股**（代码 `600519`/`sh600519`；重复添加幂等）| 体验版 |
| `ashare_watchlist_remove` | **删自选股** | 体验版 |
| `ashare_watchlist_quotes` | **自选股批量行情**（正常扣 1 次数据额度）| — |
| `ashare_scanner` | **选股员（scanner Agent）**（自然语言条件 → 只读工具 → 候选池 + 引用 + 工具轨迹）· **BYOK**：另需环境变量 `ASHARE_LLM_KEY`（模型 Key）· 专业版 ¥99 起 · scanner 额度独立 2,000 次 | 专业版 |
| `ashare_analyst` | **复盘分析师（analyst Agent）**（scanner 快照 → T+1/5/20 收益/基准/超额/命中率 + 复盘）· 只读 · 可选 BYOK | 专业版 |
| `ashare_ask_user` | **歧义时向用户提问**（返回 1–4 个带说明的选项 · 由模型生成描述）| — |
| `ashare_notice` | **公告**：不传 `id` 取列表（支持 `type` / `limit` / `offset`，**可回溯约 20 年**）；传 `id` 取详情（标题 + 日期 + **PDF 链接**）| 标准版 |
| `ashare_market_overview` | 市场总览（画像/估值/风格轮动）| — |
| `ashare_changedist` | 涨跌分布（市场广度）| — |
| `ashare_orderbook` | 五档盘口（买五卖五 + 挂单量）| 体验版 |
| `ashare_snapshot` | 全字段行情画像（估值/市值/股本/涨停价）| 标准版 |
| `ashare_chip` | 筹码分布 / 持仓成本（获利盘比例 · 平均成本 · 90%/70% 集中度 · 可 `date` 回看近 1 年）| 标准版 |
| `ashare_profile` | **公司简况**（上市日期 / 主营业务 / 所属行业 / 官网 / 注册资本 / 董事长）· 缓存 24 小时 · 多只用 `ashare_profile_batch` | 体验版 |
| `ashare_snapshot_batch` | ⭐ **批量全字段画像**（多只一次取 35+ 字段，逐只标明成功与否 · 专业版 ≤200 只 / 机构版 ≤250 只 · 300 只约 0.4 秒）| 专业版 |
| `ashare_profile_batch` | ⭐ **批量公司简况**（上市日期 / 主营 / 行业 / 官网 / 注册资本 / 董事长，多只一次取 · 专业版 ≤100 只 / 机构版 ≤150 只 · 100 只约 6.8 秒）| 专业版 |
| `ashare_chip_batch` | ⭐ **批量筹码分布**（获利盘比例 / 平均成本 / 90%·70% 集中度，多只一次取 · 专业版 ≤200 只 / 机构版 ≤300 只 · 200 只约 3.9 秒）| 专业版 |
| `ashare_shareholder_batch` | ⭐ **批量股东研究**（十大股东 / 十大流通股东 / 股东户数统计，多只一次取 · 专业版 ≤200 只 / 机构版 ≤300 只 · 200 只约 4.1 秒）| 专业版 |
| `ashare_finance_batch` | ⭐ **批量财报**（利润表 / 资产负债表 / 现金流量表，多只一次取 · 专业版 ≤10 只 / 机构版 ≤20 只 · 10 只 × 4 期约 4.2 秒；财报数据源配额紧，超量请分批）| 专业版 |
| `ashare_technical_batch` | ⭐ **批量技术指标**（MA / MACD / KDJ / RSI / BOLL 等共 55 项，多只一次取 · 专业版 ≤500 只 / 机构版 ≤1000 只 · 500 只约 1.2 秒 · 支持北交所/港股/美股/指数混传）| 专业版 |
| `ashare_finance` | 财务报表（利润表 / 资产负债表 / 现金流量表）| 体验版 |
| `ashare_fund` | 个股资金 + 龙虎榜 + 大宗 + 两融（一接口拿全）| 体验版 |
| `ashare_fund_batch` | **批量资金流**（一次拿多只股票的资金面，逐只标明成功与否 · 专业版 ≤200 只 / 机构版 ≤1000 只）| 专业版 |
| `ashare_fund_flow` | **个股资金流向**（A 股 / 港股）：主力与散户的买入 / 卖出 / 净额 + 均价、收盘价 · 金额单位**元** · ⚠️ 港股只能用本工具（`ashare_fund` 仅 A 股）| 专业版 |
| `ashare_fund_short` | **卖空数据**（港股 / 美股）：卖空股数 / 金额 / 比率 · ⚠️ **请传 `date`**（不传且当日未发布时只回标识字段、无卖空数值）· A 股没有卖空数据（融券用 `ashare_margin_trade`）| 专业版 |
| `ashare_fund_south` | **港股通南下资金持仓**（季度）：持股数 / 持股比例 / 持股市值 · 仅港股 · 是**季度持仓**不是逐日流水，逐日净流入请用 `ashare_fund_flow` | 专业版 |
| `ashare_lhb` | 龙虎榜分榜（机构 / 游资 / 活跃席位）| 体验版 |
| `ashare_bigorder` | **L2 大单资金分时**（分钟级大单净额 · 正=净买入 / 负=净卖出 · 仅当日）· **机构版专属** | 机构版 |
| `ashare_bigorder_flow` | **L2 大单成交明细**（逐笔 · **主动/被动 × 买/卖** 四方向 · 金额阈值 30万~1000万）· **机构版专属** | 机构版 |
| `ashare_bigorder_flow_full` | **L2 大单成交·全天完整**（一次拿全当日全部大单 · 算主力净流入 / 四方向金额 · 自动去重）· **机构版专属** | 机构版 |
| `ashare_bigorder_queue` | **L2 大单委托流**（挂单明细 · **撤单/涨停标记** · 阈值 500手~1万手 / 30万~1000万）· **机构版专属** | 机构版 |
| `ashare_bigorder_history` | **L2 历史大单净额**（逐日 · 往回最多 **100 个交易日** · 看大单是持续吸还是只今天冲）· **机构版专属** | 机构版 |
| `ashare_bigorder_split` | **L2 主力四分解**（分钟级 · **主动买/被动买/主动卖/被动卖** + 买卖**加权均价** · 可回看历史）· **机构版专属** | 机构版 |
| `ashare_bigorder_rank` | **L2 全市场主力净额榜**（约 **5568 只** · 8 种排序：净流入/净流出/主买/主卖/涨跌/换手/市值）· **机构版专属** | 机构版 |
| `ashare_lhb_seats` | **龙虎榜席位明细**（营业部买入/卖出/净买额 · **游资标记** · 最多 10 席）· **机构版专属** | 机构版 |
| `ashare_lhb_agency` | **龙虎榜机构参与个股榜**（全市场）：某交易日**机构席位在龙虎榜参与过的所有个股**一次拿完（单日约 51 只）· `net_buy` 机构**净**买入额（⚠️ 负值 = 净卖出）· `join_num` 参与机构家数 / 涨幅 / 振幅 / 换手 / 流通·总市值 / 所属风口板块 · ⭐ 问「今天机构买什么」用本工具，问「这只票是谁买的」用 `ashare_lhb_seats` · **机构版专属** | 机构版 |
| `ashare_margin_trade` | **融资融券明细**（融资余额 / 买入 / 偿还 · 融券余额 / 卖出 / 偿还）· `code` 支持逗号批量 | 标准版 |
| `ashare_block_trade` | **大宗交易成交明细**（成交价 / 折溢价率 / 买卖方营业部）· `code` 留空 = 当日全市场 | 标准版 |
| `ashare_technical` | 技术指标 MA / MACD / KDJ / RSI / BOLL | 标准版 |
| `ashare_shareholder` | 股东研究（十大股东 / 股东户数 / 机构持仓）| 标准版 |
| `ashare_consensus` | **卖方一致预期**：分析师**目标价** + 未来预测（EPS / 营收 / 净利润 / 预测 PE·PB·PS / 机构覆盖数）· `codes` 逗号多只、逐只回 `ok`、单次 **≤15 只**（超了数据源**静默丢数据**）· ⚠️ **港股没有目标价**，只有 `*Forecast` 一套 | 专业版 |
| `ashare_rating` | **卖方机构评级**：目标价（均值/最高/最低）+ 评级分布（买入/增持/中性/减持/卖出 + 覆盖机构数）+ **评级月度趋势** · ⚠️ **仅港股 / 美股**（A 股 422，请用 `ashare_consensus`）| 专业版 |
| `ashare_score` | **股票评分**（仅 A 股）：基本面 / 技术 / 综合 / 资金 / 风险 五维，每维 `value` + `chg_week`/`chg_month`/`chg_quarter`（0~100，越高越好）· 已**结构化**，⛔ 不用自己解析字符串 · `date` 最早到 2026-04 下旬 | 专业版 |
| `ashare_events` | 个股事件标签（42 类）| 标准版 |
| `ashare_screen` | 因子选股（多因子交集 / 22 个预设）| 专业版 |
| `ashare_sector` | 板块行情榜（行业 / 概念 / 地域）| 体验版 |
| `ashare_sector_valuation` | 板块估值（含历史百分位）| 体验版 |
| `ashare_industry_chain` | **产业链**（183 个主题 · `mode=list` 主题列表 / `graph` 图谱 / `stock` 个股定位）| 体验版 |
| `ashare_macro` | 宏观数据（GDP / CPI / PMI / LPR / 国债收益率）| 体验版 |
| `ashare_bond` | 可转债条款（溢价率 / 双低 / 强赎触发价）| 体验版 |
| `ashare_etf` | ETF 数据（`kind`：概览 / 详情 / 持仓 / 净值 / 公司 / 持有人 / 财务）| 标准版 |
| `ashare_stocks` | **全市场股票清单**（一次拿全 A 股约 5576 只）：代码 / 名称 / 市场 / 上市日期 / 行业 / 板块 / 发行价 / 注册资本 · `market` / `industry` 过滤，`limit` / `offset` 分页 | 体验版 |
| `ashare_index_list` | **指数全量清单**（1223 个）：code / name · 分页 `limit`(≤500) + `offset` · A 股与港股指数混在一起（sh/sz/cs/hk 前缀）· 拿到代码后用 `ashare_index_constituent` 取成分股 | 专业版 |
| `ashare_index_constituent` | **指数成分股全量清单**（沪深300 / 上证50 / 中证500 / 中证1000 / 科创50 / 创业板指 / 恒生…）· ⚠️ **只有名单没有权重**（权重用 `ashare_etf(kind='持仓')`）· 只接受**指数代码**、一次 1 个 · ⚠️ 港股返回**中文键**（`代码`/`名称`/`涨跌幅`/`成交额`），⛔ 不能按 A 股键名解析 | 标准版 |
| `ashare_ipo` | 新股日历（发行 / 申购 / 中签 / 上市）| 标准版 |
| `ashare_calendar` | **个股事件日历**（分红派息 / 限售解禁 / 财报披露 / 新股 / 会议 / 增发 · 约 1 个月窗口 · 多段结构）| 体验版 |
| `ashare_disclosure` | **业绩预约披露日**：哪天披露财报（`disclosureDate`）+ 报告期（`reportEndDate`）+ 说明文案 · A 股 / 港股 / 美股 · ⚠️ 与 `ashare_calendar`（分红/解禁/会议）不是一回事 · **港股 `disclosureDate` 常为空**，日期写在 `disclosureDesc` 文案里 | 标准版 |
| `ashare_dividend` | 分红送转历史 | 标准版 |
| `ashare_buyback` | **公司股份回购记录**（公司自己买自己，区别于 `ashare_shareholder` 的谁持有）· ⚠️ **返回结构按市场不同**：A 股 = 事件概要 `code`/`name`/`market`；港股 = 逐日明细 `date`/`BuybackMoney`/`BuybackPrice`/`BuybackShares`/`BuybackCumMoney`/`closePrice` | 标准版 |
| `ashare_dehydrated` | 脱水研报（券商研报摘要）| 专业版 |
| `ashare_report` | **卖方研报**：不传 `id` ⇒ 列表（标题 + 机构 + 评级 + 类型）；传 `id` ⇒ **研报全文**（Markdown，含财务点评）· A 股 / 港股都覆盖 · 列表单次 **≤20 条**（`limit`>20 会 422），翻页用 `offset` · 与 `ashare_dehydrated`（脱水摘要）互补 | 专业版 |
| `ashare_search` | 股票 / 基金 / 板块搜索（模糊词消歧）| 体验版 |
| `ashare_usage` | 查询自己的用量与额度 | — |
| `ashare_wiki_search` | **产品文档检索**（字段单位 / 口径 / 常见误用）—— **不确定某字段含义时先查这里** | — |
| `ashare_abnormal` | **异动 / 偏离值**（短线监管异动：触发严重异动 / 10日100% 偏离 / 异动盯盘，`mode` 6 类）| 标准版 |
| `ashare_suspension` | **停复牌清单**（沪深 / 港股 / 美股）：哪些票停牌、哪些复牌、停牌原因 · `market` 传中文（沪深/港股/美股）或 hs/hk/us · ⚠️ **选股过滤停牌股用这个** —— 因子/策略筛选**不剔除停牌**，拿到候选后与本清单交叉核对 | 标准版 |
| `ashare_review` | **短线复盘**（涨停结构：`mode=board` 板块主线（题材 + 涨停数 + 成交额）/ `mode=ladder` 连板梯队（按板分组 + 反包标记））| 标准版 |
| `ashare_limit_up` | **短线打板**（涨停池明细：全量涨停股 + **涨停原因** / 封单额 / 主力净额 / 概念 / 换手）| 标准版 |
| `ashare_auction` | **集合竞价**（个股 9:15–9:25 竞价分时 + **竞价触及涨停判定** · `mode` 3 类：当日分时 / 历史秒级逐笔 / 竞价量额）| 专业版 |
| `ashare_market_mood` | **市场情绪**（破板率 + 赚钱效应 9 日趋势）：`break_count` 破板家数 / `break_rate` 破板率% / 9 日 `success_rate` 成功率% + `profit_rate` 盈利概率%（可为负）· **机构版专属** | 机构版 |
| `ashare_limit_reason` | **涨停原因**（单只票历史）：每次涨停的**完整原因文案** + 所属板块 + 当日「日内龙几」· 与 `ashare_limit_up` 分工：涨停池看今天全市场，本工具看单票历史 · **机构版专属** | 机构版 |
| `ashare_broken_board` | **炸板历史**（某日被砸开的涨停）：`code` / `name` / `concepts` 概念 · 与 `ashare_limit_up` 互补（封住的 vs 没封住的）· `date` 留空 = 最近工作日 · **机构版专属** | 机构版 |
| `ashare_tail_chase` | **尾盘抢筹**（全市场约 292 只）：`chase_amount` 抢筹金额（元）/ `theme` 题材 / `change_pct` 涨幅% / `masked` 打码标记 · ⚠️ **上游付费墙**：头 4 行代码名打码（金额完整），`masked=true` 勿当标的 · **机构版专属** | 机构版 |
| `ashare_northbound` | **A 股北向分板块持仓**（季度）：`plate_code` / `plate_name` + 顶层 `total_net` 净额（元，可为负）/ `total_hold` 总持仓 · 🔴 **须传季度末**（如 2026-09-30），留空自动取最近季度末 · 与 `ashare_fund_south`（港股通南下）不同 · **机构版专属** | 机构版 |
| `ashare_new_high` | **百日新高**（按题材）：`theme` 题材 / `counts` 家数字符串（如 `17,13`）/ `plate_code` · 新高家数多的题材 = 资金主线 · ⚠️ `counts` 两个家数含义未确认，原样给出 · **机构版专属** | 机构版 |
| `ashare_futures` | **外盘期货单合约快照**：最新价 / 买一卖一 / 结算价 / 持仓量与当日增减 / 到期日 / 52 周高低 / VWAP · 代码如 `fuGC`（COMEX 黄金）/ `fuCL`（原油）/ `fuES`（标普期货）· **机构版** | 机构版 |
| `ashare_forex` | **10 个外汇现货报价**：`fxUSDCNY` / `fxCNH` / `fxEURUSD` / `fxGBPUSD` / `fxUSDJPY` / `fxUSDHKD` / `fxEURCNY` / `fxHKDCNY` / `fxCNYJPY` / `fxDINIW` · **机构版** | 机构版 |

> ⚠️ **K 线复权口径由服务端固定**（**没有** `adjust` 参数）：日线及以上为**前复权**（除权除息日不跳空），分钟线为**不复权** —— **不要再自己复权**（会二次复权）。
>
> ⚠️ **`ashare_minute`（分时）≠ `ashare_kline` 的分钟线**：前者是每分钟一个价+累计量，后者是 OHLC 蜡烛。
>
> 💡 **计费 = 次数**：`ashare_snapshot` 一次拿全估值+市值+股本+涨停价，比分别调 quote / valuation / orderbook **更省次数**。

---

## 返回形态

工具返回的是**可读文本 + 结构化数据**，AI Agent 直接读，不需要你再解析：

| 情况 | 返回 |
|---|---|
| 有数据 | 文本摘要 + `structuredContent`（含 `data` 数组、`endpoint`、`tier`、`elapsed_ms`） |
| 该标的无此数据（如停牌） | `ok:false` + 明确说明「数据不存在」—— **不是故障**，不扣次数 |
| 取数失败 | `ok:false` + 已自动换源，**不扣次数**，重试一次通常就好 |
| 参数不合法 | 422 + 可用取值清单 + 怎么改 |

---

## 错误处理

| 现象 | 含义 | 怎么办 |
|---|---|---|
| `401` / 「需要 Key」 | 调了付费工具但没带 Key | 请求头加 `Authorization: Bearer <你的 Key>` |
| `403` / 「需要专业版」 | 档位不够（批量 / L2 / 期货外汇） | 升档，或改用免费/低档工具 |
| `422` | 参数不合法（代码写错 / 取值越界） | 按返回的可选取值改，**不要重试** |
| `429` | 频率超限 | 按提示等待；解 PoW 可提额 |
| `ok:false` 但无错误码 | 该标的确实没这项数据（停牌等） | 换标的，不是故障 |

> 每次响应带 `trace_id`，报障时报这个号即可定位那一次请求。

---

## 示例

配好之后，直接在对话里问（AI Agent 会自己挑工具）：

```
「茅台今天多少」「sh600519 最近 30 天日 K」
「今天涨停里成交额最大的 10 只」「哪些板块资金净流入最多」
「600519 的最新财报：营收 / 净利 / 毛利率」
「帮我筛 PE<20 且 ROE>15 的股票」
「黄金现在多少（fuGC）」「美元人民币多少（fxUSDCNY）」
```

---

## 开发 / 测试

```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

测试会以**真实 MCP 协议（stdio）**起一次服务端并取工具清单（**不发起任何网络请求**）。

---

## 环境要求

| 项 | 要求 |
|---|---|
| 托管端点 | 任意支持 Streamable HTTP 的 MCP 客户端；公网 HTTPS，**不支持 localhost** |
| 本地运行（本仓） | Python **3.9+** · `pip install -r requirements.txt` · `mcp` SDK 1.x / 2.x |
| 网络 | 能访问 `https://api.ashareapi.com` |

---

## 版本记录

当前版本 **2026.11.24**（94 个工具）。完整变更见 [CHANGELOG.md](CHANGELOG.md)；
站点更新日志：<https://ashareapi.com/changelog>

---

## 相关

**官方 SDK**：Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`

**Agent Skill**（给 AI Agent 读的接口说明书）：<https://ashareapi.com/skill>

---

## License

MIT · 数据仅供研究参考，不构成投资建议
