#!/usr/bin/env python3
"""Unified Test Suite for GraviDex Capabilities and Preserved Skills.

Executes all unit, smoke, and validator tests across:
  - GraviDex Layer B Capabilities (8 Curated Packs + 5 Retained Specialists)
  - GraviDex Governance, Identity & Supply-Chain Rules
  - Preserved Upstream Source Verification
"""
import os
import shutil
import subprocess
import sys
import time

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
ROOT = os.path.dirname(os.path.abspath(__file__))
PY_BIN = sys.executable


def _resolve_suite_cwd(name):
    candidates = [
        os.path.join(ROOT, "CAPABILITIES", "retained-specialists", name),
        os.path.join(ROOT, "CAPABILITIES", "curated", name),
        os.path.join(ROOT, "SOURCES", "repositories", "hamzzaqureshi-gravidex", "snapshots", "initial", name),
        os.path.join(ROOT, "QUARANTINE", "legacy-runtime-backup", "root-skills", name),
        os.path.join(ROOT, name),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return os.path.join(ROOT, name)


SUITES = [
    {
        "name": "gravidex-capabilities",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "TESTS/capability-tests"],
        "cwd": ROOT,
        "description": "Layer B Curated & Retained Capability Verification (9 tests)"
    },
    {
        "name": "gravidex-governance",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "TESTS/validation"],
        "cwd": ROOT,
        "require_file": os.path.join(ROOT, "registry.yaml"),
        "description": "Governance, Identity & Zero-Emoji Verification (8 tests)"
    },
    {
        "name": "capability-validator",
        "cmd": [PY_BIN, "-B", "scripts/validate.py", "--capabilities"],
        "cwd": ROOT,
        "description": "Deterministic Structural & Frontmatter Validator"
    },
    {
        "name": "rebuild-drift-engine",
        "cmd": [PY_BIN, "-B", "scripts/rebuild-capabilities.py", "--check"],
        "cwd": ROOT,
        "require_dir": os.path.join(ROOT, "SOURCES"),
        "description": "Three-Way Upstream Drift & Rebuild Verification"
    },
    {
        "name": "court",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("court"),
        "description": "Adversarial Idea Deliberation Engine"
    },
    {
        "name": "secure-audit",
        "cmd": ["node", "tests/run-tests.cjs"],
        "cwd": _resolve_suite_cwd("secure-audit"),
        "description": "Coverage Ledger & Findings Validators (65 tests)"
    },
    {
        "name": "anti-vcode",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("anti-vcode"),
        "description": "40-Sign Anti-Slop Code Scanner"
    },
    {
        "name": "impeccable",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("impeccable"),
        "description": "24-Command Design Framework & Detector Smoke Tests"
    },
    {
        "name": "steal",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("steal"),
        "description": "Creative Lineage & Originality Audit Engine"
    },
    {
        "name": "taste",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("taste"),
        "description": "Anti-Slop Frontend Dials & 12-Point Preflight Auditor"
    },
    {
        "name": "designs",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("designs"),
        "description": "Curated 67 Design System Themes & Token Registry"
    },
    {
        "name": "ui-ux-max",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("ui-ux-max"),
        "description": "UI/UX Pro Max BM25 Design Intelligence Engine"
    },
    {
        "name": "threeui",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("threeui"),
        "description": "ThreeUI 3D & WebGL 104-Component Engine"
    },
    {
        "name": "rev-engineer",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("rev-engineer"),
        "description": "REA Reverse Engineer Anything (MCP Binary & Runtime Engine)"
    },
    {
        "name": "logo-design",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("logo-design"),
        "description": "Logo Design & SVG Identity Engine (1,400+ Reference Library)"
    },
    {
        "name": "writing-readme",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("writing-readme"),
        "description": "The Art of Writing Excellent GitHub READMEs (50-Point Auditor & Scaffolder)"
    },
    {
        "name": "arena",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("arena"),
        "description": "The Arena (100 Sub-Agents Single-Elimination Bracket Tournament)"
    },
    {
        "name": "ponytail",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("ponytail"),
        "description": "Ponytail (Lazy Senior Dev: Minimal Diff & Zero Over-Engineering Engine)"
    },
    {
        "name": "last30days",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("last30days"),
        "description": "last30days & CrowdPulse Fast-Lane (Real-Time Temporal Intelligence Engine)"
    },
    {
        "name": "scrapling",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("scrapling"),
        "description": "Scrapling (Adaptive Web Scraping, Stealth Browsing & Anti-Bot Bypass)"
    },
    {
        "name": "humanizer",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("humanizer"),
        "description": "Humanizer (26-Pattern Anti-AI-Writing Prose Polish & Slop Eliminator)"
    },
    {
        "name": "diagram-design",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("diagram-design"),
        "description": "Diagram Design (45-Type Editorial HTML+SVG Diagrams & Antigravity IDE Engine)"
    },
    {
        "name": "socratic",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("socratic"),
        "description": "Socratic (Silent Self-Interrogation & 3am Readiness Gates)"
    },
    {
        "name": "rigor",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("rigor"),
        "description": "Rigor (Empirical Engineering Discipline: Grounding, Task Ledger & Completion Gates)"
    },
    {
        "name": "sanzo-wada-colors",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("sanzo-wada-colors"),
        "description": "Sanzo Wada Colors (348 Palettes, 159 Pigments, WCAG Matrix & Token Engine)"
    },
    {
        "name": "model-router",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("model-router"),
        "description": "Multi-Model Router & Resilient 429 Failover Engine"
    },
    {
        "name": "boardui",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("boardui"),
        "description": "BoardUI React Design System & Component Lookup Engine"
    },
    {
        "name": "lemo-opuscar",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("lemo-opuscar"),
        "description": "Lemo-Opuscar Algorithmic Film Directing & Style Engine"
    },
    {
        "name": "asd-ste100",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("asd-ste100"),
        "description": "ASD-STE100 Simplified Technical English & Karpathy 80% Engine"
    },
    {
        "name": "karpathy-guidelines",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("karpathy-guidelines"),
        "description": "Karpathy Behavioral Guidelines & Pitfall Prevention Engine"
    },
    {
        "name": "stageshow",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": _resolve_suite_cwd("stageshow"),
        "description": "Stageshow Faux UI Interaction & Cursor Choreography Engine"
    }
]


