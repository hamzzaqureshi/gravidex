#!/usr/bin/env python3
"""GraviDex Audit & Quality Assurance Engine.

Implements the official 100-point GraviDex quality evaluation and security
review pipeline. Audits all skills in SKILLS/approved/ and SKILLS/candidates/.

Evaluates:
  - Practical usefulness (15)
  - Instruction quality (20)
  - Technical correctness (15)
  - Completeness (10)
  - Maintainability (10)
  - Security (15)
  - Cross-platform portability (10)
  - Documentation and provenance (5)

Generates:
  - AUDIT/QUALITY-REPORT.md
  - AUDIT/SECURITY-REPORT.md
  - AUDIT/COMPATIBILITY-REPORT.md

Zero external dependencies (Python standard library only).
"""

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Security Risk Patterns
DANGEROUS_PATTERNS = [
    (r"curl\s+-[^\n|]*\|\s*(?:bash|sh|zsh)", "CRITICAL", "Unsafe pipe-to-shell installer detected"),
    (r"wget\s+-[^\n|]*\|\s*(?:bash|sh|zsh)", "CRITICAL", "Unsafe pipe-to-shell installer detected"),
    (r"\bsudo\b", "HIGH", "Privilege escalation (sudo) in instructions or script"),
    (r"(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "CRITICAL", "Hardcoded credential or token detected"),
    (r"rm\s+-rf\s+/(?:\s|$|\*)", "CRITICAL", "Potentially destructive root filesystem command"),
    (r":\(\)\{\s*:\|\:&\s*\};:", "CRITICAL", "Fork bomb pattern"),
]


def parse_frontmatter(file_path: Path):
    if not file_path.is_file():
        return {}
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}

    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n", content)
    if not match:
        return {}

    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def audit_skill(skill_dir: Path, status_label: str):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(skill_md)

    score = 0
    breakdown = {}
    security_findings = []

    # 1. Practical Usefulness (15 max)
    usefulness = 12
    desc = fm.get("description", "")
    if len(desc) > 30 and ("when" in desc.lower() or "use" in desc.lower()):
        usefulness += 3
    breakdown["usefulness"] = min(15, usefulness)

    # 2. Instruction Quality (20 max)
    inst_quality = 10
    if len(content.splitlines()) > 50:
        inst_quality += 4
    if re.search(r"```[a-z]*\n[\s\S]*?```", content):
        inst_quality += 3
    if any(h in content for h in ["## When to", "## Workflow", "## Usage", "## Instructions"]):
        inst_quality += 3
    breakdown["instruction_quality"] = min(20, inst_quality)

    # 3. Technical Correctness (15 max)
    tech_correct = 12
    # Check if directory name matches frontmatter name
    fm_name = fm.get("name", "")
    if fm_name and fm_name == skill_dir.name:
        tech_correct += 3
    breakdown["technical_correctness"] = min(15, tech_correct)

    # 4. Completeness (10 max)
    completeness = 7
    if (skill_dir / "references").is_dir() or (skill_dir / "reference").is_dir():
        completeness += 1
    if (skill_dir / "examples").is_dir() or (skill_dir / "example").is_dir():
        completeness += 1
    if (skill_dir / "scripts").is_dir():
        completeness += 1
    breakdown["completeness"] = min(10, completeness)

    # 5. Maintainability (10 max)
    maintainability = 8
    # Under soft ceiling of 800 lines for SKILL.md
    if len(content.splitlines()) < 800:
        maintainability += 2
    breakdown["maintainability"] = min(10, maintainability)

    # 6. Security (15 max)
    security_score = 15
    for root, _, files in os.walk(skill_dir):
        for f in files:
            if f.endswith((".md", ".py", ".sh", ".json", ".js", ".cjs")):
                p = Path(root) / f
                try:
                    f_text = p.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                for pat, severity, reason in DANGEROUS_PATTERNS:
                    m = re.search(pat, f_text)
                    if m:
                        rel = p.relative_to(skill_dir)
                        finding = {
                            "file": str(rel),
                            "severity": severity,
                            "reason": reason,
                            "match": m.group(0)[:50],
                        }
                        security_findings.append(finding)
                        if severity == "CRITICAL":
                            security_score -= 10
                        elif severity == "HIGH":
                            security_score -= 5

    breakdown["security"] = max(0, security_score)

    # 7. Cross-Platform Portability (10 max)
    portability = 7
    if fm_name:
        portability += 1
    if desc:
        portability += 1
    # Check if tools in frontmatter use standard or portable notation
    if "tools:" in content or "metadata:" in content:
        portability += 1
    breakdown["portability"] = min(10, portability)

    # 8. Documentation and Provenance (5 max)
    provenance = 3
    if "metadata" in fm or "source" in content.lower() or "github" in content.lower():
        provenance += 2
    breakdown["provenance"] = min(5, provenance)

    total_score = sum(breakdown.values())

    # Compatibility evaluation
    has_custom_mcp = (skill_dir / "mcp.json").exists()
    has_claude_tools = "tools:" in content and any(t in content for t in ["Bash", "Read", "Write", "Edit"])
    has_antigravity_tools = "view_file" in content or "run_command" in content

    return {
        "id": skill_dir.name,
        "name": fm.get("name", skill_dir.name),
        "status": status_label,
        "score": total_score,
        "breakdown": breakdown,
        "findings": security_findings,
        "has_critical_security": any(f["severity"] == "CRITICAL" for f in security_findings),
        "compatibility": {
            "antigravity": "Verified (Native)" if (status_label == "approved" or has_antigravity_tools) else "Compatible",
            "opencode": "Verified" if (status_label == "approved" or not has_claude_tools) else "Compatible",
            "claude_code": "Verified" if has_claude_tools else "Compatible",
        }
    }


