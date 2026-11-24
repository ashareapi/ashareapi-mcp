"""ashareapi 容器入口 —— 双模式：mcp（stdio，给 AI Agent）/ gateway（HTTP 转发，给内网）。

用法：
    docker run -i --rm -e ASHARE_KEY=ct-xxx ashareapi/mcp            # mcp 模式（默认）
    docker run -p 8080:8080 -e ASHARE_KEY=ct-xxx ashareapi/mcp gateway

⚠️ 本文件与 mcp_ashare.py 一样，**只做客户端**：所有数据都来自 ASHARE_API（我们的服务端）。
   本镜像内**不含任何数据源**，只有一个 Key 才能取到数据。
"""
import os
import sys

MODE = (sys.argv[1] if len(sys.argv) > 1 else "mcp").strip().lower()
UPSTREAM = os.environ.get("ASHARE_API", "https://api.ashareapi.com").rstrip("/")
KEY = os.environ.get("ASHARE_KEY", "").strip()


def run_mcp() -> None:
    """MCP 模式：直接交给 mcp_ashare.py（stdio 传输）。"""
    os.execvp("python", ["python", "mcp_ashare.py", *sys.argv[2:]])


def run_gateway() -> None:
    """Gateway 模式：把请求原样转发到 ASHARE_API（只换鉴权头）。

    ⛔ 这里**没有任何取数逻辑** —— 只是 HTTP 转发，方便内网统一出口 / 加审计 / 做 Key 映射。
    """
    if not KEY:
        sys.exit("gateway 模式需要环境变量 ASHARE_KEY（你的 API Key）")
    import httpx
    import uvicorn
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse, PlainTextResponse

    app = FastAPI(title="ashareapi · local gateway", docs_url=None, redoc_url=None)

    @app.get("/healthz", include_in_schema=False)
    async def healthz():
        return PlainTextResponse("ok")

    @app.api_route("/{path:path}", methods=["GET", "POST"])
    async def forward(path: str, request: Request):
        url = f"{UPSTREAM}/{path}"
        headers = {"Authorization": f"Bearer {KEY}"}
        async with httpx.AsyncClient(timeout=90) as client:
            try:
                if request.method == "GET":
                    r = await client.get(url, params=dict(request.query_params), headers=headers)
                else:
                    body = await request.body()
                    r = await client.post(url, params=dict(request.query_params),
                                          content=body, headers=headers)
            except httpx.RequestError as e:
                return JSONResponse({"ok": False, "error": f"upstream unreachable: {e}"}, status_code=502)
        try:
            return JSONResponse(r.json(), status_code=r.status_code)
        except ValueError:
            return PlainTextResponse(r.text, status_code=r.status_code)

    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


def main() -> None:
    # ⭐ 调试透传：`docker run -it ashareapi/mcp sh` 也能进容器（否则被 ENTRYPOINT 吃掉）
    if MODE in ("sh", "bash", "python", "python3") or MODE.startswith("-"):
        os.execvp(MODE, sys.argv[1:])
    if MODE == "mcp":
        run_mcp()
    elif MODE in ("gateway", "proxy"):
        run_gateway()
    else:
        sys.exit(f"未知模式：{MODE}（可用：mcp / gateway）\n"
                 f"用法：docker run -e ASHARE_KEY=... ashareapi/mcp [mcp|gateway]")

if __name__ == "__main__":
    main()