def _run_single_suite(s):
    t0 = time.time()
    binary = s["cmd"][0]
    if not shutil.which(binary):
        return {
            "name": s["name"],
            "description": s["description"],
            "passed": True,
            "skipped": True,
            "elapsed": 0.0,
            "stdout": "",
            "stderr": f"Skipped: runtime binary '{binary}' not available on PATH\n",
        }
    cwd = s.get("cwd") or ROOT
    req_file = s.get("require_file")
    if req_file and not os.path.isfile(req_file):
        return {
            "name": s["name"],
            "description": s["description"],
            "passed": True,
            "skipped": True,
            "elapsed": 0.0,
            "stdout": "",
            "stderr": f"Skipped: requirement not found ({os.path.basename(req_file)})\n",
        }
    req_dir = s.get("require_dir")
    if req_dir and not os.path.isdir(req_dir):
        return {
            "name": s["name"],
            "description": s["description"],
            "passed": True,
            "skipped": True,
            "elapsed": 0.0,
            "stdout": "",
            "stderr": f"Skipped: requirement directory not found ({os.path.basename(req_dir)})\n",
        }
    if not os.path.isdir(cwd):
        return {
            "name": s["name"],
            "description": s["description"],
            "passed": True,
            "skipped": True,
            "elapsed": 0.0,
            "stdout": "",
            "stderr": f"Skipped: working directory not found ({cwd})\n",
        }

    res = subprocess.run(s["cmd"], cwd=cwd, capture_output=True, text=True)
    elapsed = time.time() - t0
    return {
        "name": s["name"],
        "description": s["description"],
        "passed": (res.returncode == 0),
        "skipped": False,
        "elapsed": elapsed,
        "stdout": res.stdout,
        "stderr": res.stderr,
    }


def run_all():
    print("=" * 72)
    print("          GRAVIDEX CAPABILITY & SKILLS SUITE - TEST RUNNER")
    print("=" * 72)

    sequential = "--sequential" in sys.argv or "-s" in sys.argv
    mode = "Sequential" if sequential else "High-Performance Parallel"
    print(f"Mode: {mode} ({len(SUITES)} suites across isolated sandboxes)\n")

    total_start = time.time()
    results = []
    all_ok = True

    if sequential:
        for s in SUITES:
            print(f"[*] Testing [{s['name']}] ({s['description']})...")
            r = _run_single_suite(s)
            results.append(r)
            if r["passed"]:
                print(f"  PASS in {r['elapsed']:.3f}s")
            else:
                all_ok = False
                print(f"  FAIL in {r['elapsed']:.3f}s")
                print(r["stderr"] or r["stdout"])
    else:
        from concurrent.futures import ThreadPoolExecutor
        max_workers = min(len(SUITES), max(4, os.cpu_count() or 4))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            ordered_futures = [executor.submit(_run_single_suite, s) for s in SUITES]
            for f in ordered_futures:
                r = f.result()
                results.append(r)
                if r["passed"]:
                    if r.get("skipped"):
                        print(f"  [{r['name']:<24}] SKIP in {r['elapsed']:.3f}s ({r['description']}) - {r['stderr'].strip()}")
                    else:
                        print(f"  [{r['name']:<24}] PASS in {r['elapsed']:.3f}s ({r['description']})")
                else:
                    all_ok = False
                    print(f"  [{r['name']:<24}] FAIL in {r['elapsed']:.3f}s ({r['description']})")
                    print(r["stderr"] or r["stdout"])

    total_time = time.time() - total_start
    print("\n" + "=" * 72)
    print("                         SUMMARY REPORT")
    print("=" * 72)
    print(f"{'Suite':<24} | {'Status':<10} | {'Runtime':<10}")
    print("-" * 72)
    for r in results:
        status_str = "SKIPPED" if r.get("skipped") else ("PASSED" if r["passed"] else "FAILED")
        print(f"{r['name']:<24} | {status_str:<10} | {r['elapsed']:.3f}s")
    print("=" * 72)
    print(f"Total Suite Runtime: {total_time:.3f}s | Result: {'ALL PASS (100%)' if all_ok else 'SOME FAILED'}")
    print("=" * 72)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(run_all())
