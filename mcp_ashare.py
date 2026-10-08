"""A股数据 API 的 MCP Server —— 让 AI / LLM / Agent **直接消费**数据。

配置（Claude Desktop / Cursor / Dify / 任意 MCP 客户端）：

```json
{
  "mcpServers": {
    "ashare": {
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

配置后可以直接说：
  "查一下 600667 现在多少钱"
  "帮我筛一下 PE<20 且 ROE>15 的股票"
  "今天市场什么情况"
→ AI 自动调用下面的工具拿真实数据（不是编造）。

自测：python mcp_ashare.py --selftest
"""
import asyncio
import json
import os
import sys

import requests

API = os.environ.get("ASHARE_API", "https://api.ashareapi.com").rstrip("/")
KEY = os.environ.get("ASHARE_KEY", "").strip()
_PRICING_URL = "https://ashareapi.com/pricing"

# 服务版本：格式 `YYYY.M.D`（**不补零**，否则不是合法 SemVer），取值 = CHANGELOG.md 最新条目的日期。
# 必须显式声明 —— 不传时 SDK 会用它自己的版本兜底，用户报上来的版本号就无法用于排查。
SERVER_VERSION = "2026.10.8"

# ── 工具定义（表驱动：name → (路径, 说明, 参数 schema)）─────────
def _p(name, typ, desc, required=False):
    d = {"type": typ, "description": desc}
    return name, d, required


