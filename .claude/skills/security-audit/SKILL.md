---
name: security-audit
description: "Perform comprehensive security reviews and vulnerability assessments across codebases, APIs, and microservices. Covers OWASP Top 10 detection, input sanitization, authentication/authorization validation, credential leakage prevention, and secure code-authoring workflows. Use before commits, during PR reviews, or when handling sensitive data."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [security, audit, owasp, auth, secret-detection]
  sources_count: 2
---

# Security Audit

Consolidated capability for auditing codebase security, validating authentication/authorization boundaries, preventing credential exposure, and enforcing secure development standards.

## When to Activate
- Reviewing code that handles user input, authentication, payments, or file system access.
- Conducting pre-commit security audits of API endpoints, database queries, and environment configs.
- Scanning for hardcoded secrets, API tokens, SQL injection, XSS, SSRF, or path traversal vulnerabilities.
- Verifying rate limiting, CORS policies, and CSRF protection on public endpoints.

## When NOT to Activate
- Auditing AI agent harness configurations (.claude/, .agents/, hooks, MCP allowlists) (use `agentshield`).
- General code quality or naming refactoring (use `technical-documentation`).

## Core Execution Workflow

1. **Mandatory Security Checklist:**
   - Zero hardcoded credentials or API keys.
   - All external user input validated with strict schemas before processing.
   - Parameterized SQL/database queries (no string concatenation).
   - Rate limiting and CSRF protection enabled on all mutable endpoints.
   - Consult [references/codebase-security-audit.md](references/codebase-security-audit.md).

2. **Secure Code-Authoring Review:**
   - Execute the 6-phase review before any commit touching auth, payments, or sensitive state.
   - Consult [references/secure-coding-review.md](references/secure-coding-review.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [codebase-security-audit.md](references/codebase-security-audit.md) | Comprehensive 6-phase security review, vulnerability classification, reports | `hamzzaqureshi/gravidex` (`secure-audit`) |
| [secure-coding-review.md](references/secure-coding-review.md) | Code-authoring security triggers, auth checklists, OWASP patterns | `affaan-m/ECC` (`security-review`) |
