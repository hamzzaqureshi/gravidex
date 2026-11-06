---
name: quality-engineering
description: "Empirical quality assurance, automated testing, and verification discipline for AI coding agents. Enforces test-driven development (TDD) with 80%+ coverage, Playwright E2E automation, formal evaluation harnesses, pre-completion verification checklists, delivery gates, and documentation grounding. Use when writing tests, verifying bug fixes, or running pre-completion gates."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [testing, tdd, e2e, verification, rigor, delivery-gate]
  sources_count: 6
---

# Quality Engineering

Consolidated capability for empirical test-driven development, automated end-to-end verification, eval harnesses, and rigorous completion gates.

## When to Activate
- Authoring unit, integration, or E2E tests before or alongside code changes.
- Enforcing test-driven development (RED -> GREEN -> REFACTOR) with 80%+ test coverage.
- Building or running Playwright end-to-end test suites with Page Object Model.
- Executing pre-completion verification checklists before declaring tasks finished.
- Enforcing mechanical delivery gates against hallucinated task completion.

## When NOT to Activate
- Pure UI design review (use `interface-design`).
- Codebase vulnerability or penetration audits (use `security-audit`).

## Core Execution Workflow

1. **Test-Driven Development (TDD):**
   - Write tests first (RED). Run tests to verify failure. Implement minimal code to pass (GREEN). Refactor cleanly.
   - Enforce Arrange-Act-Assert (AAA) test structure and descriptive test naming.
   - Consult [references/test-driven-development.md](references/test-driven-development.md).

2. **End-to-End Testing & Evals:**
   - Use Playwright Page Object Model for critical user journeys.
   - Formulate eval harnesses for agent tasks with clear scoring rubrics.
   - Consult [references/playwright-e2e-testing.md](references/playwright-e2e-testing.md) and [references/eval-driven-development.md](references/eval-driven-development.md).

3. **Empirical Grounding & Completion Gates:**
   - Zero hallucinated completion: never declare work done without executing real tests on disk and verifying exit code 0.
   - Consult [references/empirical-verification-rigor.md](references/empirical-verification-rigor.md) and [references/pre-completion-verification.md](references/pre-completion-verification.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [test-driven-development.md](references/test-driven-development.md) | TDD workflow, AAA structure, test isolation, 80%+ coverage | `affaan-m/ECC` (`tdd-workflow`) |
| [playwright-e2e-testing.md](references/playwright-e2e-testing.md) | Playwright E2E patterns, Page Object Model, CI/CD integration | `affaan-m/ECC` (`e2e-testing`) |
| [eval-driven-development.md](references/eval-driven-development.md) | Formal evaluation harness, benchmark suites, agent testing | `affaan-m/ECC` (`eval-harness`) |
| [empirical-verification-rigor.md](references/empirical-verification-rigor.md) | Documentation grounding, verifiable task ledgers, exit code proof | `hamzzaqureshi/gravidex` (`rigor`) |
| [pre-completion-verification.md](references/pre-completion-verification.md) | Comprehensive pre-completion checklist, sanity gates | `affaan-m/ECC` (`verification-loop`) |
| [delivery-gate-enforcement.md](references/delivery-gate-enforcement.md) | Mechanical stop hook preventing premature completion | `affaan-m/ECC` (`delivery-gate`) |
