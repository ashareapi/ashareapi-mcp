"""工具表与 MCP 接线校验（不联网）。

跑法：pytest -q
"""
import asyncio
import importlib.util
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("mcp_ashare", ROOT / "mcp_ashare.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load()

FREE_TOOLS = {
    "ashare_quote", "ashare_kline", "ashare_hot",
    "ashare_market_overview", "ashare_changedist",
}


def test_tool_count():
    assert len(M.TOOLS) == 25


def test_default_api_is_official_domain():
    # 默认必须指向官方域，不能是本地地址
    assert M.API == "https://api.ashareapi.com"


def test_every_tool_is_well_formed():
    for name, (path, desc, params) in M.TOOLS.items():
        assert name.startswith("ashare_"), name
        assert path.startswith("/v1/"), name
        assert desc.strip(), name
        assert isinstance(params, list), name
        for pname, schema, required in params:
            assert schema.get("type") in {"string", "integer", "number", "boolean"}, name
            assert isinstance(required, bool), name


def test_free_tools_are_marked():
    marked = {n for n, (_, d, _) in M.TOOLS.items() if "免费工具" in d}
    assert marked == FREE_TOOLS


def test_mcp_stdio_end_to_end():
    """以真实 MCP 协议（stdio）起一次服务端，取工具清单。

    这条同时覆盖两件事：① 服务端能在当前安装的 mcp SDK 上跑起来；
    ② 注册出来的工具数与 TOOLS 表一致。不发起任何网络请求。
    """
    pytest.importorskip("mcp")
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=sys.executable, args=[str(ROOT / "mcp_ashare.py")])

    async def _run():
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                listed = await session.list_tools()
                return listed.tools

    tools = asyncio.run(_run())
    assert len(tools) == 25
    assert {t.name for t in tools} == set(M.TOOLS)
    for t in tools:
        assert t.description, t.name
        # mcp 1.x 字段名 inputSchema；2.x 改为 input_schema
        schema = getattr(t, "inputSchema", None) or getattr(t, "input_schema", None)
        assert schema and schema.get("type") == "object", t.name


def test_anonymous_401_429_get_friendly_hint(monkeypatch):
    """匿名时 401/429 换成"配 Key"的提示，且**不再提 PoW**（stdio 客户端解不了）。"""
    monkeypatch.setattr(M, "KEY", "")
    raw = ('{"error":"匿名限流 2 次/分","pow":"x.y",'
           '"how_to":"解 PoW 后带请求头 X-PoW: <challenge>.<nonce>，匿名配额提升到 15 次/分"}')
    t401 = M._friendly(401, '{"error":"需要 API Key（此端点属付费层）"}')
    t429 = M._friendly(429, raw)
    for t in (t401, t429):
        assert "ASHARE_KEY" in t
        assert "PoW" not in t and "X-PoW" not in t
        assert M._PRICING_URL in t
    assert "付费层" in t401
    assert "匿名额度已用完" in t429


def test_key_configured_passes_through(monkeypatch):
    """配了 Key 就原样返回（付费用户不经过匿名限流）。"""
    monkeypatch.setattr(M, "KEY", "ct-xxx")
    assert M._friendly(429, '{"ok":true}') == '{"ok":true}'
    assert M._friendly(200, '{"ok":true}') == '{"ok":true}'


def test_anonymous_200_passes_through(monkeypatch):
    """匿名但正常返回 ⇒ 不动内容。"""
    monkeypatch.setattr(M, "KEY", "")
    assert M._friendly(200, '{"ok":true,"data":[]}') == '{"ok":true,"data":[]}'