TOOLS = {
    "ashare_quote": (
        "/v1/quote",
        ("A股/港股/美股实时行情快照（**轻量 8 字段**：现价/开高低/成交量/成交额/换手率）。"
         "用户问'某股票现在多少钱/什么价'用这个。"
         "⚠️ `data` 是**数组**（默认 30 条日线，`data[0]` 为最新）—— 取现价用 `data[0].last`。"
         "⚠️ 换手率的字段名是 **`turnover`**（%）—— 与 /v1/snapshot **同名同值**。"
         "⚠️ **不含**估值/市值 —— 用 ashare_snapshot（35 字段，付费）。"
         "要**历史走势**请用 ashare_kline；要**五档盘口（order book）**请用 ashare_orderbook。"
         "只读查询；交易时段内实时。"
         "· 免费工具（无需 Key）"),
        [_p("code", "string", "股票代码，带市场前缀：sh600667 / sz000001 / hk00700", True)],
    ),
    "ashare_orderbook": (
        "/v1/orderbook",
        ("**五档盘口**：买一~买五 / 卖一~卖五的**价格与挂单量（手）** + 现价/涨跌/数据时间。"
         "用户问'封单多少/买盘卖盘/盘口/挂单/支撑压力位/有没有大单托着'用这个。"
         "字段：`b1_p`/`b1_v`~`b5_p`/`b5_v` 买档价格/量 · `a1_p`/`a1_v`~`a5_p`/`a5_v` 卖档。"
         "⚠️ 本工具是**秒级快照**（每 10 秒刷新），**盘中才有意义**（收盘后为当日最后快照）——"
         "要**实时成交价**用 ashare_quote（**免费**，字段少更轻）。"
         "⚠️ 量单位是**手**（×100 = 股）；**跌停买档全 0 / 涨停卖档全 0**（正常）。"),
        [_p("code", "string", "股票代码：sh600667", True)],
    ),
    "ashare_snapshot": (
        "/v1/snapshot",
        ("**全字段行情画像**：价格 + 盘口（买五卖五+委差）+ 估值（PE TTM/动/静 + PB）+ "
         "市值（流通/总）+ 股本（流通/总）+ 打板（涨停/跌停价 + 量比 + 振幅 + 涨速）+ "
         "标识（证券类型/股票状态/币种）+ 外盘/内盘。"
         "用户问'这股票估值怎么样/PE PB 多少/市值多大/股本多少/涨停价多少/涨停跌停板在哪'用这个。"
         "⚠️ **与 ashare_quote 的分工**：quote 轻（8 字段）**免费**；本工具**全（35 字段）· 付费**——"
         "**只要现价/涨跌用 ashare_quote 更轻**（字段少、省上下文）。"
         "✅ **计费 = 次数**：本工具 1 次拿全——要估值+市值+股本+涨停价**多项**时，"
         "比分别调 quote/valuation/orderbook **更省次数**（3 次 → 1 次）。"
         "⚠️ **仅 A 股**（港股/美股字段布局不同，用 ashare_quote）——**传其他市场返回空，不返回错数据**。"
         "⚠️ 单位：量=手 · 成交额=万元 · 市值=亿元 · 股本=股 · 比率=百分数。"),
        [_p("code", "string", "A 股代码：sh600667 / 600667 / sz300750", True)],
    ),
    "ashare_kline": (
        "/v1/kline",
        ("K线（日/周/月/季/年 + 分钟线）。用户问'走势/最近表现/历史K线/趋势'用这个。"
         "⚠️ 只要**当前价**用 ashare_quote；要**分时**（盘中每分钟价+累计量）用 ashare_minute ——"
         "**分钟 K 线**（OHLC 蜡烛）用本工具的 `period=m1/m5/...`，两者不是一回事。"
         "⚠️ 换手率字段名是 **`turnover`**（%）—— 与 ashare_quote、ashare_snapshot 同名同值。"
         "⚠️ 复权口径由服务端固定（无 `adjust` 参数）：日线及以上**前复权**（除权除息日不跳空），"
         "分钟线**不复权** —— **不要再自己复权**（会二次复权）。"
         "⚠️ **分钟线属付费层**（日/周/月免费），必须同时传 `start`+`end`（窗口近 1 个月），"
         "不支持 北交所 / 期货 / 外汇。"
         "只读查询；按收盘更新。"
         "· 免费工具（无需 Key）· 分钟线除外"),
        [_p("code", "string", "股票代码：sh600667", True),
         _p("period", "string", "周期：day / week / month / season / year / m1 / m5 / m15 / m30 / m60 / m120（默认 day）"),
         _p("count", "integer", "条数（默认 30，最大 1212）"),
         _p("start", "string", "起始日期 YYYY-MM-DD（仅 day 与分钟线；须与 end 配对；分钟线必填）"),
         _p("end", "string", "结束日期 YYYY-MM-DD（仅 day 与分钟线；须与 start 配对；分钟线必填）")],
    ),
    "ashare_kline_full": (
        "/v1/kline-full",
        ("全历史K线（**10 年日线**，2016-08-08 起）+ **可选复权口径**。"
         "用户问'十年走势/长期回测/全历史数据/复权价/后复权/原始价'用这个。"
         "⚠️ 与 ashare_kline 的**三点不同**："
         "① 数据量与范围 —— 本工具**全历史 10 年**（2465 条）；ashare_kline 上限 1212 条；"
         "② 复权可选 —— 本工具有 **`fq`** 参数（qfq 前复权 / hfq 后复权 / nofq 原始价）；"
         "ashare_kline **写死前复权、无参数**；"
         "③ 标的范围 —— 本工具**仅 A 股股票**（⛔ ETF/可转债/指数/板块/港股/美股/期货/外汇"
         "传进来会**明确报错**，请改用 ashare_kline）。"
         "⚠️ 做**回测**请用 `fq=hfq` 或 `fq=nofq`（前复权序列会随新的除权除息重算，不可复现）。"
         "⚠️ 字段固定 7 列：`time open high low close volume amount`（**无 turnover**）。"
         "⚠️ **付费工具**（需 Key）—— 门槛为 **Standard（¥29.9）及以上**，"
         "Trial（¥9.9）不可用；且有**独立日额度**（Standard 200 / Pro 500 / Unlimited 2000"
         " 次/天），余量可查 ashare_usage。"),
        [_p("code", "string", "A股代码：sh600667 / sz000001 / bj920047（⛔ 不支持 ETF/指数/板块/港美股）", True),
         _p("fq", "string", "复权：qfq 前复权（默认）/ hfq 后复权 / nofq 原始价"),
         _p("start", "string", "起始日期 YYYY-MM-DD（省略 = 从 2016-08-08）"),
         _p("end", "string", "结束日期 YYYY-MM-DD（省略 = 到最新）")],
    ),
    "ashare_minute": (
        "/v1/minute",
        ("**分时**（当日 / 近 5 日盘中走势）：盘中每分钟的价格与累计成交量。"
         "用户问'今天分时/盘中走势/日内走势/近 5 日分时'用这个。"
         "⚠️ 与 ashare_kline 的**分钟 K 线不是一回事**：本工具返回**分时**（每分钟一个价+累计量），"
         "K 线返回 OHLC 蜡烛 —— 要蜡烛图用 ashare_kline 的 `period=m1/m5/...`。"
         "⚠️ `days` **只有 1（当日）和 5（近 5 个交易日）两档**，没有 2/3/4。"
         "⚠️ **付费工具**（需 Key）。"),
        [_p("code", "string", "股票代码：sh600667（同样支持 指数/板块/ETF/港股/美股/可转债）", True),
         _p("days", "integer", "档位：1 = 当日（默认）· 5 = 近 5 个交易日")],
    ),
    "ashare_backtest": (
        "/v1/backtest",
        ("**量化回测**：按策略跑历史收益（返回收益/最大回撤/交易次数/净值曲线等）。"
         "用户问'回测一下/这个策略收益如何/买卖点效果/最大回撤'用这个。"
         "⚠️ 两种模式：`mode=single`（默认）**单标的实时计算**，须配 `code`；"
         "`mode=portfolio` **组合**（须用 `strategies` 里的组合策略，区间受预置批次限制）。"
         "⚠️ `weighting=inv_vol`（按波动率倒数配仓）**仅组合模式 + 不限量版**可用。"
         "⚠️ 想知道有哪些策略/参数范围，先调 ashare_strategies；"
         "想一次跑多标的×多策略，用 ashare_backtest_batch。"
         "⚠️ **付费工具**（需 Key）：单标的 **Standard（¥29.9）起**；"
         "组合 / 批量回测为 **Pro 及以上**，且有独立日额度，余量可查 ashare_usage。"),
        [_p("strategy", "string", "策略名（如 buy_hold / mom20 / lowvol20；清单见 ashare_strategies）", True),
         _p("mode", "string", "single 单标的实时（默认，须配 code）/ portfolio 组合（预置区间）"),
         _p("code", "string", "股票代码：sh600667（mode=single 时必填）"),
         _p("start", "string", "起始日期 YYYY-MM-DD（mode=single 时可用）"),
         _p("end", "string", "结束日期 YYYY-MM-DD（mode=single 时可用）"),
         _p("initial_cash", "number", "初始资金（默认 1000000 = 100 万）"),
         _p("weighting", "string", "组合配仓：equal 等权（默认）/ inv_vol 波动率倒数（仅组合模式 + 不限量版）"),
         _p("include_equity", "boolean", "是否返回净值曲线（默认 false —— 曲线数据量大，只在需要画图时开）")],
    ),
    "ashare_backtest_batch": (
        "/v1/backtest-batch",
        ("**批量回测**：一次跑 **多标的 × 多策略**，返回对比矩阵（哪个组合最好一目了然）。"
         "用户问'这几只股票用不同策略分别跑一下/批量回测/策略对比'用这个。"
         "⚠️ 与 ashare_backtest 的区别：本工具**一次给多标的×多策略的横向对比**，"
         "ashare_backtest 只跑**一个**策略。"
         "⚠️ 上限：标的 ≤20 · 策略 ≤10 · 组合 ≤60（**超限直接报错，不静默截断**）。"
         "⚠️ 组合策略不能用于批量回测（批量只支持单标的择时策略）。"
         "⚠️ 参数可传**列表**（自动转逗号）。"
         "⚠️ **付费工具**（需 Key）：**Pro（¥69）及以上**，有独立日额度。"),
        [_p("codes", "string", "股票代码，多个用逗号分隔：sh600667,sz000001（≤20 只）", True),
         _p("strategies", "string", "策略名，多个用逗号分隔：buy_hold,mom20（≤10 个）", True),
         _p("start", "string", "起始日期 YYYY-MM-DD（默认 2019-01-01）"),
         _p("end", "string", "结束日期 YYYY-MM-DD"),
         _p("initial_cash", "number", "初始资金（默认 1000000 = 100 万）")],
    ),
    "ashare_strategies": (
        "/v1/strategies",
        ("**量化策略清单**：返回可回测的全部策略（20 条单标的择时 + 9 条组合），含各自参数范围与说明。"
         "用户问'有哪些策略/能跑哪些策略/策略参数是什么'用这个。"
         "⚠️ 这是**清单**（静态元数据，不跑计算）；要真跑回测用 ashare_backtest。"
         "⚠️ **付费工具**（需 Key）：**Standard（¥29.9）及以上**。"),
        [],
    ),
    "ashare_factors": (
        "/v1/factors",
        ("**量化因子库**：88 个因子 + 50 个筛选入口 + 22 个预设组合，可按分类/类型筛选。"
         "用户问'有哪些因子/因子库/选股因子/因子分类'用这个。"
         "⚠️ 这是**清单**（静态元数据）；要用因子实际选股，用 ashare_screen。"
         "⚠️ `category` / `kind` **只接受中文枚举值**"
         "（category：估值/行情/盈利/成长/财务/资金…；kind：排行/标签/事件）。传英文会返回空。"
         "⚠️ **付费工具**（需 Key）：**Standard（¥29.9）及以上**。"),
        [_p("category", "string", "按分类筛选（**中文值**：估值/行情/盈利/成长…；省略=全部）"),
         _p("kind", "string", "按类型筛选（**中文值**：排行/标签/事件；省略=全部）")],
    ),
    "ashare_playbooks": (
        "/v1/playbooks",
        ("**量化方法论库**：13 条「怎么判断市场」的流程（含判据 / 阶段 / 实测证据）。"
         "用户问'怎么判断/交易方法/方法论/判断流程'用这个。"
         "⚠️ 这是**方法论清单**（帮助判断，非投资建议）；要看可回测的策略用 ashare_strategies。"
         "⚠️ 可按分类或 id 取单条。"
         "⚠️ **付费工具**（需 Key）：**Standard（¥29.9）及以上**。"),
        [_p("category", "string", "按分类筛选（省略=全部）"),
         _p("id", "string", "取单条方法论（省略=返回全部）")],
    ),
    "ashare_finance": (
        "/v1/finance",
        ("财务报表（利润表/资产负债表/现金流量表，**最近 N 期**）。用户问'营收/净利润/毛利率/负债/财务数据'用这个。"
         "⚠️ 返回**三张表**：data[0]=利润表 · data[1]=资产负债表 · data[2]=现金流量表；"
         "每表按期次**降序**（最新一期在最前）。"
         "⚠️ 只要估值倍数（PE/PB）请用 ashare_sector_valuation 或 ashare_quote 的估值字段。"
         "只读查询；按财报披露节奏更新（未到披露日就没有新数据，不是故障）。"),
        [_p("code", "string", "股票代码：sh600667", True),
         _p("num", "integer", "期数（默认 4，最近 N 期）")],
    ),
    "ashare_fund": (
        "/v1/fund",
        ("个股级交易面：这只股的 主力资金（当日/5/10/20 日净流入+全市场排名）+ 龙虎榜上榜明细"
         "（上榜原因/营业部）+ 大宗交易 + 融资融券。用户问'某只股票的主力资金/机构动向'用这个。"
         "⚠️ 全市场榜单（今天机构榜/游资榜/活跃席位）请用 ashare_lhb——本工具只针对单只股票。"),
        [_p("code", "string", "股票代码：sh600667", True)],
    ),
    "ashare_technical": (
        "/v1/technical",
        ("技术指标 MA/MACD/KDJ/RSI/BOLL。用户问'技术面/指标/金叉死叉/超买超卖'用这个。"
         "⚠️ 只要原始 K 线（不算指标）请用 ashare_kline——本工具返回已算好的指标值。"
         "只读查询；按日线收盘更新。"),
        [_p("code", "string", "股票代码：sh600667", True)],
    ),
    "ashare_shareholder": (
        "/v1/shareholder",
        ("股东研究：十大股东/股东户数（筹码集中度）/机构持仓。用户问'谁在持有/股东变化/筹码集中/机构持仓'用这个。"
         "⚠️ 要看机构**整体**在全市场买什么，请用 ashare_lhb 的机构榜。"
         "只读查询；股东户数按定期报告披露（季度级）。"),
        [_p("code", "string", "股票代码：sh600667", True)],
    ),
    "ashare_events": (
        "/v1/events",
        ("个股事件标签（42 类：大宗/龙虎榜/回购/分红/解禁等）。用户问'这只股票最近有什么大事/解禁/回购/定增'用这个。"
         "⚠️ 要看**全市场**某一类事件名单，请用 ashare_lhb（龙虎榜分榜）或 ashare_dividend（分红送转）"
         "——本工具是**单只股票**的事件总览。只读查询；按披露节奏更新。"),
        [_p("code", "string", "股票代码：sh600667", True)],
    ),
    "ashare_lhb": (
        "/v1/lhb",
        ("全市场龙虎榜分榜：type=institution 机构榜（机构买入/净买/机构数）/ hotmoney 游资榜 / "
         "activeseat 活跃席位。用户问'今天机构买了什么/游资动向/活跃席位'用这个。"
         "⚠️ 某只股票的上榜明细（上榜原因/营业部）请用 ashare_fund——本工具是市场级榜单，不针对单只股票。"),
        [_p("type", "string", "榜单类型（默认 institution）")],
    ),
    "ashare_screen": (
        "/v1/screen",
        ("因子选股（量化筛股）。expression 是多因子交集表达式，"
         "例：intersect([PE_TTM > 0, PE_TTM < 20, ROETTM > 15])；"
         "常用字段：PE_TTM/PB/PS_TTM/ROE/ROETTM/ROIC/DividendRatioTTM/"
         "OperatingRevenueGrowRate/DebtAssetsRatio。用户问'筛选/选股/符合条件的股票'用这个。"),
        [_p("expr", "string", "因子表达式，如 intersect([PE_TTM>0, PE_TTM<20])"),
         _p("orderby", "string", "排序字段（如 ROETTM）"),
         _p("limit", "integer", "条数（默认 20）")],
    ),
    "ashare_sector": (
        "/v1/sector",
        ("板块行情榜（行业/概念/地域涨幅 + 领涨股 + 涨跌家数）。用户问'哪些板块在涨/板块轮动/"
         "行业热度'用这个。⚠️ 要板块**估值分位**请用 ashare_sector_valuation；要**产业链上下游**请用"
         "对应工具。只读查询；交易时段内更新。"),
        [],
    ),
    "ashare_sector_valuation": (
        "/v1/sector-valuation",
        ("板块估值（PE/PB/PS/PCF + 股息率 + 历史百分位）。用户问'某板块贵不贵/估值分位'用这个。"
         "⚠️ 要看板块**涨跌幅与领涨股**请用 ashare_sector——本工具只给估值指标。"
         "只读查询；板块代码形如 pt01801780（pt 前缀 + 8 位）。"),
        [_p("code", "string", "板块代码：pt01801780", True)],
    ),
    "ashare_market_overview": (
        "/v1/market-overview",
        ("市场级画像。type=summary 画像总评/trade 收盘/interval 多周期/technical 大盘技术/"
         "valuation 估值分位/rotation 风格轮动。用户问'今天市场怎么样/大盘环境/风格轮动/估值分位'用这个。"
         "⚠️ 涨跌家数（市场广度）请用 ashare_changedist：本工具的 updown 模块为 **T-1 口径**"
         "（返回里会标数据日期，可能滞后一个交易日），已不推荐用于回答'今天的涨跌家数'。"
         "· 免费工具（无需 Key）"),
        [_p("type", "string", "类型（默认 summary；涨跌家数请改用 ashare_changedist）")],
    ),
    "ashare_changedist": (
        "/v1/changedist",
        ("全市场涨跌家数与市场广度（**当期口径**）：上涨/下跌/平盘/停牌家数 + 上涨占比 + 涨停/跌停 + "
         "11 档涨跌幅区间分布 + 两市成交额。用户问'今天涨跌家数/多少家涨停/市场情绪/市场广度'用这个"
         "——这是市场广度的**唯一推荐入口**。"
         "⚠️ 不要用 ashare_market_overview 的 updown 模式取同一数据（那是 T-1 口径，数值会与此不一致）。"
         "· 免费工具（无需 Key）"),
        [],
    ),
    "ashare_hot": (
        "/v1/hot",
        "热搜榜（A股/美股/ETF 关注度）。用户问'什么股票热门/大家在看什么'用这个。· 免费工具（无需 Key）",
        [_p("limit", "integer", "条数（默认 30，上限 50）")],
    ),
    "ashare_macro": (
        "/v1/macro",
        ("宏观数据（GDP/CPI/PMI/LPR/国债收益率/财政）。用户问'宏观/经济数据/利率/LPR/CPI'用这个。"
         "⚠️ 要**指数行情**请用 ashare_quote 或 ashare_market_overview——本工具只给宏观指标。"
         "只读查询；按发布日历更新（未到发布日就没有新值）。"),
        [_p("region", "string", "地区（默认 cn）"),
         _p("names", "string", "指标短名（如 cn_gdp/cn_cpi_ppi/cn_lpr）")],
    ),
    "ashare_bond": (
        "/v1/bond",
        ("可转债完整条款：溢价率/转股价值/双低值/强赎触发价/回售触发价/转股价/正股/到期日/评级。"
         "用户问'转债条款/强赎/双低/溢价'用这个。⚠️ 要转债**行情价**请用 ashare_quote（同样支持转债代码）。"
         "只读查询；代码形如 sh113052（沪）/ sz123138（深）。"),
        [_p("code", "string", "转债代码：sh113052", True)],
    ),
    "ashare_etf": (
        "/v1/etf",
        ("ETF 行情/规模/溢折率/资金流。用户问'ETF'时用这个。"
         "⚠️ 要 ETF 的**成分股/净值/持有人**请用对应端点（本工具给运作概览）。"
         "只读查询；代码形如 sh510300。"),
        [_p("code", "string", "ETF 代码：sh510300", True)],
    ),
    "ashare_ipo": (
        "/v1/ipo",
        ("新股日历（发行/申购/中签/上市）。用户问'新股/打新/IPO'用这个。"
         "只读查询；按发行日历更新。"),
        [_p("days", "integer", "天数（默认 15）")],
    ),
    "ashare_dividend": (
        "/v1/dividend",
        ("分红送转历史（每股分红/送股/除权日）。用户问'分红/股息/送转'用这个。"
         "⚠️ 要**分红派息日历**（哪天除权）请用 ashare_events——本工具是历史记录。"
         "只读查询；按公告披露更新。"),
        [_p("code", "string", "股票代码：sh600667", True),
         _p("years", "integer", "年数（默认 3）")],
    ),
    "ashare_dehydrated": (
        "/v1/dehydrated",
        ("脱水研报（券商研报摘要）。用户问'研报/机构观点/券商怎么说'用这个。"
         "mode=list 列表 / mode=detail 详情（detail 需给 symbol）。"
         "⚠️ 要**个股新闻/公告**请用 ashare_events。只读查询；按研报发布更新。"),
        [_p("mode", "string", "list / detail（默认 list）"),
         _p("symbol", "string", "股票代码（detail 时用）"),
         _p("limit", "integer", "条数（默认 10）")],
    ),
    "ashare_search": (
        "/v1/search",
        ("股票/基金/板块搜索（模糊词消歧）。用户只给名称时**先用这个确认代码**。"
         "⚠️ 本工具只返回代码与名称，不含行情——拿到代码后再调 ashare_quote / ashare_kline。"
         "只读查询。"),
        [_p("q", "string", "关键词，如 '太极实业' 或 '600667'", True)],
    ),
    "ashare_usage": (
        "/v1/usage",
        ("查自己的 API 用量与剩余额度（今日调用次数/剩余总量/到期时间/限流额度）。"
         "用户问'我的额度还剩多少/今天调了多少次'用这个。只读查询；需 API Key。"),
        [],
    ),
}


