# AgentShield False-Positive Taxonomy & Triage Guide

This reference provides operational guidance for interpreting AgentShield audit reports and distinguishing genuine security risks from benign templates, documentation examples, and project-local overrides.

## Confidence Levels and Weighting

AgentShield assigns a `runtimeConfidence` rating to every detected finding:

| Source Kind | Weight | Meaning | Example Path |
|---|---|---|---|
| `active-runtime` | 1.0x | File is actively loaded in agent runtime execution | `.claude/settings.json`, `.agents/skills/` |
| `project-local-optional` | 0.75x | User-local override file, not shared across team | `.claude/settings.local.json` |
| `plugin-manifest` | 0.5x | Declared manifest behavior requiring companion script | `hooks/hooks.json` |
| `template-example` | 0.25x | Catalog or template file; not active configuration | `mcp-configs/mcp-servers.json` |
| `docs-example` | 0.25x | Documentation or tutorial sample configuration | `docs/examples/settings.json` |

---

## Triage Matrix: Common Edge Cases

### 1. Template Catalogs (`template-example`)
- **Symptom:** High finding count (e.g., 50+ findings) in `mcp-configs/` or similar catalog repositories.
- **Triage:** These represent available options for users, not active runtime configurations.
- **Rule:** Deductions are capped at 10 points per score category. Review findings for supply-chain risks if any template is copied into active `settings.json`.

### 2. Documentation and Markdown Examples (`docs-example`)
- **Symptom:** Hardcoded dummy keys like `sk-ant-test12345` or placeholder allowlists in `README.md` or `docs/`.
- **Triage:** If the key is clearly a synthetic dummy token or within a fenced markdown tutorial, it is a documentation artifact.
- **Exception:** Real production keys (e.g. valid `ghp_...` tokens) found in documentation remain CRITICAL risks because public git commits leak credentials regardless of file path.

### 3. Exact Network Allow Rules vs. Overly Permissive Commands
- **Symptom:** Finding flags `Bash(curl https://api.github.com/repos/...)` as permissive command.
- **Triage:** Pinned, explicit URLs with exact argument signatures do not constitute arbitrary shell access.
- **Verdict:** Downgrade from HIGH to INFO if the command target and URL are fixed without parameter substitution.

### 4. Narrow Specialist Subagent Capabilities
- **Symptom:** Subagent configuration for a code-reviewer or test-runner requests `Bash` access.
- **Triage:** Dedicated task runners need execution capabilities. If the subagent's scope is strictly constrained in prompt and tools, the severity is MEDIUM rather than HIGH. Generalist assistants with full shell access remain HIGH.

### 5. Repository-Scoped Filesystem MCP
- **Symptom:** Filesystem MCP server mounted at `./` or `./workspace`.
- **Triage:** Mounting the current repository root is standard practice for coding agents.
- **Verdict:** Graded as MEDIUM or ACCEPTABLE. Only mount roots targeting `/` (system root) or `~` (entire user home directory) are graded as HIGH risk.

