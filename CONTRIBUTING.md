# Contributing to GraviDex

Thank you for your interest in contributing to **GraviDex**! This project provides a production-grade, model-agnostic library of AI coding skills designed for Google Antigravity IDE, OpenCode, Claude Code, and other LLM agent harnesses.

---

## Guiding Principles

1. **Model-Agnostic & Zero External Dependencies**:
   - Helper scripts and engines MUST use the Python standard library only.
   - Avoid external `pip` or `npm` runtime dependencies to ensure instant installation across any environment.
2. **Progressive Disclosure**:
   - Keep `SKILL.md` entrypoints concise and dense with YAML frontmatter.
   - Place specialized references, token dictionaries, and deep technical specs in `references/` so the agent reads them strictly on-demand.
3. **Empirical Verification (100% Pass Rate)**:
   - Every skill must have an automated test suite discoverable via standard `unittest`.
   - Run `python3 -B test_all.py` and `python3 -B -m unittest discover -s TESTS/validation` before submitting any changes.
4. **Strict Emoji Ban**:
   - Do not output emoji characters in code, documentation, test suites, terminal logs, or git commits.

---

## Candidate Ingestion & Lifecycle Workflow

Every new skill follows the GraviDex governance lifecycle:

1. **Evaluation**:
   - Run `python3 -B scripts/audit.py` to evaluate the skill against the 100-point rubric.
   - The skill must achieve an overall score >= 80/100 with zero critical security findings.
2. **Staging**:
   - Add new skill into `SKILLS/candidates/<skill-name>`.
   - Record upstream provenance and SHA in `registry.yaml`.
3. **Seven-Day Observation**:
   - Candidate remains in `SKILLS/candidates/` for 7 days to evaluate real-world usage, stability, and prompt adherence.
4. **Validation & Promotion**:
   - Run `python3 -B scripts/validate.py` to assert YAML schema and link integrity.
   - Run `python3 -B scripts/audit.py` to confirm security status.
   - Promote to `SKILLS/approved/<skill-name>` upon passing observation and owner approval.

---

## Directory Structure for New Skills

Every skill must conform to the following directory layout:

```text
<skill-name>/
├── SKILL.md             # [Required] Concise agent entrypoint with YAML frontmatter
├── README.md            # [Required] Quickstart, commands, and usage documentation
├── LICENSE              # [Required] Open-source license (MIT / Apache-2.0)
├── references/          # [Required/Optional] In-depth guides and progressive disclosure
├── scripts/             # [Required/Optional] Zero-dependency Python CLI or engine
├── resources/           # [Optional] Offline data, templates, or schemas
└── tests/               # [Required] Automated unit tests
```

---

## Step-by-Step: Adding a New Skill

1. **Create the Skill Directory in Candidates**:
   ```bash
   mkdir -p SKILLS/candidates/<skill-name>/{scripts,references,tests}
   ```

2. **Author `SKILL.md`**:
   Ensure it includes valid YAML frontmatter:
   ```markdown
   ---
   name: <skill-name>
   description: "Concise summary of what the skill does and when the agent should invoke it."
   ---
   ```

3. **Author Automated Tests**:
   Create `tests/test_<skill_name>.py` using standard Python `unittest`.

4. **Run Validation and Tests**:
   ```bash
   python3 -B scripts/validate.py
   python3 -B scripts/audit.py
   python3 -B -m unittest discover -s TESTS/validation
   ```
