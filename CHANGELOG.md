# GraviDex Changelog

All notable changes, migrations, audits, and security updates for GraviDex are documented in this file.
The format is based on Keep a Changelog.

---

## [2.2.0] - 2026-11-07

### Capabilities Expansion: Karpathy Guidelines & Stageshow Faux UI
- **Active Capabilities Suite (21 Active Capabilities):**
  - Expanded from 19 to 21 active capabilities (8 Curated Capability Packs + 13 Retained Independent Specialists).
  - Integrated 2 new Retained Specialists:
    - `karpathy-guidelines`: Behavioral guidelines derived from Andrej Karpathy's observations on LLM coding pitfalls. Enforces 4 core pillars: Think Before Coding, Simplicity First, Surgical Changes, and Goal-Driven Execution. Includes sanitized reference examples, Claude Code behavioral integration, and Cursor IDE rule definitions.
    - `stageshow`: Benji Taylor's faux product UI engine. Features deterministic React interaction choreography (`Act<S>` API), device geometry for macOS/iOS Dynamic Island/browsers, realistic cursor arcs, and automated contact-sheet frame verification scripts (`film.mjs`, `jumps.mjs`, `layout.mjs`).
- **Zero-Emoji Governance Enforcement:**
  - Sanitized all upstream emoji characters across code, fixtures, and documentation to strictly uphold the zero-emoji ban.
- **Unified Test Harness:**
  - Expanded from 29 to 31 parallel test suites with high-performance sandboxing (`test_karpathy_guidelines.py`, `test_stageshow.py`).
  - 100% test pass rate across all suites.
- **Installer & Registry Updates:**
  - Updated `install.py` and `install.sh` to support all 21 capabilities across interactive and automated modes.
  - Synchronized `CAPABILITIES/capability-registry.yaml`, `.agents/skills`, `.claude/skills`, and `.opencode/skills`.

---

## [2.1.0] - 2026-11-06

### Capabilities Expansion & Distribution Architecture
- **Active Capabilities Suite (19 Active Capabilities):**
  - Expanded from 13 to 19 active capabilities (8 Curated Capability Packs + 11 Retained Independent Specialists).
  - Integrated 6 new Retained Specialists:
    - `asd-ste100`: Simplified Technical English (Issue 9) & Karpathy 80% Pragmatic Mode, deterministic standard library linter (`ste_lint.py`), and offline dictionary lookup (`ste_lookup.py`).
    - `boardui`: React design system for agentic dashboards (69 source components, 400+ semantic tokens, RTL support).
    - `awwwards`: Award-caliber site builder, art direction, and WebGL animation engine.
    - `jury`: Objective blind-critic website scoring against Awwwards juror standards.
    - `motionsites-web-builder`: Cinematic motion recipes, media shelf, and Playwright screenshot QA loop.
    - `lemo-opuscar`: 67-style algorithmic film directing, Kokoro TTS voice, and procedural audio.
- **Unified Test Harness:**
  - Expanded to 29 parallel test suites with high-performance sandboxing.
  - Added public repository checkout resiliency for CI runners and clean installations.
- **Packaging & Documentation:**
  - Standardized release packaging via `package.py` producing `gravidex.zip` (6.89 MB), `gravidex.tar.gz` (6.36 MB), and Antigravity plugin drop-in `gravidex-pack/`.
  - Achieved 50/50 on the Writing README Quality Scorecard and 100/100 on the Humanizer Prose Audit.
  - Verified 100% passing GitHub Actions CI across Python 3.10, 3.11, 3.12, and 3.13.

---

## [2.0.0] - 2026-11-05

### Capability Consolidation & Source Preservation Architecture
- **Two-Layer Architecture:** Migrated GraviDex from an uncurated collection of 48 individual skills into a two-layer capability library:
  - **Layer A (Source Library - `SOURCES/`):** Full, immutable upstream source archive preserving all 48 original skills across 6 upstream repositories (`hamzzaqureshi-gravidex`, `affaan-m-ecc`, `heydamir-unslop`, `dickwu-apple-design`, `affaan-m-agentshield`, `tripleyak-skillforge`) with `source-index.yaml` and `license-register.yaml`.
  - **Layer B (Curated Capability Library - `CAPABILITIES/`):** 13 active runtime capabilities (8 Curated Capability Packs + 5 Retained Independent Specialists) exposed to Google Antigravity IDE, OpenCode, and Claude Code.
- **Cognitive & Token Footprint Reduction:**
  - Active runtime entry points reduced from 48 down to 13 (-73%).
  - Discovery `SKILL.md` word count reduced from 90,714 words down to ~14,200 words (-84%).
  - Deployed directory footprint reduced from 169 down to 39 directories (-77%).
- **Curated Capability Packs (`CAPABILITIES/curated/`):**
  - `autonomous-agent-engineering`: Ponytail minimal diffs, Socratic interrogation, Court, Arena, Model Router, Impeccable lifecycle, ECC memory vault.
  - `backend-engineering`: API design, backend patterns, error handling, MCP server patterns.
  - `design-systems`: TypeUI 67 themes, Sanzo Wada color matrix, logo design identity, editorial diagram design.
  - `frontend-engineering`: Frontend React/Next.js patterns, Three.js WebGL scenes, browser QA verification.
  - `interface-design`: Apple HIG design, UI/UX Pro Max guidelines, anti-slop redline pass, taste motion calibration.
  - `quality-engineering`: Test-driven development, empirical verification (Rigor), E2E testing, evaluation harness.
  - `security-audit`: Coverage-led vulnerability hunting, OWASP Top 10 detection, security review.
  - `technical-documentation`: README-driven development, Architectural Decision Records (ADRs), codebase onboarding, git workflow.
