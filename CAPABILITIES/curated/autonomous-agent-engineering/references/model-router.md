---
name: model-router
description: >-
  Multi-model routing, quality-ranked cloud model directory, and resilient 429 rate-limit failover engine.
  Connects Antigravity to DeepSeek (R1/V3), Claude (3.7/3.5), Qwen (2.5 Coder 32B), Groq (Llama 3.3),
  and OpenRouter. Runs standalone via CLI or mounts directly as an Antigravity MCP server.
argument-hint: "[models | status | query | cascade | mcp] [options]"
---

# Model Router: Resilient Multi-Provider Subagent Engine

The Model Router equips Google Antigravity with multi-model dispatch, a quality-ranked cloud model directory, and zero-downtime rate-limit resilience, inspired by OpenCode's universal provider architecture and Austin Kleon's creative synthesis principles.

When working on demanding projects, hitting rate limits (`HTTP 429` / quota exhaustion) on your primary model halts progress. This engine routes tasks to specialized cloud models and automatically cascades down a fallback chain if an upstream provider is throttled or offline.

---

## Ranked Cloud Models Directory (Best on Top, Weakest at Bottom)

The router maintains an evaluated catalog across frontier cloud providers:

| Tier | Model ID | Score | Context | Strengths |
| :--- | :--- | :---: | :--- | :--- |
| **Tier 1 (Frontier S-Tier)** | `deepseek/deepseek-r1` | 99/100 | 64k/128k | Deep mathematical reasoning, formal logic & complex architectural bugs |
| **Tier 1 (Frontier S-Tier)** | `anthropic/claude-3.7-sonnet` | 98/100 | 200k | Hybrid thinking + instant coding benchmark leader |
| **Tier 1 (Frontier S-Tier)** | `anthropic/claude-3.5-sonnet` | 97/100 | 200k | Full-stack software engineering gold standard |
| **Tier 1 (Frontier S-Tier)** | `qwen/qwen-2.5-coder-32b-instruct`| 96/100 | 128k | Highest open-weight coding benchmark; ultra-fast on Groq |
| **Tier 1 (Frontier S-Tier)** | `google/gemini-2.5-pro` | 95/100 | 2M | Massive multi-file repository context comprehension |
| **Tier 1 (Frontier S-Tier)** | `openai/o3-mini` | 94/100 | 200k | STEM, algorithms, unit test derivation, concise logic |
| **Tier 2 (Workhorse A-Tier)**| `deepseek/deepseek-chat` (V3) | 92/100 | 64k/128k | High-efficiency general development and architecture |
| **Tier 2 (Workhorse A-Tier)**| `meta-llama/llama-3.3-70b-versatile`| 91/100 | 128k | Free tier on Groq, 280+ tokens/sec |
| **Tier 2 (Workhorse A-Tier)**| `openai/gpt-4o` | 90/100 | 128k | Multi-modal diagram reading, structured JSON extraction |
| **Tier 3 (Budget B-Tier)**   | `anthropic/claude-3.5-haiku` | 85/100 | 200k | Rapid linting, docstrings, JSON transforms |
| **Tier 4 (Deprecated)**      | `openai/gpt-3.5-turbo` | 45/100 | 16k | Superseded; prone to hallucinating modern APIs |
| **Tier 4 (Deprecated)**      | `meta-llama/llama-2-70b-chat`| 38/100 | 4k | Obsolete instruction tuning; easily confused on multi-file diffs |

---

## Configuration

The router reads from standard environment variables or a local configuration file at `~/.config/model-router/config.json`.

```bash
export OPENROUTER_API_KEY="sk-or-..."  # Single key unlocks 200+ ranked models
export DEEPSEEK_API_KEY="sk-..."       # DeepSeek R1 & V3
export GROQ_API_KEY="gsk_..."          # Free tier available at console.groq.com
export DASHSCOPE_API_KEY="sk-..."      # Alibaba Qwen
```

---

## Mounting in Antigravity as an MCP Server

Add to your Antigravity MCP configuration (`~/.gemini/config/mcp_config.json`):

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

Antigravity tools exposed:
1. `list_ranked_models`: Inspects the directory of cloud models ranked from S-Tier to Deprecated.
2. `cascade_query`: Executes a prompt with automatic rate-limit failover across cloud providers.
3. `consult_model`: Explicitly queries a specific model (e.g. DeepSeek R1).
4. `list_providers`: Reports which providers are currently configured and online.

---

## CLI Usage

```bash
# View ranked model directory
python3 scripts/router.py models

# Fetch live real-time directory from OpenRouter API
python3 scripts/router.py models --live

# Check provider readiness
python3 scripts/router.py status

# Run with automatic rate-limit failover
python3 scripts/router.py cascade --role reason --prompt "Solve this race condition in Node PTY"
python3 scripts/router.py cascade --role code --prompt "Write a TypeScript parser for JSON lines"
```
