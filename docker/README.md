# ashareapi 容器 —— 镜像 `ashareapi/mcp`

A 股数据 API 的 **MCP 服务器 + 本地网关**。镜像里**不打包任何数据**：Key 只通过环境变量传入，数据从 ashareapi API 取。

## 前提

一个 ashareapi API Key（`ct-` 开头，见 <https://ashareapi.com/pricing>）才能调付费工具/端点；免费工具无需 Key。

## 模式 1：MCP（默认，推荐）

给 AI Agent 客户端（Claude Code / Codex / Cursor）用，stdio 协议。

```bash
docker run -i --rm -e ASHARE_KEY=ct-xxx ashareapi/mcp
docker run -i --rm -e ASHARE_KEY=ct-xxx ashareapi/mcp mcp
```

MCP 配置示例（Claude Code / Cursor 等）：

```json
{
  "mcpServers": {
    "ashareapi": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "ASHARE_KEY=ct-xxx", "ashareapi/mcp"]
    }
  }
}
```

Codex（`~/.codex/config.toml`）用 `env_vars` 把 Key 从环境变量传入，不写进配置文件：

```toml
[mcp_servers.ashareapi]
command = "docker"
args = ["run", "-i", "--rm", "-e", "ASHARE_KEY", "ashareapi/mcp"]
env_vars = ["ASHARE_KEY"]
```

## 模式 2：本地网关

给脚本 / 内网批量用：起一个 HTTP 服务，把请求转发到 ashareapi API（方便统一出口、加审计、做 Key 映射）。

```bash
docker run -p 8080:8080 -e ASHARE_KEY=ct-xxx ashareapi/mcp gateway
curl "http://localhost:8080/v1/quote?code=600519"
```

## 环境变量

| 变量 | 说明 | 默认 |
|---|---|---|
| `ASHARE_KEY` | API Key（免费工具可不填） | 无 |
| `ASHARE_API` | API 地址 | `https://api.ashareapi.com` |
| `PORT` | gateway 端口 | `8080` |

## 构建

```bash
# 在 ashareapi-mcp 仓库根目录执行
docker build -f docker/Dockerfile.dockerhub -t ashareapi/mcp .
```

## 安全

镜像内是 `mcp_ashare.py`（MCP 客户端）+ `entrypoint.py`：Key 只通过环境变量传入，不写进镜像、不写进日志。镜像内**没有任何数据源**，全部数据来自 `ASHARE_API`。