- **Retained Independent Specialists (`CAPABILITIES/retained-specialists/`):**
  - `agentshield`: Hardened agent harness and configuration auditor.
  - `last30days`: Real-time cross-platform social intelligence engine.
  - `rev-engineer`: Reverse engineering and binary deconstruction tools.
  - `scrapling`: Adaptive web scraping, stealth browsing, and anti-bot bypass.
  - `skillforge`: AI agent skill lifecycle management and governance.
- **Operational Automation & Lifecycle Tools:**
  - `scripts/rebuild-capabilities.py`: Automated three-way rebuild and upstream drift analysis engine.
  - `scripts/consolidate.py`: Interactive and scripted engine for consolidating future skills into capability packs.
  - `scripts/validate.py`: Upgraded to support `--capabilities` and `--all-scopes`.
  - `scripts/rollback.sh`: Added instant non-destructive rollback capability.
  - `test_all.py`: Expanded to 26 suites, integrating capability verification, governance rules, and isolated sandboxes.
- **Governance & Policy Artifacts:**
  - Established `GOVERNANCE/` documentation: `SOURCE-PROVENANCE.md`, `CONSOLIDATION-POLICY.md`, `UPDATE-POLICY.md`, `QUALITY-STANDARDS.md`, `RELEASE-POLICY.md`.
  - Established `AUDIT/` consolidation records: `PRE-CONSOLIDATION-INVENTORY.md`, `CONSOLIDATION-ARCHITECTURE.md`, `SKILL-CONSOLIDATION-MAP.md`, `SOURCE-MAPPING.md`, `CONSOLIDATION-REPORT.md`.
- **Strict Compliance:**
  - 100% zero-emoji enforcement across code, markdown, logs, and manifests.
  - Zero external dependencies: pure Python standard library only.
  - Non-destructive legacy quarantine staged in `QUARANTINE/legacy-runtime-backup/`.

---

## [1.0.0] - 2026-11-04

### Ecosystem Initialization & Governance Architecture
- **Governance Framework:** Established `GRAVIDEX.md` master specification, operating rules, and supply-chain protocols.
- **Central Registry:** Established `registry.yaml` tracking 44 skills (22 approved production skills, 22 candidate workflow skills) under `https://github.com/hamzzaqureshi/gravidex`.
- **Directory Canonicalization:** Created `SKILLS/approved/`, `SKILLS/candidates/`, and `SKILLS/archived/` tiers to isolate production skills from candidates undergoing 7-day observation.
- **Audit Reports Generated:**
  - `AUDIT/INVENTORY.md`: Discovered and mapped 131 skill instances across repository root, canonical storage, Antigravity global (`~/.gemini/config/skills/`), and OpenCode.
  - `AUDIT/QUALITY-REPORT.md`: Evaluated all 44 skills against the 100-point rubric (average quality score: 94.0/100).
  - `AUDIT/SECURITY-REPORT.md`: Verified zero critical vulnerabilities and safe command execution across all skills.
  - `AUDIT/COMPATIBILITY-REPORT.md`: Verified cross-platform execution readiness for Antigravity, OpenCode, and Claude Code.
  - `AUDIT/UPDATE-REPORT.md`: Established baseline commit tracking for upstream provenance.

### Security Remediation & Patches
- **Safe Installer Patch (last30days):** Applied `PATCHES/last30days-safe-installer.patch` to neutralize unsafe `curl -fsSL ... | bash` patterns, replacing them with verified download-inspect-execute commands.
- **Safe Installer Patch (writing-readme):** Applied `PATCHES/writing-readme-safe-installer.patch` in CLI documentation template.
- **Runtime Binary Guard (test_all.py):** Applied `PATCHES/test-all-node-fallback.patch` to prevent test runner crashes in environments lacking a `node` runtime.

### Automation Tooling
- **Inventory Engine:** Implemented `scripts/inventory.py` and `scripts/inventory.sh`.
- **Quality & Security Auditor:** Implemented `scripts/audit.py` and `scripts/audit.sh`.
- **Structural Validator:** Implemented `scripts/validate.py` and `scripts/validate.sh`.
- **Upstream Tracker:** Implemented `scripts/check-updates.py` and `scripts/check-updates.sh`.
- **Platform Synchronizer:** Implemented `scripts/sync-skills.py` and `scripts/sync-skills.sh`.
- **Automated Test Suite:** Created `TESTS/validation/test_skills.py` enforcing YAML frontmatter validation, zero emoji compliance, and supply-chain safety.

---

## [0.9.0] - 2026-10-29

### Production Skills Suite Baseline
- Established original 21 production skills in repository root.
- Integrated `model-router` for resilient 429 rate-limit failover across DeepSeek, Claude, and Qwen.
- Implemented high-performance parallel test runner `test_all.py` executing 21 isolated sandboxes.