def _call(path: str, **params):
    """调我们的 REST API。"""
    p = {k: v for k, v in params.items() if v not in (None, "")}
    h = {"Authorization": f"Bearer {KEY}"} if KEY else {}
    try:
        r = requests.get(API + path, params=p, headers=h, timeout=45)
        return r.status_code, r.text
    except Exception as e:
        return 0, json.dumps({"error": f"请求失败: {type(e).__name__}: {e}"},
                             ensure_ascii=False)


def _friendly(status: int, text: str) -> str:
    """匿名（未配 Key）时，把 REST 的 401/429 原文换成"该怎么做"的提示。

    措辞与托管端点 `https://api.ashareapi.com/mcp` 保持一致；配了 Key 就原样返回。
    """
    if not KEY:
        if status == 401:
            return ("该工具属付费层，需要 API Key。请在 MCP 客户端配置里把 "
                    "`ASHARE_KEY` 设成你的 Key（体验版 ¥9.9 起，26 个工具全开）。"
                    "免费工具（行情快照 / K线 / 热搜 / 市场总览 / 涨跌分布）无需 Key 即可用。"
                    f"档位与购买：{_PRICING_URL}")
        if status == 429:
            return ("匿名额度已用完（5 次/分 · 每天最多 10 万条，免费工具共享）。"
                    "继续高频使用请配置 API Key："
                    "在 MCP 客户端配置里把 `ASHARE_KEY` 设成你的 Key"
                    f"（体验版 ¥9.9 起）。档位与购买：{_PRICING_URL}")
    return text


