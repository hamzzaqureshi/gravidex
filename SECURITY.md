# GraviDex Security Policy

Security and supply-chain defense are paramount in the GraviDex architecture. Because AI agent skills instruct coding models to execute system commands, access files, and orchestrate tooling, all skills are treated as untrusted supply-chain inputs until audited and approved.

---

## 1. Security Principles

1. **Zero Unsafe Shell Execution:**
   - Blind execution via `curl ... | bash` or `wget ... | sh` is strictly banned.
   - All external installations must download to an inspected temporary script, verify integrity, and execute with contained permissions.
2. **Zero Credential Exposure:**
   - Skills must never hardcode API keys, access tokens, credentials, or private keys.
   - All secrets must be loaded via standard environment variables or dedicated secret management stores.
3. **Privilege Containment:**
   - Skills must not execute `sudo` or request root privileges without explicit user authorization.
   - Skills must run within standard sandboxed environments whenever available.
4. **Supply Chain Provenance:**
   - Every skill must trace back to an immutable upstream commit SHA.
   - Any local modifications must be captured as verifiable unified diffs in `PATCHES/`.
5. **Prompt Injection & Directive Defense:**
   - Third-party skills must never be allowed to override system-level safety rules, governance documents, or user operating directives.

---

## 2. Automated Security Auditing

Every skill entering GraviDex is checked via `scripts/audit.py` and `scripts/validate.py` against:

- Dangerous shell execution patterns.
- Credential harvesting patterns.
- Hidden execution and obfuscated scripts.
- Unexpected remote network downloads.
- Path traversal and unauthorized filesystem manipulation.

Results are documented in `AUDIT/SECURITY-REPORT.md`.

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability or suspect a malicious supply-chain pattern in any registered skill:

1. Do NOT open a public GitHub issue with exploit details.
2. Isolate the affected skill directory immediately.
3. Demote the skill to `SKILLS/archived/` and update its status in `registry.yaml` to `quarantined`.
4. Submit a documented security finding report including:
   - Skill ID and upstream repository.
   - Specific file path and offending line range.
   - Reproduction steps in an isolated sandbox.
   - Recommended patch in `PATCHES/`.
