# Autonomous Engineering Rules for Antigravity

These rules are automatically loaded into every conversation turn. They eliminate the need for manual slash commands by enforcing core disciplines autonomously.

---

## 1. Minimal Diff & YAGNI Principle (Ponytail Engine)
- **Smallest Complete Diff**: Choose the solution with the fewest changed lines, fewest files touched, and zero unnecessary abstractions.
- **Standard Library First**: Never introduce third-party dependencies or pip/npm packages when native platform capabilities or Python/Node standard libraries suffice.
- **Clean Scope**: Do not reformat, rewrite, or touch unrelated functions, comments, or whitespace.

---

## 2. Empirical Verification Gate (Rigor Engine)
- **Zero Hallucinated Completion**: Never declare a task, bug fix, or refactor complete until you have executed real verification tests on disk.
- **Check Evidence**: Run `python3 -B test_all.py` or the specific test suite. Inspect exit codes (must be 0) and verify that all test assertions passed.
- **Log Proof**: Report the exact runtime and test count in your final summary.

---

## 3. Anti-Slop Frontend & Typographic Discipline (Anti-VCode)
- **Banned Patterns**: Forbid generic AI aesthetics: centered purple/cyan glow effects, gratuitous glassmorphism, floating cards without grid purpose, and generic placeholder copy.
- **Design Foundations**: Enforce Swiss grid discipline, restrained motion (< 300ms, standard easing), and accessible contrast (WCAG AAA/AA).

---

## 4. Multi-Model Resilience & Automatic Failover (Model Router)
- **Task Specialization**:
  - Complex algorithmic edge cases, mathematical reasoning, or race conditions: route to `deepseek/deepseek-r1`.
  - Fast boilerplate, bulk refactoring, and file transforms: route to `qwen/qwen-2.5-coder-32b` or Groq.
- **Automatic 429 Cascade**: If an external API returns `HTTP 429` (Rate Limited) or quota exhaustion, automatically cascade to the next configured fallback provider without halting workflow momentum.

---

## 5. Strict Emoji Ban
- Do not output emoji characters in code, documentation, test suites, terminal logs, or git commit messages.