# ── MCP 接线（同一份工具表，兼容 mcp SDK 1.x 与 2.x）────────────────────────
#  1.x：`Server(...)` + `@server.list_tools()` / `@server.call_tool()` 装饰器注册
#  2.x：`Server(..., on_list_tools=…, on_call_tool=…)` 回调注册
#  两版只差在「工具怎么挂上去」—— TOOLS 表与 _call 跟协议层解耦，
#  换 SDK 大版本不必动工具定义。
def build_server():
    from mcp.server.lowlevel import Server
    from mcp.server.stdio import stdio_server
    from mcp import types

    def _tool_list():
        out = []
        for name, (path, desc, ps) in TOOLS.items():
            props, req = {}, []
            for pname, schema, required in ps:
                props[pname] = schema
                if required:
                    req.append(pname)
            out.append(types.Tool(
                name=name,
                description=f"{desc}（额度消耗 1 次）",
                inputSchema={"type": "object", "properties": props,
                             **({"required": req} if req else {})}))
        return out

    async def _invoke(name: str, arguments) -> str:
        """执行一次工具调用，返回给客户端的文本。"""
        if name not in TOOLS:
            return f"未知工具：{name}"
        status, text = await asyncio.to_thread(_call, TOOLS[name][0], **(arguments or {}))
        return _friendly(status, text)

    if hasattr(Server, "list_tools"):          # ── mcp SDK 1.x：装饰器式
        server = Server("ashare-data-api", version=SERVER_VERSION)

        @server.list_tools()
        async def list_tools():
            return _tool_list()

        @server.call_tool()
        async def call_tool(name: str, arguments: dict):
            return [types.TextContent(type="text",
                                      text=await _invoke(name, arguments))]

    else:                                      # ── mcp SDK 2.x：回调式
        async def on_list_tools(ctx, params):
            return types.ListToolsResult(tools=_tool_list())

        async def on_call_tool(ctx, params):
            text = await _invoke(params.name, params.arguments)
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=text)])

        server = Server("ashare-data-api",
                        version=SERVER_VERSION,
                        on_list_tools=on_list_tools,
                        on_call_tool=on_call_tool)

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream,
                             server.create_initialization_options())

    return main


def selftest():
    """自测：直连 REST 验证工具可用性（不启 MCP）。"""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"API = {API}")
    print(f"KEY = {KEY[:12]}..." if KEY else "KEY = (未设，走匿名免费层)")
    print(f"工具数 = {len(TOOLS)}")
    cases = [("ashare_quote", {"code": "sh600667"}),
             ("ashare_hot", {"limit": 3}),
             ("ashare_market_overview", {"type": "summary"}),
             ("ashare_screen", {"expr": "intersect([PE_TTM > 0, PE_TTM < 20, ROETTM > 15])",
                               "orderby": "ROETTM", "limit": 3})]
    for name, args in cases:
        path = TOOLS[name][0]
        st, body = _call(path, **args)
        print(f"\n--- {name} {args} ---")
        print(f"  status={st}  {body[:280]}")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        asyncio.run(build_server()())
