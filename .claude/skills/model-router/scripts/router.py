#!/usr/bin/env python3
"""Model Router & Subagent Failover Engine.

Inspired by OpenCode's multi-provider architecture and rate-limit resilience.
Routes queries to DeepSeek, Qwen, Groq, and OpenRouter with automatic
cascade failover when 429 (Rate Limit) or quota exhaustion occurs.
Maintains a curated, quality-ranked catalog of cloud AI models (best on top,
least recommended / deprecated at the bottom).
Runs standalone via CLI or as an Antigravity MCP Server over stdin/stdout.
Zero external dependencies (pure Python standard library).
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

VERSION = "1.1.0"

# Default API endpoints for supported cloud providers
DEFAULT_ENDPOINTS = {
    "deepseek": "https://api.deepseek.com/chat/completions",
    "qwen": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
}

# Role-based fallback chains (cloud-first, zero local requirement)
DEFAULT_CHAINS = {
    "reason": [
        {"provider": "deepseek", "model": "deepseek-reasoner"},
        {"provider": "openrouter", "model": "deepseek/deepseek-r1"},
        {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    ],
    "code": [
        {"provider": "qwen", "model": "qwen-2.5-coder-32b-instruct"},
        {"provider": "groq", "model": "qwen-2.5-coder-32b"},
        {"provider": "openrouter", "model": "qwen/qwen-2.5-coder-32b-instruct"},
        {"provider": "deepseek", "model": "deepseek-chat"},
    ],
    "fast": [
        {"provider": "groq", "model": "llama-3.3-70b-versatile"},
        {"provider": "deepseek", "model": "deepseek-chat"},
        {"provider": "openrouter", "model": "meta-llama/llama-3.3-70b-instruct"},
    ],
    "plan": [
        {"provider": "deepseek", "model": "deepseek-chat"},
        {"provider": "openrouter", "model": "anthropic/claude-3.5-sonnet"},
        {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    ],
}

# Curated, quality-ranked directory of cloud models.
# Ranked strictly from best/frontier (S-Tier) down to legacy/poor at bottom.
RANKED_CLOUD_MODELS = [
    # Tier 1: Frontier / State of the Art (Top Tier)
    {
        "id": "deepseek/deepseek-r1",
        "name": "DeepSeek R1",
        "provider": "deepseek / openrouter",
        "tier": "Tier 1 (Frontier S-Tier)",
        "score": 99,
        "specialty": "Deep reasoning, math, formal logic & complex architectural bugs",
        "context": "64k / 128k",
        "speed": "Medium (~25 tok/s)",
    },
    {
        "id": "anthropic/claude-3.7-sonnet",
        "name": "Claude 3.7 Sonnet (Hybrid)",
        "provider": "openrouter",
        "tier": "Tier 1 (Frontier S-Tier)",
        "score": 98,
        "specialty": "Flagship hybrid thinking + instant coding benchmark leader",
        "context": "200k",
        "speed": "Fast (~70 tok/s)",
    },
    {
        "id": "anthropic/claude-3.5-sonnet",
        "name": "Claude 3.5 Sonnet",
        "provider": "openrouter",
        "tier": "Tier 1 (Frontier S-Tier)",
        "score": 97,
        "specialty": "Gold standard for full-stack code generation and refactoring",
        "context": "200k",
        "speed": "Fast (~75 tok/s)",
    },
    {
        "id": "qwen/qwen-2.5-coder-32b-instruct",
        "name": "Qwen 2.5 Coder 32B",
        "provider": "qwen / groq / openrouter",
        "tier": "Tier 1 (Frontier S-Tier)",
        "score": 96,
        "specialty": "Highest open-weight coding benchmark; rivals 70B+ proprietary",
        "context": "128k",
        "speed": "Ultra-Fast (300+ tok/s on Groq)",
    },
    {
        "id": "google/gemini-2.5-pro",
        "name": "Gemini 2.5 Pro",
        "provider": "google / openrouter",
        "tier": "Tier 1 (Frontier S-Tier)",
        "score": 95,
        "specialty": "Massive context codebase comprehension & multi-file reasoning",
        "context": "2,000k (2M)",
        "speed": "Medium (~40 tok/s)",
    },
    {
        "id": "openai/o3-mini",
        "name": "OpenAI o3-mini",
        "provider": "openrouter",
        "tier": "Tier 1 (Frontier S-Tier)",
        "score": 94,
        "specialty": "STEM, algorithms, unit test derivation, concise logic",
        "context": "200k",
        "speed": "Fast (~60 tok/s)",
    },

    # Tier 2: Workhorses / Specialized High-Capability
    {
        "id": "deepseek/deepseek-chat",
        "name": "DeepSeek V3 (671B MoE)",
        "provider": "deepseek / openrouter",
        "tier": "Tier 2 (Workhorse A-Tier)",
        "score": 92,
        "specialty": "Extremely cost-effective general development & architecture",
        "context": "64k / 128k",
        "speed": "Fast (~60 tok/s)",
    },
    {
        "id": "meta-llama/llama-3.3-70b-versatile",
        "name": "Llama 3.3 70B Versatile",
        "provider": "groq / openrouter",
        "tier": "Tier 2 (Workhorse A-Tier)",
        "score": 91,
        "specialty": "Ultra-high speed execution, free tier on Groq, strong reasoning",
        "context": "128k",
        "speed": "Extreme (280+ tok/s on Groq)",
    },
    {
        "id": "openai/gpt-4o",
        "name": "GPT-4o",
        "provider": "openrouter",
        "tier": "Tier 2 (Workhorse A-Tier)",
        "score": 90,
        "specialty": "Multi-modal diagram reading, structured JSON extraction",
        "context": "128k",
        "speed": "Fast (~80 tok/s)",
    },
    {
        "id": "google/gemini-2.5-flash",
        "name": "Gemini 2.5 Flash",
        "provider": "google / openrouter",
        "tier": "Tier 2 (Workhorse A-Tier)",
        "score": 89,
        "specialty": "High speed, multi-million token repository scanning",
        "context": "1,000k (1M)",
        "speed": "Very Fast (~120 tok/s)",
    },

    # Tier 3: Budget & Rapid Scaffolding
    {
        "id": "anthropic/claude-3.5-haiku",
        "name": "Claude 3.5 Haiku",
        "provider": "openrouter",
        "tier": "Tier 3 (Budget / Fast B-Tier)",
        "score": 85,
        "specialty": "Rapid linting, docstrings, JSON transforms, fast test passes",
        "context": "200k",
        "speed": "Very Fast (~100 tok/s)",
    },
    {
        "id": "mistralai/mistral-large-2411",
        "name": "Mistral Large 2",
        "provider": "openrouter",
        "tier": "Tier 3 (Budget / Fast B-Tier)",
        "score": 84,
        "specialty": "Multilingual reasoning, French/German/Spanish codebases",
        "context": "128k",
        "speed": "Medium (~45 tok/s)",
    },
    {
        "id": "openai/gpt-4o-mini",
        "name": "GPT-4o Mini",
        "provider": "openrouter",
        "tier": "Tier 3 (Budget / Fast B-Tier)",
        "score": 82,
        "specialty": "Inexpensive bulk parsing and small script generation",
        "context": "128k",
        "speed": "Very Fast (~110 tok/s)",
    },

    # Tier 4: Least Recommended / Legacy / Deprecated (Ranked at Bottom)
    {
        "id": "openai/gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo (Legacy)",
        "provider": "openrouter",
        "tier": "Tier 4 (Least Recommended / Deprecated)",
        "score": 45,
        "specialty": "Superseded by GPT-4o-mini; prone to hallucinating modern APIs",
        "context": "16k",
        "speed": "Fast",
    },
    {
        "id": "meta-llama/llama-2-70b-chat",
        "name": "Llama 2 70B (Obsolete)",
        "provider": "openrouter",
        "tier": "Tier 4 (Least Recommended / Deprecated)",
        "score": 38,
        "specialty": "Outdated instruction tuning; easily confused on multi-file diffs",
        "context": "4k",
        "speed": "Slow",
    },
    {
        "id": "mistralai/mistral-7b-instruct-v0.1",
        "name": "Mistral 7B v0.1 (Obsolete)",
        "provider": "openrouter",
        "tier": "Tier 4 (Least Recommended / Deprecated)",
        "score": 30,
        "specialty": "First-generation release; superseded by modern 7B/8B architectures",
        "context": "8k",
        "speed": "Fast",
    },
]


class ModelRouter:
    """Manages multi-provider connections, task roles, and failovers."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.config/model-router/config.json")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration from file and environment variables."""
        cfg = {"providers": {}, "chains": DEFAULT_CHAINS.copy()}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    if "providers" in file_data:
                        cfg["providers"].update(file_data["providers"])
                    if "chains" in file_data:
                        cfg["chains"].update(file_data["chains"])
            except Exception as e:
                sys.stderr.write(f"Warning: Failed to parse config file: {e}\n")

        # Overlay environment variables
        env_map = {
            "deepseek": "DEEPSEEK_API_KEY",
            "qwen": "DASHSCOPE_API_KEY",
            "groq": "GROQ_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
        }
        for provider, env_var in env_map.items():
            key = os.environ.get(env_var)
            if key:
                if provider not in cfg["providers"]:
                    cfg["providers"][provider] = {}
                cfg["providers"][provider]["api_key"] = key

        return cfg

    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Returns readiness and configuration status for each cloud provider."""
        status = {}
        for p in ["deepseek", "groq", "openrouter", "qwen"]:
            p_cfg = self.config.get("providers", {}).get(p, {})
            has_key = bool(p_cfg.get("api_key"))
            endpoint = p_cfg.get("base_url") or DEFAULT_ENDPOINTS.get(p)

            status[p] = {
                "configured": has_key,
                "endpoint": endpoint,
                "requires_key": True,
                "ready": has_key,
                "note": "API Key detected" if has_key else "Missing API Key",
            }
        return status

    def get_ranked_models(
        self,
        filter_provider: Optional[str] = None,
        filter_tier: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Returns models ordered from highest quality down to least recommended."""
        models = RANKED_CLOUD_MODELS.copy()
        if filter_provider:
            p_lower = filter_provider.lower()
            models = [m for m in models if p_lower in m["provider"].lower() or p_lower in m["id"].lower()]
        if filter_tier:
            t_lower = filter_tier.lower()
            models = [m for m in models if t_lower in m["tier"].lower()]
        return sorted(models, key=lambda x: x.get("score", 0), reverse=True)

    def fetch_live_openrouter_models(self, limit: int = 40) -> List[Dict[str, Any]]:
        """Fetches live directory from OpenRouter API and sorts by ranking/context."""
        url = "https://openrouter.ai/api/v1/models"
        req = urllib.request.Request(url, headers={"User-Agent": f"ModelRouter/{VERSION}"})
        try:
            with urllib.request.urlopen(req, timeout=6.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_models = data.get("data", [])

                # Map into standard schema
                parsed = []
                for m in raw_models:
                    m_id = m.get("id", "")
                    name = m.get("name", m_id)
                    ctx = f"{m.get('context_length', 0) // 1024}k" if m.get("context_length") else "N/A"
                    pricing = m.get("pricing", {})
                    prompt_price = float(pricing.get("prompt", 0)) * 1_000_000
                    completion_price = float(pricing.get("completion", 0)) * 1_000_000

                    # Compute quality heuristic
                    score = 70
                    tier = "Tier 3 (Budget / Fast)"
                    if any(x in m_id.lower() for x in ["r1", "claude-3-7", "claude-3.5", "o3-mini", "coder-32b", "gemini-2.5-pro"]):
                        score = 95
                        tier = "Tier 1 (Frontier S-Tier)"
                    elif any(x in m_id.lower() for x in ["v3", "70b", "gpt-4o", "large"]):
                        score = 88
                        tier = "Tier 2 (Workhorse A-Tier)"
                    elif any(x in m_id.lower() for x in ["3.5-turbo", "llama-2", "v0.1", "legacy"]):
                        score = 30
                        tier = "Tier 4 (Least Recommended / Deprecated)"

                    parsed.append({
                        "id": m_id,
                        "name": name,
                        "provider": "openrouter",
                        "tier": tier,
                        "score": score,
                        "context": ctx,
                        "pricing_per_1m": f"${prompt_price:.2f} in / ${completion_price:.2f} out",
                        "specialty": m.get("description", "Cloud inference endpoint")[:80],
                    })

                # Sort: S-Tier and high scores first, deprecated/bad models at bottom
                parsed.sort(key=lambda x: x["score"], reverse=True)
                return parsed[:limit]
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to fetch live OpenRouter models: {e}\n")
            return self.get_ranked_models()

    def query(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 4096,
        timeout: float = 60.0,
    ) -> Dict[str, Any]:
        """Queries a single OpenAI-compatible provider."""
        p_cfg = self.config.get("providers", {}).get(provider, {})
        endpoint = p_cfg.get("base_url") or DEFAULT_ENDPOINTS.get(provider)
        if not endpoint:
            raise ValueError(f"Unknown provider: {provider}")

        api_key = p_cfg.get("api_key")
        if not api_key:
            raise PermissionError(f"Missing API key for provider '{provider}'")

        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"ModelRouter/{VERSION}",
            "Authorization": f"Bearer {api_key}",
        }
        if provider == "openrouter":
            headers["HTTP-Referer"] = "https://github.com/hamzzaqureshi/gravidex"
            headers["X-Title"] = "GraviDex Model Router"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})
                content = message.get("content", "")
                reasoning = message.get("reasoning_content") or message.get("reasoning")
                usage = data.get("usage", {})

                return {
                    "success": True,
                    "provider": provider,
                    "model": model,
                    "content": content,
                    "reasoning": reasoning,
                    "usage": usage,
                }
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            return {
                "success": False,
                "provider": provider,
                "model": model,
                "http_status": e.code,
                "error": f"HTTP {e.code}: {e.reason}",
                "body": err_body,
                "is_rate_limit": e.code in (429, 503, 402),
            }
        except Exception as e:
            return {
                "success": False,
                "provider": provider,
                "model": model,
                "http_status": 0,
                "error": str(e),
                "is_rate_limit": False,
            }

    def cascade_query(
        self,
        role: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """Cascades through fallback models when 429 or quota limit occurs."""
        chain = self.config.get("chains", {}).get(role)
        if not chain:
            chain = DEFAULT_CHAINS.get(role, DEFAULT_CHAINS["code"])

        attempts = []
        for step in chain:
            provider = step["provider"]
            model = step["model"]

            # Quick readiness check
            p_cfg = self.config.get("providers", {}).get(provider, {})
            if not p_cfg.get("api_key"):
                attempts.append({
                    "provider": provider,
                    "model": model,
                    "status": "skipped",
                    "reason": "Missing API Key",
                })
                continue

            res = self.query(provider, model, messages, temperature=temperature)
            if res["success"]:
                return {
                    "success": True,
                    "role": role,
                    "provider": provider,
                    "model": model,
                    "content": res["content"],
                    "reasoning": res.get("reasoning"),
                    "usage": res.get("usage", {}),
                    "attempts": attempts,
                }

            # Record failure
            attempts.append({
                "provider": provider,
                "model": model,
                "status": "failed",
                "http_status": res.get("http_status"),
                "error": res.get("error"),
                "is_rate_limit": res.get("is_rate_limit", False),
            })

            # If it's a rate limit or server busy, log and cascade immediately
            if res.get("is_rate_limit"):
                sys.stderr.write(
                    f"[Cascade Failover] {provider}:{model} hit rate limit ({res.get('http_status')}). "
                    f"Cascading to next provider in '{role}' chain...\n"
                )

        return {
            "success": False,
            "role": role,
            "error": "All providers in cascade chain failed or were unconfigured.",
            "attempts": attempts,
        }


# ==============================================================================
# Model Context Protocol (MCP) Server Implementation
# ==============================================================================

def run_mcp_server(router: ModelRouter):
    """Executes a JSON-RPC 2.0 MCP server over stdin and stdout."""
    tools = [
        {
            "name": "consult_model",
            "description": "Send a prompt to an external cloud model (DeepSeek R1/V3, Qwen 2.5 Coder, Groq, OpenRouter).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "provider": {
                        "type": "string",
                        "enum": ["deepseek", "qwen", "groq", "openrouter"],
                        "description": "The cloud AI provider to route to.",
                    },
                    "model": {
                        "type": "string",
                        "description": "Model ID (e.g. 'deepseek-reasoner', 'qwen-2.5-coder-32b-instruct', 'llama-3.3-70b-versatile').",
                    },
                    "prompt": {"type": "string", "description": "The prompt or task description."},
                    "system_prompt": {"type": "string", "description": "Optional system prompt."},
                    "temperature": {"type": "number", "default": 0.2},
                },
                "required": ["provider", "model", "prompt"],
            },
        },
        {
            "name": "cascade_query",
            "description": "Resilient multi-model query with automatic rate-limit (429) failover cascade across cloud providers.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "enum": ["reason", "code", "fast", "plan"],
                        "description": "The task specialization role.",
                    },
                    "prompt": {"type": "string", "description": "The prompt or coding task."},
                    "system_prompt": {"type": "string", "description": "Optional system prompt."},
                    "temperature": {"type": "number", "default": 0.2},
                },
                "required": ["role", "prompt"],
            },
        },
        {
            "name": "list_ranked_models",
            "description": "Get the complete directory of cloud AI models ranked from best (frontier S-Tier) down to least recommended.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "provider": {"type": "string", "description": "Optional filter by provider name."},
                    "live": {"type": "boolean", "description": "Whether to fetch real-time directory from OpenRouter."},
                },
            },
        },
        {
            "name": "list_providers",
            "description": "Check the status and readiness of configured external cloud AI providers.",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
    ]

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "model-router", "version": VERSION},
                },
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            pass

        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": tools},
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "list_providers":
                status = router.get_provider_status()
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(status, indent=2)}]
                    },
                }
            elif tool_name == "list_ranked_models":
                provider_filter = arguments.get("provider")
                live = arguments.get("live", False)
                if live:
                    models = router.fetch_live_openrouter_models()
                else:
                    models = router.get_ranked_models(filter_provider=provider_filter)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(models, indent=2)}]
                    },
                }
            elif tool_name == "consult_model":
                provider = arguments.get("provider")
                model = arguments.get("model")
                prompt = arguments.get("prompt")
                sys_prompt = arguments.get("system_prompt")
                temp = arguments.get("temperature", 0.2)

                msgs = []
                if sys_prompt:
                    msgs.append({"role": "system", "content": sys_prompt})
                msgs.append({"role": "user", "content": prompt})

                res = router.query(provider, model, msgs, temperature=temp)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}],
                        "isError": not res.get("success", False),
                    },
                }
            elif tool_name == "cascade_query":
                role = arguments.get("role", "code")
                prompt = arguments.get("prompt")
                sys_prompt = arguments.get("system_prompt")
                temp = arguments.get("temperature", 0.2)

                msgs = []
                if sys_prompt:
                    msgs.append({"role": "system", "content": sys_prompt})
                msgs.append({"role": "user", "content": prompt})

                res = router.cascade_query(role, msgs, temperature=temp)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}],
                        "isError": not res.get("success", False),
                    },
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"},
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def print_models_table(models: List[Dict[str, Any]]):
    """Prints models ranked cleanly with best on top, legacy at bottom."""
    print("\nRANKED CLOUD MODELS DIRECTORY (Best on Top, Weakest at Bottom):")
    print("=" * 115)
    print(f"{'Tier / Model ID':<36} | {'Score':<5} | {'Context':<8} | {'Speed':<18} | {'Specialization'}")
    print("-" * 115)

    current_tier = ""
    for m in models:
        tier = m.get("tier", "")
        if tier != current_tier:
            current_tier = tier
            print(f"\n[{current_tier.upper()}]")

        model_name = m.get("name") or m["id"]
        score_str = f"{m.get('score', 0):>3}/100"
        ctx = m.get("context", "N/A")
        speed = m.get("speed", "Medium")[:18]
        desc = m.get("specialty", "")[:45]
        print(f"  {model_name:<34} | {score_str} | {ctx:<8} | {speed:<18} | {desc}")

    print("=" * 115 + "\n")


def main():
    router = ModelRouter()

    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("Model Router & Subagent Failover Engine v" + VERSION)
        print("\nCommands:")
        print("  models [--live] [--filter <str>]  Display full ranked cloud model directory")
        print("  status                           List provider readiness and configured keys")
        print("  query [options]                  Query a specific model directly")
        print("  cascade [options]                Query with automatic 429 rate-limit failover")
        print("  --mcp                            Run as an Antigravity MCP Server over stdin/stdout")
        print("\nExamples:")
        print("  python3 router.py models")
        print("  python3 router.py models --live")
        print("  python3 router.py status")
        print("  python3 router.py cascade --role reason --prompt 'Solve this race condition'")
        print("  python3 router.py query --provider deepseek --model deepseek-reasoner --prompt 'Explain...'")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd in ("--mcp", "mcp"):
        run_mcp_server(router)
        return

    if cmd == "models":
        live = "--live" in sys.argv
        filter_str = None
        for i, a in enumerate(sys.argv):
            if a in ("--filter", "-f") and i + 1 < len(sys.argv):
                filter_str = sys.argv[i + 1]

        if live:
            print("Fetching live model directory from OpenRouter API...")
            models = router.fetch_live_openrouter_models(limit=40)
        else:
            models = router.get_ranked_models(filter_provider=filter_str)

        if "--json" in sys.argv:
            print(json.dumps(models, indent=2))
        else:
            print_models_table(models)
        return

    if cmd == "status":
        status = router.get_provider_status()
        print("\nCLOUD PROVIDER READINESS REPORT:")
        print("----------------------------------------------------------------------")
        print(f"{'Provider':<14} | {'Ready':<7} | {'Endpoint':<36} | Note")
        print("----------------------------------------------------------------------")
        for p, d in status.items():
            ready_str = "YES" if d["ready"] else "NO"
            print(f"{p:<14} | {ready_str:<7} | {d['endpoint']:<36} | {d['note']}")
        print("----------------------------------------------------------------------\n")
        return

    if cmd == "query":
        provider = "deepseek"
        model = "deepseek-chat"
        prompt = ""
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--provider" and i + 1 < len(sys.argv):
                provider = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--model" and i + 1 < len(sys.argv):
                model = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--prompt" and i + 1 < len(sys.argv):
                prompt = sys.argv[i + 1]
                i += 2
            else:
                prompt = sys.argv[i]
                i += 1

        if not prompt:
            print("Error: --prompt is required.")
            sys.exit(1)

        res = router.query(provider, model, [{"role": "user", "content": prompt}])
        if res["success"]:
            if res.get("reasoning"):
                print(f"[REASONING]:\n{res['reasoning']}\n")
            print(res["content"])
        else:
            print(f"Error ({res.get('http_status')}): {res.get('error')}")
            sys.exit(1)

    elif cmd == "cascade":
        role = "code"
        prompt = ""
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--role" and i + 1 < len(sys.argv):
                role = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--prompt" and i + 1 < len(sys.argv):
                prompt = sys.argv[i + 1]
                i += 2
            else:
                prompt = sys.argv[i]
                i += 1

        if not prompt:
            print("Error: --prompt is required.")
            sys.exit(1)

        res = router.cascade_query(role, [{"role": "user", "content": prompt}])
        if res["success"]:
            print(f"Answered by [{res['provider']}:{res['model']}]:\n")
            if res.get("reasoning"):
                print(f"[REASONING]:\n{res['reasoning']}\n")
            print(res["content"])
        else:
            print(f"Cascade Failure: {res.get('error')}")
            for a in res.get("attempts", []):
                print(f"  - {a['provider']}:{a['model']} -> {a.get('status')} ({a.get('error') or a.get('reason')})")
            sys.exit(1)


if __name__ == "__main__":
    main()
