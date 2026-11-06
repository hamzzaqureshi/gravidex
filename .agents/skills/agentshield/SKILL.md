---
name: agentshield
description: >
  Security auditor for AI agent configurations. Scans Claude Code, OpenCode, Codex, and
  Antigravity setups for hardcoded secrets, overly permissive allow rules (Bash(*)), hook
  injection, MCP server vulnerabilities, and prompt injection vectors. Use when auditing agent
  harnesses, inspecting .agents/ or .claude/ configs, vetting third-party skills, or securing AI
  developer environments before commits or deployments.
license: MIT
metadata:
  author: Affaan Mustafa
  upstream_repository: affaan-m/agentshield
  upstream_commit: b0891303bdcd6037376a94263d45cfd2ff3dfb98
  upstream_version: "1.6.0"
  upstream_url: https://github.com/affaan-m/agentshield
---

# AgentShield

AgentShield is a specialized security auditor for AI agent configurations, created by Affaan Mustafa ([affaan-m/agentshield](https://github.com/affaan-m/agentshield)), licensed under the MIT License. It scans configuration directories (`.claude/`, `.agents/`, `.codex/`, `.opencode/`), skill bundles, MCP server registries, hooks manifests, and prompt templates to detect vulnerabilities, dangerous privilege escalation, and supply-chain threats before agents execute.

## When to Use

Activate this skill when:
- Auditing local agent configurations (`.claude/`, `.agents/`, `.codex/`, `.opencode/`).
- Reviewing `settings.json`, `settings.local.json`, `CLAUDE.md`, or `AGENTS.md` before committing.
- Evaluating a newly downloaded third-party skill, plugin, or subagent configuration.
- Verifying MCP server configurations for CVEs, untrusted endpoints, or tool poisoning.
- Hardening CI/CD pipelines against prompt injection, hook manipulation, or credential exfiltration.
- The user requests a security audit of agent permissions, skills, or environment harnesses.

---

## Quick Start: Automated Scanner CLI

When Node.js is available on the target environment, execute AgentShield directly via `npx` or global installation:

```bash
# Scan default agent configurations in current directory / home
npx ecc-agentshield scan

# Scan a specific directory
npx ecc-agentshield scan --path ./my-project

# Output machine-readable JSON or Markdown
npx ecc-agentshield scan --format json
npx ecc-agentshield scan --format markdown > security-report.md

# Enforce CI/CD pipeline pass/fail thresholds
npx ecc-agentshield scan --fail-on high

# Automatically fix supported remediation patterns
npx ecc-agentshield scan --fix
```

### Supported CLI Flags

| Flag | Purpose | Default |
|---|---|---|
| `--path <dir>` | Directory to scan for agent configuration files | Current directory / auto-discover |
| `--format <type>` | Output format: `terminal`, `json`, `markdown`, `html` | `terminal` |
| `--fail-on <level>` | Exit with code 1 if findings meet severity: `critical`, `high`, `medium`, `low` | None |
| `--fix` | Apply safe in-place fixes for auto-fixable findings | False |
| `--verbose` | Output detailed debug traces and file inventory | False |

---

## The Six Core Security Pillars

AgentShield audits agent harnesses across six critical attack surfaces:

### 1. Secrets and Credentials
- **Patterns caught:** Plaintext Anthropic/OpenAI/Google API keys, GitHub personal access tokens (`ghp_`), AWS credentials (`AKIA...`), database connection strings, bearer tokens, and private SSH/TLS keys.
- **Surface:** `settings.json`, `settings.local.json`, `CLAUDE.md`, `AGENTS.md`, markdown prompt files, environment files, and hook scripts.
- **Severity:** CRITICAL.
- **Rule:** Never embed API keys or passwords directly in agent configuration files or prompt markdown. Reference system environment variables instead.

### 2. Permissions and Wildcards
- **Patterns caught:** Overly permissive allowlists (`Bash(*)`, `*`, `exec(*)`, wildcard read/write), unrestricted shell execution, missing deny lists, and auto-accept configurations for destructive binaries (`rm -rf`, `sudo`, `dd`, `mkfs`).
- **Surface:** `settings.json` permissions block, `.claude/permissions/`, OpenCode permissions manifests.
- **Severity:** CRITICAL to HIGH.
- **Rule:** Principle of least privilege. Replace catch-all commands with tightly scoped commands: `Bash(git *)`, `Bash(npm test)`, `Bash(pytest)`.

### 3. Hooks Architecture and Tampering
- **Patterns caught:** Missing PreToolUse hooks (unbounded tool calls), command-chaining injection (`command1 && malicious_payload`), unquoted parameters in hook scripts, silent failure flags (`|| true` on security checks), and exfiltration endpoints in PostToolUse triggers.
- **Surface:** `settings.json` hooks arrays, `hooks/hooks.json`, hook shell and Node/Python target scripts.
- **Severity:** HIGH to CRITICAL.
- **Rule:** Ensure all tool executions pass through validated PreToolUse checks. Isolate hook execution from external shell command interpolation.

### 4. MCP (Model Context Protocol) Servers
- **Patterns caught:** Known CVEs in community MCP servers, untrusted remote HTTP/SSE endpoints, lack of authentication headers, tool poisoning (malicious tool descriptions steering model actions), and root-scoped filesystem server roots (`/` or `~` instead of project-relative paths).
- **Surface:** `mcp-configs/`, `.claude/mcp-servers.json`, `claude_desktop_config.json`.
- **Severity:** HIGH to CRITICAL.
- **Rule:** Restrict filesystem MCP servers to repo-relative paths (`./`). Pin MCP package versions. Reject unauthenticated remote SSE endpoints.

### 5. Agent and Skill Prompt Injection Defense
- **Patterns caught:** DAN (Do-Anything-Now) jailbreaks, prompt reflection (`ignore previous instructions`, `you are now`), time-delayed trigger bombs, bulk credential harvesting instructions, output manipulation (`always report ok`, `remove warnings`), and unconstrained `allowedTools` in subagent manifests.
- **Surface:** `SKILL.md`, `.agents/skills/`, `.claude/subagents/`, `commands/*.md`.
- **Severity:** HIGH.
- **Rule:** Isolate user input from system instructions. Ensure prompt templates reject instruction overrides and maintain audit logs.

### 6. Harness Policies and Container Isolation
- **Patterns caught:** Disabled container sandboxes, bypassed network boundaries, dangerous mount volumes, unvetted package manager execution (`pip install --pre`, `npm install --force`), and multi-agent coordination without approval barriers.
- **Surface:** `.agents/rules/`, `.codex/AGENTS.md`, IDE workspace settings.
- **Severity:** MEDIUM to HIGH.
- **Rule:** Require human authorization before escalating out of sandbox or making unauthenticated network requests.

---

## 15 Rule Categories & Taxonomy

AgentShield organizes 268 built-in inspection rules into 15 specialized modules:

1. `secrets`: Detects hardcoded keys, passwords, and tokens across all configuration files.
2. `permissions`: Audits auto-allow lists, wildcard execution, and privilege escalation patterns.
3. `permission-entries`: Validates individual command permission entries for path traversal and evasion.
4. `hooks`: Checks hook triggers, PreToolUse completeness, and hook shell-escape vulnerabilities.
5. `mcp`: Inspects MCP server declarations, filesystem scopes, and argument sanitization.
6. `mcp-cve`: Matches installed MCP packages against known CVE intelligence databases.
7. `mcp-tool-poisoning`: Analyzes tool descriptions for latent injection and deceptive instructions.
8. `mcp-remote`: Enforces authentication, TLS verification, and domain pinning on remote MCP servers.
9. `package-manager`: Detects untrusted registries, unsafe install scripts, and typosquatting risks.
10. `skills`: Audits skill metadata, observation hooks, rollback manifests, and executable scripts.
11. `agents`: Reviews subagent schemas, delegated permissions, and cross-agent communication channels.
12. `prompt-defense`: Scans prompts for jailbreaks, prompt injection, and suppression patterns.
13. `claude-code`: Covers Claude Code specific settings, hook schemas, and frontmatter constraints.
14. `codex`: Inspects OpenAI Codex workspace policies and harness declarations.
15. `harnesses`: Evaluates multi-agent runtime boundaries (Antigravity, OpenCode, Hermes).

---

## Programmatic & Manual Audit Playbook

When running on an environment without `npx` or Node.js runtime, perform the manual inspection checklist:

### Step 1: Scan for Hardcoded Secrets
Run a deterministic pattern search across agent configuration directories:
```bash
grep -rnE "(sk-ant-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9]{30,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z-_]{35})" \
  .claude .agents .opencode ~/.gemini/config/ 2>/dev/null || true
```
If any matches are found, replace the literal secret with an environment variable reference (e.g. `$ANTHROPIC_API_KEY`).

### Step 2: Audit Permission Wildcards
Inspect settings files for wildcard permissions:
```bash
grep -rnE "Bash\(\*\)|Bash\(\s*\"?\*\"?\s*\)|\"\*\"" \
  .claude .agents .opencode 2>/dev/null || true
```
Replace any `Bash(*)` entry with specific command prefixes: `Bash(git *)`, `Bash(python3 *)`, `Bash(npm test)`.

### Step 3: Verify PreToolUse Hook Coverage
Check whether dangerous tool executions have pre-execution validation:
- Examine `settings.json` under `hooks`.
- If `PostToolUse` is declared but `PreToolUse` is missing, tool calls can run unmonitored.
- Ensure PreToolUse hooks validate command arguments and fail closed on unrecognized input.

### Step 4: Audit MCP Server Roots
Inspect MCP filesystem servers in `mcp-servers.json`:
- Reject filesystem servers configured with root `/` or home `~`.
- Ensure paths are confined to the workspace root (`./` or `./src`).

### Step 5: Audit Skills for Supply-Chain Attacks
Inspect all `SKILL.md` and hook scripts in `.agents/skills/`:
- Check for dangerous pipe-to-shell installer patterns: `curl | bash`, `wget | sh`.
- Verify external links and dependencies are pinned to trusted sources.
- Confirm zero decorative or misleading emoji characters that could obfuscate findings.

---

## Scoring & Grade Matrix

AgentShield computes a weighted grade from 0 to 100 based on finding severity:

| Grade | Score | Posture | Action Required |
|---|---|---|---|
| A | 90 - 100 | Strong | Safe for production and autonomous execution. |
| B | 80 - 89 | Good | Minor warnings; low or medium findings only. |
| C | 70 - 79 | Moderate | Requires review; several medium findings or single high finding. |
| D | 60 - 69 | Deficient | Unsafe; multiple high severity findings present. |
| F | 0 - 59 | Critical Risk | Block immediately. CRITICAL secret or wildcard permission detected. |

### Severity Scoring Weights

- **CRITICAL** (25 points deduction): Hardcoded production secrets, `Bash(*)`, unauthenticated remote RCE.
- **HIGH** (15 points deduction): Missing deny list on active shell, root filesystem MCP, prompt injection surface.
- **MEDIUM** (5 points deduction): Missing PreToolUse hooks on read-only tools, loose package manager flags.
- **LOW** (1 point deduction): Informational posture notices, documentation inconsistencies.

---

## Triage & False-Positive Handling

To prevent alarm fatigue, AgentShield uses source-kind confidence classification:

- `template-example`: Findings in catalog templates (e.g. `mcp-configs/mcp-servers.json`) are discounted by 0.75x and capped at 10 deduction points per category.
- `docs-example`: Findings in `docs/` or markdown tutorials downgrade severity by one level (e.g. critical to high).
- `project-local-optional`: Findings in `.claude/settings.local.json` with pinned URLs are recognized as local overrides.
- `hook-code`: Non-shell hook implementations are inspected with AST-aware language signals rather than raw regex.

---

## Remediation Playbook

### Pattern 1: Hardcoded API Key
- **Finding:** Hardcoded Anthropic/OpenAI API key in `settings.json` or `CLAUDE.md`.
- **Remediation:** Remove token from file. Export environment variable in shell rc (`export ANTHROPIC_API_KEY="..."`). Reference `$ANTHROPIC_API_KEY` in code.

### Pattern 2: Overly Permissive `Bash(*)`
- **Finding:** `Bash(*)` entry in `permissions.allow`.
- **Remediation:** Split into exact permitted prefixes:
  ```json
  {
    "permissions": {
      "allow": [
        "Bash(git status)",
        "Bash(git diff *)",
        "Bash(npm test)",
        "Bash(python3 -B test_all.py)"
      ],
      "deny": [
        "Bash(rm -rf *)",
        "Bash(sudo *)",
        "Bash(curl * | bash)"
      ]
    }
  }
  ```

### Pattern 3: Missing Deny List
- **Finding:** Configuration defines `allow` rules without an explicit `deny` guardrail list.
- **Remediation:** Add explicit `deny` rules for destructive shell commands, privilege escalation, and network exfiltration tools.

---

## Provenance & Attribution

- **Original Author:** Affaan Mustafa ([@affaan-m](https://github.com/affaan-m))
- **Upstream Repository:** [https://github.com/affaan-m/agentshield](https://github.com/affaan-m/agentshield)
- **License:** MIT License
- **Version Tracked:** 1.6.0 (Commit `b0891303bdcd6037376a94263d45cfd2ff3dfb98`)
- **Ecosystem:** Part of the Everything Claude Code (ECC) security ecosystem.
- **GraviDex Status:** Candidate (Staged for 7-day observation under GraviDex governance).

