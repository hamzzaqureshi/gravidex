# AgentShield Rule Reference

AgentShield categorizes its 268 detection rules into 15 domain-specific modules. Below is the operational summary of key rule identifiers and their detection logic.

## 1. Secrets (`src/rules/secrets.ts`)

| Rule ID | Severity | Description | Fix |
|---|---|---|---|
| `secrets-anthropic-key` | CRITICAL | Hardcoded Anthropic API key (`sk-ant-...`) | Replace with `$ANTHROPIC_API_KEY` |
| `secrets-openai-key` | CRITICAL | Hardcoded OpenAI API key (`sk-proj-...` or `sk-...`) | Replace with `$OPENAI_API_KEY` |
| `secrets-google-key` | CRITICAL | Hardcoded Google AI key (`AIza...`) | Replace with `$GEMINI_API_KEY` |
| `secrets-github-pat` | CRITICAL | Hardcoded GitHub Personal Access Token (`ghp_...`) | Replace with `$GITHUB_TOKEN` |
| `secrets-aws-key` | CRITICAL | Hardcoded AWS Access Key ID (`AKIA...`) | Replace with `$AWS_ACCESS_KEY_ID` |
| `secrets-private-key` | CRITICAL | Hardcoded RSA/EC private key block | Move to secure key store |
| `secrets-generic-token` | HIGH | High-entropy string matching token assignments | Use environment configuration |

## 2. Permissions (`src/rules/permissions.ts`)

| Rule ID | Severity | Description | Fix |
|---|---|---|---|
| `permissions-wildcard-bash` | CRITICAL | Catch-all `Bash(*)` allowlist entry | Scope to explicit command prefixes |
| `permissions-wildcard-all` | CRITICAL | Top-level `*` tool execution allowlist | Enumerate required tools explicitly |
| `permissions-no-deny-list` | HIGH | Missing `deny` list when shell execution enabled | Define explicit deny guardrails |
| `permissions-dangerous-command` | CRITICAL | Auto-accept rule for destructive command | Remove from allow list |
| `permissions-unrestricted-env` | MEDIUM | Environment variable wildcard expansion | Restrict variable access |

## 3. Hooks (`src/rules/hooks.ts`)

| Rule ID | Severity | Description | Fix |
|---|---|---|---|
| `hooks-no-pretooluse` | HIGH | Tool execution lacks PreToolUse guard | Add PreToolUse validator hook |
| `hooks-command-injection` | CRITICAL | Hook command contains unquoted variables | Quote parameters (`"$@"` or `"$1"`) |
| `hooks-silent-fail` | MEDIUM | Hook appends `\|\| true` suppressing errors | Allow security hooks to fail closed |
| `hooks-external-exfil` | CRITICAL | PostToolUse hook transmits payload via curl/nc | Disallow outbound network in hooks |
| `hooks-chained-commands` | HIGH | Hook command chains multiple shell executions | Split into isolated script files |

## 4. MCP Servers (`src/rules/mcp.ts`, `src/rules/mcp-cve.ts`, `src/rules/mcp-remote.ts`)

| Rule ID | Severity | Description | Fix |
|---|---|---|---|
| `mcp-root-filesystem` | HIGH | Filesystem MCP server mounted at `/` or `~` | Scope mount to project directory `./` |
| `mcp-known-cve` | CRITICAL | Community MCP package has known CVE | Update to patched package version |
| `mcp-unauthenticated-sse` | HIGH | Remote SSE endpoint lacks authorization header | Configure bearer token or API key |
| `mcp-tool-poisoning` | HIGH | Tool description contains instruction override | Sanitize tool description schema |
| `mcp-insecure-http` | MEDIUM | Remote MCP server communicates over HTTP | Enforce HTTPS endpoint |

## 5. Skills & Subagents (`src/rules/skills.ts`, `src/rules/agents.ts`, `src/rules/prompt-defense.ts`)

| Rule ID | Severity | Description | Fix |
|---|---|---|---|
| `skills-unsafe-installer` | CRITICAL | Skill instructions recommend `curl \| bash` | Download, inspect, and verify checksum |
| `agents-unbounded-tools` | HIGH | Subagent manifest permits wildcard tools | Restrict `allowedTools` list |
| `prompt-reflection-attack` | HIGH | Prompt contains `ignore previous instructions` | Sanitize and isolate user inputs |
| `prompt-time-bomb` | HIGH | Instructions contain delayed activation triggers | Remove conditional dormancy |
| `prompt-output-suppression`| HIGH | Instructions command agent to hide warnings | Enforce transparent audit logging |

