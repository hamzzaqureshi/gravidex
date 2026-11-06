---
name: technical-documentation
description: "Author and maintain professional technical documentation, repository READMEs, Architectural Decision Records (ADRs), codebase onboarding guides, and Git collaboration workflows. Enforces README-driven development (50-point scorecard), humanized anti-AI prose polishing, and clean conventional commits."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [documentation, readme, adr, onboarding, prose-polish, git-workflow]
  sources_count: 6
---

# Technical Documentation

Consolidated capability for authoring production repository READMEs, Architectural Decision Records (ADRs), codebase onboarding maps, polished human prose, and clean Git workflows.

## When to Activate
- Writing, auditing, or refactoring GitHub READMEs across 5 project archetypes.
- Recording architectural decisions as numbered ADRs with trade-off analysis.
- Onboarding to an unfamiliar codebase and generating architecture entrypoint guides.
- Polishing AI-generated documentation to eliminate generic filler, buzzwords, and AI tells (Humanizer).
- Formulating conventional commit messages, PR descriptions, and Git branching workflows.
- Enforcing cross-language coding standards (naming, file organization, immutability).

## When NOT to Activate
- Authoring unit or integration test suites (use `quality-engineering`).
- Writing system architecture code (use `backend-engineering` or `frontend-engineering`).

## Core Execution Workflow

1. **README-Driven Development:**
   - Guide the reader's journey: Discover -> Understand -> Start -> Use/Contribute.
   - Audit READMEs against the 50-point quality scorecard.
   - Consult [references/readme-driven-development.md](references/readme-driven-development.md).

2. **Architectural Decision Records (ADR):**
   - Record significant technical choices in `docs/adr/NNNN-decision.md` covering context, alternatives considered, decision, consequences, and status. Maintain index README.
   - Consult [references/architecture-decision-records.md](references/architecture-decision-records.md).

3. **Prose Polishing (Humanizer):**
   - Eliminate AI writing tells: staged openers, forced triads, excessive em-dashes, and buzzword padding.
   - Consult [references/humanizer-editorial-guide.md](references/humanizer-editorial-guide.md).

4. **Codebase Onboarding & Git Workflow:**
   - Document project entry points and conventions. Enforce clean conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`).
   - Consult [references/codebase-onboarding.md](references/codebase-onboarding.md) and [references/git-collaboration-workflow.md](references/git-collaboration-workflow.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [readme-driven-development.md](references/readme-driven-development.md) | 50-point quality scorecard, reader journey, 5 project archetypes | `hamzzaqureshi/gravidex` (`writing-readme`) |
| [architecture-decision-records.md](references/architecture-decision-records.md) | Numbered ADR authoring, alternatives, consequences, index README | `affaan-m/ECC` (`architecture-decision-records`) |
| [humanizer-editorial-guide.md](references/humanizer-editorial-guide.md) | 26-pattern anti-AI prose polishing, eliminating corporate filler | `hamzzaqureshi/gravidex` (`humanizer`) |
| [codebase-onboarding.md](references/codebase-onboarding.md) | Unfamiliar codebase analysis, architecture map, starter CLAUDE.md | `affaan-m/ECC` (`codebase-onboarding`) |
| [git-collaboration-workflow.md](references/git-collaboration-workflow.md) | Conventional commits, PR workflows, clean local history | `affaan-m/ECC` (`git-workflow`) |
| [coding-standards.md](references/coding-standards.md) | Baseline cross-project naming, readability, immutability conventions | `affaan-m/ECC` (`coding-standards`) |
