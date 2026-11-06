---
name: autonomous-agent-engineering
description: "Core discipline, orchestration, and decision-making for autonomous AI coding agents. Enforces minimal diffs (Ponytail Engine), silent self-interrogation across 14 engineering domains (Socratic), multi-agent deliberation (Court & Arena), multi-model resilience (Model Router), durable memory vault, context budget management, and intent scoping."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [agents, orchestration, multi-model, memory, yagni, deliberation]
  sources_count: 11
---

# Autonomous Agent Engineering

Consolidated capability governing agent execution discipline, minimal diff footprints, adversarial deliberation, multi-model resilience, durable context sharing, and context budget management.

## When to Activate
- Scoping ambiguous or underspecified user requests into testable acceptance criteria.
- Enforcing minimal diffs, YAGNI, and standard library reuse on coding tasks.
- Interrogating system architecture silently across 14 engineering domains before planning.
- Stress-testing architectural proposals or technical claims via adversarial deliberation (Court / Arena).
- Managing multi-model failover cascades (429 handling) and task specialization.
- Preserving durable memory across agent sessions or managing context compaction.

## When NOT to Activate
- Direct implementation of frontend React code (use `frontend-engineering`).
- Writing unit and E2E test suites (use `quality-engineering`).

## Core Execution Workflow

1. **Ponytail Minimal Diff & YAGNI Principle:**
   - Smallest complete diff: write the fewest changed lines, touch the fewest files, introduce zero speculative abstractions. Standard library first.
   - Consult [references/ponytail-yagni.md](references/ponytail-yagni.md).

2. **Silent Pre-Implementation Interrogation (Socratic):**
   - Interrogate design silently across 14 engineering domains (requirements, API, security, infra, data, testing). Surface only decisions requiring human authority.
   - Consult [references/socratic-interrogation.md](references/socratic-interrogation.md).

3. **Adversarial Deliberation (Court & Arena):**
   - When proposals require rigorous critical pushback, simulate prosecution/defense debate or bracket tournaments.
   - Consult [references/court-deliberation.md](references/court-deliberation.md) and [references/arena-tournament.md](references/arena-tournament.md).

4. **Multi-Model Resilience & Context Vault:**
   - Route algorithmic reasoning to deep thinking models; cascade on 429 rate limits.
   - Maintain durable handoffs via memory vaults and compact context at natural task boundaries.
   - Consult [references/model-router.md](references/model-router.md), [references/agent-unified-memory.md](references/agent-unified-memory.md), and [references/context-budget-compaction.md](references/context-budget-compaction.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [ponytail-yagni.md](references/ponytail-yagni.md) | Lazy senior dev mode, minimal diffs, YAGNI, standard library first | `hamzzaqureshi/gravidex` (`ponytail`) |
| [socratic-interrogation.md](references/socratic-interrogation.md) | Silent self-interrogation across 14 engineering domains | `hamzzaqureshi/gravidex` (`socratic`) |
| [court-deliberation.md](references/court-deliberation.md) | Adversarial panel trial (prosecutor, defense, jury, verdict) | `hamzzaqureshi/gravidex` (`court`) |
| [arena-tournament.md](references/arena-tournament.md) | Single-elimination subagent bracket tournament deliberation | `hamzzaqureshi/gravidex` (`arena`) |
| [model-router.md](references/model-router.md) | Task-specialized model routing and resilient 429 failover cascade | `hamzzaqureshi/gravidex` (`model-router`) |
| [impeccable-lifecycle.md](references/impeccable-lifecycle.md) | 24-command design lifecycle system and UI architecture framework | `hamzzaqureshi/gravidex` (`impeccable`) |
| [agent-unified-memory.md](references/agent-unified-memory.md) | Durable memory vault and handoffs across Claude, OpenCode, Antigravity | `affaan-m/ECC` (`unified-memory`) |
| [agent-introspection-recovery.md](references/agent-introspection-recovery.md) | Structured agent self-debugging and failure recovery reports | `affaan-m/ECC` (`agent-introspection-debugging`) |
| [context-budget-compaction.md](references/context-budget-compaction.md) | Context capacity checks, strategic compaction at logical phases | `affaan-m/ECC` (`context-budget`, `strategic-compact`) |
| [intent-driven-scoping.md](references/intent-driven-scoping.md) | Scoping ambiguous user requests into verifiable acceptance criteria | `affaan-m/ECC` (`intent-driven-development`) |
| [plan-canvas-annotations.md](references/plan-canvas-annotations.md) | Interactive local browser canvas for plan review and annotations | `affaan-m/ECC` (`plan-canvas`) |
