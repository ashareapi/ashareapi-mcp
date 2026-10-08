# 更新记录

> **端点 / 工具本身永远是最新的**（服务端演进，**无需重新部署本文件**）—— 只有**工具定义**变化时才需要更新。
> 完整更新日志：<https://ashareapi.com/changelog>

---

## 2026-10-08

- **新增 5 个量化工具**：`ashare_backtest`（量化回测）、`ashare_backtest_batch`（批量回测）、`ashare_strategies`（策略清单）、`ashare_factors`（因子库）、`ashare_playbooks`（方法论库）。工具总数 **26 → 31**。
  - `ashare_backtest`（`/v1/backtest`）：按策略跑历史收益，返回收益 / 最大回撤 / 交易次数 / 净值曲线。`mode=single` 单标的实时（配 `code`）· `mode=portfolio` 组合（预置区间，`weighting=inv_vol` 按波动率倒数配仓，仅**不限量版**）。
  - `ashare_backtest_batch`（`/v1/backtest-batch`）：一次跑**多标的 × 多策略**，返回对比矩阵。上限 标的 ≤20 · 策略 ≤10 · 组合 ≤60（超限直接报错，不静默截断）。
  - `ashare_strategies`（`/v1/strategies`）：量化策略清单（20 条单标的择时 + 9 条组合，含参数范围）。
  - `ashare_factors`（`/v1/factors`）：量化因子库（88 因子 + 50 筛选入口 + 22 预设）。⚠️ `category` / `kind` **只接受中文枚举值**。
  - `ashare_playbooks`（`/v1/playbooks`）：量化方法论库（13 条「怎么判断市场」流程，含判据 / 阶段 / 实测证据）。
  ⚠️ 均为**付费工具**（需 Key）：策略 / 因子 / 方法论清单、单标的回测门槛为 **Standard（¥29.9）及以上**；**组合与批量回测为 Pro（¥69）及以上**，且有独立日额度，余量可查 `ashare_usage`。
  ⚠️ 想知道有哪些策略 / 参数范围，先调 `ashare_strategies`；要用因子实际选股，用 `ashare_screen`。

## 2026-10-07

- **新增工具 `ashare_kline_full`**（对应端点 `/v1/kline-full`）：**全历史 K 线** —— 10 年日线（2016-08-08 起，约 2465 条），并支持**可选复权口径** `fq`（`qfq` 前复权 / `hfq` 后复权 / `nofq` 原始价）。工具总数 **25 → 26**。
  ⚠️ 与 `ashare_kline` 的**三点不同**：① 范围 —— 本工具全历史 10 年（`ashare_kline` 上限 1212 条）；② 复权 —— 本工具可选，`ashare_kline` 固定前复权、无参数；③ 标的 —— 本工具**仅 A 股股票**（ETF / 可转债 / 指数 / 板块 / 港美股会明确报错，请改用 `ashare_kline`）。
  ⚠️ **做回测请用 `fq=hfq` 或 `fq=nofq`** —— 前复权序列会随新的除权除息重算，不可复现。
  ⚠️ 本工具**免费工具不含**，需 Key —— 门槛为 **Standard（¥29.9）及以上**（Trial 不可用），且有**独立日额度**（Standard 200 / Pro 500 / Unlimited 2000 次/天），余量可查 `ashare_usage`。

## 2026-10-06

- **新增工具 `ashare_minute`**（对应端点 `/v1/minute`）：**分时**盘中走势 —— 每分钟一个价格 + 累计成交量，`days` 只有 `1`（当日）与 `5`（近 5 个交易日）两档。工具总数 **24 → 25**。
  ⚠️ 与 `ashare_kline` 的**分钟线不是一回事**：`ashare_kline` 给分钟 **K 线**（OHLC 蜡烛），`ashare_minute` 给**分时**。
- **`ashare_kline` 描述更新**：不再声明「不支持分钟级」；现在说明 `period` 支持 `day` / `week` / `month` / `season` / `year` 与 `m1`~`m120` 六档分钟线，并支持 `start` / `end` 日期范围。分钟线与日期范围属**付费层**。
- **匿名 PoW 提额口径调整**：解一次 PoW 挑战的匿名配额由 60 次/分调整为 **15 次/分**，429 提示同步更新。

## 2026-10-03

- **匿名 429 的提示更准确**：现在会说明「匿名单次最多 250 条、每天最多 10 万条」，并区分两种超限 —— 每分钟次数超（可解一次 PoW 提额）与当天条数超（**解 PoW 无效**，次日恢复或配 Key）。

## 2026-10-01

- 客户端握手时现在会收到明确的服务版本号（`2026.10.1`），可用于确认自己正在运行哪一份工具定义。
- 版本号规则：`serverInfo.version` = 本文件最新条目的日期，格式 `YYYY.M.D`（**不补零** —— 补零会让它变成非语义化版本）。

## 2026-09-30

- 首次公开发布：**24 个工具**（与线上 MCP 端点 `https://api.ashareapi.com/mcp` 一致）
- 兼容 **mcp SDK 1.x 与 2.x**：1.x 用 `@server.list_tools()` 装饰器注册，2.x 用 `Server(on_list_tools=…)` 回调注册
