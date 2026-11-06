# Model Router & Subagent Failover Engine

> Resilient multi-provider AI model routing and automatic 429 rate-limit cascade failover for Google Antigravity.

Inspired by OpenCode's universal provider architecture (`anomalyco/opencode`), this engine bridges Google Antigravity to **DeepSeek (R1/V3)**, **Qwen (2.5 Coder)**, **Groq**, **OpenRouter**, and local **Ollama** models.

When working on demanding engineering workflows, hitting rate limits or quota boundaries halts development. This engine provides an automated fallback cascade: if your primary model returns HTTP 429 (Too Many Requests), the prompt is immediately re-dispatched to the next provider in the chain without interrupting task momentum.

---

## Features

- **Multi-Provider Support**: DeepSeek, Qwen (DashScope), Groq, OpenRouter, and local Ollama.
- **Zero-Downtime Rate-Limit Failover**: Automatically cascades when HTTP 429, 503, or quota errors occur.
- **Task Specialization Roles**: Pre-configured chains for `reason` (logic/math), `code` (scaffolding/editing), `fast` (quick transforms), and `plan` (architecture).
- **Dual Interface**:
  - **Antigravity MCP Server**: Mount directly into `~/.gemini/config/mcp_config.json` for in-IDE tool calling.
  - **Standalone CLI**: Query directly from terminal or shell scripts.
- **Zero External Dependencies**: Pure Python standard library (`urllib.request`, `json`, `os`, `sys`).

---

## Quickstart

```bash
# Check provider status
python3 scripts/router.py status

# Query with automatic failover
python3 scripts/router.py cascade --role reason --prompt "Analyze deadlocks in this mutex pattern"
```

## MCP Configuration

Add to `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "model-router": {
      "command": "python3",
      "args": ["/home/hamza/Documents/skills/model-router/scripts/router.py", "--mcp"]
    }
  }
}
```

## Testing

```bash
python3 -B -m unittest discover -s tests
```