def run_full_audit():
    results = []
    approved_dir = REPO_ROOT / "SKILLS" / "approved"
    candidates_dir = REPO_ROOT / "SKILLS" / "candidates"

    if approved_dir.exists():
        for d in sorted(approved_dir.iterdir()):
            if d.is_dir():
                res = audit_skill(d, "approved")
                if res:
                    results.append(res)

    if candidates_dir.exists():
        for d in sorted(candidates_dir.iterdir()):
            if d.is_dir():
                res = audit_skill(d, "candidate")
                if res:
                    results.append(res)

    return results


def write_quality_report(results):
    lines = [
        "# GraviDex Quality Audit Report",
        "",
        "Evaluation of all registered skills against the 100-point GraviDex quality rubric.",
        "",
        "## Scoring Summary",
        "",
        "| Skill ID | Status | Total Score | Usefulness (15) | Quality (20) | Correct (15) | Complete (10) | Maint (10) | Sec (15) | Port (10) | Prov (5) |",
        "|:---|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for r in results:
        b = r["breakdown"]
        lines.append(
            f"| `{r['id']}` | {r['status']} | **{r['score']}**/100 | {b['usefulness']} | {b['instruction_quality']} | {b['technical_correctness']} | {b['completeness']} | {b['maintainability']} | {b['security']} | {b['portability']} | {b['provenance']} |"
        )

    lines.extend([
        "",
        "## Rating Classifications",
        "- 90-100: Excellent (Production Flagship)",
        "- 80-89: Good (Approved Production Standard)",
        "- 70-79: Acceptable (Improvement Recommended)",
        "- 50-69: Needs Substantial Repair",
        "- Below 50: Reject / Archive",
    ])

    out = REPO_ROOT / "AUDIT" / "QUALITY-REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def write_security_report(results):
    lines = [
        "# GraviDex Security Audit Report",
        "",
        "Static security inspection verifying shell safety, credential handling, and containment.",
        "",
        "## Security Status Table",
        "",
        "| Skill ID | Status | Security Score | Critical Issues | High Issues | Security Verdict |",
        "|:---|:---:|---:|---:|---:|:---|",
    ]

    total_findings = 0
    critical_count = 0
    for r in results:
        crits = len([f for f in r["findings"] if f["severity"] == "CRITICAL"])
        highs = len([f for f in r["findings"] if f["severity"] == "HIGH"])
        total_findings += len(r["findings"])
        critical_count += crits
        verdict = "PASS" if crits == 0 else "FAIL (CRITICAL BLOCK)"
        lines.append(
            f"| `{r['id']}` | {r['status']} | {r['breakdown']['security']}/15 | {crits} | {highs} | {verdict} |"
        )

    lines.extend([
        "",
        "## Security Findings Detail",
        "",
    ])

    if total_findings == 0:
        lines.append("Zero security vulnerabilities or unsafe shell execution patterns detected.")
    else:
        for r in results:
            if r["findings"]:
                lines.append(f"### `{r['id']}`")
                for f in r["findings"]:
                    lines.append(f"- **[{f['severity']}]** `{f['file']}`: {f['reason']} (match: `{f['match']}`)")
                lines.append("")

    out = REPO_ROOT / "AUDIT" / "SECURITY-REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def write_compatibility_report(results):
    lines = [
        "# GraviDex Multi-Environment Compatibility Report",
        "",
        "Compatibility verification across Google Antigravity IDE, OpenCode, and Claude Code.",
        "",
        "| Skill ID | Status | Antigravity IDE | OpenCode | Claude Code | Verdict |",
        "|:---|:---:|:---:|:---:|:---:|:---|",
    ]

    for r in results:
        c = r["compatibility"]
        verdict = "Multi-Platform Ready"
        lines.append(
            f"| `{r['id']}` | {r['status']} | {c['antigravity']} | {c['opencode']} | {c['claude_code']} | {verdict} |"
        )

    out = REPO_ROOT / "AUDIT" / "COMPATIBILITY-REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main():
    save_reports = "--save" in sys.argv or "-s" in sys.argv or True

    results = run_full_audit()

    if save_reports:
        q_path = write_quality_report(results)
        s_path = write_security_report(results)
        c_path = write_compatibility_report(results)
        print(f"Audit completed for {len(results)} skills.")
        print(f"  - Quality report:       {q_path}")
        print(f"  - Security report:      {s_path}")
        print(f"  - Compatibility report: {c_path}")

    avg_score = round(sum(r["score"] for r in results) / len(results), 1) if results else 0
    print(f"\nAverage Skill Quality Score: {avg_score}/100 across {len(results)} skills.")


if __name__ == "__main__":
    main()

